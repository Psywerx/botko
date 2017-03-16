Botko - a simple IRC bot with cool plugins [![Build Status](https://travis-ci.org/Psywerx/botko.svg?branch=master)](https://travis-ci.org/Psywerx/botko/builds) [![Circle CI](https://circleci.com/gh/Psywerx/botko.svg?style=shield)](https://circleci.com/gh/Psywerx/botko) [![Python 3](https://pyup.io/repos/github/Psywerx/botko/python-3-shield.svg)](https://pyup.io/repos/github/Psywerx/botko/) [![Updates](https://pyup.io/repos/github/Psywerx/botko/shield.svg)](https://pyup.io/repos/github/Psywerx/botko/) [![Dependency Status](https://www.versioneye.com/user/projects/5417525c69b273bcff0000df/badge.svg?style=flat)](https://www.versioneye.com/user/projects/5417525c69b273bcff0000df) [![GitHub issues](https://img.shields.io/github/issues/psywerx/botko.svg)](https://github.com/Psywerx/botko/issues) [![Coverage Status](https://coveralls.io/repos/Psywerx/botko/badge.png)](https://coveralls.io/r/Psywerx/botko) [![codecov.io](https://codecov.io/github/Psywerx/botko/coverage.svg?branch=master)](https://codecov.io/github/Psywerx/botko?branch=master) [![Code Health](https://landscape.io/github/Psywerx/botko/master/landscape.svg)](https://landscape.io/github/Psywerx/botko/master) [![Scrutinizer](https://scrutinizer-ci.com/g/Psywerx/botko/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/Psywerx/botko/?branch=master) [![codebeat badge](https://codebeat.co/badges/2111d9c9-b3dc-4be1-b28f-202511979a4d)](https://codebeat.co/projects/github-com-psywerx-botko) [![Codacy Badge](https://www.codacy.com/project/badge/cc6934f4b32740ba9791d0efb3cf4f10)](https://www.codacy.com/public/hairyfotr/botko) [![Code Climate](https://codeclimate.com/github/Psywerx/botko/badges/gpa.svg)](https://codeclimate.com/github/Psywerx/botko) [![QuantifiedCode](http://www.quantifiedcode.com/api/v1/project/3e36564674de47f7876cdb4599e8271b/badge.svg)](http://www.quantifiedcode.com/app/project/3e36564674de47f7876cdb4599e8271b)
=======================================

Plugins:
---------
 * PsywerxHistory (Log chats)
 * PsywerxKarma (Keep track of user karma)
 * PsywerxGroups (Define groups within a channel)
 * NSFW image detector
 * Read links (Read twitter, youtube, and vimeo links)
 * Uptime (Show server and bot uptimes)
  
Psywerx* plugins require the [psywerx server](https://github.com/Psywerx/psywerx).
 
Usage:
---------
     # setup:
     pip install virtualenv
     ./setup_venv
     # start dev in mode:
     ./run
     # start as daemon:
     ./run_daemon start|stop|restart
     # run tests and code analysis:
     ./run_tests
     ./run_analysis
