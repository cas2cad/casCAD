# from owlready2 import get_ontology, World, Thing, Property, FunctionalProperty, Ontology
# from aletheia.agents.knowlege import *
from .knowlege import *
# from aletheia.agents.entity import *
# from aletheia.agents.property import *
# from aletheia.agents.desires import *
from .desires import *
# from aletheia.utils.constant import *
from .constant import *
# from aletheia.settings import BASE_DIR
from cascad.settings import BASE_DIR
import os


class Belief:
    def __init__(self, _id):
        self.world = World()
        self.agent_id = _id
        # self.onto = self.world.get_ontology(
        #     'http://www.aletheia.org/2021/agent' + str(_id) + '/')
        self.onto = self.world
        self.init_knowlege()

    def init_knowlege(self):

        # myself
        self.onto.myself = Agent("agent" + str(self.agent_id))

        # tokens
        self.onto.DUET = Token(DUET)
        self.onto.BTC = Token(BTC)
        self.onto.USDT = Token(USDT)
        self.onto.NAS = Token(NAS)

        # dassets
        self.onto.ZBTC = DAsset(ZBTC)
        self.onto.ZUSD = DAsset(ZUSD)
        self.onto.ZNAS = DAsset(ZNAS)

        # corresponding relation
        self.onto.BTC.corresponding_currency = self.onto.ZBTC

        self.onto.USDT.corresponding_currency = self.onto.ZUSD

        self.onto.NAS.corresponding_currency = self.onto.ZNAS

        self.onto.DUET_USDT = LiquidityPool(DUET_USDT)
        self.onto.ZUSD_USDT = LiquidityPool(ZUSD_USDT)
        self.onto.ZBTC_ZUSD = LiquidityPool(ZBTC_ZUSD)
        self.onto.ZNAS_ZUSD = LiquidityPool(ZNAS_ZUSD)

        self.onto.DUET_USDT.has_token1 = self.onto.DUET
        self.onto.DUET_USDT.has_token2 = self.onto.USDT

        self.onto.ZUSD_USDT.has_token1 = self.onto.ZUSD
        self.onto.ZUSD_USDT.has_token2 = self.onto.USDT

        self.onto.ZBTC_ZUSD.has_token1 = self.onto.ZBTC
        self.onto.ZBTC_ZUSD.has_token2 = self.onto.ZUSD

        self.onto.ZNAS_ZUSD.has_token1 = self.onto.ZNAS
        self.onto.ZNAS_ZUSD.has_token2 = self.onto.ZUSD

        # actions
        self.onto.mint = Mint(MINT1)
        self.onto.redeem = Redeem(REDEEM)
        self.onto.swap = Swap(SWAP1)
        self.onto.stake = Stake(STAKE)
        self.onto.farm = Farm(FARM)
        self.onto.farm_withdraw = FarmWithdraw(FRAMWITHDRAW)
        self.onto.stake_withdraw = StakeWithdraw(STAKEWITHDRAW)
        self.onto.idle = Idle(IDLE)
        # self.onto.sandwich_attack = SandwichAttack(SANDWICHATTACK)

        # this action is used when there nee two step of mint in operation
        self.onto.mint2 = Mint(MINT2)
        self.onto.swap2 = Swap(SWAP2)

        # this action is used in spread actions, its tooooo long
        self.onto.swap3 = Swap(SWAP3)
        self.onto.swap4 = Swap(SWAP4)


        # here init the state of the state agents
        self.onto.myself.duet_holding_time = 0
        self.onto.myself.short_farming_time = 0

    def set_desire(self, desire: Desire):
        self.onto.myself.has_desire = desire

    def create_action(self, _type, **kwargs):
        if _type == MINT1:
            amount = kwargs['mint_amount']
            mint_token = kwargs['mint_token']
            self.onto.mint.mint_token = mint_token
            self.onto.mint.mint_amount = amount
            return self.onto.mint

        elif _type == MINT2:
            amount = kwargs['mint_amount']
            mint_token = kwargs['mint_token']
            self.onto.mint2.mint_token = mint_token
            self.onto.mint2.mint_amount = amount
            return self.onto.mint2

        elif _type == REDEEM:
            amount = kwargs['redeem_amount']
            redeem_token = kwargs['redeem_token']
            self.onto.redeem.redeem_amount = amount
            self.onto.redeem.redeem_token = redeem_token
            return self.onto.redeem

        elif _type == SWAP1:
            swap_origin_token = kwargs['swap_origin_token']
            swap_target_token = kwargs['swap_target_token']
            swap_amount = kwargs['swap_amount']
            self.onto.swap.swap_origin_token = swap_origin_token
            self.onto.swap.swap_target_token = swap_target_token
            self.onto.swap.swap_amount = swap_amount
            return self.onto.swap

        elif _type == SWAP2:
            swap_origin_token = kwargs['swap_origin_token']
            swap_target_token = kwargs['swap_target_token']
            swap_amount = kwargs['swap_amount']
            self.onto.swap2.swap_origin_token = swap_origin_token
            self.onto.swap2.swap_target_token = swap_target_token
            self.onto.swap2.swap_amount = swap_amount
            return self.onto.swap2

        elif _type == SWAP3:
            swap_origin_token = kwargs['swap_origin_token']
            swap_target_token = kwargs['swap_target_token']
            swap_amount = kwargs['swap_amount']
            self.onto.swap3.swap_origin_token = swap_origin_token
            self.onto.swap3.swap_target_token = swap_target_token
            self.onto.swap3.swap_amount = swap_amount
            return self.onto.swap3
        
        elif _type == SWAP4:
            swap_origin_token = kwargs['swap_origin_token']
            swap_target_token = kwargs['swap_target_token']
            swap_amount = kwargs['swap_amount']
            self.onto.swap4.swap_origin_token = swap_origin_token
            self.onto.swap4.swap_target_token = swap_target_token
            self.onto.swap4.swap_amount = swap_amount
            return self.onto.swap4

        elif _type == STAKE:
            stake_amount = kwargs['stake_amount']
            self.onto.stake.stake_amount = stake_amount
            return self.onto.stake

        elif _type == FARM:
            farm_pool = kwargs['farm_pool']
            token1_amount = kwargs['farm_token1_amount']
            token2_amount = kwargs['farm_token2_amount']
            self.onto.farm.farm_pool = farm_pool
            self.onto.farm.farm_token1_amount = token1_amount
            self.onto.farm.farm_token2_amount = token2_amount
            return self.onto.farm

        elif _type == FRAMWITHDRAW:
            farm_withdraw_amount = kwargs['farm_withdraw_amount']
            farm_pool = kwargs['farm_pool']
            self.onto.farm_withdraw.farm_withdraw_amount = farm_withdraw_amount
            self.onto.farm_withdraw.farm_pool = farm_pool
            return self.onto.farm_withdraw

        elif _type == STAKEWITHDRAW:
            stake_withdraw_amount = kwargs['stake_withdraw_amount']
            self.onto.stake_withdraw.stake_withdraw_amount = stake_withdraw_amount
            return self.onto.stake_withdraw

        elif _type == SANDWICHATTACK:
            pass
