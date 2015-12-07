'''
Created on December 7, 2015

@author: zidarsk8
'''
from plugins import base

import unittest
import mock


class BotTest(unittest.TestCase):

    def setUp(self):
        bot = mock.MagicMock()
        bot.nick = "_test_bot_"
        self.plugin = base.BotPlugin(bot=bot)

    def test_handle_valid_tokens(self):

        callback = mock.MagicMock()
        self.plugin.handle_tokens(
            "#test_channel",
            "@token",
            ('token',),
            callback)
        self.assertEqual(callback.call_count, 1)

        self.plugin.handle_tokens(
            "#test_channel",
            "@token: with some text",
            ('token',),
            callback)
        self.assertEqual(callback.call_count, 2)

    def test_bot_nick_token(self):
        callback = mock.MagicMock()
        self.plugin.handle_tokens(
            "#test_channel",
            "_test_bot_: with some text",
            ('_test_bot_',),
            callback)
        self.assertEqual(callback.call_count, 0)

        self.plugin.handle_tokens(
            "#test_channel",
            "_test_bot_: token",
            ('token',),
            callback)
        self.assertEqual(callback.call_count, 1)

        self.plugin.handle_tokens(
            "#test_channel",
            "_test_bot_ token",
            ('token',),
            callback)
        self.assertEqual(callback.call_count, 2)

    def test_without_tokens(self):
        callback = mock.MagicMock()
        self.plugin.handle_tokens(
            "#test_channel",
            "token: with some text",
            ('token',),
            callback)
        self.assertEqual(callback.call_count, 0)

    def test_invalid_tokens(self):
        callback = mock.MagicMock()
        self.plugin.handle_tokens(
            "#test_channel",
            "to@ken: with some text",
            ('token',),
            callback)
        self.assertEqual(callback.call_count, 0)
