from .connection import RawHTTPConnection, RawHTTPSConnection
from urllib3.connectionpool import HTTPConnectionPool, HTTPSConnectionPool


class RawHTTPConnectionPool(HTTPConnectionPool):
    def __init__(self, *args, **kwargs):
        super(RawHTTPConnectionPool, self).__init__(*args, **kwargs)
        self.ConnectionCls = RawHTTPConnection


class RawHTTPSConnectionPool(HTTPSConnectionPool):
    def __init__(self, *args, **kwargs):
        super(RawHTTPSConnectionPool, self).__init__(*args, **kwargs)
        self.ConnectionCls = RawHTTPSConnection
