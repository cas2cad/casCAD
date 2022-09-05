# from aletheia.scenario_generator.timeline import TimeLine
from cascad.aritificial_world.timeline import TimeLine
import os
# from aletheia.settings import BASE_DIR
from cascad.settings import  BASE_DIR
# from aletheia.utils.constant import *
from .constant import *
import csv


base_path = os.path.join(BASE_DIR, 'resources')


class Oracle(object):
    def __init__(self, timeline: TimeLine):
        self.prices = {
            'USDT': [1] * 730,
            'BTC': [ float(x) for x in self.load_data_from_csv(BTC)],
            'NAS': [ float(x) for x in self.load_data_from_csv(NAS)],
            'DUET': [float(x[1:]) for x in self.load_data_from_csv(DUET)]
        }
        self.timeline = timeline
        self.corresponding_token = {
            ZBTC : BTC,
            ZNAS : NAS,
            ZUSD: USDT
        }

    def load_data_from_csv(self, token):
        # get recently two years data
        result = []

        if token == DUET: # use rei his data as duet price
            token = REI
        btc = token.lower()
        btc = "{}.csv".format(btc)
        file_path = os.path.join(base_path, btc)
        with open(file_path, newline='') as csvfile:
            # file_reader = csv.reader(csvfile)
            file_reader = csv.DictReader(csvfile)
            for row in file_reader:
                result.append(row['Close'])

        result = list(reversed(result[:730]))
        # result = result[:730]
        if len(result) <= 730:
            left_length = 730 - len(result)
            result = result + list(result[:left_length])
        return result


    def get_price(self, token, high=True):
        # price is roughlhy here in one day
        # next step to verify the oracle function of it
        if not isinstance(token, str):
            token = token.name

        tick = self.timeline.tick
        if token not in self.prices.keys():
            token = self.corresponding_token[token]
        price_list = self.prices[token]
        if tick <= len(price_list) - 1:
            result = price_list[tick]
        else:
            result = price_list[-1]

        if isinstance(result, str) and result.startswith('$'):
            return float(result[1:])
        else:
            return float(result)

    def set_price(self, token, days, factor):

        for day in days:
            self.prices[token][day - 1]= self.prices[token][day - 1] * factor

        return True

