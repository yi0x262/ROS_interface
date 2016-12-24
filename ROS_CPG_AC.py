from publisher import joint_publisher
from subscribers import list_subscriber,JointState_subscriber,ImuState_subscriber

class input_integrater(list_subscriber):
    def __new__(self,jointstate_name,imu_names):
        return [JointState_subscriber(jointstate_name),ImuState_subscriber(imu_names)]

#from CPG_AC import CPG_Actor_Critic
class ROS_CPG_AC(object):
    def __init__(self,jointstate,imus,jointcommands):
        self.input = input_integrater(jointstate,imus)
        self.output = joint_publisher(jointcommands)

        self.reward_index = len(jointcommands)*9 + 2

    def __call__(self,dt):
        state = self.input()

        if not hasattr(self,'cpg_ac'):
            self.cpg_ac = CPG_Actor_Critic((len(state),len(self.output)))

        r = self.reward(state)
        self.output(self.cpg_ac.action(state,r,dt))

        return r

    def reward(self,state):
        return state[self.reward_index]

if __name__ == '__main__':
    from clock import clock_manager
    
