import requests
from requests import *
from .adapters import RawAdapter
from .__version__ import (__title__, __description__, __url__,
                          __version__, __build__, __author__, __author_email__,
                          __license__, __copyright__)


class Session(requests.Session):
    def __init__(self):
        super(Session, self).__init__()
        self.mount("http://", RawAdapter())
        self.mount("https://", RawAdapter())

    def raw(self, url, data, **kwargs):
        kwargs.setdefault('allow_redirects', True)
        return self.request(__title__, url, data=data, **kwargs)


def session():
    return Session()


def raw(url, data, **kwargs):
    with Session() as session:
        return session.request(__title__, url, data=data, **kwargs)


def patch_all():
    setattr(requests, "raw", raw)
    setattr(requests.api, "raw", raw)
    setattr(requests.sessions, "Session", Session)
