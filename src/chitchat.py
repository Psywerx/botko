
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
    messages = 5

    # used when deciding whether to speak
    window_big = 60
    window_small = 10

    def __init__(self):
        self.buffer = []
        self.corpus = Corpus()
        self.avg_len = range(self.messages)
        self.counter = 0
        self.recent_timestamps = range(self.CHATTINESS_LONG)

    def chat(self, line):
        if "PRIVMSG "+settings.CHANNEL not in line:
            return False, ""

        _, meta, message = line.split(':', 2)

        self.buffer.append(message)
        self.avg_len[self.counter%self.messages] = len(message.split(" "))

        if len(self.buffer) >= self.messages:
            self.corpus.add(" ".join(self.buffer))
            del self.buffer[:]

        speak = self.should_speak() or self.mentioned(message)
        msg = self.talk() if speak else ""

        # counter used for calculating various stuff
        self.counter += 1

        return speak, msg

    def talk(self):
        if self.counter < self.messages:
            return "I'm just admiring the shape of your skull"

        self.corpus.rewind()
        line = take(ceil(sum(self.avg_len)/self.messages),
                    self.corpus)

        return " ".join([" ".join(ngram) for ngram in line])

    def should_speak(self):
        # starting conditions, we don't have enough timestamps :(
        if self.counter < self.CHATTINESS_LONG:
            return False


        # talk more when heated debate is happening
        now = int(time())

        # current counter minus <60> is oldest timestamp
        i = (self.counter-self.CHATTINESS_LONG-1)%self.CHATTINESS_LONG
        oldest = self.recent_timestamps[i]
        # oldest timestamp plus <50> is oldest of last <10> timestamps
        oldest_10 = self.recent_timestamps[(i+self.CHATTINESS_LONG-self.CHATTINESS_SHORT)\
                                               %self.CHATTINESS_LONG]

        # calculate rate of acceleration change
        # TODO: code could be prettier
        last_15 = [self.recent_timestamps[(i+j)%self.CHATTINESS_LONG]
                   for j in range(i, i+15)]
        v1 = sum([abs(now-last_15[j]) for j in range(5)])/5.0
        v2 = sum([abs(now-last_15[j]) for j in range(5, 10)])/5.0
        v3 = sum([abs(now-last_15[j]) for j in range(10, 15)])/5.0
        a1 = v1-v2
        a2 = v3-v2
        try:
            accel = float(a2)/float(a1)
            if accel < 0:
                accel = 0.0001
        except ZeroDivisionError:
            accel = 0.0001

        # add new timestamp
        self.recent_timestamps[i] = now


        return random.random() < max(self.accel_rate(),
                                     self.velocity_rate())

    def velocity_rate(self):
        # the oldest timestamp is exactly opposite current in the ist
        oldest = self.timestamps(-self.window_big+1)
        oldest_10 = self.timestamps(-self.window_big+10)

        now = int(time())

        return float(now-oldest_10)/float(now-oldest)

    def timestamps(self, start, end = None):
        cur = self.counter%self.window_big

        start = (cur+start)%self.window_big

        if end == None:
            return self.recent_timestamps[start]

        end = (cur+end)%self.window_big
        return self.recent_timestamps[start:end]

    def mentioned(self, msg):
        return settings.BOT_NICK in msg
