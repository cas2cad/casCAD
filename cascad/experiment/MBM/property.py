from owlready2 import get_ontology, World, Thing, Property, FunctionalProperty, DataProperty, ObjectProperty
from aletheia.agents.entity import *

with onto:
    class current_uniswap_price(DataProperty, FunctionalProperty):
        domain = [Cryptocurrency]
        range = [float]

    class current_oracle_price(DataProperty, FunctionalProperty):
        domain = [Cryptocurrency]
        range = [float]

    class corresponding_currency(ObjectProperty, FunctionalProperty):
        domain = [Token, DAsset]
        range = [Token, DAsset]

    class has_desire(ObjectProperty, FunctionalProperty):
        domain = [Agent]
        range = [Desire]

    class has_action(ObjectProperty, Property):
        domain = [Plan]
        range = [Action]

    class has_plan(Property):
        pass

    class has_intent(Property):
        pass

    class mint_token(ObjectProperty, FunctionalProperty):
        domain = [Mint]
        range = [DAsset]

    class mint_amount(DataProperty, FunctionalProperty):
        domain = [Mint]
        range = [float]

    class mint_duet_amount(DataProperty, FunctionalProperty):
        domain = [Mint]
        range = [float]

    class redeem_token(ObjectProperty, FunctionalProperty):
        domain = [Redeem]
        range = [DAsset]

    class redeem_amount(DataProperty, FunctionalProperty):
        domain = [Redeem]
        range = [float]

    class swap_origin_token(ObjectProperty, FunctionalProperty):
        domain = [Swap]
        range = [Cryptocurrency]

    class swap_target_token(ObjectProperty, FunctionalProperty):
        domain = [Swap]
        range = [Cryptocurrency]

    class swap_amount(DataProperty, FunctionalProperty):
        domain = [Swap]
        range = [float]

    class farm_pool(ObjectProperty, FunctionalProperty):
        domain = [Farm, FarmWithdraw]
        range = [LiquidityPool]

    class farm_token1_amount(DataProperty, FunctionalProperty):
        domain = [Farm]
        range = [float]

    class farm_token2_amount(DataProperty, FunctionalProperty):
        domain = [Farm]
        range = [float]

    class farm_withdraw_amount(DataProperty, FunctionalProperty):
        domain = [FarmWithdraw]
        range = [float]

    class stake_amount(DataProperty, FunctionalProperty):
        domain = [Stake]
        range = [float]

    class stake_withdraw_amount(DataProperty, FunctionalProperty):
        domain = [StakeWithdraw]
        range = [float]

    class has_token1(ObjectProperty, FunctionalProperty):
        domain = [LiquidityPool]
        range = [Cryptocurrency]

    class has_token2(ObjectProperty, FunctionalProperty):
        domain = [LiquidityPool]
        range = [Cryptocurrency, Token, DAsset]

    class has_fraction(DataProperty, FunctionalProperty):
        domain = [LiquidityPool]
        range = [float]


    class locked_up_period(DataProperty, FunctionalProperty):
        domain = [Cryptocurrency]
        range = [float]


    class token_cost(DataProperty, FunctionalProperty):
        domain = [Cryptocurrency]
        range = [float]


    class has_apy(DataProperty, FunctionalProperty):
        domain = [LiquidityPool]
        range = [float]

    class has_apr(DataProperty, FunctionalProperty):
        domain = [LiquidityPool]
        range = [float]

    # token related
    class unit_cost(DataProperty, FunctionalProperty):
        domain = [Cryptocurrency]
        range = [float]

    # myself property
    class expect_rise_rate(DataProperty, FunctionalProperty):
        domain = [Agent]
        range = [float]

    class stand_drop_rate(DataProperty, FunctionalProperty):
        domain = [Agent]
        range = [float]

    class duet_holding_time(DataProperty, FunctionalProperty):
        domain = [Agent]
        range = [float]

    class desire_benefit(DataProperty, FunctionalProperty):
        domain = [Agent]
        range = [float]

    class short_farming_time(DataProperty, FunctionalProperty):
        domain = [Agent]
        range = [float]

    class short_farming_min_time(DataProperty, FunctionalProperty):
        domain = [Agent]
        range = [float]

    class using_farm_pool(ObjectProperty, Property):
        domain = [Agent]
        range = [LiquidityPool]

    class operate_amount(DataProperty, FunctionalProperty):
        domain = [Agent]
        range = [float]
    
    class desire_pool(ObjectProperty, FunctionalProperty):
        domain = [Agent]
        range = [LiquidityPool]

    class desire_token(ObjectProperty, FunctionalProperty):
        domain = [Agent]
        range = [Cryptocurrency]

    class short_framing_sell_time(DataProperty, FunctionalProperty):
        domain = [Agent]
        range = [float]

    class founder_sell_time(DataProperty, FunctionalProperty):
        domain = [Agent]
        range = [float]

    class incent_benefit_limit(DataProperty, FunctionalProperty):
        domain = [Agent]
        range = [float]

    class expect_apy(DataProperty, FunctionalProperty):
        domain = [Agent]
        range = [float]
