#!/usr/bin/python
'''
Created on Oct 7, 2011

@author: smotko
'''

from traceback import format_exc
from datetime import datetime
from time import sleep

if __name__ == '__main__':
    from handler import Bot
    
    while True:
            
        try:
            
            # initialize
            mypybot = Bot()
             
            # and run
            mypybot.run('irc.freenode.org', 6667)
            
        except Exception as e:
            
            f = open('error_log', 'a')
            f.write(str(datetime.now()) + "\n")
            f.write(str(format_exc() + "\n\n"))
            f.close()
            sleep(1)
            