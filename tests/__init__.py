import os
import unittest

from mock import Mock

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BasePluginTestCase(unittest.TestCase):
    def setUp(self):
        self.bot = Mock()
        self.fixtures_dir = os.path.join(BASE_DIR, 'fixtures/')
