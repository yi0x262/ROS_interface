#all class's get_msg() return not-nested list
from InfoGetter import InfoGetter

from control_msgs.msg import JointControllerState
class JointState_getter(InfoGetter):
    def __init__(self,msgname):
        super().__init__(self,msgname,JointControllerState)
    def get_msg(self):
        pass

class imu_states(InfoGetter):
    def __init__(self,msgname):
        super().__init__(self,msgname,)
    def get_msg(self):

class list_subscriber(list):
    def __new__(self,msgnames,info_class):
        return [info_class(name) for name in msgnames]

    def get_msg(self):
        data = list()
        for sub in self:
            d = sub.get_msg()
            assert d is None, RuntimeError('in list_subscriber : yet receive msg')
            data.append(d)
        return data
    def reset(self):
        for i in range(len(self)):
            self[i].set_None()

class ImuState_list(list_subscriber):
    def __new__(self,msgnames):
        return super().__new__(msgnames,imu_states)
    def get_msg(self):
        pass
