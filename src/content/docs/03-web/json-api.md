---
title: JSON と API
description: curl で API を呼び、返ってきた JSON を読み、JSON を送る
sidebar:
  order: 3
---

## このページでできるようになること

- curl で、コマンドからリクエストを送れる
- API が返す JSON を読める
- curl で JSON を POST で送れる

かかる時間の目安は40分です。

## 始める前に

レッスン3-2（GET と POST）を終え、`~/practice/web/webdemo.py` ができている必要があります。

## なぜこれを覚えるのか

これまでのサーバーは画面に表示するための HTML を返していました。一方で、データだけを決まった形で返すサーバーもあります。画面を持たず、プログラムから呼ばれることを前提にした窓口を「API」と呼びます。

今の Web アプリの多くは、画面を作る部分とデータを扱う部分が分かれていて、その間を API でつないでいます。API が返すデータの形として、最もよく使われているのが「JSON」です。

## ターミナルを2つ使う

1つ目のターミナルで、練習用のサーバーを動かします。

```bash
cd ~/practice/web
python3 webdemo.py
```

サーバーが動いている間、このターミナルは使えません。VS Code のターミナルの右上にある「+」を押して、2つ目のターミナルを開きます。ここから先のコマンドは2つ目のターミナルで打ちます。

## curl でリクエストを送る

`curl` は、ブラウザを使わずにリクエストを送るコマンドです。

```bash
curl "http://localhost:8000/api/hello?name=yachiyo"
```

```text
{"message": "こんにちは、yachiyoさん", "method": "GET"}
```

これが JSON です。返ってきた文の最後に改行がないので、次のプロンプトが同じ行に続いて表示されることがあります。そうなっても問題ありません。

:::tip[URL は " " で囲む]
`?` や `&` は、ターミナルにとって特別な意味を持つ記号です。URL に含まれるときは、`" "` で囲んでおくと確実です。
:::

## JSON を読む

JSON はデータを「名前」と「値」の組で表す書き方です。

```json
{"message": "こんにちは、yachiyoさん", "method": "GET"}
```

- `{ }` で囲んだものが1つのまとまり（オブジェクト）
- `"message"` が名前、`"こんにちは、yachiyoさん"` がその値
- 組と組の間は `,` で区切る

値には文字だけでなく、数、真偽（`true` か `false`）、別のまとまり、並び（配列）も入れられます。並びは `[ ]` で囲みます。

```json
{
  "name": "やちよ",
  "age": 28,
  "member": true,
  "hobbies": ["散歩", "読書"],
  "address": {"city": "千代田区"}
}
```

この例は「名前がやちよ、年齢が28、会員である、趣味は散歩と読書、住所の市区町村は千代田区」というデータを表しています。

## 返事の詳しい中身を見る：curl -i

`-i` を付けると、返事の中身の前に、ステータスコードやヘッダーも表示されます。

```bash
curl -i "http://localhost:8000/api/hello?name=yachiyo"
```

```text
HTTP/1.0 200 OK
Server: BaseHTTP/0.6 Python/3.12.3
Date: Tue, 20 Oct 2026 06:36:17 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 63

{"message": "こんにちは、yachiyoさん", "method": "GET"}
```

`Content-Type: application/json` は「返事の中身は JSON です」という意味です。Python のバージョンや日時、長さの数は、人によって違うことがあります。

## JSON を送る

API に JSON を送るときは、POST を使います。

```bash
curl -i -X POST -H "Content-Type: application/json" -d '{"name":"yachiyo"}' http://localhost:8000/api/hello
```

```text
HTTP/1.0 201 Created
…（ヘッダーは省いています）

{"message": "こんにちは、yachiyoさん", "method": "POST"}
```

それぞれの指定の意味は次のとおりです。

| 指定 | 意味 |
| --- | --- |
| `-X POST` | メソッドを POST にする |
| `-H "Content-Type: application/json"` | 「送る中身は JSON です」とサーバーに伝える |
| `-d '{"name":"yachiyo"}'` | 本文として送る中身 |

ステータスコードの `201 Created` は「受け取って、作りました」という意味です。何かを登録する API は、`200` ではなく `201` を返すことがよくあります。

## 形の崩れた JSON を送る

わざと JSON でないものを送ってみます。

```bash
curl -i -X POST -H "Content-Type: application/json" -d 'yachiyo' http://localhost:8000/api/hello
```

```text
HTTP/1.0 400 Bad Request
…（ヘッダーは省いています）

{"error": "JSON として読めませんでした"}
```

`400` は「お願いの形がおかしい」という意味でした（レッスン3-1）。API の多くは、うまくいかなかったときも JSON で理由を返します。

## 本物の API を呼ぶ

インターネット上にも、誰でも呼べる API があります。GitHub の利用者の情報を返す API を呼んでみます。

```bash
curl https://api.github.com/users/octocat
```

```json
{
  "login": "octocat",
  "id": 583231,
  …
  "name": "The Octocat",
  …
}
```

途中を省いています。名前と値の組がたくさん並んだ JSON が返ってきます。仕組みは手元の練習用のサーバーと同じです。

:::note
短い時間に何度も呼ぶと、`403` と「API rate limit exceeded」が返ってくることがあります。呼べる回数に上限があるためです。しばらく待ってから呼び直してください。
:::

## 困ったとき

- **「Failed to connect to localhost port 8000」と出た**：1つ目のターミナルでサーバーが動いていません。`python3 webdemo.py` を動かしてください。
- **「curl: command not found」と出た**：`sudo apt install curl` で入れてください。
- **`-d` で送った JSON が 400 になる**：JSON は `' '`（一重の引用符）で囲み、JSON の中の名前と文字の値は `" "` で囲みます。引用符の組み合わせを確かめてください。

## 確かめよう

1. `curl` で `http://localhost:8000/api/hello?name=tanaka` を GET で呼ぶ
2. `curl` で `{"name":"suzuki"}` を POST で送り、`-i` でステータスコードを確かめる
3. 次の JSON を読んで、「趣味の2つ目」と「住所の市区町村」を答える

```json
{"name": "やちよ", "hobbies": ["散歩", "読書", "料理"], "address": {"pref": "東京都", "city": "八王子市"}}
```

1で `こんにちは、tanakaさん` と `"method": "GET"` が、2で `201 Created` と `こんにちは、suzukiさん` が出て、3の答えが「読書」と「八王子市」なら完了です。確かめたら、1つ目のターミナルで Ctrl+C を押してサーバーを止めます。

## 今は知らなくてよいこと

- API を呼ぶときの、本人であることの伝え方（認証）
- JSON を見やすく整えて表示する道具

## 次のレッスン

次は、ログインの状態がどこに保たれているのかを見ます。
