---
title: 複数のコンテナをまとめて動かす
description: docker compose で、データベースとその管理画面を一度に起動する
sidebar:
  order: 2
---

## このページでできるようになること

- compose のファイルを読んで、何が動くのかを説明できる
- `docker compose` で、複数のコンテナをまとめて起動し、止められる
- コンテナどうしが、名前で互いにつながることを確かめられる

かかる時間の目安は40分です。

## 始める前に

レッスン4-1（コンテナを動かす）を終えている必要があります。

## なぜこれを覚えるのか

実際のアプリは1つのコンテナでは動きません。画面、API、データベースのように、いくつものコンテナが組み合わさって動きます。それぞれを `docker run` で長いコマンドを打って動かすのは大変ですし、打ち間違いも起きます。

docker compose はどのコンテナをどう動かすかを1つのファイルに書いておき、1回のコマンドでまとめて動かす仕組みです。ファイルを共有すれば、チームの全員が同じ組み合わせを動かせます。

## compose のファイルを書く

練習用のフォルダを作ります。

```bash
mkdir -p ~/practice/compose1
cd ~/practice/compose1
touch compose.yaml
code compose.yaml
```

`compose.yaml` に、次の内容を書いて保存します。

```yaml
services:
  db:
    image: postgres:17
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: practice
  adminer:
    image: adminer
    ports:
      - "8080:8080"
    depends_on:
      - db
```

:::caution[行の頭の空白をそろえる]
このファイルの書き方（YAML）では、行の頭の空白の数で、どこが何の中身なのかを表します。空白はスペースで入れ、上の例とそろえてください。
:::

## ファイルを読む

このファイルは2つのコンテナ（compose では「サービス」と呼びます）を動かすように書いています。

- `db`：データベースの PostgreSQL。`postgres:17` は「postgres のイメージの、バージョン17」という意味です。`environment` で、最初に作る利用者の名前（`app`）、パスワード（`secret`）、データベースの名前（`practice`）を指定しています。
- `adminer`：ブラウザからデータベースの中身を見るための管理画面。パソコンの8080番のポートにつないでいます。`depends_on` は「`db` を先に動かしてから動かす」という意味です。

`db` には `ports` を書いていません。データベースはパソコンのブラウザから直接使うものではないからです。`adminer` からだけつながれば足ります。

:::note
パスワードの `secret` は練習用です。本物のアプリでは推測されにくいパスワードを使い、Git で記録するファイルには書きません。
:::

## まとめて動かす：docker compose up

```bash
docker compose up -d
```

初めてのときはイメージを取ってくるので、少し時間がかかります。終わったら、動いているものを見ます。

```bash
docker compose ps
```

`db` と `adminer` の2つが並び、どちらも `Up` になっていれば動いています。

## 管理画面からデータベースにつなぐ

ブラウザで `http://localhost:8080` を開くと、Adminer のログイン画面が出ます。次のように入れて、ログインします。

| 項目 | 入れるもの |
| --- | --- |
| データベース種類（System） | PostgreSQL |
| サーバ（Server） | `db` |
| ユーザ名（Username） | `app` |
| パスワード（Password） | `secret` |
| データベース（Database） | `practice` |

ログインできると、`practice` データベースの画面が出ます。まだ何も入っていません。

「サーバ」には `db` と入れました。compose で一緒に動かしたコンテナどうしは、compose のファイルに書いたサービスの名前で、互いにつながれます。`adminer` のコンテナから見ると、データベースは `db` という名前の相手です。

## ログを見る

```bash
docker compose logs db
```

`db` のコンテナのログが出ます。最後の方に、次の1行があれば、データベースが準備できています。

```text
database system is ready to accept connections
```

サービスの名前を付けずに `docker compose logs` と打つと、すべてのコンテナのログがまとめて出ます。

## まとめて止める：docker compose down

```bash
docker compose down
```

2つのコンテナが止まり、消えます。`docker compose ps` を打つと、一覧が空になっています。

:::note
`docker compose` のコマンドは `compose.yaml` のあるフォルダで打ちます。別のフォルダで打つと、「no configuration file provided」と出ます。
:::

## 困ったとき

- **「yaml: line …」のようなエラーが出た**：`compose.yaml` の書き方が崩れています。行の頭の空白の数と、`:` の後ろの空白を確かめてください。
- **Adminer で「接続できません」のように出た**：「サーバ」に `db` と入れたか確かめてください。動かしてすぐは、データベースの準備が終わっていないこともあります。少し待ってから試してください。
- **「port is already allocated」と出た**：レッスン4-1の nginx のコンテナが8080番を使ったままかもしれません。`docker ps` で確かめて、止めてください。

## 確かめよう

1. `compose.yaml` の `adminer` のポートを、`"8090:8080"` に書き換えて保存する
2. `docker compose up -d` で動かし、`docker compose ps` で2つが動いていることを確かめる
3. ブラウザで `http://localhost:8090` を開き、Adminer から `practice` データベースにログインする
4. `docker compose down` で止める

3でログインでき、4の後の `docker compose ps` で一覧が空になれば完了です。確かめたら、ポートを `"8080:8080"` に戻しておいてください。次のレッスンでも、このファイルを使います。

## 今は知らなくてよいこと

- 自分で作ったアプリのイメージを compose で動かす方法
- パスワードなどを Git で記録するファイルに書かずに渡す方法（レッスン10-2で扱います）

## 次のレッスン

次は、コンテナを消してもデータベースの中身が消えないようにする方法を学びます。
