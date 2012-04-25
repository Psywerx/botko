
from time import time
from itertools import *
from Corpus import Corpus

CORPUS = Corpus()


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
    CORPUS.add(message)

    print talk(5)
    print ""


    return False, ""
