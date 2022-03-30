from cascad.agents.aritifcial_system.chain import  ChainBase
from cascad.agents.aritifcial_system.contracts.token.ERC20 import ERC20
from cascad.aritificial_world import World
from cascad.aritificial_world.scheduler import BaseScheduler
from cascad.aritificial_world.timeline import TimeLine
from cascad.experiment.cdec import Cdec
from cascad.models.kb import Entity, Property
from cascad.utils.constant import *
from cascad.experiment.token_sender.agents import RandomAgent
import uuid


has_chain = Property("has_chain", "has_chain")

class ERC20CDEC(Cdec):
    def __init__(self):
        pass

class ERC20TokenWorld(World):
    _name = "ERC20World"

    def __init__(self, agent_ratio, agent_number, iter_number):

        self.entity = Entity(unique_id=self.next_id(), name=self._name)
        self.entity['name'] = self._name
        self.agent_ratio = agent_ratio
        self.agent_number = agent_number
        self.iter_number = iter_number
        self.scheduler = BaseScheduler(self, self.next_id())
        self.entity[has_scheduler] = self.scheduler.entity
        self.timeline = TimeLine()
        self.chain = ChainBase()
        self.erc20_token = ERC20()
        erc20_addess = self.chain.add_contract(self.erc20_token)
        self.erc20_address = erc20_addess
        self.entity[has_chain] = self.chain.entity
        self.init_world()

    def init_world(self):
        for i in range(self.agent_number):
            agent = RandomAgent(0.5, self.next_id(), self)
            self.erc20_token.transfer(agent.unique_id, 1000, address_1)
            stmt = Entity(self.next_id(), "HasToken")
            self.erc20_token.entity[has_stmt] = stmt
            stmt['has_object'] = agent.entity
            stmt['has_subject'] = self.erc20_token.entity
            stmt['has_amount'] = 1000
            self.scheduler.add(agent)

    def step(self):
        for agent in self.scheduler.agents:
            agent.step()
        self.timeline.step()

    def next_id(self) -> str:
        return uuid.uuid4().hex

    def run(self):
        while self.timeline.tick < self.iter_number:
            self.step()

class ERC20TokenRandom:
    def __init__(self, agent_ratio, agent_number, iter_number) -> None:
        self.agent_number = agent_number
        self.agent_ratio = agent_ratio
        self.iter_number = iter_number
        # self.chain = ChainBase()
        # self.token_address = self.chain.add_contract(ERC20())


