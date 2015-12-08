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

    def test_empty_tokens(self):

        callback = mock.MagicMock()
        self.plugin.handle_tokens(
            "",
            ('token',),
            callback)
        self.assertEqual(callback.call_count, 0)

    def test_handle_valid_tokens(self):

        callback = mock.MagicMock()
        self.plugin.handle_tokens(
            "@token",
            ('token',),
            callback)
        self.assertEqual(callback.call_count, 1)

        self.plugin.handle_tokens(
            "@token: with some text",
            ('token',),
            callback)
        self.assertEqual(callback.call_count, 2)

    def test_bot_nick_token(self):
        callback = mock.MagicMock()
        self.plugin.handle_tokens(
            "_test_bot_: with some text",
            ('_test_bot_',),
            callback)
        self.assertEqual(callback.call_count, 0)

        self.plugin.handle_tokens(
            "_test_bot_: token",
            ('token',),
            callback)
        self.assertEqual(callback.call_count, 1)

        self.plugin.handle_tokens(
            "_test_bot_ token",
            ('token',),
            callback)
        self.assertEqual(callback.call_count, 2)

    def test_without_tokens(self):
        callback = mock.MagicMock()
        self.plugin.handle_tokens(
            "token: with some text",
            ('token',),
            callback)
        self.assertEqual(callback.call_count, 0)

    def test_invalid_tokens(self):
        callback = mock.MagicMock()
        self.plugin.handle_tokens(
            "to@ken: with some text",
            ('token',),
            callback)
        self.assertEqual(callback.call_count, 0)

    def test_handle_tokens_callback_args(self):
        callback = mock.MagicMock()
        self.plugin.handle_tokens(
            "@token: with some text",
            ('token',),
            callback,
            "#channel_name"
        )
        self.assertIn("#channel_name", callback.call_args[0])

        self.plugin.handle_tokens(
            "@token: with some text",
            ('token',),
            callback,
            "#channel_name",
            "nickname",
            1
        )
        self.assertEqual("#channel_name", callback.call_args[0][1])
        self.assertEqual("nickname", callback.call_args[0][2])
        self.assertEqual(1, callback.call_args[0][3])
