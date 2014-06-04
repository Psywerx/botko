from plugins.base import PsywerxPlugin
from settings import TOKEN, SERVER_URL

class PsywerxHistory(PsywerxPlugin):
    process_self = True

    def handle_message(self, channel, nick, msg, line=None):
        r = self.request(channel, 'irc/add', {'raw': line}, line)
        if not r:
            return
        if r.startswith('REPOST'):
            self.handle_repost(r, channel)
        elif r != 'OK':
            self.bot.log_error(r)

    # TODO: add a method to log bot responses

    def handle_repost(self, r, channel):
        _, nick, repostNick, messageType, num = r.split(' ')
        if messageType != 'M':
            return

        response = self.pick_response(nick == repostNick, int(num) > 1)
        line = self.bot.say(response % {
            'nick': nick,
            'repostNick': repostNick,
            'num': num
        }, channel)

        msg = ":" + self.bot.nick + "!~" + self.bot.nick + "@6.6.6.6 " + line
        self.request(channel, 'irc/add', {'raw': line}, line)

    def pick_response(self, is_self, is_multiple):
        from response import *
        f = [
                [REPOSTS, MULTIPLE_REPOST],
                [SELF_REPOSTS, MULTIPLE_SELF_REPOST]
        ]
        return random_response(f[is_self][is_multiple])
