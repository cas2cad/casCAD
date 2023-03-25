# from pargov.agent import InforAgent as Agent
# # from aletheia.utils.constant import *
# from pargov.constant import *
# # from aletheia.artificial_system.uniswap.fpmm import UniswapFPMM
# from pargov.fpmm import UniswapFPMM

from cascad.experiment.pargov.agent import InforAgent as Agent
from cascad.experiment.pargov.constant import *
from cascad.experiment.pargov.fpmm import UniswapFPMM
import copy
import math


class PredictMarket(object):
    def __init__(self) -> None:
        super().__init__()
        self.proposals = []

    def buy(self, agent):
        pass

    def sell(self, agent):
        pass

    def observe(self, agent):
        pass

class Omen(object):
    def __init__(self):
        self.states = {}
        self.states[PROPOSAL] = {}
        self.states[MARKET] = {}
        self.states[ACCEPT_TOKEN] = {}


    def add_proposal(self, proposal_id, amount_1, amount_2, accept_token):
        token_1 = '{}_{}_YES'.format(proposal_id, accept_token)
        token_2 = '{}_{}_NO'.format(proposal_id, accept_token)
        market_id = '{}_{}'.format(proposal_id, accept_token)
        self.states[ACCEPT_TOKEN][market_id] = accept_token
        self.states[MARKET][market_id] = UniswapFPMM(token_1, token_2, init_states={
            TRADES: [],
            LP: math.sqrt(amount_1 * amount_2),
            FEES: {token_1: 0, token_2:0},
            POOL: { token_1: amount_1, token_2: amount_2},
            APY: 0,
            APR: 0 
           
        }, uniswap=self, fee=0.02)

    def buy(self, agent:Agent, proposal_id, token_type, amount, accept_token):
        market_id = '{}_{}'.format(proposal_id, accept_token)
        amm: UniswapFPMM = self.states[MARKET][market_id]
        # accept_token = self.states[ACCEPT_TOKEN][proposal_id]
        if agent.states[accept_token] <= amount:
            # return False
            amount = agent.states[accept_token]
        if amount <= 0.1:
            return

        agent.states[accept_token] -= amount
        if token_type == YES_TOKEN:
            origin_token = '{}_{}_YES'.format(proposal_id, accept_token)
            another_token = '{}_{}_NO'.format(proposal_id, accept_token)
        else:
            origin_token = '{}_{}_NO'.format(proposal_id, accept_token)
            another_token = '{}_{}_YES'.format(proposal_id, accept_token)

        if origin_token in agent.states.keys():
            agent.states[origin_token] += amount
            agent.states[another_token] += amount
        else:
            agent.states[origin_token] = amount
            agent.states[another_token] = amount

        result = amm.swap(agent, another_token, amount, with_fee=False)
        if not result:
            return False


    def sell(self, agent:Agent, proposal_id, token_type, amount, accept_token):
        market_id = '{}_{}'.format(proposal_id, accept_token)
        amm: UniswapFPMM = self.states[MARKET][market_id]
        # accept_token = self.states[ACCEPT_TOKEN][proposal_id]
        if token_type == YES_TOKEN:
            origin_token = '{}_{}_YES'.format(proposal_id, accept_token)
            another_token = '{}_{}_NO'.format(proposal_id, accept_token)
        else:
            origin_token = '{}_{}_NO'.format(proposal_id, accept_token)
            another_token = '{}_{}_YES'.format(proposal_id, accept_token)

        x = amm.states[POOL][origin_token]
        y = amm.states[POOL][another_token]

        if agent.states[origin_token] <= amount:
            amount = agent.states[origin_token]

        # agent.states[origin_token] -= amount
        # b = -(y -x + amount)
        # c =  - x*amount

        # delta_y = - b + math.sqrt(b**2 - 4*c)
        # if delta_y < 0 or delta_y > amount:
        #     delta_y = - b - math.sqrt(b**2 - 4*c)
        if amount <= 0.1:
            return
        a = x/y
        delta_x = a * amount / (1 + a)
        delta_y = delta_x

        result = amm.swap(agent, origin_token, delta_y, with_fee=False)
        target_amount = amount - delta_y

        if result:
            agent.states[accept_token] += result
            agent.states[origin_token] -= result 
            agent.states[another_token] -= result 
        
        if agent.states[origin_token] < 0 or agent.states[another_token] <0:
            print('debug')

    def get_price(self, proposal_id, token_type, accept_token):
        market_id = '{}_{}'.format(proposal_id, accept_token)
        amm: UniswapFPMM = self.states[MARKET][market_id]

        if token_type == YES_TOKEN:
            origin_token = '{}_{}_YES'.format(proposal_id, accept_token)
            another_token = '{}_{}_NO'.format(proposal_id, accept_token)
        else:
            origin_token = '{}_{}_NO'.format(proposal_id, accept_token)
            another_token = '{}_{}_YES'.format(proposal_id, accept_token)

        x = amm.states[POOL][origin_token]
        y = amm.states[POOL][another_token]

        return y / (x + y)

class Uniswap(object):
    def __init__(self, oracle=None):
        self.states = {}
        self.states[PRICES] = {
            VALUE : {
                ZUSD: 0,
                USDT: 1,
                DUET: 0,
                ZBTC: 0,
                ZNAS: 0
            },
            CHANGE : {
                ZUSD: 0,
                USDT: 1,
                DUET: 0,
                ZBTC: 0,
                ZNAS: 0
            },
            TRADINGVALUE : {
                ZUSD : 0,
                USDT : 0,
                DUET : 0,
                ZBTC : 0,
                ZNAS : 0
            },
            HIGH : {
                ZUSD : 0,
                USDT : 0,
                DUET : 0,
                ZBTC : 0,
                ZNAS : 0
            },
            LOW : {
                ZUSD : 1000000000,
                USDT : 1000000000,
                DUET : 1000000000,
                ZBTC : 1000000000,
                ZNAS : 1000000000,
            },
            
        }
        self.states[HISTORY] =[]
        self.oracle = oracle
        self.init_uniswap()
        # self.step()

    def init_uniswap(self):
        self.states[DUET_USDT] = UniswapFPMM(DUET, USDT,
        init_states= {
            TRADES: [],
            LP: math.sqrt(119464 * 600632),
            FEES: {DUET: 0, USDT:0},
            POOL: { DUET: 119464, USDT: 600632},
            APY: 64363.5592,
            APR: 11.0723
        },uniswap=self
                
        )
        self.states[ZUSD_USDT] = UniswapFPMM(ZUSD, USDT,
         init_states= {
            TRADES: [],
            LP: math.sqrt(855296 * 842826),
            FEES: {ZUSD:0, USDT:0},
            POOL: { ZUSD: 855296, USDT: 842826},
            APY: 529.7571,
            APR: 6.2743
        },uniswap=self
        )
        self.states[ZBTC_ZUSD] = UniswapFPMM(ZBTC, ZUSD,
          init_states= {
            TRADES: [],
            LP: math.sqrt(10.20535 * 166501),
            FEES: {ZBTC:0, ZUSD:0},
            POOL: { ZBTC: 10.20535, ZUSD: 166501},
            APY: 602484.7781,
            APR: 13.3088
        },  uniswap=self
        )
        self.states[ZNAS_ZUSD] = UniswapFPMM(ZNAS, ZUSD,
           init_states= {
            TRADES: [],
            LP: math.sqrt(100.35 * 100000),
            FEES: {ZNAS:0, ZUSD:0},
            POOL: { ZNAS: 100.35, ZUSD: 100000},
            APY: 0,
            APR: 0
        }, uniswap=self
        )
        self.step()

    def farm(self, agent, pool, token1, token2, fee):
        amm = self.states[pool]
        return amm.farm(agent, token1, token2, fee)

    def withdraw(self, agent, pool, lp_amount):
        amm = self.states[pool]
        return amm.withdraw(agent, lp_amount)

    def swap(self, agent, origin_token, amount, target_token):
        pool = origin_token + '_' + target_token
        if pool in self.states.keys():
            amm = self.states[pool]
        else:
            pool = target_token + '_' + origin_token
            amm = self.states[pool]
        # if success, update trading values prices
        result = amm.swap(agent, origin_token, amount)
        if result:
            origin_token_price = self.get_current_usdt_price(origin_token)
            if origin_token_price > self.states[PRICES][HIGH][origin_token]:
                self.states[PRICES][HIGH][origin_token] = origin_token_price
            elif origin_token_price < self.states[PRICES][LOW][origin_token]:
                self.states[PRICES][LOW][origin_token] = origin_token_price
            self.states[PRICES][TRADINGVALUE][origin_token] += amount

            target_token_price = self.get_current_usdt_price(target_token)
            if target_token_price > self.states[PRICES][HIGH][target_token]:
                self.states[PRICES][HIGH][target_token] = target_token_price
            elif target_token_price < self.states[PRICES][LOW][target_token]:
                self.states[PRICES][LOW][target_token] = target_token_price
            self.states[PRICES][TRADINGVALUE][target_token] += amount
        return result

    def get_price(self, origin_token, target_token):
        pool = origin_token + '_' + target_token
        if pool in self.states.keys():
            amm = self.states[pool]
        else:
            pool = target_token + '_' + origin_token
            amm = self.states[pool]
        return amm.current_price(origin_token)

    def _get_price_usdt(self, token):
        if token == ZUSD or token == DUET:
            return self.get_price(token, USDT)
        elif token == USDT:
            return 1
        else:
            return self.get_price(token, ZUSD) * self.get_price(ZUSD, USDT)


    def get_fraction(self, pool):
        # return self.states[pool].prop
        return self.states[pool].get_prop()

    def add_reward(self, pool, amount):
        self.states[pool].add_reward(amount)

    def get_pool_by_token(self, token):
        token_map = {
            DUET: self.states[DUET_USDT],
            ZUSD: self.states[ZUSD_USDT],
            ZBTC: self.states[ZBTC_ZUSD],
            ZNAS: self.states[ZNAS_ZUSD]
        }
        return token_map[token]

    def get_fee(self, token, amount):
        """
        not include USDT
        """
        pool = self.get_pool_by_token(token)
        fee = pool.get_fee(amount)
        return fee

    def evaluate_swap(self, origin_token, amount, target_token):
        pool = origin_token + '_' + target_token
        if pool in self.states.keys():
            amm = self.states[pool]
        else:
            pool = target_token + '_' + origin_token
            amm = self.states[pool]

        # for uncertain amount
        if isinstance(amount, str):
            amount = 100

        val = amm.evaluate_swap(origin_token, amount)
        return val

    def evaluate_price(self, token, amount):
        if token == ZUSD or token == DUET:
            return self.evaluate_swap(token, amount, USDT)
        elif token == USDT:
            return amount
        else:
            zusd_amunt = self.evaluate_swap(token, amount, ZUSD)
            return self.evaluate_swap(ZUSD, zusd_amunt, USDT)


    def step(self):
        for k, v in self.states[PRICES][VALUE].items():
            new_price = self._get_price_usdt(k)
            if v == 0:
                change = 0
            else:
                change = (new_price - v) / v
            self.states[PRICES][VALUE][k] = new_price
            self.states[PRICES][CHANGE][k] = change
            self.states[PRICES][HIGH][k] =  new_price
            self.states[PRICES][LOW][k] =  new_price
           


        for pool in [DUET_USDT, ZUSD_USDT, ZBTC_ZUSD, ZNAS_ZUSD]:
            self.states[pool].step()

        prices_copy = copy.deepcopy(self.states[PRICES])
        self.states[HISTORY].append(prices_copy)

        for k, v in self.states[PRICES][TRADINGVALUE].items():
            self.states[PRICES][TRADINGVALUE][k] = 0
            # if len(self.states[HISTORY]) >= 6:
        #     last_prices = self.states[HISTORY][-6]
        #     for k,v in self.states[PRICES][VALUE].items():
        #         last_price = last_prices[VALUE][k]
        #         change = (v - last_price)/last_price
        #         self.states[PRICES][_7_DAY_PRICE] = change

        # if len(self.states[HISTORY]) >= 30:
        #     last_prices = self.states[HISTORY][-30]
        #     for k,v in self.states[PRICES][VALUE].items():
        #         last_price = last_prices[VALUE][k]
        #         change = (v - last_price)/last_price
        #         self.states[PRICES][_30_DAY_PRICE] = change


    def get_usdt_price(self, token):
        return self.states[PRICES][VALUE][token]

    def get_price_change(self, token):
        return self.states[PRICES][CHANGE][token]

    def get_current_usdt_price(self, token):
        return self._get_price_usdt(token)

    def get_current_price_change(self, token):
        new_price = self._get_price_usdt(token)
        v = self.states[PRICES][VALUE][token]

        if v==0:
            return 0
        else:
            change = (new_price - v) / v
            return change


    def get_pool_lp_value(self, pool, lp_amount):
        return self.states[pool].get_lp_value(lp_amount)

    def n_day_price_change(self, token, num):

        if len(self.states[HISTORY]) <= num:
            return 0
            
        v = self.get_current_usdt_price(token)
        last_prices = self.states[HISTORY][-30]
        last_price = last_prices[VALUE][token]
        change = (v - last_price)/last_price
        return change
       
    def get_apy(self, pool, with_reward = False):
        if with_reward:
            return self.states[pool].states[APY_WITH_REWARD]
        else:
            return self.states[pool].states[APY]
