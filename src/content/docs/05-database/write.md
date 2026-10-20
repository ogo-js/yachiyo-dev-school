---
title: SQL でデータを書く
description: INSERT・UPDATE・DELETE でデータを変え、トランザクションで取り消せるようにする
sidebar:
  order: 2
---

## このページでできるようになること

- `INSERT` で行を足せる
- `UPDATE` と `DELETE` で、条件に合う行だけを変えたり消したりできる
- トランザクションを使って、変更を確かめてから確定したり、取り消したりできる

かかる時間の目安は40分です。

## 始める前に

レッスン5-1（SQL でデータを読む）を終え、練習用のデータが入っている必要があります。

## なぜこれを覚えるのか

画面で「登録」「更新」「削除」のボタンを押したとき、データベースの中では、このレッスンで扱う SQL が動いています。

データを読むだけの `SELECT` は、何度打っても中身は変わりません。一方、このレッスンの SQL は中身を変えます。打ち間違えると、たくさんのデータを一度に壊してしまうこともあります。安全に使うための習慣も一緒に身につけます。

psql の中に入っておきます。

```bash
cd ~/practice/compose1
docker compose up -d
docker compose exec db psql -U app -d practice
```

## 行を足す：INSERT

新しい社員を1人足します。

```sql
INSERT INTO employees (id, name, department_id, salary, hired_on)
VALUES (7, '山本', 1, 240000, '2025-04-01');
```

```text
INSERT 0 1
```

`INSERT 0 1` の最後の `1` は「1行足した」という意味です。表の名前の後ろに列の名前を並べ、`VALUES` の後ろに、同じ順番で値を並べます。

`SELECT * FROM employees;` で、山本さんが増えたことを確かめてください。

同じ `id` の行をもう一度足そうとすると、エラーになります。

```sql
INSERT INTO employees (id, name, department_id, salary, hired_on)
VALUES (7, '中村', 1, 240000, '2025-04-01');
```

```text
ERROR:  duplicate key value violates unique constraint "employees_pkey"
DETAIL:  Key (id)=(7) already exists.
```

`id` は、表を作るときに `PRIMARY KEY`（主キー）として決めた列です。主キーは行を見分けるための値なので、同じ値を2つ入れることはできません。

## 値を変える：UPDATE

田中さん（`id` が4）の給料を26万円に変えます。

```sql
UPDATE employees SET salary = 260000 WHERE id = 4;
```

```text
UPDATE 1
```

`UPDATE 1` は「1行変えた」という意味です。`SET` の後ろに変える列と値を、`WHERE` の後ろにどの行を変えるかを書きます。

:::danger[WHERE を忘れると、すべての行が変わる]
`UPDATE` で `WHERE` を書き忘れると、表のすべての行が変わります。`DELETE` も同じで、すべての行が消えます。データベースにはごみ箱も「元に戻す」ボタンもありません。
:::

## 行を消す：DELETE

さっき足した山本さんを消します。

```sql
DELETE FROM employees WHERE id = 7;
```

```text
DELETE 1
```

## 変える前に、確かめる

`UPDATE` や `DELETE` を打つ前には、同じ `WHERE` を付けた `SELECT` で、対象の行を確かめる習慣を付けてください。

```sql
SELECT * FROM employees WHERE id = 4;
```

ここで出てきた行だけが同じ `WHERE` を付けた `UPDATE` や `DELETE` の対象になります。出てきた件数と、実行した後の `UPDATE 1` や `DELETE 1` の数が合っているかも確かめます。

## 取り消せるようにする：トランザクション

いくつかの変更を「ひとまとまり」として扱い、最後にまとめて確定したり、まとめて取り消したりする仕組みを「トランザクション」と呼びます。

`BEGIN;` と打つと、トランザクションが始まります。

```sql
BEGIN;
UPDATE employees SET salary = 0;
```

```text
BEGIN
UPDATE 6
```

`WHERE` を忘れて、全員の給料を0にしてしまいました。確かめます。

```sql
SELECT name, salary FROM employees ORDER BY id LIMIT 2;
```

```text
 name | salary
------+--------
 佐藤 |      0
 鈴木 |      0
(2 rows)
```

トランザクションの中なので、まだ確定していません。`ROLLBACK;` で取り消せます。

```sql
ROLLBACK;
SELECT name, salary FROM employees ORDER BY id LIMIT 2;
```

```text
ROLLBACK
 name | salary
------+--------
 佐藤 | 280000
 鈴木 | 320000
(2 rows)
```

元に戻りました。正しい変更だったときは、`ROLLBACK;` の代わりに `COMMIT;` と打つと確定します。

:::tip[手で変更するときは BEGIN から]
データベースの中身を手で直すときは、`BEGIN;` で始めて、`SELECT` で結果を確かめてから `COMMIT;` する習慣を付けてください。間違えても `ROLLBACK;` でやり直せます。
:::

## 困ったとき

- **「ERROR: current transaction is aborted」と出た**：トランザクションの途中でエラーが起きたので、それ以降の SQL が受け付けられなくなっています。`ROLLBACK;` で取り消してから、やり直してください。
- **「ERROR: insert or update on table "employees" violates foreign key constraint」と出た**：`department_id` に、部署の表にない番号を入れようとしています。部署の表にある番号（1〜3）か、`NULL` を使ってください。

## 確かめよう

psql の中で、次のことをやってみてください。

1. `BEGIN;` でトランザクションを始める
2. 開発部（`department_id` が3）の全員の給料を、1万円ずつ上げる（ヒント：`SET salary = salary + 10000`）
3. `SELECT` で、高橋さんが36万円、伊藤さんが31万円になったことを確かめる
4. `COMMIT;` で確定する
5. psql を `\q` で出て、もう一度入り、開発部の2人の給料が変わったままであることを確かめる

5で高橋さんが `360000`、伊藤さんが `310000` なら完了です。

## 今は知らなくてよいこと

- 複数の人が同時にデータを変えたときに起きる問題と、その防ぎ方
- 表の形を後から変える方法（`ALTER TABLE`）

## 次のレッスン

次は社員の表と部署の表をつないで、「誰がどの部署にいるか」をまとめて読みます。
