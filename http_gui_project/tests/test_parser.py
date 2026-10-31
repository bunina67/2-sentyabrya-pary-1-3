import unittest
from src.http.parser import Parser
from src.http.url import ParseError
from src.http.request import Request
from src.http.response import Response
from src.http.serializer import Serializer

class ParserTests(unittest.TestCase):
    def test_basic_request(self):
        r=Parser.parse_request(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"); self.assertEqual((r.method,r.path),("GET","/"))
    def test_request_body(self):
        r=Parser.parse_request(b"POST / HTTP/1.1\r\nHost: x\r\nContent-Length: 3\r\n\r\nabc"); self.assertEqual(r.body,b"abc")
    def test_missing_host(self):
        with self.assertRaises(ParseError): Parser.parse_request(b"GET / HTTP/1.1\r\n\r\n")
    def test_bad_start_line(self):
        with self.assertRaises(ParseError): Parser.parse_request(b"GARBAGE\r\n\r\n")
    def test_missing_separator(self):
        with self.assertRaises(ParseError): Parser.parse_request(b"GET / HTTP/1.1\r\nHost: x")
    def test_invalid_header(self):
        with self.assertRaises(ParseError): Parser.parse_request(b"GET / HTTP/1.1\r\nHost localhost\r\n\r\n")
    def test_bad_length(self):
        with self.assertRaises(ParseError): Parser.parse_request(b"POST / HTTP/1.1\r\nHost: x\r\nContent-Length: abc\r\n\r\nx")
    def test_chunked(self):
        raw=b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n3\r\nabc\r\n0\r\n\r\n"
        self.assertEqual(Parser.parse_response(raw).body,b"abc")
    def test_response_length(self):
        r=Parser.parse_response(b"HTTP/1.1 200 OK\r\nContent-Length: 3\r\n\r\nabcEXTRA"); self.assertEqual(r.body,b"abc")
    def test_header_limit(self):
        with self.assertRaises(ParseError): Parser.parse_request(b"GET / HTTP/1.1\r\nX: "+b"a"*9000)
    def test_conflicting_framing_headers(self):
        raw=b"POST / HTTP/1.1\r\nHost: x\r\nContent-Length: 3\r\nTransfer-Encoding: chunked\r\n\r\nabc"
        with self.assertRaises(ParseError): Parser.parse_request(raw)
    def test_serializer_request_terminator(self):
        data=Serializer.serialize_request(Request("GET","/",headers={"Host":"x"})); self.assertIn(b"\r\n\r\n",data)
    def test_serializer_response_length(self):
        data=Serializer.serialize_response(Response(200,body=b"abc")); self.assertIn(b"Content-Length: 3",data)
    def test_parse_response(self):
        r=Parser.parse_response(b"HTTP/1.1 418 I'm a teapot\r\nContent-Length: 1\r\n\r\nx"); self.assertEqual(r.status,418)
