'''
Created on May 10, 2012

@author: smotko
'''
from handler import Bot
from logic import BotLogic

import unittest


class BotTest(unittest.TestCase):

    def setUp(self):
        self.bot = Bot()
        self.logic = BotLogic(self.bot)

    def testParsePrivMsg(self):
        line = ":HairyFotr!~Matic@89-212-218-130.dynamic.t-2.net " \
            + "PRIVMSG #psywerx :I will try to improve my tunapasta " \
            + "from this data :P"
        nick, msg, _ = self.logic.parse_msg(line)
        self.assertEqual("HairyFotr", nick, "Nick does not match")
        self.assertEqual("I will try to improve my tunapasta "
                         + "from this data :P", msg, "Msg does not match")

    def testParseEvent(self):
        line = ":smotko!~smotko@cpe-212-85-162-22.cable.telemach.net QUIT " \
            + ":Quit: smotko"
        nick, msg, _ = self.logic.parse_msg(line)
        self.assertEqual("smotko", nick)
        self.assertEqual("Quit: smotko", msg)

    def testParseWeird(self):
        line = ":smotko!~smotko@2001:1470:fffe:fe01:4c8b:3839:ad5f:3bbb " \
            + "JOIN #smotko-testing"
        nick, msg, channel = self.logic.parse_msg(line)
        self.assertEqual("smotko", nick)
        self.assertEqual("#smotko-testing", channel)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
