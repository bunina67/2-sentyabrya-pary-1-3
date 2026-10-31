"""URL parsing for the raw-socket HTTP client."""
from dataclasses import dataclass
from urllib.parse import urlsplit

class ParseError(ValueError):
    """Raised when a URL or HTTP message cannot be parsed safely."""

@dataclass(frozen=True)
class Url:
    scheme: str
    host: str
    port: int
    path: str
    query: str = ""

    @property
    def target(self) -> str:
        return self.path + (f"?{self.query}" if self.query else "")

    @classmethod
    def parse(cls, value: str) -> "Url":
        if not isinstance(value, str) or not value.strip():
            raise ParseError("URL не должен быть пустым")
        try:
            parts = urlsplit(value.strip())
            scheme = parts.scheme.lower()
            if scheme not in ("http", "https"):
                raise ParseError("Поддерживаются только http:// и https://")
            if not parts.hostname:
                raise ParseError("В URL отсутствует имя хоста")
            if parts.username is not None or parts.password is not None:
                raise ParseError("URL с логином и паролем не поддерживается")
            port = parts.port or (443 if scheme == "https" else 80)
            if not 1 <= port <= 65535:
                raise ParseError("Порт должен быть в диапазоне 1–65535")
            path = parts.path or "/"
            return cls(scheme, parts.hostname, port, path, parts.query)
        except ValueError as exc:
            if isinstance(exc, ParseError):
                raise
            raise ParseError(f"Некорректный URL: {exc}") from exc
