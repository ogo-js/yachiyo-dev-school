---
title: データを残す
description: コンテナを消してもデータベースの中身が残るように、ボリュームを使う
sidebar:
  order: 3
---

## このページでできるようになること

- コンテナの中にコマンドを送って、データベースを操作できる
- コンテナを消すと中のデータも消えることを、自分で確かめられる
- ボリュームを使って、データを残せる

かかる時間の目安は30分です。

## 始める前に

レッスン4-2（複数のコンテナをまとめて動かす）を終え、`~/practice/compose1/compose.yaml` ができている必要があります。

## なぜこれを覚えるのか

コンテナは、消して作り直すのが当たり前の使い方です。イメージのバージョンを上げるときも、設定を変えるときも、コンテナは作り直します。

ところが、コンテナの中に保存したデータは、コンテナと一緒に消えます。データベースの中身が作り直すたびに消えてしまっては困ります。そこで使うのが「ボリューム」です。

## コンテナにコマンドを送る：docker compose exec

データベースを動かします。

```bash
cd ~/practice/compose1
docker compose up -d
```

`docker compose up -d` はコンテナを動かし始めたところで終わります。中のデータベースが使えるようになるのは、その数秒後です。数秒待ってから、次へ進んでください。

:::note
データベースの準備が終わる前に操作すると、次のどちらかが出ます。数秒待ってから、打ち直してください。

- `FATAL:  the database system is starting up`
- `connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: No such file or directory`
:::

`db` のコンテナの中で、PostgreSQL を操作するコマンド（`psql`）を動かして、表を1つ作ります。

```bash
docker compose exec db psql -U app -d practice -c "CREATE TABLE memo (body text);"
```

```text
CREATE TABLE
```

`docker compose exec db` は「`db` のコンテナの中で、続くコマンドを動かす」という意味です。`-U app` は利用者、`-d practice` はデータベース、`-c` の後ろが送る命令です。命令の中身（SQL）は第5部で学びます。

続けて、表に1行入れて、中身を見ます。

```bash
docker compose exec db psql -U app -d practice -c "INSERT INTO memo VALUES ('こんにちは');"
docker compose exec db psql -U app -d practice -c "SELECT * FROM memo;"
```

```text
INSERT 0 1
    body
------------
 こんにちは
(1 row)
```

「こんにちは」が保存されています。

## コンテナを消すと、データも消える

コンテナを消して、作り直します。

```bash
docker compose down
docker compose up -d
```

数秒待ってから、もう一度、中身を見ます。

```bash
docker compose exec db psql -U app -d practice -c "SELECT * FROM memo;"
```

```text
ERROR:  relation "memo" does not exist
LINE 1: SELECT * FROM memo;
                      ^
```

「`memo` という表がない」と言われました。表もデータも消したコンテナと一緒に消えています。

## ボリュームを使う

ボリュームは、Docker が管理する、コンテナの外にあるデータの置き場所です。コンテナの中のフォルダとつないでおくと、そのフォルダに書いたものはボリュームに保存され、コンテナを消しても残ります。

`compose.yaml` を、次のように書き換えて保存します。増えたのは、`db` の中の `volumes` の2行と、ファイルの最後の `volumes` の2行です。

```yaml
services:
  db:
    image: postgres:17
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: practice
    volumes:
      - db-data:/var/lib/postgresql/data
  adminer:
    image: adminer
    ports:
      - "8080:8080"
    depends_on:
      - db

volumes:
  db-data:
```

- 最後の `volumes:` と `db-data:`：`db-data` という名前のボリュームを用意する
- `db` の中の `- db-data:/var/lib/postgresql/data`：`db-data` を、コンテナの中の `/var/lib/postgresql/data` につなぐ。ここは PostgreSQL がデータを保存するフォルダです

## データが残ることを確かめる

書き換えた設定で動かし直します。

```bash
docker compose down
docker compose up -d
```

数秒待ってから、もう一度、表を作って1行入れます。

```bash
docker compose exec db psql -U app -d practice -c "CREATE TABLE memo (body text);"
docker compose exec db psql -U app -d practice -c "INSERT INTO memo VALUES ('こんにちは');"
```

コンテナを消して、作り直します。

```bash
docker compose down
docker compose up -d
```

数秒待ってから、中身を見ます。

```bash
docker compose exec db psql -U app -d practice -c "SELECT * FROM memo;"
```

```text
    body
------------
 こんにちは
(1 row)
```

今度は、コンテナを作り直しても「こんにちは」が残っています。

手元にあるボリュームは次のコマンドで見られます。

```bash
docker volume ls
```

`compose1_db-data` のように、フォルダの名前が頭に付いた名前で並んでいます。

## ボリュームごと消す

データベースを空から作り直したいときは、ボリュームも消します。

:::danger[ボリュームを消すと、データは戻せません]
`docker compose down -v` の `-v` は「ボリュームも消す」という意味です。消したデータは元に戻せません。本当に消してよいデータかを確かめてから使ってください。
:::

```bash
docker compose down -v
```

## 困ったとき

- **「service "db" is not running」と出た**：コンテナが動いていません。`docker compose up -d` で動かしてから打ってください。
- **`CREATE TABLE` で「already exists」と出た**：同じ名前の表がもうあります。ボリュームでデータが残っているので、作り直す必要はありません。

## 確かめよう

1. `docker compose up -d` で動かし、数秒待ってから `memo` の表に「さようなら」の行を足す
2. `docker compose down` で止めて消し、`docker compose up -d` で作り直す
3. 数秒待ってから、`memo` の表の中身を見る

3で「こんにちは」と「さようなら」の2行が出れば完了です。確かめたら、`docker compose down` で止めておきます。データは次の部で使うので、`-v` は付けないでください。

## 今は知らなくてよいこと

- パソコンのフォルダを直接コンテナにつなぐ方法（バインドマウント）
- ボリュームのデータを別の場所に控えておく方法

## 次のレッスン

これで第4部は終わりです。次からは第5部です。このデータベースを使って、SQL でデータを読み書きします。
