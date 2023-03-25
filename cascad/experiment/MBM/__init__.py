from cascad.agents.aritifcial_system.chain import  ChainBase
from cascad.agents.aritifcial_system.contracts.token.ERC20 import ERC20
from cascad.aritificial_world import World
from cascad.aritificial_world.scheduler import BaseScheduler
from cascad.aritificial_world.timeline import TimeLine
from cascad.experiment.cdec import Cdec
from cascad.models.datamodel import ComputeExperimentModel, ExperimentResultModel
from cascad.models.kb import Entity, Property
from cascad.experiment.token_sender.agents import RandomAgent
from cascad.experiment import  Experiment
import uuid
from cascad.experiment.MBM.MBM import MBMSystem
from cascad.experiment.MBM.constant import  *
from cascad.scenario_generator.parallel import ParallelScenario
from cascad.experiment.MBM.agent import AgentFactory
from cascad.experiment.MBM.desires import *
from tqdm import tqdm
# import threading
from multiprocessing import Process, Pool
from cascad.settings import BASE_DIR

has_chain = Property("has_chain", "has_chain")


import numpy as np
import os
import csv
import json
from random import randint, random, choice, shuffle
import math


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
    BEARISHDASSET: BearrishDAsset
}

desire_dict = {
    MINTMODEL : [
        DUETHOLDANDFARM, DASSETHOLDANDFARM, SHORTFARMARBITRAGE, SPREAD, BULLISHDASSET, BEARISHDASSET, DASSETHOLD
    ],

    REDEEMMODEL : [
        SHORTFARMARBITRAGE, SPREAD, BULLISHDASSET, BEARISHDASSET
    ],

    SWAPMODEL : [
        DUETHOLDANDFARM, DASSETHOLDANDFARM, SHORTFARMARBITRAGE, SPREAD, BULLISHDASSET, BULLISHDUET, BEARISHDUET, BEARISHDASSET, DUETHOLD
    ],

    FARMINGMODEL : [
        DUETHOLDANDFARM, DASSETHOLDANDFARM, SHORTFARMARBITRAGE
    ],

    STAKINGMODEL : [
        DUETHOLDANDSTAKE
    ]
}


class Sample(object):
    def gen(self, pop_num):
        pop = []
        for i in range(pop_num):
            pop.append({
                'code': [0.1, 0.1, 0.1, 0.2, 0.3, 0.2]
            })


class MBMCdec(Cdec):
    def __init__(self):
        pass

    
    def encode(self, code):
        file_path = 'experiment_{}.json'.format(code[0])
        return{
            'code': code,
            'experiment': MBMExperiment(file_path)
        }        

class MBMSample(Sample):
    def __init__(self) -> None:
        self.unique_id = -1 
        super().__init__()

    def sample_experiment(self, num):
        result = []
        for _ in range(num):
            result.append([self.next_id()])
        return result
        
    def next_id(self):
        self.unique_id += 1
        return self.unique_id


class MBMExperiment(Experiment):
    def __init__(self, file_path = '', start_reward_day=0, trade_limit = 500, price_change=False, no_reward=False, low_liquity=False, high_gas=False, different_ratio=[0.1, 0.2, 0.3, 0.3,0.1], init_token = 5000, code=[]):
        self.timeline = TimeLine()
        self.duet_system = MBMSystem(self.timeline)
        self._name = "MBM Experiment"
        self.max_step = 730 # run 2 years 730 day
        # self.max_step = 180

        self.scheduler = BaseScheduler(self, self.next_id())
        self.agent_uniq_id = -1
        self.unique_id = self.next_id()
        self.running = True
        self.max_agent = 720

        # for priace dramatically changing
        # self.price_change = price_change
        if price_change:
            self.set_price_changing()

        self.no_reward = no_reward
        self.no_reward_flag = False
        self.no_liquity = low_liquity
        self.no_farm_flag = False

        self.high_gas = high_gas
        self.gas_fee_flag = False


        self.init_experiment()

        self.model_counter = {
            MINTMODEL : 0,
            REDEEMMODEL : 0,
            SWAPMODEL : 0,
            FARMINGMODEL : 0,
            STAKINGMODEL : 0
        }

        self.result= []
        self.code = code

        # self.collector = DataCollector(self.duet_system, self.scheduler, self.timeline, file_path)
        # self.system_collector = DataCollector(self.duet_system, self.scheduler, self.timeline, file_path)

        self.collector = DataCollector(self.duet_system, self.scheduler, self, self.timeline, file_path)
        self.start_reward_day = start_reward_day

        self.model_list = [MINTMODEL, REDEEMMODEL, SWAPMODEL, FARMINGMODEL, STAKINGMODEL]
        different_ratio = [int(x * 100) for x in different_ratio]
        # # print(different_ratio)
        # different_ratio = [x if x > 0 else 1 for x in different_ratio]
        # self.desire_list = [DUETHOLDANDFARM, DASSETHOLDANDFARM, SHORTFARMARBITRAGE, SPREAD, BULLISHDASSET, BULLISHDUET, BEARISHDUET, BEARISHDASSET, DUETHOLD]

        self.desire_list = [DUETHOLDANDFARM, DUETHOLD] * different_ratio[0]  + [DASSETHOLDANDFARM, DASSETHOLD, SHORTFARMARBITRAGE] * different_ratio[1] + [BULLISHDASSET, BULLISHDUET] * different_ratio[2] + [BEARISHDASSET, BEARISHDUET] * different_ratio[3] + [SPREAD] * different_ratio[4] + [DUETHOLD]
        self.trade_limit = trade_limit
        # self.pbar = tqdm(total=self.max_step)
        self.init_token = init_token

        # ComputeExperimentModel(
        #     unique_id=self.unique_id,
        #     experiment_name = self._name,
        #     status = "Start"
        # ).save()

    def next_id(self) -> str:
        return uuid.uuid4().hex   
    def init_experiment(self):

        # prie changing
        # if self.price_dramatically:
            # self.change_token_prices()

        # if self.cut_the_liquidity:
            # self.        # sepcical_agent
        speci_states = {
            USDT : 0,
            DUET : 0,
            ZUSD : 0,
            ZBTC : 0,
            ZNAS : 0,
            STAKE: 0,
            DUET_USDT : 0.9,
            ZUSD_USDT : 0.9,
            ZBTC_ZUSD : 0.9,
            ZNAS_ZUSD : 0.9,
            STAKE_REWARD : 0,
            FARM_REWARD : 0
        }
        operate_amount = self.get_operate_amount()
        self.special_agent = AgentFactory.create_agent(self.next_id(), speci_states, self.duet_system, HOLDFOUNDER)



        states = {
            USDT : 0,
            DUET : 100000,
            ZUSD : 0,
            ZBTC : 0,
            ZNAS : 0,
            STAKE: 0,
            DUET_USDT : 0,
            ZUSD_USDT : 0,
            ZBTC_ZUSD : 0,
            ZNAS_ZUSD : 0,
            STAKE_REWARD : 0,
            FARM_REWARD : 0
        }


        for _ in range(10):
            operate_amount = self.get_operate_amount()
            agent = AgentFactory.create_agent(self.next_id(), states, self.duet_system, HOLDFOUNDER, operate_amount=operate_amount)

            # agent.step()
            self.scheduler.add(agent)


        for _ in range(10):
            operate_amount = self.get_operate_amount()
            sell_time = self.get_founder_sell_time()
            bearish_stand_drop = self.get_bearish_stand_drop() # bearish
            agent = AgentFactory.create_agent(self.next_id(), states, self.duet_system, SELLFOUNDER, operate_amount=operate_amount, founder_sell_time=sell_time, bearish_stand_drop=bearish_stand_drop)
             
            # agent.step()
            self.scheduler.add(agent)

    def new_agent(self):
        dice = randint(0, 4)
        # focus_model = self.model_list[dice]

        states = {
            USDT : self.init_token,
            DUET : 0,
            ZUSD : 0,
            ZBTC : 0,
            ZNAS : 0,
            STAKE: 0,
            DUET_USDT : 0,
            ZUSD_USDT : 0,
            ZBTC_ZUSD : 0,
            ZNAS_ZUSD : 0,
            STAKE_REWARD : 0,
            FARM_REWARD : 0
        }

        # for test
        
        # desires = desire_dict[focus_model]
        # if SPREAD in desires:
        #     desires.remove(SPREAD)

        # gen datas
        # agent_number = randint(1, 10)
        agent_number = 10
        if (self.timeline.tick) % 7 == 0 and self.timeline.tick < 700:

            # this assume special traders
            # self.add_trader()

            # this assume trader normal
            agent_number = 11

        for _ in range(agent_number):
            focus_model = choice(self.model_list)
            # desires = desire_dict[focus_model]
            # desire = choice(desires)
            desire = choice(self.desire_list)
            desire_token, desire_pool = self.get_desire_token_and_pool() # used only when desire is dassetinvest
            # if desire == BULLISHDUET:
            #     # print('debug')
            short_farming_sell_time = self.get_short_farming_sell_time() # used only when desire is short farming
            operate_amount = self.get_operate_amount() # spread
            bullish_expect_rise = self.get_bullish_expect_rise() # bullish
            bearish_stand_drop = self.get_bearish_stand_drop() # bearish
            founders_sell_time =self.get_founder_sell_time() # sell founder
            expect_apy = self.get_farm_expect_apy()
            accept_no_reward = self.get_accept_no_reward()


            agent = AgentFactory.create_agent(
                self.next_id(), states, self.duet_system, desire, desire_token, desire_pool, 
                operate_amount, short_farming_sell_time, bullish_expect_rise, bearish_stand_drop, founders_sell_time, expect_apy=expect_apy
            )
            agent.set_focus_model(focus_model)
            agent.set_accept_no_reward(accept_no_reward)
            self.scheduler.add(agent)
            self.model_counter[focus_model] += 1
            if self.model_counter[focus_model] >= 1500:
                self.model_list.remove(focus_model)
                focus_model = choice(self.model_list)
            
            if len(self.scheduler.agents) >= self.max_agent:
                self.random_remove_agent()
            # agent.step()


    def add_trader(self, num=1):
        dice = randint(0, 4)
        # focus_model = self.model_list[dice]

        states = {
            USDT : 10000,
            DUET : 10000,
            ZUSD : 0,
            ZBTC : 0,
            ZNAS : 0,
            STAKE: 0,
            DUET_USDT : 0,
            ZUSD_USDT : 0,
            ZBTC_ZUSD : 0,
            ZNAS_ZUSD : 0,
            STAKE_REWARD: 0,
            FARM_REWARD: 0
        }

        # desires = desire_dict[focus_model]
        # agent_number = randint(1, 10)
        for _ in range(num):
            desire = TRADER
            desire_token, desire_pool = self.get_desire_token_and_pool() # used only when desire is dassetinvest
            short_farming_sell_time = self.get_short_farming_sell_time() # used only when desire is short farming
            operate_amount = self.get_operate_amount() # spread
            bullish_expect_rise = self.get_bullish_expect_rise() # bullish
            bearish_stand_drop = self.get_bearish_stand_drop() # bearish
            founders_sell_time =self.get_founder_sell_time() # sell founder

            agent = AgentFactory.create_agent(
                self.next_id(), states, self.duet_system, desire, desire_token, desire_pool, 
                operate_amount, short_farming_sell_time, bullish_expect_rise, bearish_stand_drop, founders_sell_time
            )
            # agent.set_focus_model(focus_model)
            self.scheduler.add(agent)
            self.random_remove_agent()

    # def next_id(self):
    #     self.agent_uniq_id += 1
    #     return self.agent_uniq_id

    def get_desire_token_and_pool(self):
        """ how to choose desire token and pool of each agent
        """
        token_list = [ZUSD, ZBTC, ZNAS]
        desire_token = choice(token_list)
        if desire_token == ZUSD:
            desire_pool = choice([ZUSD_USDT, ZBTC_ZUSD, ZNAS_ZUSD])
        elif desire_token == ZBTC:
            desire_pool = ZBTC_ZUSD
        elif desire_token == ZNAS:
            desire_pool = ZNAS_ZUSD

        return desire_token,desire_pool

    def get_operate_amount(self):
        operate_amount_list =  list(range(50, 800, 40))
        return choice(operate_amount_list)

    def get_short_farming_sell_time(self):
        sell_time_list = list(range(10, 60, 1))
        return choice(sell_time_list)

    def get_bullish_expect_rise(self):
        expect_rise_list = list(np.arange(0.1, 0.5, 0.01))
        expect_rise_list = [float(v) for v in expect_rise_list]
        return choice(expect_rise_list)

    def get_bearish_stand_drop(self):
        stand_drop_list = list(np.arange(0.1, 0.5, 0.01))
        stand_drop_list = [float(v) for v in stand_drop_list]
        return choice(stand_drop_list)

    def get_farm_expect_apy(self):
        expect_apy = list(np.arange(0.1, 0.8, 0.1))
        expect_apy = [float(v) for v in expect_apy]
        return choice(expect_apy)

    def get_founder_sell_time(self):
        founder_sell_time = list(range(60, 700, 1))
        return choice(founder_sell_time)
    def get_accept_no_reward(self):
        dice = random()
        if dice <= 0.1: # only one percentage agent accept this
            return True
        else:
            return False

    def set_price_changing(self):
        # days = [100, 300, 500]
        # days2 = [ 200, 400, 600]
        # very_high = [1, 31, 61, 91]
        # very_low = [121, 151, 181, 211]
        # medium_high = []
        # medium_low = [] 
        very_high = list(range(1, 7)) + list(range(31, 37)) + list(range(61, 67)) + list(range(91, 97)) + list(range(121, 127)) + list(range(151, 157)) 
        very_low = list(range(181, 187)) + list(range(211, 217)) + list(range(241, 247)) + list(range(271, 277)) + list(range(301, 307)) + list(range(331, 337))
        medium_high = list(range(361, 367)) + list(range(391, 397)) + list(range(421, 427)) + list(range(451, 457)) + list(range(481, 487)) + list(range(511, 517))
        medium_low = list(range(541, 547)) + list(range(571, 577)) + list(range(601, 607)) + list(range(631, 637)) + list(range(661, 667)) + list(range(691, 697))

        self.duet_system.oracle.set_price(BTC, very_high, 2) # 1/0.5
        self.duet_system.oracle.set_price(BTC, very_low, 0.5)
        self.duet_system.oracle.set_price(BTC, medium_high, 4/3) # 1/0.75
        self.duet_system.oracle.set_price(BTC, medium_low, 0.75)

        # self.duet_system.oracle.set_price(BTC, days, 2)
        # self.duet_system.oracle.set_price(NAS, days2, 2)
        
    def set_no_reward(self):
        # start_day = 360
        start_day = 365
        end_day = 750
        if self.no_reward:
            if self.timeline.tick >= start_day and self.timeline.tick <= end_day:
                self.no_farm_flag = True
                self.no_reward_flag = True

    def set_no_liquity(self):
        # start_day = 360
        start_day = 365  # test

        end_day = 750
        if self.no_liquity:
            if self.timeline.tick >= start_day and self.timeline.tick <= end_day:
                self.no_farm_flag = True

    def set_high_gas(self):
        start_day = 365
        end_day = 750
        if self.high_gas:
            if self.timeline.tick >= start_day and self.timeline.tick <= end_day:
                # self.gas_fee_flag= True
                self.duet_system.blockchain.set_turn_on()
            else:
                self.duet_system.blockchain.set_turn_off()

    def random_remove_agent(self):
        agent_index = list(range(len(self.scheduler.agents)))
        agent_index = agent_index[100:]
        index = choice(agent_index)
        self.scheduler.remove(self.scheduler.agents[index])

    def step(self):

        self.new_agent() # each day new agent coming
        # self.scheduler.step()
        # for test
        if self.no_reward:
            self.set_no_reward()

        if self.no_liquity:
            self.set_no_liquity()

        if self.high_gas:
            self.set_high_gas()

        for agent in self.scheduler.agents:
            if self.no_reward_flag:
                agent.stop_farm()
                agent.withdraw_all()
            if self.no_farm_flag:
                if not self.no_reward_flag:
                    self.special_agent.withdraw_all()
                if not agent.accept_no_reward:
                    agent.stop_farm()
                    agent.withdraw_all()
                    

            else:
                agent.resume_farm()
            # if self.timeline.tick == 1 and self.agent_uniq_id==100:
                # print('debug')

            agent.init_atom_actions()
        # limit the agent trade number
        agent_index = list(range(len(self.scheduler.agents)))


        shuffle(agent_index)
        agent_index = agent_index[:20]
        flag = True
        while agent_index:
            index = choice(agent_index)
            agent = self.scheduler.agents[index]
            flag = agent.step_one_atom_action()
            if not flag:
                agent_index.remove(index)


        if self.timeline.tick == 30:
            # print('debug')
            pass

        self.timeline.step()
        self.duet_system.step()
        if self.timeline.tick >= self.start_reward_day and not self.no_reward_flag:
            self.duet_system.reward(self.scheduler.agents)
        # print('step {} '.format(self.timeline.tick))
        # print(self.duet_system.uniswap.states['prices']['value'])
        # print('agent_number {}'.format(len(self.scheduler.agents)))
        # self.pbar.update(1)
        if self.timeline.tick >= self.max_step:
            self.running = False
            # self.pbar.close()
            # self.save_result()
            self.compute_result()
            # print(self.result)

        self.collector.step()
        self.result.append(self.collector.get_record(self.timeline.tick, self.code))

    def save_result(self):
        for data in self.result:
            ExperimentResultModel(experiment_id = self.unique_id, day=data[0], result=data[1:], code=self.code).save()
            pass

    def compute_result(self):
        # average = sum([ abs(x[1] - x[2])/(x[1] + x[2]) + abs(x[3] - x[4])/(x[3] + x[4]) + abs(x[7] - x[8])/(x[7] + x[8]) + abs(x[9] - x[10])/(x[9] + x[10]) for x in self.result] )/ len(self.result)
        average = sum([ abs(x[1] - x[2])+ abs(x[3] - x[4])+ abs(x[7] - x[8])+ abs(x[9] - x[10]) for x in self.result] )/ len(self.result)

        self.result= [average, self.result]

class DuetParallel(ParallelScenario):
    def __init__(self, popsize, ngen, sample, cdec, result_path: str):
        super().__init__(popsize, ngen, sample, cdec, result_path)
        pops = self.sample.sample_experiment()
        self.pops = [
            self.cdec.encode(experiment) for experiment in pops
        ]

    def start(self):
        for iter in range(self.ngen):
            # print('_' * 10  + '_____iter_{}______'.format(iter) + '_' * 10)
            for experiment in self.pops:
                while experiment.running:
                    experiment.step()

                    
class DataCollector:
    def __init__(self, duet_system, scheduler, experiment, timeline, file_path='result', split=30) -> None:
        self.duet_system = duet_system
        self.scheduler = scheduler
        # self.file_path = file_path
        self.file_path = os.path.join(BASE_DIR, 'resources', file_path)
        if not os.path.exists(self.file_path):
            os.mkdir(self.file_path)
        # self.json_file_path = file_path + ".json"
        # self.csv_file_path = os.path.join(BASE_DIR, file_path, 'result.csv')
        # self.csv_file_path = file_path + '.csv'
        self.timeline = timeline
        # self.init_file()
        self.split = split
        self.result = []
        self.experiment = experiment

    def get_record(self, day=0, code=[]):
        uniswap_states = self.duet_system.uniswap.states
        redeemmint_states = self.duet_system.mintRedeemModel.states
        stake = self.duet_system.staker.states[TOTAL]
        staker_states = self.duet_system.staker.states
        oracle = self.duet_system.oracle

        data = [
            day, 
            uniswap_states[PRICES][VALUE][ZUSD],
            # uniswap_states[PRICES][TRADINGVALUE][ZUSD],
            # uniswap_states[PRICES][LOW][ZUSD],
            # uniswap_states[PRICES][HIGH][ZUSD],
            1,


            uniswap_states[PRICES][VALUE][USDT],
            # uniswap_states[PRICES][TRADINGVALUE][USDT],
            # uniswap_states[PRICES][LOW][USDT],
            # uniswap_states[PRICES][HIGH][USDT],
            1,

            uniswap_states[PRICES][VALUE][DUET],
            # uniswap_states[PRICES][TRADINGVALUE][DUET],
            # uniswap_states[PRICES][LOW][DUET],
            # uniswap_states[PRICES][HIGH][DUET],
            oracle.get_price(DUET),

            uniswap_states[PRICES][VALUE][ZBTC],
            # uniswap_states[PRICES][TRADINGVALUE][ZBTC],
            # uniswap_states[PRICES][LOW][ZBTC],
            # uniswap_states[PRICES][HIGH][ZBTC],
            oracle.get_price(BTC),

            uniswap_states[PRICES][VALUE][ZNAS],
            # uniswap_states[PRICES][TRADINGVALUE][ZNAS],
            # uniswap_states[PRICES][LOW][ZNAS],
            # uniswap_states[PRICES][HIGH][ZNAS],
            oracle.get_price(NAS),
            
        ]
        # ExperimentResultModel(experiment_id = self.experiment.unique_id, day=day, result=data, code=self.experiment.code).save()
        return data

    def step(self):
        # print(self.get_record())
        pass

    # def run(self):
    #     while self.running:
    #         self.step()

    #     model = ComputeExperimentModel.objects.get(unique_id=self.unique_id)
    #     model.status = "end"
    #     model.save()

def do_experiment():
    experiment = MBMExperiment()
    while experiment.running:
        experiment.step()
    # experiment.run()
    # model = ComputeExperimentModel.objects.get(unique_id=experiment.unique_id)
    # model.status = "end"
    # model.save()

if __name__ == '__main__':

    # with Pool(100) as p:
    # p = Pool(100)
    # p.map(do_experiment, []*100)
    do_experiment()


    # p.close()
    # p.join()
    # t1 = Process(target=do_experiment)
    # t2 = Process(target=do_experiment)
    

    # t1.start()
    # t2.start()

    # t1.join()
    # t2.join()

