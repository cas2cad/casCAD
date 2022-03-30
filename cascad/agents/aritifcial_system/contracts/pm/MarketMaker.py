from cascad.agents.aritifcial_system.contracts.token.ERC20 import ERC20

class MarketMaker:
    def __init__(self, pmSystem, collateralToken: ERC20, conditionIds, atomicOutcomeSlotCount, fee, funding, stage, whitelist, outcomeSlotCounts, collectionIds, positionIds, owner=None):
        self.pmSystem = pmSystem
        self.collateralToken = collateralToken
        self.conditionIds = conditionIds
        self.atomicOutcomeSlotCount = atomicOutcomeSlotCount
        self.fee = fee
        self.funding = funding
        self.stage = stage
        self.whitelist = whitelist
        self.outcomeSlotCounts = outcomeSlotCounts
        self.collectionIds = collectionIds
        self.positionIds = positionIds
        self.owner = owner

    def changeFunding(self, fundingChange, caller):
        assert fundingChange != 0
        if (fundingChange > 0):
            pass

    def pause(self):
        pass

    def resume(self):
        pass

    def changeFee(self, fee):
        pass
    
    def trade(self, outcomeTokenAmounts, collateralLimit):
        pass

    def calMarketFee(self, outcomeTokenCost):
        pass

    