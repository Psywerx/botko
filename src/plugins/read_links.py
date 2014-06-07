from base import BotPlugin
from tweepy import OAuthHandler, API
from settings import TWITTER as t
import re
oauth = OAuthHandler(t['consumer_key'], t['consumer_secret'])
oauth.set_access_token(t['access_token_key'], t['access_token_secret'])
twt = API(oauth)
twt_regex = re.compile("https?://(?:www\\.)?twitter\\.com/.*/status(?:es)?/([0-9]+).*")

class ReadLinks(BotPlugin):

    def handle_message(self, channel, nick, msg, line=None):
        res = twt_regex.search(msg)
        if not res: return
        try:
            status = twt.get_status(str(res.groups()[0]))
            response = unicode("@" + status.user.screen_name + " on Twitter says: " + status.text)
            response = response.encode('utf8')
            self.bot.say(response, channel)
        except Exception, e:
            self.bot.say('Sorry, I wasn\'t able to read the last tweet :(' + str(e), channel)
