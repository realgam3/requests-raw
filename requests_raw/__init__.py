import urllib3
import requests
import email.parser
from requests import *
from .api import request, raw
from .adapters import RawAdapter
from .sessions import Session, session
from http.client import HTTPResponse, HTTPMessage
from .__version__ import (__version__, __build__,
                          __title__, __description__,
                          __author__, __author_email__,
                          __url__, __license__, __copyright__)

# Original Monkey patched functions
_request = requests.Session.request
_begin = HTTPResponse.begin


# Fixes Bug https://github.com/realgam3/requests-raw/issues/1
# Added Feature https://github.com/realgam3/requests-raw/issues/5
def begin(self):
    self._method = self._method or __title__
    if self.headers is not None:
        # we've already started reading the response
        return

    line = self.fp.peek()
    if not line.startswith(b"HTTP/"):
        self.code = self.status = 0
        self.reason = "Non Standard"
        self.version = 0
        self.headers = self.msg = email.parser.Parser(_class=HTTPMessage).parsestr("")
        self.length = None
        self.chunked = False
        self.will_close = True
        return

    return _begin(self)


# In case there is a Session object made before importing requests_raw
def __request(self, method, url, *args, **kwargs):
    if not getattr(self, "_raw_adapter_mounted", False):
        self.mount("http://", RawAdapter())
        self.mount("https://", RawAdapter())
        setattr(self, "_raw_adapter_mounted", True)
    return _request(self, method, url, *args, **kwargs)


def monkey_patch_all():
    setattr(requests, "raw", raw)
    setattr(requests.api, "raw", raw)
    setattr(requests.sessions.Session, "raw", Session.raw)
    setattr(requests.sessions.Session, "request", __request)
    setattr(HTTPResponse, "begin", begin)

    return True


# Monkey Patch Automatically
monkey_patch_all()
