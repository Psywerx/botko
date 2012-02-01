#!/usr/bin/python
'''
Created on Oct 7, 2011

@author: smotko
'''

from traceback import format_exc
from datetime import datetime
from time import sleep
from settings import *

if __name__ == '__main__':
    from handler import Bot
    
    while True:
            
        try:

            # initialize
            botko = Bot()
             
            # and run
            botko.run(IRC_SERVER, IRC_PORT)
            
            
        except Exception as e:
            # ugly code to restart the bot on error
            
            f = open('error_log', 'a')
            f.write(str(datetime.now()) + "\n")
            f.write(str(format_exc() + "\n\n"))
            f.close()
            sleep(1)
            