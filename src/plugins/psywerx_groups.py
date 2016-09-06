from base import PsywerxPlugin
import settings
import re
import json


class PsywerxGroups(PsywerxPlugin):

    def __init__(self, bot=None):
        super(PsywerxGroups, self).__init__(bot=bot)
        self.actions = {
            '@mygroup': self._basic_action('irc/mygroups'),
            '@group': self._basic_action('irc/groups'),
            '@leaveall': self._basic_action('irc/leaveAll'),
            '@leave': self._leave_action,
            '@join': self._join_action,
        }

    def _basic_action(self, url):
        def _req(channel, params, msg_lower):
            return self.request(channel, url, params)
        return _req

    def _join_action(self, channel, params, msg_lower):
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

    def _leave_action(self, channel, params, msg_lower):
        splited = msg_lower.split(' ')
        if len(splited) == 2:
            group = splited[1].replace('@', '')
            params['group'] = group
            return self.request(channel, 'irc/leave', params)

    def _handle_actions(self, channel, nick, msg):
        msg_lower = msg.lower()
        for action in self.actions:
            if msg_lower.startswith(action):
                params = {'nick': nick}
                response = self.actions[action](channel, params, msg_lower)
                if response:
                    self.bot.say(response.replace('"', ''), channel)
                return True
        return False

    def _handle_mentions(self, channel, nick, msg):
        msg_lower = msg.lower()
        mentions = set()
        offline_mentions = set()

        for group in re.findall(r'@(\w+\'?)', msg_lower):
            # if @group' ends with ', or empty msg, don't send to offline
            offline_mention = group[-1] != "'" and \
                re.match(r'(@\w+\'?[ \^]*)+$', msg_lower.strip()) is None

            if group[-1] == "'":
                group = group[:-1]

            if re.match(settings.BOTS_REGEX, nick):
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
        if not self._handle_actions(channel, nick, msg):
            self._handle_mentions(channel, nick, msg)
