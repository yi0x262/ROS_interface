from xml.etree import ElementTree

def urdf_reader(path):
    etree = ElementTree.parse(path)
    ret = list()
    for plugin in etree.getroot().findall('.//plugin'):
        if plugin.attrib['name'] != 'gazebo_ros_imu':
            continue
        topicname = plugin.find('topicName').text
        ret.append(topicname)
    return ret

import yaml
class config_reader(dict):
    def __init__(self,path,*args,**keys):
        super().__init__(self,*args,**keys)
        with open(path,'r') as f:
            self.update(yaml.load(f))
    def robotname(self):
        return list(self.keys())[0]
    def jointnames(self):
        ret = list()
        for data in self[self.robotname()].items():
            if data[1]['type'] == 'joint_state_controller/JointStateController':
                continue
            ret.append(data[0])
        return ret

if __name__ == '__main__':
    import sys

    cr = config_reader(sys.argv[1])
    print(yaml.dump(cr))
    print(cr.robotname())
    print(cr.jointnames())

    print(urdf_reader(sys.argv[2]))
