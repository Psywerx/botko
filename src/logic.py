from urllib import urlencode
from urllib2 import urlopen, URLError
import re
import pickle
from collections import defaultdict

import settings

def static_var(varname, value):
    """Create a static var `varname` with initial `value` on a decorated function."""
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate

class BotLogic:
    def __init__(self, bot):
        self.bot = bot  # reference back to asynchat handler
        self.joined_channel = False
        self.trimmer = re.compile('[ ]+')  # used for replacing a series of spaces with a single one
        self.usertrim = re.compile('[!+@]')  # used to strip nicknames of any mode-dependent prefixes (@-op, +-voice, etc.)
        self.known_users = {}   # dict of known users present in the channel
        self.actions = {}   # actions dict, holding 'keyword':action_func, easily populated below for multiple keywords per action
                            # action_func accepts one argument, which is a list of tokens following the keyword
        karma = (self.karma, ('karma', 'leaderboard', 'upboats', 'upvotes', 'stats', ))
        movies = (self.movie_night, ('movie', 'movie-night', 'movies', 'moviez', ))
        notify = (self.notifications, ('notify', 'remind', 'tell', ))
        for action in (karma, movies, notify):
            for keyword in action[1]:
                self.actions[keyword] = action[0]
        
    def log_line_and_notify_on_repost(self, line):
      try:
          params = urlencode({'raw': line, 'token': settings.TOKEN})
          response = urlopen(settings.SERVER_URL, params).read()
          if response.startswith('REPOST'):
              _, nick, repostNick, messageType = response.split(' ')
              if messageType == 'M':
                  responses = response.SELF_REPOSTS if nick == repostNick else response.REPOSTS
                  self.bot.say(responses[random.randint(0, len(responses) - 1)] % {'nick':nick, 'repostNick':repostNick})
          elif response != 'OK':
              self.bot.log_error(response)
      except URLError:
          self.bot.log_error('ERROR Could not log line: ' + line)
    
    def get_action_code(self, line):
        if line.startswith('ERROR'): raise Exception('some IRC error')
        # behold, IRC protocol documentation:
        # :card.freenode.net 376 kjhgfdsa :End of /MOTD command.
        # :card.freenode.net 353 kjhgfdsa = #ubuntu :cornfeed calexnk edlinde Jettis zenix
        # :card.freenode.net 366 kjhgfdsa #ubuntu :End of /NAMES list.
        # :MsAshley!~pjwaffle@75-172-10-58.tukw.qwest.net PRIVMSG #ubuntu :It opens an http-vnc port, however, according to nmap
        # :sh4d0wg0d!~root@187.101.162.128 JOIN #ubuntu
        # :Dreamer3!~Dreamer3@74-133-171-106.dhcp.insightbb.com QUIT :Quit: Leaving...
        action = line.split(' ', 2)[1]
        if action == '376': return 'END_MOTD'
        if action == '353': return 'NAMES_LIST'
        if action == '366': return 'END_NAMES'
        return action.upper()

    def parse_msg(self, line):
        nick = line[1:line.find('!')]
        msg_start = line.find(':', 1)
        msg = line[msg_start + 1:].strip() if msg_start > 0 else ''   # JOIN messages have no ': message'
        return nick, msg

    def new_input(self, line):
        if line.startswith('PING'): return self.bot.write('PONG')  # ping-pong
        try:
            action_code = self.get_action_code(line)
        except:
            return self.bot.log_error('ERROR on IRC: ' + line)
          
        if action_code == 'END_MOTD':  # after server MOTD, join desired channel
            self.bot.write('JOIN ' + self.bot.channel)
        elif action_code == 'NAMES_LIST':
            self.known_users = {nick.lower():nick for nick in self.usertrim.sub('', line.split(':')[2]).split(' ')}
        elif action_code == 'END_NAMES':  # after NAMES list, the bot is in the channel
            self.joined_channel = True

        elif self.joined_channel:  # respond to some messages     
            try:
                nick, msg = self.parse_msg(line)
            except:
                return self.bot.log_error('ERROR parsing msg line: ' + line)
            
            if action_code == 'JOIN':
                self.known_users[nick.lower()] = nick  # make newly-joined user known
            elif action_code in ('PART', 'QUIT'):
                del self.known_users[nick]  # forget user when he quits/parts?
            
            self.log_line_and_notify_on_repost(line)
                
            msg_lower = msg.lower()
            
            # Simon says action
            if msg_lower.startswith('simon says: ') and nick in settings.SIMON_USERS:
                self.bot.say(msg[12:])   
            
            # FFA fortune cookies
            if msg_lower.startswith('i want a cookie'):
                self.bot.say(' '.join(urlopen(settings.COOKIEZ_URL).read().split('\n')))
            
            if msg_lower == '@all':
              self.bot.say('CC: ' + ', '.join(self.known_users.values()))
            
            # count karma upvote
            if '++' in msg_lower:
                for user in msg.split(' '):
                    if user.startswith('++') and user[2:] in self.known_users and user[2:] != nick:
                        self.increase_karma(self.known_users[user[2:]])
                    elif user.endswith('++') and user[:-2] in self.known_users and user[:-2] != nick:
                        self.increase_karma(self.known_users[user[:-2]])
                  
            
            tokens = self.trimmer.sub(' ', msg_lower).split(' ')
            
            # other actions require that botko is called first, e.g.
            # Someone: _botko_ gief karma statz
            if len(tokens) >= 2 and tokens[0] == self.bot.nick:
              
                # allow action keyword on the first or the second place, e.g.
                #   Someone: _botko_ action_kw_here action_params
                #   Someone: _botko_ whatever action_kw_here action_params
                action, kw_pos = self.actions.get(tokens[1]), 1
                if action is None and len():
                    action, kw_pos = self.actions.get(tokens[2]), 2
                
                if action is not None:
                    action(tokens[kw_pos+1:])   # send following tokens to the action logic
                else:
                    self.bot.say('What you want, I don\'t even...')
                    self.print_usage()
    
    def karma(tokens):          
        # show karma stats
        pass
        
    def increase_karma(user):
        try:
            f = open('karma_stats.dict', 'rb')
            stats = pickle.load(f)
            f.close()
        except pickle.UnpicklingError:
            stats = defaultdict(int)
        
        stats[user] += 1
        f = open('karma_stats.dict', 'wb')
        pickle.dump(stats, f, pickle.HIGHEST_PROTOCOL)
        f.close()
    
    def movie_night(tokens):
        pass
    
    def notifications(tokens):
        pass
    
    def print_usage():
        pass

