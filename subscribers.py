#all class's get_msg() return not-nested list
from InfoGetter import InfoGetter

from control_msgs.msg import JointControllerState
class JointState_subscriber(InfoGetter):
    def __init__(self,msgname):
        super().__init__(self,msgname,JointControllerState)
    def get_msg(self):
        data = super().get_msg()
        ret = list()
        ret.extend(data['position'])
        ret.extend(data['velocity'])
        ret.extend(data['effort'])
        return ret

def get_xyz(dictionary):
    return [dictionary['x'],dictionary['y'],dictionary['z']]

from sensor_msgs.msg import Imu
class imu_states(InfoGetter):
    def __init__(self,msgname):
        super().__init__(self,msgname,Imu)
    def get_msg(self):
        data = super().get_msg()
        ret = list()
        ret.extend(get_xyz(data['orientation']))
        ret.extend(get_xyz(data['angular_velocity']))
        ret.extend(get_xyz(data['linear_acceleration']))
        return ret

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
