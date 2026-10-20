---
title: 道具を足す
description: skill を作って、決まった作業の手順を名前で呼べるようにする
sidebar:
  order: 3
---

## このページでできるようになること

- skill の役割と、CLAUDE.md との違いを説明できる
- 自分で skill を作れる
- skill を `/名前` で呼んだり、Claude Code に自動で使わせたりできる

かかる時間の目安は40分です。

## 始める前に

付録の「指示を置いておく」を終えている必要があります。

## なぜこれを覚えるのか

「プルリクエストを出す前に、この順で確かめる」のような手順を、毎回チャットに貼り付けるのは大変です。CLAUDE.md に書くこともできますが、CLAUDE.md は毎回すべてが読み込まれるので、たまにしか使わない長い手順を書くと、コンテキストの無駄になります。

skill は手順や知識を1つのフォルダにまとめたものです。普段は名前と説明だけが読み込まれ、使うときに初めて中身が読み込まれます。

| | CLAUDE.md・rule | skill |
| --- | --- | --- |
| 読み込まれるとき | 毎回すべて | 使うときだけ（普段は名前と説明だけ） |
| 向いているもの | 毎回守る、短い決まり | たまに使う手順や、長い知識 |
| 呼び方 | 呼ばなくても効く | `/名前` で呼ぶか、Claude Code が必要と判断して使う |

## skill を作る

skill は `.claude/skills/` の下に、skill の名前のフォルダを作り、その中に `SKILL.md` を置いて作ります。

```bash
cd ~/practice/business-app
mkdir -p .claude/skills/pre-pr-check
code .claude/skills/pre-pr-check/SKILL.md
```

```markdown
---
description: プルリクエストを出す前の確かめをする。プルリクエストを出す前や、変更を見直したいと言われたときに使う。
---

次の順で確かめ、結果を表にまとめる。

1. `cd rr1 && npm run typecheck` を動かす
2. `cd rr1 && npx vitest run` を動かす
3. `dotnet test api1.Tests` を動かす
4. `git diff main` を読み、次のものが残っていないか確かめる
   - 確かめるために足した `console.log`
   - パスワードなどの、人に見せてはいけない情報
   - 今回の作業と関係のない変更

失敗したものがあっても、直さずに報告だけする。
```

- フォルダの名前（`pre-pr-check`）が、呼ぶときの名前になる
- 頭の `---` で囲んだ部分の `description` は、Claude Code がこの skill をいつ使うかを決める手がかり。何をするものか、どんなときに使うかを書く
- その下が skill を使うときに読み込まれる手順

## skill を呼ぶ

Claude Code の入力欄で、`/` に続けて名前を打ちます。

```text
/pre-pr-check
```

また、「プルリクエストを出す前に確かめて」のように頼むと、`description` に合うので、Claude Code が自分でこの skill を使うこともあります。

`/skills` と打つと、使える skill の一覧が見られます。

## 自動で使わせたくないとき

コミットやデプロイのように、自分が決めたときだけ動いてほしいものは、頭に `disable-model-invocation: true` を書きます。

```markdown
---
description: 変更をコミットする
disable-model-invocation: true
---
```

こうすると、Claude Code が自分の判断でこの skill を使うことはなくなり、`/名前` で呼んだときだけ動きます。

## 置き場所

| 置き場所 | 使える範囲 |
| --- | --- |
| `プロジェクト/.claude/skills/` | そのプロジェクト。Git に入れればチームで共有できる |
| `~/.claude/skills/` | 自分のすべてのプロジェクト |

:::note
以前は `.claude/commands/` に Markdown のファイルを置いて、自分のコマンドを作っていました。今は skill にまとめられています。`.claude/commands/` のファイルも今まで通り動きますが、新しく作るときは skill を使います。
:::

## 困ったとき

- **頼んでも skill が使われない**：`description` に、自分が頼むときに使う言葉が入っているか確かめてください。`/名前` で直接呼ぶこともできます。
- **頼んでいないのに skill が使われる**：`description` をもっと絞るか、`disable-model-invocation: true` を書いてください。

## 確かめよう

1. 上の `pre-pr-check` を作る
2. `/pre-pr-check` で呼び、確かめの結果が表で返ることを確かめる
3. `description` に合う言葉で頼み、Claude Code が自分でこの skill を使うことを確かめる

2と3の両方で、型の検査とテストの結果、`git diff` の見直しの結果が返れば完了です。

## 今は知らなくてよいこと

- skill の中にスクリプトや参考の資料を一緒に置く方法
- 外の道具（データベースや課題の管理の道具など）につなぐ仕組み（MCP）

## 次のレッスン

次は作業をセッションをまたいでつないだり、サブエージェントに任せたりする方法を学びます。
