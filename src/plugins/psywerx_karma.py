from base import PsywerxPlugin
import re
import json


class PsywerxKarma(PsywerxPlugin):

    # factorize users current karma

    def fact(self, tokens, channel):
        try:
            def pf(number):
                factors = []
                d = 2
                while number > 1:
                    while number % d == 0:
                        factors.append(d)
                        number = number / d
                    d += 1
                return factors

            if len(tokens) != 1:
                response = self.request(channel, 'irc/karma_nick_all', {})
                r = json.loads(response)
                r = sorted(r, key=lambda x: pf(x['karma']))
                for p in r:
                    karmas = pf(p['karma'])
                    if int(p['karma']) < 2:
                        continue
                    # insert sleep to prevent floods
                    self.bot.say(str(p['nick']) + " " + str(max(karmas)) +
                                 " (" + str(p['karma']) + "=" +
                                 "*".join(map(str, karmas)) + ")", channel)
                self.bot.say(str("** CONGRATS " + p['nick'] + " **"), channel)

        except Exception:
            self.bot.log_error('Could not get upboats.')

    def _karma(self, tokens, channel):
        if len(tokens) != 1:
            response = self.request(channel, 'irc/karma_nick', {})
            if not response:
                msg = "Sorry, could not get karmas."
                self.bot.say(msg, channel)
                return
            s = ""
            for p in json.loads(response):
                s += str(p['nick']) + " (" + str(p['karma']) + "), "
            self.bot.say(s[:-2], channel)
        else:
            users = self.bot.known_users[channel]
            nick = tokens[0] if tokens[0] not in users else users[tokens[0]]
            params = {'nick': nick}
            response = self.request(channel, 'irc/karma_nick', params)
            if not response:
                msg = "Sorry, could not get karma for " + nick + "."
                self.bot.say(msg, channel)
                return
            nick = tokens[0] if tokens[0] not in users else users[tokens[0]]
            self.bot.say(nick + " has " + response + " karma.", channel)

    def handle_message(self, channel, nick, msg, line=None):
        msg_lower = msg.lower()
        self.handle_tokens(channel, msg,
                           ('karma', 'karmas', 'leaderboard',
                            'upboats', 'upvotes', 'stats',), self._karma)

        # count karma upvote
        if '++' not in msg_lower:
            return

        for user in re.split('[.,!?]* ', msg):
            users = self.bot.known_users[channel]
            name = user.replace('+', '')
            name_lower = name.lower()
            if (user.endswith('++') or user.startswith('++')) \
                    and name_lower in users:
                if name_lower == nick.lower():
                    self.bot.say("Nice try " + nick +
                                 ", but you can't give karma to yourself!",
                                 channel)
                    return
                else:
                    self.request(channel, 'irc/karma',
                                 {'nick': users[name_lower]})
