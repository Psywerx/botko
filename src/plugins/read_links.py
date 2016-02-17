from base import BotPlugin
from tweepy import OAuthHandler, API as TWITTER_API
from settings import TWITTER as T
from response import random_response
from urllib2 import urlopen
import re
import json
import requests
import lxml.html
import regex

TWITTER_OAUTH = OAuthHandler(T['consumer_key'], T['consumer_secret'])
TWITTER_OAUTH.set_access_token(T['access_token_key'], T['access_token_secret'])
TWITTER = TWITTER_API(TWITTER_OAUTH)

# These will be filtered out in _read_webistes
__all_non_web__ = [regex.TWITTER, regex.YOUTUBE, regex.VIMEO]

VIDEO_RESPONSES = [
    "That video is titled '%(title)s'. "
    + "You will waste %(seconds)ss of your life watching it. ",
    "The title of that %(service)s video is '%(title)s'. "
    + "It has been viewed %(views)s times. ",
    "Title: '%(title)s', Views: %(views)s, duration: %(seconds)ss.",
    "Title of that %(service)s video is '%(title)s'.",
    "%(service)s video is titled '%(title)s' and has %(rating)s.",
    "Here is the title of that %(service)s video: '%(title)s'.",
    "I found the title of that %(service)s video, here it is: '%(title)s'",
    "If you click that link you will watch a video titled '%(title)s'. "
    + "Good luck!",
]

WEB_RESPONSES = [
    "The title of that page is '%(title)s'",
    "That page might be about %(title)s",
    "That page has an interesting title: '%(title)s'",
    "The title of that page makes me want to read the whole thing '%(title)s'",
    "%(title)s",
]


class ReadLinks(BotPlugin):

    def _get_tweet_info(self, status_id):
        status = TWITTER.get_status(status_id)
        name = status.user.screen_name
        text = status.text.replace('\n', ' ')
        return name, text

    def _read_twitter(self, channel, msg):
        twt_res = regex.TWITTER.search(msg)
        if not twt_res:
            return
        try:
            (name, text) = self._get_tweet_info(twt_res.group('id'))
            response = unicode("@" + name + " on Twitter says: " + text)
            response = response.encode('utf8')
            self.bot.say(response, channel)
        except:
            self.bot.log_error('Could not get tweet from: "' + msg + '"')
            self.bot.say('Sorry, I wasn\'t able to read the last tweet :(',
                         channel)

    def _get_vimeo_info(self, video_id):
        api_url = "https://vimeo.com/api/v2/video/" + video_id + ".json"
        r = requests.get(api_url)
        video = json.loads(r.text)[0]
        if "stats_number_of_likes" in video:
            likes = ("%d likes." % video["stats_number_of_likes"])
        else:
            likes = "an unknown number of likes"
        return {
            'service': "vimeo",
            'title': video["title"].encode('utf8'),
            'seconds': str(video["duration"]),
            'views': str(video["stats_number_of_plays"]),
            'rating': likes
        }

    def _read_vimeo(self, channel, msg):
        vimeo_res = regex.VIMEO.search(msg)
        if not vimeo_res:
            return
        try:
            video_info = self._get_vimeo_info(vimeo_res.group('id'))
            self.bot.say(random_response(VIDEO_RESPONSES) % video_info,
                         channel)
        except:
            self.bot.log_error('Could not get title of vimeo link from: "'
                               + msg + '"')
            self.bot.say('For some reason I couldn\'t read the title of that '
                         + 'vimeo link.', channel)

    def _get_youtube_info(self, video_id):
        import pafy
        url = "https://www.youtube.com/watch?v={0}".format(video_id)
        video = pafy.new(url)

        if video.rating is not None:
            average_rating = float(video.rating)
            rating = ("an average rating of %.2f" % average_rating)
        else:
            rating = "no rating"
        return {
            'service': "youtube",
            'title': video.title.encode('utf-8'),
            'seconds': video.length,
            'views': video.viewcount,
            'rating': rating
        }

    def _read_youtube(self, channel, msg):
        yt_res = regex.YOUTUBE.search(msg)
        if not yt_res:
            return
        try:
            video_info = self._get_youtube_info(yt_res.group('id'))
            self.bot.say(random_response(VIDEO_RESPONSES) % video_info,
                         channel)
        except:
            self.bot.log_error('Could not get title of youtube link from: "'
                               + msg + '"')
            self.bot.say('For some reason I couldn\'t read the title of that '
                         + 'youtube link.', channel)

    def _read_websites(self, channel, msg):
        links = regex.WEB_URL.findall(msg)
        for link in links:
            if [r for r in __all_non_web__ if r.search(link)]:
                continue
            try:
                t = lxml.html.parse(urlopen(link))  # nopep8 # nosec: regex.WEB_URL only allows http(s)
                t = t.find(".//title").text
                t = t.strip().replace('\n', ' ')
                if len(re.sub("[^a-zA-Z0-9]", "", t)) >= 5:
                    self.bot.say(random_response(WEB_RESPONSES) % {'title': t},
                                 channel)
            except:
                self.bot.log_error('Could not get title of webpage: "'
                                   + msg + '"')

    def handle_message(self, channel, nick, msg, line=None):
        if "PRIVMSG" in line:
            self._read_twitter(channel, msg)
            self._read_youtube(channel, msg)
            self._read_vimeo(channel, msg)
            self._read_websites(channel, msg)
