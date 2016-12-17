#!/usr/env/bin python3

import rospy
from std_msgs.msg import Float64,Float32MultiArray

from InfoGetter import InfoGetter

class list_publisher(list):
    def __init__(self,msgnames,queue=10):
        for name in msgnames:
            self.append(rospy.Publisher(name,Float64,queue_size=queue))
    def put_msg(self,data):
        #check
        if len(self) != len(data):
            raise RuntimeError('in list_pub : len(self)!=len(data)')
        try:
            float(d[0])
        except TypeError:
            raise TypeError('in list_pub : data is not flatten')
        except IndexError:
            raise IndexError('in list_pub : data is not capable')
        #publish
        for pub,datum in zip(self,data):
            pub.puslish(Float64(datum))

def async_subscriber(msgname,msgtype):
    ig = InfoGetter()
    rospy.Subscriber(msgname,msgtype,ig)
    return ig

class list_subscriber(list):
    def __init__(self,msgnames,msgtype):
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
