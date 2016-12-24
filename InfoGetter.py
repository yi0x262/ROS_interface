#from answers.ros.org/question/215813
#how-to-return-an-array-from-my-subscriber-function

#add set_None
import rospy
import threading
class InfoGetter(object):
    """support to rospy.Subscriber, whenever&wherever can read subscribed msg"""
    def __init__(self):
        #event that will block until the info is received
        self._event = threading.Event()
        #attribute for storing the rx'd message
        self._msg = None
    def __call__(self,msg):
        #Uses __call__ so the object itself acts as the callback
        #save the data, trigger the event
        self._msg = msg
        self._event.set()
    def get_msg(self,timeout=None):
        """Blocks until the data is rx'd with optional timeout. Returns the received message"""
        self._event.wait(timeout)
        if self._msg is None:
            rospy.logwarn('Not receive any msg yet')
            raise RuntimeError('Not receive any msg yet')
        return self._msg
    def reset(self):
        self._msg = None

if __name__ == '__main__':
    import rospy
    from std_msgs.msg import Int64
    ig = InfoGetter()
    rospy.Subscriber('test',Int64,ig)
    rospy.init_node('tesset')
    print ig.get_msg()
