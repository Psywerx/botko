import re

__all__ = [
    'BotPlugin'
]


class BotPlugin(object):

    """Base class other plugins must inherit from."""

    name = None
    description = None
    trimmer = re.compile('[ ]+')

    def __init__(self, bot):
        """
        :param bot: Bot instance.
        """
        self.bot = bot

    def handle_tokens(self, channel, msg, keywords, callback):
        """
        Tokenize message and handle callbacks.

        Handle callbacks if the message starts with @ or the server name.
        """
        tokens = msg.lower().replace(':', '').split()
        token = None
        if tokens and tokens[0].startswith("@"):
            token = tokens.pop(0).replace('@', '')
        elif tokens[0] == self.bot.nick and len(tokens) > 1:
            token = tokens[1:].pop(0)

        if token in keywords:
            callback(tokens, channel)

    def handle_message(self, channel, nick, msg, line):
        """
        Handle channel message lines and optionally perform actions.

        :param channel: Channel to which the message was sent to.
        :param nick: User which has sent the message.
        :param msg: Actual message.
        :param line: Raw line received from serve
        """
        raise NotImplementedError('handle_message not implemented')

    def handle_say(self, channel, msg, line):
        """Handle responses the bot has made."""
        pass


class PsywerxPlugin(BotPlugin):

    """Base class that communicates with the psywerx server."""

    def request(self, channel, url, extra_params):
        from settings import PSYWERX as P
        from urllib import urlencode
        from urllib2 import urlopen
        try:
            params = urlencode(dict({
                'token': P['TOKEN'],
                'channel': channel
            }, **extra_params))
            return urlopen(P['SERVER_URL'] + url, params).read()
        except:
            self.bot.log_error('Request failed: ' + url + params)
