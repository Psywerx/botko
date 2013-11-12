from urllib import urlencode
from urllib2 import urlopen, URLError
from time import time
from datetime import timedelta
from os import popen
from response import *
import re
import settings
import json

from plugins.nsfw_image_detector import NSFWImageDetectorPlugin


def static_var(varname, value):
    """
    Create a static var `varname` with initial `value` on a decorated
    function.
    """
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate


class BotLogic(object):
    def __init__(self, bot):
        self.bot = bot  # reference back to asynchat handler
        self.joined_channel = False
        self.trimmer = re.compile('[ ]+')  # used for replacing a series of spaces with a single one
        self.usertrim = re.compile('[!+@]')  # used to strip nicknames of any mode-dependent prefixes (@-op, +-voice, etc.)
        self.known_users = {}   # dict of known users present in the channel
        self.actions = {}   # actions dict, holding 'keyword':action_func, easily populated below for multiple keywords per action
                            # action_func accepts one argument, which is a list of tokens following the keyword
        karma = (self.karma, ('karma', 'leaderboard', 'upboats', 'upvotes', 'stats',))
        cookie = (self.cookie, ('cookie', 'fortune',))
        uptime = (self.uptime, ('uptime',))
        help = (self.help, ('help', 'commands', 'man', '???', 'usage',))

        #movies = (self.movie_night, ('movie', 'movie-night', 'movies', 'moviez', ))
        #notify = (self.notifications, ('notify', 'remind', 'tell', ))
        for action in (karma, cookie, uptime, help):  # movies, notify):
            for keyword in action[1]:
                self.actions[keyword] = action[0]

        # TODO: Proper plugin loading 'n stuff
        self.plugins = [NSFWImageDetectorPlugin(bot=self)]

    def log_line_and_notify_on_repost(self, line, noRepost=False, channel=""):
        try:
            params = urlencode({'raw': line, 'token': settings.TOKEN, 'channel': channel})
            r = urlopen(settings.SERVER_URL + 'irc/add', params).read()
            if not noRepost and r.startswith('REPOST'):
                _, nick, repostNick, messageType, num = r.split(' ')
                if messageType == 'M':
                    responses = SELF_REPOSTS if nick == repostNick else REPOSTS
                    if int(num) == 1:
                        self.bot.say(random_response(responses) % {'nick': nick, 'repostNick': repostNick}, channel)
                    elif int(num) > 1:
                        if nick == repostNick:
                            self.bot.say(random_response(MULTIPLE_SELF_REPOST) % {'nick': nick, 'repostNick': repostNick, 'num': num}, channel)
                        else:
                            self.bot.say(random_response(MULTIPLE_REPOST) % {'nick': nick, 'repostNick': repostNick, 'num': num}, channel)
            elif r != 'OK':
                self.bot.log_error(r)
        except URLError:
            self.bot.log_error('ERROR Could not log line: ' + line)

    def get_action_code(self, line):
        if line.startswith('ERROR'):
            raise Exception('some IRC error')
        # behold, IRC protocol documentation:
        # :card.freenode.net 376 kjhgfdsa :End of /MOTD command.
        # :card.freenode.net 353 kjhgfdsa = #ubuntu :cornfeed calexnk edlinde Jettis zenix
        # :card.freenode.net 366 kjhgfdsa #ubuntu :End of /NAMES list.
        # :MsAshley!~pjwaffle@75-172-10-58.tukw.qwest.net PRIVMSG #ubuntu :It opens an http-vnc port, however, according to nmap
        # :sh4d0wg0d!~root@187.101.162.128 JOIN #ubuntu
        # :Dreamer3!~Dreamer3@74-133-171-106.dhcp.insightbb.com QUIT :Quit: Leaving...
        action = line.split(' ', 2)[1]
        if action == '376':
            return 'END_MOTD'
        if action == '353':
            return 'NAMES_LIST'
        if action == '366':
            return 'END_NAMES'
        return action.upper()

    def parse_msg(self, line):
        sline = line.split(' ', 1)

        nick = line[1:sline[0].find('!')]
        msg_start = sline[1].find(':', 1)
        msg_chan = sline[1].find('#', 1)
        msg = sline[1][msg_start + 1:].strip() if msg_start > 0 else ''   # JOIN messages have no ': message'
        end = msg_start if msg_start > 0 else len(sline[1])
        channel = sline[1][msg_chan:end].strip()
        return nick, msg, channel

    def new_input(self, line):
        if line.startswith('PING'):
            return self.bot.write('PONG')  # ping-pong
        try:
            action_code = self.get_action_code(line)
        except:
            return self.bot.log_error('ERROR on IRC: ' + line)

        if action_code == 'END_MOTD':  # after server MOTD, join desired channel
            for c in self.bot.channel:
                self.known_users[c] = {}
                self.bot.write('JOIN ' + c)
        elif action_code == 'NAMES_LIST':
            _, _, channel = self.parse_msg(line)
            for nick in self.usertrim.sub('', line.split(':')[2]).split(' '):
                self.known_users[channel][nick.lower()] = nick
            # object comprehension does not work in python 2.6.x
            # self.known_users = {nick.lower():nick for nick in self.usertrim.sub('', line.split(':')[2]).split(' ')}

        elif action_code == 'END_NAMES':  # after NAMES list, the bot is in the channel
            self.joined_channel = True

        elif self.joined_channel:  # respond to some messages
            try:
                nick, msg, channel = self.parse_msg(line)
            except:
                return self.bot.log_error('ERROR parsing msg line: ' + line)

            if action_code == 'JOIN':
                self.known_users[channel][nick.lower()] = nick  # make newly-joined user known

            elif action_code == 'QUIT':
                for c in self.known_users.keys():
                    if nick.lower() in self.known_users[c]:
                        del self.known_users[c][nick.lower()]  # forget user when he quits/parts?

            elif action_code == 'PART':
                del self.known_users[channel][nick.lower()]

            elif action_code == 'NICK':
                for c in self.known_users.keys():
                    if nick.lower() in self.known_users[c]:
                        del self.known_users[c][nick.lower()]  # forget user when he quits/parts?
                        self.known_users[c][msg.lower()] = msg

            self.log_line_and_notify_on_repost(line, False, channel)

            msg_lower = msg.lower()

            # TODO: Proper plugin loading n' stuff
            # Run plugins
            for plugin in self.plugins:
                plugin.handle_message(channel=channel, nick=nick, msg=msg)

            # Simon says action
            if msg_lower.startswith('simon says: ') and nick in settings.SIMON_USERS:
                self.bot.say(msg[12:], channel)
            elif msg_lower.startswith('@mygroup'):
                params = urlencode({'token': settings.TOKEN, 'channel': channel, 'nick': nick})
                response = urlopen(settings.SERVER_URL + 'irc/mygroups', params).read()
                self.bot.say(response.replace('"', ''), channel)
            elif msg_lower.startswith('@group'):
                params = urlencode({'token': settings.TOKEN, 'channel': channel})
                response = urlopen(settings.SERVER_URL + 'irc/groups', params).read()
                self.bot.say(response.replace('"', ''), channel)
            elif msg_lower.startswith('@join'):

                def parse_join(splt):

                    if len(splt) == 2:
                        return splt[1].replace('@', ''), False
                    elif len(splt) == 3:
                        return splt[1].replace('@', ''), True
                    else:
                        return False
                g = parse_join(msg_lower.split(' '))
                if g:
                    params = urlencode({'token': settings.TOKEN, 'channel': channel, 'nick': nick, 'group': g[0], 'offline': g[1]})
                    response = urlopen(settings.SERVER_URL + 'irc/join', params).read()
                    self.bot.say(response.replace('"', ''), channel)
            elif msg_lower.startswith('@leaveall'):
                params = urlencode({'token': settings.TOKEN, 'channel': channel, 'nick': nick})
                response = urlopen(settings.SERVER_URL + 'irc/leaveAll', params).read()
                self.bot.say(response.replace('"', ''), channel)
            elif msg_lower.startswith('@leave'):
                splited = msg_lower.split(' ')
                if(len(splited) == 2):
                    group = splited[1].replace('@', '')
                    params = urlencode({'token': settings.TOKEN, 'channel': channel, 'nick': nick, 'group': group})
                    response = urlopen(settings.SERVER_URL + 'irc/leave', params).read()
                    self.bot.say(response.replace('"', ''), channel)
            else:
                mentions = set()
                offline_mentions = set()
                for group in re.findall(r'@(\w+)', msg_lower):
                    if group in ["join", "leave", "leaveAll"] or nick.lower() == '_haibot_':
                        continue

                    params = urlencode({'token': settings.TOKEN, 'channel': channel, 'group': group})
                    response = json.loads(urlopen(settings.SERVER_URL + 'irc/mention', params).read())
                    for n, c, o in response:
                        if n.lower() == nick.lower():
                            continue
                        if n.lower() in self.known_users[channel]:
                            mentions.add(n.encode('ascii', 'ignore'))
                        elif o:
                            offline_mentions.add(n.encode('ascii', 'ignore'))

                if(len(mentions) > 0):
                    self.bot.say("CC: " + ', '.join(mentions), channel)
                if(len(offline_mentions) > 0):
                    self.bot.say("@msg " + ','.join(offline_mentions) + " " + msg, channel)

                #blacklist = [settings.BOT_NICK, nick, '_awwbot_', '_haibot_', '_mehbot_']
                #self.bot.say('CC: ' + ', '.join([i for i in self.known_users[channel].values() if i not in blacklist]), channel)

            # count karma upvote
            if '++' in msg_lower:
                for user in msg.split(' '):
                    if (user.endswith('++') or user.startswith('++')) and user.replace('+', '').lower() in self.known_users[channel]:
                        if user.replace('+', '') == nick:
                            self.bot.say("Nice try " + nick + ", but you can't give karma to yourself!", channel)
                        else:
                            self.increase_karma(self.known_users[channel][user.replace('+', '').lower()], channel)

            tokens = self.trimmer.sub(' ', msg_lower).replace(':', '').split(' ')
            # other actions require that botko is called first, e.g.
            # Someone: _botko_ gief karma statz
            if len(tokens) >= 1 and (tokens[0] == self.bot.nick or '@' in tokens[0]):
                tokens[0] = tokens[0].replace('@', '')
                # allow action keyword on the first or the second place, e.g.
                #   Someone: _botko_ action_kw_here action_params
                #   Someone: _botko_ whatever action_kw_here action_params

                action, kw_pos = self.actions.get(tokens[0]), 0
                if action is None and len(tokens) > 1:
                    action, kw_pos = self.actions.get(tokens[1]), 1
                if action is None and len(tokens) > 2:  # and len(): #len()???
                    action, kw_pos = self.actions.get(tokens[2]), 2

                if action is not None:
                    action(tokens[kw_pos + 1:], channel)   # send following tokens to the action logic
                #else:
                    #self.bot.say('Sorry, I don\'t understand that. Get a list of commands by typing \'' + settings.BOT_NICK + ' help\'.')

    def karma(self, tokens, channel):
        try:
            if len(tokens) != 1:
                params = urlencode({'token': settings.TOKEN, 'channel': channel})
                response = urlopen(settings.SERVER_URL + 'irc/karma_nick', params).read()
                r = json.loads(response)
                s = ""
                for p in r:
                    s += str(p['nick']) + " (" + str(p['karma']) + "), "
                self.bot.say(s[:-2], channel)
            else:
                params = urlencode({'nick': self.known_users[channel][tokens[0].lower()], 'token': settings.TOKEN, 'channel': channel})
                response = urlopen(settings.SERVER_URL + 'irc/karma_nick', params).read()
                self.bot.say(self.known_users[channel][tokens[0].lower()] + " has " + response + " karma.", channel)
        except Exception:
            from traceback import format_exc
            print "ERR " + str(format_exc())
            self.bot.log_error('ERROR getting upboats')

    def increase_karma(self, user, channel):
        try:
            params = urlencode({'nick': user, 'token': settings.TOKEN, 'channel': channel})
            urlopen(settings.SERVER_URL + 'irc/karma', params).read()
        except:
            self.bot.log_error('ERROR giving upboat to ' + user)

    def movie_night(self, tokens, channel):
        pass

    def notifications(self, tokens, channel):
        pass

    def uptime(self, tokens, channel):

        server_uptime = popen("uptime").read()
        current_uptime = time() - self.bot.uptime
        t = str(timedelta(seconds=current_uptime)).split('.')[0]
        self.bot.say("My uptime: %s, server uptime: %s" % (t, server_uptime.split(',')[0].split('up ')[1]), channel)

    def help(self, tokens, channel):
        self.print_usage(channel)

    # FFA fortune cookies
    def cookie(self, tokens, channel):
        self.bot.say(' '.join(urlopen(settings.COOKIEZ_URL).read().split('\n')), channel)

    def print_usage(self, channel):
        self.bot.say("Commands: uptime, karma [nick], join <group name> [offline], leave <group name>, leaveall, group, mygroup", channel)
