#!/usr/env/bin python3
import rospy
from control_msgs.msg import JointControllerState
from
from service_caller import service_caller

from clock import clock_manager
from service_caller import service_caller

class simulation_manager(object):
    def __init__(self,func,node_name,joint_names,sensor_names,sensor_types):
        rospy.init_node(node_name)

        self.clock_manager = clock_manager(func)

        self.joint_states = list_subscriber([name+'/state' for name in joint_names],JointControllerState)
        self.joint_commands = list_publisher([name+'/command' for name in joint_names])
        #self.link_states = async_subscriber('/gazebo/link_states',LinkStates)
        self.sensor_states = imu_states(sensor_names,sensor_types)

    def get_msg(self):
        data = list()
        data.extend(self.joint_states.get_msg())
        #data.extend(self.link_states.get_msg())
        data.extend(self.sensor_states.get_msg())

    def reset(self):
        #reset simulation
        service_caller('/gazebo/pause_physics')()
        service_caller('/gazebo/reset_simulation')()

        #reset timer
        self.clock_manager.reset()
        #reset subscribers
        self.joint_states.reset()
        #self.link_states.set_None()

        #restart simulation
        service_caller('/gazebo/unpause_physics')()
