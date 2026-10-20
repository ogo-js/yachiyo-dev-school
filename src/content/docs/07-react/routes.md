---
title: ページと URL
description: URL ごとにページを分け、リンクで移動し、URL の一部を受け取る
sidebar:
  order: 3
---

## このページでできるようになること

- `routes.ts` に、URL とページのファイルの組を書ける
- `Link` で、ページの間を移動できる
- `/employees/2` のような URL から、`2` の部分を受け取って使える

かかる時間の目安は45分です。

## 始める前に

レッスン7-2（状態とイベント）を終えている必要があります。

## なぜこれを覚えるのか

アプリには一覧のページ、詳しく見るページ、登録のページのように、たくさんのページがあります。それぞれに URL があると、ブックマークできたり、URL を人に送って同じページを見てもらえたりします。

React Router はその名前のとおり、URL とページの組み合わせ（ルート）を扱う仕組みです。

## データを別のファイルに分ける

社員のデータを、いくつかのページから使えるように、別のファイルに分けます。

```bash
mkdir -p app/data
touch app/data/employees.ts
code app/data/employees.ts
```

```tsx
export type Employee = {
  id: number;
  name: string;
  department: string;
};

export const employees: Employee[] = [
  { id: 1, name: "佐藤", department: "総務部" },
  { id: 2, name: "鈴木", department: "営業部" },
  { id: 3, name: "高橋", department: "開発部" },
];
```

## URL とページの組を書く：routes.ts

`app/routes.ts` を、次のように書き換えて保存します。

```ts
import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("employees", "routes/employees.tsx"),
  route("employees/:id", "routes/employee.tsx"),
] satisfies RouteConfig;
```

| 書き方 | URL | 表示するファイル |
| --- | --- | --- |
| `index("routes/home.tsx")` | `/` | `app/routes/home.tsx` |
| `route("employees", "routes/employees.tsx")` | `/employees` | `app/routes/employees.tsx` |
| `route("employees/:id", "routes/employee.tsx")` | `/employees/1` など | `app/routes/employee.tsx` |

`:id` は「ここには何が入ってもよい。入ったものを `id` という名前で受け取る」という意味です。

この時点では、まだ `employees.tsx` と `employee.tsx` がないので、ターミナルにエラーが出ます。次の手順でファイルを作ると消えます。

## 一覧のページ

`app/routes/employees.tsx` を作り、7-2で `home.tsx` に書いた一覧を移します。

```tsx
import { useState } from "react";
import { Link } from "react-router";
import { employees } from "../data/employees";
import { EmployeeCard } from "../components/EmployeeCard";

export default function Employees() {
  const [keyword, setKeyword] = useState("");
  const shown = employees.filter((employee) => employee.name.includes(keyword));

  return (
    <main>
      <h1>社員一覧</h1>
      <input value={keyword} onChange={(event) => setKeyword(event.target.value)} placeholder="名前で絞る" />
      {shown.map((employee) => (
        <div key={employee.id}>
          <EmployeeCard name={employee.name} department={employee.department} />
          <Link to={`/employees/${employee.id}`}>詳しく見る</Link>
        </div>
      ))}
    </main>
  );
}
```

`Link` は、別のページへ移るためのリンクです。`to` に、移り先の URL を書きます。

## トップのページ

`app/routes/home.tsx` は、一覧へのリンクだけにします。

```tsx
import { Link } from "react-router";

export default function Home() {
  return (
    <main>
      <h1>トップ</h1>
      <Link to="/employees">社員一覧へ</Link>
    </main>
  );
}
```

## 詳しく見るページ：URL の一部を受け取る

`app/routes/employee.tsx` を作ります。

```tsx
import { Link } from "react-router";
import type { Route } from "./+types/employee";
import { employees } from "../data/employees";

export default function Employee({ params }: Route.ComponentProps) {
  const employee = employees.find((e) => e.id === Number(params.id));

  if (!employee) {
    return <p>社員が見つかりません</p>;
  }

  return (
    <main>
      <h1>{employee.name}さん</h1>
      <p>部署：{employee.department}</p>
      <Link to="/employees">一覧に戻る</Link>
    </main>
  );
}
```

- `params.id`：URL の `:id` の部分に入っていた文字。`/employees/2` なら `"2"`
- `Number(params.id)`：文字の `"2"` を、数の `2` に変える。`id` は数なので、そろえてから比べる
- `find`：配列の中から、条件に合う最初の1つを探す。見つからなければ `undefined` になる

`import type { Route } from "./+types/employee";` は、このページのための型を読み込んでいます。React Router が `routes.ts` の内容から自動で作ってくれます。`params` に `id` があることも、この型が知っています。

ブラウザで `http://localhost:5173` を開き、「社員一覧へ」→「詳しく見る」→「一覧に戻る」と移動できることを確かめてください。

## Link と a の違い

HTML の `<a href="…">` でも移動はできます。違いは移動のしかたです。

- `<a>`：ページ全体をサーバーから読み込み直す
- `Link`：必要な部分だけを入れ替える。速く、入力中の状態なども失われにくい

アプリの中のページへの移動には `Link` を使います。

## ないページを開く

`http://localhost:5173/nothing` を開くと、「404」「The requested page could not be found.」と表示されます。`routes.ts` にない URL なので、React Router が404のページを出しています。この表示は `app/root.tsx` の中で決められています。

## 困ったとき

- **ターミナルに「Could not find route module」のように出た**：`routes.ts` に書いたファイルの名前と、実際のファイルの名前が違います。
- **`./+types/employee` が見つからないと赤い波線が出る**：型は、開発用のサーバーが動いているときに自動で作られます。`npm run dev` を動かしてから、少し待ってください。
- **「社員が見つかりません」と出る**：`Number(params.id)` で数に変えずに比べていないか確かめてください。

## 確かめよう

1. `routes.ts` に `about` という URL を足し、「このアプリについて」と表示する `app/routes/about.tsx` を作る
2. トップのページに、`/about` へのリンクを足す
3. `/employees/3` を直接開いて高橋さんが表示され、`/employees/99` を開いて「社員が見つかりません」と表示されることを確かめる

トップから「このアプリについて」へ移動でき、3の2つの表示が確かめられれば完了です。

## 今は知らなくてよいこと

- ページの外枠を共通にする書き方（レイアウト）
- URL の `?` の後ろ（クエリ文字列）を読む方法

## 次のレッスン

次はページを表示する前に、サーバーでデータを取ってくる `loader` を学びます。
