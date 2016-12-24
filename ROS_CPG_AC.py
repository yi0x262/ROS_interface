from publisher import joint_publisher
from subscribers import list_subscriber,JointState_subscriber,ImuState_subscriber

class input_integrater(list_subscriber):
    def __new__(self,jointstate_name,imu_names):
        return [JointState_subscriber(jointstate_name),ImuState_subscriber(imu_names)]

import numpy as np
from CPG_Actor_Critic import cpg_actor_critic
class ROS_CPG_AC(object):
    def __init__(self,def_A,jointstate,imus,jointcommands):
        self.input = input_integrater(jointstate,imus)
        self.output = joint_publisher(jointcommands)

        self.reward_index = len(jointcommands)*9 + 2

        i,o = len(jointcommands)*9+len(imus)*9, len(jointcommands)
        self.cpg_ac = cpg_actor_critic((i,o),def_A(o))

    def __call__(self,dt):
        state = self.input()

        r = self.reward(state)
        self.output(self.cpg_ac.action(np.array([state]),r,dt))

        return r

    def reward(self,state):
        """
        R^n -> R
        """
        return state[self.reward_index]

if __name__ == '__main__':
#init node
    import rospy
    rospy.init_node('ROS_CPG_AC')
#make ROS_CPG_AC
    #make joint_names,imu_sensor_names
    import sys
    from config_reader import urdf_reader,config_reader
    cr = config_reader(sys.argv[1])
    joint_commands = ['/{}/{}/command'.format(cr.robotname(),jname) for jname in cr.jointnames()]
    imu_topicnames = urdf_reader(sys.argv[2])
    #init ros_cpg_ac
    import numpy as np
    def def_A(o):
        return np.random.normal((o,o))
    roscpgac = ROS_CPG_AC(def_A,'/{}/joint_states'.format(cr.robotname()),imu_names,joint_names)
    #make clock_manager
    from clock import clock_manager
    c = clock_manager()
