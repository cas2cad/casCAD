import sys

from plotly.subplots import make_subplots
import plotly.graph_objs as go 
sys.path.append('.')
from cascad.settings import BASE_DIR

from sqlite3.dbapi2 import Row
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
# from aletheia.agents.desires import SellFounder, HoldFounder, DuetHold, DuetHoldAndFarm, DuetHoldAndStake, DAssetHold, DAssetHoldAndFarm, ShortFarmArbitrage, Spread, BullishDAsset, BullishDUET, BearrishDUET, BearrishDAsset
from cascad.experiment.MBM.desires import SellFounder, HoldFounder, DuetHold, DuetHoldAndFarm, DuetHoldAndStake, DAssetHold, DAssetHoldAndFarm, ShortFarmArbitrage, Spread, BullishDAsset, BullishDUET, BearrishDUET, BearrishDAsset

from cascad.experiment.MBM.constant import BTC

# from aletheia.utils.constant import BTC
# from aletheia.settings import BASE_DIR
import os


import pandas as pd
from pandas import  DataFrame
import glob

MINT_ZUSD_ORIING = 'mint_zusd_origin'
MINT_ZUSD_TARGET = 'mint_zusd_target'
MINT_ZNAS_ORIGIN = 'mint_znas_origin'
MINT_ZNAS_TARGET = 'mint_znas_target'
MINT_ZBTC_ORIGIN = 'mint_zbtc_origin'
MINT_ZBTC_TARGET = 'mint_zbtc_target'
REDEEM_ZUSD_ORIGIN = 'redeem_zusd_origin'
REDEEM_ZUSD_TARGET = 'redeem_zusd_target'
REDEEM_ZNAS_ORIGIN = 'redeem_znas_origin'
REDEEM_ZNAS_TARGET = 'redeem_znas_target'
REDEEM_ZBTC_ORIGIN = 'redeem_zbtc_origin'
REDEEM_ZBTC_TARGET = 'redeem_zbtc_target'
USDT_ZUSD1 = 'usdt->zusd1'
USDT_ZUSD2 = 'usdt->zusd2'
ZUSD_ZBTC1 = 'zusd->zbtc1'
ZUSD_ZBTC2 = 'zusd->zbtc2'
ZUSD_ZNAS1 = 'zusd->znas1'
ZUSD_ZNAS2 = 'zusd->znas2'
ZUSD_USDT1 = 'zusd->usdt1'
ZUSD_USDT2 = 'zusd->usdt2'
ZNAS_ZUSD1 = 'znas->zusd1'
ZNAS_ZUSD2 = 'znas->zusd2'
ZBTC_ZUSD1 = 'zbtc->zusd1'
ZBTC_ZUSD2 = 'zbtc->zusd2'
DUET_PRICE = 'duet_price'
DUSD_PRICE = 'dusd_price'
DBTC_PRICE = 'dbtc_price'
DNAS_PRICE = 'dnas_price'

price_dict = {
MINT_ZUSD_ORIING : DUET_PRICE,
MINT_ZUSD_TARGET : DUSD_PRICE,
MINT_ZNAS_ORIGIN : DUET_PRICE, 
MINT_ZNAS_TARGET : DNAS_PRICE, 
MINT_ZBTC_ORIGIN : DUET_PRICE, 
MINT_ZBTC_TARGET : DBTC_PRICE, 
REDEEM_ZUSD_ORIGIN : DUSD_PRICE, 
REDEEM_ZUSD_TARGET : DUET_PRICE, 
REDEEM_ZNAS_ORIGIN : DNAS_PRICE, 
REDEEM_ZNAS_TARGET : DUET_PRICE, 
REDEEM_ZBTC_ORIGIN : DBTC_PRICE, 
REDEEM_ZBTC_TARGET : DUET_PRICE, 
USDT_ZUSD2 : DUSD_PRICE, 
ZUSD_ZBTC1 : DUSD_PRICE, 
ZUSD_ZBTC2 : DBTC_PRICE, 
ZUSD_ZNAS1 : DUSD_PRICE, 
ZUSD_ZNAS2 : DNAS_PRICE, 
ZUSD_USDT1 : DUSD_PRICE, 
ZNAS_ZUSD1 : DNAS_PRICE, 
ZNAS_ZUSD2 : DUSD_PRICE, 
ZBTC_ZUSD1 : DBTC_PRICE, 
ZBTC_ZUSD2 : DUSD_PRICE 
}


def load_pl_sheet(name):

    path = os.path.join(BASE_DIR, 'resources', 'exp3')

    # pl_sheet_path = os.path.join(path, 'dasset_pl_new.csv')
    pl_sheet_path = os.path.join(path, 'dasset_pl_new_{}.csv'.format(name))

    df = pd.read_csv(pl_sheet_path)
    for k,v in price_dict.items():
        df[k] = df[k] * df[v]

    return df

def compute_lp_reward(df: DataFrame, pool: str):
    
    df['Agents Num'] = df['agent_count'].expanding(2).sum()
    df['Agents Num'][0] = df['agent_count'][0]

    reward_column = pool + '_reward'
    pool_column = pool + '_lp'
    pool_agent_num = pool + '_num'
    df[pool_agent_num][0] += 0.1
    # df['Farming Reward'] = df[reward_column] 

    farming_reward_1 = df[reward_column][1:]
    farming_reward_1.reset_index(inplace=True, drop=True)
    farming_reward_2 = df[reward_column][:-1]
    farming_reward_2.reset_index(inplace=True, drop=True)
    farming_reward = farming_reward_1 -farming_reward_2
    farming_reward.index += 1

    df['Farming Reward'] =  farming_reward
    df['Farming Reward'][0] = 0
    df['Farming Reward'] = (farming_reward * df['duet_price']) / df[pool_agent_num]
   
    df['Farming LP'] = df[pool_column] / df[pool_agent_num]
    return df


def compute_pnl(df:DataFrame, daset=True):
    # df['networth_dasset'] = df.apply(lambda x: x['dusd_value'] + x['dbtc_value'] + x['duet_value'] + x['dnas_value']  + x['usdt_num'], axis=1)
    # df['networth_asset'] = df.apply(lambda x: x['usd_value'] + x['btc_value'] + x['nas_value']  + x['duet_value'] + x['usdt_num'], axis=1)
    df['networth_dasset'] = df.apply(lambda x: x['dusd_value'] + x['dbtc_value'] + x['dnas_value']  + x['usdt_num'], axis=1)
    df['networth_asset'] = df.apply(lambda x: x['usd_value'] + x['btc_value'] + x['nas_value']   + x['usdt_num'], axis=1)

    networth_dasset_1 = df['networth_dasset'][1:]
    networth_dasset_1.reset_index(inplace=True, drop=True)
    networth_dasset_2 = df['networth_dasset'][:-1]
    networth_dasset_2.reset_index(inplace=True, drop=True)

    df['profit_dasset'] = networth_dasset_1 - networth_dasset_2
    # df['profit_dasset'] =  df['networth_dasset'][1:] - df['networth_dasset'][:-1]
    # df['profit_asset'] =  df['networth_asset'][1:] - df['networth_asset'][:-1]
    networth_asset_1 = df['networth_asset'][1:]
    networth_asset_1.reset_index(drop=True, inplace=True)
    networth_asset_2 = df['networth_asset'][:-1]
    networth_asset_2.reset_index(drop=True, inplace=True)

    df['profit_asset'] = networth_asset_1 - networth_asset_2
    df['profit_diff'] = df['profit_dasset'] - df['profit_asset']

    # return df['profit_dasset'], df['profit_asset']
    return df


def create_multiline(df: DataFrame, columns = [
        'day'
    ], sum_up=False):

    if sum_up:
        result = {
            'day' : [],
            'value': [],
            # 'color': []
        }
    else:
        result = {
            'day' : [],
            'value': [],
            'color': []
        }


    column_name = {
        'dbtc_value': 'dBTC Value',
        'dbtc_num': 'dBTC Num',
        'btc_value': 'BTC Value',
        'dnas_value': 'dNAS Value',
        'dnas_num': 'dNAS Num',
        'nas_value': 'NAS Value',
        'dusd_value': 'dUSD Value',
        'usd_value': 'USD Value',
        'dusd_num': 'dUSD Num',
        'usdt_num': 'USDT Value',
        'mint_zusd_origin': 'Minted DUET',
        'mint_zusd_target': 'Gained dUSD',
        'mint_znas_origin': 'Minted DUET',
        'mint_znas_target': 'Gained dNAS',
        'mint_zbtc_origin': 'Minted DUET',
        'mint_zbtc_target': 'Gained dBTC',
        'redeem_zusd_origin': 'Redeemed dUSD',
        'redeem_zusd_target': 'Gained DUET',
        'redeem_znas_origin': 'Redeemed dNAS',
        'redeem_znas_target': 'Gained DUET',
        'redeem_zbtc_origin': 'Redeemed dBTC',
        'redeem_zbtc_target': 'Gained DUET',
        'duet_num': 'DUET Num',
        'duet_value': 'DUET Value',
        'usdt->zusd1': 'USDT',
        'usdt->zusd2': 'dUSD',
        'zusd->zbtc1': 'dUSD',
        'zusd->zbtc2': 'dBTC',
        'zusd->znas1': 'dUSD',
        'zusd->znas2': 'dNAS',
        'zusd->usdt1': 'dUSD',
        'zusd->usdt2': 'USDT',
        'znas->zusd1': 'dNAS',
        'znas->zusd2': 'dUSD',
        'zbtc->zusd1': 'dBTC',
        'zbtc->zusd2': 'dUSD',
        'profit_asset': 'PNL with Assets',
        'profit_dasset': 'PNL with dAssets',
        'profit_diff': 'PNL difference between using Assets and dAssets',
        'Farming Reward': 'Farming Reward',
        'Farming LP': 'Farming LP'
    }

    if sum_up:
        for index, row in df.iterrows():
            value = 0
    
            result['day'].append(row['day'])
    
            for column in columns:
                value += row[column]
            result['value'].append(value)
    else:
        for index, row in df.iterrows():
            for column in columns:
                result['day'].append(row['day'])
                result['value'].append(row[column])
                result['color'].append(column_name[column])

    return pd.DataFrame(data = result)

def create_dfs(name, choose=1):
    # names = ['duetdatas-high-gas-final_6', 'duetdatas-normal-final_6', 'duetdatas-pries-change-final_6', 'duetdatas-low-liquidity-final_6', 'duetdatas-no-reward-final_6']

    # for name in names:
    #     df = load_pl_sheet(name)
    df = load_pl_sheet(name)
    if choose == 1:

        df_btc = create_multiline(df, columns = [
        'dbtc_value',
        # 'dbtc_num',
        'btc_value',
        ])
        
        return df_btc

    elif choose == 2:

        df_nas = create_multiline(df, columns = [
        'dnas_value',
        # 'dnas_num',
        'nas_value',
        ])

        return df_nas

    elif choose == 3:

        df_usd = create_multiline(df, columns = [
        'dusd_value',
        'usd_value',
        # 'dusd_num',
        ])
        
        return df_usd

    elif choose == 4:
        df_count = df[['day', 'agent_count']]
        df_count['Agents Num'] = df_count['agent_count'].expanding(2).sum()
        df_count['Agents Num'][0] = df_count['agent_count'][0]
        return df_count

    elif choose == 5:
        df_networth = df[['day', 'networth']]
        df_networth['Net Worth'] = df_networth['networth']
        return df_networth

    # dusd
    elif choose == 6:
        df_dusd_mint_origin = create_multiline(df, columns = [
            'mint_zusd_origin',
            # 'mint_zusd_target'
        ], sum_up = True)
        df_dusd_mint_target = create_multiline(df, columns = [
            'mint_zusd_target',
            # 'mint_zusd_target'
            'usdt->zusd2'
        ])
        df_dusd_swap_1 = create_multiline(df, columns = [
            'usdt->zusd1'
        ])

        return df_dusd_mint_origin, df_dusd_mint_target, df_dusd_swap_1

    #dnas
    elif choose == 7:
        df_dnas_mint_origin = create_multiline(df, columns = [
            'mint_znas_origin',
            # 'mint_znas_target'
        ], sum_up = True)
        df_dnas_mint_target = create_multiline(df, columns = [
            # 'mint_znas_origin',
            'mint_znas_target',
            'zusd->znas2'
        ])
        df_dnas_swap_1= create_multiline(df, columns = [
            'zusd->znas1'
        ])


        return df_dnas_mint_origin, df_dnas_mint_target, df_dnas_swap_1

    #dbtc
    elif choose == 8:
        df_dbtc_mint_origin = create_multiline(df, columns = [
            'mint_zbtc_origin',
            # 'mint_zbtc_target'
        ], sum_up=True)

        df_dbtc_mint_target = create_multiline(df, columns = [
            # 'mint_zbtc_origin',
            'mint_zbtc_target',
            'zusd->zbtc2'
        ])
        
        df_dbtc_swap_1= create_multiline(df, columns = [
            'zusd->zbtc1'
        ])

        return df_dbtc_mint_origin, df_dbtc_mint_target, df_dbtc_swap_1


    #dusd
    elif choose == 9:
        df_dusd_redeem_origin = create_multiline(df, columns = [
            'redeem_zusd_origin',
            # 'redeem_zusd_target'
            'zusd->usdt1'
        ], sum_up=True)

        df_dusd_redeem_target = create_multiline(df, columns = [
            'redeem_zusd_target',
            # 'redeem_zusd_target'
            # 'zusd->usdt1'
        ])

        df_dusd_swap_2 = create_multiline(df, columns=[
            'zusd->usdt2'
        ])

        return df_dusd_redeem_origin, df_dusd_redeem_target, df_dusd_swap_2

    #dnas
    elif choose == 10:
        df_dnas_redeem_origin = create_multiline(df, columns = [
            'redeem_znas_origin',
            # 'redeem_znas_target'
            'znas->zusd1'
        ], sum_up=True)

        df_dnas_redeem_target = create_multiline(df, columns = [
            'redeem_znas_target',
        ])

        df_dnas_swap_2 = create_multiline(df, columns = [
            'znas->zusd2',
        ])


        return df_dnas_redeem_origin, df_dnas_redeem_target, df_dnas_swap_2

    #dbtc
    elif choose == 11:
        df_dbtc_redeem_origin = create_multiline(df, columns = [
            'redeem_zbtc_origin',
            'zbtc->zusd1'
        ], sum_up=True)

        df_dbtc_redeem_target = create_multiline(df, columns = [
            'redeem_zbtc_target',
        ])

        df_dbtc_swap_2 = create_multiline(df, columns = [
            'zbtc->zusd2',
        ])

        return df_dbtc_redeem_origin, df_dbtc_redeem_target, df_dbtc_swap_2

    # holding
    elif choose == 12:
        df_holdings = create_multiline(df, columns = [
            'dusd_value',
            'dbtc_value',
            'dnas_value',
            'duet_value',
            'usdt_num'
        ])
        return df_holdings

    elif choose == 13:
        df = compute_pnl(df)
        df_pnl = create_multiline(df, columns = [
            'profit_asset',
            'profit_dasset'
        ])

        return df_pnl

    elif choose == 14:
        df = compute_pnl(df)
        df_pnl = create_multiline(df, columns = [
            'profit_diff'
        ])
        return df_pnl

    elif choose == 15:
        df = compute_lp_reward(df, 'zusd_usdt')
        df_lp_reward_reward = create_multiline(df, columns = [
            'Farming Reward',
            # 'Farming LP'
        ])

        df_lp_reward_lp =  create_multiline(df, columns = [
            # 'Farming Reward',
            'Farming LP'
        ])

        return df_lp_reward_reward, df_lp_reward_lp

    elif choose == 16:
        df = compute_lp_reward(df, 'zbtc_zusd')
        df_lp_reward_reward = create_multiline(df, columns = [
            'Farming Reward',
            # 'Farming LP'
        ])

        df_lp_reward_lp =  create_multiline(df, columns = [
            # 'Farming Reward',
            'Farming LP'
        ])

        return df_lp_reward_reward, df_lp_reward_lp


    elif choose == 17:
        df = compute_lp_reward(df, 'znas_zusd')
        df_lp_reward_reward = create_multiline(df, columns = [
            'Farming Reward',
            # 'Farming LP'
        ])

        df_lp_reward_lp =  create_multiline(df, columns = [
            # 'Farming Reward',
            'Farming LP'
        ])

        return df_lp_reward_reward, df_lp_reward_lp



def create_fig(choose = 1, name=''):
    df = create_dfs(name, choose)
    if choose == 4:
        df_count_fig = px.line(df, x='day', y='Agents Num', title='Agents Number Distribution')
        # df_count_fig = px.bar(df, x='day', y='Agents Num', title='Agents Number Distribution', barmode="group")

        return dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id = 'agent_number',
                        figure=df_count_fig,
                        style = { 'width': '100%'}
                    )
                )
            ]
        )
    
    elif choose == 5:
        df_networth_fig = px.bar(df, x='day', y='Net Worth', title='Agents Networth Distribution')
        return dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id = 'agent_networth',
                        figure=df_networth_fig,
                        style = { 'width': '100%'}
                    )
                )
            ]
        )
    elif choose == 6: #dusd mint
        # df_minting_fig = px.bar(df, x='day', y='value', color='color', title='dUSD Minting Amounts', barmode="group")
        # df_minting_fig = make_subplots(rows=2, cols=1, title='dUSD Minting Redeeming Amount')
        df_minting_fig = make_subplots(rows=2, cols=2, specs=[
            [{}, {}],
            [{'colspan': 2}, None]
            ])

        df_minting_fig.append_trace(
            go.Bar(x= df[0]['day'], y=df[0]['value'], name='Minted DUET'), row=1, col=1
        )
        df_minting_fig.append_trace(
            go.Bar(x= df[1]['day'], y=df[1]['value'], name='Gained dUSD'), row=2, col=1
        )

        df_minting_fig.append_trace(
            go.Bar(x=df[2]['day'], y = df[2]['value'], name='Swapped USDT'), row=1, col=2
        )
        for i in range(1,4): 
            df_minting_fig['layout']['xaxis{}'.format(i)]['title']='day'
            df_minting_fig['layout']['yaxis{}'.format(i)]['title']='value'

        df_minting_fig.update_layout(title_text='dUSD Minting and Swapping Amount')
        # df_minting_fig['layout']['xaxis']['title']='Label x-axis 1'
        # df_minting_fig['layout']['xaxis2']['title']='Label x-axis 2'


        return dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                    id = 'dusd_minting',
                    figure = df_minting_fig,
                    style = { 'width': '100%', 'height': '1200px'}
                    )
                    )
            ])
    elif choose == 7: #dnas  mint
        # df_minting_fig = px.bar(df, x='day', y='value', color='color', title='dNAS Minting Amounts', barmode="group")
        # df_minting_fig = make_subplots(rows=2, cols=1, title='dNAS Minting Redeeming Amount')
        df_minting_fig = make_subplots(rows=2, cols=2,specs = [
            [{}, {}],
            [{'colspan': 2}, None]
        ])

        df_minting_fig.append_trace(
            go.Bar(x= df[0]['day'], y=df[0]['value'], name='Minted DUET'), row=1, col=1
        )
        df_minting_fig.append_trace(
            go.Bar(x= df[1]['day'], y=df[1]['value'], name='Gained dNAS'), row=2, col=1
        )

        df_minting_fig.append_trace(
            go.Bar(x= df[2]['day'], y=df[2]['value'], name='Swapped dUSD'), row=1, col=2
        )
        df_minting_fig.update_layout(title_text='dNAS Minting and Swapping Amount')
        for i in range(1,4): 
            df_minting_fig['layout']['xaxis{}'.format(i)]['title']='day'
            df_minting_fig['layout']['yaxis{}'.format(i)]['title']='value'


        return dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                    id = 'dnas_minting',
                    figure = df_minting_fig,
                    style = { 'width': '100%', 'height': '1200px'}
                    )
                    )
            ])
    elif choose == 8: #dbtc mint
        # df_minting_fig = px.bar(df, x='day', y='value', color='color', title='dBTC Minting Amounts', barmode="group")
        # df_minting_fig = make_subplots(rows=2, cols=1, title='dBTC Minting Redeeming Amount')
        df_minting_fig = make_subplots(rows=2, cols=2, specs = [
            [{}, {}],
            [{'colspan': 2}, None]
        ])

        df_minting_fig.append_trace(
            go.Bar(x= df[0]['day'], y=df[0]['value'], name='Minted DUET'), row=1, col=1
        )
        df_minting_fig.append_trace(
            go.Bar(x= df[1]['day'], y=df[1]['value'], name='Gained dBTC'), row=2, col=1
        )
        df_minting_fig.append_trace(
            go.Bar(x= df[2]['day'], y=df[2]['value'], name='Swapped dUSD'), row=1, col=2
        )
        df_minting_fig.update_layout(title_text='dBTC Minting and Swapping Amount')
        for i in range(1,4): 
            df_minting_fig['layout']['xaxis{}'.format(i)]['title']='day'
            df_minting_fig['layout']['yaxis{}'.format(i)]['title']='value'

        return dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                    id = 'dbtc_minting',
                    figure = df_minting_fig,
                    style = { 'width': '100%', 'height': '1200px'}
                    )
                )
            ])

    elif choose == 9: #dusd redeem
        # df_minting_fig = px.bar(df, x='day', y='value', color='color', title='dUSD Redeeming Amounts', barmode="group")
        df_minting_fig = make_subplots(rows=2, cols=2, specs=[
            [{}, {}],
            [{'colspan': 2}, None]
            ])

        df_minting_fig.append_trace(
            go.Bar(x= df[0]['day'], y=df[0]['value'], name='Cost dUSD'), row=2, col=1
        )
        df_minting_fig.append_trace(
            go.Bar(x= df[1]['day'], y=df[1]['value'], name='Redeem Gained DUET'), row=1, col=1
        )

        df_minting_fig.append_trace(
            go.Bar(x=df[2]['day'], y = df[2]['value'], name='Swap Gained USDT'), row=1, col=2
        )
        df_minting_fig.update_layout(title_text='dUSD Redeeming and Swapping Amount')
        for i in range(1,4): 
            df_minting_fig['layout']['xaxis{}'.format(i)]['title']='day'
            df_minting_fig['layout']['yaxis{}'.format(i)]['title']='value'


        return dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                    id = 'dusd_redeeming',
                    figure = df_minting_fig,
                    style = { 'width': '100%', 'height': '1200px'}
                    )
                    )
            ])
    elif choose == 10: #dnas  redeem
        # df_minting_fig = px.bar(df, x='day', y='value', color='color', title='dNAS Redeeming Amounts', barmode="group")
        df_minting_fig = make_subplots(rows=2, cols=2,  specs=[
            [{}, {}],
            [{'colspan': 2}, None]
            ])

        df_minting_fig.append_trace(
            go.Bar(x= df[0]['day'], y=df[0]['value'], name='Cost dNAS'), row=2, col=1
        )
        df_minting_fig.append_trace(
            go.Bar(x= df[1]['day'], y=df[1]['value'], name='Redeem Gained DUET'), row=1, col=1
        )

        df_minting_fig.append_trace(
            go.Bar(x=df[2]['day'], y = df[2]['value'], name='Swap Gained dUSD'), row=1, col=2
        )

        df_minting_fig.update_layout(title_text='dNAS Redeeming and Swapping Amount')
        for i in range(1,4): 
            df_minting_fig['layout']['xaxis{}'.format(i)]['title']='day'
            df_minting_fig['layout']['yaxis{}'.format(i)]['title']='value'


        return dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                    id = 'dnas_redeeming',
                    figure = df_minting_fig,
                    style = { 'width': '100%', 'height': '1200px'}
                    )
                    )
            ])
    elif choose == 11: #dbtc redeem
        # df_minting_fig = px.bar(df, x='day', y='value', color='color', title='dBTC Redeeming Amounts', barmode="group")
        df_minting_fig = make_subplots(rows=2, cols=2,  specs=[
            [{}, {}],
            [{'colspan': 2}, None]
            ])

        df_minting_fig.append_trace(
            go.Bar(x= df[0]['day'], y=df[0]['value'], name='Cost dBTC'), row=2, col=1
        )
        df_minting_fig.append_trace(
            go.Bar(x= df[1]['day'], y=df[1]['value'], name='Redeem Gained DUET'), row=1, col=1
        )

        df_minting_fig.append_trace(
            go.Bar(x=df[2]['day'], y = df[2]['value'], name='Swap Gained dUSD'), row=1, col=2
        )

        df_minting_fig.update_layout(title_text='dBTC Redeeming and Swapping Amount')

        for i in range(1,4): 
            df_minting_fig['layout']['xaxis{}'.format(i)]['title']='day'
            df_minting_fig['layout']['yaxis{}'.format(i)]['title']='value'


        return dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                    id = 'dbtc_redeeming',
                    figure = df_minting_fig,
                    style = { 'width': '100%', 'height': '1200px'}
                    )
                )
            ])

    elif choose == 12: #dasset holdings
        df_dasset_holding= px.pie(df, values='value', names='color', title='dAssets Holdings')
        return dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                    id = 'dAssets_holding',
                    figure = df_dasset_holding,
                    style = { 'width': '50%', 'textAlign': 'center'}
                    )
                )
            ])

    elif choose == 13:
        # df_dasset_pnl = create
        df_count_fig = px.line(df, x='day', y='value', color='color', title='Assets/dAssets Profit and Loss')

        return dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id = 'agent_number_idf',
                        figure=df_count_fig,
                        style = { 'width': '92%'}
                    )
                )
            ]
        )

    elif choose == 14:
        # df_dasset_pnl = create
        df_count_fig = px.line(df, x='day', y='value', color='color', title='Assets/dAssets Profit and Loss Difference')

        return dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id = 'agent_profit_diff',
                        figure=df_count_fig,
                        style = { 'width': '100%'}
                    )
                )
            ]
        )
    elif choose == 15:
        # df_dasset_pnl = create
        # df_count_fig = px.line(df, x='day', y='value', color='color', title='dUSD/USDT Farming LP and Reward')

        df_minting_fig = make_subplots(rows=1, cols=2,  specs=[
            [{}, {}],
            # [{'colspan': 2}, None]
            ])

        df_minting_fig.append_trace(
            go.Line(x= df[0]['day'], y=df[0]['value'], name='dUSD/USDT Farming Rewards'), row=1, col=1
        )
        df_minting_fig.append_trace(
            go.Line(x= df[1]['day'], y=df[1]['value'], name='dUSD/USDT Farming LP Share'), row=1, col=2
        )

        df_minting_fig.update_layout(title_text='dUSD/USDT Farming LP Share and Rewards')

        for i in range(1,3): 
            df_minting_fig['layout']['xaxis{}'.format(i)]['title']='day'
            df_minting_fig['layout']['yaxis{}'.format(i)]['title']='value'


        return dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                    id = 'dusd_usdt_lp',
                    figure = df_minting_fig,
                    style = { 'width': '100%', 'height': '600px'}
                    )
                )
            ])

        # return dbc.Row(
        #     [
        #         dbc.Col(
        #             dcc.Graph(
        #                 id = 'farming lp reward',
        #                 figure=df_count_fig,
        #                 style = { 'width': '100%'}
        #             )
        #         )
        #     ]
        # )

    elif choose == 16:
        # df_dasset_pnl = create
        # df_count_fig = px.line(df, x='day', y='value', color='color', title='dBTC/dUSD Farming LP and Reward')

        df_minting_fig = make_subplots(rows=1, cols=2,  specs=[
            [{}, {}],
            # [{'colspan': 2}, None]
            ])

        df_minting_fig.append_trace(
            go.Line(x= df[0]['day'], y=df[0]['value'], name='dBTC/dUSD Farming Rewards'), row=1, col=1
        )
        df_minting_fig.append_trace(
            go.Line(x= df[1]['day'], y=df[1]['value'], name='dBTC/dUSD Farming LP Share'), row=1, col=2
        )

        df_minting_fig.update_layout(title_text='dBTC/dUSD Farming LP Share and Rewards')

        for i in range(1,3): 
            df_minting_fig['layout']['xaxis{}'.format(i)]['title']='day'
            df_minting_fig['layout']['yaxis{}'.format(i)]['title']='value'


        return dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                    id = 'dusd_usdt_lp',
                    figure = df_minting_fig,
                    style = { 'width': '100%', 'height': '600px'}
                    )
                )
            ])

        # return dbc.Row(
        #     [
        #         dbc.Col(
        #             dcc.Graph(
        #                 id = 'farming lp reward',
        #                 figure=df_count_fig,
        #                 style = { 'width': '100%'}
        #             )
        #         )
        #     ]
        # )

    elif choose == 17:
        # df_dasset_pnl = create
        # df_count_fig = px.line(df, x='day', y='value', color='color', title='dNAS/dUSD Farming LP and Reward')
        df_minting_fig = make_subplots(rows=1, cols=2,  specs=[
            [{}, {}],
            # [{'colspan': 2}, None]
            ])

        df_minting_fig.append_trace(
            go.Line(x= df[0]['day'], y=df[0]['value'], name='dNAS/dUSD Farming Rewards'), row=1, col=1
        )
        df_minting_fig.append_trace(
            go.Line(x= df[1]['day'], y=df[1]['value'], name='dNAS/dUSD Farming LP Share'), row=1, col=2
        )

        df_minting_fig.update_layout(title_text='dNAS/dUSD Farming LP Share and Rewards')

        for i in range(1,3): 
            df_minting_fig['layout']['xaxis{}'.format(i)]['title']='day'
            df_minting_fig['layout']['yaxis{}'.format(i)]['title']='value'


        return dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                    id = 'dusd_usdt_lp',
                    figure = df_minting_fig,
                    style = { 'width': '100%', 'height': '600px'}
                    )
                )
            ])


        # return dbc.Row(
        #     [
        #         dbc.Col(
        #             dcc.Graph(
        #                 id = 'farming lp reward',
        #                 figure=df_count_fig,
        #                 style = { 'width': '100%'}
        #             )
        #         )
        #     ]
        # )




def create_row_show(name, choose=1):
    df = create_dfs(name, choose)


    if choose == 1:

        df_btc_fig = px.line(df, x='day', y='value', color='color', title='{} Distribution'.format('dBTC'))

        df_btc_fig.update_layout(
            xaxis = dict(
                tickmode = 'linear',
                tick0 = df['day'][0],
                dtick = 7,
                tickfont_size=8,
            )
        )
        return dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='{}_btc'.format(name),
                        figure=df_btc_fig,
                        style = { 'width': '100%'}
                    )
                ),
            ]
        )

    elif choose == 2:

        df_nas_fig = px.line(df, x='day', y='value', color='color', title='{} Distribution'.format('dNAS'))

        df_nas_fig.update_layout(
            xaxis = dict(
                tickmode = 'linear',
                tick0 = df['day'][0],
                dtick = 7,
                tickfont_size=8,
            )
        )

        return dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='{}_nas'.format(name),
                        figure=df_nas_fig,
                        style = { 'width': '100%'}
                    )
                )
            ]
        )

    elif choose == 3:

        df_usd_fig = px.line(df, x='day', y='value', color='color', title='{} Distribution'.format('dUSD'))
        df_usd_fig.update_layout(
            xaxis = dict(
                tickmode = 'linear',
                tick0 = df['day'][0],
                dtick = 7,
                tickfont_size=8,
            )
        )

        return dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='{}_usd'.format(name),
                        figure=df_usd_fig,
                        style = { 'width': '100%'}
                    )
                )
            ]
        )

def create_detail_fig(name):

    # names = ['duetdatas-high-gas-final_6', 'duetdatas-normal-final_6', 'duetdatas-pries-change-final_6', 'duetdatas-low-liquidity-final_6', 'duetdatas-no-reward-final_6']
    # names = ['duetdatas-high-gas-final_6', 'duetdatas-pries-change-final_6', 'duetdatas-low-liquidity-final_6', 'duetdatas-no-reward-final_6']

    # names = ['duetdatas-high-gas-final_6']
    names = [name]


    figs = [html.Hr()]
    for name in names:
        figs.append(dbc.Row(dbc.Col(html.H1(name))))

        figs.append(create_row_show(name, 1))
        figs.append(create_row_show(name, 2))
        figs.append(create_row_show(name, 3))
        figs.append(create_fig(4, name))
        figs.append(create_fig(5, name))
        figs.append(create_fig(6, name))
        figs.append(create_fig(7, name))
        figs.append(create_fig(8, name))
        figs.append(create_fig(9, name))
        figs.append(create_fig(10, name))
        figs.append(create_fig(11, name))
        figs.append(create_fig(12, name))
        figs.append(create_fig(13, name))
        figs.append(create_fig(14, name))
        figs.append(create_fig(15, name))
        figs.append(create_fig(16, name))
        figs.append(create_fig(17, name))

        figs.append(html.Hr())


    page_layout = html.Div(figs, style={'display': 'inline-block', 'width': '100%'})
    return page_layout
   
def get_index_page():
    # names = ['duetdatas-high-gas-final_6', 'duetdatas-normal-final_6', 'duetdatas-pries-change-final_6', 'duetdatas-low-liquidity-final_6', 'duetdatas-no-reward-final_6']
    names = [SellFounder.name, HoldFounder.name, DuetHold.name,DuetHoldAndFarm.name, DuetHoldAndStake.name, DAssetHold.name, DAssetHoldAndFarm.name, ShortFarmArbitrage.name, Spread.name, BullishDAsset.name, BullishDUET.name, BearrishDAsset.name, BearrishDUET.name]

    names = ["Iter {}".format(name) for name in range(730)]
    links = []
    for name in names:
        item = {
            'name': name,
            'href': '/{}'.format(name)
        }
        links.append(item)

    card_links = []
    for link in links:
        card_content = [
            dbc.CardHeader(link['name']),
            dbc.CardBody([
                dcc.Link('details', href=link['href'])
            ])
        ]
        card_links.append(card_content)

    link_number = len(card_links)
    result = []

    for i in range(1, 30):
        i_start = (i - 1) * 6
        i_end = i * 6
        if i_start >= link_number:
            break
        tmp_row = dbc.Row(
            [
                dbc.Col(dbc.Card(x, color='success', outline=True)) for x in card_links[i_start: i_end]
            ]
        )
        result.append(tmp_row)

    page = html.Div(result)
    return page