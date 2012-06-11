import settings
from urllib import urlencode
from urllib2 import urlopen
import re

class BotLogic:
    def __init__(self, bot):
        self.bot = bot  # reference back to asynchat handler
        self.trimmer = re.compile('[ ]+')  # used for replacing a series of spaces with a single one
        self.actions = {}   # actions dict, holding 'keyword':action_func, easily populated below for multiple keywords per action
                            # action_func accepts one argument, which is a list of tokens following the keyword
        karma = (self.karma_stats, ('karma', 'leaderboard', 'upboats', 'upvotes', 'stats', ))
        movies = (self.movie_night, ('movie', 'movie-night', 'movies', 'moviez'))
        for action in (karma, movies):
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
        msg = line[msg_start:].strip() if msg_start > 0 else ''   # JOIN messages have no ': message'
        return nick, msg

    def new_input(self, line):
        if line.startswith('PING'):   # respond to pings
            return self.bot.write('PONG')
        try:
            action_code = self.get_action_code(line)
        except:
            return self.bot.log_error('ERROR on IRC: ' + line)
          
        if action_code is 'END_MOTD':  # after server MOTD, join desired channel
            self.bot.write('JOIN ' + bot.channel)
        
        elif action_code is 'NAMES_LIST':
            pass  # TODO
        
        elif action_code is 'END_NAMES':  # after NAMES list, the bot is in the channel
            self.bot.joined_channel = True
        elif bot.joined_channel:  # respond to some messages     
            try:
                nick, msg = parse_msg(line)
            except:
                return self.bot.log_error('ERROR parsing msg line: ' + line)
            
            if action_code is 'JOIN':
                pass  # TODO
            elif action_code is in ('PART', 'QUIT'):
                pass  # TODO
            
            self.log_line_and_notify_on_repost(line)
                
            msg_lower = msg.lower()
            
            # Simon says action
            if msg_lower.startswith('simon says: ') and nick in settings.SIMON_USERS:
                self.bot.say(msg[12:])   
            
            # FFA fortune cookies
            if msg_lower.startswith('i want a cookie'):
                self.bot.say(' '.join(urlopen(settings.COOKIEZ_URL).read().split('\n')))
            
            # count karma upvote
            if '++' in msg_lower:
              pass  # TODO
            
            tokens = self.trimmer.sub(' ', msg_lower).split(' ')
            
            # other actions require that botko is called first, e.g.
            # Someone: _botko_ gief karma stac
            if len(tokens) >= 2 and tokens[0] == bot.nick:
              
              # allow action keyword on the first or the second place, e.g.
              # Someone: _botko_ action_kw_here or_action_kw_here
              action, kw_pos = self.actions.get(tokens[1]), 2
              if action is None and len():
                action, kw_pos = self.actions.get(tokens[2]), 3
              
              if action is not None:
                action(tokens[kw_pos:])
              else:
                self.bot.say('What, I don\'t even...')
                self.print_usage()
    
    def karma_stats(tokens):
        # show karma stats
        pass
    
    def movie_night(tokens):
        pass

