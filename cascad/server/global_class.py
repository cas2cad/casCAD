from cascad.utils.myfuncs import Singleton


class GlobalExperiments(metaclass=Singleton):
    def __init__(self):
        self.experiments = {}
    def add_experiment(self, unique_id, exp):
        self.experiments[unique_id] = exp
        return True
        
    def remove_experiment(self, unique_id):
        del self.experiments[unique_id]
        return True

    def get_experiment(self, unique_id):
        return self.experiments[unique_id]

