from random import sample, seed


class Storage:
    def __init__(self, data):
        seed()
        self.data = data

    def get_all(self):
        return self.data

    def get_exact_part(self, count: int):
        return sample(self.data, count)

    def get_percent_part(self, percent: int):
        return self.data
