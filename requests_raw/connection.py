from .__version__ import __title__
from requests.utils import urlparse
from urllib3.connection import HTTPConnection, HTTPSConnection

try:
    from http import client
except ImportError:
    import httplib as client


class RawHTTPConnection(HTTPConnection):
    def __init__(self, *args, **kwargs):
        super(RawHTTPConnection, self).__init__(*args, **kwargs)
        self.__url = None
        self.__method = None

    def putrequest(self, method, url, *args, **kwargs):
        self.__method = method.lower()
        if self.__method != __title__:
            return super(RawHTTPConnection, self).putrequest(
                method, url, *args, **kwargs
            )

        self.__url = urlparse(url)
        if self._HTTPConnection__response and self._HTTPConnection__response.isclosed():
            self._HTTPConnection__response = None

        if self._HTTPConnection__state == client._CS_IDLE:
            self._HTTPConnection__state = client._CS_REQ_STARTED
        else:
            raise client.CannotSendRequest(self._HTTPConnection__state)

    def putheader(self, header, *values):
        if self.__method != __title__:
            return super(RawHTTPConnection, self).putheader(header, *values)

        if self._HTTPConnection__state != client._CS_REQ_STARTED:
            raise client.CannotSendHeader()

    def endheaders(self, message_body=None, **kwargs):
        if self.__method != __title__:
            return super(RawHTTPConnection, self).endheaders(message_body=message_body, **kwargs)

        buffer = message_body
        # HTTP Proxy
        if self.__url.scheme and self.__url.netloc:
            _buffer = buffer.split(b"/", 1)
            if _buffer[0].endswith(b" "):
                _buffer.insert(1, "{url.scheme}://{url.netloc}/".format(url=self.__url).encode())
            else:
                _buffer.insert(1, b"/")
            buffer = b"".join(_buffer)
        if self._HTTPConnection__state == client._CS_REQ_STARTED:
            self._HTTPConnection__state = client._CS_REQ_SENT
        else:
            raise client.CannotSendHeader()
        self.send(buffer)


class RawHTTPSConnection(HTTPSConnection):
    def __init__(self, *args, **kwargs):
        super(RawHTTPSConnection, self).__init__(*args, **kwargs)

    def putrequest(self, method, url, *args, **kwargs):
        self.__method = method.lower()
        if self.__method != __title__:
            return super(RawHTTPSConnection, self).putrequest(
                method, url, *args, **kwargs
            )

        if self._HTTPConnection__response and self._HTTPConnection__response.isclosed():
            self._HTTPConnection__response = None

        if self._HTTPConnection__state == client._CS_IDLE:
            self._HTTPConnection__state = client._CS_REQ_STARTED
        else:
            raise client.CannotSendRequest(self._HTTPConnection__state)

    def putheader(self, header, *values):
        if self.__method != __title__:
            return super(RawHTTPSConnection, self).putheader(header, *values)

        if self._HTTPConnection__state != client._CS_REQ_STARTED:
            raise client.CannotSendHeader()

    def endheaders(self, message_body=None, **kwargs):
        if self.__method != __title__:
            return super(RawHTTPSConnection, self).endheaders(message_body=message_body, **kwargs)

        if self._HTTPConnection__state == client._CS_REQ_STARTED:
            self._HTTPConnection__state = client._CS_REQ_SENT
        else:
            raise client.CannotSendHeader()
        self.send(message_body)
