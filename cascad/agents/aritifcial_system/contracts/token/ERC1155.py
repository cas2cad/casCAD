"""this is a class simulate the ERC 1155 Token Interface
"""
address_0 = "0x00000000000000000"
# from cascad models.datamodel import TransferModel, ApprovelModel
from operator import add
from cascad.models.datamodel import TransferModel, ApprovelModel

class ERC1155:
    def __init__(self):
        self._balances = {}
        self._operatorApprovals = {}

    def balanceOf(self, owner, id):
        assert owner != address_0
        if id not in self._balances.keys():
            self._balances[id] = {}
        return self._balances[id][owner]

    def balanceOfBatch(self, owners, ids):
        assert len(owners) == len(ids)

        batchBalances = []
        for index, owner in enumerate(owners):
            assert owner != address_0
            batchBalances[index] = self._balances[ids[index]][owners[index]]

        return batchBalances