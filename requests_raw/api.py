from .sessions import Session
from .__version__ import __title__


def raw(url, data, **kwargs):
    with Session() as session:
        return session.request(__title__, url, data=data, **kwargs)
