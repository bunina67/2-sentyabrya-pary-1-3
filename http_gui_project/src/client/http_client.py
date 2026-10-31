import socket
from abc import ABC, abstractmethod
from ..http.url import Url, ParseError
from ..http.request import Request
from ..http.parser import Parser
from ..http.serializer import Serializer
from ..http.response import Response
from ..net.tcp_client import TcpClient

class HttpTransport(ABC):
    @abstractmethod
    def get(self, url: str, headers=None) -> Response: ...
    @abstractmethod
    def post(self, url: str, body: bytes, content_type: str, headers=None) -> Response: ...

class HttpClient(HttpTransport):
    def __init__(self, timeout_ms=5000): self.timeout_ms = timeout_ms
    def set_timeout(self, ms: int):
        if ms <= 0: raise ValueError("Таймаут должен быть положительным")
        self.timeout_ms = ms
    def _request(self, method, url_text, body=b"", content_type=None, headers=None):
        url = Url.parse(url_text); request_headers = dict(headers or {})
        if not any(k.lower()=="host" for k in request_headers): request_headers["Host"] = url.host
        if body and content_type and not any(k.lower()=="content-type" for k in request_headers): request_headers["Content-Type"] = content_type
        request = Request(method, url.target, "HTTP/1.1", request_headers, body)
        payload = Serializer.serialize_request(request)
        try: raw = TcpClient(self.timeout_ms).exchange(url, payload)
        except socket.timeout as exc: raise TimeoutError("Истекло время ожидания соединения") from exc
        except OSError as exc: raise ConnectionError(f"Ошибка соединения: {exc}") from exc
        return Parser.parse_response(raw)
    def get(self, url: str, headers=None) -> Response: return self._request("GET", url, headers=headers)
    def post(self, url: str, body: bytes, content_type: str="text/plain", headers=None) -> Response:
        return self._request("POST", url, body, content_type, headers)
