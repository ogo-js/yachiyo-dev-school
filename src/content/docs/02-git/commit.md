---
title: 変更の履歴を残す
description: Git でファイルの変更を記録し、見返し、記録する前の変更を取り消す
sidebar:
  order: 1
---

## このページでできるようになること

- Git を使い始めるための設定ができる
- ファイルの変更を確かめて、記録（コミット）できる
- 記録の一覧を見返し、記録する前の変更を取り消せる

かかる時間の目安は45分です。

## 始める前に

レッスン1-2（ファイルを扱う）を終えている必要があります。

## なぜ Git を使うのか

ファイルを直すときに、`報告書_最新.docx`、`報告書_最新_修正版.docx` のように、名前を変えたコピーを残したことはないでしょうか。どれが本当の最新なのか、どこを変えたのかがすぐに分からなくなります。

Git はファイルの変更を「いつ・誰が・何を変えたか」の記録として残す道具です。ファイルは1つのままで、過去の状態をいつでも見返せます。開発の現場では、ほぼすべてのプログラムが Git で管理されています。

## Git が入っているか確かめる

VS Code で Ubuntu につなぎ、ターミナルで次のように打ちます。

```bash
git --version
```

```text
git version 2.43.0
```

数字は違っていてもかまいません。`command not found` と出た場合は、次のように打って Git を入れてください。

```bash
sudo apt update
sudo apt install git
```

`sudo` は「管理者として実行する」という意味です。パスワードを聞かれたら、レッスン0-1で決めた Ubuntu のパスワードを打ってください（画面には出ません）。

## 最初の設定

Git の記録には、記録した人の名前とメールアドレスが入ります。最初に1回だけ、次の5つを設定します。

```bash
git config --global user.name "Yachiyo"
git config --global user.email "yachiyo@example.com"
git config --global init.defaultBranch main
git config --global core.editor "code --wait"
git config --global pull.rebase false
```

1行目と2行目は、自分の名前とメールアドレスに置き換えてください。名前は英字で書くのがおすすめです。

3行目から5行目はこの教材の画面の表示や動きとそろえるための設定です。今は意味が分からなくてかまいません。

設定できたかは次のように確かめられます。

```bash
git config --global --list
```

```text
user.name=Yachiyo
user.email=yachiyo@example.com
init.defaultbranch=main
core.editor=code --wait
pull.rebase=false
```

## 記録を始める：git init

練習用のフォルダを作り、Git で記録を始めます。

```bash
mkdir ~/practice/git1
cd ~/practice/git1
git init
```

```text
Initialized empty Git repository in /home/yachiyo/practice/git1/.git/
```

Git で記録をとるフォルダを「リポジトリ」と呼びます。`git init` は、今いるフォルダをリポジトリにするコマンドです。

## 今の状態を見る：git status

```bash
git status
```

```text
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

`git status` は、リポジトリの今の状態を表示します。これから何度も使うコマンドです。迷ったら、まず `git status` を打ってください。

今は「まだ記録がない（No commits yet）」「記録するものもない（nothing to commit）」と言っています。

## ファイルを作る

`todo.txt` を作って、VS Code で開きます。

```bash
touch todo.txt
code todo.txt
```

1行目に「牛乳を買う」と書いて、保存してください。もう一度、状態を見ます。

```bash
git status
```

```text
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	todo.txt

nothing added to commit but untracked files present (use "git add" to track)
```

`Untracked files` は「Git がまだ記録の対象にしていないファイル」という意味です。

## 記録するものを選ぶ：git add

Git の記録は2つの段階に分かれています。

1. `git add` で、次の記録に入れるファイルを選ぶ
2. `git commit` で、選んだものを記録する

荷物を送るときに、箱に詰める（add）のと、送り状を書いて出す（commit）のが分かれているようなものです。いくつかのファイルを変えたときも、関係するものだけを選んで1つの記録にできます。

```bash
git add todo.txt
git status
```

```text
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   todo.txt
```

`Changes to be committed` は「次の記録に入るもの」という意味です。

## 記録する：git commit

```bash
git commit -m "やることリストを作る"
```

```text
[main (root-commit) 1a8cbd0] やることリストを作る
 1 file changed, 1 insertion(+)
 create mode 100644 todo.txt
```

1回の記録を「コミット」と呼びます。`-m` のあとの文はその記録の説明です。後から見返したときに、何をした記録なのかが分かるように書きます。

`1a8cbd0` はコミットごとに付く番号で、人によって違う値になります。

## 記録を見返す：git log

```bash
git log --oneline
```

```text
1a8cbd0 (HEAD -> main) やることリストを作る
```

これまでのコミットが新しい順に並びます。`(HEAD -> main)` は「今いるのはここ」という印です。詳しくは次のレッスンで扱います。

## 変更を確かめてから記録する：git diff

`todo.txt` の2行目に「本を返す」と書いて、保存してください。何が変わったかを確かめます。

```bash
git diff
```

```text
diff --git a/todo.txt b/todo.txt
index 4d4d760..27f841e 100644
--- a/todo.txt
+++ b/todo.txt
@@ -1 +1,2 @@
 牛乳を買う
+本を返す
```

`+` で始まる行が足した行です。消した行には `-` が付きます。上の4行はどのファイルを比べた結果かを表す見出しなので、今は読み飛ばしてかまいません。

:::note
`\ No newline at end of file` という行が出ることがあります。「ファイルの最後に改行がない」という意味で、気にしなくてかまいません。
:::

確かめたら、記録します。

```bash
git add todo.txt
git commit -m "本を返すを足す"
git log --oneline
```

```text
9159aa5 (HEAD -> main) 本を返すを足す
1a8cbd0 やることリストを作る
```

コミットが2つになりました。

## 記録する前の変更を取り消す：git restore

`todo.txt` の3行目に「まちがい」と書いて、保存してください。この変更をやめて、最後に記録した状態へ戻します。

```bash
git restore todo.txt
cat todo.txt
```

```text
牛乳を買う
本を返す
```

「まちがい」の行が消えました。VS Code の画面にも、少し待つと戻った内容が表示されます。

:::caution
`git restore` で取り消した変更は記録されていないので戻せません。取り消す前に `git diff` で、消えてよい変更かどうかを確かめてください。
:::

## 困ったとき

- **「Please tell me who you are」と出た**：名前とメールアドレスの設定がされていません。「最初の設定」をやり直してください。
- **「not a git repository」と出た**：今いるフォルダがリポジトリではありません。`pwd` で場所を確かめ、`cd ~/practice/git1` で移動してください。

## 確かめよう

`~/practice/git1` で、次のことをやってみてください。

1. `todo.txt` の3行目に「部屋を片付ける」と書き、`git diff` で確かめてからコミットする
2. `todo.txt` の1行目を消して保存し、その変更を `git restore` で取り消す

最後に、次の3つを打ちます。

```bash
git log --oneline
cat todo.txt
git status
```

コミットが3つ並び、`todo.txt` が3行あり、`git status` の最後に次の1行が出れば完了です。

```text
nothing to commit, working tree clean
```

これは「記録していない変更は何もない」という意味です。

## 今は知らなくてよいこと

- コミットした後に、そのコミットを取り消す方法
- 記録しないファイルを指定する方法（`.gitignore`）

どちらも必要になったレッスンで扱います。

## 次のレッスン

次は「ブランチ」を使って、本筋の記録を残したまま、別の作業を試せるようにします。
