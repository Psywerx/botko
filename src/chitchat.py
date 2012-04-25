
from time import time
from itertools import *
from Corpus import Corpus
from math import ceil
import random

import settings

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


class Chatty(object):
    # how many recent messages to consider in stuff
    MSGS = 5

    # used when deciding whether to speak
    CHATTINESS_LONG = 60
    CHATTINESS_SHORT = 10

    def __init__(self):
        self.buffer = []
        self.corpus = Corpus()
        self.avg_len = range(self.MSGS)
        self.counter = 0
        self.recent_timestamps = range(self.CHATTINESS_LONG)

    def chat(self, line):
        if "PRIVMSG" not in line:
            return False, ""

        _, meta, message = line.split(':', 2)

        self.buffer.append(message)
        self.avg_len[self.counter%self.MSGS] = len(message.split(" "))

        if len(self.buffer) >= self.MSGS:
            self.corpus.add(" ".join(self.buffer))
            del self.buffer[:]

        speak = self.should_speak() or self.mentioned(message)
        msg = self.talk() if speak else ""

        self.counter += 1

        return speak, msg

    def talk(self):
        if self.counter < self.MSGS:
            return "I'm just admiring the shape of your skull"

        self.corpus.rewind()
        line = take(ceil(sum(self.avg_len)/self.MSGS),
                    self.corpus)

        return " ".join([" ".join(ngram) for ngram in line])

    def should_speak(self):
        # talk more when heated debate is happening
        now = int(time())

        # current counter minus <60> is oldest timestamp
        i = (self.counter-self.CHATTINESS_LONG-1)%self.CHATTINESS_LONG
        oldest = self.recent_timestamps[i]
        # oldest timestamp plus <50> is oldest of last <10> timestamps
        oldest_10 = self.recent_timestamps[(i+self.CHATTINESS_LONG-self.CHATTINESS_SHORT)\
                                               %self.CHATTINESS_LONG]

        # add new timestamp
        self.recent_timestamps[i] = now

        # starting conditions
        if self.counter < self.CHATTINESS_LONG:
            return False

        # ratio between speed of last <10> messages and speed of last <60>
        # determines probability of speaking
        return random.random() > 1-float(now-oldest_10)/float(now-oldest)

    def mentioned(self, msg):
        return settings.BOT_NICK in msg
