from copy import deepcopy
from cascad.experiment.MBM.constant import *
from cascad.experiment.MBM.belief import Belief
from cascad.experiment.MBM.knowlege import *
from cascad.experiment.MBM.desires import *
from cascad.utils import get_id
from cascad.models.kb import Entity, Property
from cascad.experiment.MBM.plans import Plan
import random


class AgentFactory:

    @staticmethod
    def create_agent(unique_id: int, states: dict, system, _type: str, desire_token: Cryptocurrency=None,
     desire_pool: LiquidityPool=None, operate_amount: float = 100, short_farming_sell_time: float = 10,
     bullish_expect_rise:float = 0.1, bearish_stand_drop:float = 0.1, founder_sell_time: float = 60, incent_limit_benefit:float = 10,
     expect_apy = 0.1):
        """
        states = {
            'DUET': 0,
            'USDT': 0,
            'ZUSD': 0,
            'ZBTC': 0,
            'ZNAS': 0
        }
        """
        states = {k:v for k,v in states.items()}

        desire = desire_dict[_type]()
        belief = Belief(unique_id)
        agent = Agent(unique_id, states, belief, system)
        agent.set_desire(desire)

        onto = belief.onto

        token_dict = {
            USDT : onto.USDT,
            ZUSD : onto.ZUSD,
            ZBTC : onto.ZBTC,
            ZNAS : onto.ZNAS,
            DUET : onto.DUET
        }

        pool_dict = {
            DUET_USDT : onto.DUET_USDT,
            ZUSD_USDT : onto.ZUSD_USDT,
            ZBTC_ZUSD : onto.ZBTC_ZUSD,
            ZNAS_ZUSD : onto.ZNAS_ZUSD
        }

        if desire_token:
            desire_token = token_dict.get(desire_token)

        if desire_pool:
            desire_pool = pool_dict.get(desire_pool)

        # set the varibales of agent
        agent.set_bullish_expect_rise(bullish_expect_rise)
        agent.set_desire_token(desire_token)
        agent.set_desire_pool(desire_pool)
        agent.set_operate_amount(operate_amount)
        agent.set_short_farming_sell_time(short_farming_sell_time)
        agent.set_bearish_stand_drop(bearish_stand_drop)
        agent.set_founder_sell_time(founder_sell_time)
        agent.set_agent_incent_limit(incent_limit_benefit)
        agent.set_agent_expect_apy(expect_apy)
        return agent

class Agent:

    _name = "MBMAgent"

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
        # self.entity = Entity(unique_id, self._name)
        # self.entity['name'] = self._name

    def set_accept_no_reward(self, accept):
        self.accept_no_reward = accept

    def init_atom_actions(self):
        self.atom_actions = [('observe and think', (self.step, []))] 

    def set_desire(self, desire):
        self.desire = desire
        self.belief.set_desire(desire)
        if self.state == -1:
            self.state = 1

    def stop_farm(self):
        self.farm_flag = False

    def resume_farm(self):
        self.farm_flag = True

    def get_token_by_name(self, token):
        token_pair = {
            USDT: self.belief.onto.USDT,
            ZUSD: self.belief.onto.ZUSD,
            ZBTC: self.belief.onto.ZBTC,
            ZNAS: self.belief.onto.ZNAS,
            DUET: self.belief.onto.DUET
        }
        return token_pair[token].name


    def set_varible_of_agent(self, lock_up_period: float = 60, short_farming_min_time: float = 10, expect_rise_rate: float = 0.1):
        # locked up time
        self.belief.onto.myself.locked_up_period = lock_up_period
        self.belief.onto.myself.short_farming_min_time = short_farming_min_time
        self.belief.onto.myself.expect_rise_rate = expect_rise_rate


    def set_focus_model(self, model:str):
        """ 
        """
        self.focus_model = model

    def set_desire_token(self, token):
        """ the agent will choose this token when he has a chance to choose a token
        """
        self.belief.onto.myself.desire_token = token

    def set_desire_pool(self, pool):
        """ the agent will choose this pool when he has a chance to choose a pool
        """
        self.belief.onto.myself.desire_pool = pool

    def set_operate_amount(self, amount):
        """ for the spread agent, how many token operated one time
        """
        self.belief.onto.myself.operate_amount = amount

    def set_short_farming_sell_time(self, sell_time):
        """ when the short farming will sell his asset
        """
        self.belief.onto.myself.short_farming_sell_time = sell_time
        pass

    def set_bullish_expect_rise(self, rise_rate):
        """ when the bullish will sell his asset
        """
        self.belief.onto.myself.expect_rise_rate = rise_rate

    def set_bearish_stand_drop(self, drop_rate):
        """ when the bearish will drop his asset
        """
        self.belief.onto.myself.stand_drop_rate = drop_rate

    def set_founder_sell_time(self, sell_time):
        """ when the sell founder will sell his duet
        """
        self.belief.onto.myself.founder_sell_time = sell_time

    def set_agent_incent_limit(self, benefit):
        self.belief.onto.myself.incent_benefit_limit = benefit
        pass

    def set_agent_expect_apy(self, apy):
        self.belief.onto.myself.expect_apy = apy 

    def get_configs(self):
        onto = self.belief.onto
        return {
            'focus_model': self.focus_model,
            'desire': self.desire.name,
            'desire_token' : onto.myself.desire_token,
            'desire_pool' : onto.myself.desire_pool,
            'operate_amount' : onto.myself.operate_amount,
            'short_farming_sell_time': onto.myself.short_farming_sell_time,
            'bullish_expect_rise': onto.myself.expect_rise_rate,
            'bearish_stand_drop': onto.myself.stand_drop_rate,
            'founder_sell_time': onto.myself.founder_sell_time,
            'expect_apy': onto.myself.expect_apy
        }

    def observe(self):
        """ here is the agent can get information from the system
        """

        self.belief.onto.ZBTC.current_uniswap_price = self.system.get_price(
            ZBTC, ZUSD)
        self.belief.onto.ZUSD.current_uniswap_price = self.system.get_price(
            ZUSD, USDT)
        self.belief.onto.ZNAS.current_uniswap_price = self.system.get_price(
            ZNAS, ZUSD)
        self.belief.onto.DUET.current_uniswap_price = self.system.get_price(
            DUET, USDT)

        self.belief.onto.BTC.current_oracle_price = self.system.get_oracle_price(
            BTC)

        self.belief.onto.NAS.current_oracle_price = self.system.get_oracle_price(
            NAS)

        self.belief.onto.USDT.current_oracle_price = self.system.get_oracle_price(
            USDT)

        self.belief.onto.DUET.current_oracle_price = self.system.get_oracle_price(
            DUET)

        self.belief.onto.DUET_USDT.has_fraction = self.system.get_fraction(
            self.belief.onto.DUET_USDT.name)

        self.belief.onto.ZUSD_USDT.has_fraction = self.system.get_fraction(
            self.belief.onto.ZUSD_USDT.name)

        self.belief.onto.ZBTC_ZUSD.has_fraction = self.system.get_fraction(
            self.belief.onto.ZBTC_ZUSD.name)

        self.belief.onto.ZNAS_ZUSD.has_fraction = self.system.get_fraction(
            self.belief.onto.ZNAS_ZUSD.name)

        flag = True
        self.belief.onto.DUET_USDT.has_apy= self.system.get_apy(
            self.belief.onto.DUET_USDT.name, flag)

        self.belief.onto.ZUSD_USDT.has_apy= self.system.get_apy(
            self.belief.onto.ZUSD_USDT.name, flag)

        self.belief.onto.ZBTC_ZUSD.has_apy= self.system.get_apy(
            self.belief.onto.ZBTC_ZUSD.name, flag)

        self.belief.onto.ZNAS_ZUSD.has_apy= self.system.get_apy(
            self.belief.onto.ZNAS_ZUSD.name, flag)

        # time + 1
        self.belief.onto.myself.duet_holding_time += 1
        self.belief.onto.myself.short_farming_time += 1

        # mini duration time of short farm

    def init_think(self):
        """
        here is reason logic of the agent
        """
        # if self.unique_id == 250 and self.system.timeline.tick==36:
        # if self.unique_id == 105:
        #     # print('debug')

        create_action = self.belief.create_action
        onto = self.belief.onto
        operate_amount = onto.myself.operate_amount

        operate_amount = random.randint(self.mini_amount, operate_amount)

        # if self.desire == DuetHold:
        #     self.belief.onto.myself.has_action.append(Swap('swap'))
        self.belief.onto.swap.swap_origin_token = self.belief.onto.USDT
        self.belief.onto.swap.swap_target_token = self.belief.onto.DUET

        if self.desire.name == Trader.name:
            pass

        elif self.desire.name == SellFounder.name:
            # do nothing at beggining
            # sell proportion
            self.belief.onto.myself.duet_holding_time = 0

        elif self.desire.name == HoldFounder.name:
            # do nothing at begging
            pass

        elif self.desire.name == DuetHold.name:
            # self.belief.onto.swap.swap_amount = self.states[USDT]
            # self.belief.onto.myself.has_action.append(self.belief.onto.swap)
            if self.states[USDT] >= self.mini_amount_usdt:
                buy_action = self.belief.create_action(
                    _type = SWAP1,
                    swap_origin_token = self.belief.onto.USDT,
                    swap_target_token = self.belief.onto.DUET,
                    swap_amount = operate_amount
                )
                # self.belief.onto.myself.has_action.append(buy_action)
                self.add_action(buy_action)

        elif self.desire.name == DuetHoldAndFarm.name:
            # for this kind of person, he will split his duet half and half
            # use all of them to farm
            # rest of them? just hold, like a human beings
            fraction = 0.5

            if not self.farm_flag:
                return

            buy_action = create_action(
                _type =  SWAP1,
                swap_origin_token = onto.USDT,
                swap_target_token = onto.DUET,
                swap_amount = fraction * operate_amount 
            )
            self.add_action(buy_action)

            # onto.myself.has_action.append(buy_action)

            onto.myself.using_farm_pool.append(onto.DUET_USDT)

            farm_action = create_action(
                _type = FARM,
                farm_pool = onto.DUET_USDT,
                farm_token1_amount = MAX,
                farm_token2_amount = MAX
            )

            # onto.myself.has_action.append(farm_action)
            # if blocked, not take farming action
            # if self.farm_flag:
            self.add_action(farm_action)

        elif self.desire.name == DuetHoldAndStake.name:
            buy_action = self.belief.create_action(
                _type = SWAP1,
                swap_origin_token = self.belief.onto.USDT,
                swap_target_token = self.belief.onto.DUET,
                swap_amount = operate_amount 
            )
            self.add_action(buy_action)

            stake_action = create_action(
                _type = STAKE,
                stake_amount = MAX
            )
            self.add_action(stake_action)

        elif self.desire.name == DAssetHold.name:
            target_token = onto.myself.desire_token

            buy_action = create_action(
                _type = SWAP1,
                swap_origin_token = onto.USDT,
                swap_target_token = onto.DUET,
                swap_amount = operate_amount 
            )
            self.add_action(buy_action)
            
            mint_action = create_action(
                _type = MINT1,
                mint_token = target_token,
                mint_amount = MAX
            )
            self.add_action(mint_action)

        elif self.desire.name == DAssetHoldAndFarm.name:

            # self.dasset_farming()
            self.dasset_farming_from_usdt(True)
            
        elif self.desire.name == ShortFarmArbitrage.name:
            # self.dasset_farming()
            self.dasset_farming_from_usdt(True)

        elif self.desire.name == Spread.name:
            # at the begining, do nothing
            #target_token = onto.myself.desire_token
            amount = onto.myself.operate_amount
            if self.unique_id == 101:
                print('debug')

            plan = Plan.choose_spread_plan(self, amount)
            for action in plan:
                self.add_action(action)

        elif self.desire.name == BullishDUET.name:
            current_price =self.system.get_current_usdt_price(DUET)
            expect_rise_rate = onto.myself.expect_rise_rate
            stand_drop_rate = onto.myself.stand_drop_rate

            # who think duet price will go high
            buy_action = create_action(
                _type = SWAP1,
                swap_origin_token = onto.USDT,
                swap_target_token = onto.DUET,
                swap_amount = operate_amount 
            )
            self.add_action(buy_action)

        elif self.desire.name == BullishDAsset.name:
            # todo

            target_token = onto.myself.desire_token

            current_price =self.system.get_current_usdt_price(target_token.name)
            expect_rise_rate = onto.myself.expect_rise_rate
            stand_drop_rate = onto.myself.stand_drop_rate
            # price change
            # if self.system.get_tax(DUET) > onto.DUET.current_uniswap_price * self.tax_accept:
            #     return 

            plan = Plan.choose_swap_plan(onto.USDT, target_token, self, operate_amount)
            for action in plan:
                self.add_action(action)

        elif self.desire.name == BearrishDUET.name:
            # who think dasset price will go high
            current_price =self.system.get_current_usdt_price(DUET)
            expect_rise_rate = onto.myself.expect_rise_rate
            stand_drop_rate = onto.myself.stand_drop_rate
            # price change
            price_change = (current_price - self.start_point) / self.start_point
            self.start_point = current_price

            buy_action = create_action(
                _type = SWAP1,
                swap_origin_token = onto.USDT,
                swap_target_token = onto.DUET,
                swap_amount = operate_amount
            )
            self.add_action(buy_action)

        elif self.desire.name == BearrishDAsset.name:
            target_token = onto.myself.desire_token
            current_price =self.system.get_current_usdt_price(target_token.name)
            expect_rise_rate = onto.myself.expect_rise_rate
            stand_drop_rate = onto.myself.stand_drop_rate
            # price change
            # if self.system.get_tax(DUET) > onto.DUET.current_uniswap_price * self.tax_accept:
            #     return 

            plan = Plan.choose_swap_plan(onto.USDT, target_token, self, operate_amount)
            
            for action in plan:
                self.add_action(action)

    def add_action(self, action):
        onto = self.belief.onto
        onto.myself.has_action.append(action)

    def think(self):
        """
        """
        if self.unique_id == 105:
            print('debug')

        create_action = self.belief.create_action
        onto = self.belief.onto
        operate_amount = onto.myself.operate_amount
        operate_amount = random.randint(self.mini_amount, operate_amount)


        self.belief.onto.swap.swap_origin_token = self.belief.onto.USDT
        self.belief.onto.swap.swap_target_token = self.belief.onto.DUET

        if self.desire.name == Trader.name:
            # the trader when price drop, they buy, when price rise, they sell
            operate_amount = operate_amount
            # price_change = self.system.n_day_price_change(DUET, 30)
            current_price =self.system.get_current_usdt_price(DUET)
            expect_rise_rate = onto.myself.expect_rise_rate
            stand_drop_rate = onto.myself.stand_drop_rate

            # price change
            price_change = (current_price - self.start_point) / self.start_point

            if price_change <0 and -price_change >= stand_drop_rate and self.states[USDT] > self.mini_amount:
                plan = Plan.choose_swap_plan(onto.USDT, onto.DUET, self, operate_amount * abs(price_change))
                for action in plan:
                    self.add_action(action)
                self.start_point = current_price

            elif price_change > expect_rise_rate and self.states[DUET]>self.mini_amount:
                plan = Plan.choose_swap_plan(onto.DUET, onto.USDT, self, operate_amount * abs(price_change))
                for action in plan:
                    self.add_action(action)
                self.start_point = current_price

        elif self.desire.name == HoldFounder.name:
            pass

        elif self.desire.name == SellFounder.name:
            operate_amount =  operate_amount
            if self.states[DUET] <= operate_amount:
                operate_amount = self.states[DUET]
            price_change = self.system.n_day_price_change(DUET, 30)
            stand_drop_rate = onto.myself.stand_drop_rate
            if onto.DUET.current_uniswap_price <= self.start_point:
                self.flag = False
                self.flag_step = 0
                # the founder won't sell on a too lower price

            elif price_change <0 and -price_change >= stand_drop_rate:
                if self.flag:
                    self.flag = False
                    self.flag_step = 0
            else:
                    # the bullish rejoin the trade
                    self.flag_step += 1
                    if self.flag_step >= random.randint(7, 300):
                        self.flag = True

            # operate_amount = operate_amount * 10 # the founder selll sell big mount of duet

            if onto.myself.duet_holding_time >= onto.myself.founder_sell_time and self.states[DUET] >= self.mini_amount and self.flag:
                # print('agent {} selling DUET with amount {}'.format(self.unique_id, operate_amount))
                plan = Plan.choose_swap_plan(onto.DUET, onto.USDT, self, operate_amount)
                for action in plan:
                    self.add_action(action)
                # self.quit()

        elif self.desire.name == DuetHold.name:
            if self.states[USDT] >= self.mini_amount_usdt:
                buy_action = self.belief.create_action(
                    _type = SWAP1,
                    swap_origin_token = self.belief.onto.USDT,
                    swap_target_token = self.belief.onto.DUET,
                    swap_amount = operate_amount
                )
                # self.belief.onto.myself.has_action.append(buy_action)
                self.add_action(buy_action)

        elif self.desire.name == DuetHoldAndFarm.name:

            # if self.states[DUET] <= self.mini_amount:
                # return

            if not self.farm_flag:
                    with_draw_action = create_action(
                        _type = FRAMWITHDRAW,
                        farm_withdraw_amount = MAX,
                        farm_pool = onto.DUET_USDT 
                    )
                    self.add_action(with_draw_action)
                    return 


            expect_apy = onto.myself.expect_apy

            fraction = onto.DUET_USDT.has_fraction
            has_apy = onto.DUET_USDT.has_apy

            if has_apy < expect_apy:
                return

            token_price = onto.DUET.current_uniswap_price

            if abs(self.states[DUET] - fraction * self.states[USDT]) <= operate_amount:
                if self.states[DUET] < self.mini_amount or self.states[USDT] < self.mini_amount:
                    return

            # elif self.states[DUET] > fraction * self.states[USDT] and self.states[DUET] >= self.mini_amount: # peple want trade when the price is too way low
            #     if self.states[DUET] <= operate_amount:
            #         operate_amount = self.states[DUET]
            #     buy_action = create_action(
            #         _type = SWAP1,
            #         swap_origin_token = onto.DUET,
            #         swap_target_token = onto.USDT,
            #         swap_amount = fraction * operate_amount 
            #     )
            #     self.add_action(buy_action)

            elif self.states[DUET] < fraction * self.states[USDT] and self.states[USDT] >= self.mini_amount_usdt:
                if self.states[USDT] <= operate_amount:
                    operate_amount = self.states[USDT]

                buy_action = create_action(
                    _type =  SWAP1,
                    swap_origin_token = onto.USDT,
                    swap_target_token = onto.DUET,
                    swap_amount = fraction * operate_amount 
                )
                self.add_action(buy_action)

            farm_action = create_action(
                _type = FARM,
                farm_pool = onto.DUET_USDT,
                farm_token1_amount = MAX,
                farm_token2_amount = MAX
            )
            if has_apy > expect_apy:
                self.add_action(farm_action)

        elif self.desire.name == DuetHoldAndStake.name:

            if self.system.staker.get_apy() < onto.myself.expect_apy:
                # if not enogh apy, hold switch to usdt?
                # buy_action = self.belief.create_action(
                #     _type = SWAP1,
                #     swap_origin_token = self.belief.onto.DUET,
                #     swap_target_token = self.belief.onto.USDT,
                #     swap_amount = operate_amount 
                # )
                # self.add_action(buy_action)
                pass
            else:

                if self.states[USDT] >= self.mini_amount_usdt:
                    buy_action = self.belief.create_action(
                    _type = SWAP1,
                    swap_origin_token = self.belief.onto.USDT,
                    swap_target_token = self.belief.onto.DUET,
                    swap_amount = operate_amount 
                    )
                    self.add_action(buy_action)

                if self.states[DUET] >= self.mini_amount:

                    stake_action = create_action(
                    _type = STAKE,
                    stake_amount = MAX
                    )
                    self.add_action(stake_action)

        elif self.desire.name == DAssetHold.name:
            target_token = onto.myself.desire_token

            if self.states[USDT] > self.mini_amount_usdt:
                buy_action = create_action(
                   _type = SWAP1,
                   swap_origin_token = onto.USDT,
                   swap_target_token = onto.DUET,
                   swap_amount = operate_amount 
                )
                self.add_action(buy_action)

            if self.states[DUET] > self.mini_amount:
            
                mint_action = create_action(
                    _type = MINT1,
                    mint_token = target_token,
                    mint_amount = MAX
                )
                self.add_action(mint_action)

        elif self.desire.name == DAssetHoldAndFarm.name:
            target_token = onto.myself.desire_token
            target_pool = onto.myself.desire_pool

            if not self.farm_flag:
                    with_draw_action = create_action(
                        _type = FRAMWITHDRAW,
                        farm_withdraw_amount = MAX,
                        farm_pool = target_pool
                    )
                    self.add_action(with_draw_action)


            elif self.states[DUET] >= self.mini_amount:
                if self.states[DUET] < operate_amount:
                    operate_amount = self.states[DUET]
                self.dasset_farming_from_duet()

            elif self.states[USDT] >= self.mini_amount_usdt:
                if self.states[USDT] < operate_amount:
                    operate_amount = self.states[USDT]
                self.dasset_farming_from_usdt()

        elif self.desire.name == ShortFarmArbitrage.name:
            # todo next
            target_token = onto.myself.desire_token
            target_pool = onto.myself.desire_pool
            # if not self.farm_flag:
            #         with_draw_action = create_action(
            #             _type = FRAMWITHDRAW,
            #             farm_withdraw_amount = MAX,
            #             farm_pool = target_pool
            #         )
            #         self.add_action(with_draw_action)
            #         return 


            if onto.myself.short_farming_time >= onto.myself.short_farming_sell_time:
                lp_value = self.system.get_pool_lp_value(target_pool.name, 1)
                operate_amount = operate_amount/lp_value

                if target_pool == onto.ZUSD_USDT and self.states[ZUSD_USDT] >0:
                    with_draw_action = create_action(
                        _type = FRAMWITHDRAW,
                        farm_withdraw_amount = operate_amount,
                        farm_pool = target_pool
                    )
                    self.add_action(with_draw_action)

                    plan = Plan.choose_swap_plan(onto.ZUSD, onto.USDT, self, LAST, 0)
                    for action in plan:
                        self.add_action(action)

                if target_pool == onto.ZBTC_ZUSD and self.states[ZBTC_ZUSD] >0 :
                    
                    with_draw_action = create_action(
                        _type = FRAMWITHDRAW,
                        farm_withdraw_amount = operate_amount,
                        farm_pool = target_pool
                    )
                    self.add_action(with_draw_action)

                    swap_step = 0

                    plan1 = Plan.choose_swap_plan(onto.ZUSD, onto.USDT, self, LAST, swap_step)
                    for action in plan1:
                        self.add_action(action)
                    swap_step = Plan.count_swap(plan1)

                    plan2 = Plan.choose_swap_plan(onto.ZBTC, onto.USDT, self, LAST, swap_step)
                    for action in plan2:
                        self.add_action(action)

                if target_pool == onto.ZNAS_ZUSD and self.states[ZNAS_ZUSD] > 0:
                    with_draw_action = create_action(
                        _type = FRAMWITHDRAW,
                        farm_withdraw_amount = operate_amount,
                        farm_pool = target_pool
                    )
                    self.add_action(with_draw_action)

                    swap_step = 0

                    plan1 = Plan.choose_swap_plan(onto.ZUSD, onto.USDT, self, LAST, swap_step)
                    for action in plan1:
                        self.add_action(action)
                    swap_step = Plan.count_swap(plan1)

                    plan2 = Plan.choose_swap_plan(onto.ZNAS, onto.USDT, self, LAST, swap_step)
                    for action in plan2:
                        self.add_action(action)

                # time to quit
                # self.quit()

            elif target_pool.has_apy< onto.myself.expect_apy:

                pass
            else:
                if self.states[DUET] >= self.mini_amount:
                    if self.states[DUET] < operate_amount:
                        operate_amount = self.states[DUET]
                    self.dasset_farming_from_duet()
                elif self.states[USDT] >= self.mini_amount_usdt:
                    if self.states[USDT] < operate_amount:
                        operate_amount = self.states[USDT]
                    self.dasset_farming_from_usdt()
   
        elif self.desire.name == Spread.name:
            # todo next judge from current situation!
            # find the way to make benefit
            # when there is spread? how much benefit one agent can make, what action it will take?
            # how many tokens it will spend in one trade
            if self.unique_id == 101:
                print('debug')
            target_token = onto.myself.desire_token
            amount = onto.myself.operate_amount

            plan = Plan.choose_spread_plan(self, amount)
            for action in plan:
                self.add_action(action)

        elif self.desire.name == BullishDUET.name:
            # todo
            # two ways to get usdt from duet
            # check the rise rate of it and if acquire to a point, sell it according to amount
            amount = onto.myself.operate_amount
            # duet_unit_cost = self.unit_cost[DUET]
            expect_rise_rate = onto.myself.expect_rise_rate

            duet_token = self.belief.onto.DUET
            duet_price = duet_token.current_uniswap_price
            rise_percentage = self.system.n_day_price_change(DUET, 30)
            token_price =self.system.get_current_usdt_price(DUET)
            expect_rise_rate = onto.myself.expect_rise_rate
            stand_drop_rate = onto.myself.stand_drop_rate
            # price change
            # rise_percentage = (token_price - self.start_point) / self.start_point

            # rise_percentage = (duet_price - duet_unit_cost) / duet_unit_cost
            if duet_price <= self.start_point: # bullish don't believe duet will drop too low
                self.flag = False
                self.flag_step = 0

            if rise_percentage >= expect_rise_rate and self.states[DUET] >= self.mini_amount:
                # self.start_point = duet_price
                amount = amount * (rise_percentage / expect_rise_rate)
                if amount >= self.states[DUET]:
                    amount = self.states[DUET]

                # print('agent {} selling DUET with amount {}'.format(self.unique_id, amount))

                plan = Plan.choose_swap_plan(onto.DUET, onto.USDT, self, amount)

                for action in plan:
                    self.add_action(action)
                if self.flag:
                    self.flag = False
                    self.flag_step = 0
            else:
                if not self.flag:
                    # the bullish rejoin the trade
                    self.flag_step += 1
                    if self.flag_step >= random.randint(3,7):
                        self.flag = True

                # if (self.flag and self.states[USDT] >= self.mini_amount) or (duet_price <= self.start_point and self.states[USDT] >= self.mini_amount): # bullish buy when price is low

                if self.states[USDT] >= self.mini_amount_usdt and self.flag:
                    buy_action = create_action(
                        _type = SWAP1,
                        swap_origin_token = onto.USDT,
                        swap_target_token = onto.DUET,
                        swap_amount = operate_amount 
                    )
                    self.add_action(buy_action)

        elif self.desire.name == BullishDAsset.name:
            target_token = onto.myself.desire_token
            target_pool = onto.myself.desire_pool
            amount = onto.myself.operate_amount
            expect_rise_rate = onto.myself.expect_rise_rate

            token_price = target_token.current_uniswap_price
            # token_unit_cost = self.unit_cost[target_token.name]

            # if token_unit_cost == 0:
            #     rise_percentage = 0
            # else:
            #     rise_percentage = (token_price - token_unit_cost) / token_unit_cost
            # rise_percentage = self.system.get_price_change(target_token.name)
            rise_percentage = self.system.n_day_price_change(target_token.name, 30)
            # token_price =self.system.get_current_usdt_price(target_token.name)
            expect_rise_rate = onto.myself.expect_rise_rate
            stand_drop_rate = onto.myself.stand_drop_rate
            # price change
            # rise_percentage = (token_price - self.start_point) / self.start_point

            # if not self.flag:
            #         # the bullish rejoin the trade
            #         self.flag_step += 1
            #         if self.flag_step >= random.randint(7,30):
            #             self.flag = True


            if rise_percentage >= expect_rise_rate  and self.states[target_token.name] > 0:
                # self.start_point = token_price
                amount = amount / token_price

                amount = amount * (rise_percentage / expect_rise_rate)
                if amount >= self.states[target_token.name]:
                    amount = self.states[target_token.name]
                # print('agent {} selling DUET with amount {}'.format(self.unique_id, amount))

                plan = Plan.choose_swap_plan(target_token, onto.USDT, self, amount)

                for action in plan:
                    self.add_action(action)
                # self.flag = False
                if self.flag:
                    self.flag = False
                    self.flag_step = 0
            else:
                if not self.flag:
                    # the bullish rejoin the trade
                    self.flag_step += 1
                    if self.flag_step >= random.randint(3,7):
                        self.flag = True

                # if self.flag and  self.states[USDT] >= self.mini_amount:
                if self.states[USDT] >= self.mini_amount_usdt and self.flag:
                    plan = Plan.choose_swap_plan(onto.USDT, target_token, self, operate_amount)
                    for action in plan:
                        self.add_action(action)

        elif self.desire.name == BearrishDUET.name:
            # todo bearish will sell when they see a rop in price
            stand_drop_rate = onto.myself.stand_drop_rate
            amount = onto.myself.operate_amount
            target_token = onto.DUET
            duet_token = self.belief.onto.DUET
            duet_price = duet_token.current_uniswap_price
            rise_percentage = self.system.n_day_price_change(DUET, 30)
            token_price =self.system.get_current_usdt_price(DUET)
            expect_rise_rate = onto.myself.expect_rise_rate
            stand_drop_rate = onto.myself.stand_drop_rate
            # price change
            # price_change = (token_price - self.start_point) / self.start_point

            # price_change = self.system.get_price_change(target_token)
            price_change = self.system.n_day_price_change(DUET, 30)
            if duet_price >= self.start_point*5: # bearish don't believe duet will rise too high
                self.flag = False
                self.flag_step = 0

            if price_change <0 and - price_change >= stand_drop_rate and self.states[DUET] >= self.mini_amount:
                # self.start_point = token_price
                amount = amount * ( - price_change/ stand_drop_rate)
                if amount >= self.states[target_token.name]:
                    amount = self.states[target_token.name]
                # print('agent {} selling DUET with amount {}'.format(self.unique_id, amount))

                if self.states[DUET] <= 0:
                    return
                plan = Plan.choose_swap_plan(onto.DUET, onto.USDT, self, amount)
                for action in plan:
                    self.add_action(action)
                # self.flag = False
                if self.flag:
                    self.flag = False
                    self.flag_step = 0
            else:
                if not self.flag:
                    # the bullish rejoin the trade
                    self.flag_step += 1
                    if self.flag_step >= random.randint(3,7):
                        self.flag = True


                # if self.flag and self.states[USDT] >= self.mini_amount:
                if self.states[USDT] >= self.mini_amount_usdt and self.flag:

                    buy_action = create_action(
                        _type = SWAP1,
                        swap_origin_token = onto.USDT,
                        swap_target_token = onto.DUET,
                        swap_amount = operate_amount
                    )
                    self.add_action(buy_action)

        elif self.desire.name == BearrishDAsset.name:
            if self.unique_id == 163 and self.system.timeline.tick==16:
                print('debug')
            stand_drop_rate = onto.myself.stand_drop_rate
            target_token = onto.myself.desire_token
            amount = onto.myself.operate_amount
            token_price = target_token.current_uniswap_price
            # token_price =self.system.get_current_usdt_price(DUET)
            expect_rise_rate = onto.myself.expect_rise_rate
            stand_drop_rate = onto.myself.stand_drop_rate
            # price change
            # price_change = (token_price - self.start_point) / self.start_point

            # price_change = self.system.get_price_change(target_token)
            price_change = self.system.n_day_price_change(target_token.name, 30)

            if price_change <0 and -price_change >= stand_drop_rate and self.states[target_token.name] >0.0000001:
                # self.start_point = token_price
                amount = amount / token_price
                amount = amount * ( - price_change/ stand_drop_rate)

                # amount_fraction = (amount/5000 ) * self.states[target_token.name]
                if amount >= self.states[target_token.name]:
                    amount = self.states[target_token.name]
                # print('agent {} selling DUET with amount {}'.format(self.unique_id, amount))

                plan = Plan.choose_swap_plan(target_token, onto.USDT, self, amount)
                for action in plan:
                    self.add_action(action)
                # self.flag = False
                if self.flag:
                    self.flag = False
                    self.flag_step = 0
            else:
                if not self.flag:
                    # the bullish rejoin the trade
                    self.flag_step += 1
                    if self.flag_step >= random.randint(3,7):
                        self.flag = True


                # if self.flag and self.states[USDT] >= self.mini_amount:
                # if self.system.get_tax(DUET) > onto.DUET.current_uniswap_price * self.tax_accept:
                #     return 
                if self.states[USDT] >= self.mini_amount_usdt and self.flag:

                    plan = Plan.choose_swap_plan(onto.USDT, target_token, self, operate_amount)
            
                    for action in plan:
                        self.add_action(action)
        else:
            print('unkown')

    def record(self, data):
        # self.states[actions].append()
        tick = self.system.timeline.tick
        self.states[ACTION].append(
            data
        )

    def execute(self):
        """
        here is the adpater to the system execution
        """

        def swap(origin_token, amount, target_token):
            amount = compile_amount(amount, origin_token)
            if amount <= 0:
                    amount = 0

            result = self.system.swap(self, origin_token, amount, target_token)
            self.record({
                '_type': 'swap',
                'origin_token': origin_token,
                'amount': amount,
                'target_token': target_token,
                'result': result
            })

            if result:
                cost = self.system.evaluate_price(origin_token, amount)
                self.update_cost(target_token, result, cost)
                self.last_gen[target_token] = result
            else:
                # print('failed to swap')
                # print('swap amount: {}'.format(amount))
                break_plan(action)

            if not result:
                pass
            else:
                return result


        def farm(pool, amount1, amount2, fee=0.003):
            if not self.farm_flag:
                return False
            if self.unique_id == 70 and self.system.timeline.tick==36:
                print('debug')

            amount1 = compile_amount(amount1, token1)

            amount2 = compile_amount(amount2, token2)
            
            result, tokens = self.system.farm(self, pool, amount1, amount2, fee)
            if result:
                data = tokens
                data['_type'] = 'farm'
                data['farm_fee'] = fee
                data['farm_pool'] = pool
                data['farm_result'] = result
                self.record(data)

            if result < 0:
                    print('unexpecte value')
            if not result:
                    # print('unique id : {}'.format(self.unique_id))
                    # print('failed to farm {}'.format(pool))
                    # print('farm amount1 {}'.format(amount1))
                    # print('farm amount 2 {}'.format(amount2))
                    # print('agent desire {}'.format(self.desire))
                    break_plan(action)

            return result

        def stake(amount):

            amount = compile_amount(amount, DUET)

            result = self.system.stake(self, amount)
            self.record({
                '_type': 'stake',
                'stake_amount': amount,
                'result': result
            })
            return result

        def mint(token, duet_amount=-1):

            duet_amount = compile_amount(duet_amount, DUET)

            result, tax = self.system.mint(self, token, duet_amount = duet_amount)
            self.record({
                '_type': 'mint',
                'mint_token' : token.name,
                'mint_amount': duet_amount,
                'result': result,
                'result2': tax
            })

            if result:
                    cost = self.system.evaluate_price(DUET, duet_amount)
                    if cost < 0:
                        print('unexpected cost')
                    self.update_cost(token, duet_amount, cost)
                    self.last_gen[token.name] = result
            else:
                    # print('failed to mint')
                    break_plan(action)

            return result

        def redeem(token, amount):
            amount = compile_amount(amount, token)

            result, tax = self.system.redeem(self, token, amount)
            self.record({
                '_type': 'redeem',
                'redeem_token': token,
                'redeem_amount': amount,
                'result': result,
                'result2': tax
            })
            if result:
                cost = self.system.evaluate_price(token, amount)
                self.update_cost(token, amount, cost)
                self.last_gen[DUET] = result
            else:
                # print('failed to redeem')
                break_plan(action)
            return result

        def farm_withdraw(pool, amount):

            amount = compile_amount(amount, farm_pool.name)

            result = self.system.farm_withdraw(self, pool, amount)
            if result:
                values = list(result.values())

                self.record({
                    '_type': 'farm_withdraw',
                    'farm_pool': pool,
                    'withdraw_amount': amount,
                    'result': values[0],
                    'result2': values[1]
                })
            else:
                print(pool, amount, self.states)
            return result

        def stake_withdraw(amount):
            amount = compile_amount(amount, STAKE)

            result = self.system.stake_withdraw(self, amount)
            self.record({
                '_type': 'stake_withdraw',
                'withdraw_amount': amount,
                'result': result
            })
            return result

        def compile_amount(amount, token):
            if self.system.blockchain.turn_on:
                self.prepare_gas()# prepare the gas fee

            if not isinstance(token, str):
                token = token.name

            if amount == LAST:
                    amount =self.last_gen[token]   
            elif amount == MAX:
                    amount = self.states[token]
            elif isinstance(amount, str) and amount.startswith(FRACTION + '-'):
                    amount = self.states[token] * float(amount[8:])

            if not isinstance(amount, str):
                if amount > self.states[token]:
                        amount = self.states[token]
                if amount > self.states[token] - 42 and token == USDT and self.system.blockchain.turn_on:
                        amount = max(self.states[token] - 42, 0)
                return amount
            return amount


        actions = self.belief.onto.myself.has_action

        def break_plan(action):
            # # print(self.unique_id)
            # do nothing
            pass
            # print(self.unique_id)
            # print(action)
            # # print(self.states)
            # print('action failed')
            # while actions:
            #     actions.pop(0)

        while actions:
            action = actions.pop(0)
            if action.name == SWAP1 or action.name == SWAP2 or action.name == SWAP3 or action.name == SWAP4:
                origin_token = action.swap_origin_token.name
                target_token = action.swap_target_token.name
                amount = action.swap_amount
        

                # result = swap(origin_token, amount, target_token)
                self.atom_actions.append((action.name,(swap, [origin_token, amount, target_token])))
                # if result:
                #     cost = self.system.evaluate_price(origin_token, amount)
                #     self.update_cost(target_token, result, cost)
                #     self.last_gen[target_token] = result
                # else:
                #     # print('failed to swap')
                #     break_plan(action)

            elif action.name == FARM:
                pool = action.farm_pool
                token1 = pool.has_token1.name
                token2 = pool.has_token2.name
                pool_name = pool.name
                amount1 = action.farm_token1_amount

                amount2 = action.farm_token2_amount


                # if amount1 <0 or amount2 <0:
                    # # print('debug')
                # todo max farm compute
                # result = farm(pool_name, amount1, amount2)
                self.atom_actions.append((action.name, (farm, [pool_name, amount1, amount2])))
                # if result < 0:
                #     # print('unexpecte value')
                # if not result:
                #     # print('failed to farm')
                #     # print('farm amount1 {}'.format(amount1))
                #     # print('farm amount 2 {}'.format(amount2))
                #     # print('agent desire {}'.format(self.desire))
                #     break_plan(action)

            elif action.name == STAKE:
                amount = action.stake_amount

                # result = stake(amount)
                self.atom_actions.append((action.name,(stake, [amount])))
                
                # if not result:
                #     # # print('failed to stake')
                #     break_plan(action)

            elif action.name == MINT1 or action.name == MINT2:
                amount = action.mint_amount
                token = action.mint_token


                # result = mint(token, duet_amount = amount)
                self.atom_actions.append((action.name,(mint, [token, amount])))
                # if result:
                #     cost = self.system.evaluate_price(DUET, amount)
                #     if cost < 0:
                #         # print('unexpected cost')
                #     self.update_cost(token, amount, cost)
                #     self.last_gen[token.name] = result
                # else:
                #     # print('failed to mint')
                #     break_plan(action)

            elif action.name == REDEEM:
                # # print()
                amount = action.redeem_amount
                token = action.redeem_token


                # result = redeem(token.name, amount)

                self.atom_actions.append((action.name, (redeem, [token.name, amount])))
                # if result:
                #     cost = self.system.evaluate_price(token, amount)
                #     self.update_cost(token, amount, cost)
                #     self.last_gen[DUET] = result
                # else:
                #     # print('failed to redeem')
                #     break_plan(action)

            elif action.name == FRAMWITHDRAW:
                # # print('farm with draw')
                amount = action.farm_withdraw_amount
                farm_pool = action.farm_pool


                # result = farm_withdraw(farm_pool.name, amount)
                self.atom_actions.append((action.name, (farm_withdraw, [farm_pool.name, amount])))
                # if not result:
                #     for k,v in result.items():
                #         self.last_gen[k] = v
                #     # print('failed to withdraw')
                #     break_plan(action)

            elif action.name == STAKEWITHDRAW:
                amount = action.stake_withdraw_amount
                

                # result = stake_withdraw(amount)
                self.atom_actions.append((action.name, (stake_withdraw, [amount])))

                # if result:
                #     self.last_gen[DUET] = amount
                # else:
                #     break_plan(action)
                #     # print('failed to stake')

            else:
                raise Exception('unkown action')

    def update_cost(self, token, amount, cost):
        if not isinstance(token, str):
            token = token.name

        token = self.get_token_by_name(token)
        # past_cost = token.token_cost
        # if not past_cost:
        #     past_cost = 0
        past_cost = self.unit_cost[token]
        if past_cost == -1:
            past_cost = 0

        # each agent start from only usdt token
        past_amount = self.states[token]
        total_amount = past_amount + amount
        total_cost = past_amount * past_cost + cost
        token_cost = total_cost / total_amount
        # token.token_cost = token_cost
        self.unit_cost[token] = token_cost

    def quit(self):
        self.state = -1

    def dasset_farming_from_usdt(self, init=False):
        """ here is common farming process of agent
            from the beginning as agent hold usdt
        """

        create_action = self.belief.create_action
        onto = self.belief.onto
        target_token = onto.myself.desire_token
        target_pool = onto.myself.desire_pool
        operate_amount = onto.myself.operate_amount
        count = 0
        # if operate_amount > self.states[USDT]:
        #     operate_amount = self.states[USDT]

        # operate_amount = (operate_amount / 5000) * self.states[target_token.name]
        if not self.farm_flag:
            return []

        if target_pool.has_apy < onto.myself.expect_apy and not init:
            # if self.states[DUET] >= self.mini_amount * 10:
                # plan = Plan.choose_swap_plan(onto.DUET, onto.USDT, self, operate_amount)
            # else:
                # plan = []
            farm_flag = False
            return []
            # return plan


        farm_flag = True
        # if target_pool.has_apy < onto.myself.expect_apy:
        #     farm_flag = False
        # else:
        #     farm_flag = True
        # if not self.farm_flag:
        #     farm_flag = False


        # when tax too high, no farm
        # if self.system.get_tax(DUET) >= self.tax_accept*onto.DUET.current_uniswap_price :
        #     return []


        if self.states[USDT] < operate_amount:
            operate_amount = self.states[USDT]

        
        if target_token == onto.ZUSD:

            if target_pool == onto.ZUSD_USDT:
                # two ways to get the ZUSD, agent will choose the cheaper one
                # only considering the processes in two steps
                # agent only judge from current prices
                fraction = 0.5

                if self.states[ZUSD] < fraction * operate_amount:
                    plan = Plan.choose_swap_plan(onto.USDT, onto.ZUSD, self, fraction * operate_amount)

                    for action in plan:
                        self.add_action(action)

                farm_action = create_action(
                    _type = FARM,
                    farm_pool = target_pool,
                    farm_token1_amount = MAX,
                    farm_token2_amount = MAX
                )
                if farm_flag:
                    self.add_action(farm_action)

            elif target_pool == onto.ZBTC_ZUSD:
                fraction = 0.5


                token_prie = onto.ZBTC.current_uniswap_price

                if self.states[ZBTC] < fraction * operate_amount/token_prie:
                    plan = Plan.choose_swap_plan(onto.USDT, onto.ZBTC, self, fraction * operate_amount, 0, 0)
                
                    for action in plan:
                        self.add_action(action)
                        count = Plan.count_swap(plan)
                else:
                    count = 0


                if self.states[ZUSD] < fraction * operate_amount:
                    plan = Plan.choose_swap_plan(onto.USDT, onto.ZUSD, self, fraction * operate_amount, count, 1)

                    for action in plan:
                        self.add_action(action)


                farm_action = create_action(
                    _type = FARM,
                    farm_pool = target_pool,
                    farm_token1_amount = MAX,
                    farm_token2_amount = MAX
                )
                if farm_flag:
                    self.add_action(farm_action)

            elif target_pool == onto.ZNAS_ZUSD:
                fraction = 0.5
                

                token_prie = onto.ZNAS.current_uniswap_price

                if self.states[ZNAS] < fraction * operate_amount/token_prie:
                    plan = Plan.choose_swap_plan(onto.USDT, onto.ZNAS, self, fraction * operate_amount, 0, 0)
                
                    for action in plan:
                        self.add_action(action)
                        count = Plan.count_swap(plan)
                else:
                    count = 0


                if self.states[ZUSD] < fraction * operate_amount:
                    plan = Plan.choose_swap_plan(onto.USDT, onto.ZUSD, self, fraction * operate_amount, count, 1)

                    for action in plan:
                        self.add_action(action)


                farm_action = create_action(
                    _type = FARM,
                    farm_pool = target_pool,
                    farm_token1_amount = MAX,
                    farm_token2_amount = MAX
                )
                if farm_flag:
                    self.add_action(farm_action)
               

        elif target_token == onto.ZBTC:

                fraction = 0.5

                token_prie = onto.ZBTC.current_uniswap_price

                if self.states[ZBTC] < fraction * operate_amount/token_prie:
                    plan = Plan.choose_swap_plan(onto.USDT, onto.ZBTC, self, fraction * operate_amount, 0, 0)
                
                    for action in plan:
                        self.add_action(action)
                        count = Plan.count_swap(plan)
                else:
                    count = 0


                if self.states[ZUSD] < fraction * operate_amount:
                    plan = Plan.choose_swap_plan(onto.USDT, onto.ZUSD, self, fraction * operate_amount, count, 1)

                    for action in plan:
                        self.add_action(action)



                farm_action = create_action(
                    _type = FARM,
                    farm_pool = target_pool,
                    farm_token1_amount = MAX,
                    farm_token2_amount = MAX
                )
                if farm_flag:
                    self.add_action(farm_action)
        
        elif target_token == onto.ZNAS:
                fraction = 0.5
                
                token_prie = onto.ZNAS.current_uniswap_price

                if self.states[ZNAS] < fraction * operate_amount/token_prie:
                    plan = Plan.choose_swap_plan(onto.USDT, onto.ZNAS, self, fraction * operate_amount, 0, 0)
                
                    for action in plan:
                        self.add_action(action)
                        count = Plan.count_swap(plan)
                else:
                    count = 0


                if self.states[ZUSD] < fraction * operate_amount:
                    plan = Plan.choose_swap_plan(onto.USDT, onto.ZUSD, self, fraction * operate_amount, count, 1)

                    for action in plan:
                        self.add_action(action)




                farm_action = create_action(
                    _type = FARM,
                    farm_pool = target_pool,
                    farm_token1_amount = MAX,
                    farm_token2_amount = MAX
                )
                if farm_flag:
                    self.add_action(farm_action)

    def dasset_farming_from_duet(self, init=False):
        """ here is common farming process each time it get duet
        """

        if not self.farm_flag:
            return 

        create_action = self.belief.create_action
        onto = self.belief.onto
        target_token = onto.myself.desire_token
        target_pool = onto.myself.desire_pool
        operate_amount = onto.myself.operate_amount
        # operate_amount = (operate_amount/5000) * self.states[DUET]
        farm_flag = True
        # if target_pool.has_apy < onto.myself.expect_apy:
        #     if self.states[DUET] >= self.mini_amount * 10:
        #         plan = Plan.choose_swap_plan(onto.DUET, onto.USDT, self, operate_amount)
        #     else:
        #         plan = []
        #     return plan
        if target_pool.has_apy < onto.myself.expect_apy and not init:
            return []

        # if not self.farm_flag:
        #     farm_flag = False
            
        if self.states[DUET] < operate_amount:
            operate_amount = self.states[DUET]

        # if self.system.get_tax(target_token.name) >= target_token.has_price:
            # return []
        # when the rate is too high, not farm
        # if self.system.get_tax(DUET) >=  onto.DUET.current_uniswap_price* self.tax_accept:
        #     return []

        count = 0
        if target_token == onto.ZUSD:

            if target_pool == onto.ZUSD_USDT:
                # two ways to get the ZUSD, agent will choose the cheaper one
                # only considering the processes in two steps
                # agent only judge from current prices
                # fraction = onto.ZUSD_USDT.has_fraction
                fraction = 0.5
                
                if self.states[USDT] <= operate_amount*fraction:
                    plan = Plan.choose_swap_plan(onto.DUET, onto.USDT, self, fraction * operate_amount,0, 0)

                    for action in plan:
                        self.add_action(action)
                    count = Plan.count_swap(plan)
                else:
                    count = 0

                if self.states[ZUSD] <= operate_amount*fraction:
                    plan = Plan.choose_swap_plan(onto.DUET, onto.ZUSD, self, fraction * operate_amount, count, 1)

                    for action in plan:
                        self.add_action(action)

                farm_action = create_action(
                    _type = FARM,
                    farm_pool = target_pool,
                    farm_token1_amount = MAX,
                    farm_token2_amount = MAX
                )
                if farm_flag:
                    self.add_action(farm_action)

            elif target_pool == onto.ZBTC_ZUSD:
                fraction = 0.5
                token_prie = onto.ZBTC.current_uniswap_price

                if self.states[ZBTC] <= operate_amount*fraction /token_prie:
                    plan = Plan.choose_swap_plan(onto.DUET, onto.ZBTC, self, fraction * operate_amount, 0, 0)
                
                    for action in plan:
                        self.add_action(action)
                        count = Plan.count_swap(plan)
                    else:
                        count = 0


                if self.states[ZUSD] <= operate_amount*fraction:
                    plan = Plan.choose_swap_plan(onto.DUET, onto.ZUSD, self, fraction * operate_amount, count, 1)

                    for action in plan:
                        self.add_action(action)


                farm_action = create_action(
                    _type = FARM,
                    farm_pool = target_pool,
                    farm_token1_amount = MAX,
                    farm_token2_amount = MAX
                )
                if farm_flag:
                    self.add_action(farm_action)

            
            elif target_pool == onto.ZNAS_ZUSD:
                fraction = 0.5

                token_prie = onto.ZNAS.current_uniswap_price

                if self.states[ZNAS] <= operate_amount*fraction /token_prie:
                    plan = Plan.choose_swap_plan(onto.DUET, onto.ZNAS, self, fraction * operate_amount, 0, 0)
                
                    for action in plan:
                        self.add_action(action)
                        count = Plan.count_swap(plan)
                    else:
                        count = 0

                
                if self.states[ZUSD] <= operate_amount*fraction:
                    plan = Plan.choose_swap_plan(onto.DUET, onto.ZUSD, self, fraction * operate_amount, count, 1)

                    for action in plan:
                        self.add_action(action)



                farm_action = create_action(
                    _type = FARM,
                    farm_pool = target_pool,
                    farm_token1_amount = MAX,
                    farm_token2_amount = MAX
                )
                if farm_flag:
                    self.add_action(farm_action)
               
        elif target_token == onto.ZBTC:

                fraction = 0.5

                token_prie = onto.ZBTC.current_uniswap_price

                if self.states[ZBTC] <= operate_amount*fraction /token_prie:
                    plan = Plan.choose_swap_plan(onto.DUET, onto.ZBTC, self, fraction * operate_amount, 0, 0)
                
                    for action in plan:
                        self.add_action(action)
                        count = Plan.count_swap(plan)
                    else:
                        count = 0


                if self.states[ZUSD] <= operate_amount*fraction:
                    plan = Plan.choose_swap_plan(onto.DUET, onto.ZUSD, self, fraction * operate_amount, count, 1)

                    for action in plan:
                        self.add_action(action)


                farm_action = create_action(
                    _type = FARM,
                    farm_pool = target_pool,
                    farm_token1_amount = MAX,
                    farm_token2_amount = MAX
                )

                if farm_flag:
                    self.add_action(farm_action)
        
        elif target_token == onto.ZNAS:
                fraction = 0.5

                token_prie = onto.ZNAS.current_uniswap_price

                if self.states[ZNAS] <= operate_amount*fraction /token_prie:
                    plan = Plan.choose_swap_plan(onto.DUET, onto.ZNAS, self, fraction * operate_amount, 0, 0)
                
                    for action in plan:
                        self.add_action(action)
                        count = Plan.count_swap(plan)
                    else:
                        count = 0

               
                if self.states[ZUSD] <= operate_amount*fraction:
                    plan = Plan.choose_swap_plan(onto.DUET, onto.ZUSD, self, fraction * operate_amount, count, 1)

                    for action in plan:
                        self.add_action(action)


                farm_action = create_action(
                    _type = FARM,
                    farm_pool = target_pool,
                    farm_token1_amount = MAX,
                    farm_token2_amount = MAX
                )
                if farm_flag:
                    self.add_action(farm_action)

    def get_total_value(self):
        value = 0
        for token in [USDT, ZUSD, ZBTC, ZNAS, DUET]:
            value += self.system.get_usdt_price(token) * self.states[token]

        for pool in [DUET_USDT, ZUSD_USDT, ZBTC_ZUSD, ZNAS_ZUSD]:
            value += self.system.get_pool_lp_value(pool, self.states[pool])

        value += self.system.get_usdt_price(DUET) * self.states[STAKE]

        return value

    def step_one_atom_action(self):
        # if self.unique_id == 104 and self.system.timeline.tick==36:
        if self.system.blockchain.turn_on:
            self.prepare_gas()
        if self.unique_id == 103:
            print('debug')

        if not self.atom_actions:
            return False

        action = self.atom_actions.pop(0)
        name = action[0]
        # # print("agnt {}, with desire {} is taking action {}".format(self.unique_id, self.desire.name, name))
        action = action[1]
        prince1 = self.system.get_current_usdt_price(DUET)
        if action[1]:
            result = action[0](*action[1])
        else:
            result = action[0]()
        price2 = self.system.get_current_usdt_price(DUET)
        # if not result:
        #     # # print('debug')
        #     # print("step {}, agnt {}, with desire {} is taked action {}, but failed".format(self.system.timeline.tick, self.unique_id, self.desire.name, name))
        if price2 > prince1:
        # #     # print(action[1])
        # #     # print(name)
            # # print("step {}, agnt {}, with desire {} is taked action {}, make DUET price rise".format(self.system.timeline.tick, self.unique_id, self.desire.name, name))
            pass
        #     # # print(prince1)
        #     # print('pre')
        #     # print(self.states[ACTION])
        #     # print('after')
        #     # print(self.atom_actions)
        #     # print('a')

        elif price2 < prince1:
        # #     # print(action[1])
        # #     # print(name)
            # # print("step {}, agnt {}, with desire {} is taked action {}, make DUET price down".format(self.system.timeline.tick, self.unique_id, self.desire.name, name))
            pass
        # #     # print('ss')

            
        return True

    def get_atom_step_length(self):
        return len(self.atom_actions)

    def step(self):
        if self.state == -1:
            return True

        self.observe()

        if self.state == 0:
            self.init_think()
            self.state = 1
        else:
            self.think()

        self.execute()

        self.atom_actions.append(('upate-states', (self.update_states, [])))

        # backup_state = deepcopy(self.states)
        # backup_state = copy.deepcopy(self.states)
        return True

    def update_states(self):
        new_states = {k:v for k,v in self.states.items()}
        self.states_hist.append((self.system.timeline.tick, new_states))
        self.states[ACTION] = []

        if self.states[DUET] < 0:
            print('debug')
        return True

    def withdraw_all(self):
        for pool in [DUET_USDT, ZBTC_ZUSD, ZNAS_ZUSD, ZUSD_USDT]:
            if self.states[pool]:
                amount = self.states[pool]
                result = self.system.farm_withdraw(self, pool, amount)
                if not result:
                    print('error: withdraw all agent failed')
                
                else:
                    values = list(result.values())

                    self.record({
                        '_type': 'farm_withdraw',
                        'farm_pool': pool,
                        'withdraw_amount': amount,
                        'result': values[0],
                        'result2': values[1]
                    })
    
    def prepare_gas(self):
        # simulate that person will swap some of his token into gas fee
        # the wap is outside the system
        prices = {
            ZUSD: self.belief.onto.ZUSD.current_uniswap_price,
            ZBTC: self.belief.onto.ZBTC.current_uniswap_price,
            ZNAS: self.belief.onto.ZNAS.current_uniswap_price,
            DUET: self.belief.onto.DUET.current_uniswap_price
        }

        limit = 42 * 4
        self.mini_amount_usdt = self.mini_amount + limit
        if self.states[USDT] <= limit:
            for key in [DUET, ZUSD, ZBTC, ZNAS]:
                if self.states[key] * prices[key] >= limit:
                    self.states[USDT] += limit
                    self.states[key] -=  limit/prices[key]

desire_dict = {
    HOLDFOUNDER: HoldFounder,
    SELLFOUNDER : SellFounder,
    DUETHOLD: DuetHold,
    DUETHOLDANDFARM: DuetHoldAndFarm,
    DUETHOLDANDSTAKE: DuetHoldAndStake,
    DASSETHOLD: DAssetHold,
    DASSETHOLDANDFARM: DAssetHoldAndFarm,
    SHORTFARMARBITRAGE: ShortFarmArbitrage,
    SPREAD: Spread,
    BULLISHDUET: BullishDUET,
    BULLISHDASSET: BullishDAsset,
    BEARISHDUET: BearrishDUET,
    BEARISHDASSET: BearrishDAsset,
    TRADER: Trader
}

class AgentFactory:

    @staticmethod
    def create_agent(unique_id: int, states: dict, system, _type: str, desire_token: Cryptocurrency=None,
     desire_pool: LiquidityPool=None, operate_amount: float = 100, short_farming_sell_time: float = 10,
     bullish_expect_rise:float = 0.1, bearish_stand_drop:float = 0.1, founder_sell_time: float = 60, incent_limit_benefit:float = 10,
     expect_apy = 0.1):
        """
        states = {
            'DUET': 0,
            'USDT': 0,
            'ZUSD': 0,
            'ZBTC': 0,
            'ZNAS': 0
        }
        """
        states = {k:v for k,v in states.items()}

        desire = desire_dict[_type]()
        belief = Belief(unique_id)
        agent = Agent(unique_id, states, belief, system)
        agent.set_desire(desire)

        onto = belief.onto

        token_dict = {
            USDT : onto.USDT,
            ZUSD : onto.ZUSD,
            ZBTC : onto.ZBTC,
            ZNAS : onto.ZNAS,
            DUET : onto.DUET
        }

        pool_dict = {
            DUET_USDT : onto.DUET_USDT,
            ZUSD_USDT : onto.ZUSD_USDT,
            ZBTC_ZUSD : onto.ZBTC_ZUSD,
            ZNAS_ZUSD : onto.ZNAS_ZUSD
        }

        if desire_token:
            desire_token = token_dict.get(desire_token)

        if desire_pool:
            desire_pool = pool_dict.get(desire_pool)

        # set the varibales of agent
        agent.set_bullish_expect_rise(bullish_expect_rise)
        agent.set_desire_token(desire_token)
        agent.set_desire_pool(desire_pool)
        agent.set_operate_amount(operate_amount)
        agent.set_short_farming_sell_time(short_farming_sell_time)
        agent.set_bearish_stand_drop(bearish_stand_drop)
        agent.set_founder_sell_time(founder_sell_time)
        agent.set_agent_incent_limit(incent_limit_benefit)
        agent.set_agent_expect_apy(expect_apy)
        return agent