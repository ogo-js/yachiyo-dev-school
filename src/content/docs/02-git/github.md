---
title: GitHub に置く
description: GitHub のリポジトリを手元に持ってきて、変更を送り、GitHub 側の変更を取り込む
sidebar:
  order: 4
---

## このページでできるようになること

- GitHub に、パソコンからつなぐ準備ができる
- GitHub のリポジトリを手元に持ってこられる（クローン）
- 手元の記録を GitHub に送り（プッシュ）、GitHub 側の記録を手元に取り込める（プル）

かかる時間の目安は60分です。

## 始める前に

レッスン2-3（合流でぶつかったときに直す）を終えている必要があります。

## なぜ GitHub を使うのか

ここまでの記録は自分のパソコンの中にしかありません。パソコンが壊れれば記録も消えますし、他の人と同じリポジトリで作業することもできません。

GitHub は Git のリポジトリをインターネット上に置いて共有するためのサービスです。チームの全員が同じリポジトリを手元に持ってきて作業し、記録を GitHub に送り合います。手元のリポジトリと区別して、GitHub 上のリポジトリを「リモートリポジトリ」と呼びます。

## GitHub のアカウントを作る

アカウントをすでに持っている人は、次の「パソコンから GitHub につなぐ準備」へ進んでください。

1. ブラウザで github.com を開き、「Sign up」を押します。
2. メールアドレス、パスワード、ユーザー名を入れ、画面の案内に沿って進めます。
3. 届いたメールで、メールアドレスの確認を済ませます。

:::caution
ユーザー名はリポジトリの URL などで他の人にも見えます。後から変えると URL も変わるので、最初によく考えて決めてください。
:::

この教材では、ユーザー名が `yachiyo` の例で説明します。自分のユーザー名に置き換えて読んでください。

## パソコンから GitHub につなぐ準備

GitHub に記録を送るには、「このパソコンは本人のものだ」と GitHub に分かってもらう必要があります。この教材では「SSH 鍵」という方法を使います。

SSH 鍵は2つで1組の鍵です。

- **秘密鍵**：自分のパソコンにだけ置く。他の人には決して渡さない
- **公開鍵**：GitHub に登録する。他の人に見られてもかまわない

GitHub は登録された公開鍵と組になる秘密鍵を持っているかどうかで、本人かどうかを確かめます。

### 鍵を作る

ターミナルで次のように打ちます。メールアドレスは GitHub に登録したものに置き換えてください。

```bash
ssh-keygen -t ed25519 -C "yachiyo@example.com"
```

3回、質問が出ます。

```text
Enter file in which to save the key (/home/yachiyo/.ssh/id_ed25519):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
```

1つ目は何も打たずに Enter キーを押します。2つ目と3つ目は鍵を使うときの合言葉で、練習では空のまま Enter キーを押してかまいません。

:::note
仕事で使うパソコンでは合言葉を付けるかどうかなど、チームの決まりに従ってください。
:::

### 公開鍵を GitHub に登録する

公開鍵の中身を表示します。

```bash
cat ~/.ssh/id_ed25519.pub
```

```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA…… yachiyo@example.com
```

`ssh-ed25519` から最後のメールアドレスまでの1行を、マウスで選んでコピーします。

:::danger[.pub が付いている方だけを使う]
`id_ed25519.pub` が公開鍵、`.pub` の付かない `id_ed25519` が秘密鍵です。秘密鍵の中身は誰にも見せたり送ったりしないでください。
:::

GitHub での登録は次の順に進めます。

1. 右上の自分のアイコンを押し、「Settings」を選びます。
2. 左のメニューから「SSH and GPG keys」を選びます。
3. 「New SSH key」を押します。
4. 「Title」に、どのパソコンの鍵か分かる名前（例：`自宅のノートPC`）を入れます。
5. 「Key」に、コピーした1行を貼り付けます。
6. 「Add SSH key」を押します。

### つながるか確かめる

```bash
ssh -T git@github.com
```

初めてつなぐときは、次のように聞かれます。`yes` と打って Enter キーを押してください。

```text
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

次の1行が出れば、準備はできています。

```text
Hi yachiyo! You've successfully authenticated, but GitHub does not provide shell access.
```

「shell access は提供していない」という部分は、気にしなくてかまいません。

## GitHub にリポジトリを作る

1. GitHub の右上の「+」を押し、「New repository」を選びます。
2. 「Repository name」に `git-practice` と入れます。
3. 公開範囲は「Private」（自分だけが見られる）を選びます。
4. README を作る項目を有効にします。
5. 「Create repository」を押します。

`README.md` という説明用のファイルが1つ入った、リポジトリができます。

## 手元に持ってくる：git clone

リポジトリの画面で緑の「Code」ボタンを押し、「SSH」を選んで、表示された URL をコピーします。`git@github.com:` で始まる URL です。

練習用のフォルダに移って、クローンします。

```bash
cd ~/practice
git clone git@github.com:yachiyo/git-practice.git
```

```text
Cloning into 'git-practice'...
```

このあとに数行の表示が続きます。エラーが出ずに終わればクローンできています。

```bash
cd git-practice
ls
git log --oneline
```

```text
README.md
```

```text
a1b2c3d (HEAD -> main, origin/main, origin/HEAD) Initial commit
```

`origin` は、クローン元のリモートリポジトリに Git が付ける名前です。`origin/main` は「GitHub の `main` ブランチは、この記録のところにある」という印です。今は手元と GitHub が同じ記録を指しています。

## 手元の記録を送る：git push

`README.md` を VS Code で開き、最後に「Git の練習用のリポジトリです。」と1行書き足して保存します。いつもどおりにコミットします。

```bash
git add README.md
git commit -m "説明を書き足す"
```

この記録はまだ手元にしかありません。GitHub に送ります。

```bash
git push
```

送った量などの表示が数行出て、最後に次のような2行が出れば送れています。

```text
To github.com:yachiyo/git-practice.git
   a1b2c3d..e4f5a6b  main -> main
```

GitHub のリポジトリの画面を開き直すと、`README.md` に書き足した1行が表示されています。

## GitHub 側の記録を取り込む：git pull

チームで作業していると、他の人が GitHub に送った記録を、自分の手元に取り込む必要があります。ここでは、GitHub の画面でファイルを直して、その代わりにします。

1. GitHub のリポジトリの画面で `README.md` を開きます。
2. 右上の鉛筆の形のボタンを押します。
3. 最後に「GitHub の画面からも直せます。」と1行書き足します。
4. 「Commit changes」を押し、出てきた画面でももう一度「Commit changes」を押します。

これで、GitHub の方が手元より1つ記録が進んだ状態になりました。手元に取り込みます。

```bash
git pull
```

```text
Updating e4f5a6b..c7d8e9f
Fast-forward
 README.md | 1 +
 1 file changed, 1 insertion(+)
```

`cat README.md` で、GitHub で書き足した行が手元にも入ったことを確かめてください。

:::tip[作業を始める前に git pull]
他の人の記録が GitHub に増えているかもしれないので、作業を始める前には `git pull` で手元を最新にしておくのが基本です。
:::

## 困ったとき

- **「Permission denied (publickey)」と出た**：公開鍵が GitHub に登録されていないか、登録した鍵と手元の鍵が組になっていません。「公開鍵を GitHub に登録する」をやり直してください。
- **`git push` で「rejected」「fetch first」と出た**：GitHub の方に、手元にない記録があります。先に `git pull` で取り込んでから、もう一度 `git push` してください。
- **`git pull` でコンフリクトが起きた**：レッスン2-3と同じ方法で直して、コミットしてから `git push` してください。

## 確かめよう

`~/practice/git-practice` で、次のことをやってみてください。

1. `notes.txt` を作って1行書き、コミットして `git push` する
2. GitHub の画面で `notes.txt` が見えることを確かめる
3. GitHub の画面で `notes.txt` に1行書き足してコミットする
4. 手元で `git pull` して、書き足した行が入ったことを `cat` で確かめる

最後に、次のように打ちます。

```bash
git status
```

結果に次の2行が含まれていれば完了です。

```text
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

1行目は「手元の `main` は、最後に確かめたときの GitHub の `main` と同じ」という意味です。

## 今は知らなくてよいこと

- 手元で作ったリポジトリを、あとから GitHub につなぐ方法
- `git fetch` と `git pull` の違い

## 次のレッスン

次はチームで開発するときに欠かせない「プルリクエスト」を使って、自分の変更を他の人に見てもらいます。
