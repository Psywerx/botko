
from time import time
from itertools import *
from Corpus import Corpus

CORPUS = Corpus()


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def talk(n):
    CORPUS.reset()
    acc = take(n, CORPUS)

    return " ".join([" ".join(ngram) for ngram in acc])

BUFFER = []

def chitchat(line):
    if "PRIVMSG" not in line:
        return False, ""

    _, meta, message = line.split(':', 2)
    BUFFER.append(message)

    if len(BUFFER) >= 5: # 5 felt like a good enough number of messages to treat as a unit
        CORPUS.add(" ".join(BUFFER))
        del BUFFER[:]

        print talk(5)
        print ""


    return False, ""
