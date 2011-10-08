#!/usr/bin/python

import socket, asyncore, asynchat
from urllib import urlopen, urlencode
 
class Bot( asynchat.async_chat ):
    
    def __init__( self, nick, name, channel, debug = True):
        asynchat.async_chat.__init__( self )
        self.buffer = ''
        self.set_terminator( '\r\n' )
        self.nick = nick
        self.realname = name
        self.channel = channel
        self.ident = None
        self.debug = debug
        self.joined_channel = False
 
    def write( self, text ):
        if self.debug:
            print '>> %s' % text
        self.push( text + '\r\n' ) 
 
    def handle_connect( self ):
        self.write( 'NICK %s' % self.nick )
        self.write( 'USER %s iw 0 :%s' % ( self.ident, self.realname ))
 
    def collect_incoming_data( self, data ):
        self.buffer += data
 
    def found_terminator(self):
        line= self.buffer
        self.buffer = ''
        if self.debug:
            print '%s' % line
            
        # join desired channel:
        if line.find('End of /MOTD command.') > 0:
            self.write('JOIN %s' % self.channel)
            # I know I should be checking if the JOIN command actually worked...
            self.joined_channel = True
        
        # respond to pings:
        if self.joined_channel and line.startswith('PING'):
            self.write('PONG')
            
        # if it isn't a ping request LOG IT:
        else:
            params = urlencode({'raw': line})
            f = urlopen('http://192.168.1.102/irc:8080', params)
            if f.read() != 'OK':
                print "ERROR @ %s \n %s", line, f.read()
 
    def run(self, host, port):
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        asyncore.loop()
 

 
