from requests import *
from .__version__ import *
from functools import partial
from .adapters import RawAdapter


def __raw(self, url, **kwargs):
    kwargs.setdefault('allow_redirects', False)
    s = Session()
    s.mount("http://", RawAdapter())
    s.mount("https://", RawAdapter())
    return s.request("raw", url, **kwargs)


setattr(Session, "raw", __raw)
raw = partial(__raw, self=None)
