#!/usr/bin/python

from urllib import urlopen, urlencode
from datetime import datetime
import random
import settings
import signal
import socket
import asyncore
import asynchat

 
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
        f = open('error_log', 'a')
        f.write(str(datetime.now()) + "\n")
        f.write(str(error + "\n\n"))
        f.close()
    
    
    def found_terminator(self):
        line = self.buffer
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
            # respond to some messages     
            try:    
                # simon says:
                nick, msg = self.parse(line)
                if msg.lower().startswith('simon says: ') and nick in settings.SIMON_USERS:
                    self.say(msg[12:])   
                # fortune cookies
                if msg.lower().startswith('i want a cookie'):
                    f = urlopen(settings.COOKIEZ_URL)
                    response = ' '.join(f.read().split('\n'))
                    self.say(response)     
            except:
                self.log_error("ERROR parsing line: " + line)
                if self.debug:
                    print "ERROR parsing line: " + line 
            # log the message:    
            try:
                params = urlencode({'raw': line, 'token': settings.TOKEN})
                f = urlopen(settings.SERVER_URL, params)
                response = f.read()
                if response.startswith('REPOST'):
                    (_, nick, repostNick, messageType) = response.split(" ")
                    if messageType == "M":
                        if nick == repostNick:
                            self.say(self.SELF_REPOSTS[random.randint(0, len(self.SELF_REPOSTS) - 1)] % {'nick': nick})
                        else:
                            self.say(self.REPOSTS[random.randint(0, len(self.REPOSTS) - 1)] % {'nick': nick, 'repostNick': repostNick})
            
                elif response != 'OK':
                    self.log_error(response)
            except:
                self.log_error("ERROR Could not log line " + line)
                if self.debug:
                    print "ERROR Could not log line " + line
    def run(self, host, port):
                
        def handler(frame, neki):
            
            self.write('PRIVMSG ' + self.channel + ' :' + self.MSGS[random.randint(0, len(self.MSGS) - 1)])
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(random.randint(10, 20) * 60 * 60)
            
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        
        from time import time
        random.seed(time())
        # Set the signal handler and a 5-second alarm
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(20)

        asyncore.loop()
 
    def parse(self, line):
        if line.startswith('ERROR'): return
        s = line.split(' ', 2)
        nick = s[0].split('@')[0][1:].split('!')[0]
        msg = s[2].split(':', 1)[1]
        return nick, msg
