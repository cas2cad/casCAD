"""FPMM is created based on the market used in gnosis.
"""

from agents import Agent
from cascad.models.datamodel import AgentModel
from cascad.models.kb import Entity, Property
from cascad.utils.constant import *

class FPMM(Agent):
    _name = 'fpmm'

    def __init__(self, unique_id: str, world, fee=0.02, base_token=None) -> None:
        self.unique_id = unique_id
        self.world = world 
        self.state = {} # the agent
        self.state_history = []
        self.agentModel = AgentModel(unique_id=unique_id, state=self.state)
        self.entity = Entity(unique_id=unique_id, name=self._name)
        self.entity[has_fee] = fee
        self.entity[support_token] = base_token

    def step(self) -> None: 
        self.state = {
            'has_fee': self.entity[has_fee]
        }
        pass

    def trade(self)->None: 
        pass

    def close(self) -> None:
        pass

    def resolve(self) -> None: 
        pass
    
    def save(self) -> None:
        pass

class ConditonalToken(Agent):
    _name = 'conditional_token'
    def __init__(self, unique_id: str, world,  base_token=None) -> None:
        self.unique_id = unique_id
        self.world = world
        self.entity = Entity(unique_id=unique_id, name=self._name)
        self.entity[has_price] = 0.5

    def step(self) -> None:
        pass