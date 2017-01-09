#manage gazebo simulator's clock
import rospy

class clock_manager(object):
    def __init__(self,func,threshold):
        self.clock = clock_getter()
        self.threshold = threshold
        self.func = func


    def __call__(self):
        dt = self.clock.get_msg()
        if dt < self.threshold:
            return

        r = self.func(dt)
        if r < 0:
            self.reset()

    def reset(self):
        self.func.reset()
        self.clock.reset()

from InfoGetter import InfoGetter
from rosgraph_msgs.msg import Clock

class clock_getter(InfoGetter,object):
    def __init__(self):
        super(clock_getter,self).__init__()
        rospy.Subscriber('/clock',Clock,super(clock_getter,self).__call__)
        self.reset()
    def get_msg(self):
        now = super(clock_getter,self).get_msg().clock
        now = self.clock2float(now)
        print 'clock,now:',now
        dt = now - self.lasttime
        self.lasttime = now
        return dt
    def reset(self):
        self.lasttime = self.clock2float(super(clock_getter,self).get_msg().clock)
    def clock2float(self,clock):
        return clock.secs + 10e-9*clock.nsecs
