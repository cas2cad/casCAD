from aletheia.utils.constant import BTC
from aletheia.settings import BASE_DIR
from aletheia.utils.votality import Votality
from aletheia.artificial_system.oracle import Oracle
from aletheia.scenario_generator.timeline import TimeLine
import os


import pandas as pd
import glob

# path = r'C:\DRO\DCL_rawdata_files' # use your path
# all_files = glob.glob(path + "/*.csv")

# li = []

# for filename in all_files:
#     df = pd.read_csv(filename, index_col=None, header=0)
#     li.append(df)

# frame = pd.concat(li, axis=0, ignore_index=True)
# _votality = Votality()
_timeline = TimeLine()
_oracle = Oracle(_timeline)

class Analyze:
    def __init__(self, path_name, price_change = False):
        # self.path = os.path.join(BASE_DIR, 'resources', 'duetdatas-c')
        self.path = os.path.join(BASE_DIR, 'resources', path_name)
        self.actual_prices = _oracle.prices
        self.price_change = price_change
        if self.price_change == True:
            self.set_price_changing()

    def create_price_df(self, columns= [], x='day'):
        df = self.system_df
        result = {
            x: [],
            'value': [],
            'color': []
        }
        for index, row in df.iterrows():
            # print(row['c1'], row['c2'])
            for column in columns:
                result[x].append(row['day'])
                result['value'].append(row[column])
                result['color'].append(column)

        return pd.DataFrame(data = result)

        pass

    def create_multiline(self, columns=['zusd_total_minted', 'znas_total_minted', 'zbtc_total_minted'], x='day'):
        df = self.system_df
        result = {
            x: [],
            'value': [],
            'color': []
        }
        price_dict = {
            'zusd_total_minted': 'zusd_price',
            'znas_total_minted': 'znas_price',
            'zbtc_total_minted': 'zbtc_price',
            'zusd_total_burned': 'zusd_price',
            'znas_total_burned': 'znas_price',
            'zbtc_total_burned': 'zbtc_price'

            }
        pre_price = {}
        pre_one = {}
        for column in columns:
            pre_one[column] = 0
            pre_price[column] = 0

        for index, row in df.iterrows():
            # print(row['c1'], row['c2'])
            for column in columns:
                price_column = price_dict[column]
                # price_column_minus = price_column.iloc[1:] - price_column.iloc[:-1]
                # if index >= 0:
                adds =  row[column] - pre_one[column]
                adds = adds * row[price_column]
                
                result[x].append(row['day'])
                # result['value'].append(row[column] * row[price_column])
                result['value'].append(pre_price[column] + adds)
                result['color'].append(column.replace('z', 'd'))
                pre_one[column] = row[column]
                pre_price[column] = pre_price[column] + adds

        return pd.DataFrame(data = result)

    def set_price_changing(self):
        # days = [100, 300, 500]
        # days2 = [ 200, 400, 600]
        # very_high = [1, 31, 61, 91]
        # very_low = [121, 151, 181, 211]
        # medium_high = []
        # medium_low = [] 
        very_high = list(range(1, 7)) + list(range(31, 37)) + list(range(61, 67)) + list(range(91, 97)) + list(range(121, 127)) + list(range(151, 157)) 
        very_low = list(range(181, 187)) + list(range(211, 217)) + list(range(241, 247)) + list(range(271, 277)) + list(range(301, 307)) + list(range(331, 337))
        medium_high = list(range(361, 367)) + list(range(391, 397)) + list(range(421, 427)) + list(range(451, 457)) + list(range(481, 487)) + list(range(511, 517))
        medium_low = list(range(541, 547)) + list(range(571, 577)) + list(range(601, 607)) + list(range(631, 637)) + list(range(661, 667)) + list(range(691, 697))

        _oracle.set_price(BTC, very_high, 2) # 1/0.5
        _oracle.set_price(BTC, very_low, 0.5)
        _oracle.set_price(BTC, medium_high, 4/3) # 1/0.75
        _oracle.set_price(BTC, medium_low, 0.75)


    def load_data(self, num=25):
        # all_files = glob.glob(str(self.path) + "/reslt_system*.csv")
        # agent_files = glob.glob(self.path + "/result_[0-9][0-9]*.csv") + glob.glob(self.path + "/result_[0-9]*.csv")
        # agent_files = list(set(agent_files))

        agent_li= []
        for i in range(num):
            file_name = 'result_{}_.csv'.format(i)
        # for file_name in agent_files:
            file_name = os.path.join(self.path, file_name)
            if not os.path.exists(file_name):
                continue
            df = pd.read_csv(file_name)
            agent_li.append(df)
        
        agent_df = pd.concat(agent_li, axis=0, ignore_index=True)
        agent_df['benefit'] = agent_df['asset_value'] - agent_df['invest']
        self.whole_agent_df = agent_df

        self.agent_df = self.whole_agent_df.drop_duplicates(subset=['day', 'agent_id'], keep='last')

        # system_files = glob.glob(self.path + "/result_system*.csv")
        system_li = []
        for i in range(num):
        # for file_name in system_files:
            file_name = 'result_system_{}_.csv'.format(i)
            file_name = os.path.join(self.path, file_name)
            if not os.path.exists(file_name):
                continue
            df = pd.read_csv(file_name)
            system_li.append(df)

        # all_files = glob.glob(self.path + "/reslt_system*.csv")
        # for file_name in all_files:
        #     df = pd.read_csv(file_name)
        #     system_li.append(df)

        system_df = pd.concat(system_li, axis=0, ignore_index=True)

        system_df['usdt_asset_price'] = self.actual_prices['USDT']
        system_df['btc_asset_price'] = self.actual_prices['BTC']
        system_df['nas_asset_price'] = self.actual_prices['NAS']

        system_df['dusd_diff'] = system_df['zusd_price'] - system_df['usdt_asset_price']
        system_df['dbtc_diff'] = system_df['zbtc_price'] - system_df['btc_asset_price']
        system_df['dnas_diff'] = system_df['znas_price'] - system_df['nas_asset_price']

        system_df['dusd_price'] = system_df['zusd_price']
        system_df['dbtc_price'] = system_df['zbtc_price']
        system_df['dnas_price'] = system_df['znas_price']

        system_df['dusd_volume'] = system_df['zusd_volume']
        system_df['dbtc_volume'] = system_df['zbtc_volume']
        system_df['dnas_volume'] = system_df['znas_volume']


    
        # for column in ['usdt_origin_price', 'btc_origin_price', 'nas_origin_price']:
        #     system_df[column]

        self.system_df = system_df

        self.to_csv_file()

    def to_csv_file(self):
        agent_file = 'all_agent.csv'
        file_name = os.path.join(self.path, agent_file)
        if not os.path.exists(file_name):
            self.whole_agent_df.to_csv(file_name, index=False)

        system_file =  'all_system.csv'
        file_name = os.path.join(self.path, system_file)
        if not os.path.exists(file_name):
            self.system_df.to_csv(file_name, index=False)

    def analyze_price(self, column = 'duet_price'):
        df = self.system_df
        duet_prices = df[column]
        mean = duet_prices.mean()
        n_number = len(duet_prices)
        df[column + '_var'] = duet_prices.apply(lambda  x: (x- mean)**2/n_number)
        return df

    def analyze_data(self, day_step=7, column='duet_price', with_votality=False):
        df = self.system_df
        duet_prices = df[column]
        if with_votality:
            prices = {
            'step': [],
            'mean': [],
            'median': [],
            'std': [],
            'var':[],
            'vota': []
            }
        else:
            prices = {
            'step': [],
            'mean': [],
            'median': [],
            'std': [],
            'var':[],
            }

        for i in range(2, 730, day_step):
            duet_price = duet_prices[i: i+ day_step]
            mean = duet_price.mean()
            median = duet_price.median()
            std = duet_price.std()
            # var = duet_price.apply(lambda x: abs(x/mean - 1)).sum()/ (duet_price.__len__() - 1)
            var = duet_price.var()

            if with_votality:
                vota = _votality.s_2(duet_price, day_step) * 100
                prices['vota'].append(vota)

            prices['step'].append(i)
            prices['mean'].append(mean)
            prices['median'].append(median)
            prices['std'].append(std)
            prices['var'].append(var)
        return pd.DataFrame(data = prices)

    # def get_data(self, column='duet_price'):
    #     df = self.system_df
    #     duet_prices = df[column]
    #     prices = {
    #         'step' : [],
    #         'value': []
    #     }
    #     return 

    def analyze_agent(self, model = 'swap_model', desire='DuetHoldAndStake', day_step=7, column='benefit'):
        df = self.agent_df
        if not model == 'all':
            df = df[df['focus_model'] == model]

        if not desire == 'all':
            df = df[df['desire'] == desire]

        result = {
            'step': [],
            'mean': [],
            'median': [],
            'std': [],
            'var':[]
        }
        # mean_all = df[column].mean()
        for i in range(2, 730, day_step):
            df_i = df[df['day'].isin(range(i, i+day_step))]
            series_one = df_i[column]
            mean = series_one.mean()
            median = series_one.median()
            std = series_one.std()
            # var = series_one.var()
            # duet_price_rate = series_one.apply(lambda x: x/mean - 1)
            # var = duet_price_rate.var()
            var = series_one.apply(lambda x: abs(x/mean - 1)).sum()/ (series_one.__len__() - 1)
            # var_d = series_one.apply(lambda  x: (x - mean_all))
            result['step'].append(i)
            result['mean'].append(mean)
            result['median'].append(median)
            result['std'].append(std)
            result['var'].append(var)

        agent_df = {
            'benefit': [],
            'day': []
        }
        for i in range(0, 730):
            df_i = df[df['day'] == i]
            series_one = df_i[column]
            mean = series_one.mean()
            agent_df['benefit'].append(mean)
            agent_df['day'].append(i)

        return pd.DataFrame(data = result), pd.DataFrame(data=agent_df)

if __name__ == '__main__':
    analyze = Analyze()
    analyze.load_data()