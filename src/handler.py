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

    def __init__(self):
        asynchat.async_chat.__init__(self)
        self.known_users = {}
        self.buffer = ''
        self.set_terminator('\r\n')
        self.nick_num = 0
        self.nick = settings.NICKS[self.nick_num]
        self.logic = logic.BotLogic(self)
        self.ac_in_buffer_size = self.ac_out_buffer_size = 8192   # 2*default
        self.start_time = time()

    def print_debug(self, text):
        if settings.DEBUG:
            print(text)

    def write(self, text):
        self.print_debug('> %s' % text)
        self.push(text + '\r\n')

    def say(self, text, channel):
        if not text:
            return
        line = 'PRIVMSG %s :%s' % (channel, text)
        self.write(line)
        self.logic.self_input(channel, text, line)
        return line

    def set_nick(self):
        self.nick = settings.NICKS[self.nick_num]
        self.write('NICK %s' % self.nick)

    def next_nick(self):
        self.nick_num = (self.nick_num + 1) % len(settings.NICKS)
        self.set_nick()

    def handle_connect(self):
        self.set_nick()
        self.write('USER %s iw 0 :%s' %
                   (settings.IDENT, settings.REAL_NAME))

    def collect_incoming_data(self, data):
        self.buffer += data

    def log_error(self, text):
        with open("error.log", "a") as f:
            f.write(str(datetime.now()) + '\n')
            f.write('Error: ' + text + '\n')
            self.print_debug(text)

            from traceback import format_exception
            from sys import exc_info
            ex_type, ex_val, ex_tb = exc_info()
            ex_text = ''.join(format_exception(ex_type, ex_val, ex_tb, 10))
            f.write(ex_text + '\n')
            self.print_debug(ex_text)

    def found_terminator(self):
        line = self.buffer
        self.buffer = ''
        self.print_debug("< " + line)
        self.logic.new_input(line)

    def run(self):
        def handler(signal, frame):
            pass

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((settings.IRC_SERVER, settings.IRC_PORT))

        random.seed()
        # set the signal handler for shouting random messages
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(20)

        asyncore.loop()

    def part_user(self, channel, nick, msg):
        del self.known_users[channel][nick.lower()]

    def remove_user(self, channel, nick, msg):
        for channel in self.known_users:
            if nick.lower() in self.known_users[channel]:
                self.part_user(channel, nick, msg)

    def add_user(self, channel, nick, msg):
        self.known_users[channel][nick.lower()] = nick

    def change_user(self, channel, old_nick, new_nick):
        for channel in self.known_users:
            if old_nick.lower() in self.known_users[channel]:
                del self.known_users[channel][old_nick.lower()]
                self.known_users[channel][new_nick.lower()] = new_nick
