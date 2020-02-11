from ddpg_agent import Agent
import numpy as np

class MultiAgent():
    def __init__(self, n_agents, args):
        self.agents = [Agent(*args) for _ in range(n_agents)]
        self.same_agent_b = False
        
    def act(self, states):
        if not self.same_agent_b:
            return [agent.act(np.asarray([states[i]])) for i, agent in enumerate(self.agents)]
        else:
            return [self.agents[0].act(np.asarray([states[i]])) for i in range(len(self.agents))]
    
    def separate_memory(self, states, actions, rewards, next_states, dones):
        m_args = list(zip(states, actions, rewards, next_states, dones))
        assert len(self.agents) == len(m_args), "separate_memory() - \
agents number is different than arguments dimension"
        [self.agents[i].step(*args) for i, args in enumerate(m_args)]
        
    def common_memory(self, states, actions, rewards, next_states, dones):
        m_args = list(zip(states, actions, rewards, next_states, dones))
        assert len(self.agents) == len(m_args), "common_memory() - \
agents number is different than arguments dimension"
        for i in range(len(self.agents)):
            for j in range(len(m_args)):
                self.agents[i].step(*(m_args[j]), learn = True if j==0 else False)
        
    def same_agent(self, states, actions, rewards, next_states, dones):
        m_args = list(zip(states, actions, rewards, next_states, dones))
        assert len(self.agents) == len(m_args), "common_memory() - \
agents number is different than arguments dimension"
        for j in range(len(m_args)):
            self.agents[0].step(*(m_args[j]), learn = True if j==0 else False)
    
    
    def step(self, states, actions, rewards, next_states, dones):
        self.common_memory(states, actions, rewards, next_states, dones)
       
    def reset(self):
        [agent.noise.reset() for agent in self.agents]
        