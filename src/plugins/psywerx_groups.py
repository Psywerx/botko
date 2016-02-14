from base import PsywerxPlugin
import re
import json


class PsywerxGroups(PsywerxPlugin):

    def __init__(self, bot=None):
        super(PsywerxGroups, self).__init__(bot=bot)
        self.actions = {
            '@mygroup': self._basicAction('irc/mygroups'),
            '@group': self._basicAction('irc/groups'),
            '@leaveall': self._basicAction('irc/leaveAll'),
            '@leave': self._leaveAction,
            '@join': self._joinAction,
        }

    def _basicAction(self, url):
        def _req(channel, params, msg_lower):
            return self.request(channel, url, params)
        return _req

    def _joinAction(self, channel, params, msg_lower):
        def parse_join(splt):
            if len(splt) == 2:
                return splt[1].replace('@', ''), False
            elif len(splt) == 3:
                return splt[1].replace('@', ''), True
            else:
                return False
        g = parse_join(msg_lower.split(' '))
        if not g:
            return

        params['group'] = g[0]
        params['offline'] = g[1]
        return self.request(channel, 'irc/join', params)

    def _leaveAction(self, channel, params, msg_lower):
        splited = msg_lower.split(' ')
        if len(splited) == 2:
            group = splited[1].replace('@', '')
            params['group'] = group
            return self.request(channel, 'irc/leave', params)

    def _handleActions(self, channel, nick, msg, line=None):
        msg_lower = msg.lower()
        for a in self.actions.keys():
            if msg_lower.startswith(a):
                params = {'nick': nick}
                response = self.actions[a](channel, params, msg_lower)
                if response:
                    self.bot.say(response.replace('"', ''), channel)
                return True
        return False

    def _handleMentions(self, channel, nick, msg, line=None):
        msg_lower = msg.lower()
        mentions = set()
        offline_mentions = set()

        for group in re.findall(r'@(\w+\'?)', msg_lower):
            # if @group' ends with ', or empty msg, don't send to offline
            offline_mention = group[-1] != "'" and \
                re.match(r'(@\w+\'?[ \^]*)+$', msg_lower.strip()) is None

            if group[-1] == "'":
                group = group[:-1]

            if nick.lower() == '_haibot_':
                continue

            params = {'group': group}
            response = self.request(channel, 'irc/mention', params)
            if response:
                for n, _, o in json.loads(response):
                    if n.lower() == nick.lower():
                        continue
                    if n.lower() in self.bot.known_users[channel]:
                        mentions.add(n.encode('ascii', 'ignore'))
                    elif o and offline_mention:
                        offline_mentions.add(n.encode('ascii', 'ignore'))

        if mentions:
            self.bot.say("CC: " + ', '.join(mentions), channel)
        if offline_mentions:
            self.bot.say("@msg " + ','.join(offline_mentions)
                         + " " + msg, channel)

    def handle_message(self, channel, nick, msg, line=None):
        if not self._handleActions(channel, nick, msg, line):
            self._handleMentions(channel, nick, msg, line)
