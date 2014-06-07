from base import PsywerxPlugin
from response import REPOSTS, MULTIPLE_REPOST, \
  SELF_REPOSTS, MULTIPLE_SELF_REPOST, random_response

class PsywerxHistory(PsywerxPlugin):

    def handle_message(self, channel, nick, msg, line=None):
        r = self.request(channel, 'irc/add', {'raw': line})
        if not r:
            return
        if r.startswith('REPOST'):
            self._handle_repost(r, channel)
        elif r != 'OK':
            self.bot.log_error(r)

    def handle_say(self, channel, msg, line):
        msg = ":" + self.bot.nick + "!~" + self.bot.nick + "@6.6.6.6 " + line
        self.request(channel, 'irc/add', {'raw': msg})

    def _handle_repost(self, r, channel):
        _, nick, repostNick, messageType, num = r.split(' ')
        if messageType != 'M':
            return

        response = self._pick_response(nick == repostNick, int(num) > 1)
        self.bot.say(response % {
            'nick': nick,
            'repostNick': repostNick,
            'num': num
        }, channel)

    def _pick_response(self, is_self, is_multiple):
        f = [
                [REPOSTS, MULTIPLE_REPOST],
                [SELF_REPOSTS, MULTIPLE_SELF_REPOST]
        ]
        return random_response(f[is_self][is_multiple])
