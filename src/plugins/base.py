__all__ = [
    'BotPlugin'
]


class BotPlugin(object):
    """
    Represents a base class other plugins must inherit from.
    """

    name = None
    description = None

    def __init__(self, bot):
        """
        :param bot: Bot instance.
        """
        self.bot = bot

    def handle_message(self, channel, nick, msg, line):
        """
        Function which handles channel message lines and optionally, performs
        any necessary action.

        :param channel: Channel to which the message was sent to.
        :param nick: User which has sent the message.
        :param msg: Actual message.
        :param line: Raw line received from serve
        """
        raise NotImplementedError('handle_message not implemented')

    def handle_say(self, channel, msg, line):
        """
        Function which handles responses the bot has made.
        """
        pass

class PsywerxPlugin(BotPlugin):
    """
    Base class that communicates with the psywerx server
    """

    def request(self, channel, url, extra_params):
        from settings import PSYWERX as p
        from urllib import urlencode
        from urllib2 import urlopen, URLError
        try:
            params = urlencode(dict({
                'token': p['TOKEN'],
                'channel': channel
            }, **extra_params))
            return urlopen(p['SERVER_URL'] + url, params).read()
        except Exception:
            self.bot.log_error('Request failed: ' + url)
