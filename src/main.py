#!/usr/bin/python
'''
Created on Oct 7, 2011

@author: smotko
'''

if __name__ == '__main__':
    from handler import Bot
    
    # initialize
    mypybot = Bot()
     
    # and run
    mypybot.run('irc.freenode.org', 6667)