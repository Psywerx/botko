from plugins.base import BotPlugin
from TwitterAPI import TwitterAPI
from settings import TWITTER as t
import re,json
twt = TwitterAPI(t['consumer_key'], t['consumer_secret'], t['access_token_key'], t['access_token_secret'])
twt_regex = re.compile("https?://(?:www\\.)?twitter\\.com/.*/status(?:es)?/([0-9]+).*")

class ReadLinks(BotPlugin):

    def handle_message(self, channel, nick, msg):
        res = twt_regex.search(msg)
        if not res: return
        try:
            r = twt.request('statuses/show/:' + str(res.groups()[0]))
            d = json.loads(r.text)
            self.bot.say(str("@" + d['user']['screen_name'] + " on Twitter says: " + d['text']), channel)
        except Exception, e:
            self.bot.say('Sorry, I wasn\'t able to read the last tweet :(', channel)
