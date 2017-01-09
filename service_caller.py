import rospy
import std_srvs.srv

class service_caller(rospy.ServiceProxy):
    def __new__(self,service_name,service_type=std_srvs.srv._Empty.Empty):
        return super().__new__(self,service_name,service_type)
