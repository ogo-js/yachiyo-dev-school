---
title: action でフォームを受ける
description: フォームの送信を action で受け取って登録し、入力の誤りを画面に出す
sidebar:
  order: 5
---

## このページでできるようになること

- `Form` と `action` で、フォームの送信を受け取って登録できる
- 入力の誤りを見つけて、画面に知らせられる
- 登録した後に、別のページへ移せる

かかる時間の目安は60分です。

## 始める前に

レッスン7-4（loader でデータを取る）を終えている必要があります。

## なぜ action を使うのか

レッスン3-2で、データを変えるお願いは POST で送る、と学びました。`action` は、ページに POST で送られてきたフォームを、サーバーの上で受け取る関数です。

`loader` が「表示する前にデータを取る」係なら、`action` は「送られてきたデータで登録・更新する」係です。登録が終わると、React Router は、表示中のページの `loader` を自動でもう一度動かします。登録した結果が何もしなくても画面に反映されます。

## 登録する関数を足す

`app/data/employees.server.ts` の最後に、次の関数を書き足して保存します。

```tsx
export async function addEmployee(name: string, department: string): Promise<Employee> {
  const employee = { id: employees.length + 1, name, department };
  employees.push(employee);
  return employee;
}
```

:::note
この練習のデータはサーバーのメモリの中にあるだけなので、`npm run dev` を止めると、登録した社員は消えます。データベースに残す方法は、第10部で扱います。
:::

## 登録のページを作る

`app/routes.ts` に、登録のページの URL を足します。

```ts
import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("employees", "routes/employees.tsx"),
  route("employees/new", "routes/employee-new.tsx"),
  route("employees/:id", "routes/employee.tsx"),
] satisfies RouteConfig;
```

`app/routes/employee-new.tsx` を作ります。

```tsx
import { Form, redirect } from "react-router";
import type { Route } from "./+types/employee-new";
import { addEmployee } from "../data/employees.server";

export async function action({ request }: Route.ActionArgs) {
  const formData = await request.formData();
  const name = String(formData.get("name") ?? "").trim();
  const department = String(formData.get("department") ?? "");

  await addEmployee(name, department);
  return redirect("/employees");
}

export default function EmployeeNew() {
  return (
    <main>
      <h1>社員の登録</h1>
      <Form method="post">
        <p>
          <label>
            名前：<input name="name" />
          </label>
        </p>
        <p>
          <label>
            部署：
            <select name="department" defaultValue="">
              <option value="">選んでください</option>
              <option value="総務部">総務部</option>
              <option value="営業部">営業部</option>
              <option value="開発部">開発部</option>
            </select>
          </label>
        </p>
        <button type="submit">登録する</button>
      </Form>
    </main>
  );
}
```

`app/routes/employees.tsx` の `</main>` のすぐ上に、登録のページへのリンクを足します。

```tsx
      <Link to="/employees/new">社員を登録する</Link>
```

## 流れを追う

一覧のページから「社員を登録する」へ移り、名前に「田中」、部署に「営業部」を入れて「登録する」を押します。一覧のページに戻り、田中さんが増えています。

裏では、次のことが起きています。

1. `Form method="post"` が、入力した値を POST で今のページ（`/employees/new`）に送る
2. React Router がそのページの `action` を呼ぶ
3. `request.formData()` で、送られた値を受け取る。`formData.get("name")` の `"name"` は `<input name="name" />` の `name` と同じ
4. `addEmployee` で登録する
5. `redirect("/employees")` で、一覧のページへ移す
6. 一覧のページの `loader` が動き、田中さんを含む一覧が表示される

`Form` は、React Router が用意したフォームです。HTML の `<form>` と同じように書けますが、ページ全体を読み込み直さずに送れます。

## 入力の誤りを知らせる

名前を空のまま「登録する」を押すと、名前のない社員が登録されてしまいます。送られてきた値を確かめて、誤りがあれば知らせるようにします。

`employee-new.tsx` を、次のように書き換えて保存します。

```tsx
import { Form, data, redirect } from "react-router";
import type { Route } from "./+types/employee-new";
import { addEmployee } from "../data/employees.server";

export async function action({ request }: Route.ActionArgs) {
  const formData = await request.formData();
  const name = String(formData.get("name") ?? "").trim();
  const department = String(formData.get("department") ?? "");

  const errors: { name?: string; department?: string } = {};
  if (name === "") {
    errors.name = "名前を入れてください";
  }
  if (department === "") {
    errors.department = "部署を選んでください";
  }
  if (errors.name || errors.department) {
    return data({ errors }, { status: 400 });
  }

  await addEmployee(name, department);
  return redirect("/employees");
}

export default function EmployeeNew({ actionData }: Route.ComponentProps) {
  return (
    <main>
      <h1>社員の登録</h1>
      <Form method="post">
        <p>
          <label>
            名前：<input name="name" />
          </label>
        </p>
        {actionData?.errors.name && <p>{actionData.errors.name}</p>}
        <p>
          <label>
            部署：
            <select name="department" defaultValue="">
              <option value="">選んでください</option>
              <option value="総務部">総務部</option>
              <option value="営業部">営業部</option>
              <option value="開発部">開発部</option>
            </select>
          </label>
        </p>
        {actionData?.errors.department && <p>{actionData.errors.department}</p>}
        <button type="submit">登録する</button>
      </Form>
    </main>
  );
}
```

- `errors`：誤りがあった項目と、その知らせ方を集める
- `return data({ errors }, { status: 400 })`：誤りがあれば登録せず、`errors` を返す。ステータスコードは「お願いの形がおかしい」の400
- `{ actionData }`：`action` が返した値を受け取る。まだ送っていないときは `undefined` なので、`actionData?.` と `?` を付けて読む
- `{actionData?.errors.name && <p>…</p>}`：名前の誤りがあるときだけ、知らせる文を表示する

何も入れずに「登録する」を押すと、2つの知らせが表示されます。

:::caution[確かめるのはサーバーで]
入力欄に `required` を付けると、ブラウザも空欄を止めてくれます。ただし、ブラウザの確かめは開発者ツールなどで簡単にすり抜けられます（レッスン3-4で Cookie を書き換えたのと同じです）。登録してよいかの判断は必ずサーバーの `action` で行います。
:::

## loader と action のまとめ

| | loader | action |
| --- | --- | --- |
| 呼ばれるとき | ページを表示する前（GET） | フォームが送られたとき（POST） |
| 役割 | データを取る | データを登録・更新する |
| 動く場所 | サーバー | サーバー |
| 結果を受け取る名前 | `loaderData` | `actionData` |

## 困ったとき

- **登録しても一覧に増えない**：`npm run dev` を止めて動かし直していないか確かめてください。動かし直すと、登録した社員は消えます。
- **`/employees/new` を開くと404が出る**：`routes.ts` に `employees/new` を書き足したか、ファイルの名前が `employee-new.tsx` になっているか確かめてください。
- **`formData.get("name")` が空になる**：`<input>` に `name="name"` を書き忘れていないか確かめてください。

## 確かめよう

1. 登録のページに「入社年」（`year`）の入力欄を足す
2. `action` で、入社年が空のときと、数でないときに、それぞれ「入社年を入れてください」「入社年は数で入れてください」と知らせる（ヒント：`Number.isNaN(Number(year))`）
3. 正しく入れたときは登録して一覧に戻る。`Employee` 型と `addEmployee` にも入社年を足す

入社年を空にしたとき、「abc」と入れたとき、「2024」と入れたときで、それぞれ正しく動けば完了です。

## 今は知らなくてよいこと

- 入力した値を、誤りがあったときに入力欄に残す方法
- 送信中に「登録中…」と表示する方法

## 次のレッスン

これで第7部は終わりです。画面の側はひととおり作れるようになりました。次からは第8部です。画面から呼ばれる API を、C# と ASP.NET Core で作ります。
