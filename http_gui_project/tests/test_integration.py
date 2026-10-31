import socket, threading, time, unittest
from src.server.http_server import HttpServer
from src.client.http_client import HttpClient

class IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        probe=socket.socket(); probe.bind(("127.0.0.1",0)); cls.port=probe.getsockname()[1]; probe.close()
        cls.server=HttpServer(); cls.server.start(port=cls.port); time.sleep(.1); cls.client=HttpClient(2000); cls.base=f"http://127.0.0.1:{cls.port}"
    @classmethod
    def tearDownClass(cls): cls.server.stop()
    def test_get_hello(self):
        r=self.client.get(self.base+"/"); self.assertEqual(r.status,200); self.assertIn(b"Hello",r.body)
    def test_post_echo(self):
        r=self.client.post(self.base+"/echo",b"abc","text/plain"); self.assertEqual(r.body,b"abc"); self.assertEqual(r.status,200)
    def test_status_404(self): self.assertEqual(self.client.get(self.base+"/status/404").status,404)
    def test_unknown_route(self): self.assertEqual(self.client.get(self.base+"/nonexistent").status,404)
    def test_100_gets(self):
        for _ in range(100): self.assertEqual(self.client.get(self.base+"/").status,200)
    def test_time_json(self): self.assertIn(b'"time"',self.client.get(self.base+"/time").body)
    def test_headers_json(self): self.assertIn(b"Host",self.client.get(self.base+"/headers").body)
    def test_keep_alive_three_requests(self):
        with socket.create_connection(("127.0.0.1", self.port), timeout=2) as sock:
            sock.settimeout(2)
            for index in range(3):
                connection = "keep-alive" if index < 2 else "close"
                sock.sendall(f"GET / HTTP/1.1\r\nHost: localhost\r\nConnection: {connection}\r\n\r\n".encode())
                data=bytearray()
                while b"\r\n\r\n" not in data:
                    data.extend(sock.recv(4096))
                split=data.find(b"\r\n\r\n")+4
                head=bytes(data[:split]); body=bytes(data[split:])
                import re
                match=re.search(br"(?im)^Content-Length: (\d+)",head)
                self.assertIsNotNone(match)
                length=int(match.group(1))
                while len(body)<length: body += sock.recv(4096)
                self.assertIn(b"200 OK",head)
                self.assertIn(b"Hello",body[:length])
                self.assertEqual(b"keep-alive" in head.lower(), index < 2)
    def test_parallel_gets(self):
        statuses=[]; lock=threading.Lock()
        def work():
            status=self.client.get(self.base+"/").status
            with lock: statuses.append(status)
        threads=[threading.Thread(target=work) for _ in range(10)]
        [t.start() for t in threads]; [t.join() for t in threads]
        self.assertEqual(statuses,[200]*10)
