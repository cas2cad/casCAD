from pargov.pargov_main import  ParExperiment
from operator import  itemgetter
import random
# from aletheia.settings import BASE_DIR
from cascad.settings import  BASE_DIR
import numpy as np
import tqdm
import os
import csv

result_dir = os.path.join(BASE_DIR, 'resources', 'results')
CXPB, MUTPB, NGEN, popsize = 0.8, 0.4, 100, 100 

class Gene:
    def __init__(self, **data):
        self.__dict__.update(data)
        self.size = len(data['data'])

    def evaluate(self):
        _data = self.data
        result = []
        beta_a, beta_b = _data[0], _data[1]
        risk_coeff_up, risk_coeff_down = _data[2], _data[3]
        belief_weight_up, belief_weight_down = _data[4], _data[5]
        info_reliable_up, info_reliable_down = _data[6], _data[7]
        infor_agent_per= _data[8]
        info_gen_lam = _data[9]

        for i in range(10):
            parExperiment = ParExperiment(beta_a = beta_a, beta_b=beta_b, risk_coef_up=risk_coeff_up, risk_coef_down=risk_coeff_down, belief_weight_up=belief_weight_up, belief_reliable_down=belief_weight_down, belief_reliable_up=info_reliable_up, belief_weight_down=info_reliable_down, infor_agent_per=infor_agent_per, info_arrive_lam=info_gen_lam)

            while parExperiment.running:
                parExperiment.step()
            result.append(parExperiment.result[-1])
        
        loss1 = [x[0] for x in result]
        loss2 = [x[1] for x in result]
        loss3 = [x[2] for x in result]
        return 1 - sum(loss1)/ len(loss1), 1 - sum(loss2)/len(loss2), 1 - sum(loss3)/len(loss3)


class GA:
    def __init__(self, **parameter):
        self.popsize = parameter['popsize']
        self.bound = [[1, 10]] * 2 + [[0,1]]*7 + [[2, 10]]

        self.init_the_group()

    def init_the_group(self, experiment=0):
        pop = []
        for i in tqdm.tqdm(range(self.popsize)):
            beta_a, beta_b = np.random.randint(1, 10, 2)
            risk_coeff_up, risk_coeff_down, belief_weight_up, belief_weight_down, info_reliable_up, info_reliable_down, infor_agent_per = np.random.uniform(0, 1, size=7)
            if beta_a > beta_b:
                beta_a, beta_b  = beta_b, beta_a
            if risk_coeff_up < risk_coeff_down:
                risk_coeff_down,risk_coeff_up = risk_coeff_up, risk_coeff_down

            if belief_weight_up < belief_weight_down:
                belief_weight_up, belief_weight_down = belief_weight_down, belief_weight_up
            
            if info_reliable_up < info_reliable_down:
                info_reliable_down, info_reliable_up = info_reliable_up, info_reliable_down

            info_gen_lam = random.randint(2, 10)

            geneinfo = [beta_a, beta_b, risk_coeff_up, risk_coeff_down, belief_weight_up, belief_weight_down, info_reliable_up, info_reliable_down, infor_agent_per , info_gen_lam]

            gene = Gene(data=geneinfo)
            loss1, loss2, loss3 = gene.evaluate()

            pop.append({'Gene': gene, 'fitness': loss1 + loss2, 'loss1' :loss1, 'loss2': loss2, 'loss3': loss3})
            
        self.pop = pop
        self.bestindividual = self.selectBest(self.pop)


    def selectBest(self, pop):
        s_inds = sorted(pop, key=itemgetter('fitness'), reverse=True)
        return s_inds[0]

    def selection(self, individuals, k):
        s_inds = sorted(individuals, key=itemgetter('fitness'), reverse=True)
        sum_fits = sum(ind['fitness'] for ind in individuals)
        chosen = []
        for i in range(k):
            u = random.random() * sum_fits
            sum_ = 0
            for ind in s_inds:
                sum_ += ind['fitness']
                if sum_ >= u:
                    chosen.append(ind)
                    break
        chosen = sorted(chosen, key=itemgetter('fitness'), reverse=True)
        return chosen

    def crossoperate(self, offspring):
        dim = len(offspring[0]['Gene'].data)

        # Gene's data of first offspring chosen from the selected pop
        geninfo1 = offspring[0]['Gene'].data
        # Gene's data of second offspring chosen from the selected pop
        geninfo2 = offspring[1]['Gene'].data

        if dim == 1:
            pos1 = 1
            pos2 = 1
        else:
            # select a position in the range from 0 to dim-1,
            pos1 = random.randrange(1, dim)
            pos2 = random.randrange(1, dim)

        newoff1 = Gene(data=[])  # offspring1 produced by cross operation
        newoff2 = Gene(data=[])  # offspring2 produced by cross operation
        temp1 = []
        temp2 = []
        for i in range(dim):
            if min(pos1, pos2) <= i < max(pos1, pos2):
                temp2.append(geninfo2[i])
                temp1.append(geninfo1[i])
            else:
                temp2.append(geninfo1[i])
                temp1.append(geninfo2[i])
        newoff1.data = temp1
        newoff2.data = temp2

        return newoff1, newoff2

    def mutation(self, crossoff, bound):
        dim = len(crossoff.data)
        if dim == 1:
            pos = 0
        else:
            pos = random.randrange(0, dim)
        crossoff.data[pos] = random.randint(bound[pos][0], bound[pos][1])
        return crossoff

    def ga_main(self):
        popsize = self.popsize

        print("Start of evolution")
        result_path = os.path.join(BASE_DIR, 'resources', 'results', 'exp2.csv')
        csv_file = open(result_path, 'w', newline='')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['gen', 'avgloss', 'maxloss'])

        # Begin the evolution
        for g in tqdm.tqdm(range(NGEN)):

            print("############### Generation {} ###############".format(g))

            # Apply selection based on their converted fitness
            selectpop = self.selection(self.pop, popsize)

            nextoff = []
            while len(nextoff) != popsize:
                # Apply crossover and mutation on the offspring

                # Select two individuals
                offspring = [selectpop.pop() for _ in range(2)]

                if random.random() < CXPB:  # cross two individuals with probability CXPB
                    crossoff1, crossoff2 = self.crossoperate(offspring)
                    if random.random() < MUTPB:  # mutate an individual with probability MUTPB
                        muteoff1 = self.mutation(crossoff1, self.bound)
                        muteoff2 = self.mutation(crossoff2, self.bound)
                        # Evaluate the individuals
                        # fit_muteoff1, fit_mute_price1, fit_mute_vote1, addresses, vote_loss, address_loss = self.evaluate(
                            # muteoff1.data)
                        # Evaluate the individuals
                        # fit_muteoff2, fit_mute_price2, fit_mute_vote2, addresses, vote_loss, address_loss = self.evaluate(
                            # muteoff2.data)
                        loss1_1, loss1_2, loss1_3 = muteoff1.evaluate()
                        loss2_1, loss2_2, loss2_3 = muteoff2.evaluate()
                        nextoff.append(
                            {'Gene': muteoff1, 'fitness': loss1_1+ loss1_2, 'loss1' :loss1_1, 'loss2': loss1_2, 'loss3': loss1_3})
                        nextoff.append(
                            {'Gene': muteoff2, 'fitness': loss2_1+ loss2_2, 'loss1' :loss2_1, 'loss2': loss2_2, 'loss3': loss2_3})
                    else:
                        loss1_1, loss1_2, loss1_3 = crossoff1.evaluate()
                        loss2_1, loss2_2, loss2_3 = crossoff2.evaluate()
                        nextoff.append(
                            {'Gene': crossoff1, 'fitness': loss1_1+ loss1_2, 'loss1' :loss1_1, 'loss2': loss1_2, 'loss3': loss1_3})
                        nextoff.append(
                            {'Gene': crossoff2, 'fitness': loss2_1+ loss2_2, 'loss1' :loss2_1, 'loss2': loss2_2, 'loss3': loss2_3})

                else:
                    nextoff.extend(offspring)

            # The population is entirely replaced by the offspring
            self.pop = nextoff

            # Gather all the fitnesses in one list and print the stats
            fits = [ind['fitness'] for ind in self.pop]

            best_ind = self.selectBest(self.pop)

            if best_ind['fitness'] > self.bestindividual['fitness']:
                self.bestindividual = best_ind

            print("Best individual found is {}, {}".format(self.bestindividual['Gene'].data,
                                                           self.bestindividual['fitness']))
            print("  Max fitness of current pop: {}".format(max(fits)))
            average_fitness = sum(fits) / len(fits)
            csv_writer.writerow([g, average_fitness, max(fits)])

        print("------ End of (successful) evolution ------")
        # csv_writer.close()
        csv_writer.writerow(
            [g, average_fitness, self.bestindividual['fitness']])

        csv_file.close()

        self.save_last()

    def save_last(self):
        popsize = self.pop
        print("Start of evolution")
        result_path = os.path.join(BASE_DIR, 'resources', 'results', 'exp2.csv')
        csv_file = open(result_path, 'w', newline='')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['beta_a', 'beta_b', 'risk_coeff_up', 'risk_coeff_down', 'belief_weight_up', 'belief_weight_down', 'info_reliable_up', 'info_reliable_down', 'infor_agent_per', 'fitness', 'lam', 'loss1', 'loss2', 'loss3'])
        for gene in popsize:
            csv_writer.writerow(gene['Gene'].data + [gene['fitness'], gene['loss1'] , gene['loss2'], gene['loss3']])



class Exp1:
    def ex_main(self):
        result = []
        
        for i in tqdm.tqdm(np.arange(0, 1, 0.05)):
            loss1, loss2, loss3 = self.evaluate(i)
            result.append([1- loss1, 1- loss2, 1 - loss3, i])

        file_path = os.path.join(result_dir, 'exp1.csv')
        with open(file_path, 'w', encoding='utf8', newline='') as f:
            write = csv.writer(f)
            for line in result:
                write.writerow(line)


    def evaluate(self, per):
        result = []
        for i in range(100):
            parExperiment = ParExperiment(infor_agent_per=per)
            while parExperiment.running:
                parExperiment.step()
            result.append(parExperiment.result[-1])
        
        loss1 = [x[0] for x in result]
        loss2 = [x[1] for x in result]
        loss3 = [x[2] for x in result]
        return sum(loss1)/ len(loss1), sum(loss2)/len(loss2), sum(loss3)/len(loss3)

if __name__ == '__main__':
    # exp1 = Exp1()
    # exp1.ex_main()
    # CXPB,
    run = GA(popsize=100)
    run.ga_main()