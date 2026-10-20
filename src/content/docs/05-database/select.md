---
title: SQL でデータを読む
description: 練習用のデータを入れ、SELECT で条件を付けて検索し、並べ替える
sidebar:
  order: 1
---

## このページでできるようになること

- 練習用のデータをデータベースに入れられる
- `SELECT` で、必要な列と行だけを取り出せる
- 結果を並べ替えたり、件数を数えたりできる

かかる時間の目安は45分です。

## 始める前に

レッスン4-3（データを残す）を終え、`~/practice/compose1` でボリューム付きのデータベースを動かせる必要があります。

## なぜ SQL を覚えるのか

業務アプリのデータの多くは、データベースに「表」の形で保存されています。社員の一覧、取引の記録、商品の在庫などです。

SQL はデータベースに「この条件のデータをください」「このデータを登録して」とお願いするための言葉です。どんなに画面が新しくなっても、データベースとのやり取りの根っこには SQL があります。画面に出ている数字がおかしいときに、データベースの中身を自分で確かめられるようになると、原因を探すのがずっと楽になります。

## 練習用のデータを入れる

データベースを動かします。

```bash
cd ~/practice/compose1
docker compose up -d
```

練習用のデータを書いたファイルを作ります。

```bash
touch sample.sql
code sample.sql
```

次の内容を貼り付けて保存します。部署の表と社員の表を作り、データを入れる SQL です。

```sql
CREATE TABLE departments (
  id   integer PRIMARY KEY,
  name text NOT NULL
);

CREATE TABLE employees (
  id            integer PRIMARY KEY,
  name          text NOT NULL,
  department_id integer REFERENCES departments(id),
  salary        integer NOT NULL,
  hired_on      date NOT NULL
);

INSERT INTO departments (id, name) VALUES
  (1, '総務部'),
  (2, '営業部'),
  (3, '開発部');

INSERT INTO employees (id, name, department_id, salary, hired_on) VALUES
  (1, '佐藤', 1, 280000, '2018-04-01'),
  (2, '鈴木', 2, 320000, '2015-04-01'),
  (3, '高橋', 3, 350000, '2016-10-01'),
  (4, '田中', 2, 250000, '2022-04-01'),
  (5, '伊藤', 3, 300000, '2020-04-01'),
  (6, '渡辺', NULL, 230000, '2024-04-01');
```

ファイルの中身を、データベースに流し込みます。

```bash
docker compose exec -T db psql -U app -d practice < sample.sql
```

`CREATE TABLE` や `INSERT 0 3` のような行が出れば入っています。`<` は「このファイルの中身を、コマンドへの入力として渡す」という意味です。`-T` は、ファイルから入力を渡すときに付ける指定です。

## psql の中に入る

ここからは、データベースの中に入って、SQL を1つずつ打っていきます。

```bash
docker compose exec db psql -U app -d practice
```

```text
practice=#
```

プロンプトが `practice=#` に変わりました。ここで打つものは Ubuntu のコマンドではなく、データベースへのお願いになります。

表の一覧を見ます。`\` で始まるものは psql の便利な命令です。

```sql
\dt
```

```text
          List of relations
 Schema |    Name     | Type  | Owner
--------+-------------+-------+-------
 public | departments | table | app
 public | employees   | table | app
(2 rows)
```

psql から出るときは、`\q` と打ちます。

## すべてを取り出す：SELECT

```sql
SELECT * FROM employees;
```

```text
 id | name | department_id | salary |  hired_on
----+------+---------------+--------+------------
  1 | 佐藤 |             1 | 280000 | 2018-04-01
  2 | 鈴木 |             2 | 320000 | 2015-04-01
  3 | 高橋 |             3 | 350000 | 2016-10-01
  4 | 田中 |             2 | 250000 | 2022-04-01
  5 | 伊藤 |             3 | 300000 | 2020-04-01
  6 | 渡辺 |               | 230000 | 2024-04-01
(6 rows)
```

「`employees` の表から、すべての列（`*`）を取り出す」という意味です。SQL の最後には必ず `;` を付けます。

渡辺さんの `department_id` は空になっています。値が入っていないことを、SQL では `NULL` と呼びます。

:::tip[`;` を忘れたら]
`;` を付けずに Enter キーを押すと、プロンプトが `practice-#` に変わり、続きを待つ状態になります。`;` だけを打って Enter キーを押せば、そこまでの SQL が実行されます。
:::

## 列を選ぶ

必要な列だけを、`,` で区切って並べます。

```sql
SELECT name, salary FROM employees;
```

名前と給料の2列だけが出ます。

## 条件で絞る：WHERE

給料が30万円以上の人だけを取り出します。

```sql
SELECT name, salary FROM employees WHERE salary >= 300000;
```

```text
 name | salary
------+--------
 鈴木 | 320000
 高橋 | 350000
 伊藤 | 300000
(3 rows)
```

条件には、次のような書き方が使えます。

| 書き方 | 意味 |
| --- | --- |
| `=` | 等しい |
| `<>` | 等しくない |
| `>`、`>=`、`<`、`<=` | 大きい、以上、小さい、以下 |
| `AND` | どちらも当てはまる |
| `OR` | どちらかが当てはまる |
| `LIKE '%藤'` | 「藤」で終わる（`%` は「何文字でもよい何か」） |
| `IS NULL` | 値が入っていない |

`AND` を使って、条件を2つ重ねてみます。

```sql
SELECT name FROM employees WHERE department_id = 2 AND salary < 300000;
```

```text
 name
------
 田中
(1 row)
```

文字の値は `'佐藤'` のように一重の引用符で囲みます。

## 並べ替える：ORDER BY

入社日の古い順に並べます。

```sql
SELECT name, hired_on FROM employees ORDER BY hired_on;
```

```text
 name |  hired_on
------+------------
 鈴木 | 2015-04-01
 高橋 | 2016-10-01
 佐藤 | 2018-04-01
 伊藤 | 2020-04-01
 田中 | 2022-04-01
 渡辺 | 2024-04-01
(6 rows)
```

大きい順（新しい順）にするときは、後ろに `DESC` を付けます。`LIMIT` で、取り出す件数を決められます。

```sql
SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3;
```

```text
 name | salary
------+--------
 高橋 | 350000
 鈴木 | 320000
 伊藤 | 300000
(3 rows)
```

:::caution[並び順は指定しないと決まらない]
`ORDER BY` を付けないときの並び順は、決まっていません。同じ SQL でも、いつも同じ順で出てくるとは限りません。順番が大事なときは、必ず `ORDER BY` を付けてください。
:::

## 数える：count

```sql
SELECT count(*) FROM employees;
```

```text
 count
-------
     6
(1 row)
```

`WHERE` と組み合わせると、条件に合う件数を数えられます。

## 困ったとき

- **「ERROR: relation "employees" does not exist」と出た**：表がありません。`sample.sql` を流し込んだか、`\dt` で確かめてください。
- **「ERROR: syntax error at or near …」と出た**：SQL の書き方が崩れています。`…` の部分の近くに、綴りの誤りや `,` の過不足がないか確かめてください。
- **「ERROR: column "佐藤" does not exist」と出た**：文字の値を `" "` で囲んでいます。文字の値は `' '`（一重の引用符）で囲んでください。

## 確かめよう

psql の中で、次の SQL を自分で書いてください。

1. 開発部（`department_id` が3）の人の名前と給料
2. 2020年より後（`hired_on` が `'2020-01-01'` より後）に入社した人の名前を、入社日の新しい順に
3. 給料が25万円以上30万円未満の人の数

1が高橋と伊藤の2行、2が渡辺・田中・伊藤の順の3行、3が `2` になれば完了です。

## 今は知らなくてよいこと

- 合計や平均の出し方（`sum`、`avg`）
- 表の作り方（`CREATE TABLE`）の細かい書き方

## 次のレッスン

次はデータを足したり、変えたり、消したりする SQL を学びます。
