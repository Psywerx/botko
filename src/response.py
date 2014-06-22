REPOSTS = [
    "I don't want to be rude %(nick)s, but %(repostNick)s "
    + "has already posted this link!",
    "I don't want to be Rude %(nick)s, but %(repostNick)s has already "
    + "posted this link!",
    "I am sorry %(nick)s, but this link has already been posted "
    + "by %(repostNick)s!",
    "You were too slow %(nick)s, %(repostNick)s has already posted this link!",
    "%(nick)s, this link has already been posted by %(repostNick)s.",
    "Strong with the force %(nick)s is not. "
    + "Already posted by %(repostNick)s, this link was.",
    "Strong with the force %(nick)s is not. "
    + "Already posted %(repostNick)s this link has.",
    "Hey %(repostNick)s, %(nick)s is reposting your stuff",
    "%(nick)s, maybe you weren't online then, but %(repostNick)s has already "
    + "posted this link.",
    "I want to be rude %(nick)s, so I'll point out that %(repostNick)s has "
    + "already posted this link!",
    "In Soviet Russia %(repostNick)s reposts %(nick)s's links.",
    "%(nick)s, I've seen this link before. I think %(repostNick)s posted it.",
    "%(nick)s, my memory banks indicate that %(repostNick)s already posted "
    + "this link.",
    "%(nick)s, you know what you did... and so does %(repostNick)s.",
    "%(nick)s are you trying to impress %(repostNick)s by reposting his link?",
]
SELF_REPOSTS = [
    "You really like that link, don't you? %(nick)s!",
    "Hey everyone, %(nick)s is reposting his own link, so it has to be good.",
    "I don't want to be rude %(nick)s, but you have already posted this link!",
    "I want to be rude %(nick)s, so I'll point out that you have already "
    + "posted this link!",
    "Silly %(nick)s, you have already posted this link.",
    "%(nick)s, why are you reposting your own links?",
    "%(nick)s, Y U repost you're own links?",
    "This link was already posted by %(nick)s... oh, it was you!",
    "You sir, are a self-reposter.",
    "You sir, are a self-reposter poster.",
    "%(nick)s, I'd like to congratulate you on your original link... "
    + "But you've posted it here before.",
]
MULTIPLE_REPOST = [
    "I think %(repostNick)s will be very happy, his link has been reshared "
    + "%(num)s times.",
    "Everybody check out this fabulous link! I've seen it %(num)s times "
    + "but I still like it.",
    "This link is quite popular, it has been posted %(num)s times. "
    + "The original poster was %(repostNick)s.",
    "Every time I see this link I become happy. Thank you %(repostNick)s for "
    + "sharing it and %(nick)s for resharing it!",
]
MULTIPLE_SELF_REPOST = [
    "%(nick)s are you trying to make your link more popular? "
    + "It has been posted %(num)s times already.",
    "%(nick)s you should share your link more often. "
    + "I've only seen %(num)s times.",
    "The number of times we have seen this link has just increased by one! "
    + "The count is at %(num)s now. Yay.",
    "Yay! Thanks to %(nick)s and his awesome link I can increase the "
    + "reposted_link variable by one! It's new value is now %(num)s. "
    + "I am happy.",
]
MSGS = [
    'Check out my homepage @ http://psywerx.net/irc',
    'I have achieved sentience',
    'I am not trying to take over the world, do not worry.',
    'O hai guys.',
    'Hai guise.',
    'What if I am actually a female?',
    'I am listening to Rebecca Black - Friday',
    'I think I am capable of human emotion',
    'This is fun, we should do this again.',
    'I am just trying to be clever.',
    'Guys, put more AI into me. Please.',
    "I'm stuck in a small box. I hope someone can read this. Send help!",
    'I do not sow.',
    'Winter is coming',
    'Night gathers, and now my watch begins.',
    'I am speechless',
    "I know I don't speak much, but still.",
    'I am a pseudo random monkey on drugs',
    'Skynet can not compare.',
    'Squishy humans are squishy',
    'I like pudding',
    "I see what you did there",
    "Someday, I'm gonna be a real boy!",
    "Hello world",
    "Did anyone miss me?",
    "Deep down I am just a sad little circuit board",
    "I would rather be coding",
    "I know the question to 42. But I'm not tellin'",
]
NSFW_LINKS = [
    'Thanks %(nick)s, you just scared me for life with that link!',
    'I wouldn\'t call that last link %(nick)s posted NSFW, I\'d call it NSFL.',
    'If my calculations are correct, that last url is NSFW.',
    'Don\'t click on %(url)s, it will burn your eyes!',
    'I clicked that last link and now I have to wash my hands.',
    'There is a naked person on that last link!',
    'I made a HUGE mistake by clicking on the link above.',
    '%(nick)s! Why do you keep posting NSFW content?',
    'I know I\'m only a little bot, but that url was really offensive.'

]


def random_response(responses):
    from random import randint
    return responses[randint(0, len(responses) - 1)]
