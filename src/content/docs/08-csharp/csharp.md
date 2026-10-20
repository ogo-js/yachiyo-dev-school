---
title: C# の基本
description: .NET を入れ、クラス・メソッド・リストを使った短いプログラムを C# で書く
sidebar:
  order: 1
---

## このページでできるようになること

- .NET を入れて、C# のプログラムを動かせる
- 変数・条件分岐・メソッド・リストを使った短いプログラムを書ける
- VB.NET や TypeScript と、書き方を見比べられる

かかる時間の目安は60分です。

## 始める前に

第6部（TypeScript）を終えている必要があります。

## なぜ C# を覚えるのか

画面から呼ばれる API や、業務の計算をするサーバー側のプログラムは、画面とは別の言語で書くことがよくあります。業務アプリの世界で広く使われているのが、Microsoft の .NET と、その上で動く C# です。

C# は TypeScript と同じく、型をはっきり書く言語です。第6部で覚えた考え方の多くが、そのまま使えます。VB.NET を書いたことがある人なら、使う部品（.NET の標準の仕組み）はほとんど同じで、書き方が違うだけです。

## .NET を入れる

Ubuntu では `apt` で入れられます。

```bash
sudo apt update
sudo apt install dotnet-sdk-10.0
```

入ったことを確かめます。

```bash
dotnet --version
```

`10.0.113` のように、`10.0` で始まる番号が出れば入っています。`10.0` は .NET のバージョンで、長い期間にわたって直しが提供される版（LTS）です。

## 最初のプログラム

```bash
cd ~/practice
dotnet new console -o cs1
cd cs1
code Program.cs
```

`dotnet new console` は「画面を持たない、文字だけのプログラム」のひな形を作るコマンドです。`-o cs1` で、`cs1` というフォルダに作ります。

`Program.cs` の中身をすべて消して、次の4行を書いて保存します。

```csharp
var name = "やちよ";
int count = 1;
count = count + 1;
Console.WriteLine($"こんにちは、{name}さん。{count}回目です。");
```

```bash
dotnet run
```

```text
こんにちは、やちよさん。2回目です。
```

初めて動かすときは、準備に少し時間がかかります。

- `int count`：整数の変数。型を名前の前に書く
- `var name`：型を書かずに、右側の値から決めてもらう。`"やちよ"` なので `string` になる
- 文の最後に `;` を付ける
- `$"…{name}…"`：`$` を付けた文字列の中では `{ }` に変数の値を埋め込める（TypeScript の `` `…${name}…` `` と同じ）

## 型の間違いは動かす前に見つかる

`count` に文字列を入れてみます。1行目を次のように書き換えて保存し、`dotnet run` を打ちます。

```csharp
int count = "abc";
```

```text
Program.cs(1,13): error CS0029: Cannot implicitly convert type 'string' to 'int'
```

動く前に止まりました。表示の形は TypeScript の `tsc` のエラーとよく似ています（`(1,13)` は1行目の13文字目）。C# では、型の確かめがプログラムを作る（ビルドする）手順の中に必ず入っています。確かめたら、元に戻しておいてください。

## お金の計算は decimal

`Program.cs` の最後に、次の内容を書き足して保存し、動かします。

```csharp
decimal price = 200m;
Console.WriteLine(WithTax(price));

static decimal WithTax(decimal price)
{
    return price * 1.1m;
}
```

```text
220.0
```

レッスン6-2では、同じ計算が `220.00000000000003` になりました。C# の `decimal` は10進数の小数を誤差なく扱える型です。お金の計算では `decimal` を使います。数の後ろの `m` は「この数は `decimal` です」という印です。

`static decimal WithTax(decimal price)` は、メソッド（関数）です。戻り値の型を名前の前に、引数の型を引数の名前の前に書きます。

## クラスとリスト

`Program.cs` の最後に、次の内容を書き足して保存し、動かします。

```csharp
var employees = new List<Employee>
{
    new Employee("佐藤", "総務部", 280000),
    new Employee("鈴木", "営業部", 320000),
    new Employee("高橋", "開発部", 350000),
};

foreach (var employee in employees)
{
    Console.WriteLine($"{employee.Name}さんは{employee.Department}です");
}

var names = employees
    .Where(employee => employee.Salary >= 300000)
    .Select(employee => employee.Name)
    .ToList();
Console.WriteLine(string.Join("、", names));

record Employee(string Name, string Department, int Salary);
```

```text
佐藤さんは総務部です
鈴木さんは営業部です
高橋さんは開発部です
鈴木、高橋
```

- `record Employee(…)`：社員を表す型。名前・部署・給料を持つ。TypeScript の `type Employee = { … }` にあたる
- `List<Employee>`：社員だけを入れられるリスト（配列のようなもの）
- `foreach (var employee in employees)`：リストの要素を1つずつ取り出して繰り返す
- `Where` と `Select`：TypeScript の `filter` と `map` にあたる。この書き方を LINQ（リンク）と呼ぶ

`record` の行はファイルの最後に置きます。C# では型の定義を、上から順に動く処理より後ろに書く決まりがあるからです。

## 3つの言語を見比べる

| したいこと | VB.NET | C# | TypeScript |
| --- | --- | --- | --- |
| 変数 | `Dim count As Integer = 1` | `int count = 1;` | `let count: number = 1;` |
| 条件分岐 | `If x >= 3 Then … End If` | `if (x >= 3) { … }` | `if (x >= 3) { … }` |
| 等しいか | `=` | `==` | `===` |
| 関数 | `Function WithTax(price As Decimal) As Decimal` | `decimal WithTax(decimal price)` | `function withTax(price: number): number` |
| 繰り返し | `For Each e In employees … Next` | `foreach (var e in employees) { … }` | `for (const e of employees) { … }` |
| 文字列の埋め込み | `$"{name}さん"` | `$"{name}さん"` | `` `${name}さん` `` |
| 値がない | `Nothing` | `null` | `null`、`undefined` |

C# の大文字と小文字は区別されます。`console.writeline` と書くと、エラーになります。

## 困ったとき

- **「error CS1002: ; expected」と出た**：文の最後の `;` を書き忘れています。表示された行を見てください。
- **「error CS0103: The name '…' does not exist in the current context」と出た**：まだ作っていない変数やメソッドの名前を使っているか、大文字と小文字を間違えています。
- **`record` の行で「Top-level statements must precede namespace and type declarations」と出た**：`record` の行より後ろに、処理を書いています。`record` の行を、ファイルの一番最後に移してください。

## 確かめよう

`Program.cs` に、次のことをする処理を書き足してください。書き足す場所は `record` の行より上です。

1. 「田中、営業部、250000」の社員をリストに足す（ヒント：`employees.Add(…)`）
2. 給料が30万円未満の人の名前を、「、」でつないで表示する
3. 全員の給料の合計を表示する（ヒント：`employees.Sum(employee => employee.Salary)`）

結果の最後の2行が次のようになれば完了です。

```text
佐藤、田中
1200000
```

## 今は知らなくてよいこと

- `class` を使った、より細かい型の作り方
- `namespace` と、ファイルを分けるときの書き方

## 次のレッスン

次は ASP.NET Core を使って、URL に応じて JSON を返す API を作ります。
