from owlready2 import get_ontology, World, Thing, Property

onto = get_ontology('http://www.aletheia.org/2021/agent')

with onto:
    class Agent(Thing):
        pass

    class Founder(Agent):
        pass

    class Participant(Agent):
        pass

    class Cryptocurrency(Thing):
        pass

    class Token(Cryptocurrency):
        pass

    class DAsset(Cryptocurrency):
        pass

    class Desire(Thing):
        pass

    class HoldFounder(Desire):
        pass

    class SellFounder(Desire):
        pass

    class DuetValueInvest(Desire):
        pass

    class DuetHold(DuetValueInvest):
        pass

    class DuetHoldAndFarm(DuetValueInvest):
        pass

    class DuetHoldAndStake(DuetValueInvest):
        pass

    class DAssetValueInvest(Desire):
        pass

    class DAssetHold(DAssetValueInvest):
        pass

    class DAssetHoldAndFarm(DAssetValueInvest):
        pass

    class Arbitrage(Desire):
        pass

    class ShortFarmArbitrage(Arbitrage):
        pass

    class Spread(Arbitrage):
        pass

    class ShortTermInvest(Desire):
        pass

    class BullishDUET(ShortTermInvest):
        pass

    class BullishDAsset(ShortTermInvest):
        pass

    class BearrishDUET(ShortTermInvest):
        pass

    class BearrishDAsset(ShortTermInvest):
        pass

    class Founder(Desire):
        pass

    class HoldFounder(Founder):
        pass

    class SellFounder(Desire):
        pass

    class Plan(Thing):
        pass

    class Intent(Thing):
        pass

    class Attack(Thing):
        pass

    class Action(Thing):
        pass

    class Mint(Action):
        pass

    class Redeem(Action):
        pass

    class Swap(Action):
        pass

    class Stake(Action):
        pass

    class Farm(Action):
        pass

    class FarmWithdraw(Action):
        pass

    class StakeWithdraw(Action):
        pass

    class Idle(Action):
        pass

    class SandwichAttack(Attack):
        pass

    class LiquidityPool(Thing):
        pass

    # class Buy(Action):
    #     pass

    # class Sell(Action):
    #     pass

    # class Stake(Action):
    #     pass
