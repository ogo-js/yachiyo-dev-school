---
title: 待つ処理を書く
description: async と await で、時間のかかる処理や API の結果を待つ処理を書く
sidebar:
  order: 3
---

## このページでできるようになること

- 「待つ処理」が書いた順に終わるとは限らないことを説明できる
- `async` と `await` を使って、結果を待ってから次へ進む処理を書ける
- `fetch` で API を呼び、うまくいかなかったときの処理も書ける

かかる時間の目安は40分です。

## 始める前に

レッスン6-2（型を付ける）を終えている必要があります。API を呼ぶところではレッスン3-2の `~/practice/web/webdemo.py` を使います。

## なぜこれを覚えるのか

API を呼ぶと、返事が届くまでに時間がかかります。データベースから読むときも、ファイルを読むときも同じです。

プログラムは返事を待っている間も止まらずに先へ進もうとします。そのため、「返事が届いてから次の処理をする」と、はっきり書く必要があります。そのための書き方が `async` と `await` です。画面を作るときにも API からデータを取ってくる所で必ず使います。

## 待つ処理を書く

`~/practice/js1` に `wait.ts` を作り、次の内容を書いて保存します。

```typescript
function wait(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function main() {
  console.log("1. はじめ");
  await wait(2000);
  console.log("2. 2秒たった");
}

main();
console.log("3. main を呼んだ後");
```

`wait` は、指定したミリ秒（1000で1秒）だけ待つ関数です。中身は今は分からなくてかまいません。

```bash
node wait.ts
```

```text
1. はじめ
3. main を呼んだ後
2. 2秒たった
```

書いた順と、表示された順が違います。

- `await wait(2000)`：`main` の中は2秒待ってから次の行へ進む
- `main` の外は待たない。`main()` を呼んだら、`main` が終わるのを待たずにすぐ次の行へ進むので、「3」が先に出る

`await` は「この処理が終わるまで、ここで待つ」という意味です。`await` を使う関数には頭に `async` を付けます。

## API を呼ぶ：fetch

1つ目のターミナルで、練習用のサーバーを動かします。

```bash
cd ~/practice/web
python3 webdemo.py
```

2つ目のターミナルで `~/practice/js1` に移り、`api.ts` を作って、次の内容を書いて保存します。

```typescript
type Hello = {
  message: string;
  method: string;
};

async function main() {
  const response = await fetch("http://localhost:8000/api/hello?name=yachiyo");
  console.log(response.status);
  const data: Hello = await response.json();
  console.log(data.message);
}

main();
```

```bash
node api.ts
```

```text
200
こんにちは、yachiyoさん
```

`fetch` は、URL にリクエストを送る関数です。返事が届くまで時間がかかるので、`await` で待ちます。

- `response.status`：ステータスコード（レッスン3-1）
- `response.json()`：返ってきた JSON を、JavaScript のオブジェクトに変える。これも待つ処理なので `await` を付ける
- `const data: Hello`：受け取った値を、`Hello` 型として扱う

:::caution[await を付け忘れると]
`await` を付け忘れると、結果ではなく「まだ終わっていない処理」そのものを受け取ってしまいます。`data.message` が `undefined` になるときは、`await` の付け忘れを疑ってください。
:::

## うまくいかなかったときに備える：try と catch

1つ目のターミナルで Ctrl+C を押してサーバーを止めてから、もう一度 `node api.ts` を動かします。

```text
TypeError: fetch failed
  [cause]: Error: connect ECONNREFUSED 127.0.0.1:8000
```

長いエラーの中に、このような行が出て止まります。`ECONNREFUSED` は「つなごうとしたが断られた」という意味です。サーバーが動いていないので、つながりませんでした。

API は、相手が止まっていたり、通信が切れたりして、いつ失敗するか分かりません。失敗したときにどうするかを、`try` と `catch` で書いておきます。

`api.ts` の `main` を、次のように書き換えて保存します。

```typescript
async function main() {
  try {
    const response = await fetch("http://localhost:8000/api/hello?name=yachiyo");
    const data: Hello = await response.json();
    console.log(data.message);
  } catch (error) {
    console.log("API を呼べませんでした");
  }
}
```

サーバーを止めたまま動かすと、次の1行だけが出ます。

```text
API を呼べませんでした
```

`try` の `{ }` の中でエラーが起きると、そこで中断して、`catch` の `{ }` の中へ移ります。プログラム全体が止まらずに、決めておいた処理ができます。

## 困ったとき

- **「await is only valid in async functions」と出た**：`await` を、`async` の付いていない関数の中で使っています。外側の関数の頭に `async` を付けてください。
- **`npx tsc` で「Property 'json' does not exist」のように出た**：`fetch` の結果に `await` を付け忘れています。

## 確かめよう

1. 1つ目のターミナルで練習用のサーバーを動かす
2. `~/practice/js1` に `practice-api.ts` を作り、次のことをする `main` 関数を書く
   - `http://localhost:8000/api/hello?name=suzuki` と `http://localhost:8000/api/hello?name=tanaka` を、この順に `fetch` で呼ぶ
   - それぞれの `message` を表示する
   - 失敗したときは「API を呼べませんでした」と表示する
3. `npx tsc` で型の間違いがないことを確かめ、`node practice-api.ts` で動かす

サーバーが動いているときに次の2行が、止めているときに「API を呼べませんでした」が出れば完了です。

```text
こんにちは、suzukiさん
こんにちは、tanakaさん
```

## 今は知らなくてよいこと

- `Promise` の中身と、`then` を使った書き方
- いくつもの待つ処理を、同時に進める方法

## 次のレッスン

これで第6部は終わりです。次からは第7部です。React を使って、画面を部品に分けて作ります。
