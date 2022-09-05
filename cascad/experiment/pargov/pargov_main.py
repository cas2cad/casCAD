# from aletheia.settings import BASE_DIR
# from aletheia.scenario_generator.experiment import Experiment
# from aletheia.scenario_generator.timeline import TimeLine
# from pargov.timeline import  TimeLine
from cascad.aritificial_world.experiment import Experiment
from cascad.aritificial_world.timeline import TimeLine
from cascad.aritificial_world.scheduler import BaseScheduler
from cascad.settings import BASE_DIR
from random import randint, random, choice, shuffle
# from aletheia.scenario_generator.scheduler import BaseScheduler
import numpy as np
import random
import os
import csv
import json

from pargov.agent import InforAgent
from pargov.gnosystem import  GNOSystem

base_path = os.path.join(BASE_DIR, 'resources', 'datasets')

# random.seed(10)
# np.random.seed(10)

class ParExperiment(Experiment):
    def __init__(self, file_path='', beta_a=3, beta_b=3, risk_coef_up=0, risk_coef_down=0, belief_weight_up = 0.5, belief_weight_down=0, belief_reliable_up=1, belief_reliable_down =0.5, infor_agent_per=0.2, info_arrive_lam=5):
        self.timeline = TimeLine()
        self.gnosystem = GNOSystem(self.timeline)
        self.scheduler = BaseScheduler(self)
        self.file_path  = file_path

        # parameters
        self.beta_a = beta_a
        self.beta_b = beta_b
        self.risk_coef_up = risk_coef_up
        self.risk_coef_down = risk_coef_down
        self.belief_weight_up = belief_weight_up
        self.belief_weight_down = belief_weight_down
        self.belief_reliable_up = belief_reliable_up
        self.belief_reliable_down = belief_reliable_down
        self.infor_agent_per = infor_agent_per
        self.info_arrive_lam = info_arrive_lam

        self.max_step = 36
        self.new_agent()
        self.running = True
        # self.add_proposal()
        self.vote_datas = {
            'gip_1': self.load_vote_datas('gip1.csv'),
            'gip_3': self.load_vote_datas('gip3.csv')
        }
        self.uniq_id = 0
        self.add_proposal()
        self.result = []

    def next_id(self):
        self.uniq_id += 1
        return self.uniq_id

    def load_data_from_csv(self, name='gip1.csv'):
        result = []

        file_path = os.path.join(base_path, name)
        with open(file_path, newline='') as csvfile:
            # file_reader = csv.reader(csvfile)
            file_reader = csv.DictReader(csvfile)
            for row in file_reader:
                result.append([row['address'], float(row['balance']), row['choice'], int(row['day'])])

        return result

    def load_vote_datas(self, name='gip1.csv'):
        gip_datas = self.load_data_from_csv(name)
        result = {}
        for votes in gip_datas:
            if votes[3] not in result.keys():
                result[votes[3]] = []
                result[votes[3]].append({votes[2] : votes[1]})
            else:
                result[votes[3]].append({votes[2] : votes[1]})

        vote_result = {}
        for day in range(8):
            tmp_votes = {}
            current_yes = sum([x.get('1', 0) for x in list(result[day])])
            current_no = sum([x.get('2', 0) for x in list(result[day])])

            if day >= 1:
                tmp_votes[1] = current_yes + vote_result[day - 1][1]
                tmp_votes[2] = current_no + vote_result[day - 1][2]
                tmp_votes['result'] = float(tmp_votes[1] / (tmp_votes[2] + tmp_votes[1]))
            else:
                tmp_votes[1] = current_yes
                tmp_votes[2] = current_no
                tmp_votes['result'] = float(tmp_votes[1] / (tmp_votes[2] + tmp_votes[1]))
            vote_result[day] = tmp_votes
        return vote_result

    def info_agent_1(self):
        for proposal in self.gnosystem.activate_proposals:
            info = self.get_info_avg_impact(proposal.count_result())
            for agent in self.scheduler.agents:
                if agent.available == 1:
                    agent.update_belief_with_info(info, proposal._id)

    def get_info_avg_impact(self, positive):
        
        n = np.random.poisson(self.info_arrive_lam)
        if n == 0:
            return 0
        infos = np.random.uniform(0, 0.5, n)

        # if positive:
        #     infos = np.random.uniform(0, 0.5, n)
        # else:
        #     infos = np.random.uniform(-0.5, 0, n)
        return float(sum(infos)/n)

    def new_agent(self):
        gip_1_datas = self.load_data_from_csv('gip1.csv')
        gip_2_datas = self.load_data_from_csv('gip3.csv')
        datas = gip_1_datas  + gip_2_datas
        gip_datas = []
        address_set = set()
        for data in datas:
            if data[0] not in address_set:
                gip_datas.append(data)
                address_set.add(data[0])

        # belief = np.random.beta(self.beta_a, self.beta_b)       
        # available = choice([0, 0.5, 1])
        # risk_coeffient = np.random.uniform(0, 1)
        agent_num = len(gip_datas)
        infor_num = int(agent_num * self.infor_agent_per)
        infor_idx = random.sample(list(range(agent_num)), infor_num)


        for idx, data in enumerate(gip_datas):
            belief_weight_middle = (self.belief_weight_up + self.belief_weight_down) / 2
            u_no = np.random.uniform(self.belief_weight_down, belief_weight_middle)
            u_yes = np.random.uniform(belief_weight_middle, self.belief_weight_up)

            risk_coeffient = np.random.uniform(self.risk_coef_down, self.risk_coef_up)

            vote_day = data[3]
            # if vote_day == 0:
                # vote_day = 1
            vote_choice = int(data[2])
            balance = data[1]
            address = data[0]
            if idx in infor_idx:
                available = 1
            else:
                available = 0

            agent = InforAgent(address, self.gnosystem, u_yes, u_no, risk_coeffient, available, vote_day, {GNO: float(balance), DAI:5000}, self.beta_a, self.beta_b, self.belief_reliable_up, self.belief_reliable_down, vote_choice=vote_choice)

            self.scheduler.add(agent)

    def add_proposal(self, _type='gip_1'):
        self.gnosystem.submit(self.next_id(), _type)

    def info_agent(self):
        for proposal in self.gnosystem.activate_proposals:
            # actual_vote = self.vote_datas[proposal._type][proposal.dura_time]['result']
            for accept_token in [GNO, DAI]:
                price = self.gnosystem.get_token_price(proposal._id, YES_TOKEN, accept_token)
                for agent in self.scheduler.agents:
                    agent.update_belief_with_price(price, proposal._id)

    def step(self):
        agent_indexs = list(range(len(self.scheduler.agents)))
        shuffle(agent_indexs)
        for index in agent_indexs:
            self.scheduler.agents[index].observe()

        self.info_agent_1()

        for index in agent_indexs:
            self.scheduler.agents[index].step()

        self.info_agent()

        if self.timeline.tick >= self.max_step:
        # if not self.gnosystem.activate_proposals:
            self.running = False

        if self.timeline.tick % 7 == 0 and self.timeline.tick != 0:
            # print(self.evaluate())
            self.evaluate()
            
        if self.timeline.tick == 7:
            self.add_proposal('gip_1')
            # self.add_proposal('gip_3')

        if self.timeline.tick == 14:
            # self.add_proposal('gip_1')
            self.add_proposal('gip_3')
            # self.add_proposal('gip_1')
            # self.add_proposal('gip_3')

        if self.timeline.tick == 21:
            self.add_proposal('gip_1')
            # self.add_proposal('gip_3')
            # self.add_proposal('gip_1')
            # self.add_proposal('gip_3')
            # self.add_proposal('gip_1')
            # self.add_proposal('gip_3')
            # self.add_proposal('gip_1')
            # self.add_proposal('gip_3')
        if self.timeline.tick == 28:
            self.add_proposal('gip_3')


        self.gnosystem.step()
        self.timeline.step()

    def evaluate(self):
        agents = self.scheduler.agents
        avaliable_agents = [agent.total_wealth()[1] - agent.init_GNO for agent in agents if agent.available == 1]
        wealth_loss = [x for x in avaliable_agents if x >= 0]
        if not avaliable_agents:
            loss_1 = 0
        else:
            loss_1 = float(len(wealth_loss) / len(avaliable_agents))

        proposals = self.gnosystem.finished_proposals
        length = len(proposals)
        
        consist_count = 0
        for proposal in proposals:
            vote_result = 1 if proposal.passed else 0
            yes_token = self.gnosystem.get_token_price(proposal._id, YES_TOKEN, GNO, True)
            no_token = self.gnosystem.get_token_price(proposal._id, NO_TOKEN, GNO, True)
            market_result = 1 if yes_token >= no_token else 0
            if vote_result == market_result:
                consist_count += 1
        loss_2 = float(consist_count / length)


        agents = self.scheduler.agents
        avaliable_agents = [agent.total_wealth()[1] - agent.init_GNO for agent in agents]
        wealth_loss = [x for x in avaliable_agents if x >= 0]
        if not avaliable_agents:
            loss_3 = 0
        else:
            loss_3 = float(len(wealth_loss) / len(avaliable_agents))


        self.result.append([loss_1, loss_2, loss_3])

        # if loss_2 <= 0.5:
            # print('debug')
        return loss_1, loss_2, loss_3


if __name__ == '__main__':
    parExperiment = ParExperiment(infor_agent_per=0.9)
    while parExperiment.running:
        parExperiment.step()

    print(parExperiment.result)

    # print(parExperiment.evaluate())
    # result = parExperiment.load_vote_datas('gip1.csv')
    # print(result)