from itertools import *
import random
import UserDict

def pairwise(iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = tee(iterable)
        next(b, None)
        return izip(a, b)

def ngrams(text, l):
    text = text.split(" ")
    return [text[i:i+l] for i in xrange(len(text)-l) if len(text[i:i+l]) > 0]

class Corpus(UserDict.IterableUserDict):
    ngram_len = 1
    decay = 0.1

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
                     'weight': 1,
                     'next': {}}
            self.data[key] = entry

        return entry

    def __setitem__(self, ngram, value):
        key = self.__hash(ngram)
        self.data[key] = value

    # adapted from
    # http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/
    def __weighted_choice(self, items):
        rnd = random.random() * sum([w for w, k in items])
        for i, item in enumerate(items):
            rnd -= item[0]
            if rnd < 0:
                return item[1]

    def __next(self, ngram):
        item = self.__getitem__(ngram)

        if len(item['next']) == 0:
            raise StopIteration

        return self.data[self.__weighted_choice(zip(item['next'].values(),
                                                    item['next'].keys()))
                         ]['text']

    def next(self):
        if not hasattr(self, 'current_ngram'):
            self.rewind()

        self.current_ngram = self.__next(self.current_ngram)
        return self.current_ngram

    def add_pair(self, current, next):
        key1 = self.__hash(current)
        key2 = self.__hash(next)

        entry1 = self.__getitem__(current)
        entry2 = self.__getitem__(next) # for the side-effect

        # weaken old connections and drop bad ones
        self.data[key1]['next'] = dict([(k, w-self.decay)
                                        for k, w in self.data[key1]['next'].items()
                                        if w > 0])

        # increase weight
        try:
            self.data[key1]['next'][key2] += 1
        except KeyError:
            self.data[key1]['next'][key2] = 1

        self.data[key1]['weight'] += 1

    def add(self, text):
        # decrease main weights and drop useless entries
        for k in self.data.keys():
            self.data[k]['weight'] -= self.decay
            if self.data[k]['weight'] < 0:
                del self.data[k]

        [self.add_pair(cur, next) for cur, next in pairwise(ngrams(text,
                                                                   self.ngram_len))]

    def rewind(self):
        # make a weighed random pick where to start

        self.current_ngram = self.data[
            self.__weighted_choice(zip([e['weight'] for e in self.data.values()],
                                       self.data.keys()))
            ]['text']
