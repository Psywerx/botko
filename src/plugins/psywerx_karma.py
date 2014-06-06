from plugins.base import PsywerxPlugin
import re, json

class PsywerxKarma(PsywerxPlugin):

    def _karma(self, tokens, channel):
        if len(tokens) != 1:
            r = json.loads(self.request(channel, 'irc/karma_nick', {}))
            s = ""
            for p in r:
                s += str(p['nick']) + " (" + str(p['karma']) + "), "
            self.bot.say(s[:-2], channel)
        else:
            users =  self.bot.known_users[channel]
            nick = tokens[0] if tokens[0] not in users else users[tokens[0]]
            params = {'nick': nick}
            response = self.request(channel, 'irc/karma_nick', params)
            if not response:
                return
            nick = tokens[0] if tokens[0] not in users else users[tokens[0]]
            self.bot.say(nick + " has " + response + " karma.", channel)

    def handle_message(self, channel, nick, msg, line=None):
        msg_lower = msg.lower()
        self.handle_tokens(channel, msg,
          ('karma', 'karmas', 'leaderboard', 'upboats', 'upvotes', 'stats',), self._karma)

        # count karma upvote
        if '++' not in msg_lower:
            return

        for user in re.split('[.,!?]* ', msg):
            users =  self.bot.known_users[channel]
            name = user.replace('+', '')
            name_lower = name.lower()
            if (user.endswith('++') or user.startswith('++')) \
                and name_lower in users:
                if name_lower == nick.lower():
                    self.bot.say("Nice try " + nick + \
                      ", but you can't give karma to yourself!", channel)
                    return
                else:
                    self.request(channel, 'irc/karma', {'nick': users[name_lower]})
