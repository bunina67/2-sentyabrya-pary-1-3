import json
from datetime import datetime, timezone
from ..http.response import Response

def hello(req):
    body = b"<!doctype html><html><body><h1>Hello</h1></body></html>"
    return Response(200, "OK", headers={"Content-Type":"text/html; charset=utf-8"}, body=body)

def echo(req):
    content_type = next((v for k,v in req.headers.items() if k.lower()=="content-type"), "application/octet-stream")
    return Response(200, "OK", headers={"Content-Type":content_type}, body=req.body)

def current_time(req):
    body = json.dumps({"time":datetime.now(timezone.utc).isoformat()}, ensure_ascii=False).encode()
    return Response(200, "OK", headers={"Content-Type":"application/json; charset=utf-8"}, body=body)

def request_headers(req):
    body = json.dumps(req.headers, ensure_ascii=False, indent=2).encode()
    return Response(200, "OK", headers={"Content-Type":"application/json; charset=utf-8"}, body=body)
