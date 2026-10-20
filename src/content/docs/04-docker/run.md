---
title: コンテナを動かす
description: Docker を入れ、イメージからコンテナを起動し、止めて、消す
sidebar:
  order: 1
---

## このページでできるようになること

- WSL2 の Ubuntu に Docker を入れられる
- イメージとコンテナの違いを説明できる
- コンテナを起動し、様子を見て、止めて、消せる

かかる時間の目安は60分です。

## 始める前に

第3部（Web の仕組み）を終えている必要があります。

## なぜ Docker を使うのか

アプリを動かすには、アプリそのものの他に、決まったバージョンのデータベースや、Web サーバーや、さまざまな道具が必要です。これを人ごとに手で入れていくと、「自分のパソコンでは動くのに、あの人のパソコンでは動かない」が起きます。

Docker はアプリと、それが動くのに必要なものを1つの箱にまとめて動かす道具です。この箱を「コンテナ」と呼びます。同じ箱を使えば、誰のパソコンでも同じように動きます。

## Docker を入れる

この教材では Ubuntu の中に「Docker Engine」を入れて使います。Docker Engine は Docker の中心になる部分で、オープンソースのソフトウェアです。仕事で使う場合も含めて、無料で使えます。

:::note[Docker Desktop は使わない]
Windows 向けには、画面から操作できる「Docker Desktop」もあります。Docker Desktop は一定以上の規模の会社で使うには有料の契約が必要です。この教材のコマンドは Docker Engine だけで動きます。
:::

:::caution
すでに Docker Desktop を入れているパソコンでは、先に Docker Desktop を消すか、Docker Desktop の設定の「WSL integration」で Ubuntu との連携を切ってから進めてください。両方が同じ Ubuntu の中で動くと、どちらの Docker が使われているのか分からなくなります。
:::

Docker Engine の入れ方は時期によって細かく変わります。公式の手順に従ってください。

1. ブラウザで、Docker の公式の説明「Install Docker Engine on Ubuntu」（docs.docker.com/engine/install/ubuntu）を開きます。
2. 「Install using the apt repository」の節にあるコマンドを、上から順に1つずつターミナルに貼り付けて実行します。

続けて、`sudo` を付けなくても Docker を使えるようにします。

```bash
sudo usermod -aG docker $USER
```

この設定を効かせるには、Ubuntu を一度止める必要があります。

1. VS Code を閉じます。
2. Windows の PowerShell を開き（管理者でなくてかまいません）、`wsl --shutdown` と打ちます。
3. VS Code を開き直して、Ubuntu につなぎます。

## 入ったことを確かめる

```bash
docker run hello-world
```

いくつかの行が表示され、その中に次の1行があれば、Docker は動いています。

```text
Hello from Docker!
```

## イメージとコンテナ

さっきのコマンドの中で、Docker は2つのことをしました。

1. `hello-world` という「イメージ」をインターネットから取ってきた
2. そのイメージから「コンテナ」を作って動かした

イメージとコンテナの関係は、料理のレシピと、作った料理の関係に似ています。

| | イメージ | コンテナ |
| --- | --- | --- |
| たとえ | レシピ | レシピから作った料理 |
| 中身 | 動かすのに必要なものをまとめた「型」 | 型から作って、実際に動いているもの |
| 数 | 1つ | 同じイメージから、いくつでも作れる |

イメージは Docker Hub という場所で、さまざまな人や会社が公開しています。

## Web サーバーのコンテナを動かす

Web サーバーの nginx（エンジンエックス）を、コンテナで動かしてみます。

```bash
docker run -d -p 8080:80 --name web nginx
```

| 指定 | 意味 |
| --- | --- |
| `-d` | 裏で動かす。ターミナルはすぐに使える状態に戻る |
| `-p 8080:80` | パソコンの8080番のポートを、コンテナの中の80番のポートにつなぐ |
| `--name web` | このコンテナに `web` という名前を付ける |
| `nginx` | もとにするイメージの名前 |

ブラウザで `http://localhost:8080` を開くと、「Welcome to nginx!」というページが出ます。パソコンに nginx を入れていないのに、Web サーバーが動いています。

`-p 8080:80` の意味はレッスン3-1のポート番号を思い出すと分かります。コンテナの中の nginx は80番で待っていますが、外からは見えません。パソコンの8080番に届いたリクエストを、コンテナの80番に渡すようにつないでいます。

## 動いているコンテナを見る：docker ps

```bash
docker ps
```

```text
CONTAINER ID   IMAGE   COMMAND                  CREATED         STATUS         PORTS                  NAMES
3f2a9c1b7d4e   nginx   "/docker-entrypoint.…"   2 minutes ago   Up 2 minutes   0.0.0.0:8080->80/tcp   web
```

動いているコンテナが並びます。`NAMES` が `web`、`STATUS` が `Up`（動いている）になっています。

## ログを見る：docker logs

```bash
docker logs web
```

nginx が受け取ったリクエストの記録が出ます。レッスン3-1の Python のサーバーと同じように、`GET /` の行があるはずです。

## 止める・動かす・消す

```bash
docker stop web
docker ps
```

`docker ps` の一覧から `web` が消えます。止めただけで、コンテナはまだ残っています。止まっているものも含めて見るには、`-a` を付けます。

```bash
docker ps -a
```

`web` の `STATUS` が `Exited`（止まっている）になっています。もう一度動かすこともできます。

```bash
docker start web
```

使い終わったら、止めてから消します。

```bash
docker stop web
docker rm web
```

コンテナを消しても、もとのイメージは残っています。手元にあるイメージは `docker images` で見られます。

## 困ったとき

- **「permission denied while trying to connect to the Docker daemon socket」と出た**：`docker` のグループに入る設定が効いていません。「Docker を入れる」の後半の、`wsl --shutdown` からやり直してください。
- **「Cannot connect to the Docker daemon」と出た**：Docker が動いていません。`sudo service docker start` で動かしてください。
- **「port is already allocated」と出た**：8080番のポートを別のものが使っています。`docker ps` で同じポートのコンテナが残っていないか確かめてください。
- **「The container name "/web" is already in use」と出た**：同じ名前のコンテナが止まったまま残っています。`docker rm web` で消してから、もう一度動かしてください。

## 確かめよう

1. nginx のコンテナを、`web2` という名前で、パソコンの8081番のポートにつないで動かす
2. ブラウザで `http://localhost:8081` を開き、「Welcome to nginx!」が出ることを確かめる
3. `docker logs web2` で、ブラウザからのリクエストが記録されていることを確かめる
4. `web2` を止めて消す

最後に `docker ps -a` を打ち、`web2` が一覧にないことを確かめれば完了です。

## 今は知らなくてよいこと

- 自分でイメージを作る方法（Dockerfile）
- コンテナの中に入って操作する方法

## 次のレッスン

次は Web のアプリとデータベースのように、いくつものコンテナを組み合わせて、まとめて動かす方法を学びます。
