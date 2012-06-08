#!/usr/bin/python

if __name__ == '__main__':
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
            