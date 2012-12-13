#!/usr/bin/env python

import sys, time
from daemon import Daemon

def run_bot():
    import settings
    from handler import Bot
    
    while True:
        try:
            # initialize
            botko = Bot()
            # and run
            botko.run(settings.IRC_SERVER, settings.IRC_PORT)
            
        except Exception as e:
            # log the error
            from traceback import format_exc
            from datetime import datetime
            from time import sleep
            
            print "ERR " + str(format_exc())
            
            f = open('error_log', 'a')
            f.write(str(datetime.now()) + "\n")
            f.write(str(format_exc() + "\n\n"))
            f.close()
            sleep(10)

class BotkoDaemon(Daemon):
    def run(self):
        run_bot()

if __name__ == "__main__":
    daemon = BotkoDaemon('/tmp/botko.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'nodaemon' == sys.argv[1]:
            run_bot()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
