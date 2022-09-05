# from aletheia.utils.constant import *
from .constant import *


class Thing:
    def __init__(self, name) -> None:
        self.name = name

class Agent(Thing):
    is_a  = [Thing]
    def __init__(self, name) -> None:
        super().__init__(name)

        # functional property, data property
        self.expect_rise_rate = 0
        self.stand_drop_rate = 0
        self.duet_holding_time =0
        self.desire_benefit = 0
        self.short_farming_time = 0
        self.short_farming_min_time = 0
        self.operate_amount = 0
        self.short_farming_sell_time = 0
        self.founder_sell_time = 0
        self.incent_benefit_limit = 0
        self.expect_apy =0
        # self.is_a = [super(self)]

        # functional property, object property
        self.desire_pool = None
        self.desire_token = None
        self.has_desire = None

        # property
        self.has_action = []
        self.using_farm_pool = []
# tokens
class Cryptocurrency(Thing):
    is_a = [Thing]
    def __init__(self, name) -> None:
        super().__init__(name)
        self.address = None

        self.current_uniswap_price = 0
        self.current_oracle_price = 0
        self.unit_cost = 0
        self.cost = 0
        self.amount = 0

class Token(Cryptocurrency):
    is_a = [Cryptocurrency]
    def __init__(self, name) -> None:
        super().__init__(name)

class DAsset(Cryptocurrency):
    is_a = [Cryptocurrency]
    def __init__(self, name) -> None:
        super().__init__(name)

# pool
class LiquidityPool(Thing):
    def __init__(self, name) -> None:
        super().__init__(name)

        self.has_token1 = None
        self.has_token2 = None
        self.has_fration = None
        self.has_apy = None
        self.has_apr = None

class Plan(Thing):
    is_a = [Thing]
    def __init__(self, name) -> None:
        super().__init__(name)

        self.has_action = []


# actions
class Action(Thing):
    def __init__(self, name) -> None:
        super().__init__(name)

class Mint(Action):
    def __init__(self, name) -> None:
        super().__init__(name)

        self.mint_token = None
        self.mint_amount = 0

class Redeem(Action):
    def __init__(self, name) -> None:
        super().__init__(name)

        self.redeem_token = None
        self.redeem_amount = 0

class Swap(Action):
    def __init__(self, name) -> None:
        super().__init__(name)

        self.swap_origin_token = None
        self.swap_target_token = None
        self.swap_amount = 0

class Stake(Action):

    def __init__(self, name) -> None:
        super().__init__(name)

        self.stake_token = DUET
        self.stake_amount = None

class Farm(Action):

    def __init__(self, name) -> None:
        super().__init__(name)

        self.farm_pool = None
        self.farm_token1_amount = 0
        self.farm_token2_amount = 0

class FarmWithdraw(Action):

    def __init__(self, name) -> None:
        super().__init__(name)

        self.farm_pool = None
        self.farm_withdraw_amount = 0

class StakeWithdraw(Action):
    def __init__(self, name) -> None:
        super().__init__(name)

        self.stake_withdraw_amount = 0

class Idle(Action):
    pass


class World(dict):

    def dotGet (self, attr):
        return dict.__getitem__(self, attr)

    def dotSet (self, attr, value):
        return dict.__setitem__(self, attr, value)

    def allowDotting (self, state=True):
        if state:
            self.__getattr__ = self.dotGet
            self.__setattr__ = self.dotSet
        else:
            del self.__setattr__
            del self.__getattr__
