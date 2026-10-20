# 練習用の小さな Web サーバー（第3部で使います）
# 起動：python3 webdemo.py   止める：Ctrl+C
import json
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

FORM_PAGE = """<!doctype html>
<html lang="ja"><meta charset="utf-8"><title>フォームの練習</title>
<h1>フォームの練習</h1>
<h2>GET で送る</h2>
<form method="get" action="/hello">
  <input name="name" placeholder="名前"> <button>送る</button>
</form>
<h2>POST で送る</h2>
<form method="post" action="/hello">
  <input name="name" placeholder="名前"> <button>送る</button>
</form>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def send_text(self, status, body, content_type="text/html; charset=utf-8", headers=None):
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(data)

    def send_json(self, status, obj):
        self.send_text(status, json.dumps(obj, ensure_ascii=False), "application/json; charset=utf-8")

    def read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length).decode("utf-8")

    def current_user(self):
        cookie = SimpleCookie(self.headers.get("Cookie", ""))
        return cookie["user"].value if "user" in cookie else None

    def do_GET(self):
        url = urlparse(self.path)
        query = parse_qs(url.query)
        if url.path == "/":
            self.send_text(200, FORM_PAGE)
        elif url.path == "/hello":
            name = query.get("name", ["名無し"])[0]
            self.send_text(200, f"<p>こんにちは、{name}さん（GET で受け取りました）</p>")
        elif url.path == "/api/hello":
            name = query.get("name", ["名無し"])[0]
            self.send_json(200, {"message": f"こんにちは、{name}さん", "method": "GET"})
        elif url.path == "/me":
            user = self.current_user()
            if user:
                self.send_text(200, f"<p>ログイン中：{user}さん</p><p><a href='/logout'>ログアウト</a></p>")
            else:
                self.send_text(200, "<p>ログインしていません</p><p><a href='/login?user=yachiyo'>yachiyo としてログイン</a></p>")
        elif url.path == "/login":
            user = query.get("user", ["yachiyo"])[0]
            self.send_text(200, f"<p>{user}さんとしてログインしました</p><p><a href='/me'>確かめる</a></p>",
                           headers={"Set-Cookie": f"user={user}; Path=/"})
        elif url.path == "/logout":
            self.send_text(200, "<p>ログアウトしました</p><p><a href='/me'>確かめる</a></p>",
                           headers={"Set-Cookie": "user=; Path=/; Max-Age=0"})
        else:
            self.send_text(404, "<p>そのページはありません</p>")

    def do_POST(self):
        url = urlparse(self.path)
        body = self.read_body()
        if url.path == "/hello":
            name = parse_qs(body).get("name", ["名無し"])[0]
            self.send_text(200, f"<p>こんにちは、{name}さん（POST で受け取りました）</p>")
        elif url.path == "/api/hello":
            try:
                data = json.loads(body or "{}")
            except json.JSONDecodeError:
                self.send_json(400, {"error": "JSON として読めませんでした"})
                return
            name = data.get("name", "名無し")
            self.send_json(201, {"message": f"こんにちは、{name}さん", "method": "POST"})
        else:
            self.send_text(404, "<p>そのページはありません</p>")


if __name__ == "__main__":
    print("http://localhost:8000 で待っています（止めるときは Ctrl+C）")
    HTTPServer(("", 8000), Handler).serve_forever()
