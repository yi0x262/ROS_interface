#!/usr/env/bin python3

import rospy
from std_msgs.msg import Float64,Float32MultiArray

class list_publisher(list):
    def __init__(self,names,queue=10):
        for name in names:
            self.append(rospy.Publisher(name,Float64,queue_size=queue))
    def __call__(self,data):
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

class list_subscriber(list):
    def __init__(self,names,datatype):
        for name in names:
            ig = InfoGetter()
            self.append(ig)
            rospy.Subscriber(name,datatype,ig)
    def __call__(self):
        data = []
        for sub in self:
            d = sub.get_msg()
            if d is None:
                raise RuntimeError('in list_subscriber : yet receive msg')
            data.append(d)
        return data
