import requests
from .api import raw
from requests import *
from .sessions import Session
from .adapters import RawAdapter
from .__version__ import (__title__, __description__, __url__,
                          __version__, __build__, __author__, __author_email__,
                          __license__, __copyright__)


def patch_all():
    setattr(requests, "raw", raw)
    setattr(requests.api, "raw", raw)
    setattr(requests.sessions, "Session", Session)
