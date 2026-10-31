import unittest
from src.http.url import Url, ParseError

class UrlTests(unittest.TestCase):
    def test_full_url(self):
        u=Url.parse("http://host:8080/path?q=1"); self.assertEqual((u.host,u.port,u.path,u.query),("host",8080,"/path","q=1"))
    def test_default_http_port(self): self.assertEqual(Url.parse("http://host/path").port,80)
    def test_default_https_port(self): self.assertEqual(Url.parse("https://host").port,443)
    def test_empty(self):
        with self.assertRaises(ParseError): Url.parse("")
    def test_garbage(self):
        with self.assertRaises(ParseError): Url.parse("garbage")
    def test_unsupported_scheme(self):
        with self.assertRaises(ParseError): Url.parse("ftp://host")
    def test_query_only(self): self.assertEqual(Url.parse("http://host?q=2").target,"/?q=2")
    def test_port_range(self):
        with self.assertRaises(ParseError): Url.parse("http://host:70000")
    def test_credentials_rejected(self):
        with self.assertRaises(ParseError): Url.parse("http://u:p@host")
