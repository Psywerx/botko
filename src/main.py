#!/usr/bin/env python

import sys, time
from daemon import Daemon

class BotkoDaemon(Daemon):
    def run(self):
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
                
                f = open('error_log', 'a')
                f.write(str(datetime.now()) + "\n")
                f.write(str(format_exc() + "\n\n"))
                f.close()
                sleep(10)

if __name__ == "__main__":
    daemon = BotkoDaemon('/tmp/daemon-example.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
