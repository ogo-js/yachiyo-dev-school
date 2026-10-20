---
title: コンポーネントを作る
description: React Router のプロジェクトを作り、画面を部品（コンポーネント）に分けて組み立てる
sidebar:
  order: 1
---

## このページでできるようになること

- React Router のプロジェクトを作って、開発用のサーバーを動かせる
- コンポーネントを作り、値（props）を渡して表示できる
- 配列から、コンポーネントの一覧を作れる

かかる時間の目安は60分です。

## 始める前に

第6部（TypeScript）を終えている必要があります。

## なぜ React を使うのか

画面には、同じ形をした部分がたくさんあります。社員の一覧なら、名前と部署を表示する欄が、人数分だけ並びます。

React は画面を「コンポーネント」という部品に分けて作る仕組みです。部品を1つ作れば、中身を変えながら何度でも使えます。部品の見た目を直したいときも、部品の1か所を直せば、すべての場所に反映されます。

React Router は React で作った画面に、ページの切り替えや、サーバーとのデータのやり取りの仕組みを足したものです。この教材では最初から React Router のプロジェクトとして作ります。

## プロジェクトを作る

```bash
cd ~/practice
npx create-react-router@latest rr1
```

途中で、いくつか質問されます。

- `Need to install the following packages` と出たら、`y` を打って Enter キーを押します。
- そのほかの質問（Git のリポジトリを作るか、必要なものを入れるか、など）は、Enter キーを押して、最初から選ばれている答えのまま進めます。

`That's it!` と出れば完成です。

```bash
cd rr1
npm run dev
```

```text
  ➜  Local:   http://localhost:5173/
```

ブラウザで `http://localhost:5173` を開くと、React Router の歓迎のページが出ます。止めるときは Ctrl+C です。ここから先はサーバーを動かしたまま作業してかまいません。ファイルを保存すると、画面が自動で新しくなります。

## ファイルの置き場所

`app` フォルダの中に、画面のファイルが入っています。

| ファイル | 役割 |
| --- | --- |
| `app/root.tsx` | すべてのページに共通の外枠 |
| `app/routes.ts` | どの URL でどのファイルを表示するかの一覧 |
| `app/routes/home.tsx` | `/`（トップ）のページ |

`.tsx` は、TypeScript の中に画面の形（後で説明する JSX）を書けるファイルです。

## 最初のコンポーネント

`app/routes/home.tsx` の中身をすべて消して、次の内容に書き換えて保存します。

```tsx
export default function Home() {
  return (
    <main>
      <h1>社員一覧</h1>
      <p>ここに社員を並べます</p>
    </main>
  );
}
```

ブラウザに「社員一覧」と表示されます。

コンポーネントは画面の形を返す関数です。`return` の後ろの、HTML によく似た書き方を「JSX」と呼びます。`export default` は「このファイルの代表として外に出す」という意味で、React Router は、ページのファイルが `export default` で出したコンポーネントを表示します。

:::note
このプロジェクトには、見た目を整える仕組み（Tailwind CSS）が最初から入っています。そのため、見出しも普通の文字と同じ大きさで表示されます。見た目の整え方はこの教材では扱いません。
:::

## JSX の決まり

JSX は HTML によく似ていますが、いくつか違いがあります。

- 返すのは、1つの要素で全体を囲んだもの。上の例では `<main>` で囲んでいます
- HTML の `class` は `className` と書く
- `{ }` の中には TypeScript の値や式を書ける

```tsx
const count = 3;
return <p>社員は{count}人です</p>;
```

## 部品を作る：props

社員1人分を表示する部品を作ります。`app` の中に `components` フォルダを作り、`EmployeeCard.tsx` を作ります。

```bash
mkdir -p app/components
touch app/components/EmployeeCard.tsx
code app/components/EmployeeCard.tsx
```

```tsx
type Props = {
  name: string;
  department: string;
};

export function EmployeeCard({ name, department }: Props) {
  return (
    <div>
      <h2>{name}</h2>
      <p>{department}</p>
    </div>
  );
}
```

コンポーネントが外から受け取る値を「props」と呼びます。`Props` 型で、名前と部署を受け取ることを決めています。

`home.tsx` で、この部品を使います。

```tsx
import { EmployeeCard } from "../components/EmployeeCard";

export default function Home() {
  return (
    <main>
      <h1>社員一覧</h1>
      <EmployeeCard name="佐藤" department="総務部" />
      <EmployeeCard name="鈴木" department="営業部" />
    </main>
  );
}
```

`import` は、別のファイルが外に出したものを使う、という意味です。部品は HTML の要素と同じように `<EmployeeCard />` と書いて使い、props は `name="佐藤"` のように渡します。

`department` を渡し忘れると、VS Code で赤い波線が出ます。props にも型が付いているからです。

## 配列から一覧を作る：map

社員が増えるたびに `<EmployeeCard />` を書き足すのは大変です。配列から作ります。

```tsx
import { EmployeeCard } from "../components/EmployeeCard";

const employees = [
  { id: 1, name: "佐藤", department: "総務部" },
  { id: 2, name: "鈴木", department: "営業部" },
  { id: 3, name: "高橋", department: "開発部" },
];

export default function Home() {
  return (
    <main>
      <h1>社員一覧</h1>
      {employees.map((employee) => (
        <EmployeeCard key={employee.id} name={employee.name} department={employee.department} />
      ))}
    </main>
  );
}
```

レッスン6-1の `map` で、社員1人ずつを `<EmployeeCard />` に変えた配列を作り、`{ }` で画面に並べています。

`key` は、React が一覧の中のそれぞれを見分けるための値です。一覧を作るときは、重ならない値（ここでは `id`）を必ず `key` に渡します。

## 困ったとき

- **ブラウザの開発者ツールに「Each child in a list should have a unique "key" prop」と出た**：`map` で作った要素に `key` を渡していません。
- **「Cannot find module '../components/EmployeeCard'」と出た**：ファイルの場所か名前が違います。`app/components/EmployeeCard.tsx` にあるか、大文字と小文字まで確かめてください。
- **画面に何も出ず、ターミナルにエラーが出ている**：JSX の閉じ忘れ（`<div>` に対する `</div>` など）がないか確かめてください。

## 確かめよう

1. `employees` の配列に「田中、営業部」の人を足す
2. `EmployeeCard` に、入社年（`year`、数）の props を足し、「2022年入社」のように表示する
3. 全員の入社年を配列に書き足して、画面に表示する

ブラウザに4人が並び、それぞれに入社年が表示されれば完了です。`year` を渡し忘れた人がいると、VS Code で赤い波線が出ることも確かめてください。

## 今は知らなくてよいこと

- 見た目を整える方法（CSS、Tailwind CSS）
- `app/root.tsx` の中身

## 次のレッスン

次はボタンを押したり文字を入れたりしたときに、画面の表示を変える方法を学びます。
