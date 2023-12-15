try:
    import socks
except ImportError:
    import warnings
    from urllib3.exceptions import DependencyWarning

    warnings.warn(
        (
            "SOCKS support in urllib3 requires the installation of optional "
            "dependencies: specifically, PySocks.  For more information, see "
            "https://urllib3.readthedocs.io/en/1.26.x/contrib.html#socks-proxies"
        ),
        DependencyWarning,
    )
    raise

from socket import error as SocketError
from socket import timeout as SocketTimeout
from urllib3.contrib.socks import SOCKSProxyManager
from urllib3.exceptions import ConnectTimeoutError, NewConnectionError

from .connection import RawHTTPConnection, RawHTTPSConnection
from .connectionpool import RawHTTPConnectionPool, RawHTTPSConnectionPool


class RawSOCKSConnection(RawHTTPConnection):
    """
    A plain-text HTTP connection that connects via a SOCKS proxy.
    """

    def __init__(self, *args, **kwargs):
        self._socks_options = kwargs.pop("_socks_options")
        super(RawSOCKSConnection, self).__init__(*args, **kwargs)

    def _new_conn(self):
        """
        Establish a new connection via the SOCKS proxy.
        """
        extra_kw = {}
        if self.source_address:
            extra_kw["source_address"] = self.source_address

        if self.socket_options:
            extra_kw["socket_options"] = self.socket_options

        try:
            conn = socks.create_connection(
                (self.host, self.port),
                proxy_type=self._socks_options["socks_version"],
                proxy_addr=self._socks_options["proxy_host"],
                proxy_port=self._socks_options["proxy_port"],
                proxy_username=self._socks_options["username"],
                proxy_password=self._socks_options["password"],
                proxy_rdns=self._socks_options["rdns"],
                timeout=self.timeout,
                **extra_kw
            )

        except SocketTimeout:
            raise ConnectTimeoutError(
                self,
                "Connection to %s timed out. (connect timeout=%s)"
                % (self.host, self.timeout),
            )

        except socks.ProxyError as e:
            # This is fragile as hell, but it seems to be the only way to raise
            # useful errors here.
            if e.socket_err:
                error = e.socket_err
                if isinstance(error, RawHTTPSConnection):
                    raise ConnectTimeoutError(
                        self,
                        "Connection to %s timed out. (connect timeout=%s)"
                        % (self.host, self.timeout),
                    )
                else:
                    raise NewConnectionError(
                        self, "Failed to establish a new connection: %s" % error
                    )
            else:
                raise NewConnectionError(
                    self, "Failed to establish a new connection: %s" % e
                )

        except SocketError as e:  # Defensive: PySocks should catch all these.
            raise NewConnectionError(
                self, "Failed to establish a new connection: %s" % e
            )

        return conn


# We don't need to duplicate the Verified/Unverified distinction from
# urllib3/connection.py here because the HTTPSConnection will already have been
# correctly set to either the Verified or Unverified form by that module. This
# means the SOCKSHTTPSConnection will automatically be the correct type.
class RawSOCKSHTTPSConnection(RawSOCKSConnection, RawHTTPSConnection):
    pass


class RawSOCKSHTTPConnectionPool(RawHTTPConnectionPool):
    ConnectionCls = RawSOCKSConnection


class RawSOCKSHTTPSConnectionPool(RawHTTPSConnectionPool):
    ConnectionCls = RawSOCKSHTTPSConnection


class RawSOCKSProxyManager(SOCKSProxyManager):
    pool_classes_by_scheme = {
        "http": RawSOCKSHTTPConnectionPool,
        "https": RawSOCKSHTTPSConnectionPool,
    }

    def __init__(
            self,
            proxy_url,
            username=None,
            password=None,
            num_pools=10,
            headers=None,
            **connection_pool_kw
    ):
        super(RawSOCKSProxyManager, self).__init__(
            proxy_url,
            username=username,
            password=password,
            num_pools=num_pools,
            headers=headers,
            **connection_pool_kw
        )
        self.pool_classes_by_scheme = RawSOCKSProxyManager.pool_classes_by_scheme
