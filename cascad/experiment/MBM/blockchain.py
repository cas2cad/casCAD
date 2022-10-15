import random

from numpy import mat
from .constant import FARM, FRAMWITHDRAW, MINT1, REDEEM, STAKE, STAKEWITHDRAW, SWAP1, TOTALTRAD, TRADS
from copy import deepcopy
import math

class BlockChain:
    def __init__(self, drop_prob=0.03, turn_on = False):
        self.states = {
            TOTALTRAD : 0,
            TRADS: []
        }
        # self.transactions = []
        self.drop_prop = drop_prob
        self.turn_on = turn_on
        self.history = []

    def submit(self, from_agent, to_agent, action, amount1=None, amount2=None, result1=None, reuslt2=None):
        self.states[TRADS].append(
            (from_agent, to_agent, action, amount1, amount2, result1, reuslt2)
        )
        self.states[TOTALTRAD] += 1
        return self.get_fee(action)


    def set_turn_on(self):
        self.turn_on = True

    def set_turn_off(self):
        self.turn_on = False

    def get_fee(self, _type):
        if not self.turn_on:
            return True

        trade = self.states[TOTALTRAD]
        fee = random.random() * trade 
        fee = math.log10(fee + 1.1)/(math.log10(fee + 1.1) + 1)
        GWEIS = {
            MINT1: 30,
            REDEEM: 30,
            SWAP1: 41, # 10,
            FARM: 33,
            STAKE: 42,
            FRAMWITHDRAW: 30, # unverified
            STAKEWITHDRAW: 30,
        }

        fee = GWEIS[_type] * fee

        return fee

    def step(self):
        states = deepcopy(self.states)
        self.history.append(states)
        self.states[TOTALTRAD] = 0
        self.states[TRADS] = []
