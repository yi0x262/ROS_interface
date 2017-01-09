import rospy
import std_srvs.srv

class service_caller(rospy.ServiceProxy,object):
    def __init__(self,service_name,service_type=std_srvs.srv._Empty.Empty):
        super(service_caller,self).__init__(service_name,service_type)

def service(service_name):
    return rospy.ServiceProxy(service_name,service_type)
