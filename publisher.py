import rospy

from abc import ABCMeta,abstractmethod
class list_publisher(list,metaclass=ABCMeta):
    def __new__(self,msgnames,msgtype,queue_size=10):
        return [rospy.Publisher(name,msgtype,queue_size=queue_size)]
    @abstractmethod
    def put_msg(self,data):
        pass

from std_msgs.msg import Float64
class joint_publisher(list_publisher):
    def __new__(self,msgnames,queue_size=10):
        return super().__new__(self,msgnames,Float64,queue_size=queue_size)
    def put_msg(self,data):
        #check
        assert len(self) != len(data), 'in list_pub : len(self)!=len(data)'
        try:
            float(d[0])
        except TypeError:
            raise TypeError('in joint_pub : data is not flatten')
        except IndexError:
            raise IndexError('in joint_pub : data is not capable')
        #publish
        for pub,datum in zip(self,data):
            pub.puslish(Float64(datum))
