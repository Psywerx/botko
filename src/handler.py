#!/usr/bin/python

from datetime import datetime
from time import time
import random
import signal
import socket
import asyncore
import asynchat

import settings
import logic


class Bot(asynchat.async_chat):

    def __init__(self, debug=True):
        asynchat.async_chat.__init__(self)
        self.known_users = {}
        self.buffer = ''
        self.set_terminator('\r\n')
        self.nicks = settings.BOT_NICKS
        self.nick_num = 0
        self.nick = self.nicks[0]
        self.realname = settings.BOT_NAME
        self.channels = settings.CHANNELS
        self.ident = 'botko'
        self.debug = debug
        self.logic = logic.BotLogic(self)
        self.ac_in_buffer_size = self.ac_out_buffer_size = 8192   # 2*default
        self.uptime = time()

    def write(self, text):
        if self.debug:
            print '> {0!s}'.format(text)
        self.push(text + '\r\n')

    def say(self, text, channel):
        if text == '':
            return
        line = 'PRIVMSG {0!s} :{1!s}'.format(channel, text)
        self.write(line)
        self.logic.self_input(channel, text, line)
        return line

    def set_nick(self):
        self.nick = self.nicks[self.nick_num]
        self.write('NICK {0!s}'.format(self.nick))

    def next_nick(self):
        self.nick_num = (self.nick_num + 1) % len(self.nicks)
        self.set_nick()

    def handle_connect(self):
        self.set_nick()
        self.write('USER {0!s} iw 0 :{1!s}'.format(self.ident, self.realname))

    def collect_incoming_data(self, data):
        self.buffer += data

    def log_error(self, error):
        with open("error.log", "a") as f:
            f.write(str(datetime.now()) + '\n')
            f.write(str(error) + '\n\n')
        if self.debug:
            print error

    def found_terminator(self):
        line = self.buffer
        self.buffer = ''
        if self.debug:
            print "< " + line
        self.logic.new_input(line)

    def run(self, host, port):
        def handler(signal, frame):
            pass

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))

        random.seed()
        # set the signal handler for shouting random messages
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(20)

        asyncore.loop()

    def part_user(self, channel, nick, msg):
        del self.known_users[channel][nick.lower()]

    def remove_user(self, channel, nick, msg):
        for channel in self.known_users.keys():
            if nick.lower() in self.known_users[channel]:
                self.part_user(nick, channel, msg)

    def add_user(self, channel, nick, msg):
        self.known_users[channel][nick.lower()] = nick

    def change_user(self, channel, old_nick, new_nick):
        for channel in self.known_users.keys():
            if old_nick.lower() in self.known_users[channel]:
                del self.known_users[channel][old_nick.lower()]
                self.known_users[channel][new_nick.lower()] = new_nick
