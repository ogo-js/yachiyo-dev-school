---
title: 型を付ける
description: TypeScript で引数・戻り値・オブジェクトに型を付け、型のエラーを読んで直す
sidebar:
  order: 2
---

## このページでできるようになること

- TypeScript で型を確かめる準備ができる
- 変数・引数・戻り値・オブジェクトに型を付けられる
- 型のエラーを読んで、どこが何と食い違っているかが分かる

かかる時間の目安は50分です。

## 始める前に

レッスン6-1（JavaScript の基本）を終えている必要があります。

## なぜ型を付けるのか

JavaScript はプログラムを動かしてみるまで、値の種類の食い違いに気づけません。前のレッスンの `"1" + 1` が `"11"` になったように、エラーにならずに、間違った結果のまま動いてしまうこともあります。

TypeScript では「この変数には数が入る」「この関数は文字列を受け取る」という決まり（型）を書いておけます。プログラムを動かす前に、決まりに合わない使い方を見つけてくれます。小さな間違いが、本番で大きな事故になるのを防げます。

## 準備する

練習用のフォルダで、TypeScript を入れます。

```bash
cd ~/practice/js1
npm init -y
npm install --save-dev typescript
```

- `npm init -y`：このフォルダを、Node.js のプロジェクトにする。`package.json` という設定のファイルができる
- `npm install --save-dev typescript`：このプロジェクトに TypeScript を入れる

続けて、型を確かめるときの設定を書いた `tsconfig.json` を作ります。

```bash
touch tsconfig.json
code tsconfig.json
```

次の内容を書いて保存します。

```json
{
  "compilerOptions": {
    "noEmit": true,
    "moduleDetection": "force"
  }
}
```

今は意味が分からなくてかまいません。「型を確かめるだけにする」「ファイルごとに別々に扱う」という設定です。

## 型を付けて書く

`employee.ts` を作って、次の内容を書いて保存します。TypeScript のファイルは名前の最後を `.ts` にします。

```typescript
type Employee = {
  name: string;
  salary: number;
};

function raise(employee: Employee, amount: number): Employee {
  return { ...employee, salary: employee.salary + amount };
}

const sato: Employee = { name: "佐藤", salary: 280000 };
console.log(raise(sato, "10000"));
```

型の書き方を、上から順に見ていきます。

- `type Employee = { … }`：「社員」という型を決める。`name` は文字列（`string`）、`salary` は数（`number`）
- `employee: Employee`、`amount: number`：引数の型。名前の後ろに `:` と型を書く
- `): Employee`：戻り値の型。この関数は社員を返す
- `{ ...employee, salary: … }`：`employee` の中身を写したうえで、`salary` だけを新しい値にしたオブジェクトを作る

最後の行で、わざと間違えています。`amount` には数を渡すはずなのに、文字列の `"10000"` を渡しています。

## 動かすとどうなるか

Node.js は `.ts` のファイルもそのまま動かせます。

```bash
node employee.ts
```

```text
{ name: '佐藤', salary: '28000010000' }
```

エラーにならずに動きました。そのかわり、給料が `28000010000` という、おかしな値になっています。数と文字列を足したので、文字としてつながってしまいました。

Node.js は型を読み飛ばして動かすだけで、型が合っているかは確かめません。

## 型を確かめる：tsc

型を確かめるのは、TypeScript の `tsc` というコマンドです。

```bash
npx tsc
```

```text
employee.ts(11,25): error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.
```

動かす前に、間違いが見つかりました。`npx` は「このプロジェクトに入れた道具を動かす」という意味です。

VS Code でも、`"10000"` の下に赤い波線が出ています。マウスを重ねると、同じエラーが表示されます。

## 型のエラーを読む

エラーの文はいつも同じ形をしています。

| 部分 | 意味 |
| --- | --- |
| `employee.ts` | どのファイルか |
| `(11,25)` | 11行目の、25文字目 |
| `TS2345` | エラーの種類の番号 |
| `Argument of type 'string'` | 渡した引数の型は `string` だが |
| `is not assignable to parameter of type 'number'` | 受け取る側の型は `number` なので、合わない |

英語ですが、「何の型が」「何の型と」合わないのかを読み取れば、ほとんどのエラーは直せます。

`"10000"` を `10000` に直して保存し、もう一度 `npx tsc` を打ちます。何も表示されなければ、型の間違いはありません。`node employee.ts` で動かすと、給料が `290000` になっています。

## よく見るエラー

`employee.ts` の最後に、次の行を足してみてください。

```typescript
const suzuki: Employee = { name: "鈴木" };
console.log(sato.nam);
```

```bash
npx tsc
```

```text
employee.ts(12,7): error TS2741: Property 'salary' is missing in type '{ name: string; }' but required in type 'Employee'.
employee.ts(13,18): error TS2551: Property 'nam' does not exist on type 'Employee'. Did you mean 'name'?
```

- 1つ目：`Employee` には `salary` が必要なのに、書いていない
- 2つ目：`Employee` に `nam` はない。`name` の打ち間違いではないか

どちらも JavaScript のままなら、動かしてみるまで気づけない間違いです。確かめたら、足した2行は消しておいてください。

## 困ったとき

- **`npx tsc` を打ったら、使い方の説明が長々と表示された**：`tsconfig.json` がないか、別のフォルダで打っています。`~/practice/js1` に `tsconfig.json` があるか確かめてください。
- **「Parameter 'x' implicitly has an 'any' type」と出た**：引数に型を書いていません。`(x: number)` のように型を書いてください。
- **VS Code の赤い波線が消えない**：保存していない可能性があります。保存しても消えないときは、`npx tsc` の結果の方を信じてください。

## 確かめよう

`~/practice/js1` に `product.ts` を作り、次のことをしてください。

1. 商品を表す型 `Product` を作る。名前（`name`、文字列）と値段（`price`、数）を持つ
2. 商品を受け取り、税込みの値段（値段の1.1倍）を返す関数 `withTax` を、引数と戻り値に型を付けて書く
3. 「ノート、200円」の商品を作り、`withTax` の結果を表示する

`npx tsc` で何も表示されず、`node product.ts` の結果が `220.00000000000003` になれば完了です。

:::note
`220` ではなく `220.00000000000003` になるのは、コンピューターが小数を扱うときの誤差です。お金の計算では、この誤差が問題になるので、実際のアプリでは円単位の整数で計算するなどの工夫をします。
:::

## 今は知らなくてよいこと

- `interface` を使った型の書き方
- `any` という、型の確かめを止める書き方

## 次のレッスン

次は API を呼んで結果を待つときのような、「待つ処理」の書き方を学びます。
