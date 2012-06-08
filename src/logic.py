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
                  self.bot.say(responses[random.randint(0, len(responses) - 1)] % {'nick': nick, 'repostNick': repostNick})
          elif response != 'OK':
              self.bot.log_error(response)
      except URLError:
          self.bot.log_error('ERROR Could not log line: ' + line)

    def parse(self, line):
        if line.startswith('ERROR'):
          raise Exception('some error')
        # TODO: document IRC protocol more
        s = line.split(' ', 2)
        nick = s[0].split('@')[0][1:].split('!')[0]
        msg = s[2].trim().split(':', 1)[1].trim()
        return nick, msg

    def new_input(self, line):
        if 'End of /MOTD command.' in line:  # after server MOTD, join desired channel
            # TODO: ensure 'End of /MOTD command.' message came from server
            self.bot.write('JOIN %s' % bot.channel)
        elif 'End of /NAMES list.' in line:  # after NAMES list, the bot is in the channel
            # TODO: ensure command from server
            # TODO: catch NAMES
            self.bot.joined_channel = True
        elif line.startswith('PING'):   # respond to pings
            self.bot.write('PONG')
            
        elif bot.joined_channel:  # respond to some messages     
            try:
                nick, msg = parse(line)
            except:
                self.bot.log_error('ERROR parsing line: ' + line)
                return
            
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
              pass
            
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

