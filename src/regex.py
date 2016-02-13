import re

twt_regex = re.compile(
    "https?://(?:www\\.)?twitter\\.com/.*/status(?:es)?/([0-9]+)")
yt_regex = re.compile(
    "https?://(?:www\\.)?(?:youtu[.]be|youtube[.]com)/"
    + "(?:embed/)?(?:[^/ ]*?[?&]v=)?([A-Za-z0-9_-]{11})(?:[^A-Za-z0-9_-]|$)")
vimeo_regex = re.compile(
    "https?://(?:www\\.)?vimeo.com/(?:videos?/)?([0-9]+)")
url_regex = re.compile(
    r"(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s'!()\[\]{};:'\".,<>?']))")
web_regex = re.compile(
    r"(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s'!()\[\]{};:'\".,<>?']))")
