from random import randrange, random
import pandas as pd
from collections import namedtuple

Data = namedtuple("Data", ["label", "value"])
DataPair = namedtuple("DataPair", ["left", "right", "is_match"])


class Generator(object):
    def __init__(self, data_funcs):
        self.data_funcs = data_funcs
        self.total = len(self.data_funcs)
        self.data_funcs_dict = {f.__name__: f for f in self.data_funcs}

    def _random_data(self, exclude=[]):
        func_list = [f for f in self.data_funcs if f.__name__ not in exclude]
        total = len(func_list)
        ind = randrange(0, total)
        f = func_list[ind]
        data = str(f())
        return Data(label=f.__name__, value=data)

    def random_data_gen(self, cnt):
        for _ in range(cnt):
            yield self._random_data()

    def _random_true(self):
        left = self._random_data()
        right_func = self.data_funcs_dict[left.label]
        right = Data(label=right_func.__name__, value=right_func())
        return DataPair(left=left, right=right, is_match=True)

    def _random_false(self):
        left = self._random_data()
        right = self._random_data([left.label])
        return DataPair(left=left, right=right, is_match=False)

    def random_pair_gen(self, cnt, is_match=None, reverse=True):
        for _ in range(cnt):
            choose = choose = random() < 0.5 if is_match is None else is_match
            r = self._random_true() if choose else self._random_false()
            yield r
            if reverse:
                yield DataPair(left=r.right, right=r.left, is_match=r.is_match)

