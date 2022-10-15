# from aletheia.scenario_generator.sample import Sample
# from aletheia.scenario_generator.cdec import Cdec
# from aletheia.scenario_generator.experiment import Experiment
# from .scenario_generator.sample import Sample
from .sample import Sample
from .cdec import Cdec
from .experiment import Experiment

import os
import shutil
import json

class ParallelScenario:
    def __init__(self, popsize, ngen, sample: Sample, cdec: Cdec, result_path: str):
        self.popsize = popsize
        self.ngen = ngen
        # self.pop = sample.gen(popsize)
        self.sample = sample
        self.cdec = cdec
        self.result_path = result_path

    def init_scenario(self):
        if os.path.exists(self.result_path):
            if os.path.isfile(self.result_path):
                os.remove(self.result_path)
            elif os.isdir(self.result_path):
                shutil.rmtree(self.result_path)

    def gen_pop(self):
        pop = self.sample.gen(self.popsize)
        result = []
        for item in pop:
            code = item['code']
            config = self.cdec.decode(code)
            experiment = Experiment(**config)
            states = experiment.evaluate()
            result.append({
                'code': code,
                'states': states
            })
        self.pop = result

    def save_gen(self, gen):
        with open(self.result_path, 'a', encoding='utf-8') as f:
            datas = {
                'gen': gen,
                # 'pop': [data.]
                'pop': self.pop
            }
            datas = json.dumps(datas, ensure_ascii=False)
            f.write(datas + "\n")

    def p_main(self):
        print('statrt')
        for g in range(self.ngen):
            self.gen_pop()
            self.save_gen(g)