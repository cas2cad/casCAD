from copy import deepcopy
from .constant import *


class Agent:
    def __init__(self, unique_id: int, states: dict, belief, system):
        """
        states = {
            'DUET': 0,
            'USDT': 0,
            'ZUSD': 0,
            'ZBTC': 0,
            'ZNAS': 0,

        }
        """
        self.unique_id = unique_id
        self.states = states
        self.states[ACTION] = []
        self.states_hist = []
        self.belief = belief
        self.desire = None
        self.intent = None
        self.system = system
        self.state = 0  # 0 for init agent, 1 for runing, -1 for quit
        self.farm_reward = 0
        self.last_gen = {
            DUET : 0,
            USDT : 0,
            ZUSD : 0,
            ZBTC: 0,
            ZNAS: 0
        } # this is used when the action amount refer to last, means use the last operation genreated amounts

        self.unit_cost = {
            DUET: -1,
            USDT: -1,
            ZUSD: -1,
            ZBTC: -1,
            ZNAS: -1
        }

        # for some random action, we random number below this, take action
        self.action_dice = 0.05
        self.focus_model = None


        # for bearish and bullish
        self.flag = True
        self.flag_step = 0 # after how long time, this bullish will trade again

        # for minium USDT or DUET trading amount
        self.mini_amount = 10
        self.mini_amount_usdt = self.mini_amount
        self.start_point = 5

        self.invest_value = self.states[USDT] + self.states[DUET] * self.start_point
        # for simulate concurrent
        # self.atom_actions = [('observe and think', (self.step, []))] 
        # self.init_atom_actions()
        self.farm_flag = True

        self.tax_accept = 1 # how much tax can this agent accept

        self.accept_no_reward = False
