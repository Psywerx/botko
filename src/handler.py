#!/usr/bin/python

import socket, asyncore, asynchat
 
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
        if line.find('End of /MOTD command.') > 0:
            self.write('JOIN %s' % self.channel)
        if line.startswith('PING'):
            self.write('PONG')
 
    def run(self, host, port):
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        asyncore.loop()
 

 
