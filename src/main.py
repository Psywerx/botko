'''
Created on Oct 7, 2011

@author: smotko
'''



if __name__ == '__main__':
    from handler import Bot
    
    # initialize
    mypybot = Bot( 'botko', 'botko')
     
    # and run
    mypybot.run( 'irc.freenode.org', 6667 )