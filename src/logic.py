from plugins.nsfw_image_detector import NSFWImageDetectorPlugin
from plugins.read_links import ReadLinks
from plugins.psywerx_history import PsywerxHistory
from plugins.psywerx_groups import PsywerxGroups
from plugins.psywerx_karma import PsywerxKarma
from plugins.uptime import Uptime
import settings
import re

class BotLogic(object):
    def __init__(self, bot):
        self.bot = bot  # reference back to asynchat handler
        self.joined_channel = False
        self.usertrim = re.compile('[!+@]')  # used to strip nicknames of any mode-dependent prefixes (@-op, +-voice, etc.)
        self.bot.known_users = {}  # dict of known users present in the channel

        self.plugins = [
            PsywerxHistory(bot=bot),
            PsywerxKarma(bot=bot),
            PsywerxGroups(bot=bot),
            NSFWImageDetectorPlugin(bot=bot),
            ReadLinks(bot=bot),
            Uptime(bot=bot),
        ]

    def get_action_code(self, line):
        if line.startswith('ERROR'):
            raise Exception('some IRC error')

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
        msg = sline[1][msg_start + 1:].strip() if msg_start > 0 else ''  # JOIN messages have no ': message'
        end = msg_start if msg_start > 0 else len(sline[1])
        channel = sline[1][msg_chan:end].strip()
        return nick, msg, channel

    def self_input(self, channel, msg, line):
        for plugin in self.plugins:
            try:
                plugin.handle_say(channel, msg, line)
            except:
                return self.bot.log_error('ERROR parsing self msg line: ' + line)

    def new_input(self, line):
        if line.startswith('PING'):
            return self.bot.write('PONG')  # ping-pong
        try:
            action_code = self.get_action_code(line)
        except:
            return self.bot.log_error('ERROR on IRC: ' + line)

        if action_code == 'END_MOTD':  # after server MOTD, join desired channel
            for c in self.bot.channel:
                self.bot.known_users[c] = {}
                self.bot.write('JOIN ' + c)
        elif action_code == "NOTICE" or action_code == "MODE":
            # Ignore these
            return

        elif action_code == 'NAMES_LIST':
            _, _, channel = self.parse_msg(line)
            for nick in self.usertrim.sub('', line.split(':')[2]).split(' '):
                self.bot.known_users[channel][nick.lower()] = nick

        elif action_code == 'END_NAMES':  # after NAMES list, the bot is in the channel
            self.joined_channel = True

        elif action_code == 'NICK_IN_USE': # TODO: Could loop, if all nicks are taken
            self.bot.next_nick()
            
        elif self.joined_channel:  # respond to some messages
            try:
                nick, msg, channel = self.parse_msg(line)
            except:
                return self.bot.log_error('ERROR parsing msg line: ' + line)

            if action_code == 'JOIN':
                self.bot.known_users[channel][nick.lower()] = nick

            elif action_code == 'QUIT':
                for c in self.bot.known_users.keys():
                    if nick.lower() in self.bot.known_users[c]:
                        del self.bot.known_users[c][nick.lower()]

            elif action_code == 'PART':
                del self.bot.known_users[channel][nick.lower()]

            elif action_code == 'NICK':
                for c in self.bot.known_users.keys():
                    if nick.lower() in self.bot.known_users[c]:
                        del self.bot.known_users[c][nick.lower()]
                        self.bot.known_users[c][msg.lower()] = msg

            # Run plugins
            for plugin in self.plugins:
                plugin.handle_message(channel, nick, msg, line)
