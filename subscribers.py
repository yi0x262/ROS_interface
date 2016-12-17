#all class's get_msg() return not nested list


class state_getter(InfoGetter):
    def __init__(self,msgname,msgtype):
        super().__init__(self)
        rospy.Subscriber(msgname,msgtype,self)

from gazebo_msgs.msg import LinkStates
class link_states(state_getter):
    def __init__(self,msgname):
        super().__init__(self,msgname,LinkStates)
    def extend_xyz(self,*args):
        ret = list()
        for data in args:
            for d in data:
                ret.extend(d.x,d.y,d.z)
        return ret
    def get_msg(self):
        data = super().get_msg()
        #!!!not done!!!

from sensor_msgs.msg import JointState
class joint_states(state_getter):
    def __init__(self,msgname):
        super().__init__(self,msgname,JointState)
    def get_msg(self):
        data = super().get_msg()
        ret = list()
        ret.extend(data.position)
        ret.extend(data.velocity)
        ret.extend(data.effort)
        return ret

class list_subscriber(list):
    def __init__(self,msgnames,classnames):
        if not isinstance(msgtype,(list,tuple)):
            msgtypes = [msgtype for _ in msgnames]
        else:
            msgtypes = msgtype
        for name,mt in zip(msgnames,msgtypes):
            self.append(async_subscriber(name,mt))

    def get_msg(self):
        data = list()
        for sub in self:
            d = sub.get_msg()
            if d is None:
                raise RuntimeError('in list_subscriber : yet receive msg')
            data.append(d)
        return data
    def reset(self):
        for i in range(len(self)):
            self[i].set_None()

class imu_states(list_subscriber):
    def get_msg(self):
