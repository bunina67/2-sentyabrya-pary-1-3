"""Bounded HTTP/1.x message parser."""
import re
from .request import Request
from .response import Response
from .url import ParseError

REASONS = {200:"OK", 201:"Created", 204:"No Content", 301:"Moved Permanently", 302:"Found", 400:"Bad Request", 404:"Not Found", 418:"I'm a teapot", 500:"Internal Server Error", 501:"Not Implemented"}
MAX_HEADER = 8192

def _split_head(raw: bytes):
    if len(raw) > MAX_HEADER and b"\r\n\r\n" not in raw[:MAX_HEADER]:
        raise ParseError("HTTP-заголовки превышают 8 КБ")
    marker = raw.find(b"\r\n\r\n")
    if marker < 0:
        raise ParseError("Не найден разделитель заголовков HTTP")
    head, body = raw[:marker], raw[marker+4:]
    try:
        lines = head.decode("iso-8859-1").split("\r\n")
    except UnicodeDecodeError as exc:
        raise ParseError("Некорректная кодировка заголовков") from exc
    return lines, body

def parse_headers(lines):
    headers = {}
    for line in lines:
        if not line or line[0] in " \t" or ":" not in line:
            raise ParseError("Некорректный HTTP-заголовок")
        name, value = line.split(":", 1)
        name = name.strip()
        if not name or not re.fullmatch(r"[!#$%&'*+.^_`|~0-9A-Za-z-]+", name):
            raise ParseError("Некорректное имя заголовка")
        if any(ord(c) < 32 and c != "\t" for c in value):
            raise ParseError("Недопустимый символ в заголовке")
        headers[name] = value.strip()
    return headers

class Parser:
    @staticmethod
    def parse_request(raw: bytes) -> Request:
        lines, body = _split_head(raw)
        match = re.fullmatch(r"([A-Z]+) ([^ ]+) (HTTP/1\.[01])", lines[0])
        if not match:
            raise ParseError("Некорректная стартовая строка запроса")
        method, path, version = match.groups()
        headers = parse_headers(lines[1:])
        if version == "HTTP/1.1" and "host" not in {k.lower() for k in headers}:
            raise ParseError("Для HTTP/1.1 обязателен заголовок Host")
        lower = {k.lower(): v for k, v in headers.items()}
        if "transfer-encoding" in lower and "content-length" in lower:
            raise ParseError("Нельзя одновременно передавать Content-Length и Transfer-Encoding")
        if "transfer-encoding" in lower and lower["transfer-encoding"].lower() == "chunked":
            body = Parser.decode_chunked(body)
        elif "content-length" in lower:
            try: length = int(lower["content-length"])
            except ValueError as exc: raise ParseError("Некорректный Content-Length") from exc
            if length < 0 or length > 10_000_000: raise ParseError("Недопустимый размер тела")
            if len(body) < length: raise ParseError("Тело запроса обрезано")
            body = body[:length]
        elif "transfer-encoding" in lower:
            raise ParseError("Неподдерживаемый Transfer-Encoding")
        return Request(method, path, version, headers, body)

    @staticmethod
    def parse_response(raw: bytes) -> Response:
        lines, body = _split_head(raw)
        match = re.fullmatch(r"(HTTP/1\.[01]) ([0-9]{3})(?: (.*))?", lines[0])
        if not match: raise ParseError("Некорректная стартовая строка ответа")
        version, status, reason = match.groups()
        headers = parse_headers(lines[1:])
        lower = {k.lower(): v for k, v in headers.items()}
        if lower.get("transfer-encoding", "").lower() == "chunked": body = Parser.decode_chunked(body)
        elif "content-length" in lower:
            try: length = int(lower["content-length"])
            except ValueError as exc: raise ParseError("Некорректный Content-Length") from exc
            if length < 0: raise ParseError("Отрицательный Content-Length")
            if len(body) < length: raise ParseError("Тело ответа обрезано")
            body = body[:length]
        return Response(int(status), reason or REASONS.get(int(status), "Unknown"), version, headers, body)

    @staticmethod
    def decode_chunked(data: bytes) -> bytes:
        result = bytearray(); pos = 0
        while True:
            end = data.find(b"\r\n", pos)
            if end < 0: raise ParseError("Обрезанный chunked-ответ")
            size_line = data[pos:end].split(b";", 1)[0]
            try: size = int(size_line.strip(), 16)
            except ValueError as exc: raise ParseError("Некорректный размер chunk") from exc
            pos = end + 2
            if size == 0:
                if data[pos:pos+2] != b"\r\n" and b"\r\n\r\n" not in data[pos:]:
                    raise ParseError("Некорректное завершение chunked-тела")
                return bytes(result)
            if size < 0 or pos + size + 2 > len(data): raise ParseError("Обрезанный chunk")
            result.extend(data[pos:pos+size]); pos += size
            if data[pos:pos+2] != b"\r\n": raise ParseError("Нет CRLF после chunk")
            pos += 2
