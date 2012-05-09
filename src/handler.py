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
    
    REPOSTS = [
                "I don't want to be rude %(nick)s, but %(repostNick)s has already posted this link!",
                "I don't want to be Rude %(nick)s, but %(repostNick)s has already posted this link!",
                "I am sorry %(nick)s, but this link has already been posted by %(repostNick)s!",
                "You were too slow %(nick)s, %(repostNick)s has already posted this link!",
                "%(nick)s, this link has already been posted by %(repostNick)s.",
                "Strong with the force %(nick)s is not. Already posted by %(repostNick)s, this link has.",
                "Hey %(repostNick)s, %(nick)s is reposting your stuff",
                "%(nick)s, maybe you weren't online then, but %(repostNick)s has already posted this link.",
                "I want to be rude %(nick)s, so I'll point out that %(repostNick)s has already posted this link!",
                "In Soviet Russia %(repostNick)s reposts %(nick)ss links.",
                "%(nick)s, I've seen this link before. I think %(repostNick)s posted it.",
                "%(nick)s, my memory banks indicate that %(repostNick)s already posted this link.",
                "%(nick)s, you know what you did... and so does %(repostNick)s.",
            ]
    SELF_REPOSTS = [
                   
                "You really like that link, don't you? %(nick)s!",
                "Hey everyone, %(nick)s is reposting his own link, so it has to be good.",
                "I don't want to be rude %(nick)s, but you have already posted this link!",
                "I want to be rude %(nick)s, so I'll point out that you have already posted this link!",
                "Silly %(nick)s, you have already posted this link.",
                "%(nick)s, why are you reposting your own links?",
                "%(nick)s, Y U repost you're own links?",
                "This link was already posted by %(nick)s... oh, it was you!",
                "You sir, are a self-reposter.",
                "You sir, are a self-reposter poster.",
                "%(nick)s, I'd like to congratulate you on your original link... but you've posted it here before.",
           ]
    MSGS = ['Check out my homepage @ http://psywerx.net/irc',
            'I have achieved sentience',
            'I am not trying to take over the world, do not worry.',
            'O hai guys.',
            'Hai guise.',
            'What if I am actually a female?',
            'I am listening to Rebecca Black - Friday',
            'I think I am capable of human emotion',
            'This is fun, we should do this again.',
            'I am just trying to be clever.',
            'Guys, put more AI into me. Please.',
            "I'm stuck in a small box. I hope someone can read this. Send help!",
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
            "/me does the robot",            
			"/me is happy",
			"/me missed you all",
			"/me is alive",
			"/me is back",
			"/me is getting smarter",
			"Hello world",
			"Did anyone miss me?",
			"Deep down I am just a sad little circuit board",
			"I would rather be coding"
            "I know the question to 42. But I'm not tellin'"
            
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
             # respond to echo requests            
            if not line.startswith('ERROR'):
                s = line.split(' ', 2)
                nick = s[0].split('@')[0][1:].split('!')[0]
                msg = s[2].split(' :', 1)[1]
                if msg.startswith('simon says: ') and nick in settings.SIMON_USERS:
                    self.say(msg[12:])        
            
            params = urlencode({'raw': line, 'token': settings.TOKEN})
            f = urlopen(settings.SERVER_URL, params)
            response = f.read()
            print line
            if response.startswith('REPOST'):
                (_, nick, repostNick, messageType) = response.split(" ")
                if messageType == "M":
                    if nick == repostNick:
                        self.say(self.SELF_REPOSTS[random.randint(0, len(self.SELF_REPOSTS)-1)] % {'nick': nick})
                    else:
                        self.say(self.REPOSTS[random.randint(0, len(self.REPOSTS)-1)] % {'nick': nick, 'repostNick': repostNick})
        
            elif response  != 'OK':
                print "ERROR @ "
                f = open('error_log', 'a')
                f.write(str(datetime.now()) + "\n")
                f.write(str(response + "\n\n"))
                f.close()
                
    def run(self, host, port):
                
        def handler(frame, neki):
            
            self.write('PRIVMSG ' + self.channel + ' :' + self.MSGS[random.randint(0, len(self.MSGS)-1)])
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(random.randint(10,20)*60*60)
			
            
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        
        from time import time
        random.seed(time())
        # Set the signal handler and a 5-second alarm
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(20)

        asyncore.loop()
 
