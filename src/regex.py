import re

TWITTER = re.compile(
    "https?://(?:www[.])?twitter[.]com/.*/status(?:es)?/(?P<id>[0-9]+)")
YOUTUBE = re.compile(
    "https?://(?:www[.])?(?:youtu[.]be|youtube[.]com)/(?:embed/)?(?:[^/ ]*?[?&]v=)?(?P<id>[A-Za-z0-9_-]{11})(?:[^A-Za-z0-9_-]|$)")  # noqa: E501
VIMEO = re.compile(
    "https?://(?:www[.])?vimeo.com/(?:videos?/)?(?P<id>[0-9]+)")
IMGUR = re.compile(
    "https?://(?:www[.])?imgur.com/(?:(?:gallery/)|(?:r/[a-z]+/))?(?P<id>[A-Za-z0-9]+)")  # noqa: E501
ANY_URL = re.compile(
    r"(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))*\))+(?:\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))*\)|[^\s'!()\[\]{};:\".,<>?]))")  # noqa: E501,P103
WEB_URL = re.compile(
    r"(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))*\))+(?:\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))*\)|[^\s'!()\[\]{};:\".,<>?]))")  # noqa: E501,P103
