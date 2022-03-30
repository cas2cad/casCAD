"""this is a class simulate the ERC 20 Token Interface
"""
# address_0 = "0x00000000000000000"
# from cascad models.datamodel import TransferModel, ApprovelModel
from cascad.models.datamodel import TransferModel, ApprovelModel
import uuid
from cascad.models.kb import Entity, Property
from cascad.utils.constant import *
from cascad.utils import get_id

class ERC20:
    _balances = {}
    _allowances = {}
    _totalSupply = 0
    _name = "ERC20"
    
    def __init__(self) -> None:
        self.entity = Entity(get_id(), self._name)
        self._balances[address_1] = 100000000000000
        self.name = "SampleToken"


    def _beforeTokenTransfer(_from, _to, amount, caller=None): 
        pass

    def _transfer(self, sender, recipient, amount, caller=None):
        assert sender != address_0
        assert recipient != address_0
        self._beforeTokenTransfer(sender, recipient, amount)
        self._balances[sender] = self._balances[sender] - amount
        self._balances[recipient] = self._balances.get(recipient, 0) + amount
        TransferModel(
            unique_id = uuid.uuid4().hex,
            sender = sender,
            recipient = recipient,
            amount = amount
        ).save()

    def _mint(self, account, amount, caller=None):
        assert account != address_0
        self._beforeTokenTransfer(address_0, account, amount)

        self._totalSupply = self._totalSupply + amount
        self._balances[account] = self._balances[account] + amount
        TransferModel(
            unque_id = uuid.uuid4().hex,
            sender = address_0,
            recipient = account,
            amount = amount
        ).save()

    def _burn(self, account, amount, caller=None):
        assert account != address_0
        self._beforeTokenTransfer(account, address_0, amount)

        self._balances[account] = self._balances[account] - amount
        self._totalSupply = self.totalSupply - amount
        TransferModel(
            unique_id = uuid.uuid4().hex,
            sender = account,
            recipient = address_0,
            amount = amount
        ).save()

    def _approve(self, owner, spender, amount, caller=None):
        assert owner != address_0
        assert spender != address_0
        if owner not in self._allowances.keys():
            self._allowances[owner] = {}
        self._allowances[owner][spender] = amount
        ApprovelModel(
            unique_id = uuid.uuid4().hex,
            owner=owner,
            spender = spender,
            amount = amount
        )

    def _burnFrom(self, account, amount, caller=None):
        self._burn(account, amount)
        self._approve(account, caller, self._allowances[account][caller] - amount)

    def totalSupply(self, caller=None)->int:
        return self._totalSupply

    def balanceOf(self, address, caller=None)->int:
        return self._balances[address]

    def transfer(self, recipient, amount, caller=None)->bool:
        self._transfer(caller, recipient, amount)
        return True

    def allowance(self, owner, spender, caller=None):
        return self._allowances[owner][spender]

    def approve(self, spender, amount, caller=None):
        self._approve(caller, spender, amount)
        return True

    def transferFrom(self, sender, recipient, amount, caller=None):
        self._transfer(sender, recipient, amount, caller)
        self._approve(sender, caller, self._allowances[sender][caller]- amount)
        return True

    def increaseAllowance(self, spender, addedValue, caller):
        self._approve(caller, spender, self._allowances[caller][spender] + addedValue)
        return True

    def decreaseAllowance(self, spender, subtracValue, caller):
        self._approve(caller, spender, self._allowances[caller][spender] - subtracValue)
        return True