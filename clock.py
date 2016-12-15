#manage gazebo simulator's clock
import rospy
from rosgraph_msgs.msg import Clock

from InfoGetter import InfoGetter

class clock_manager(object):
    def __init__(self):
        self.lasttime = 0.
        self.clock = InfoGetter()
        rospy.Subscriber('/clock',Clock,self.clock)
    def __call__(self):
        now = self.clock.get_msg()
        dt = now - self.lasttime
        self.lasttime = now
        return dt
    def reset(self):
        self.lasttime = 0

class clock_manager2(InfoGetter):
    def __init__(self):
        self.lasttime = 0
        rospy.Subscriber('/clock',Clock,super().__call__)
    def __call__(self):
        now = self.get_msg()
        dt = now - self.lasttime
        self.lasttime = now
        return dt
    def reset(self):
        self.lasttime = 0
