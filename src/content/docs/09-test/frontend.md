---
title: TypeScript のテスト
description: 入力の確かめをテストから先に書き、React のコンポーネントを Testing Library でテストする
sidebar:
  order: 3
---

## このページでできるようになること

- テストを先に書いてから、そのテストが通るようにロジックを書ける
- `action` の中のロジックを関数に分けて、テストしやすくできる
- Testing Library で、コンポーネントの表示とボタンの動きを確かめられる

かかる時間の目安は60分です。

## 始める前に

レッスン9-1（なぜ自動テストを書くのか）と、第7部（React と React Router）を終えている必要があります。このレッスンでは `~/practice/rr1` を使います。

## なぜこれを覚えるのか

画面のプログラムには、2種類のものが混ざっています。

- ロジック：入力の確かめ、計算、データの組み立てなど。決まった値を渡せば、決まった結果が返る
- 見た目と操作：何が表示されるか、ボタンを押したら何が起きるか

ロジックはレッスン9-1と同じように関数のテストで確かめられます。決まりがはっきりしているので、テストを先に書いて決まりを固めてから、作り始めることもできます。見た目と操作は、Testing Library という道具で、利用者と同じように画面を操作して確かめます。

## 準備する

```bash
cd ~/practice/rr1
npm install --save-dev vitest jsdom @testing-library/react @testing-library/user-event
```

- `jsdom`：ブラウザの代わりになる仕組み。テストの中で、画面を組み立てられるようにする
- `@testing-library/react`：コンポーネントを組み立てて、中身を探す道具
- `@testing-library/user-event`：クリックや文字の入力を、利用者と同じように行う道具

テストの設定のファイル `vitest.config.ts` を、`rr1` のすぐ下に作ります。

```typescript
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "jsdom",
  },
});
```

`environment: "jsdom"` は、「テストを、ブラウザの代わりの仕組みの中で動かす」という設定です。

## テストを先に書く

7-5で、`action` の中に入力の確かめを書きました。この確かめを関数に分けて、テストしやすくします。

まず、作りたい関数の決まりを、テストとして書きます。まだ関数はありません。`app/data/validation.test.ts` を作ります。

```typescript
import { expect, test } from "vitest";
import { validateEmployee } from "./validation";

test("名前と部署があれば誤りはない", () => {
  expect(validateEmployee("田中", "営業部")).toEqual({});
});

test("名前が空なら知らせる", () => {
  expect(validateEmployee("", "営業部")).toEqual({ name: "名前を入れてください" });
});

test("名前が空白だけでも知らせる", () => {
  expect(validateEmployee("   ", "営業部")).toEqual({ name: "名前を入れてください" });
});

test("部署が空なら知らせる", () => {
  expect(validateEmployee("田中", "")).toEqual({ department: "部署を選んでください" });
});
```

`toEqual` は、オブジェクトの中身が同じかを確かめます（`toBe` は、数や文字のような1つの値を比べるときに使います）。

動かすと、失敗します。

```bash
npx vitest run
```

```text
Error: Failed to resolve import "./validation" from "app/data/validation.test.ts". Does the file exist?
```

関数がまだないので、当然です。ここで、テストが関数の決まりの説明書になっていることに注目してください。空白だけの名前も誤りにする、という決まりは、7-5のときには `trim()` の中に埋もれていて、読み取りにくいものでした。

## テストが通るように書く

`app/data/validation.ts` を作ります。

```typescript
export type EmployeeErrors = {
  name?: string;
  department?: string;
};

export function validateEmployee(name: string, department: string): EmployeeErrors {
  const errors: EmployeeErrors = {};
  if (name.trim() === "") {
    errors.name = "名前を入れてください";
  }
  if (department === "") {
    errors.department = "部署を選んでください";
  }
  return errors;
}
```

```bash
npx vitest run
```

```text
 ✓ app/data/validation.test.ts (4 tests) 7ms

 Test Files  1 passed (1)
      Tests  4 passed (4)
```

すべて通りました。「テストを書く → 失敗する → 通るように書く」の順に進めるやり方を「テスト駆動開発」と呼びます。

## action から使う

`app/routes/employee-new.tsx` の `action` を、この関数を使う形に書き換えます。ファイルの先頭に `import` を1行足し、`action` を次のようにします。

```tsx
import { validateEmployee } from "../data/validation";
```

```tsx
export async function action({ request }: Route.ActionArgs) {
  const formData = await request.formData();
  const name = String(formData.get("name") ?? "").trim();
  const department = String(formData.get("department") ?? "");

  const errors = validateEmployee(name, department);
  if (errors.name || errors.department) {
    return data({ errors }, { status: 400 });
  }

  await addEmployee(name, department);
  return redirect("/employees");
}
```

`action` は「受け取る・確かめる・登録する」の流れだけになり、確かめの中身はテストで守られた関数に任せる形になりました。`npm run dev` で、7-5と同じように動くことを確かめてください。

## コンポーネントをテストする

7-2で作った `EmployeeCard` を、テストで確かめます。`app/components/EmployeeCard.test.tsx` を作ります。

```tsx
import { afterEach, expect, test } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { EmployeeCard } from "./EmployeeCard";

afterEach(() => {
  cleanup();
});

test("名前と部署を表示する", () => {
  render(<EmployeeCard name="佐藤" department="総務部" />);

  expect(screen.getByRole("heading", { name: "佐藤" })).toBeDefined();
  expect(screen.getByText("総務部")).toBeDefined();
});

test("いいねを押すと数が増える", async () => {
  const user = userEvent.setup();
  render(<EmployeeCard name="佐藤" department="総務部" />);

  await user.click(screen.getByRole("button", { name: "いいね（0）" }));

  expect(screen.getByRole("button", { name: "いいね（1）" })).toBeDefined();
});
```

- `render(<EmployeeCard … />)`：コンポーネントを、ブラウザの代わりの仕組みの中に組み立てる
- `screen.getByRole("heading", { name: "佐藤" })`：「佐藤」という見出しを探す。見つからなければ、テストはその場で失敗する
- `screen.getByText("総務部")`：「総務部」という文字を探す
- `user.click(…)`：見つけたボタンを押す。押す処理は待つ処理なので `await` を付ける
- `afterEach(() => { cleanup(); })`：テストを1つ終えるたびに、組み立てた画面を片付ける

```bash
npx vitest run
```

```text
 ✓ app/data/validation.test.ts (4 tests) 7ms
 ✓ app/components/EmployeeCard.test.tsx (2 tests) 420ms

 Test Files  2 passed (2)
      Tests  6 passed (6)
```

:::tip[利用者と同じ探し方をする]
`getByRole` は、「見出し」「ボタン」のような役割と、そこに書かれた文字で探します。利用者も画面を「ボタンに『いいね』と書いてある」のように見ています。利用者と同じ探し方をしておくと、見た目を整えるためにコードを書き換えても、テストが壊れにくくなります。
:::

## どちらをテストで守るか

| | ロジック | コンポーネント |
| --- | --- | --- |
| 例 | 入力の確かめ、計算 | 表示、ボタンの動き |
| テストの書きやすさ | 書きやすい。値を渡して結果を比べるだけ | 画面を組み立てるので、手間がかかる |
| テストを先に書くか | 先に書きやすい | 見た目を作りながら、後から書くことが多い |

大事な決まりはできるだけロジックとしてコンポーネントの外に出し、関数のテストで守ります。コンポーネントのテストは利用者の操作で大事な流れに絞って書きます。

## 困ったとき

- **「document is not defined」と出た**：`vitest.config.ts` がないか、`environment: "jsdom"` が書かれていません。
- **「Unable to find an accessible element with the role "button" and name …」と出た**：探している文字と、画面に出ている文字が違います。全角と半角の括弧の違いなど、1文字ずつ確かめてください。
- **2つ目のテストで「Found multiple elements」と出た**：前のテストで組み立てた画面が残っています。`afterEach` の `cleanup()` を書き忘れていないか確かめてください。

## 確かめよう

1. `validation.test.ts` に、「名前が21文字以上なら『名前は20文字以内で入れてください』と知らせる」テストを先に書き、失敗することを確かめる
2. `validateEmployee` を直して、テストを通す
3. 7-2の検索欄のように、名前で絞り込む部品を `EmployeeSearch` として作り、「文字を入れると、その文字を含む人だけが表示される」ことを確かめるテストを書く（ヒント：`user.type(入力欄, "藤")`、入力欄は `screen.getByPlaceholderText("名前で絞る")` で探せる）

`npx vitest run` で、すべてのテストが通れば完了です。

## 今は知らなくてよいこと

- `loader` や `action` を含めた、ページ全体のテストの書き方
- ブラウザを実際に動かして確かめるテスト（E2E テスト）

## 次のレッスン

これで第9部は終わりです。次は第10部、総仕上げです。ここまでのすべてを組み合わせて、小さな業務アプリを作ります。
