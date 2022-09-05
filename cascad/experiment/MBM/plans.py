from random import choice, choices
from sqlite3.dbapi2 import apilevel
# from aletheia.agents.property import mint_amount, mint_token, redeem_amount, redeem_token, swap_amount, swap_origin_token, swap_target_token
# from aletheia.artificial_system import duet
# from aletheia.agents.entity import *
# from aletheia.agents.knowlege import *
# from aletheia.utils.constant import *
from .knowlege import *
from .constant import *

class Plan:

    @staticmethod
    def count_swap(plan):
        count = 0
        for action in plan:
            if isinstance(action, Swap):
                count += 1
        return count
    
    @staticmethod
    def choose_swap_plan(from_token, to_token, agent, amount, step=0, mint_step=0):
        ''' step is the wich step in one sequence to use
        '''
        plan = []
        onto = agent.belief.onto
        create_action = agent.belief.create_action
        duet_system = agent.system

        step_swap_dict = {
            0 : SWAP1,
            1 : SWAP2,
            2 : SWAP3,
            3 : SWAP4
        }

        step_mint_dict = {
            0 : MINT1,
            1 : MINT2,
            2 : MINT3,
            3 : MINT4
        }

        # usdt -> zusd
        if from_token == onto.USDT and to_token == onto.ZUSD:
            duet_value = duet_system.evaluate_swap(onto.USDT, amount, onto.DUET)
            mint_zusd_alue = duet_system.evaluate_mint(onto.ZUSD, duet_value)

            swap_zusd_value = duet_system.evaluate_swap(onto.USDT, amount, onto.ZUSD)
            
            _swap = step_swap_dict[step]
            if swap_zusd_value >=  mint_zusd_alue:
                buy_action = create_action(
                    _type = _swap,
                    swap_origin_token = from_token,
                    swap_target_token = to_token,
                    swap_amount = amount
                )
                step += 1
                plan.append(buy_action)
            else:
                buy_action = create_action(
                    _type = _swap,
                    swap_origin_token = onto.USDT,
                    swap_target_token = onto.DUET,
                    swap_amount = amount 
                )
                step += 1
                plan.append(buy_action)

                _mint = step_mint_dict[mint_step]
                mint_action = create_action(
                    _type = _mint,
                    mint_token = to_token,
                    mint_amount = LAST
                )
                mint_step += 1
                plan.append(mint_action)

        #usdt -> zbtc
        elif from_token == onto.USDT and to_token == onto.ZBTC:
            duet_value = duet_system.evaluate_swap(onto.USDT, amount, onto.DUET)
            mint_zbtc_value = duet_system.evaluate_mint(onto.ZBTC, duet_value)

            zusd_value = duet_system.evaluate_swap(onto.USDT, amount, onto.ZUSD)
            swap_zbtc_value = duet_system.evaluate_swap(onto.ZUSD, zusd_value, onto.ZBTC)

            duet_value = duet_system.evaluate_swap(onto.USDT, amount, onto.DUET)
            zusd_value2 = duet_system.evaluate_mint(onto.ZUSD, duet_value)
            swap_zbtc_value2 = duet_system.evaluate_swap(onto.ZUSD, zusd_value2, onto.ZBTC)

            rank_value = [(1, mint_zbtc_value), (2, swap_zbtc_value), (3, swap_zbtc_value2)]
            rank_value = sorted(rank_value, key=lambda x: x[0], reverse=True)[0]
            # rank_value = choice(rank_value)
            if rank_value[0] == 1:
                _swap = step_swap_dict[step]
                buy_action = create_action(
                    _type = _swap,
                    swap_origin_token = from_token,
                    swap_target_token = onto.DUET,
                    swap_amount = amount
                )
                step += 1
                plan.append(buy_action)

                _mint = step_mint_dict[mint_step]
                mint_action = create_action(
                    _type = _mint,
                    mint_token = to_token,
                    mint_amount = LAST
                )
                mint_step += 1
                plan.append(mint_action)

            elif rank_value[0] == 2:
                _swap = step_swap_dict[step]
                buy_action = create_action(
                    _type = _swap,
                    swap_origin_token = from_token,
                    swap_target_token = onto.ZUSD,
                    swap_amount = amount
                )
                step += 1
                plan.append(buy_action)

                _swap = step_swap_dict[step]
                buy_action2 = create_action(
                    _type = _swap,
                    swap_origin_token = onto.ZUSD,
                    swap_target_token = to_token,
                    swap_amount = LAST
                )
                step += 1
                plan.append(buy_action2)
            elif rank_value[0] == 3:
                _swap = step_swap_dict[step]
                buy_action = create_action(
                    _type = _swap,
                    swap_origin_token = from_token,
                    swap_target_token = onto.DUET,
                    swap_amount = amount
                )
                step += 1
                plan.append(buy_action)

                _mint = step_mint_dict[mint_step]
                mint_action = create_action(
                    _type = _mint,
                    mint_token = onto.ZUSD,
                    mint_amount = LAST
                )
                mint_step += 1
                plan.append(mint_action)

                _swap = step_swap_dict[step]
                buy_action = create_action(
                    _type = _swap,
                    swap_origin_token = onto.ZUSD,
                    swap_target_token = to_token,
                    swap_amount = LAST 
                )
                step += 1
                plan.append(buy_action)


        #usdt -> znas
        elif from_token == onto.USDT and to_token == onto.ZNAS:
            duet_value = duet_system.evaluate_swap(onto.USDT, amount, onto.DUET)
            mint_znas_value = duet_system.evaluate_mint(onto.ZNAS, duet_value)

            zusd_value = duet_system.evaluate_swap(onto.USDT, amount, onto.ZUSD)
            swap_znas_value = duet_system.evaluate_swap(onto.ZUSD, zusd_value, onto.ZNAS)

            duet_value = duet_system.evaluate_swap(onto.USDT, amount, onto.DUET)
            zusd_value2 = duet_system.evaluate_mint(onto.ZUSD, duet_value)
            swap_znas_value2 = duet_system.evaluate_swap(onto.ZUSD, zusd_value2, to_token)

            rank_value = [(1, mint_znas_value), (2, swap_znas_value), (3, swap_znas_value2)]
            rank_value = sorted(rank_value, key=lambda x: x[0], reverse=True)[0]

            # rank_value = choice(rank_value)
            if rank_value[0] == 1:
                _swap = step_swap_dict[step]
                buy_action = create_action(
                    _type = _swap,
                    swap_origin_token = from_token,
                    swap_target_token = onto.DUET,
                    swap_amount = amount
                )
                step += 1
                plan.append(buy_action)

                _mint = step_mint_dict[mint_step]
                mint_action = create_action(
                    _type = _mint,
                    mint_token = to_token,
                    mint_amount = LAST
                )
                mint_step += 1
                plan.append(mint_action)

            elif rank_value[0] == 2:
                _swap = step_swap_dict[step]
                buy_action = create_action(
                    _type = _swap,
                    swap_origin_token = from_token,
                    swap_target_token = onto.ZUSD,
                    swap_amount = amount
                )
                step += 1
                plan.append(buy_action)

                _swap = step_swap_dict[step]
                buy_action2 = create_action(
                    _type = _swap,
                    swap_origin_token = onto.ZUSD,
                    swap_target_token = to_token,
                    swap_amount = LAST
                )
                step += 1
                plan.append(buy_action2)
            elif rank_value[0] == 3:
                _swap = step_swap_dict[step]
                buy_action = create_action(
                    _type = _swap,
                    swap_origin_token = from_token,
                    swap_target_token = onto.DUET,
                    swap_amount = amount
                )
                step += 1
                plan.append(buy_action)

                _mint = step_mint_dict[mint_step]
                mint_action = create_action(
                    _type = _mint,
                    mint_token = onto.ZUSD,
                    mint_amount = LAST
                )
                mint_step += 1
                plan.append(mint_action)

                _swap = step_swap_dict[step]
                buy_action = create_action(
                    _type = _swap,
                    swap_origin_token = onto.ZUSD,
                    swap_target_token = to_token,
                    swap_amount = LAST 
                )
                step += 1
                plan.append(buy_action)

        #duet -> zusd
        elif from_token == onto.DUET and to_token == onto.ZUSD:

            _mint = step_mint_dict[mint_step]
            mint_action = create_action(
                _type = _mint,
                mint_token = onto.ZUSD,
                mint_amount = amount
            )
            mint_step += 1
            # buy_action = create_action(
            #     _type = SWAP1,
            #     swap_origin_token = from_token,
            #     swap_target_token = to_token,
            #     swap_amount = amount
            # )
            plan.append(mint_action)

        #duet -> usdt : here for simple, only conside one step
        elif from_token == onto.DUET and to_token == onto.USDT:
            swap_usdt = duet_system.evaluate_swap(onto.DUET, amount, onto.USDT)

            mint_zusd = duet_system.evaluate_mint(onto.ZUSD, amount)
            swap_usdt1 = duet_system.evaluate_swap(onto.ZUSD, mint_zusd, onto.USDT)

            if swap_usdt >= swap_usdt1:

                _swap = step_swap_dict[step]
                buy_action = create_action(
                    _type = _swap,
                    swap_origin_token = from_token,
                    swap_target_token = to_token,
                    swap_amount = amount
                )
                step += 1
                plan.append(buy_action)
            else:
                _mint = step_mint_dict[mint_step]
                mint_action = create_action(
                    _type = _mint,
                    mint_token = onto.ZUSD,
                    mint_amount = amount
                )
                mint_step += 1
                plan.append(mint_action)

                _swap = step_swap_dict[step]
                buy_action = create_action(
                    _type = _swap,
                    swap_origin_token = onto.ZUSD,
                    swap_target_token = to_token,
                    swap_amount = LAST 
                )
                step += 1
                plan.append(buy_action)

        #duet -> zbtc
        elif from_token == onto.DUET and to_token ==onto.ZBTC:
            _mint = step_mint_dict[mint_step]
            mint_action = create_action(
                _type = _mint,
                mint_token = onto.ZBTC,
                mint_amount = amount
            )
            mint_step += 1
            plan.append(mint_action)

        #duet -> znas
        elif from_token == onto.DUET and to_token == onto.ZNAS:
            _mint = step_mint_dict[mint_step]
            mint_action = create_action(
                _type = _mint,
                mint_token = onto.ZNAS,
                mint_amount = amount
            )
            mint_step += 1
            plan.append(mint_action)


        #zusd -> usdt
        elif from_token == onto.ZUSD and to_token == onto.USDT:
            # zusd_swap_value = duet_system.evaluate_swap(onto.ZUSD, amount, onto.ZUSD)
            
            _type = step_swap_dict[step]
            buy_action = create_action(
                _type = _type,
                swap_origin_token = from_token,
                swap_target_token = to_token,
                swap_amount = amount
            )
            step += 1
            plan.append(buy_action)

        #zbtc -> usdt
        elif from_token == onto.ZBTC and to_token == onto.USDT:
            zusd_swap_value = duet_system.evaluate_swap(onto.ZBTC, amount, onto.ZUSD)
            usdt_swap_value1 = duet_system.evaluate_swap(onto.ZUSD, zusd_swap_value, onto.USDT)

            duet_redeem_value = duet_system.evaluate_redeem(onto.ZBTC, amount)
            usdt_swap_value2 = duet_system.evaluate_swap(onto.DUET, duet_redeem_value, onto.USDT)

            if usdt_swap_value1 > usdt_swap_value2:
                _type = step_swap_dict[step]
                buy_zusd_action = create_action(
                    _type = _type,
                    swap_origin_token = from_token,
                    swap_target_token = onto.ZUSD,
                    swap_amount = amount
                )
                plan.append(buy_zusd_action)

                step += 1
                _type = step_swap_dict[step]
                buy_usdt_action = create_action(
                    _type = _type,
                    swap_origin_token = onto.ZUSD,
                    swap_target_token = onto.USDT,
                    swap_amount = LAST
                )
                step += 1
                plan.append(buy_usdt_action)

            else:
                redeem_action = create_action(
                    _type = REDEEM,
                    redeem_amount = amount,
                    redeem_token = onto.ZBTC
                )
                plan.append(redeem_action)

                _swap = step_swap_dict[step]
                buy_usdt_action = create_action(
                    _type = _swap,
                    swap_origin_token = onto.DUET,
                    swap_target_token = onto.USDT,
                    swap_amount = LAST
                )
                step += 1
                plan.append(buy_usdt_action)

        #znas -> usdt
        elif from_token == onto.ZNAS and to_token == onto.USDT:

            zusd_swap_value = duet_system.evaluate_swap(onto.ZNAS, amount, onto.ZUSD)
            usdt_swap_value1 = duet_system.evaluate_swap(onto.ZUSD, zusd_swap_value, onto.USDT)

            duet_redeem_value = duet_system.evaluate_redeem(onto.ZNAS, amount)
            usdt_swap_value2 = duet_system.evaluate_swap(onto.DUET, duet_redeem_value, onto.USDT)

            if usdt_swap_value1 > usdt_swap_value2:
                _type = step_swap_dict[step]
                buy_zusd_action = create_action(
                    _type = _type,
                    swap_origin_token = from_token,
                    swap_target_token = onto.ZUSD,
                    swap_amount = amount
                )
                plan.append(buy_zusd_action)

                step += 1
                _type = step_swap_dict[step]
                buy_usdt_action = create_action(
                    _type = _type,
                    swap_origin_token = onto.ZUSD,
                    swap_target_token = onto.USDT,
                    swap_amount = LAST
                )
                plan.append(buy_usdt_action)

            else:
                redeem_action = create_action(
                    _type = REDEEM,
                    redeem_amount = amount,
                    redeem_token = onto.ZNAS
                )
                plan.append(redeem_action)

                _type = step_swap_dict[step]
                buy_usdt_action = create_action(
                    _type = _type,
                    swap_origin_token = onto.DUET,
                    swap_target_token = onto.USDT,
                    swap_amount = LAST
                )
                step += 1
                plan.append(buy_usdt_action)

        return plan

    @staticmethod
    def choose_spread_plan(agent, amount, start_token=USDT):
        """ choose one spread asset, but each one only mutiplay on one asset
        """

        if agent.states[start_token] <= agent.mini_amount:
            return []

        # plan = []
        onto = agent.belief.onto
        create_action = agent.belief.create_action
        duet_system = agent.system
        benefit_limit = onto.myself.incent_benefit_limit

        # usdt -> zusd -> duet -> usdt
        def take_plan_1():
            plan = []
            buy_zusd = create_action(
                _type = SWAP1,
                swap_origin_token = onto.USDT,
                swap_target_token = onto.ZUSD,
                swap_amount = amount
            )
            plan.append(buy_zusd)
            redeem_action = create_action(
                _type = REDEEM,
                redeem_amount = LAST,
                redeem_token = onto.ZUSD
            )
            plan.append(redeem_action)
            sell_zusd = create_action(
                _type = SWAP2,
                swap_origin_token = onto.DUET,
                swap_target_token = onto.USDT,
                swap_amount = LAST
            )
            plan.append(sell_zusd)
            return plan

        def eval_plan_1():
            zusd_swap_value = duet_system.evaluate_swap(onto.USDT, amount, onto.ZUSD)
            redeem_value = duet_system.evaluate_redeem(onto.ZUSD,  zusd_swap_value)
            usdt_swap_value = duet_system.evaluate_swap(onto.DUET, redeem_value, onto.USDT)
            return usdt_swap_value - amount


        # usdt -> duet -> zusd -> usdt
        def eval_plan_2():
            duet_swap_value = duet_system.evaluate_swap(onto.USDT, amount, onto.DUET)
            zusd_mint_value = duet_system.evaluate_mint(onto.ZUSD, duet_swap_value)
            usdt_swap_value_re = duet_system.evaluate_swap(onto.ZUSD, zusd_mint_value, onto.USDT)
            return usdt_swap_value_re - amount

        def take_plan_2():
            plan = []
            if start_token == USDT:

                buy_duet = create_action(
                    _type = SWAP1,
                    swap_origin_token = onto.USDT,
                    swap_target_token = onto.DUET,
                    swap_amount = amount
                )
    
                plan.append(buy_duet)

            if start_token == ZUSD:

                mint_action = create_action(
                    _type = MINT1,
                    mint_amount = amount,
                    mint_token = onto.ZUSD
                )
                plan.append(mint_action)
            else:
                mint_action = create_action(
                    _type = MINT1,
                    mint_amount = LAST,
                    mint_token = onto.ZUSD
                )
                plan.append(mint_action)

            sell_zusd = create_action(
                _type = SWAP2,
                swap_origin_token = onto.ZUSD,
                swap_target_token = onto.USDT,
                swap_amount = LAST
            )
            plan.append(sell_zusd)
            return plan

        # onto.ZBTC  onto.ZNAS
        # for token in [onto.ZBTC, onto.ZNAS]:

        # usdt -> zusd -> dasset -> duet -> usdt
        def eval_plan_3(token):
            zusd_swap_value = duet_system.evaluate_swap(onto.USDT, amount, onto.ZUSD)
            dasset_swap_value = duet_system.evaluate_swap(onto.ZUSD, zusd_swap_value, token)
            dasset_redeem_value = duet_system.evaluate_redeem(token, dasset_swap_value)
            usdt_swap_value = duet_system.evaluate_swap(onto.DUET, dasset_redeem_value, onto.USDT)
            return  usdt_swap_value - amount
        
        def take_plan_3(token):
                plan = []
                buy_zusd = create_action(
                    _type = SWAP1,
                    swap_origin_token = onto.USDT,
                    swap_target_token = onto.ZUSD,
                    swap_amount = amount
                )
                plan.append(buy_zusd)

                buy_dasset = create_action(
                    _type = SWAP2,
                    swap_origin_token = onto.ZUSD,
                    swap_target_token = token,
                    swap_amount = LAST
                )
                plan.append(buy_dasset)

                dasset_redeem = create_action(
                    _type = REDEEM,
                    redeem_token = token,
                    redeem_amount = LAST
                )
                plan.append(dasset_redeem)

                buy_usdt = create_action(
                    _type = SWAP3,
                    swap_origin_token = onto.DUET,
                    swap_target_token = onto.USDT,
                    swap_amount = LAST
                )
                plan.append(buy_usdt)
                return plan
        

        # usdt -> duet -> dasset -> zusd -> usdt
        # for token in [onto.ZBTC, onto.ZNAS]:
        def eval_plan_4(token):
            duet_swap_value = duet_system.evaluate_swap(onto.USDT, amount, onto.DUET)
            dasset_mint_value = duet_system.evaluate_mint(token, duet_swap_value)
            dasset_swap_value = duet_system.evaluate_swap(token, dasset_mint_value, onto.ZUSD)
            usdt_swap_value = duet_system.evaluate_swap(onto.ZUSD, dasset_swap_value, onto.USDT)
            return usdt_swap_value - amount

        #if usdt_swap_value > amount:
        def take_plan_4(token):
                plan = []
                if start_token == USDT:
                    buy_duet = create_action(
                        _type = SWAP1,
                        swap_origin_token = onto.USDT,
                        swap_target_token = onto.DUET,
                        swap_amount = amount
                    )
                    plan.append(buy_duet)

                if start_token == DUET:
                    mint_action = create_action(
                        _type = MINT1,
                        mint_token = token,
                        mint_amount = amount
                    )
                    plan.append(mint_action)
                else:
                    mint_action = create_action(
                        _type = MINT1,
                        mint_token = token,
                        mint_amount = LAST
                    )
                    plan.append(mint_action)

                dasset_swap = create_action(
                    _type = SWAP2,
                    swap_origin_token = token,
                    swap_target_token = onto.ZUSD,
                    swap_amount = LAST
                )
                plan.append(dasset_swap)

                usdt_swap = create_action(
                    _type = SWAP3,
                    swap_origin_token = onto.ZUSD,
                    swap_target_token = onto.USDT,
                    swap_amount = LAST
                )
                plan.append(usdt_swap)
                return plan


        # usdt->zusd->duet->zusd
        # usdt->duet->zusd->usdt
        # usdt -> zusd - swap -duet -> usdt
        def take_plan_5():
            plan = []
            buy_zusd = create_action(
                _type = SWAP1,
                swap_origin_token = onto.USDT,
                swap_target_token = onto.ZUSD,
                swap_amount = amount
            )
            plan.append(buy_zusd)
            redeem_action = create_action(
                _type = SWAP2,
                swap_origin_token = onto.ZUSD,
                swap_target_token = onto.DUET,
                swap_amount = LAST 
            )
            plan.append(redeem_action)
            sell_zusd = create_action(
                _type = SWAP3,
                swap_origin_token = onto.DUET,
                swap_target_token = onto.USDT,
                swap_amount = LAST
            )
            plan.append(sell_zusd)
            return plan

        def eval_plan_5():
            zusd_swap_value = duet_system.evaluate_swap(onto.USDT, amount, onto.ZUSD)
            redeem_value = duet_system.evaluate_swap(onto.ZUSD,  zusd_swap_value, onto.DUET)
            usdt_swap_value = duet_system.evaluate_swap(onto.DUET, redeem_value, onto.USDT)
            return usdt_swap_value - amount


        # usdt -> duet - mint -zusd -> zbtc-redeem- duet - mint zusd -> usdt
        def eval_plan_6(token):
            duet_swap_value = duet_system.evaluate_swap(onto.USDT, amount, onto.DUET)
            mint_zusd = duet_system.evaluate_mint(onto.ZUSD, duet_swap_value)
            zbtc_swap_value = duet_system.evaluate_swap(onto.ZUSD, mint_zusd, token)
            zbtc_redeem_value = duet_system.evaluate_redeem(token, zbtc_swap_value)
            zusd_mint_value2 = duet_system.evaluate_mint(onto.ZUSD, zbtc_redeem_value)
            zusd_swap_value = duet_system.evaluate_swap(onto.ZUSD, zusd_mint_value2, onto.USDT)
            
            return zusd_swap_value - amount

        def take_plan_6(token):
            plan = []
            if start_token == USDT:
                buy_duet = create_action(
                    _type = SWAP1,
                    swap_origin_token = onto.USDT,
                    swap_target_token = onto.DUET,
                    swap_amount = amount
                )
    
                plan.append(buy_duet)

            mint_action = create_action(
                    _type = MINT1,
                    mint_token = onto.ZUSD,
                    mint_amount = LAST
                )
            plan.append(mint_action)

            zbtc_swap = create_action(
                _type = SWAP2,
                swap_origin_token = onto.ZUSD,
                swap_target_token = token,
                swap_amount = LAST
            )
            plan.append(zbtc_swap)

            zbtc_redeem = create_action(
                _type = REDEEM,
                redeem_token = token,
                redeem_amount = LAST
            )
            plan.append(zbtc_redeem)

            mint_action2 = create_action(
                    _type = MINT2,
                    mint_token = onto.ZUSD,
                    mint_amount = LAST
                )
            plan.append(mint_action2)

            sell_zusd = create_action(
                _type = SWAP3,
                swap_origin_token = onto.ZUSD,
                swap_target_token = onto.USDT,
                swap_amount = LAST
            )
            plan.append(sell_zusd)
            return plan

        evals = [
             {'val': eval_plan_1(), 'action': take_plan_1, 'name': 'usdt -> zusd -> duet -> usdt', 'weight': 1},
             {'val': eval_plan_2(), 'action': take_plan_2, 'name': 'usdt -> duet -> zusd -> usdt', 'weight': 2}, # suggest using duet to get benefit
             {'val': eval_plan_3(onto.ZBTC), 'action': take_plan_3, 'parameter': onto.ZBTC, 'name': 'usdt -> zusd -> zbtc -> duet -> usdt', 'weight': 1},
             {'val': eval_plan_3(onto.ZNAS), 'action': take_plan_3, 'parameter': onto.ZNAS, 'name': 'usdt -> zusd -> znas -> duet -> usdt', 'weight': 1},
             {'val': eval_plan_4(onto.ZBTC), 'action': take_plan_4, 'parameter': onto.ZBTC, 'name': 'usdt -> duet -> zbtc -> zusd -> usdt', 'weight': 1.2},
             {'val': eval_plan_4(onto.ZNAS), 'action': take_plan_4, 'parameter': onto.ZNAS, 'name': 'usdt -> duet -> znas -> zusd -> usdt', 'weight': 1.2},
            #  {'val': eval_plan_5(), 'action': take_plan_5, 'name': 'usdt -> zusd swap duet -> usdt', 'weight': 1},
             {'val': eval_plan_6(onto.ZBTC), 'action': take_plan_6, 'parameter': onto.ZBTC,'name': 'usdt -> duet - mint -zusd -> zbtc-redeem- duet - mint zusd -> usdt', 'weight': 1},
             {'val': eval_plan_6(onto.ZNAS), 'action': take_plan_6, 'parameter': onto.ZNAS,'name': 'usdt -> duet - mint -zusd -> znas-redeem- duet - mint zusd -> usdt', 'weight': 1},

        ]
        evals =  sorted(evals, key=lambda x: x['val'] * x['weight'], reverse=True)
        evals = [x for x in evals if x['val'] > benefit_limit]
        # final_plan = evals[0]
        if not evals:
            return []

        # final_plan = choice(evals)
        # final_plan = evals[0]
        final_plan = choices(population=evals, weights=[x['val'] for x in evals], k =1)[0]

        if final_plan['val'] > benefit_limit:
            
            # for adjust
            # amount = (final_plan['val'] / benefit_limit) * amount
            if final_plan['val'] < amount/4:
                amount = final_plan['val']
            elif final_plan['val'] < amount:
                amount = amount
            else:
                amount_inc = ((final_plan['val']) / amount) ** 2
                amount  = amount * amount_inc

            if agent.states[start_token] <= amount:
                amount = agent.states[start_token]

            print('choose {}'.format(final_plan['name']))
            if 'parameter' in final_plan.keys():
                return final_plan['action'](final_plan['parameter'])

            else:
                return final_plan['action']()
        else:
            return []

    @staticmethod
    def choose_invest_plan(agent):
        onto = agent.belief.onto
        create_action = agent.belief.create_action
        duet_system = agent.system

        # choose stake farm pool fram the benefit

        # stake duet
        def eval_plan_1():
            pass

        # farm deut_usdt

        # farm zusd_usdt

        # farm zbtc_zusd

        # farm znas_zusd
