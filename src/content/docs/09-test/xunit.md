---
title: C# のテスト
description: xUnit でテストのプロジェクトを作り、C# のメソッドのテストを書いて動かす
sidebar:
  order: 2
---

## このページでできるようになること

- テストのプロジェクトを作り、テストしたいプロジェクトとつなげられる
- xUnit で、`[Fact]` と `[Theory]` のテストを書ける
- 例外が投げられることを確かめるテストを書ける

かかる時間の目安は45分です。

## 始める前に

レッスン9-1（なぜ自動テストを書くのか）と、第8部（C# と ASP.NET Core）を終えている必要があります。このレッスンでは `~/practice/api1` を使います。

## なぜこれを覚えるのか

レッスン9-1の考え方は C# でも同じです。C# では、テストをアプリとは別のプロジェクトに書くのが普通です。アプリのプロジェクトにはテストのコードを混ぜず、テストのプロジェクトからアプリのコードを呼んで確かめます。

## テストするクラスを書く

賞与（ボーナス）を計算するクラスを、`api1` に足します。評価がAなら給料の2か月分、Bなら1.5か月分、Cなら1か月分です。

```bash
cd ~/practice/api1
mkdir -p Services
touch Services/BonusCalculator.cs
code Services/BonusCalculator.cs
```

```csharp
namespace api1.Services;

public static class BonusCalculator
{
    public static decimal Calculate(decimal salary, string rating)
    {
        if (salary < 0)
        {
            throw new ArgumentException("給料は0以上にしてください");
        }

        decimal months = rating switch
        {
            "A" => 2.0m,
            "B" => 1.5m,
            "C" => 1.0m,
            _ => throw new ArgumentException($"評価が正しくありません：{rating}"),
        };
        return salary * months;
    }
}
```

- `rating switch { … }`：`rating` の値に応じて、`=>` の右側の値を選ぶ。`_` は「それ以外すべて」
- `throw new ArgumentException(…)`：正しくない値を渡されたら、例外を投げて処理を止める

## テストのプロジェクトを作る

テストのプロジェクトは `api1` の隣に作ります。

```bash
cd ~/practice
dotnet new xunit -o api1.Tests
dotnet add api1.Tests reference api1
```

- `dotnet new xunit`：xUnit を使うテストのプロジェクトのひな形を作る
- `dotnet add api1.Tests reference api1`：テストのプロジェクトから、`api1` のクラスを使えるようにつなぐ

フォルダは次のように並びます。

```text
~/practice
├── api1         … アプリ
└── api1.Tests   … テスト
```

## テストを書く

ひな形に入っている `api1.Tests/UnitTest1.cs` は使わないので消し、`BonusCalculatorTests.cs` を作ります。

```bash
rm api1.Tests/UnitTest1.cs
touch api1.Tests/BonusCalculatorTests.cs
code api1.Tests/BonusCalculatorTests.cs
```

```csharp
using api1.Services;

namespace api1.Tests;

public class BonusCalculatorTests
{
    [Fact]
    public void 評価Aなら給料の2か月分()
    {
        var bonus = BonusCalculator.Calculate(300000m, "A");

        Assert.Equal(600000m, bonus);
    }
}
```

- `[Fact]`：このメソッドがテストだという印
- `Assert.Equal(期待する値, 実際の値)`：2つが同じであることを確かめる。Vitest の `expect(実際の値).toBe(期待する値)` と、並べる順が逆なので気を付ける
- メソッドの名前に日本語を使い、確かめる決まりを書いている。C# ではメソッドの名前に日本語を使える

テストの中は「用意する・動かす・確かめる」の順に書くと読みやすくなります。今回は用意するものがないので、動かして（`Calculate`）、確かめて（`Assert.Equal`）います。

## テストを動かす

```bash
dotnet test api1.Tests
```

初めて動かすときは、準備に時間がかかります。最後に、合格（Passed）と失敗（Failed）の数がまとめて表示されます。失敗が0で、合格が1なら通っています。

## 値を変えて何度も確かめる：Theory

評価ごとに同じ形のテストを3つ書く代わりに、値だけを変えて同じテストを繰り返せます。`BonusCalculatorTests` の中に、次のメソッドを足します。

```csharp
    [Theory]
    [InlineData("A", 600000)]
    [InlineData("B", 450000)]
    [InlineData("C", 300000)]
    public void 評価ごとの月数で計算する(string rating, decimal expected)
    {
        var bonus = BonusCalculator.Calculate(300000m, rating);

        Assert.Equal(expected, bonus);
    }
```

- `[Theory]`：値を受け取って繰り返すテストだという印
- `[InlineData("A", 600000)]`：1回分の値。メソッドの引数に、`rating` が `"A"`、`expected` が `600000` として渡される

このテストは3回分として数えられます。

## 例外を確かめる

正しくない評価を渡したら、例外が投げられることも決まりの1つです。次のメソッドを足します。

```csharp
    [Fact]
    public void 評価が正しくなければ例外を投げる()
    {
        Assert.Throws<ArgumentException>(() => BonusCalculator.Calculate(300000m, "Z"));
    }
```

`Assert.Throws<ArgumentException>(…)` は、「`( )` の中を動かすと、`ArgumentException` が投げられること」を確かめます。投げられなければ、テストは失敗します。

`dotnet test api1.Tests` を動かし、合格が5つ（1 + 3 + 1）になることを確かめてください。

## わざと失敗させる

`BonusCalculator.cs` の `"B" => 1.5m` を `"B" => 1.6m` に書き換えて保存し、テストを動かします。`評価ごとの月数で計算する` の `"B"` の回が失敗し、期待した値（`450000`）と実際の値（`480000`）が表示されます。確かめたら、元に戻しておいてください。

## 困ったとき

- **「The type or namespace name 'Services' does not exist」と出た**：テストのプロジェクトと `api1` がつながっていません。`dotnet add api1.Tests reference api1` を打ったか確かめてください。
- **`dotnet test` で「No test is available」のように出た**：メソッドに `[Fact]` か `[Theory]` を付け忘れているか、メソッドが `public` になっていません。
- **`api1` のビルドで、テストのファイルが見つからないというエラーが出た**：`api1.Tests` を `api1` の中に作っていないか確かめてください。2つのフォルダは隣に並べます。

## 確かめよう

1. `BonusCalculatorTests` に、給料がマイナスのときに例外を投げることを確かめるテストを足す
2. 給料が0円のときは、評価に関係なく0円になることを、`[Theory]` で3つの評価について確かめるテストを足す
3. `dotnet test api1.Tests` で、すべて通ることを確かめる

合格が9つ（5 + 1 + 3）で、失敗が0なら完了です。

## 今は知らなくてよいこと

- データベースや API をまたいだテスト（結合テスト）の書き方
- テストのために、つなぎ先を偽物に差し替える方法（モック）

## 次のレッスン

次は画面のテストです。TypeScript のロジックをテストから先に書く方法と、React のコンポーネントのテストを学びます。
