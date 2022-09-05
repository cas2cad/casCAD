# from aletheia.agents.knowlege import Thing
# from aletheia.utils.constant import *
from .knowlege import Thing
from .constant import *


# desires to be used
class Desire(Thing):
    name = 'DESIRE'
    def __init__(self) -> None:
        pass

class Trader(Desire):
    name = 'Trader'

class HoldFounder(Desire):
    name = 'HoldFounder' 

class SellFounder(Desire):
    name = 'SellFounder' 

class DuetValueInvest(Desire):
    name = 'DuetValueInvest'

class DuetHold(DuetValueInvest):
    name = 'DuetHold'
    pass

class DuetHoldAndFarm(DuetValueInvest):
    name = 'DuetHoldAndFarm'
    pass

class DuetHoldAndStake(DuetValueInvest):
    name = 'DuetHoldAndStake'
    pass

class DAssetValueInvest(Desire):
    name = 'DAssetValueInvest'
    pass

class DAssetHold(DAssetValueInvest):
    name = 'DAssetHold'
    pass

class DAssetHoldAndFarm(DAssetValueInvest):
    name = 'DAssetHoldAndFarm'
    pass

class Arbitrage(Desire):
    name = 'Arbitrage'
    pass

class ShortFarmArbitrage(Arbitrage):
    name = 'ShortFarmArbitrage'
    pass

class Spread(Arbitrage):
    name = 'Spread'
    pass

class ShortTermInvest(Desire):
    name = 'ShortTermInvest'
    pass

class BullishDUET(ShortTermInvest):
    name = 'BullishDuet'
    pass

class BullishDAsset(ShortTermInvest):
    name = 'BullishDAsset'
    pass

class BearrishDUET(ShortTermInvest):
    name = 'BearrishDuet'
    pass

class BearrishDAsset(ShortTermInvest):
    name = 'BearrishDAsset'
    pass
