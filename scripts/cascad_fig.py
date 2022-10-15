from enum import unique
import sys
import os

from cascad.settings import BASE_DIR
sys.path.append('..')
sys.path.append('.')
import unittest
from cascad.models.datamodel import GeneResultModel
import csv


def gen_data(pk= "633418de618a90cec943bfe9"):
    resultModel = GeneResultModel.objects(pk= pk)
    result_data = list(resultModel)[0].result
    return result_data

    
def save_csv(result_data, _type='last_detail'):
    for index,datas in enumerate(result_data):
        file_path = os.path.join(BASE_DIR, 'resources', 'results', 'exp2_' + _type + str(index) + ".csv")
        csv_file = open(file_path, 'w', newline='')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['day', 'ZUSD', 'USD', 'USDT', 'USD', 'DUET', 'ADUET', 'ZBTC', 'BTC', 'ZNAS', 'NAS'])
        csv_writer.writerows(datas)

    csv_file.close()

if __name__ == '__main__':
    # result_data = gen_data()
    # save_csv(result_data)

    # result_data2 = gen_data("6339bf20369b744fbc093f35")
    # save_csv(result_data2, 'init0_detail')

    # result_data2 = gen_data("6339bf167a6549d183b7775f")
    # save_csv(result_data2, 'init1_detail')

    # result_data2 = gen_data("6339bf131f5adb3d06f8fcdb")
    # save_csv(result_data2, 'init2_detail')

    result_data2 = gen_data("633a81b205ec0d15591c90bd")
    save_csv(result_data2, 'init_detail2')
