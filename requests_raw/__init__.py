import requests
from .api import raw
from requests import *
from .sessions import Session
from .adapters import RawAdapter
from .__version__ import (__version__, __build__,
                          __title__, __description__,
                          __author__, __author_email__,
                          __url__, __license__, __copyright__)

# Original session request function
_request = requests.Session.request


def monkey_patch_all():
    def __request(self, method, url, *args, **kwargs):
        if not getattr(self, "_raw_adapter_mounted", False):
            self.mount("http://", RawAdapter())
            self.mount("https://", RawAdapter())
            setattr(self, "_raw_adapter_mounted", True)
        return _request(self, method, url, *args, **kwargs)

    setattr(requests, "raw", raw)
    setattr(requests.api, "raw", raw)
    setattr(requests.sessions.Session, "raw", Session.raw)
    setattr(requests.sessions.Session, "request", __request)
