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
            self.bot.log_error("Response not OK: " + r)

    def handle_say(self, channel, msg, line):
        msg = ":" + self.bot.nick + "!~" + self.bot.nick + "@6.6.6.6 " + line
        self.request(channel, 'irc/add', {'raw': msg})

    def _handle_repost(self, r, channel):
        _, nick, repost_nick, message_type, num = r.split(' ')
        if message_type != 'M':
            return

        response = self._pick_response(nick == repost_nick, int(num) > 1)
        self.bot.say(response % {
            'nick': nick,
            'repost_nick': repost_nick,
            'num': num,
        }, channel)

    @staticmethod
    def _pick_response(is_self, is_multiple):
        f = [
            [REPOSTS, MULTIPLE_REPOST],
            [SELF_REPOSTS, MULTIPLE_SELF_REPOST],
        ]
        return random_response(f[is_self][is_multiple])
