#manage gazebo simulator's clock
import rospy
from rosgraph_msgs.msg import Clock

from InfoGetter import InfoGetter

class clock_manager(object):
    def __init__(self,func,threshold):
        self.clock = clock_getter()
        self.threshold = threshold
        self.func = func

    def __call__(self):
        dt = self.clock.get_msg()
        if dt < self.threshold:
            return

        self.func(dt)

    def reset(self):
        self.func.reset()
        self.clock.reset()

class clock_getter(InfoGetter):
    def __init__(self):
        self.lasttime = 0
        rospy.Subscriber('/clock',Clock,super().__call__)
    def get_msg(self):
        now = self.get_msg()
        dt = now - self.lasttime
        self.lasttime = now
        return dt
    def reset(self):
        self.lasttime = 0
