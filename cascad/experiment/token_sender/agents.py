from cascad.agents.artificial_participant import Participant
from cascad.models.kb import Entity, Property
from cascad.utils.constant import *
from cascad.utils import get_id
from random import choice, random, uniform
from cascad.models.datamodel import AgentModel

class RandomAgent(Participant):
    _name = 'RandomAgent'
    def __init__(self, prob=0.5, unique_id = None, world=None):
        self.prob = prob
        self.entity = Entity(unique_id=unique_id, name=self._name)
        self.entity["name"] = self._name
        has_prob = Property("has_prob", "has_prob")
        self.entity[has_prob] = prob
        self.target_addresses = []
        self.unique_id = unique_id
        self.world = world
        AgentModel(
            unique_id = get_id(),
            world_id = self.world.unique_id,
            step = self.world.timeline.get_time(),
            state = {
                'token' : self.world.erc20_token.balanceOf(self.unique_id, self.unique_id),
                'prob': self.prob
                }
        ).save()


        
    def observe(self):
        self.target_addresses = [agent.unique_id for agent in self.world.scheduler.agents]

    def step(self):
        self.observe()

        balance = self.world.erc20_token.balanceOf(self.unique_id, self.unique_id)
        amount = uniform(0, balance)
        if len(self.target_addresses) == 0 :
            return
        address = choice(self.target_addresses)
        self.world.erc20_token.approve(self.unique_id, amount, self.unique_id)
        self.world.erc20_token.transferFrom(self.unique_id, address, amount, self.unique_id)
        AgentModel(
            unique_id = get_id(),
            world_id = self.world.unique_id,
            step = self.world.timeline.get_time(),
            state = {
                'token' : self.world.erc20_token.balanceOf(self.unique_id, self.unique_id),
                'prob': self.prob
                }
        ).save()


