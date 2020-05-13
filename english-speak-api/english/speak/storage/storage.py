from random import sample, seed


class Storage:
    def __init__(self, data):
        seed()
        self.data = data

    def get_all(self):
        return self.data

    def get_exact_part(self, count: int):
        if count < len(self.data):
            return sample(self.data, count)
        else:
            return self.data

    def get_percent_part(self, percent: int):
        return self.data
