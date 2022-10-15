'''
gen samples randomly
'''


class Sample(object):

    def gen(self, pop_num):
        # result = [{'Gene':'', 'Observe':''}]
        pop = []
        for i in range(pop_num):
            pop.append({
                'code': [0.1, 0.1, 0.1, 0.2, 0.3, 0.2]
            })
            pass
        pass
