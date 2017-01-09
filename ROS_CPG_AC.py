#!/usr/bin/env python2

from publisher import joint_publisher
from subscribers import list_subscriber,JointState_subscriber,ImuState_subscriber

class input_integrater(list_subscriber):
    def __init__(self,jointstate_name,imu_names):
        super(input_integrater,self).__init__([JointState_subscriber(jointstate_name),ImuState_subscriber(imu_names)])

import numpy as np
from cpg_actor_critic import cpg_actor_critic
from service_caller import service_caller
class ROS_CPG_AC(object):
    def __init__(self,def_A,jointstate,imus,jointcommands):
        self.input = input_integrater(jointstate,imus)
        self.output = joint_publisher(jointcommands)

        self.reward_index = len(jointcommands)*3 + 2

        i,o = len(jointcommands)*3+len(imus)*9, len(jointcommands)
        self.cpg_ac = cpg_actor_critic((i,o),def_A(o))

        #service caller
        self.gazebo_reset = service_caller('/gazebo/reset_simulation')
        self.pause_physics = service_caller('/gazebo/pause_physics')
        self.unpause_physics = service_caller('/gazebo/unpause_physics')

    def __call__(self,dt):
        state = self.input.get_msg()
        print len(state)
        print state

        r = self.reward(state)

        print 'ROS_CPG_AC\n',self.cpg_ac(np.array([state]),r,dt),'ROS_CPG_AC'
        self.output.put_msg(self.cpg_ac(np.array([state]),r,dt)[0])

        return r

    def reward(self,state):
        """
        R^n -> R
        """
        return state[self.reward_index]-0.1

    def reset(self):
        self.pause_physics()
        self.gazebo_reset()
        self.unpause_physics()

print 'ros_cpg_accccccccccccccccccccccccccccccccccccccccccccccc'
if __name__ == '__main__':
#if __name__ == 'ros_cpg_ac':

#init node
    import rospy
    rospy.init_node('ROS_CPG_AC')
#make ROS_CPG_AC
    #make joint_names,imu_sensor_names
    from grep_command import grep_command
    joint_names = grep_command('rostopic list','/command').split('\n')[:-1]
    imu_names = grep_command('rostopic list','/imu').split('\n')[:-1]
    joint_states = grep_command('rostopic list','/joint_states').split('\n')[0]

    import numpy as np
    def def_A(o):
        A = np.random.normal(np.zeros((o,o)),np.ones((o,o)))*np.tri(o)
        return A+A.T
    roscpgac = ROS_CPG_AC(def_A,joint_states,imu_names,joint_names)

#make clock_manager
    from clock import clock_manager
    c = clock_manager(roscpgac,0.05)
    while 1:
        c()
        rospy.sleep(0.01)
