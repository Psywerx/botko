import settings
from urllib import urlencode
from urllib2 import urlopen
import re

def parse(line):
    if line.startswith('ERROR'):
      raise Exception('some error')
    # TODO: document IRC protocol more
    s = line.split(' ', 2)
    nick = s[0].split('@')[0][1:].split('!')[0]
    msg = s[2].split(':', 1)[1]
    return nick, msg


def new_input(line, bot):
  
  if line.find('End of /MOTD command.'):  # after server MOTD, join desired channel
      # TODO: ensure 'End of /MOTD command.' message came from server
      bot.write('JOIN %s' % bot.channel)
  elif line.find('End of /NAMES list.'):  # after NAMES list, the bot is in the channel
      # TODO: ensure command from server
      bot.joined_channel = True
  elif line.startswith('PING'):   # respond to pings
      bot.write('PONG')
      
  elif bot.joined_channel:
      # respond to some messages     
      try:
          nick, msg = parse(line)
          msg_lower = msg.lower()
          
          if msg_lower.startswith('simon says: ') and nick in settings.SIMON_USERS:
              bot.say(msg[12:])   
          
          if msg_lower.startswith('i want a cookie'):   # FFA fortune cookies
              bot.say(' '.join(urlopen(settings.COOKIEZ_URL).read().split('\n')))
          
          tokens = new_input.trim_spaces.sub(' ', msg_lower).split(' ')
          
          # TODO: here.
      
          # log the line and potentially notify of reposts
          params = urlencode({'raw': line, 'token': settings.TOKEN})
          f = urlopen(settings.SERVER_URL, params)
          response = f.read()
          if response.startswith('REPOST'):
              (_, nick, repostNick, messageType) = response.split(' ')
              if messageType == 'M':
                  responses = response.SELF_REPOSTS if nick == repostNick else response.REPOSTS
                  bot.say(responses[random.randint(0, len(responses) - 1)] % {'nick': nick, 'repostNick': repostNick})
          elif response != 'OK':
              bot.log_error(response)
          
      except URLError:
          bot.log_error('ERROR Could not log line: ' + line)
          if bot.debug:
              print 'ERROR Could not log line:', line
      except:
          bot.log_error('ERROR parsing line: ' + line)
          if bot.debug:
              print 'ERROR parsing line:', line 


new_input.trim_spaces = re.compile('[ ]+')  # used for replacing a series of spaces with a single one
