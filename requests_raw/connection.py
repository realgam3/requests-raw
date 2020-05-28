from http import client
from requests.utils import urlparse
from urllib3.connection import HTTPConnection, HTTPSConnection


class RawHTTPConnection(HTTPConnection):
    def __init__(self, *args, **kwargs):
        super(RawHTTPConnection, self).__init__(*args, **kwargs)

    def putrequest(self, method, url, skip_host=False, skip_accept_encoding=False):
        self.__url = urlparse(url)
        if self._HTTPConnection__response and self._HTTPConnection__response.isclosed():
            self._HTTPConnection__response = None

        if self._HTTPConnection__state == client._CS_IDLE:
            self._HTTPConnection__state = client._CS_REQ_STARTED
        else:
            raise client.CannotSendRequest(self._HTTPConnection__state)

    def putheader(self, header, *values):
        if self._HTTPConnection__state != client._CS_REQ_STARTED:
            raise client.CannotSendHeader()

    def endheaders(self, message_body=None, *, encode_chunked=False):
        buffer = message_body
        # HTTP Proxy
        if self.__url.scheme and self.__url.netloc:
            _buffer = buffer.split(b"/", 1)
            _buffer.insert(1, f"{self.__url.scheme}://{self.__url.netloc}/".encode())
            buffer = b"".join(_buffer)
        if self._HTTPConnection__state == client._CS_REQ_STARTED:
            self._HTTPConnection__state = client._CS_REQ_SENT
        else:
            raise client.CannotSendHeader()
        self.send(buffer)


class RawHTTPSConnection(HTTPSConnection):
    def __init__(self, *args, **kwargs):
        super(RawHTTPSConnection, self).__init__(*args, **kwargs)

    def putrequest(self, method, url, skip_host=False, skip_accept_encoding=False):
        if self._HTTPConnection__response and self._HTTPConnection__response.isclosed():
            self._HTTPConnection__response = None

        if self._HTTPConnection__state == client._CS_IDLE:
            self._HTTPConnection__state = client._CS_REQ_STARTED
        else:
            raise client.CannotSendRequest(self._HTTPConnection__state)

    def putheader(self, header, *values):
        if self._HTTPConnection__state != client._CS_REQ_STARTED:
            raise client.CannotSendHeader()

    def endheaders(self, message_body=None, *, encode_chunked=False):
        if self._HTTPConnection__state == client._CS_REQ_STARTED:
            self._HTTPConnection__state = client._CS_REQ_SENT
        else:
            raise client.CannotSendHeader()
        self.send(message_body)
