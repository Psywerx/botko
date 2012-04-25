
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
    accel_damp = 5

    def __init__(self):
        self.buffer = []
        self.corpus = Corpus()
        self.avg_len = range(self.messages)
        self.counter = 0
        self.recent_timestamps = range(self.window_big)

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
        if self.counter < self.window_big:
            return False

        return random.random() < max(self.accel_rate(),
                                     self.velocity_rate())

    def velocity_rate(self):
        # the oldest timestamp is exactly opposite current in the ist
        oldest = self.timestamps(-self.window_big+1)
        oldest_10 = self.timestamps(-self.window_big+self.window_small)

        now = int(time())

        return float(now-oldest_10)/float(now-oldest)

    def accel_rate(self):
        w = self.accep_damp

        last_15 = self.timestamps(0, w*3)

        v = [self.avg_diff(last_15[s:e]) for s,e in
             zip(range(0, w*3+w, w),
                 range(w, w*3+w, w))]

        a1 = float(v[0]-v[1])
        a2 = float(v[1]-v[2])

        if a2 <= 0 or a1 <= 0:
            return 0.0001

        return a2/a1

    def avg_diff(self, l):
        return map(lambda a: abs(a[0]-a[1]), zip(l, l[1:]))


    def timestamps(self, start, length = None):
        cur = self.counter%self.window_big

        start = (cur+start)%self.window_big

        if length == None:
            return self.recent_timestamps[start]

        return [self.recent_timestamps[(start+i)%self.window_big] for i in range(length)]

    def mentioned(self, msg):
        return settings.BOT_NICK in msg
