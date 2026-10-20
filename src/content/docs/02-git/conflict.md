---
title: 合流でぶつかったときに直す
description: 2つのブランチで同じ所を変えたときに起きるコンフリクトを読み、直して合流を終える
sidebar:
  order: 3
---

## このページでできるようになること

- コンフリクトが起きたことに気づける
- コンフリクトの起きたファイルを読んで、正しい内容に直せる
- 直した結果を記録して合流を終えるか、合流そのものを取りやめられる

かかる時間の目安は30分です。

## 始める前に

レッスン2-2（ブランチで作業を分ける）を「確かめよう」まで終えている必要があります。このレッスンでも `~/practice/git1` を使います。

## なぜこれを覚えるのか

チームで開発していると、自分と他の人が同じファイルの同じ行を変えることがあります。どちらの変更を残すかは Git には決められません。このとき Git は合流を途中で止めて、人に判断を求めます。これを「コンフリクト」と呼びます。

コンフリクトは失敗ではなく、開発ではよく起きることです。落ち着いて読めば、直し方は毎回同じです。

## わざとコンフリクトを起こす

買い物メモの卵の数を、2つのブランチで別々に変えます。

まず、`egg-count` というブランチで「卵を10個」に変えます。

```bash
cd ~/practice/git1
git switch -c egg-count
```

`shopping.txt` の1行目を「卵を10個」に書き換えて保存し、コミットします。

```bash
git add shopping.txt
git commit -m "卵を10個にする"
```

次に、`main` に戻って、同じ行を「卵を6個」に書き換えて保存し、コミットします。

```bash
git switch main
```

```bash
git add shopping.txt
git commit -m "卵を6個にする"
```

これで、同じ行を2つのブランチで別々に変えた状態になりました。`egg-count` を `main` に合流させます。

```bash
git merge egg-count
```

```text
Auto-merging shopping.txt
CONFLICT (content): Merge conflict in shopping.txt
Automatic merge failed; fix conflicts and then commit the result.
```

`CONFLICT` と出ました。「`shopping.txt` でぶつかったので、直してからコミットしてください」という意味です。

## 状態を見る

```bash
git status
```

```text
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   shopping.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

`both modified` は「両方のブランチで変えられたファイル」という意味です。ここに並んだファイルを直していきます。

## ファイルを読む

`shopping.txt` を VS Code で開くと、次のようになっています。

```text
<<<<<<< HEAD
卵を6個
=======
卵を10個
>>>>>>> egg-count
```

Git が書き込んだ3種類の印で、2つの変更が区切られています。

| 印 | 意味 |
| --- | --- |
| `<<<<<<< HEAD` | ここから下が、今いるブランチ（`main`）の内容 |
| `=======` | 2つの内容の境目 |
| `>>>>>>> egg-count` | ここから上が、合流させようとしたブランチ（`egg-count`）の内容 |

## 直す

どちらを残すかを決めて、ファイルを正しい内容に書き換えます。今回は「卵を10個」を残すことにします。

印の行と「卵を6個」の行を消して、次の1行だけにして保存してください。

```text
卵を10個
```

:::caution
印の行（`<<<<<<<`、`=======`、`>>>>>>>`）を消し忘れると、その印がファイルの中身として記録されてしまいます。保存する前に、印が残っていないか確かめてください。
:::

:::tip[VS Code のボタンでも直せる]
VS Code でコンフリクトのあるファイルを開くと、印の上に「現在の変更を取り込む」「入力側の変更を取り込む」などのボタンが出ます（英語の場合は Accept Current Change、Accept Incoming Change）。押すと、選んだ方だけが残り、印も消えます。表示はバージョンによって少し違うことがあります。
:::

## 直したことを伝えて、合流を終える

直したファイルを `git add` すると、「このファイルは直した」と Git に伝えたことになります。

```bash
git add shopping.txt
git status
```

```text
On branch main
All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)

Changes to be committed:
	modified:   shopping.txt
```

「すべて直したが、まだ合流の途中」と言っています。コミットして合流を終えます。

```bash
git commit -m "卵の数を10個にそろえる"
```

記録の流れを、枝分かれの形で見てみます。

```bash
git log --oneline --graph
```

```text
*   4b3cb9d (HEAD -> main) 卵の数を10個にそろえる
|\
| * 67faa25 (egg-count) 卵を10個にする
* | 0458b00 卵を6個にする
|/
* 3b6fb27 窓をふくを足す
* 4e03752 買い物メモを作る
```

2本に分かれた記録が、一番上のコミットで1本に合流しているのが分かります。以下の行は省いています。

使い終わった `egg-count` ブランチを消しておきます。

```bash
git branch -d egg-count
```

## 合流を取りやめる：git merge --abort

コンフリクトが起きたときに、どちらを残すか自分では決められないこともあります。そのときは、合流そのものを取りやめて、合流する前の状態に戻せます。

```bash
git merge --abort
```

取りやめたら、変更した人に相談してから、もう一度合流させてください。

## 困ったとき

- **コミットしようとしたら「Committing is not possible because you have unmerged files」と出た**：まだ `git add` していない、コンフリクトの起きたファイルがあります。`git status` の `Unmerged paths` に並んだファイルを直して、`git add` してください。
- **どこがぶつかっているか分からない**：ファイルの中で `<<<<<<<` を探してください。VS Code なら Ctrl キーを押しながら F キーを押すと、ファイルの中を検索できます。

## 確かめよう

`~/practice/git1` で、次のことをやってみてください。

1. `main` から `book` というブランチを作り、`todo.txt` の「本を返す」を「本を図書館に返す」に変えてコミットする
2. `main` に戻り、同じ行を「本を2冊返す」に変えてコミットする
3. `book` を `main` に合流させ、コンフリクトを起こす
4. 1行を「本を2冊、図書館に返す」に直して、合流を終える
5. `book` ブランチを消す

最後に、次の3つを打ちます。

```bash
git status
git log --oneline --graph
cat todo.txt
```

`git status` の最後が `nothing to commit, working tree clean` で、`git log` に枝分かれと合流の形があり、`todo.txt` に「本を2冊、図書館に返す」があれば完了です。印の行が残っていないことも確かめてください。

## 今は知らなくてよいこと

- コンフリクトを起こしにくくする作業の進め方
- 合流させる別の方法（rebase）

## 次のレッスン

次は GitHub です。ここまで自分のパソコンの中だけで使ってきたリポジトリを、インターネット上に置いて、他の人と共有できるようにします。
