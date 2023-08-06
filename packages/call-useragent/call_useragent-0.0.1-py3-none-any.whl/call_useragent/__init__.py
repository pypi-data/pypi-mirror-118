from call_useragent.head import UserAgents
from random import choice


def random():
    browser = choice(list(UserAgents.keys()))
    ug = choice(UserAgents[browser])
    return f"'User-Agent':{ug}"
