import requests
from .api import raw
from requests import *
from .sessions import Session
from .adapters import RawAdapter
from .__version__ import (__version__, __build__,
                          __title__, __description__,
                          __author__, __author_email__,
                          __url__, __license__, __copyright__)


def monkey_patch_all():
    setattr(requests, "raw", raw)
    setattr(requests.api, "raw", raw)
    setattr(requests, "Session", Session)
    setattr(requests.sessions, "Session", Session)
