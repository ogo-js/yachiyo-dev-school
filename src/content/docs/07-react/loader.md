---
title: loader でデータを取る
description: ページを表示する前に、サーバーで動く loader でデータを取り、画面に渡す
sidebar:
  order: 4
---

## このページでできるようになること

- `loader` を書いて、ページを表示する前にデータを取れる
- `loader` がサーバーで動き、コンポーネントがブラウザでも動くことを確かめられる
- データが見つからないときに、404を返せる

かかる時間の目安は45分です。

## 始める前に

レッスン7-3（ページと URL）を終えている必要があります。

## なぜ loader を使うのか

これまでは、社員のデータを画面のファイルから直接読んでいました。実際のアプリでは、データはデータベースにあり、API を通して取ってきます。取ってくるには時間がかかり（レッスン6-3）、パスワードのような、ブラウザに渡してはいけない情報を使うこともあります。

`loader` は、ページを表示する前に、サーバーの上で動く関数です。ここでデータを取ってから、コンポーネントに渡します。

- データを取る処理（サーバー）と、画面を描く処理（コンポーネント）を分けられる
- データがそろってから画面を描くので、「読み込み中」の途中の画面を考えなくてよい
- サーバーでしか使わない情報を、ブラウザに渡さずに済む

## データを取る関数にする

データのファイルを、API やデータベースから取ってくる形に近づけます。`app/data/employees.ts` の名前を `employees.server.ts` に変えます。

```bash
mv app/data/employees.ts app/data/employees.server.ts
```

中身を、次のように書き換えて保存します。

```tsx
export type Employee = {
  id: number;
  name: string;
  department: string;
};

const employees: Employee[] = [
  { id: 1, name: "佐藤", department: "総務部" },
  { id: 2, name: "鈴木", department: "営業部" },
  { id: 3, name: "高橋", department: "開発部" },
];

export async function getEmployees(): Promise<Employee[]> {
  return employees;
}

export async function getEmployee(id: number): Promise<Employee | undefined> {
  return employees.find((employee) => employee.id === id);
}
```

配列はそのまま外に出さず、取ってくるための `async` の関数だけを出します。今は配列を返しているだけですが、後でデータベースや API を使う形に変えても、呼ぶ側を直さずに済みます。

:::note[名前の .server]
ファイルの名前に `.server` が付いていると、React Router は、そのファイルをブラウザに送らないようにします。サーバーでしか使わないものを、うっかりブラウザに送ってしまうのを防げます。
:::

名前を変えたので、`employees.tsx` と `employee.tsx` の `import` がエラーになります。次の手順で直します。

## 一覧のページに loader を書く

`app/routes/employees.tsx` を、次のように書き換えて保存します。

```tsx
import { useState } from "react";
import { Link } from "react-router";
import type { Route } from "./+types/employees";
import { getEmployees } from "../data/employees.server";
import { EmployeeCard } from "../components/EmployeeCard";

export async function loader() {
  console.log("loader が動きました");
  const employees = await getEmployees();
  return { employees };
}

export default function Employees({ loaderData }: Route.ComponentProps) {
  const [keyword, setKeyword] = useState("");
  const shown = loaderData.employees.filter((employee) => employee.name.includes(keyword));

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

- `export async function loader()`：このページの `loader`。`loader` という名前で外に出すと、React Router がページを表示する前に呼ぶ
- `return { employees }`：返した値がコンポーネントに渡る
- `{ loaderData }`：`loader` が返した値を受け取る。型は `Route.ComponentProps` から自動で決まるので、`loaderData.employees` が社員の配列だと VS Code も分かっている

## loader はどこで動いているか

`/employees` を開いて、2つの場所を見比べます。

- `npm run dev` を動かしているターミナル：`loader が動きました` と出ている
- ブラウザの開発者ツールのコンソール：何も出ていない

`loader` はサーバーで動いています。一方、7-2の「いいね」のボタンの `console.log` はブラウザの開発者ツールに出ました。

| | 動く場所 |
| --- | --- |
| `loader` | サーバー |
| コンポーネントの中の、ボタンを押したときの処理 | ブラウザ |

トップから「社員一覧へ」のリンクで移ったときも、ターミナルに `loader が動きました` が出ます。リンクで移るときは、ブラウザが裏でサーバーに `loader` の結果だけをお願いしています。開発者ツールのネットワークのタブを見ると、そのリクエストが確かめられます。

## 詳しく見るページに loader を書く

`app/routes/employee.tsx` を、次のように書き換えて保存します。

```tsx
import { Link, data } from "react-router";
import type { Route } from "./+types/employee";
import { getEmployee } from "../data/employees.server";

export async function loader({ params }: Route.LoaderArgs) {
  const employee = await getEmployee(Number(params.id));
  if (!employee) {
    throw data("社員が見つかりません", { status: 404 });
  }
  return { employee };
}

export default function Employee({ loaderData }: Route.ComponentProps) {
  const { employee } = loaderData;
  return (
    <main>
      <h1>{employee.name}さん</h1>
      <p>部署：{employee.department}</p>
      <Link to="/employees">一覧に戻る</Link>
    </main>
  );
}
```

- `loader({ params })`：`loader` でも、URL の `:id` の部分を受け取れる
- `throw data("…", { status: 404 })`：見つからなかったら、ステータスコード404で止める。コンポーネントは呼ばれず、404のページが出る

コンポーネントの中から、「見つからなかったら」の分かれ道がなくなりました。`loader` が、見つかったときだけコンポーネントに社員を渡すからです。

`/employees/99` を開くと、404のページが出ます。開発者ツールのネットワークのタブでも、ステータスコードが `404` になっていることを確かめてください（レッスン3-1）。

## 困ったとき

- **「loaderData is undefined」のように出た**：`loader` を `export` し忘れています。`export async function loader()` と書いてください。
- **`loaderData.employees` に赤い波線が出る**：`import type { Route } from "./+types/employees";` のファイル名がページのファイル名と合っているか確かめてください。
- **`loader` の `console.log` がブラウザに出ない**：正しい動きです。`loader` の `console.log` はターミナルに出ます。

## 確かめよう

1. `employees.server.ts` に、部署の名前を受け取って、その部署の社員だけを返す `getEmployeesByDepartment` を足す
2. `routes.ts` に `departments/:name` という URL を足し、その部署の社員を一覧で表示するページを作る。データは `loader` で取る
3. 社員がいない部署（例：`/departments/人事部`）では、404を返す

`/departments/開発部` で高橋さんだけが表示され、`/departments/人事部` で404のページが出れば完了です。

## 今は知らなくてよいこと

- `loader` から本物の API を呼ぶ方法（第10部で扱います）
- ブラウザだけで動く `clientLoader`

## 次のレッスン

次はフォームから送られたデータを受け取って登録する `action` を学びます。
