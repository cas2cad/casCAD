import sys
sys.path.append('.')
from .constant import DUET, LP_AMOUNT, STAKE, LP, STAKE_REWARD, FARM_REWARD, TOTAL
# from aletheia.scenario_generator.timeline import TimeLine
# from aletheia.scenario_generator.timeline import TimeLine
from cascad.aritificial_world.timeline import TimeLine
import math


class RewardModel:
    def __init__(self, uniswap, reward_func='sin', timeline = None):
        self.uniswap = uniswap
        self.states = {
        }
        self.day_reward = (140000000/(730)) * 1.57079876
        self.reward_func = reward_func
        self.timeline = timeline
        self.should_total_spend = 0
        self.actual_total_spend = 0
        # self._current_day_reward = 0
        self.current_day_reward = 0

    def reward_stake(self, agents, factor=1/7):
        reward = self.current_day_reward * factor
        total = sum([agent.states[STAKE] for agent in agents])
        if total == 0:
            return 0
        for agent in agents:
            amount = (agent.states[STAKE]/total) * reward
            agent.states[DUET] += amount
            agent.states[STAKE_REWARD] += amount
            self.actual_total_spend += amount
        return reward

    def reward_pool(self, pool, agents, factor=2/7):
        reward = self.current_day_reward * factor
        total = self.uniswap.states[pool].states[LP_AMOUNT]
        actual_lp_amount = 0
        for agent in agents:
            if agent.states[pool] > 0:
                actual_lp_amount += agent.states[pool]
        if not actual_lp_amount:
            return 0

        for agent in agents:
            if agent.states[pool] > 0:
                amount = (agent.states[pool]/actual_lp_amount) * reward
                agent.states[DUET] += amount
                agent.farm_reward += amount
                self.actual_total_spend += amount
            # actual_lp_amount += agent.states[pool]
        # if actual_lp_amount != total - 1:
            # raise Exception('not equal')
        return reward
    
    def get_should_total_reward(self):
        total = 0
        time_tick = self.timeline.tick + 1
        
        if time_tick == 729:
            return 140000000
        if time_tick == 0:
            return 0
        for i in range(time_tick):
            total += self.get_current_day_reward(i)
        return total

    def step(self):
        tick = self.timeline.tick
        # self.current_day_reward = self.get_curr
        self.should_total_spend = self.get_should_total_reward()
        rest_reward = self.should_total_spend - self.actual_total_spend
        # print('rest_reward {} not be rewarded'.format(rest_reward))
        self.current_day_reward = rest_reward

    def get_current_day_reward(self, time_tick):
        # time_tick = self.timeline.tick
        x = math.pi / 730
        x = x * time_tick
        y = math.sin(x)
        y = self.day_reward * y
        # if time_tick == 729:
            # return 140000000
        return y

if __name__ == '__main__':
    am = 0
    timeline = TimeLine()
    reward = RewardModel(None, 'sin', timeline=timeline)
    total = 0
    for i in range(180):
        total += am
        # reward.step()
        print(am)
        timeline.step()
        reward.step()
        am = reward.current_day_reward
    print(total)