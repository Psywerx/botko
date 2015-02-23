Botko - a simple IRC bot with some cool plugins [![Build Status](https://travis-ci.org/Psywerx/botko.svg?branch=master)](https://travis-ci.org/Pyswerx/botko/builds) [![Dependency Status](https://www.versioneye.com/user/projects/5417525c69b273bcff0000df/badge.svg?style=flat)](https://www.versioneye.com/user/projects/5417525c69b273bcff0000df) [![GitHub issues](https://img.shields.io/github/issues/psywerx/botko.svg)](https://github.com/Psywerx/botko/issues) [![Coverage Status](https://coveralls.io/repos/Psywerx/botko/badge.png)](https://coveralls.io/r/Psywerx/botko) [![Code Health](https://landscape.io/github/Psywerx/botko/master/landscape.svg)](https://landscape.io/github/Psywerx/botko/master) [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/Psywerx/botko/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/Psywerx/botko/?branch=master) [![Codacy Badge](https://www.codacy.com/project/badge/cc6934f4b32740ba9791d0efb3cf4f10)](https://www.codacy.com/public/hairyfotr/botko) [![Code Climate](https://codeclimate.com/github/Psywerx/botko/badges/gpa.svg)](https://codeclimate.com/github/Psywerx/botko)
======================================

Plugins:
-------
 * PsywerxHistory (Log chats)
 * PsywerxKarma (Keep track of user karma)
 * PsywerxGroups (Define groups within a channel)
 * NSFW image detector
 * Read links (Read twitter, youtube, and vimeo links)
 * Uptime (Show server and bot uptimes)
  
All Psywerx* plugins require the psywerx server (https://github.com/Smotko/psywerx)
 
Usage:
---
     # setup:
     pip install virtualenv
     ./setup_venv
     # start dev in mode:
     ./run
     # start as daemon:
     ./run_daemon start|stop|restart
     # run tests:
     ./run_tests
