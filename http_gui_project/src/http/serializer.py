from datetime import datetime, timezone
from email.utils import format_datetime
from .request import Request
from .response import Response
from .parser import REASONS

class Serializer:
    @staticmethod
    def serialize_request(request: Request) -> bytes:
        headers = dict(request.headers)
        lower = {k.lower() for k in headers}
        headers.setdefault("Host", "localhost")
        headers.setdefault("Connection", "close")
        headers.setdefault("Content-Length", str(len(request.body)))
        head = f"{request.method.upper()} {request.path} {request.version}\r\n" + "".join(f"{k}: {v}\r\n" for k,v in headers.items()) + "\r\n"
        return head.encode("iso-8859-1") + request.body

    @staticmethod
    def serialize_response(response: Response) -> bytes:
        headers = dict(response.headers)
        headers.setdefault("Content-Length", str(len(response.body)))
        headers.setdefault("Content-Type", "text/plain; charset=utf-8")
        headers.setdefault("Date", format_datetime(datetime.now(timezone.utc), usegmt=True))
        headers.setdefault("Connection", "close")
        reason = response.reason or REASONS.get(response.status, "Unknown")
        head = f"{response.version} {response.status} {reason}\r\n" + "".join(f"{k}: {v}\r\n" for k,v in headers.items()) + "\r\n"
        return head.encode("iso-8859-1") + response.body
