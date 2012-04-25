
from time import time
from itertools import *

from Corpus import Corpus

CORPUS = Corpus()


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


def trigrams(text):
    text = text.split(" ")
    return [text[i:i+1] for i in xrange(len(text)-1) if len(text[i:i+1]) > 0]

def index(ngram_pair):
    cur, next = ngram_pair
    CORPUS.add(cur, next)

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def talk(n):
    acc = take(n, CORPUS)

    return " ".join([" ".join(ngram) for ngram in acc])


def chitchat(line):
    if "PRIVMSG" not in line:
        return False, ""

    _, meta, message = line.split(':')
    map(index, pairwise(trigrams(message)))

    print talk(5)
    print ""


    return False, ""
