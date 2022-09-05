from cascad.agents.aritifcial_system.chain import  ChainBase
from cascad.agents.aritifcial_system.contracts.token.ERC20 import ERC20
from cascad.aritificial_world import World
from cascad.aritificial_world.scheduler import BaseScheduler
from cascad.aritificial_world.timeline import TimeLine
from cascad.experiment.cdec import Cdec
from cascad.models.datamodel import ComputeExperimentModel
from cascad.models.kb import Entity, Property
from cascad.utils.constant import *
from cascad.experiment.token_sender.agents import RandomAgent
from cascad.experiment import  Experiment
import uuid

has_chain = Property("has_chain", "has_chain")


import numpy as np
import random
import os
import csv
import json


random.seed(10)


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
            'experiment': DuetExperiment(file_path)
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
    def __init__(self):
        self.timeline = TimeLine()
        self.MBM_system = None
        pass
    pass