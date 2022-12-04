"""
A statistics counter class used to make tracking mins, maxes, and averages easier
"""


class StatisticsCounter:
    def __init__(self):
        self.count = 0
        self.total_val = 0
        self.values = []
        self.min = 10000000
        self.max = -10000000

    def add_sample(self, sample):
        self.count += 1
        self.values.append(sample)
        self.total_val += sample
        if sample < self.min:
            self.min = sample
        if sample > self.max:
            self.max = sample

    def average(self):
        return self.total_val / self.count

    def __str__(self):
        return "avg: %1.2f   min: %1.2f   max: %1.2f   count: %5d" % (self.average(), self.min, self.max, self.count)