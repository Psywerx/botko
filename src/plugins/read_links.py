from base import BotPlugin
from tweepy import OAuthHandler, API
from settings import TWITTER as T
from response import random_response
import re
oauth = OAuthHandler(T['consumer_key'], T['consumer_secret'])
oauth.set_access_token(T['access_token_key'], T['access_token_secret'])
twt = API(oauth)
twt_regex = re.compile(
    "https?://(?:www\\.)?twitter\\.com/.*/status(?:es)?/([0-9]+)")
yt_regex = re.compile(
    "https?://(?:www\\.)?(?:youtu[.]be|youtube[.]com)/"
    + "(?:embed/)?(?:[^/ ]*?[?&]v=)?([A-Za-z0-9_-]{11})(?:[^A-Za-z0-9_-]|$)")

YOUTUBE_RESPONSES = [
    "That video is titled '%(title)s'. "
    + "You will waste %(seconds)ss of your life watching it. ",
    "The title of that yt video is '%(title)s'. "
    + "It has been viewed %(views)s times. ",
    "Title: '%(title)s', Views: %(views)s, duration: %(seconds)ss.",
    "Title of that yt video is '%(title)s'.",
    "Yt video is titled '%(title)s' and has %(rating)s.",
    "Here is the title of that yt video: '%(title)s'.",
    "I found the title of that yt video, here it is: '%(title)s'",
    "If you click that link you will watch a video titled '%(title)s'. "
    + "Good luck!"
]


class ReadLinks(BotPlugin):

    def _get_name_text(self, id):
        status = twt.get_status(id)
        name = status.user.screen_name
        text = status.text.replace('\n', ' ')
        return name, text

    def _read_twitter(self, channel, msg):
        res = twt_regex.search(msg)
        if not res:
            return
        try:
            (name, text) = self._get_name_text(str(res.groups()[0]))
            response = unicode("@" + name + " on Twitter says: " + text)
            response = response.encode('utf8')
            self.bot.say(response, channel)
        except Exception as e:
            print e
            self.bot.log_error('ERROR could not get tweet from: "'
                               + msg + '" the exception was: ' + str(e))
            self.bot.say('Sorry, I wasn\'t able to read the last tweet :(',
                         channel)

    def _read_youtube(self, channel, msg):
        res = yt_regex.search(msg)
        if not res:
            return
        try:
            video_id = str(res.groups()[0])
            from gdata.youtube import service
            client = service.YouTubeService()
            video = client.GetYouTubeVideoEntry(video_id=video_id)
            avarage_rating = float(video.rating.average)
            if video.rating is not None:
                rating = ("an average rating of %.2f" % avarage_rating)
            else:
                rating = "no rating"
            video_info = {
                'title': video.title.text,
                'seconds': video.media.duration.seconds,
                'views': video.statistics.view_count,
                'rating': rating
            }
            self.bot.say(random_response(YOUTUBE_RESPONSES) % video_info,
                         channel)
        except Exception as e:
            self.bot.log_error('ERROR could not get title of a yt link from: "'
                               + msg + '" the exception was: ' + str(e))
            self.bot.say('For some reason I couldn\'t read the title of that '
                         + 'yt link.', channel)

    def handle_message(self, channel, nick, msg, line=None):
        if "PRIVMSG" in line:
            self._read_twitter(channel, msg)
            self._read_youtube(channel, msg)
