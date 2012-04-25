
from itertools import *
import random
import UserDict

class Corpus(UserDict.IterableUserDict):

    def __iter__(self):
        return self

    def __hash(self, s):
        return hash(",".join(s))

    def __getitem__(self, ngram):
        # side effect of creating empty values
        key = self.__hash(ngram)

        try:
            entry = self.data[key]
        except KeyError:
            entry = {'text': ngram,
                     'next': {}}
            self.data[key] = entry

        return entry

    def __setitem__(self, ngram, value):
        key = self.__hash(ngram)
        self.data[key] = value

    # from http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/
    def __weighted_choice(self, weights):
        rnd = random.random() * sum(weights)
        for i, w in enumerate(weights):
            rnd -= w
            if rnd < 0:
                return i

    def __next(self, ngram):

        keys = []
        weights = []
        item = self.__getitem__(ngram)

        if len(item['next']) == 0:
            raise StopIteration

        for k, w in item['next'].items():
            keys.append(k)
            weights.append(w)

        key = keys[self.__weighted_choice(weights)]

        return self.data[key]['text']

    def next(self):
        if not hasattr(self, 'current_ngram'):
            self.current_ngram = self.data[random.choice(self.keys())]['text']

        self.current_ngram = self.__next(self.current_ngram)
        return self.current_ngram

    def add(self, current, next):
        key1 = self.__hash(current)
        key2 = self.__hash(next)

        entry1 = self.__getitem__(current)
        entry2 = self.__getitem__(next) # for the side-effect

        # increase weight
        try:
            entry1['next'][key2] += 1
        except KeyError:
            entry1['next'][key2] = 1

        try:
            self.data[key1]['next'][key2] += 1
        except KeyError:
            self.data[key1]['next'][key2] = 1
