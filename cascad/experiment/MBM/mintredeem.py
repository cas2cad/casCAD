# from aletheia.artificial_system import duet
# from aletheia.artificial_system.oracle import Oracle
# from aletheia.scenario_generator.timeline import TimeLine
from .oracle import Oracle
from cascad.aritificial_world.timeline import TimeLine
from .constant import BURNEDVALUE, EXPECEDMINTRATE, EXPECTEDREDEEMRATE, MINTEDVALUE, TAXRATE, THRESHOLD, TOTALBURNEDVALUE, TOTALMINTEDVALUE, ZUSD, ZBTC, ZNAS, DUET, BURNED, MINTED, TAX, TOTALBURNED, TOTALMINTED
# from aletheia.agents.agent import Agent
# from aletheia.artificial_system.database import Memory
from .memory import Memory
import numpy as np
import math


class MintRedeemModel(object):
    def __init__(self, oracle: Oracle, timeline: TimeLine, db: Memory, 
        states: dict = {
            BURNED: {DUET: 0, ZUSD: 0, ZBTC: 0, ZNAS: 0}, 
            MINTED: {DUET: 0, ZUSD: 0, ZBTC: 0, ZNAS: 0},
            TOTALBURNED: {DUET: 0, ZUSD: 0, ZBTC: 0, ZNAS: 0}, 
            TOTALMINTED: {DUET: 0, ZUSD: 0, ZBTC: 0, ZNAS: 0},
            BURNEDVALUE: {DUET: 0, ZUSD: 0, ZBTC: 0, ZNAS: 0}, 
            MINTEDVALUE: {DUET: 0, ZUSD: 0, ZBTC: 0, ZNAS: 0},
            TOTALBURNEDVALUE: {DUET: 0, ZUSD: 0, ZBTC: 0, ZNAS: 0}, 
            TOTALMINTEDVALUE: {DUET: 0, ZUSD: 0, ZBTC: 0, ZNAS: 0},
            TAX: {DUET: 0, ZUSD: 0, ZBTC: 0, ZNAS: 0},
            EXPECEDMINTRATE:  {ZUSD: 0, ZBTC: 0, ZNAS: 0},
            EXPECTEDREDEEMRATE: { ZUSD: 0, ZBTC: 0, ZNAS: 0},
            TAXRATE: {DUET: 0, ZUSD: 0, ZBTC: 0, ZNAS: 0},
            THRESHOLD : {DUET: 1000000, ZUSD: 100000, ZBTC: 100000, ZNAS: 100000},
            }, a=1000000, uniwap = None, threshold=100000):
        self.oracle = oracle
        self.timeline = timeline
        self.db = db
        self.states = states
        self.db.value[ZUSD] = 0
        self.db.value[ZBTC] = 0
        self.db.value[ZNAS] = 0
        self.a = a
        self.uniswap = uniwap
        self.threshold = threshold

    def mint(self, agent, token: str, amount: float = -1, duet_amount: float = -1):
        """
        mint function
        if duet_amount is provided, compute the amount of target token minted
        else compute the cost with taget minted token
        """
        if amount == -1 and duet_amount == -1:
            return False, False

        token_price = self.oracle.get_price(token)
        # duet_price = self.oracle.get_price(DUET)
        duet_price = self.uniswap.get_current_usdt_price(DUET)
        price = token_price / duet_price
        
        if duet_amount == -1:
            cost = price * amount + self.compute_tax(DUET, price * amount)
        else:
            # amount = duet_amount / price
            # track
            test_duet_amount = duet_amount - self.compute_tax(DUET, duet_amount)
            if test_duet_amount <= 0:
                # print('tax is toooo high')
                duet_amount = duet_amount / 2
            else:
                duet_amount = test_duet_amount
            amount = duet_amount / price
            tax = self.compute_tax(DUET, duet_amount)
            cost = duet_amount + tax

        if cost <= agent.states[DUET]:
            agent.states[DUET] -= cost
            agent.states[token] += amount
            # self.db.value[token] += amount
            self.states[BURNED][DUET] += cost
            self.states[MINTED][token] += amount
            self.states[BURNEDVALUE][DUET] += cost * duet_price
            self.states[MINTEDVALUE][token] += amount * token_price
            self.states[TAX][DUET] += tax * duet_price 
            return amount, tax * duet_price
        else:
            return False, False

    def evaluate_mint(self, token, duet_amount, with_tax = True):
        # price = self.oracle.get_price(token)
        token_price = self.oracle.get_price(token)
        # duet_price = self.oracle.get_price(DUET)
        duet_price = self.uniswap.get_current_usdt_price(DUET)

        price = duet_price / token_price

        # amount = duet_amount / price
        if with_tax:
            cost = self.compute_tax(DUET, duet_amount) #
            amount = (duet_amount - cost) * price # here is just appear solution
            return amount
        else:
            amount =  price* duet_amount
            return amount

    def evaluate_redeem(self, token, amount, with_tax=True):
        # price = self.oracle.get_price(token)
        token_price = self.oracle.get_price(token)
        # duet_price = self.oracle.get_price(DUET)
        duet_price = self.uniswap.get_current_usdt_price(DUET)

        price = token_price /duet_price 

        if with_tax:
            cost = self.compute_tax(token, amount)
            amount = (amount - cost) * price 
            return amount
        else:
            amount = amount * price
            return amount

    def redeem(self, agent, token: str, amount: float):
        '''
        redeem function
        '''
        token_price = self.oracle.get_price(token)
        # duet_price = self.oracle.get_price(DUET)
        duet_price = self.uniswap.get_current_usdt_price(DUET)
        price = token_price / duet_price

        amount = amount - self.compute_tax(token, amount)
        if amount <= 0:
            return 0, 0

        tax = self.compute_tax(token, amount)
        cost = amount + tax

        if cost <= agent.states[token]:
            agent.states[token] -= cost
            agent.states[DUET] += amount*price
            # self.db.value[token] -= cost
            self.states[BURNED][token] += cost
            self.states[MINTED][DUET] += amount * price
            self.states[BURNEDVALUE][token] += cost * token_price
            self.states[MINTEDVALUE][token] += amount * price * duet_price
            self.states[TAX][token] += tax * token_price
            if amount* price == 0:
                return False, False
            return amount*price, tax*token_price
        else:
            return False, False

    def compute_tax(self, token, amount, usdt=True):
        if token == DUET:
            token_price = self.uniswap.get_current_usdt_price(DUET)
        else:
            token_price = self.oracle.get_price(token)

        amount = amount * token_price
        burned = self.states[BURNEDVALUE][token]
        tax = (burned + amount) * 2 * math.atan((burned + amount) / (self.a)) - burned * 2 * math.atan(burned/self.a)
        tax = tax / math.pi
        if tax == 0:
            return 0
        return tax/token_price

    def get_oracle_price(self, token):
        return self.oracle.get_price(token)

    def is_limited(self, token):
        if self.states[MINTED][token] >= self.threshold:
            return True
        else:
            return False

    def step(self):
        for key in self.states[EXPECEDMINTRATE].keys():
            self.states[EXPECEDMINTRATE][key] = self.evaluate_mint(key, 1, with_tax=False)

        for key in self.states[EXPECTEDREDEEMRATE].keys():
            self.states[EXPECTEDREDEEMRATE][key] = self.evaluate_redeem(key, 1, with_tax=False)

        for key in self.states[TAXRATE].keys():
            self.states[TAXRATE][key] = self.compute_tax(key, 1) * self.get_oracle_price(key)

        for key in self.states[BURNED].keys():
            self.states[TOTALBURNED][key] += self.states[BURNED][key]
            self.states[TOTALMINTED][key] += self.states[MINTED][key]
            self.states[TOTALBURNEDVALUE][key] += self.states[BURNEDVALUE][key]
            self.states[TOTALMINTEDVALUE][key] += self.states[MINTEDVALUE][key]

        for key in self.states[BURNED].keys():
            self.states[BURNED][key] = 0
            self.states[MINTED][key] = 0
            self.states[BURNEDVALUE][key] = 0
            self.states[MINTEDVALUE][key] = 0


    def get_tax(self, token):
        return self.states[TAXRATE][token]

    pass