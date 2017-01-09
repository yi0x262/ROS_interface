#!/usr/bin/env python2
#all class's get_msg() return not-nested list

import rospy

from InfoGetter import InfoGetter
class subscriber(InfoGetter,object):
    def __init__(self,msgname,msgtype):
        super(subscriber,self).__init__()
        rospy.Subscriber(msgname,msgtype,self)

#from control_msgs.msg import JointControllerState
from sensor_msgs.msg import JointState
class JointState_subscriber(subscriber,object):
    def __init__(self,msgname):
        super(JointState_subscriber,self).__init__(msgname,JointState)
    def get_msg(self):
        data = super(JointState_subscriber,self).get_msg()
        return data.position + data.velocity + data.effort

def get_xyz(d):
    return [d.x,d.y,d.z]

from sensor_msgs.msg import Imu
class imu_states(subscriber):
    def __init__(self,msgname):
        super(imu_states,self).__init__(msgname,Imu)
    def get_msg(self):
        data = super(imu_states,self).get_msg()
        ori_pos = get_xyz(data.orientation)
        ang_vel = get_xyz(data.angular_velocity)
        lin_acc = get_xyz(data.linear_acceleration)
        return ori_pos + ang_vel + lin_acc

class list_subscriber(list):
    def __init__(self,msgnames,info_class):
        super(list_subscriber,self).__init__([info_class(name) for name in msgnames])
    def get_msg(self):
        ret = list()
        for sub in self:
            data = sub.get_msg()
            assert data is not None, AssertionError('in list_subscriber : not receive msg yet')
            #if data is None:
            #   return None
            ret.extend(data)
        return ret
    def reset(self):
        for i in range(len(self)):
            self[i].reset()

class ImuState_subscriber(list_subscriber):
    def __init__(self,msgnames):
        super(ImuState_subscriber,self).__init__(msgnames,imu_states)



if __name__ == '__main__':
    print 'p'
    rospy.init_node('subscriber_test')
    from grep_command import grep_command

    #joint_states
    joint_state_name = grep_command('rostopic list','/joint_states').split('\n')[0]
    print joint_state_name
    assert len(joint_state_name) != 0,AssertionError('in __main__ : no joint_state')
    js = JointState_subscriber(joint_state_name,)
    for t in range(0):
        print 'time',t
        print js.get_msg()
        rospy.sleep(1.)

    imu_names = grep_command('rostopic list','/imu').split('\n')[:-1]
    print imu_names
    imu_s = ImuState_subscriber(imu_names)
    for t in range(1000):
        print 'time',t
        print imu_s.get_msg()
        rospy.sleep(0.01)

    rospy.spin()
