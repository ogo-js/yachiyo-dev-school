---
title: さらに学ぶ
description: この教材を終えた後に読むとよい、公式のチュートリアルや資料
---

この教材では業務アプリを作るのに最低限要るところだけを扱いました。ここでは、もう一歩進みたいときに読むとよい資料を、部ごとに挙げます。

どれも、この教材を終えた人なら読み進められるものです。最初から全部を読む必要はありません。仕事で分からないことに出会ったときに、関係する部の資料を開いてください。

:::note
英語の資料も混ざっています。英語のページはブラウザの翻訳の機能を使って読んでもかまいません。コマンドやコードは、翻訳されたものではなく元の英語のページから写してください。
:::

## Git と GitHub（第2部の続き）

| 資料 | 内容 | 言語 |
| --- | --- | --- |
| [Pro Git](https://git-scm.com/book/ja/v2) | Git の仕組みを、基本から細かいところまで説明した本。Web で全文を読める | 日本語 |
| [GitHub Docs](https://docs.github.com/ja) | GitHub の公式の説明。プルリクエストのレビューや、Actions の使い方など | 日本語 |
| [GitHub Actions のクイックスタート](https://docs.github.com/ja/actions/get-started/quickstart) | プッシュやプルリクエストのたびに、テストなどを自動で動かす仕組み（CI）の入門 | 日本語 |

この教材の「今は知らなくてよいこと」で後回しにした、コミットの取り消しや `rebase` は Pro Git の「Git の基本」と「Git のブランチ機能」の章にあります。

レッスン10-2の「今は知らなくてよいこと」に挙げた CI は、GitHub Actions で作れます。クイックスタートを読んだら、[.NET でのビルドとテスト](https://docs.github.com/ja/actions/tutorials/build-and-test-code/net)と[Node.js のビルドとテスト](https://docs.github.com/ja/actions/tutorials/build-and-test-code/nodejs)を見ながら、`business-app` の `dotnet test` と `npx vitest run` をプルリクエストのたびに動かすようにしてみてください。

## Web の仕組み（第3部の続き）

| 資料 | 内容 | 言語 |
| --- | --- | --- |
| [MDN の HTTP の説明](https://developer.mozilla.org/ja/docs/Web/HTTP) | HTTP のメソッド、ステータスコード、ヘッダー、Cookie の詳しい説明 | 日本語 |

ステータスコードやヘッダーの意味を調べたいときは、まずここを引きます。

## Docker（第4部の続き）

| 資料 | 内容 | 言語 |
| --- | --- | --- |
| [Docker の Get started](https://docs.docker.com/get-started/) | Docker の公式の入門。Dockerfile を書いて、自分のアプリのイメージを作るところまで | 英語 |

## データベース（第5部の続き）

| 資料 | 内容 | 言語 |
| --- | --- | --- |
| [PostgreSQL 文書](https://www.postgresql.jp/document/) | PostgreSQL の公式の説明書の日本語訳。最初の「チュートリアル」の章から読める | 日本語 |

## JavaScript と TypeScript（第6部の続き）

| 資料 | 内容 | 言語 |
| --- | --- | --- |
| [JavaScript Primer](https://jsprimer.net/) | JavaScript の基本の文法を、今の書き方で順に説明した入門書。Web で全文を読める | 日本語 |
| [サバイバル TypeScript](https://typescriptbook.jp/) | TypeScript を実務で使うために必要なことをまとめた入門書 | 日本語 |
| [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) | TypeScript の公式の説明 | 英語 |

## React と React Router（第7部の続き）

| 資料 | 内容 | 言語 |
| --- | --- | --- |
| [React の学習](https://ja.react.dev/learn) | React の公式のチュートリアル。コンポーネントの分け方や、状態の考え方を詳しく説明している | 日本語 |
| [React Router のチュートリアル（Address Book）](https://reactrouter.com/tutorials/address-book) | 連絡先の管理アプリを作りながら、loader と action、入れ子のルートなどを学ぶ公式のチュートリアル | 英語 |

React Router のチュートリアルは、第7部で作った社員の一覧とよく似た形のアプリを作ります。第7部の続きとして取り組むと、ページの外枠を共通にする書き方や、送信中の表示など、この教材で後回しにしたことを学べます。

## C# と ASP.NET Core（第8部の続き）

| 資料 | 内容 | 言語 |
| --- | --- | --- |
| [C# のドキュメント](https://learn.microsoft.com/ja-jp/dotnet/csharp/) | C# の公式の説明。言語の機能を1つずつ調べられる | 日本語 |
| [ASP.NET Core で Web API を作るチュートリアル](https://learn.microsoft.com/ja-jp/aspnet/core/tutorials/first-web-api) | Web API を作る公式のチュートリアル | 日本語 |
| [Npgsql のドキュメント](https://www.npgsql.org/doc/) | 第8部で使った、C# から PostgreSQL につなぐ部品の説明 | 英語 |
| [ASP.NET Core 認証の概要](https://learn.microsoft.com/ja-jp/aspnet/core/security/authentication/) | ログインの仕組み（認証）の公式の説明。業務アプリにはほぼ必ず要る | 日本語 |
| [開発中のアプリ シークレットの安全な保存](https://learn.microsoft.com/ja-jp/aspnet/core/security/app-secrets) | レッスン10-2で使ったユーザーシークレットの公式の説明 | 日本語 |

ログインはレッスン3-4の Cookie の話の続きです。どのやり方を選ぶかは会社で決められていることが多いので、まず職場で使っている方法を確かめてから読んでください。

## テスト（第9部の続き）

| 資料 | 内容 | 言語 |
| --- | --- | --- |
| [Vitest のガイド](https://vitest.dev/guide/) | Vitest の公式の説明 | 英語 |
| [Testing Library のドキュメント](https://testing-library.com/docs/) | コンポーネントの探し方や、操作のしかたの説明 | 英語 |
| [xUnit.net](https://xunit.net/) | xUnit の公式のサイト | 英語 |
