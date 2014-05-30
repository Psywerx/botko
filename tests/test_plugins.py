import os
import glob
import unittest

from mock import Mock, patch

from plugins.nsfw_image_detector import NSFWImageDetectorPlugin
from plugins.read_links import ReadLinks
from tests import BasePluginTestCase


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

    @patch('plugins.nsfw_image_detector.re')
    def test_plugin_basic_functionality(self, mock_re):
        # Mock methods, we dont want plugin to actually download files
        self.plugin._download_image = Mock()
        self.plugin._is_image_url = Mock()
        self.plugin._is_image_url.return_value = True

        # First test "safe" images
        for file_path in self.safe_images:
            message = 'check this out %(url)s' % {'url': file_path}

            mock_re.findall.return_value = [file_path]
            self.plugin._download_image.return_value = file_path

            self.plugin.handle_message('channel', 'nick', message)
            self.assertFalse(self.plugin.bot.say.called)

        # Then test NSFW images
        for file_path in self.unsafe_images:
            message = 'check this out %(url)s' % {'url': file_path}

            mock_re.findall.return_value = [file_path]
            self.plugin._download_image.return_value = file_path

            self.plugin.handle_message('channel', 'nick', message)


            expected_args = ['%s is probably NSFW' % (file_path), 'channel']

        self.assertTrue(self.plugin.bot.say.call_count == len(self.unsafe_images))

class ReadLinksTestCase(BasePluginTestCase):
    def setUp(self):
        super(ReadLinksTestCase, self).setUp()

        self.plugin = ReadLinks(bot=self.bot)

    def test_sanity(self):

        self.plugin.handle_message('channel', 'nick', 'No tweet')
        self.assertFalse(self.plugin.bot.say.called)

    def test_tweet_in_message(self):
        say = self.plugin.bot.say
        self.plugin.handle_message('channel', 'nick', 'https://twitter.com/Smotko/status/469540345366450177')
        self.assertTrue(say.called)
        self.assertTrue("@Smotko on Twitter says" in say.call_args[0][0])

    def test_unicode(self):
        say = self.plugin.bot.say
        self.plugin.handle_message('channel', 'nick', 'https://twitter.com/davision/status/470158246335250432')
        self.assertTrue(say.called)
        self.assertFalse('Sorry, I wasn\'t able to read the last tweet :(' in say.call_args[0][0])

if __name__ == '__main__':
    unittest.main()
