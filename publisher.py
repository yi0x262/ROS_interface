#!/usr/bin/env python2
import rospy
from abc import ABCMeta,abstractmethod

#class list_publisher(list,metaclass=ABCMeta):#3
class list_publisher(list,object):
    __metaclass__=ABCMeta
    def __init__(self,msgnames,msgtype,queue_size=10):
        super(list_publisher,self).__init__([rospy.Publisher(name,msgtype,queue_size=queue_size) for name in msgnames])
    @abstractmethod
    def put_msg(self,data):
        pass

from std_msgs.msg import Float64
class joint_publisher(list_publisher,object):
    def __init__(self,msgnames,queue_size=10):
        super(joint_publisher,self).__init__(msgnames,Float64,queue_size=queue_size)
    def put_msg(self,data):
        #check
        assert len(self) == len(data),'in list_pub : |self|!=|data| ({}!={})'.format(len(self),len(data))
        try:
            float(data[0])
        except TypeError:
            raise TypeError('in joint_pub : data is not flatten')
        except IndexError:
            raise IndexError('in joint_pub : data is not capable')
        #publish
        for pub,datum in zip(self,data):
            print 'pub {} as {}'.format(datum,str(pub))
            print Float64(datum)
            pub.publish(Float64(datum))

if __name__ == '__main__':
    rospy.init_node('publisher_test')
    jp = joint_publisher(['a','b','c'],queue_size=0)
    for i in range(30):
        print i
        jp.put_msg([0.1,0.2,0.3])
        rospy.sleep(1.)
    #jp.put_msg([0.1,0.2,0.3,0.4])
    rospy.spin()
