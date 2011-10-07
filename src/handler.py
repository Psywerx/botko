#!/usr/bin/env python

import socket, asyncore, asynchat, random
 
class Bot( asynchat.async_chat ):
    def __init__( self, nick, name, debug = True ):
        asynchat.async_chat.__init__( self )
        self.buffer = ''
        self.set_terminator( '\r\n' )
        self.nick = nick + str(random.random())[4:7]
        self.realname = name
        self.ident = None
        self.debug = debug
 
    def write( self, text ):
        if self.debug == 1:
            print '>> %s' % text
        self.push( text + '\r\n' )
 
 
    def handle_connect( self ):
        self.write( 'NICK %s' % self.nick )
        self.write( 'USER %s iw 0 :%s' % ( self.ident, self.realname ))
 
    def collect_incoming_data( self, data ):
        self.buffer += data

 
    def found_terminator(self ):
        line= self.buffer
        self.buffer = ''
        if self.debug == 1:
            print '> %s' % line
        if line.find('End of /MOTD command.') > 0:
            self.write('JOIN #smotko-testing')
            
        if line.find('PING') > -1:
            self.write('PONG')
        
 
    def run( self, host, port ):
        self.create_socket( socket.AF_INET, socket.SOCK_STREAM )
        self.connect( ( host, port ) )
        asyncore.loop()
 

 
