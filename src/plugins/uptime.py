from base import BotPlugin
from time import time
from datetime import timedelta


class Uptime(BotPlugin):

    def _uptime(self, tokens, channel):
        try:
            with open("/proc/uptime", 'r') as f:
                server_uptime_seconds = float(f.readline().split()[0])
                server_uptime = str(timedelta(seconds=int(server_uptime_seconds)))
        except:
            server_uptime = "unknown"

        bot_uptime_seconds = time() - self.bot.uptime
        bot_uptime = str(timedelta(seconds=int(bot_uptime_seconds)))
        self.bot.say("My uptime: %s, server uptime: %s"
                     % (bot_uptime, server_uptime),
                     channel)

    def handle_message(self, channel, nick, msg, line=None):
        self.handle_tokens(channel, msg, ('uptime',), self._uptime)
