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

    def handle_message(self, channel, nick, msg):
        """
        Function which handles channel message lines and optionally, performs
        any necessary action.

        :param channel: Channel to which the message was sent to.
        :param nick: User which has sent the message.
        :param msg: Actual message.
        """
        raise NotImplementedError('handle_message not implemented')
