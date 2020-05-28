from requests.adapters import HTTPAdapter
from .connectionpool import RawHTTPConnectionPool, RawHTTPSConnectionPool


class RawAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        super(RawAdapter, self).__init__(*args, **kwargs)
        self.poolmanager.pool_classes_by_scheme["http"] = RawHTTPConnectionPool
        self.poolmanager.key_fn_by_scheme["http"] = self.poolmanager.key_fn_by_scheme["http"]

        self.poolmanager.pool_classes_by_scheme["https"] = RawHTTPSConnectionPool
        self.poolmanager.key_fn_by_scheme["https"] = self.poolmanager.key_fn_by_scheme["https"]
