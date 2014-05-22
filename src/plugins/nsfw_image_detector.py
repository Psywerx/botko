"""
Plugin which tries to detect NSFW image URLs.

Requirements:

* Pillow
* requests
* jpeg decoder for PIL (libjpeg-dev package on Ubuntu)
"""

import re
import os
import uuid
import tempfile
from os.path import join as pjoin

import requests
from PIL import Image

from plugins.base import BotPlugin

__all__ = [
    'NSFWImageDetectorPlugin'
]

IMAGE_EXTENSIONS = [
    '.png',
    '.jpg',
    '.gif'
]

CHUNK_SIZE = 1024

SKIN_PERCENTAGE_THRESHOLD = 30


class NSFWImageDetectorPlugin(BotPlugin):

    name = 'NSFW Image Detector'
    description = ('Scans image URLs for potential NSFW images and warns '
                   'users about them')

    def __init__(self, bot):
        super(NSFWImageDetectorPlugin, self).__init__(bot=bot)
        self._images_dir = tempfile.mkdtemp(suffix='nsfw-images')

    def handle_message(self, channel, nick, msg):
        urls = re.findall(r'(https?://[^\s]+)', msg)

        if not urls:
            return

        image_urls = [url for url in urls if self._is_image_url(url=url)]

        if not image_urls:
            return

        nsfw_image_urls = self._process_images(urls=image_urls)

        for url in nsfw_image_urls:
            from response import NSFW_LINKS, random_response
            msg = random_response(NSFW_LINKS) % {'url': url, 'nick': nick}
            self.bot.say(msg, channel)

    def _process_images(self, urls):
        """
        Download all the images and return links which include potentially NSFW
        content.
        """
        nsfw_urls = []

        for url in urls:
            file_path = self._download_image(url=url)
            is_nsfw = self._is_nsfw_image(file_path=file_path)

            if is_nsfw:
                nsfw_urls.append(url)

        return nsfw_urls

    def _is_nsfw_image(self, file_path):
        """
        Detects if the provided image file is NSFW.

        Current version of this function is very simple and only detects very
        basic nudity by measuring skin tone precentage in the image.
        """
        skin_percent = self._get_skin_ratio_percentage(file_path)
        return skin_percent > SKIN_PERCENTAGE_THRESHOLD

    def _get_skin_ratio_percentage(self, file_path):
        im = Image.open(file_path)
        im = im.convert('RGB')

        im = im.crop((int(im.size[0] * 0.2), int(im.size[1] * 0.2),
                     im.size[0] - int(im.size[0] * 0.2),
                     im.size[1] - int(im.size[1] * 0.2)))

        colors = im.getcolors(im.size[0] * im.size[1])

        skin = sum([count for count, rgb in colors if rgb[0] > 60
                    and rgb[1] < (rgb[0] * 0.85) and rgb[1] < (rgb[0] * 0.7)
                    and rgb[1] > (rgb[0] * 0.4) and rgb[1] > (rgb[0] * 0.2)])

        percentage = float(skin) / float(im.size[0] * im.size[1])
        percentage = percentage * 100
        return percentage

    def _is_image_url(self, url):
        # Very simple logic, doesn't support urls which don't have an extension
        url = url.lower()
        extension = os.path.splitext(url)[1]

        return extension in IMAGE_EXTENSIONS

    def _download_image(self, url):
        """
        Download image in a temporary directory and return path to the
        downloaded file.
        """
        extension = os.path.splitext(url)[1]
        response = requests.get(url, stream=True)

        if not response.status_code == 200:
            return

        name = str(uuid.uuid4()) + extension
        file_path = pjoin(self._images_dir, name)

        with open(file_path, 'wb') as fp:
            for chunk in response.iter_content(CHUNK_SIZE):
                fp.write(chunk)

        return file_path
