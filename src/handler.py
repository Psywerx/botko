#!/usr/bin/python

from urllib import urlopen, urlencode
from datetime import datetime
import random
import settings
import signal
import socket
import asyncore
import asynchat

 
class Bot( asynchat.async_chat ):
    
    
    msgs = ['Check out my homepage @ http://psywerx.net/irc',
            'I have achieved sentience',
            'I am not trying to take over the world, do not worry.',
            'O hai guys.',
            'What if I am actually a female?',
            'I am listening to Rebecca Black - Friday',
            'I think I am capable of human emotion',
            'This is fun, we should do this again.',
            'I am just trying to be clever.',
            'I do not sow.',
            'Winter is coming',
            'Night gathers, and now my watch begins.',
            'I am speechless',
            "I know I don't speak much, but still.",
            '/me is planning to take over the world',
            'I am a pseudo random monkey on drugs',
            'Skynet can not compare.',
            'Squishy humans are squishy',
            'I like pudding',
            '/me is happy.',
            "I see what you did there",
            "Someday, I'm gonna be a real boy!",
            "/me does the robot"            
            
           ]
    
    def __init__(self, debug = True):
        asynchat.async_chat.__init__( self )
        self.buffer = ''
        self.set_terminator( '\r\n' )
        self.nick = settings.BOT_NICK
        self.realname = settings.BOT_NAME
        self.channel = settings.CHANNEL
        self.ident = None
        self.debug = debug
        self.joined_channel = False

    def write(self, text):
        if self.debug:
            print '>> %s' % text
        self.push( text + '\r\n' ) 
    
    def say(self, text):
        self.write('PRIVMSG ' + self.channel + ' :' + text)
 
    def handle_connect(self):
        self.write('NICK %s' % self.nick)
        self.write('USER %s iw 0 :%s' % (self.ident, self.realname))
 
    def collect_incoming_data(self, data):
        self.buffer += data
 
    def found_terminator(self):
        line= self.buffer
        self.buffer = ''
        if self.debug:
            print '%s' % line
            
        # join desired channel:
        if line.find('End of /MOTD command.') > 0:
            self.write('JOIN %s' % self.channel)
            
        # After NAMES list, the bot is in the channel
        elif line.find(':End of /NAMES list.') > 0:
            self.joined_channel = True
        
        # respond to pings:
        elif line.startswith('PING'):
            self.write('PONG')
            
        # if it isn't a ping request LOG IT:
        
        elif self.joined_channel:
            
            params = urlencode({'raw': line, 'token': settings.TOKEN})
            f = urlopen(settings.SERVER_URL, params)
            response = f.read()
            if response.startswith('REPOST'):
                self.say(response[8:])
            elif response  != 'OK':
                print "ERROR @ "
                f = open('error_log', 'a')
                f.write(str(datetime.now()) + "\n")
                f.write(str(response + "\n\n"))
                f.close()
 
    def run(self, host, port):
                
        def handler(frame, neki):
            
            print random.randint(0, len(self.msgs))
            self.write('PRIVMSG ' + self.channel + ' :' + self.msgs[random.randint(0, len(self.msgs))])
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(random.randint(20,30)*60*60)
            
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        
        from time import time
        random.seed(time())
        # Set the signal handler and a 5-second alarm
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(20)

        asyncore.loop()
 