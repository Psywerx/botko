'''
Created on May 10, 2012

@author: smotko
'''
import unittest
from handler import Bot

class BotTest(unittest.TestCase):
    
    def setUp(self):
        self.bot = Bot()

    def testParsePrivMsg(self):
        line = ":HairyFotr!~Matic@89-212-218-130.dynamic.t-2.net PRIVMSG #psywerx :I will try to improve my tunapasta from this data :P"
        nick, msg = self.bot.parse(line)
        self.assertEqual("HairyFotr", nick, "Nick does not match")
        self.assertEqual("I will try to improve my tunapasta from this data :P", msg, "Msg does not match")

    def testParseEvent(self):
        line = ":smotko!~smotko@cpe-212-85-162-22.cable.telemach.net QUIT :Quit: smotko"
        nick, msg = self.bot.parse(line)
        self.assertEqual("smotko", nick)
        self.assertEqual("Quit: smotko", msg)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()