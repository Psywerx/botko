from base import BotPlugin
from tweepy import OAuthHandler, API
from settings import TWITTER as t
import re
oauth = OAuthHandler(t['consumer_key'], t['consumer_secret'])
oauth.set_access_token(t['access_token_key'], t['access_token_secret'])
twt = API(oauth)
twt_regex = re.compile("https?://(?:www\\.)?twitter\\.com/.*/status(?:es)?/([0-9]+).*")


class ReadLinks(BotPlugin):

    def _read_twitter(self, channel, msg):
        res = twt_regex.search(msg)
        if not res:
            return
        try:
            st = twt.get_status(str(res.groups()[0])).text.replace('\n', ' ')
            name = st.user.screen_name

            response = unicode("@" + name + " on Twitter says: " + st)
            response = response.encode('utf8')
            self.bot.say(response, channel)
        except Exception, e:
            self.bot.say(
                'Sorry, I wasn\'t able to read the last tweet :('
                + str(e), channel)

    def _read_youtube(self, channel, msg):
        if 'youtu.be' not in msg and 'youtube.com' not in msg:
            return
        if 'v=' not in msg:
            return
        try:
            index = msg.index('v=')
            video_id = msg[index+2:index+13]
            print video_id
            from gdata.youtube import service
            client = service.YouTubeService()
            video = client.GetYouTubeVideoEntry(video_id=video_id)
            self.bot.say('Title of that yt video is \'' + video.title.text + '\'', channel)
        except:
            self.bot.say('For some reason I couldn\'t read the title of that yt link.')

    def handle_message(self, channel, nick, msg, line=None):
        if "PRIVMSG" in line:
            self._read_twitter(channel, msg)
            self._read_youtube(channel, msg)
