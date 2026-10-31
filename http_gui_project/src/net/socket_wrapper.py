import socket

class Socket:
    """Small RAII wrapper; socket is closed when leaving a with-block."""
    def __init__(self, sock: socket.socket): self._sock = sock
    def __enter__(self): return self
    def __exit__(self, exc_type, exc, tb): self.close(); return False
    def close(self):
        if self._sock is not None:
            try: self._sock.shutdown(socket.SHUT_RDWR)
            except OSError: pass
            self._sock.close(); self._sock = None
    def send_all(self, data: bytes): self._sock.sendall(data)
    def recv(self, n: int) -> bytes: return self._sock.recv(n)
    @property
    def raw(self): return self._sock
