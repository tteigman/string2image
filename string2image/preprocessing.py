from collections import Counter
from itertools import chain, combinations, product
from random import shuffle
import numpy as np
import pandas as pd
from PIL import Image


class String2Image(object):
    def __init__(self, s, model, flatten=True, **kwargs):
        self.s = s
        self.kwargs = kwargs
        self.flatten = flatten
        vocab = list(model.wv.vocab.keys())
        a = [model.wv[c] for c in s if c in vocab]
        self.orig_array = np.column_stack(a).transpose()
        self.im_size = self.kwargs.pop("array_size", (100, 20))
        self._resize()

    def __sub__(self, s):
        return self.array - s.array

    def __repr__(self):
        shape = self.im_size
        return f"<String2Image '{self.s}' ({shape[0]}, {shape[1]})>"

    def _resize(self):
        im_size = self.im_size
        resample = self.kwargs.get("resample", Image.NEAREST)
        mode = self.kwargs.get("mode", "L")
        img = Image.fromarray(self.orig_array, mode=mode)
        img = img.resize(im_size, resample=resample)
        self.img = img
        self.array = np.asarray(img)
        if self.flatten:
            self.array = self.array.reshape(im_size[0] * im_size[1])


class Prepare(object):
    def __init__(self, data):
        """
        data - data argument should be dictionary with key labels and iterable example values.
        """

        self.data = data

    def create_records(self, model, **kwargs):
        dfs = [
            pd.DataFrame({"data": v, "cat": [k] * len(v)}) for k, v in self.data.items()
        ]
        data_df = pd.concat(dfs)
        target = data_df.groupby("cat")["data"].count().min()
        data_df = (
            data_df.groupby("cat")
            .apply(lambda x: x.sample(target))
            .reset_index(drop=True)
        )
        data_df["string_image"] = data_df["data"].apply(
            lambda x: String2Image(x, model, **kwargs)
        )
        return data_df

    def _split_word(self, word):
        split = [c for c in word if c in self.vocab]
        return split

    def create_vocab(self, thresh=0):
        all_chars = []

        for chars in map(list, chain(*chain(*self.data.values()))):
            all_chars += chars
        vocab_counter = Counter(all_chars)
        self.vocab = [l for l, freq in vocab_counter.most_common() if freq >= thresh]
        self.remove = [l for l, freq in vocab_counter.most_common() if freq < thresh]
        self.vocab_counter = vocab_counter

    def train_data(self):
        train_data = list(map(self._split_word, chain(*self.data.values())))
        shuffle(train_data)
        return train_data

