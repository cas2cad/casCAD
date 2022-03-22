class TimeLine:
    def __init__(self):
        self.tick = 0

    def step(self):
        self.tick += 1

    def get_time(self):
        return self.tick
