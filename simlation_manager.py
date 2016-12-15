#!/usr/env/bin python3
from gazebo_msgs.msg import LinkStates
from control_msgs.msg import JointControllerState
from service_caller import service_caller

from list_pub_sub import async_subscriber,list_publisher,list_subscriber
from clock import clock_manager

class simulation_manager(object):
    def __init__(self,joint_names):
        self.delta_time = clock_manager()

        self.joint_states = list_subscriber([name+'/state' for name in joint_names],JointControllerState)
        self.joint_commands = list_publisher([name+'/command' for name in joint_names])
        self.link_states = async_subscriber('/gazebo/link_states',LinkStates)
    def __call__(self,action):
        pass
    def reset(self):
