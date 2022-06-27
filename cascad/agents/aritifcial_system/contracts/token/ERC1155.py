"""this is a class simulate the ERC 1155 Token Interface
"""
address_0 = "0x00000000000000000"
# from cascad models.datamodel import TransferModel, ApprovelModel
from operator import add
from cascad.models.datamodel import TransferModel, ApprovelModel,TransferSingleModel, TransferBatchModel

class ERC1155:
    def __init__(self, address = None):
        self._balances = {}
        self._operatorApprovals = {}
        self.address = address

    def balanceOf(self, owner, id, msg=None):
        assert owner != address_0
        if id not in self._balances.keys():
            self._balances[id] = {}
        return self._balances[id][owner]

    def balanceOfBatch(self, owners, ids, msg=None):
        assert len(owners) == len(ids)

        batchBalances = []
        for index, owner in enumerate(owners):
            assert owner != address_0
            batchBalances[index] = self._balances[ids[index]][owners[index]]

        return batchBalances

    def setApprovalForAll(self, operator, approved, msg):
        pass

    def _mint(self, to, id, value, data, msg):
        assert to != address_0
        if id  not in self._balances.keys():
            self._balances[id] = {}
            self._balances[id][to] = 0
        else:
            if to not in self._balances[id].keys():
                self._balances[id][to] = 0
        
        self._balances[id][to] = self._balances[id][to] + value
        TransferSingleModel(
            operator = msg.sender,
            _from = address_0,
            to = to,
            id = id,
            value = value
        ).save()

        # _doSafeTransferAcceptanceCheck

    def _batchMint(self, to, ids, values, data, msg):
        assert to != address_0
        assert len(ids) == len(values)
        for i in range(0, len(ids), 1):
            self._checkBalancesKeys(ids[i], values[i])
            self._balances[ids[i]][to] = values[i] + self._balances[ids[i]][to]
        TransferBatchModel()


    def _checkBalancesKeys(self, id, to):
        if id not in self._balances.keys():
            self._balances[id] = {}
            self._balances[id][to] = 0

        if to not in self._balances[id]:
            self._balances[id][to] = 0
