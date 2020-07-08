from random import randrange, random, choice
import pandas as pd
from collections import namedtuple

Data = namedtuple("Data", ["value", "label"])
fields = ("left_value", "right_value", "pair_type", "is_match")
DataPair = namedtuple("DataPair", fields, defaults=(None,) * len(fields),)


class Generator(object):
    def __init__(self, data_funcs):
        self.data_funcs = data_funcs
        self.total = len(self.data_funcs)
        self.labels = [f.__name__ for f in data_funcs]
        self.data_funcs_dict = {i: f for i, f in enumerate(self.data_funcs)}

    def random_data(self, exclude=[]):
        func_list = [f for f in self.data_funcs if f.__name__ not in exclude]
        total = len(func_list)
        ind = randrange(0, total)
        f = func_list[ind]
        value = str(f())
        label = self.labels.index(f.__name__)
        return Data(value=value, label=label)

    def random_data_gen(self, cnt):
        for _ in range(cnt):
            yield self.random_data()

    def random_true(self):
        left = self.random_data()
        right = self.random_data([left.label])
        pair_type = f"{self.labels[left.label]}-{self.labels[right.label]}"
        return DataPair(
            left_value=left.value,
            right_value=right.value,
            pair_type=pair_type,
            is_match=True,
        )

    def random_false(self):
        left = self.random_data()
        right = self.random_data([left.label])
        pair_type = f"{self.labels[left.label]}-{self.labels[right.label]}"
        return DataPair(
            left_value=left.value,
            right_value=right.value,
            pair_type=pair_type,
            is_match=False,
        )

    def random_pair_gen(self, cnt, is_match=None, include_reverse=False):
        for _ in range(cnt):
            choose = choose = random() < 0.5 if is_match is None else is_match
            r = self.random_true() if choose else self.random_false()
            yield r
            if include_reverse:
                pair_type = "-".join(reversed(r.pair_type.split("-")))
                yield DataPair(
                    left_value=r.right_value,
                    right_value=r.left_value,
                    pair_type=pair_type,
                    is_match=r.is_match,
                )


class GenerateFromPairs(Generator):
    def __init__(self, data_pairs):
        self.data_pairs = data_pairs

    def random_data(self):
        return choice(choice(self.data_pairs))

    def random_true(self):
        chosen = choice(self.data_pairs)
        return DataPair(left_value=chosen[0], right_value=chosen[1], is_match=True)

    def random_false(self):
        left, right = ("", ""), ("", "")
        while left == right:
            left = choice(self.data_pairs)
            right = choice(self.data_pairs)
        return DataPair(left=left[0], right=right[1], is_match=False)

