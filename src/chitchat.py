
from time import time
from itertools import *
import random
import pprint

CORPUS = {}

# from http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/
def weighted_choice(weights):
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


def trigrams(text):
    text = text.split(" ")
    return [text[i:i+1] for i in xrange(len(text)-1) if len(text[i:i+1]) > 0]

def _hash(s):
    return hash(",".join(s))

def entry(ngram):
    # WARNING: side-effect is adding empty entries to CORPUS
    key = _hash(ngram)

    try:
        entry = CORPUS[key]
    except KeyError:
        entry = {'text': ngram,
                 'next': {}}
        CORPUS[key] = entry

    return entry

def index(ngram_pair):
    cur, next = ngram_pair
    key1 = _hash(cur)
    key2 = _hash(next)

    entry1 = entry(cur)
    entry2 = entry(next)

    # increase weight
    try:
        entry1['next'][key2] += 1
    except KeyError:
        entry1['next'][key2] = 1

    CORPUS[key1] = entry1

    return []

def talk(key, n):
    acc = []

    while len(acc) < n:
        acc.append(CORPUS[key]['text'])

        if len(CORPUS[key]['next']) == 0:
            break

        keys = []
        weights = []
        for k, w in CORPUS[key]['next'].items():
            keys.append(k)
            weights.append(w)

        key = keys[weighted_choice(weights)]

    return " ".join([" ".join(ngram) for ngram in acc])


def chitchat(line):
    if "PRIVMSG" not in line:
        return False, ""

    _, meta, message = line.split(':')
    map(index, pairwise(trigrams(message)))

    pprint.pprint(CORPUS)

    print talk(random.choice(CORPUS.keys()),
               5)
    print ""


    return False, ""
