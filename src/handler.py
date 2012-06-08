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
        self.ident = None
        self.debug = debug
        self.joined_channel = False
        self.logic = logic
        self.ac_in_buffer_size = self.ac_out_buffer_size = 8192   # 2*default

    def write(self, text):
        if self.debug:
            print '>> %s' % text
        self.push(text + '\r\n') 
    
    def say(self, text):
        self.write('PRIVMSG ' + self.channel + ' :' + text)
 
    def handle_connect(self):
        self.write('NICK %s' % self.nick)
        self.write('USER %s iw 0 :%s' % (self.ident, self.realname))
 
    def collect_incoming_data(self, data):
        self.buffer += data
 
    def log_error(self, error):
        f = open('error.log', 'a')
        f.write(str(datetime.now()) + '\n')
        f.write(str(error + "\n\n"))
        f.close()
    
    def found_terminator(self):
        line = self.buffer
        self.buffer = ''
        if self.debug:
            print '%s' % line
        self.logic.new_input(line, self)
    
    def run(self, host, port):
        def handler(frame, neki):
            self.write('PRIVMSG ' + self.channel + ' :' + response.MSGS[random.randint(0, len(response.MSGS) - 1)])
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(random.random() * 6 * 60 * 60)   # say something about every 6 hours
            
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        
        random.seed()
        # set the signal handler for shouting random messages
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(20)

        asyncore.loop()

