
from time import time
from itertools import *
from Corpus import Corpus
from math import ceil

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


class Chatty(object):
    # how many recent messages to consider in stuff
    MSGS = 5

    def __init__(self):
        self.buffer = []
        self.corpus = Corpus()
        self.avg_len = range(self.MSGS)
        self.counter = 0

    def chat(self, line):
        if "PRIVMSG" not in line:
            return False, ""

        _, meta, message = line.split(':', 2)

        self.buffer.append(message)
        self.avg_len[self.counter%self.MSGS] = len(message.split(" "))

        if len(self.buffer) >= self.MSGS:
            self.corpus.add(" ".join(self.buffer))
            del self.buffer[:]

            print self.talk()
            print ""


        return False, ""

    def talk(self):
        self.corpus.reset()
        line = take(ceil(sum(self.avg_len)/self.MSGS),
                    self.corpus)

        return " ".join([" ".join(ngram) for ngram in line])
