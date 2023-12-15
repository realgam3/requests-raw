import typing
from http import client
from .__version__ import __title__
from urllib3.util.url import parse_url
from urllib3.connection import HTTPConnection, HTTPSConnection, _TYPE_BODY


class RawHTTPConnection(HTTPConnection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__method = None

    def request(
            self,
            method: str,
            url: str,
            body: _TYPE_BODY | None = None,
            headers: typing.Mapping[str, str] | None = None,
            *,
            chunked: bool = False,
            preload_content: bool = True,
            decode_content: bool = True,
            enforce_content_length: bool = True,
    ) -> None:
        self.__method = method.lower()
        if self.__method == __title__:
            # HTTP Proxy
            _url = parse_url(url)
            if _url.scheme and _url.netloc:
                _body = body.split(b"/", 1)
                if _body[0].endswith(b" "):
                    _body.insert(1, "{url.scheme}://{url.netloc}/".format(url=_url).encode())
                else:
                    _body.insert(1, b"/")
                body = b"".join(_body)

        return super().request(
            method, url, body, headers,
            chunked=chunked, preload_content=preload_content,
            decode_content=decode_content, enforce_content_length=enforce_content_length
        )

    def putrequest(
            self,
            method: str,
            url: str,
            skip_host: bool = False,
            skip_accept_encoding: bool = False,
    ) -> None:
        if self.__method != __title__:
            return super().putrequest(
                method, url,
                skip_host=skip_host, skip_accept_encoding=skip_accept_encoding
            )

        if self._HTTPConnection__response and self._HTTPConnection__response.isclosed():
            self._HTTPConnection__response = None

        if self._HTTPConnection__state == client._CS_IDLE:
            self._HTTPConnection__state = client._CS_REQ_STARTED
        else:
            raise client.CannotSendRequest(self._HTTPConnection__state)

    def putheader(self, header: str, *values: str) -> None:
        if self.__method != __title__:
            return super().putheader(header, *values)

        if self._HTTPConnection__state != client._CS_REQ_STARTED:
            raise client.CannotSendHeader()

    def endheaders(self, message_body=None, **kwargs):
        if self.__method != __title__:
            return super().endheaders(message_body=message_body, **kwargs)

        if self._HTTPConnection__state == client._CS_REQ_STARTED:
            self._HTTPConnection__state = client._CS_REQ_SENT
        else:
            raise client.CannotSendHeader()


class RawHTTPSConnection(RawHTTPConnection, HTTPSConnection):
    pass
