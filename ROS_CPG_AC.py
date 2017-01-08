#!/usr/bin/env python2

from publisher import joint_publisher
from subscribers import list_subscriber,JointState_subscriber,ImuState_subscriber

class input_integrater(list_subscriber):
    def __new__(self,jointstate_name,imu_names):
        return [JointState_subscriber(jointstate_name),ImuState_subscriber(imu_names)]

import numpy as np
from cpg_actor_critic import cpg_actor_critic
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
    from grep_command import grep_command
    joint_names = grep_command('rostopic list','/command').split('\n')
    imu_names = grep_command('rostopic list','/imu').split('\n')
    joint_states = grep_command('rostopic list','/joint_states').split('\n')[0]

    import numpy as np
    def def_A(o):
        return np.random.normal((o,o))
    roscpgac = ROS_CPG_AC(def_A,joint_states,imu_names,joint_names)
    #make clock_manager
    from clock import clock_manager
    c = clock_manager()
