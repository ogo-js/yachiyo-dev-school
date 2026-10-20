---
title: JavaScript の基本
description: Node.js を入れ、変数・関数・配列・オブジェクトを使った短いプログラムを書く
sidebar:
  order: 1
---

## このページでできるようになること

- Node.js を入れて、JavaScript のファイルを動かせる
- 変数・条件分岐・関数を使った短いプログラムを書ける
- 配列とオブジェクトを使って、データの一覧を扱える

かかる時間の目安は60分です。

## 始める前に

第1部（コマンドライン）と、レッスン3-3（JSON と API）を終えている必要があります。

## なぜ JavaScript を覚えるのか

ブラウザの中で動くプログラムを書ける言語は、実質的に JavaScript だけです。画面を作る部分はどんな仕組みを使っても、最後は JavaScript として動きます。

この教材では画面を作るときに TypeScript を使います。TypeScript は JavaScript に「型」を足したものです。書き方の大部分は JavaScript と同じなので、まず JavaScript を覚えます。

## Node.js を入れる

Node.js は JavaScript をブラウザの外で動かすための道具です。入れ方は時期によって変わるので、公式の手順に従ってください。

1. ブラウザで Node.js の公式サイトのダウンロードのページ（nodejs.org/ja/download）を開きます。
2. 「LTS」と書かれた版を選び、使う OS に「Linux」、入れ方に「nvm」を選びます。
3. 表示されたコマンドを、上から順に1つずつターミナルに貼り付けて実行します。

:::note
LTS は、長い期間にわたって直しが提供される版です。特に理由がなければ LTS を選びます。
:::

入ったことを確かめます。

```bash
node -v
npm -v
```

それぞれ `v24.11.1` や `11.6.2` のように、番号が1行ずつ出れば入っています。番号は時期によって違います。

## 最初のプログラム

練習用のフォルダを作り、ファイルを1つ作ります。

```bash
mkdir -p ~/practice/js1
cd ~/practice/js1
touch hello.js
code hello.js
```

`hello.js` に次の4行を書いて保存します。

```javascript
const name = "やちよ";
let count = 1;
count = count + 1;
console.log(`こんにちは、${name}さん。${count}回目です。`);
```

動かします。

```bash
node hello.js
```

```text
こんにちは、やちよさん。2回目です。
```

## 変数：const と let

値に名前を付けて覚えておくものを「変数」と呼びます。

- `const`：一度決めたら変えない値。`name` は後から変えないので `const` にしています
- `let`：後から変える値。`count` は `1` から `2` に変えるので `let` にしています

迷ったら `const` を使い、変える必要が出てきたときだけ `let` にします。

`console.log` は、値をターミナルに表示する命令です。`` ` ``（バッククォート）で囲んだ文の中では、`${ }` の中に変数を書くと、その値が埋め込まれます。

## 値の種類

| 種類 | 例 | 説明 |
| --- | --- | --- |
| 文字列 | `"佐藤"` | `" "` で囲む |
| 数 | `280000`、`0.1` | 整数も小数も同じ「数」 |
| 真偽 | `true`、`false` | 正しいか、正しくないか |
| 値がない | `undefined`、`null` | まだ何も入っていない |

種類が違う値を `+` でつなぐと、思わぬ結果になることがあります。

```javascript
console.log(1000 + 1000 * 0.1);
console.log("1" + 1);
```

```text
1100
11
```

文字列の `"1"` と数の `1` を足すと、`2` ではなく、文字をつなげた `"11"` になります。このような間違いを防ぐのが、次のレッスンで学ぶ TypeScript です。

## 条件分岐：if

```javascript
const salary = 320000;

if (salary >= 300000) {
  console.log("30万円以上です");
} else {
  console.log("30万円未満です");
}
```

`( )` の中の条件が正しければ、すぐ後の `{ }` の中が動きます。正しくなければ、`else` の後の `{ }` の中が動きます。比べ方には、SQL と同じく `>=` や `<` が使えます。等しいかどうかは `===`、等しくないかどうかは `!==` で比べます。

## 関数

いくつかの処理をまとめて名前を付けたものを「関数」と呼びます。

```javascript
function withTax(price) {
  return price + price * 0.1;
}

console.log(withTax(1000));
console.log(withTax(2500));
```

```text
1100
2750
```

`price` は、関数を呼ぶときに渡す値（引数）を受け取る名前です。`return` の後ろの値が関数の結果（戻り値）になります。

同じ関数は次のように短く書くこともできます。この書き方を「アロー関数」と呼び、よく使われます。

```javascript
const withTax = (price) => price + price * 0.1;
```

## 配列とオブジェクト

`basics.js` を作って、次の内容を書いて保存します。

```javascript
const employees = [
  { name: "佐藤", department: "総務部", salary: 280000 },
  { name: "鈴木", department: "営業部", salary: 320000 },
  { name: "高橋", department: "開発部", salary: 350000 },
];

console.log(employees.length);
console.log(employees[0].name);

for (const employee of employees) {
  console.log(`${employee.name}さんは${employee.department}です`);
}
```

```bash
node basics.js
```

```text
3
佐藤
佐藤さんは総務部です
鈴木さんは営業部です
高橋さんは開発部です
```

- `[ ]` で囲んだものが「配列」。値を順番に並べたもの
- `{ }` で囲んだものが「オブジェクト」。名前と値の組をまとめたもの
- `employees.length` は配列の要素の数、`employees[0]` は最初の要素（番号は0から数える）
- `for (const employee of employees)` は、配列の要素を1つずつ取り出して、`{ }` の中を繰り返す

この形はレッスン3-3の JSON とほとんど同じです。API から受け取った JSON は、JavaScript の中ではこのような配列やオブジェクトとして扱います。

## 配列を絞る・変える：filter と map

`basics.js` の最後に、次の行を書き足して保存し、もう一度動かします。

```javascript
const high = employees.filter((employee) => employee.salary >= 300000);
const names = high.map((employee) => employee.name);
console.log(names);
```

```text
[ '鈴木', '高橋' ]
```

- `filter`：条件に合う要素だけを残した、新しい配列を作る。SQL の `WHERE` に近い働き
- `map`：要素を1つずつ別の値に変えた、新しい配列を作る。SQL の `SELECT` で列を選ぶのに近い働き

この2つは、画面に一覧を表示するときに必ずと言ってよいほど使います。

## 困ったとき

- **「node: command not found」と出た**：Node.js が入っていないか、入れた後にターミナルを開き直していません。VS Code のターミナルを閉じて、新しく開いてください。
- **「SyntaxError」と出た**：書き方が崩れています。表示された行の近くで、`( )`、`{ }`、`[ ]` の閉じ忘れや、`,` の過不足がないか確かめてください。
- **「ReferenceError: … is not defined」と出た**：まだ作っていない変数や関数の名前を使っています。綴りを確かめてください。

## 確かめよう

`~/practice/js1` に `practice.js` を作り、次のことをするプログラムを書いてください。

1. 次の4人の配列を作る：佐藤（28万円）、鈴木（32万円）、田中（25万円）、伊藤（30万円）
2. 給料が30万円未満の人の名前だけの配列を作り、表示する
3. 全員の名前を「〇〇さん」の形にした配列を作り、表示する

`node practice.js` の結果が次の2行になれば完了です。

```text
[ '佐藤', '田中' ]
[ '佐藤さん', '鈴木さん', '田中さん', '伊藤さん' ]
```

## 今は知らなくてよいこと

- `var` という古い変数の書き方
- クラスの書き方

## 次のレッスン

次は JavaScript に型を足した TypeScript を使って、さっきの `"1" + 1` のような間違いを、動かす前に見つけられるようにします。
