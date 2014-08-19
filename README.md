Botko - a simple IRC bot with some cool plugins [![Build Status](https://travis-ci.org/Psywerx/botko.svg?branch=master)](https://travis-ci.org/Pyswerx/botko/builds)
======================================

Plugins:
-------
 * PsywerxHistory (Log chats)
 * PsywerxKarma (Keep track of user karma)
 * PsywerxGroups (Define groups within a channel)
 * NSFW image detector
 * Read links (Read twitter links)
 * Uptime (Show server and bot uptimes)
  
All Psywerx* plugins require the psywerx server (https://github.com/Smotko/psywerx)
 
Run:
---
     pip install -r requirements.txt
     # start dev in mode:
     python src/main.py nodaemon
     # daemon:
     python src/main.py start|stop|restart
