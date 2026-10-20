---
title: ブランチで作業を分ける
description: ブランチを作って切り替え、作業が終わったら本筋に合流させる
sidebar:
  order: 2
---

## このページでできるようになること

- ブランチを作って、切り替えられる
- ブランチで記録した作業を、本筋のブランチに合流（マージ）できる
- 使い終わったブランチを消せる

かかる時間の目安は30分です。

## 始める前に

レッスン2-1（変更の履歴を残す）を「確かめよう」まで終えている必要があります。このレッスンではそのとき使った `~/practice/git1` を使います。

## なぜブランチを使うのか

新しいことを試すとき、うまくいくかどうかはやってみるまで分かりません。途中で失敗すると、ちゃんと動いていた状態まで壊してしまうことがあります。

ブランチは記録の流れを枝分かれさせる仕組みです。本筋はそのまま残して、別の枝の上で作業できます。うまくいったら本筋に合流させ、だめなら枝ごと捨てられます。

開発の現場では、本筋のブランチで直接作業することはほとんどありません。作業ごとにブランチを作るのが普通です。

## 今のブランチを見る：git branch

```bash
cd ~/practice/git1
git branch
```

```text
* main
```

今あるブランチが並びます。`*` が付いているのが、今いるブランチです。レッスン2-1で設定したとおり、最初のブランチの名前は `main` です。これが本筋のブランチになります。

## ブランチを作って移る：git switch -c

買い物のメモを作る作業のために、`shopping` というブランチを作ります。

```bash
git switch -c shopping
```

```text
Switched to a new branch 'shopping'
```

`git switch -c` は「ブランチを作って、そこへ移る」コマンドです。確かめます。

```bash
git branch
```

```text
  main
* shopping
```

`*` が `shopping` に移りました。

## ブランチの上で記録する

`shopping.txt` を作って VS Code で開き、1行目に「卵」と書いて保存します。

```bash
touch shopping.txt
code shopping.txt
```

いつもどおりにコミットします。

```bash
git add shopping.txt
git commit -m "買い物メモを作る"
git log --oneline
```

```text
4e03752 (HEAD -> shopping) 買い物メモを作る
54267b8 (main) 部屋を片付けるを足す
da25ccd 本を返すを足す
d2e4a7c やることリストを作る
```

コミットの番号は人によって違います。上から2つ目の説明は、レッスン2-1の「確かめよう」で自分が書いたものになっています。

括弧の中の印を見ると、今の状態が分かります。

- `HEAD -> shopping`：今いるのは `shopping` ブランチで、その一番新しい記録がこれ
- `main`：`main` ブランチはまだ1つ前の記録のところにいる

## 本筋に戻る：git switch

`main` ブランチに戻って、ファイルを見てみます。

```bash
git switch main
ls
```

```text
todo.txt
```

`shopping.txt` が見えなくなりました。消えたわけではありません。`main` ブランチにはまだ記録されていないので、表示されていないだけです。

もう一度 `shopping` に移ると、また見えるようになります。

```bash
git switch shopping
ls
```

```text
shopping.txt  todo.txt
```

ブランチを切り替えると、フォルダの中身がそのブランチの状態に入れ替わります。VS Code で開いているファイルも、それに合わせて変わります。

## 本筋に合流させる：git merge

買い物メモの作業が終わったので、`main` に合流させます。合流させるときは、合流させる先のブランチに移ってから `git merge` を打ちます。

```bash
git switch main
git merge shopping
```

```text
Updating 54267b8..4e03752
Fast-forward
 shopping.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 shopping.txt
```

`shopping` ブランチでの記録が `main` に取り込まれました。

```bash
git log --oneline
ls
```

```text
4e03752 (HEAD -> main, shopping) 買い物メモを作る
54267b8 部屋を片付けるを足す
da25ccd 本を返すを足す
d2e4a7c やることリストを作る
```

```text
shopping.txt  todo.txt
```

`main` と `shopping` が同じ記録を指すようになりました。

:::note
今回は `shopping` ブランチで作業している間、`main` には何も記録していません。そのため、`main` を前に進めるだけで合流が終わりました。これを「Fast-forward」と呼びます。両方のブランチで同じ所を変えたときの合流は、次のレッスンで扱います。
:::

## 使い終わったブランチを消す：git branch -d

合流が終わったブランチは消してかまいません。

```bash
git branch -d shopping
```

```text
Deleted branch shopping (was 4e03752).
```

消えるのは「shopping」という枝の名前だけです。記録は `main` に取り込まれているので、残っています。

:::tip
`git branch -d` は、まだ合流させていないブランチを消そうとすると、エラーを出して止めてくれます。合流を忘れたまま記録を失うことはありません。
:::

## 困ったとき

- **ブランチを切り替えようとしたら「Your local changes … would be overwritten」と出た**：まだコミットしていない変更があり、切り替えるとその変更が上書きされてしまいます。先にコミットするか、要らない変更なら `git restore` で取り消してから切り替えてください。
- **今どのブランチにいるか分からなくなった**：`git branch` で `*` の付いた行を見てください。`git status` の1行目（`On branch …`）にも出ています。

## 確かめよう

`~/practice/git1` で、次のことをやってみてください。

1. `main` から `cleaning` というブランチを作って移る
2. `todo.txt` の最後に「窓をふく」と書き足して、コミットする
3. `main` に戻り、`todo.txt` に「窓をふく」がないことを `cat` で確かめる
4. `cleaning` を `main` に合流させる
5. `cleaning` ブランチを消す

最後に、次の3つを打ちます。

```bash
git branch
git log --oneline
cat todo.txt
```

`git branch` の結果が `* main` の1行だけで、`git log` の一番上が自分のコミットで `(HEAD -> main)` が付いていて、`todo.txt` の最後に「窓をふく」があれば完了です。

## 今は知らなくてよいこと

- ブランチの名前の付け方の決まり（チームごとに決めることが多いです）
- 合流させずにブランチを捨てる方法

## 次のレッスン

次は2つのブランチで同じ所を変えたときに起きる「コンフリクト」と、その直し方を扱います。
