---
title: 状態とイベント
description: useState で状態を持ち、ボタンや入力に応じて画面の表示を変える
sidebar:
  order: 2
---

## このページでできるようになること

- ボタンを押したときの処理を書ける
- `useState` で、変わる値（状態）を持てる
- 入力欄の文字に合わせて、一覧を絞り込める

かかる時間の目安は45分です。

## 始める前に

レッスン7-1（コンポーネントを作る）を終え、`~/practice/rr1` で `npm run dev` を動かしている必要があります。

7-1の「確かめよう」で足したものは、消してから進めてください。`home.tsx` の配列からは田中さんを、`EmployeeCard.tsx` からは入社年（`year`）を消します。この先の例は佐藤・鈴木・高橋の3人で、名前と部署だけを使って書いています。入社年を残すと、この先のコードが `year` を渡していないので、型のエラーになります。田中さんを残すと、「確かめよう」の人数が本文と合わなくなります。

## なぜこれを覚えるのか

ここまでの画面は表示したら変わりませんでした。実際のアプリの画面は、ボタンを押すと数が増えたり、検索欄に文字を入れると一覧が絞られたりします。

利用者の操作に応じて変わる値を「状態」と呼びます。React では状態を変えると、その状態を使っている画面が自動で描き直されます。画面を直接書き換えるのではなく、状態を変えるだけでよいのが React の考え方です。

## ボタンを押したときの処理：onClick

`EmployeeCard.tsx` に、ボタンを1つ足します。

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
      <button type="button" onClick={() => console.log(`${name}さんにいいね`)}>
        いいね
      </button>
    </div>
  );
}
```

ボタンを押すたびに、ブラウザの開発者ツールの「コンソール」（Console）のタブに、`佐藤さんにいいね` のように表示されます。

`onClick` に渡した関数がボタンを押したときに呼ばれます。このような「利用者の操作」を「イベント」と呼びます。

:::note
この `console.log` はターミナルではなく、ブラウザの開発者ツールに出ます。ボタンを押す処理はブラウザの中で動いているからです。
:::

## 数を覚える：useState

押した回数を数えて、ボタンに表示します。

```tsx
import { useState } from "react";

type Props = {
  name: string;
  department: string;
};

export function EmployeeCard({ name, department }: Props) {
  const [likes, setLikes] = useState(0);

  return (
    <div>
      <h2>{name}</h2>
      <p>{department}</p>
      <button type="button" onClick={() => setLikes(likes + 1)}>
        いいね（{likes}）
      </button>
    </div>
  );
}
```

`useState(0)` は「最初は `0` の状態を1つ持つ」という意味です。2つの値を返します。

- `likes`：今の値
- `setLikes`：値を変えるための関数

ボタンを押すと `setLikes(likes + 1)` が呼ばれ、`likes` が1つ増えます。React はそれに気づいて、このコンポーネントを描き直します。ボタンの数が増えて見えるのは、そのためです。

佐藤さんのボタンを押しても、鈴木さんの数は変わりません。状態はコンポーネント1つずつが別々に持っています。

:::caution[ふつうの変数では画面が変わらない]
`let likes = 0;` として `likes = likes + 1;` と書いても、画面は変わりません。React は、`useState` で作った状態が変わったときだけ描き直します。
:::

## 入力欄で絞り込む

`home.tsx` に検索欄を足し、名前に入れた文字を含む人だけを表示します。

```tsx
import { useState } from "react";
import { EmployeeCard } from "../components/EmployeeCard";

const employees = [
  { id: 1, name: "佐藤", department: "総務部" },
  { id: 2, name: "鈴木", department: "営業部" },
  { id: 3, name: "高橋", department: "開発部" },
];

export default function Home() {
  const [keyword, setKeyword] = useState("");
  const shown = employees.filter((employee) => employee.name.includes(keyword));

  return (
    <main>
      <h1>社員一覧</h1>
      <input value={keyword} onChange={(event) => setKeyword(event.target.value)} placeholder="名前で絞る" />
      {shown.map((employee) => (
        <EmployeeCard key={employee.id} name={employee.name} department={employee.department} />
      ))}
    </main>
  );
}
```

検索欄に「藤」と入れると、佐藤さんだけが表示されます。消すと、全員に戻ります。

流れを順に追うと、次のようになります。

1. 文字を入れると `onChange` が呼ばれる
2. `setKeyword` で、`keyword` の状態が入れた文字に変わる
3. React が `Home` を描き直す。そのとき `filter` がもう一度動き、`shown` が絞られた一覧になる

入力欄の中身（`value`）も状態の `keyword` から決めています。画面に出ているものはいつも状態から作られる、という形をそろえておくと、表示と中身が食い違いません。

## 困ったとき

- **「useState is not defined」と出た**：ファイルの先頭の `import { useState } from "react";` を書き忘れています。
- **入力欄に文字が入らない**：`value` だけ渡して、`onChange` で状態を変えていません。`onChange` を確かめてください。
- **画面がエラーになり、「Too many re-renders」と出た**：`onClick={setLikes(likes + 1)}` のように、`() =>` を付け忘れています。付け忘れると、押したときではなく描くたびに `setLikes` が呼ばれ、描き直しが止まらなくなります。VS Code でも `onClick` の所に赤い波線が出ます。

## 確かめよう

1. `home.tsx` に「部署で絞る」の選択欄（`select`）を足す。選択肢は「すべて」「総務部」「営業部」「開発部」
2. 名前の検索欄と、部署の選択欄の両方の条件に合う人だけを表示する
3. 一覧の上に「〇人表示中」と、表示している人数を出す

「営業部」を選ぶと鈴木さんだけになり「1人表示中」と出て、「すべて」に戻すと3人になれば完了です。

## 今は知らなくてよいこと

- `useState` 以外の、状態を扱う仕組み（`useEffect` など）
- 状態を、親のコンポーネントと子のコンポーネントで分け合う方法

## 次のレッスン

次は URL ごとにページを分け、ページの間を移動できるようにします。
