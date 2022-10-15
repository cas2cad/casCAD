from numpy.lib.arraysetops import isin
from .constant import DUET, DUET_USDT, FARM, FRAMWITHDRAW, MINT1, REDEEM, STAKE, STAKEWITHDRAW, SWAP1, ZBTC_ZUSD, ZNAS, ZNAS_ZUSD, ZUSD_USDT, USDT
# from aletheia.artificial_system.mintandredeem.mintredeem import MintRedeemModel
from .mintredeem import MintRedeemModel
# from aletheia.artificial_system.database import Memory
from .memory import Memory
# from aletheia.artificial_system.uniswap import Uniswap
from .uniswap import Uniswap
# from aletheia.artificial_system.stake import Stake
from .stake import  Stake
# from aletheia.artificial_system.rewardmodel import RewardModel
from .rewardmodel import RewardModel
# from aletheia.artificial_system.oracle import Oracle
from .oracle import Oracle
# from aletheia.artificial_system.database import Memory
from .memory import Memory
# from aletheia.artificial_system.blockchain import BlockChain
from .blockchain import BlockChain


class MBMSystem(object):
    def __init__(self, timeline):
        self.timeline = timeline
        self.oracle = Oracle(timeline)
        self.memory = Memory()
        self.uniswap = Uniswap(self.oracle)
        self.mintRedeemModel = MintRedeemModel(
            self.oracle, timeline, self.memory, uniwap=self.uniswap)
        self.staker = Stake()
        self.rewardModel = RewardModel(self.uniswap,'sin', self.timeline)
        self.factor = 1
        self.state_price = 5
        self.mintRedeemModel.step()
        self.uniswap.step()
        self.blockchain = BlockChain()

    def check_gas_fee(self, agent, _from, _to, action, amount1, amount2, result1, result2):
        fee = self.blockchain.submit( _from, _to, action, amount1, amount2, result1, result2)
        if not self.blockchain.turn_on:
            return True
        if agent.states[USDT] >= fee:
            # agent.states[USDT] -= fee
            return fee
        else:
            return False

    def mint(self, agent, token, amount = -1, duet_amount = -1, fee=0):
        if not isinstance(token, str):
            token = token.name
        # fee = self.blockchain.submit(DUET, DUET, token, duet_amount,0,0,0)
        fee = self.check_gas_fee(agent, DUET, token, MINT1, duet_amount, 0, 0, 0)
        if not fee:
            return False, False 
        return self.mintRedeemModel.mint(agent, token, amount, duet_amount)

    def redeem(self, agent, token, amount, fee=0):
        fee = self.check_gas_fee(agent, token, DUET, REDEEM, amount, 0, 0, 0)
        if not fee:
            return False, False

        return self.mintRedeemModel.redeem(agent, token, amount)

    def swap(self, agent, origin_token, amount, target_token, fee=0):
        # fee = self.blockchain.submit(DUET, DUET, token, amount,0,0,0)
        fee = self.check_gas_fee(agent, origin_token, target_token, REDEEM, amount, 0, 0, 0)
        if not fee:
            return False

        return self.uniswap.swap(agent, origin_token, amount, target_token)

    def farm(self, agent, pool, token1, token2, fee_rate=0.003):
        fee = self.check_gas_fee(agent, None, None, FARM, token1, 0, 0, 0)
        if not fee:
            return False, False
        return self.uniswap.farm(agent, pool, token1, token2, fee_rate)

    def stake(self, agent, amount, fee=0):
        fee = self.check_gas_fee(agent, DUET, None, STAKE, amount, 0, 0, 0)
        if not fee:
            return False
        return self.staker.stake(agent, amount)

    def farm_withdraw(self, agent, pool, lp_amount, fee=0):
        fee = self.check_gas_fee(agent, None, None, FRAMWITHDRAW, lp_amount, 0, 0, 0)
        if not fee:
            return False

        return self.uniswap.withdraw(agent, pool, lp_amount)

    def stake_withdraw(self, agent, amount, fee=0):
        fee = self.check_gas_fee(agent, DUET, None, STAKEWITHDRAW, amount, 0, 0, 0)
        if not fee:
            return False

        return self.staker.withdraw(agent, amount)

    def reward(self, agents, stake_reword=10000, duet_usdt_reward=50000, zusd_usdt_reward=40000, zbtc_zusd_reward=20000, znas_zusd_reward=2000):

        
        # self.factor = self.get_price_change(DUET) *(730/self.timeline.tick + 1)

        # if self.factor < 0:
        #     self.factor = 0
        # factor = self.factor

        # if self.factor > 1:
        #     self.factor = 1
        # # print('factor: {}'.format(self.factor))
        # # self.factor = (self.get_usdt_price - 5)/100
        # if self.get_usdt_price(DUET) <= self.state_price:
        #     self.factor = 0
        # else:
        #     self.state_price = self.get_usdt_price(DUET)

        stake_amount = self.rewardModel.reward_stake(agents, 1/14)
        self.staker.add_reward(stake_amount)

        reward_duet_usdt  = self.rewardModel.reward_pool(DUET_USDT, agents, 5/14)
        self.uniswap.add_reward(DUET_USDT, reward_duet_usdt)

        reward_zusd_usdt = self.rewardModel.reward_pool(ZUSD_USDT, agents, 4/14)
        self.uniswap.add_reward(ZUSD_USDT, reward_zusd_usdt)

        reward_zbtc_zusd = self.rewardModel.reward_pool(ZBTC_ZUSD, agents, 2/14)
        self.uniswap.add_reward(ZBTC_ZUSD, reward_zbtc_zusd)

        reward_znas_zusd  = self.rewardModel.reward_pool(ZNAS_ZUSD, agents, 2/14)
        self.uniswap.add_reward(ZNAS_ZUSD, reward_znas_zusd)

    def get_price(self, origin_token, target_token):
        if origin_token == target_token:
            return 1
        return self.uniswap.get_price(origin_token, target_token)

    def get_oracle_price(self, token):
        return self.mintRedeemModel.get_oracle_price(token)

    def get_fraction(self, pool):
        return self.uniswap.get_fraction(pool)

    def get_mint_redeem_tax(self, token, amount):
        return self.mintRedeemModel.compute_tax(token, amount)

    def get_fee(self, token, amount):
        return self.uniswap.get_fee(token, amount)

    def evaluate_swap(self, origin_token, amount, target_token):
        if not isinstance(origin_token, str):
            origin_token = origin_token.name

        if not isinstance(target_token, str):
            target_token = target_token.name

        # for uncertain case
        if isinstance(amount, str):
            amount = 100

        # minus gas fee
        token_price = self.get_current_usdt_price(origin_token)
        fee = self.blockchain.get_fee(SWAP1)
        if isinstance(fee, bool) and fee:
            fee = 0
        amount = amount - fee /token_price

        val = self.uniswap.evaluate_swap(origin_token, amount, target_token)

        if val:
            return val
        else:
            return 0

    def evaluate_mint(self, token, amount):
        # for uncertain case
        if isinstance(amount, str):
            amount = 100
        if not isinstance(token, str):
            token = token.name

        # minus gas fee
        token_price = self.get_current_usdt_price(DUET)
        fee = self.blockchain.get_fee(SWAP1)
        amount = amount - fee /token_price

        return self.mintRedeemModel.evaluate_mint(token, amount)

    def evaluate_redeem(self, token, amount):
        # for unceratin case
        if isinstance(amount, str):
            amount = 100

        if not isinstance(token, str):
            token = token.name

        # minus gas fee
        token_price = self.get_current_usdt_price(token)
        fee = self.blockchain.get_fee(SWAP1)
        amount = amount - fee /token_price

        return self.mintRedeemModel.evaluate_redeem(token, amount)

    def evaluate_price(self, token, amount):
        if not isinstance(token, str):
            token = token.name
        return self.uniswap.evaluate_price(token, amount)

    def get_usdt_price(self, token):
        if not isinstance(token, str):
            token = token.name

        return self.uniswap.get_usdt_price(token)
    
    def get_price_change(self, token):
        if not isinstance(token, str):
            token = token.name
        return self.uniswap.get_price_change(token)

    def get_current_usdt_price(self, token):
        if not isinstance(token, str):
            token = token.name

        return self.uniswap.get_current_usdt_price(token)
    
    def get_current_price_change(self, token):
        if not isinstance(token, str):
            token = token.name
        return self.uniswap.get_current_price_change(token)


    def step(self):
        self.uniswap.step()
        self.mintRedeemModel.step()
        self.staker.step()
        self.blockchain.step()
        self.rewardModel.step()

    def get_pool_lp_value(self, pool, lp_amount):
        return self.uniswap.get_pool_lp_value(pool, lp_amount)

    def n_day_price_change(self, token, num):
        return self.uniswap.n_day_price_change(token, num)


    def get_apy(self, pool, with_reward):
        return self.uniswap.get_apy(pool, with_reward)

    def get_tax(self, token):
        return self.mintRedeemModel.get_tax(token)
