#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import unittest

from mock import Mock, patch

from plugins.nsfw_image_detector import NSFWImageDetectorPlugin
from plugins.read_links import ReadLinks
from plugins.read_links import VIDEO_RESPONSES, WEB_RESPONSES


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BasePluginTestCase(unittest.TestCase):
    def setUp(self):
        self.bot = Mock()
        self.fixtures_dir = os.path.join(BASE_DIR, 'fixtures/')


class NSFWImageDetectorPluginTestCase(BasePluginTestCase):
    def setUp(self):
        # Test data and images are taken from
        # http://www.warriorhut.org/graphics/pornscanner/pornscanner.zip
        super(NSFWImageDetectorPluginTestCase, self).setUp()

        self.plugin = NSFWImageDetectorPlugin(bot=self.bot)
        self.fixtures_dir = os.path.join(self.fixtures_dir, 'nsfw_plugin')

        self.safe_images = glob.glob(os.path.join(self.fixtures_dir,
                                                  'safe/*.jpg'))
        self.unsafe_images = glob.glob(os.path.join(self.fixtures_dir,
                                                    'unsafe/*.jpg'))

    def test_is_image_url(self):
        valid_image_urls = [
            'http://www.foo.bar/1.jpg'
            'http://www.foo.bar/1.png'
            'http://www.foo.bar/1.gif'
            'http://www.foo.bar/1.JPG'
        ]
        invalid_image_urls = [
            'http://www.ponies.com/'
            'http://www.ponies.com/bar'
        ]

        for url in valid_image_urls:
            self.assertTrue(self.plugin._is_image_url(url))

        for url in invalid_image_urls:
            self.assertFalse(self.plugin._is_image_url(url))

    @patch('os.remove')
    @patch('plugins.nsfw_image_detector.re')
    def test_plugin_basic_functionality(self, mock_re, _):
        # Mock methods, we dont want plugin to actually download files
        self.plugin._download_image = Mock()
        self.plugin._is_image_url = Mock()
        self.plugin._is_image_url.return_value = True

        # First test "safe" images
        for file_path in self.safe_images:
            message = 'check this out {url!s}'.format(**{'url': file_path})

            mock_re.findall.return_value = [file_path]
            self.plugin._download_image.return_value = file_path

            self.plugin.handle_message('channel', 'nick', message)
            self.assertFalse(self.plugin.bot.say.called)

        # Then test NSFW images
        for file_path in self.unsafe_images:
            message = 'check this out {url!s}'.format(**{'url': file_path})

            mock_re.findall.return_value = [file_path]
            self.plugin._download_image.return_value = file_path

            self.plugin.handle_message('channel', 'nick', message)

        self.assertTrue(
            self.plugin.bot.say.call_count == len(self.unsafe_images))


class ReadLinksTestCase(BasePluginTestCase):
    def setUp(self):
        super(ReadLinksTestCase, self).setUp()
        self.line_start = ":smotko!~smotko@193.188.1.1 PRIVMSG #psywerx "
        self.plugin = ReadLinks(bot=self.bot)
        self.say = self.plugin.bot.say
        self.video_response = {'seconds': '34227', 'rating': 'no rating',
                               'views': '385293', 'service': 'youtube',
                               'title': 'ASP 2014 J-Bay Open English Day 10'}

    def handle_message(self, line):
        self.plugin.handle_message('channel', 'nick',
                                   line, self.line_start + line)

    def test_sanity(self):
        self.handle_message('No tweet')
        self.assertFalse(self.plugin.bot.say.called)

    def _test_helper(self, msg, response):
        self.handle_message(msg)
        self.assertTrue(self.say.called)
        assert response in self.say.call_args[0][0].split('\n')[0]

    @patch("plugins.read_links.ReadLinks._get_name_text")
    def test_tweet_in_message(self, name_text):
        name_text.return_value = ("Smotko", '_')
        tweet = 'https://twitter.com/Smotko/status/469540345366450177'
        response = "@Smotko on Twitter says"
        self._test_helper(tweet, response)

    @patch("plugins.read_links.ReadLinks._get_name_text")
    def test_unicode(self, name_text):
        name_text.return_value = ("Smotko", u'☺')
        tweet = 'https://twitter.com/Smotko/status/501844653583659010'
        self._test_helper(tweet, 'Smotko')

    @patch("plugins.read_links.ReadLinks._get_youtube_info")
    def test_youtube_no_average(self, yt_info):
        yt_info.return_value = self.video_response
        msg = 'https://www.youtube.com/watch?v=jc8zZ9PbYVM'
        response = 'ASP 2014'
        self._test_helper(msg, response)

    @patch("plugins.read_links.ReadLinks._get_vimeo_info")
    def test_vimeo(self, vimeo_info):
        vimeo_info.return_value = self.video_response
        msg = ':O http://vimeo.com/102825514'
        response = 'ASP 2014'
        self._test_helper(msg, response)

    def test_all_video_responses(self):
        for vr in VIDEO_RESPONSES:
            self.bot.say(vr % self.video_response, "channel")
            assert 'ASP 2014' in self.say.call_args[0][0].split('\n')[0]

    def test_all_web_responses(self):
        for wr in WEB_RESPONSES:
            self.bot.say(wr % {'title': 'test___'}, "channel")
            assert 'test___' in self.say.call_args[0][0].split('\n')[0]

    # TODO: mock out the actual request
    def test_web(self):
        msg = 'This is a silly website http://smotko.si/'
        response = 'Smotko\'s Blog'
        self._test_helper(msg, response)

    def test_web_no_title(self):
        msg = 'This is a silly image https://i.imgur.com/ndsBKWn.jpg'
        self.handle_message(msg)
        self.assertFalse(self.say.called)

    def test_web_title_with_https(self):
        msg = 'https://news.ycombinator.com'
        self._test_helper(msg, 'News')


if __name__ == '__main__':
    unittest.main()
