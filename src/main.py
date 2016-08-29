#!/usr/bin/env python

import sys
from daemon import Daemon


def run_bot():
    from handler import Bot

    while True:
        try:
            # initialize and run
            botko = Bot()
            botko.run()

        except Exception:
            # log the error
            from traceback import format_exc
            from datetime import datetime
            from time import sleep

            print("ERR " + str(format_exc()))

            f = open('error_log', 'a')
            f.write(str(datetime.now()) + "\n")
            f.write(str(format_exc() + "\n\n"))
            f.close()
            sleep(10)


def print_usage():
    print("usage: %s start|stop|restart|nodaemon" % sys.argv[0])


class BotkoDaemon(Daemon):

    def run(self):
        run_bot()

if __name__ == "__main__":
    daemon = BotkoDaemon('/tmp/botko.pid')  # nosec: predictable, but low risk
    if len(sys.argv) == 2:
        if sys.argv[1] == 'start':
            daemon.start()
        elif sys.argv[1] == 'stop':
            daemon.stop()
        elif sys.argv[1] == 'restart':
            daemon.restart()
        elif sys.argv[1] == 'nodaemon':
            run_bot()
        else:
            print_usage()
            sys.exit(2)
        sys.exit(0)
    else:
        print_usage()
        sys.exit(2)
