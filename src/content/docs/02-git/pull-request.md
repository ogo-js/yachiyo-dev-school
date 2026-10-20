---
title: プルリクエストで見てもらう
description: ブランチを GitHub に送り、プルリクエストを出して、レビューを受けてから合流させる
sidebar:
  order: 5
---

## このページでできるようになること

- 作業用のブランチを GitHub に送れる
- プルリクエストを出し、変更の中身を画面で確かめられる
- 指摘を受けて直し、プルリクエストを合流（マージ）できる

かかる時間の目安は45分です。

## 始める前に

レッスン2-4（GitHub に置く）を「確かめよう」まで終えている必要があります。このレッスンでは `~/practice/git-practice` を使います。

## なぜプルリクエストを使うのか

チームの開発では、自分の変更をいきなり `main` に合流させることはしません。合流させる前に、他の人に変更を見てもらい（レビュー）、問題がないことを確かめてから合流させます。

プルリクエストは「このブランチの変更を `main` に合流させたいので、見てください」という依頼を GitHub 上に出す仕組みです。変更の中身、話し合いの記録、合流の操作が、1つの画面にまとまります。

このレッスンでは自分でプルリクエストを出し、自分で見て、自分で合流させます。実際の仕事では、見る人と合流させる人は別の人になります。

## ブランチで作業する

いつもどおり、作業用のブランチを作ってコミットします。

```bash
cd ~/practice/git-practice
git pull
git switch -c add-profile
```

`profile.md` を作って VS Code で開き、次の2行を書いて保存します。

```text
# 自己紹介
名前：やちよ
```

```bash
git add profile.md
git commit -m "自己紹介を作る"
```

## ブランチを GitHub に送る

新しいブランチを初めて送るときは、次のように打ちます。

```bash
git push -u origin add-profile
```

`-u origin add-profile` は「`origin`（GitHub）に `add-profile` という名前で送り、この先はそこと結び付ける」という意味です。2回目からは `git push` だけで送れます。

表示の途中に、次のような行が出ます。

```text
remote: Create a pull request for 'add-profile' on GitHub by visiting:
remote:      https://github.com/yachiyo/git-practice/pull/new/add-profile
```

「プルリクエストを作るならこの URL へ」という案内です。

## プルリクエストを出す

1. GitHub のリポジトリの画面を開きます。上の方に `add-profile` についての黄色い帯が出ているので、「Compare & pull request」を押します。
2. 「base: main ← compare: add-profile」となっていることを確かめます。`add-profile` の変更を `main` に合流させる、という意味です。
3. タイトルに「自己紹介を作る」と入れます。
4. 説明の欄に、何のための変更か、見てほしい点は何かを書きます。例：「自己紹介のページを足しました。書き方に違和感がないか見てください。」
5. 「Create pull request」を押します。

## 変更を見る

プルリクエストの画面の「Files changed」のタブを開くと、変更の中身が表示されます。`git diff` と同じように、足した行は緑、消した行は赤で表示されます。

行の左にある「+」のボタンを押すと、その行にコメントを書けます。レビューをする人はここに指摘や質問を書きます。

試しに、「名前：やちよ」の行に「趣味も書いてはどうでしょう」とコメントを書き、「Add single comment」を押してみてください。

## 指摘を受けて直す

指摘に応えて、手元で直します。今いるブランチが `add-profile` であることを `git branch` で確かめてから、`profile.md` の最後に「趣味：散歩」と書き足して保存します。

```bash
git add profile.md
git commit -m "趣味を足す"
git push
```

プルリクエストの画面を開き直すと、コミットが2つに増えています。同じブランチに送った記録は、出したままのプルリクエストに自動で加わります。プルリクエストを出し直す必要はありません。

## 合流させる

1. プルリクエストの画面の下にある「Merge pull request」を押します。
2. 「Confirm merge」を押します。
3. 「Delete branch」を押して、GitHub 上の `add-profile` ブランチを消します。

GitHub の `main` に、`profile.md` が入りました。

## 手元を最新にする

合流は GitHub の上で行ったので、手元の `main` はまだ古いままです。`main` に戻って取り込みます。

```bash
git switch main
git pull
ls
```

```text
README.md  notes.txt  profile.md
```

手元の `add-profile` ブランチも、もう使わないので消します。

```bash
git branch -d add-profile
```

## 困ったとき

- **`git push` で「has no upstream branch」と出た**：新しいブランチを初めて送るときは、`git push -u origin ブランチ名` と打ってください。
- **「Compare & pull request」の帯が出ていない**：リポジトリの画面の「Pull requests」タブを開き、「New pull request」を押してください。「compare」で自分のブランチを選べば、同じ画面に進めます。
- **プルリクエストの画面に「This branch has conflicts」と出た**：`main` と同じ所を変えています。手元で `main` を取り込んでコンフリクトを直す方法は、レッスン2-3の応用になります。困ったら、レビューをする人に相談してください。

## 確かめよう

`~/practice/git-practice` で、次のことをやってみてください。

1. `add-goal` というブランチを作り、`profile.md` に「目標：アプリを作る」と書き足してコミットする
2. ブランチを GitHub に送り、プルリクエストを出す
3. 「Files changed」で自分の変更にコメントを1つ書く
4. プルリクエストを合流させ、GitHub 上のブランチを消す
5. 手元の `main` を最新にして、手元の `add-goal` ブランチを消す

最後に、次の3つを打ちます。

```bash
git branch
git status
cat profile.md
```

`git branch` が `* main` の1行だけで、`git status` に `up to date with 'origin/main'` が出て、`profile.md` の最後に「目標：アプリを作る」があれば完了です。

## 今は知らなくてよいこと

- 合流のやり方の種類（Squash and merge など）
- レビューで「承認」や「変更の依頼」を出す方法

## 次のレッスン

これで、Git と GitHub を使った基本の流れが一周しました。次からは第3部です。Web のアプリがブラウザとサーバーの間でどのようにやり取りしているかを見ていきます。
