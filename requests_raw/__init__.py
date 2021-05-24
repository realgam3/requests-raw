import requests
from requests import *
from .api import request, raw
from .adapters import RawAdapter
from .sessions import Session, session
from .__version__ import (__version__, __build__,
                          __title__, __description__,
                          __author__, __author_email__,
                          __url__, __license__, __copyright__)

# Original session request function
_request = requests.Session.request


# Fixes Bug https://github.com/realgam3/requests-raw/issues/1
def __is_response_to_head(response):
    method = response._method or __title__
    if isinstance(method, int):
        return method == 3
    return method.upper() == "HEAD"


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
    setattr(requests.packages.urllib3.response, "is_response_to_head", __is_response_to_head)


# Monkey Patch Automatically
monkey_patch_all()
