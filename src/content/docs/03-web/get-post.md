---
title: GET と POST
description: フォームの送り方の違いを、ブラウザとサーバーの両方から確かめる
sidebar:
  order: 2
---

## このページでできるようになること

- 練習用のサーバーを用意して動かせる
- フォームを GET と POST で送り、値がどこに載るかの違いを確かめられる
- GET と POST の使い分けを説明できる

かかる時間の目安は40分です。

## 始める前に

レッスン3-1（ブラウザとサーバーのやり取りを見る）を終えている必要があります。

## なぜこれを覚えるのか

リクエストには「どんな種類のお願いか」を表すメソッドが付いています。よく使うのは `GET` と `POST` の2つです。

`GET` は「ください」、`POST` は「これを受け取って」というお願いです。ページを見るだけなのか、何かを登録したり変えたりするのかで、使い分けます。この違いは後の部で画面を作るときにもそのまま出てきます。

## 練習用のサーバーを用意する

このレッスンから第3部の終わりまで、練習用の小さなサーバーを使います。

```bash
cd ~/practice/web
touch webdemo.py
code webdemo.py
```

開いたファイルに、次の内容をすべて貼り付けて保存してください。中身は今は読まなくてかまいません。

```python
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
```

保存したら、動かします。

```bash
python3 webdemo.py
```

```text
http://localhost:8000 で待っています（止めるときは Ctrl+C）
```

ブラウザで `http://localhost:8000` を開くと、「フォームの練習」のページが出ます。開発者ツールのネットワークのタブも開いておいてください。

## GET で送る

「GET で送る」の欄に「やちよ」と入れて、「送る」を押します。

「こんにちは、やちよさん（GET で受け取りました）」と表示されます。ここで、ブラウザのアドレス欄を見てください。

```text
http://localhost:8000/hello?name=やちよ
```

入れた名前が URL の `?` の後ろに載っています。この部分を「クエリ文字列」と呼びます。

ターミナルのログでは次のように見えます。

```text
127.0.0.1 - - [20/Oct/2026 15:10:00] "GET /hello?name=%E3%82%84%E3%81%A1%E3%82%88 HTTP/1.1" 200 -
```

`%E3%82%84…` は、「やちよ」を URL で送れる形に置き換えたものです。ブラウザは読みやすいように元の文字で表示していますが、実際にはこの形で送られています。

## POST で送る

ブラウザの「戻る」でフォームのページに戻り、今度は「POST で送る」の欄に「やちよ」と入れて送ります。

「こんにちは、やちよさん（POST で受け取りました）」と表示されます。アドレス欄は次のとおりです。

```text
http://localhost:8000/hello
```

名前が URL に載っていません。開発者ツールで `hello` の行を押し、「ペイロード」（Payload）のタブを開くと、次のように表示されます。

```text
name: やちよ
```

POST では、送る値は URL ではなく、リクエストの「本文」（ボディ）に載ります。ログでも、`POST /hello` の後ろに名前は出ていません。

## 使い分け

| | GET | POST |
| --- | --- | --- |
| お願いの意味 | 「ください」 | 「これを受け取って」 |
| 値が載る場所 | URL（クエリ文字列） | リクエストの本文 |
| URL をブックマークして同じ結果を出せるか | 出せる | 出せない |
| 使う場面 | 見る・探す（一覧の表示、検索） | 変える（登録、更新、削除） |

検索の条件のように、URL を他の人に送れば同じ画面を見せられるものは `GET` で送ります。データを登録したり変えたりするものは `POST` で送ります。

:::caution[パスワードは GET で送らない]
GET で送った値は URL に載るので、ブラウザの履歴やサーバーのログに残ります。パスワードのように人に見られてはいけない値は、必ず POST で送ります。
:::

## POST の後に読み込み直すと

POST で送った後の画面で、F5 キーを押してみてください。ブラウザが「フォームを再送信しますか」のように確かめてきます。

POST は「変える」お願いなので、読み込み直すと同じ登録がもう一度行われてしまうかもしれません。ブラウザはそれを心配して確かめています。ここでは「キャンセル」を選んでください。

## 困ったとき

- **「Address already in use」と出た**：レッスン3-1のサーバーが動いたままです。そちらのターミナルで Ctrl+C を押して止めてください。
- **貼り付けた後に動かすと「IndentationError」と出た**：行の頭の空白がずれています。もう一度、ファイルの中身をすべて消してから貼り付け直してください。

## 確かめよう

1. `webdemo.py` を動かし、フォームを GET と POST で1回ずつ送る
2. それぞれについて、開発者ツールでメソッドを確かめ、名前が URL とペイロードのどちらに載っているかを確かめる
3. ブラウザのアドレス欄に `http://localhost:8000/hello?name=ほげ` と直接打って開く

3で「こんにちは、ほげさん（GET で受け取りました）」と出れば完了です。フォームを使わなくても、URL を打つだけで GET のお願いが送れることが分かります。確かめたら、Ctrl+C でサーバーを止めます。

## 今は知らなくてよいこと

- `GET` と `POST` 以外のメソッド（`PUT` や `DELETE` など）
- `webdemo.py` の中身の読み方

## 次のレッスン

次は画面ではなくデータそのものを返す「API」を、ブラウザを使わずにコマンドで呼んでみます。
