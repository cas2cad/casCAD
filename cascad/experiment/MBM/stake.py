# from aletheia.agents.agent import Agent
# from aletheia.utils.constant import *
from .agent import Agent
from .constant import *
from copy import deepcopy


class Stake(object):
    def __init__(self, states={
        TOTAL: 100,
        STAKE_TOTAL_REWARD: 0,
        STAKE_APR : 1,
        STAKE_APY : 1
    }, ratio=0.1):
        self.states = states
        self.history = []
        self.ratio = ratio
        self.historys = []

    def stake(self, agent: Agent, amount):
        if agent.states[DUET] >= amount:
            self.states[TOTAL] += amount
            agent.states[DUET] -= amount
            agent.states[STAKE] += amount
            return amount

    def withdraw(self, agent: Agent, amount):
        if agent.states[STAKE] >= amount:
            self.states[TOTAL] -= amount
            agent.states[DUET] += amount
            agent.states[STAKE] -= amount
            return amount + 1

    def add_reward(self, amount):
        self.states[STAKE_TOTAL_REWARD] += amount
        
    def step(self):
        if self.history:
            last_state = self.history[-1]
            reward = self.states[STAKE_TOTAL_REWARD] - last_state[STAKE_TOTAL_REWARD] 
            interest_rate = reward/self.states[TOTAL]

            try:
                self.states[STAKE_APR] = interest_rate * 365
                self.states[STAKE_APY] = (1 + interest_rate) ** 365 - 1
            except:
                self.states[STAKE_APY] = 100000000

        state = deepcopy(self.states)
        self.history.append(state)

    def get_apy(self):
        return self.states[STAKE_APY]

    def observe(self):
        return self.states
