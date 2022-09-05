"""Simulate the chain where all smartcontract stored
"""
import uuid
# from utils.myfuncs import Singleton
from cascad.utils.myfuncs import Singleton
from cascad.models.kb import Entity, Property
from cascad.utils.constant import *
from cascad.utils import get_id

has_contract = Property("has_contract", "has_contract")
has_address = Property("has_address", "has_address")

class ChainBase(metaclass=Singleton):
    _name = "ChainBase"

    def __init__(self): 
        self.store = {}
        self.entity = Entity(get_id(), self._name)
        self.entity['name'] = self._name

    def gen_address(self):
        return str(uuid.uuid4())

    def add_contract(self, contract, invoker=None):
        address = self.gen_address()
        self.store[address] = contract
        self.entity[has_contract] = contract.entity
        contract.entity[has_address] = address
        return address

    def invoke_method(self, contract, invoker):
        pass

    def get_contract(self, address):
        return self.store[address]

    def __getitem__(self, address):
        return self.get_contract(address)
