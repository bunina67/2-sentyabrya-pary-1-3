import socket
import ssl
from ..http.url import Url
from .socket_wrapper import Socket

class TcpClient:
    def __init__(self, timeout_ms=5000): self.timeout_ms = timeout_ms
    def exchange(self, url: Url, payload: bytes) -> bytes:
        timeout = max(self.timeout_ms, 1) / 1000
        with Socket(socket.create_connection((url.host, url.port), timeout=timeout)) as wrapped:
            sock = wrapped.raw; sock.settimeout(timeout)
            if url.scheme == "https":
                context = ssl.create_default_context()
                # Replace wrapper's raw socket with the TLS-wrapped connection.
                tls_sock = context.wrap_socket(sock, server_hostname=url.host)
                wrapped._sock = tls_sock; sock = tls_sock
            sock.sendall(payload)
            chunks = []; total = 0; header_end = -1; expected = None; chunked = False
            while True:
                try: data = sock.recv(65536)
                except socket.timeout as exc: raise TimeoutError("Истекло время ожидания HTTP-ответа") from exc
                if not data: break
                chunks.append(data); total += len(data)
                joined = b"".join(chunks)
                if header_end < 0:
                    header_end = joined.find(b"\r\n\r\n")
                    if header_end >= 0:
                        head = joined[:header_end].lower()
                        for line in head.split(b"\r\n")[1:]:
                            if line.startswith(b"content-length:"):
                                try: expected = int(line.split(b":",1)[1].strip())
                                except ValueError: expected = None
                            if line.startswith(b"transfer-encoding:") and b"chunked" in line: chunked = True
                if header_end >= 0 and expected is not None and total >= header_end + 4 + expected: break
                if total > 20_000_000: raise ConnectionError("Ответ превышает лимит 20 МБ")
                if header_end >= 0 and not chunked and expected is None and b"connection: close" in joined[:header_end].lower():
                    continue
            return b"".join(chunks)
