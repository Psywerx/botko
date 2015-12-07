from plugins.uptime import Uptime
import re


class BotLogic(object):

    def __init__(self, bot):
        self.bot = bot  # reference back to asynchat handler
        self.joined_channel = False
        self.usertrim = re.compile('[!+@]')
        self.bot.known_users = {}  # dict of known users present in the channel
        self.init_actions()

        self.plugins = [
            Uptime(bot=bot),
        ]

    def _get_action_code(self, line):
        if line.startswith('ERROR'):
            raise Exception('Unknown IRC error in line: ' + line)
        if line.startswith('PING'):
            return 'PING'

        action = line.split(' ', 2)[1]
        if action == '376':
            return 'END_MOTD'
        if action == '353':
            return 'NAMES_LIST'
        if action == '366':
            return 'END_NAMES'
        if action == '433':
            return 'NICK_IN_USE'
        return action.upper()

    def parse_msg(self, line):
        sline = line.split(' ', 1)
        nick = line[1:sline[0].find('!')]
        msg_start = sline[1].find(':', 1)
        msg_chan = sline[1].find('#', 1)
        msg = sline[1][msg_start + 1:].strip() if msg_start > 0 else ''
        end = msg_start if msg_start > 0 else len(sline[1])
        channel = sline[1][msg_chan:end].strip()
        return nick, msg, channel

    def self_input(self, channel, msg, line):
        for plugin in self.plugins:
            try:
                plugin.handle_say(channel, msg, line)
            except:
                return self.bot.log_error('ERROR parsing self line: ' + line)

    def handle_end_motd(self, line):
        # after server MOTD, join desired channel
        for c in self.bot.channel:
            self.bot.known_users[c] = {}
            self.bot.write('JOIN ' + c)

    def handle_names_list(self, line):
        # after NAMES list, the bot is in the channel
        _, _, channel = self.parse_msg(line)
        for nick in self.usertrim.sub('', line.split(':')[2]).split(' '):
            self.bot.known_users[channel][nick.lower()] = nick

    def handle_end_names(self, line):
        self.joined_channel = True

    def handle_nick_in_use(self, line):
        # TODO: Could loop, if all nicks are taken
        self.bot.next_nick()

    def handle_channel_input(self, action_code, line):
        try:
            nick, msg, channel = self.parse_msg(line)
        except:
            return self.bot.log_error('ERROR parsing msg line: ' + line)

        action = self._channel_actions.get(action_code)
        if action is not None:
            action(channel, nick, msg)

        # Run plugins
        for plugin in self.plugins:
            plugin.handle_message(channel, nick, msg, line)

    def new_input(self, line):
        try:
            action_code = self._get_action_code(line)
        except:
            return self.bot.log_error('ERROR on IRC: ' + line)

        action = self._actions.get(action_code)

        if action is not None:
            return action(line)

        elif self.joined_channel:  # respond to some messages
            self.handle_channel_input(action_code, line)

    def init_actions(self):
        self._actions = {
            'PING': lambda line: self.bot.write('PONG'),  # ping-pong
            'END_MOTD': self.handle_end_motd,
            'NAMES_LIST': self.handle_names_list,
            "NOTICE": lambda line: None,
            "MODE": lambda line: None,
            'END_NAMES': self.handle_end_names,
            'NICK_IN_USE': self.handle_nick_in_use,
        }
        self._channel_actions = {
            'JOIN': self.bot.add_user,
            'QUIT': self.bot.remove_user,
            'PART': self.bot.part_user,
            'NICK': self.bot.change_user,
        }
