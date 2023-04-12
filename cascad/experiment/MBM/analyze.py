# from aletheia.settings import BASE_DIR
from cascad.models.datamodel import GeneResultModel, GeneResultModelRound0, GeneResultModelRound2
from cascad.settings import BASE_DIR
# from aletheia.artificial_system.oracle import Oracle
# from aletheia.scenario_generator.timeline import TimeLine
from cascad.experiment.MBM.constant import BTC
from cascad.aritificial_world.timeline import TimeLine
from cascad.experiment.MBM.oracle import Oracle
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
    def __init__(self, _id, path_name="", price_change = True):
        # self.path = os.path.join(BASE_DIR, 'resources', 'duetdatas-c')
        self.path = os.path.join(BASE_DIR, 'resources', path_name)
        self.actual_prices = _oracle.prices
        self.price_change = price_change
        self._id = _id
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

    def create_multiline(self, columns=['SMAMT Holder', 'SAsset Holder', 'SAsset Bulliser', 'SAsset Bearisher', 'Short-Term Speculator'], x='iter'):
        df = self.system_df
        result = {
            x: [],
            'value': [],
            'color': []
        }

        df_group = df[['iter'] + columns].groupby(by='iter', as_index=False).mean()
        # df_merge = pd.merge(df_group, df, on=['iter',  'RL and MEL'], how='left')
        # df_group = df[['iter'] + columns].groupby(by='iter', as_index=False).first()
        for index, row in df_group.iterrows():
            for column in columns:
                result[x].append(row['iter'])
                result['value'].append(row[column])
                result['color'].append(column)
        return pd.DataFrame(data = result)


    def create_multiline_RL_GL(self, columns=['MEL', 'RL'], x='iter'):
        df = self.system_df
        df['RL and MEL'] = df['RL'] + df['MEL']
        df_group = df[['iter', 'RL', 'MEL', 'RL and MEL']].groupby(by='iter', as_index=False).mean()
        # df_merge = pd.merge(df_group, df, on=['iter',  'RL and MEL'], how='left')
        # df_merge['RL'] = df_merge['RL_x']
        # df_merge['MEL'] = df_merge['MEL_x']
        result = {
            x: [],
            'value': [],
            'color': []
        }

        for index, row in df_group.iterrows():
            # print(row['c1'], row['c2'])
            for column in columns:
                
                result[x].append(row['iter'])
                # result['value'].append(row[column] * row[price_column])
                result['value'].append(row[column])
                result['color'].append(column)
        return pd.DataFrame(data = result)
        # return df_merge[['iter', 'RL', 'MEL']]

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


    def get_code_iter(self, iter):
        iter_max = self.system_df['iter'].max()
        if iter > iter_max:
            iter = iter_max
        code_data_df = self.system_df[self.system_df['iter'] == iter]
        code_data_df = code_data_df[['SMAMT Holder', 'SAsset Holder', 'SAsset Bulliser', 'SAsset Bearisher', 'Short-Term Speculator', 'Init Tokens']]
        code_data_df['Init Tokens'] = code_data_df['Init Tokens'] * 250
        return code_data_df.round(2)


    def load_data(self, num=25, round=1):
        exp_data = []
        if round == 2:
            resultModel = GeneResultModelRound2
        elif round == 0:
            resultModel = GeneResultModelRound0
        else:
            resultModel = GeneResultModel

        if round ==0 or round == 2:
            for item in resultModel.objects.only('code', 'loss', 'iter'):
                row = [str(item.pk), item.iter] + item.code + item.loss
                exp_data.append(row)
        else:
            for item in resultModel.objects(experiment_id=self._id).only('code', 'loss', 'iter'):
                row = [str(item.pk), item.iter] + item.code + item.loss
                exp_data.append(row)
        
        columns = ['id', 'iter', 'scenorio', 'SMAMT Holder', 'SAsset Holder', 'SAsset Bulliser', 'SAsset Bearisher', 'Short-Term Speculator', 'Init Tokens', 'loss1', 'loss2', 'loss3', 'loss4', 'loss5']
        system_df = pd.DataFrame(exp_data, columns=columns)
        columns_to_normalize = ['SMAMT Holder', 'SAsset Holder', 'SAsset Bulliser', 'SAsset Bearisher',
                                'Short-Term Speculator']


        if round == 2:
            system_df['Short-Term Speculator'] = 0.2
            columns_to_normalize = ['SMAMT Holder', 'SAsset Holder', 'SAsset Bulliser', 'SAsset Bearisher']
            remaining_sum = 1 - system_df['Short-Term Speculator']
            system_df[columns_to_normalize] = system_df[columns_to_normalize].div(
                system_df[columns_to_normalize].sum(axis=1), axis=0).multiply(remaining_sum, axis=0)
        else:
            system_df[columns_to_normalize] = system_df[columns_to_normalize].div(system_df[columns_to_normalize].sum(axis=1), axis=0)
        system_df['MEL'] = system_df[['loss1', 'loss2', 'loss3', 'loss4', 'loss5']].mean(axis=1)
        system_df['RL'] = system_df[['loss1', 'loss2', 'loss3', 'loss4', 'loss5']].std(axis=1)

        # print(system_df)
        self.system_df = system_df

        # self.to_csv_file()

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
    analyze.load_data(round=2)
    result = analyze.create_multiline()
    analyze.get_code_iter(3)
    analyze.create_multiline()