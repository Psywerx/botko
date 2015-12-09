from base import BotPlugin
from time import time
from datetime import timedelta
from os import popen


class Uptime(BotPlugin):

    def _uptime(self, tokens, channel):
        server_uptime = popen("uptime").read()
        current_uptime = time() - self.bot.uptime
        t = str(timedelta(seconds=current_uptime)).split('.')[0]
        self.bot.say("My uptime: %s, server uptime: %s"
                     % (t, server_uptime.split(',')[0].split('up ')[1]),
                     channel)

    def handle_message(self, channel, nick, msg, line=None):
        self.handle_tokens(msg, ('uptime',), self._uptime, channel)
