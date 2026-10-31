from typing import Callable, Dict, Tuple
from abc import ABC, abstractmethod
from ..http.request import Request
from ..http.response import Response
from .handlers import hello, echo, current_time, request_headers

Handler = Callable[[Request], Response]
class RouterInterface(ABC):
    @abstractmethod
    def dispatch(self, req: Request) -> Response: ...

class Router(RouterInterface):
    def __init__(self):
        self._routes: Dict[Tuple[str,str], Handler] = {
            ("GET", "/"): hello, ("POST", "/echo"): echo,
            ("GET", "/time"): current_time, ("GET", "/headers"): request_headers,
        }
    def route(self, method: str, path: str, handler: Handler): self._routes[(method.upper(), path)] = handler
    def dispatch(self, req: Request) -> Response:
        path = req.path.split("?", 1)[0]
        handler = self._routes.get((req.method.upper(), path))
        if handler: return handler(req)
        if req.method.upper() == "GET" and path.startswith("/status/"):
            try:
                code = int(path.rsplit("/",1)[1])
                if 100 <= code <= 599:
                    reason = {200:"OK", 400:"Bad Request", 404:"Not Found", 418:"I'm a teapot"}.get(code, "Custom Status")
                    return Response(code, reason, body=f"HTTP status {code}".encode())
            except ValueError: pass
        return Response(404, "Not Found", headers={"Content-Type":"text/plain; charset=utf-8"}, body=b"404 Not Found")
