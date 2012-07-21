#!/usr/bin/python

from datetime import datetime
import random
import signal
import socket
import asyncore
import asynchat

import settings
import response
import logic

 
class Bot(asynchat.async_chat):
    
    def __init__(self, debug=True):
        asynchat.async_chat.__init__(self)
        self.buffer = ''
        self.set_terminator('\r\n')
        self.nick = settings.BOT_NICK
        self.realname = settings.BOT_NAME
        self.channel = settings.CHANNEL
        self.ident = 'botko'
        self.debug = debug
        self.logic = logic.BotLogic(self)
        self.ac_in_buffer_size = self.ac_out_buffer_size = 8192   # 2*default

    def write(self, text):
        if self.debug: print '>> %s' % text
        self.push(text + '\r\n') 
    
    def say(self, text):
        self.write('PRIVMSG %s :%s' % (self.channel, text))
 
    def handle_connect(self):
        self.write('NICK %s' % self.nick)
        self.write('USER %s iw 0 :%s' % (self.ident, self.realname))
 
    def collect_incoming_data(self, data):
        self.buffer += data
 
    def log_error(self, error):
        f = open('error.log', 'a')
        f.write(str(datetime.now()) + '\n')
        f.write(str(error) + '\n\n')
        f.close()
        if self.debug: print error
    
    def found_terminator(self):
        line = self.buffer
        self.buffer = ''
        if self.debug: print line
        self.logic.new_input(line)
    
    def run(self, host, port):
        def handler(frame, neki):
            self.write('PRIVMSG ' + self.channel + ' :' + response.MSGS[random.randint(0, len(response.MSGS) - 1)])
            
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        
        random.seed()
        # set the signal handler for shouting random messages
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(20)

        asyncore.loop()

