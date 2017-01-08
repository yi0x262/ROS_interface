#all class's get_msg() return not-nested list
import rospy
from InfoGetter import InfoGetter

class subscriber(InfoGetter,object):
    def __init__(self,msgname,msgtype):
        super(subscriber,self).__init__()
        rospy.Subscriber(msgname,msgtype,self)


from control_msgs.msg import JointControllerState
class JointState_subscriber(subscriber,object):
    def __init__(self,msgname):
        super(JointState_subscriber,self).__init__(msgname,JointControllerState)
    def get_msg(self):
        data = super(JointState_subscriber,self).get_msg()
        return [*data['position'],*data['velocity'],*data['effort']]

def get_xyz(dictionary):
    return [dictionary['x'],dictionary['y'],dictionary['z']]

from sensor_msgs.msg import Imu
class imu_states(subscriber):
    def __init__(self,msgname):
        super(imu_states,self).__init__(self,msgname,Imu)
    def get_msg(self):
        data = super(imu_states,self).get_msg()
        ori = get_xyz(data['orientation'])
        ang = get_xyz(data['angular_velocity'])
        lin = get_xyz(data['linear_acceleration'])
        return list(*ori,*ang,*lin)

class list_subscriber(list):
    def __new__(self,msgnames,info_class):
        return [info_class(name) for name in msgnames]
    def get_msg(self):
        ret = list()
        for sub in self:
            data = sub.get_msg()
            assert data is None, RuntimeError('in list_subscriber : not receive msg yet')
            ret.extend(d)
        return ret
    def reset(self):
        for i in range(len(self)):
            self[i].reset()

class ImuState_subscriber(list_subscriber):
    def __new__(self,msgnames):
        return super().__new__(msgnames,imu_states)
