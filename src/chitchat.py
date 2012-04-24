
from time import time

# from http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/
def weighted_choice_sub(weights):
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i

def trigrams(text):
    text = text.split(" ")
    return [text[i:i+3] for i in xrange(len(text)-2)]

def chitchat(line):
    if "PRIVMSG" not in line:
        return False, ""

    _, meta, message = line.split(':')
    print trigrams(message)


    return False, ""
