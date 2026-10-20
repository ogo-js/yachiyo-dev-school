---
title: テーブルをつなぐ
description: JOIN で2つの表をつないで読み、部署ごとの人数を数える
sidebar:
  order: 3
---

## このページでできるようになること

- 2つの表がどの列でつながっているかを読み取れる
- `JOIN` で2つの表をつないで、まとめて読める
- `LEFT JOIN` と `GROUP BY` を使い分けられる

かかる時間の目安は40分です。

## 始める前に

レッスン5-2（SQL でデータを書く）を終えている必要があります。

## なぜこれを覚えるのか

社員の表には部署の名前ではなく、部署の番号（`department_id`）が入っています。部署の名前は部署の表にだけ書いてあります。

このように表を分けておくと、部署の名前を変えたいときに、部署の表の1か所を直すだけで済みます。社員の表に名前をそのまま書いていたら、その部署の全員の行を直さなければなりません。

その代わり、「誰がどの部署にいるか」を読むには、2つの表をつなぐ必要があります。それが `JOIN` です。

psql の中に入っておきます。

```bash
cd ~/practice/compose1
docker compose up -d
docker compose exec db psql -U app -d practice
```

## 2つの表のつながりを見る

2つの表を並べると、つながりが分かります。

- `employees` の `department_id`
- `departments` の `id`

この2つの列が同じ値の行どうしが、対応しています。たとえば、佐藤さんの `department_id` は `1` で、`departments` の `id` が `1` の行は「総務部」です。

## つないで読む：JOIN

```sql
SELECT employees.name, departments.name
FROM employees
JOIN departments ON employees.department_id = departments.id
ORDER BY employees.id;
```

```text
 name |  name
------+--------
 佐藤 | 総務部
 鈴木 | 営業部
 高橋 | 開発部
 田中 | 営業部
 伊藤 | 開発部
(5 rows)
```

- `JOIN departments`：`departments` の表をつなぐ
- `ON employees.department_id = departments.id`：つなぐ条件。どの列とどの列が同じなら対応するか
- `employees.name`：どちらの表にも `name` の列があるので、「表の名前.列の名前」と書いて区別する

## 短く、読みやすく書く：AS

表の名前を毎回書くのは長いので、`AS` で短い別名を付けられます。列にも結果の見出しになる別名を付けられます。

```sql
SELECT e.name AS 社員, d.name AS 部署
FROM employees AS e
JOIN departments AS d ON e.department_id = d.id
ORDER BY e.id;
```

`employees` を `e`、`departments` を `d` と呼んでいます。結果の見出しも「社員」「部署」になり、どちらの `name` か迷わなくなります。

## 対応する相手がない行も残す：LEFT JOIN

さっきの結果は5行でした。社員は6人いるはずです。渡辺さんがいません。

渡辺さんの `department_id` は `NULL` なので、対応する部署がありません。`JOIN` は、両方の表に対応する行がある組だけを残すので、渡辺さんは結果から外れました。

対応する相手がない行も残したいときは、`LEFT JOIN` を使います。

```sql
SELECT e.name AS 社員, d.name AS 部署
FROM employees AS e
LEFT JOIN departments AS d ON e.department_id = d.id
ORDER BY e.id;
```

```text
 社員 |  部署
------+--------
 佐藤 | 総務部
 鈴木 | 営業部
 高橋 | 開発部
 田中 | 営業部
 伊藤 | 開発部
 渡辺 |
(6 rows)
```

`LEFT JOIN` は、左側（`FROM` に書いた方）の表の行をすべて残します。対応する部署がない渡辺さんも残り、部署の欄は空（`NULL`）になります。

:::caution[行が消えていないか確かめる]
`JOIN` を使うと、相手のない行が知らないうちに結果から消えます。一覧の件数が思ったより少ないときは、`JOIN` で行が落ちていないかを疑ってください。
:::

## まとめて数える：GROUP BY

部署ごとの人数を数えます。

```sql
SELECT d.name AS 部署, count(*) AS 人数
FROM employees AS e
JOIN departments AS d ON e.department_id = d.id
GROUP BY d.id, d.name
ORDER BY d.id;
```

```text
  部署  | 人数
--------+------
 総務部 |    1
 営業部 |    2
 開発部 |    2
(3 rows)
```

`GROUP BY` は「同じ値の行を1つのまとまりにする」という意味です。部署ごとにまとめてから、`count(*)` でそれぞれのまとまりの行の数を数えています。

## 困ったとき

- **「ERROR: column reference "name" is ambiguous」と出た**：どちらの表の `name` か分かりません。`e.name` のように、表の名前（別名）を付けてください。
- **「ERROR: column "e.name" must appear in the GROUP BY clause」と出た**：まとめた後の結果にはまとまりごとに1つに決まる値しか出せません。`SELECT` に並べる列を `GROUP BY` にも書くか、`count` などで数える形にしてください。
- **結果の行がとても多くなった**：`ON` の条件を書き間違えて、対応しない行どうしまでつながっています。`ON` の列の組み合わせを確かめてください。

## 確かめよう

psql の中で、次の SQL を自分で書いてください。

1. 営業部の人の名前と給料を、給料の高い順に（`JOIN` を使い、`WHERE d.name = '営業部'` で絞る）
2. 部署ごとの給料の合計（ヒント：`count(*)` の代わりに `sum(e.salary)`）

1が鈴木（`320000`）、田中（`260000`）の順の2行になれば完了です。2は、総務部・営業部・開発部の3行が出れば完了です。

## 今は知らなくてよいこと

- 3つ以上の表をつなぐ書き方
- `RIGHT JOIN` や `FULL JOIN`

## 次のレッスン

これで第5部は終わりです。次からは第6部です。画面を作るための言語の TypeScript を学ぶ前に、そのもとになっている JavaScript を学びます。
