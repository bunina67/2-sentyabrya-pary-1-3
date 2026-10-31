import logging, socket, threading, time
from abc import ABC, abstractmethod
from ..http.parser import Parser
from ..http.serializer import Serializer
from ..http.response import Response
from ..http.url import ParseError
from .router import Router

class ServerInterface(ABC):
    @abstractmethod
    def start(self, host="127.0.0.1", port=8080): ...
    @abstractmethod
    def stop(self): ...

class HttpServer(ServerInterface):
    def __init__(self, logger=None, on_log=None):
        self.logger = logger or logging.getLogger("http_gui")
        self.on_log = on_log
        self.router = Router(); self._sock = None; self._thread = None
        self._stop = threading.Event(); self.port = 8080; self.host = "127.0.0.1"
        self._clients = set(); self._lock = threading.Lock()
    @property
    def running(self): return self._thread is not None and self._thread.is_alive() and not self._stop.is_set()
    def start(self, host="127.0.0.1", port=8080):
        if not 1 <= int(port) <= 65535: raise ValueError("Порт должен быть в диапазоне 1–65535")
        if self.running: raise RuntimeError("Сервер уже запущен")
        self.host, self.port = host, int(port); self._stop.clear()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM); sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port)); sock.listen(64); sock.settimeout(0.3); self._sock = sock
        self._thread = threading.Thread(target=self._serve, name="HttpServer", daemon=True); self._thread.start()
    def _serve(self):
        while not self._stop.is_set():
            try: conn, addr = self._sock.accept()
            except socket.timeout: continue
            except OSError:
                if self._stop.is_set(): break
                self.logger.exception("Ошибка accept"); continue
            with self._lock: self._clients.add(conn)
            threading.Thread(target=self._handle, args=(conn, addr), daemon=True).start()
    def _handle(self, conn, addr):
        buffer = bytearray()
        try:
            with conn:
                conn.settimeout(3)
                while not self._stop.is_set():
                    start = time.perf_counter(); method = "?"; path = "?"; status = 400
                    try:
                        while b"\r\n\r\n" not in buffer:
                            chunk = conn.recv(4096)
                            if not chunk:
                                return
                            buffer.extend(chunk)
                            if len(buffer) > 8192:
                                raise ParseError("Заголовки превышают 8 КБ")
                        header_end = buffer.find(b"\r\n\r\n") + 4
                        header = bytes(buffer[:header_end])
                        try:
                            header_lines = header.decode("iso-8859-1").split("\r\n")
                            lengths = [line.split(":", 1)[1].strip() for line in header_lines[1:]
                                       if ":" in line and line.split(":", 1)[0].lower() == "content-length"]
                            length = int(lengths[-1]) if lengths else 0
                        except ValueError as exc:
                            raise ParseError("Некорректный Content-Length") from exc
                        if length < 0 or length > 10_000_000:
                            raise ParseError("Недопустимый Content-Length")
                        while len(buffer) < header_end + length:
                            chunk = conn.recv(min(65536, header_end + length - len(buffer)))
                            if not chunk:
                                raise ParseError("Тело запроса обрезано")
                            buffer.extend(chunk)
                        raw = bytes(buffer[:header_end + length])
                        del buffer[:header_end + length]
                        request = Parser.parse_request(raw)
                        method, path = request.method, request.path
                        response = self.router.dispatch(request)
                        connection_value = next((v.lower() for k, v in request.headers.items()
                                                  if k.lower() == "connection"), "")
                        keep_alive = (request.version == "HTTP/1.1" and connection_value != "close") or connection_value == "keep-alive"
                        response.headers["Connection"] = "keep-alive" if keep_alive else "close"
                        status = response.status
                        conn.sendall(Serializer.serialize_response(response))
                        elapsed = (time.perf_counter() - start) * 1000
                        message = {"time": time.strftime("%H:%M:%S"), "method": method, "path": path,
                                   "status": status, "ms": round(elapsed, 2)}
                        self.logger.info("%s %s -> %s (%.2f ms)", method, path, status, elapsed)
                        if self.on_log:
                            try: self.on_log(message)
                            except Exception: self.logger.exception("Не удалось передать запись в GUI")
                        if not keep_alive:
                            return
                    except (ParseError, UnicodeError, ValueError, socket.timeout) as exc:
                        try:
                            payload = Serializer.serialize_response(Response(400, "Bad Request", headers={"Connection": "close"}, body=("400 Bad Request: " + str(exc)).encode("utf-8")))
                            conn.sendall(payload)
                        except OSError:
                            pass
                        self.logger.warning("Некорректный запрос от %s: %s", addr, exc)
                        return
        except OSError as exc:
            self.logger.debug("Соединение %s завершено: %s", addr, exc)
        finally:
            with self._lock:
                self._clients.discard(conn)
    def stop(self):
        self._stop.set()
        if self._sock:
            try: self._sock.close()
            except OSError: pass
            self._sock = None
        with self._lock: clients = list(self._clients)
        for client in clients:
            try: client.shutdown(socket.SHUT_RDWR)
            except OSError: pass
            try: client.close()
            except OSError: pass
        if self._thread and self._thread is not threading.current_thread(): self._thread.join(timeout=2)
        self._thread = None
