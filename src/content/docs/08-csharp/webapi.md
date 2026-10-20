---
title: Web API を作る
description: ASP.NET Core のコントローラーで、URL に応じて JSON を返し、JSON を受け取る API を作る
sidebar:
  order: 2
---

## このページでできるようになること

- ASP.NET Core の Web API のプロジェクトを作って動かせる
- コントローラーで、GET と POST の API を作れる
- 見つからないときは404、入力に誤りがあるときは400を返せる

かかる時間の目安は60分です。

## 始める前に

レッスン8-1（C# の基本）と、第3部（Web の仕組み）を終えている必要があります。

## なぜこれを覚えるのか

第3部では Python で作った練習用の API を、curl で呼びました。第7部では画面の `loader` や `action` から、サーバーでデータを取ったり登録したりしました。

実際のアプリでは画面のサーバーとは別に、データを扱う API のサーバーを置くことがよくあります。画面は API を呼び、API がデータベースを読み書きします。このレッスンではその API を ASP.NET Core で作ります。

## プロジェクトを作る

```bash
cd ~/practice
dotnet new webapi --use-controllers --no-openapi -o api1
cd api1
```

- `webapi`：Web API のひな形
- `--use-controllers`：コントローラーという書き方を使う
- `--no-openapi`：API の説明書を自動で作る仕組みを入れない（この教材では使わないため）

ひな形には天気予報を返す見本（`WeatherForecast.cs` と `Controllers/WeatherForecastController.cs`）が入っています。今回は使わないので消します。

```bash
rm WeatherForecast.cs Controllers/WeatherForecastController.cs
```

## 社員の API を作る

`Controllers/EmployeesController.cs` を作ります。

```bash
touch Controllers/EmployeesController.cs
code Controllers/EmployeesController.cs
```

```csharp
using Microsoft.AspNetCore.Mvc;

namespace api1.Controllers;

public record Employee(int Id, string Name, string Department);

[ApiController]
[Route("api/employees")]
public class EmployeesController : ControllerBase
{
    private static readonly List<Employee> Employees =
    [
        new Employee(1, "佐藤", "総務部"),
        new Employee(2, "鈴木", "営業部"),
        new Employee(3, "高橋", "開発部"),
    ];

    [HttpGet]
    public List<Employee> GetAll()
    {
        return Employees;
    }
}
```

- `[Route("api/employees")]`：このコントローラーは `/api/employees` の URL を受け持つ
- `[HttpGet]`：GET のリクエストが来たら、このメソッドを呼ぶ
- `return Employees;`：返したリストは自動で JSON に変わって返る

`[ ]` で囲んだ部分は「属性」と呼び、クラスやメソッドに「これはどんな役割か」の印を付けています。

## 日本語をそのまま返す設定

`Program.cs` を、次のように書き換えて保存します。

```csharp
using System.Text.Encodings.Web;
using System.Text.Unicode;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers().AddJsonOptions(options =>
{
    options.JsonSerializerOptions.Encoder = JavaScriptEncoder.Create(UnicodeRanges.All);
});

var app = builder.Build();

app.MapControllers();

app.Run();
```

ASP.NET Core は何も設定しないと、JSON の中の日本語を `\u4F50\u85E4` のような記号の並びに置き換えて返します。プログラムからは正しく読めますが、curl で見たときに読めないので、日本語のまま返すように設定しています。

## 動かして呼ぶ

```bash
dotnet run --urls http://localhost:5080
```

```text
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: http://localhost:5080
```

`--urls` で、待つ URL とポート番号を決めています。2つ目のターミナルで呼びます。

```bash
curl http://localhost:5080/api/employees
```

```text
[{"id":1,"name":"佐藤","department":"総務部"},{"id":2,"name":"鈴木","department":"営業部"},{"id":3,"name":"高橋","department":"開発部"}]
```

C# の `Id` や `Name` は、JSON では `id` や `name` のように、頭が小文字になって返ります。JavaScript や TypeScript の書き方に合わせてくれています。

コードを書き換えたときは、1つ目のターミナルで Ctrl+C を押して止め、もう一度 `dotnet run --urls http://localhost:5080` で動かします。

## 1人分を返す：URL の一部を受け取る

`EmployeesController` の `GetAll` の下に、次のメソッドを足します。

```csharp
    [HttpGet("{id}")]
    public ActionResult<Employee> GetOne(int id)
    {
        var employee = Employees.Find(e => e.Id == id);
        if (employee is null)
        {
            return NotFound();
        }
        return employee;
    }
```

- `[HttpGet("{id}")]`：`/api/employees/2` のような URL を受け持ち、`2` の部分を引数の `id` で受け取る。React Router の `:id` と同じ考え方
- `ActionResult<Employee>`：社員を返すか、それ以外の結果（見つからないなど）を返すかのどちらか
- `return NotFound();`：ステータスコード404を返す

動かし直して呼びます。`-i` でステータスコードも確かめます。

```bash
curl -i http://localhost:5080/api/employees/2
curl -i http://localhost:5080/api/employees/9
```

1つ目は `HTTP/1.1 200 OK` と鈴木さんの JSON が、2つ目は `HTTP/1.1 404 Not Found` が返ります。

## 登録する：POST と入力の確かめ

ファイルの先頭の `using` の行と、`public record Employee` の行を、次のように書き換えます。

```csharp
using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Mvc;

namespace api1.Controllers;

public record Employee(int Id, string Name, string Department);

public record NewEmployee(
    [Required(ErrorMessage = "名前を入れてください")] string Name,
    [Required(ErrorMessage = "部署を入れてください")] string Department);
```

`NewEmployee` は、登録するときに受け取る値の型です。`id` は API の側で決めるので、受け取りません。`[Required]` は「必ず入れる」という決まりで、空のときの知らせ方も書いておけます。

`GetOne` の下に、次のメソッドを足します。

```csharp
    [HttpPost]
    public ActionResult<Employee> Create(NewEmployee input)
    {
        var employee = new Employee(Employees.Count + 1, input.Name, input.Department);
        Employees.Add(employee);
        return CreatedAtAction(nameof(GetOne), new { id = employee.Id }, employee);
    }
```

`CreatedAtAction` は、ステータスコード201（作りました）と、作ったものを取りに行ける URL を返します。

動かし直して、レッスン3-3と同じように JSON を送ります。

```bash
curl -i -X POST -H "Content-Type: application/json" -d '{"name":"田中","department":"営業部"}' http://localhost:5080/api/employees
```

```text
HTTP/1.1 201 Created
…
Location: http://localhost:5080/api/employees/4
…

{"id":4,"name":"田中","department":"営業部"}
```

空のまま送ってみます。

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name":"","department":""}' http://localhost:5080/api/employees
```

```text
{"type":"https://tools.ietf.org/html/rfc9110#section-15.5.1","title":"One or more validation errors occurred.","status":400,"errors":{"Name":["名前を入れてください"],"Department":["部署を入れてください"]},"traceId":"…"}
```

ステータスコード400と、項目ごとの知らせが返りました。`[ApiController]` の付いたコントローラーは、`[Required]` などの決まりを自動で確かめ、守られていなければ、メソッドを呼ぶ前に400を返します。第7部の `action` で自分で書いた確かめを、属性で書けるようになっています。

:::note
この練習の社員の一覧はプログラムのメモリの中にあるだけなので、止めると登録した社員は消えます。次のレッスンで、データベースに保存するように変えます。
:::

## 困ったとき

- **「Failed to connect to localhost port 5080」と出た**：1つ目のターミナルで `dotnet run --urls http://localhost:5080` が動いているか確かめてください。
- **直したのに動きが変わらない**：`dotnet run` を止めて、動かし直してください。
- **「address already in use」と出て動かない**：前に動かした API が別のターミナルで動いたままです。そちらで Ctrl+C を押して止めてください。
- **POST で「415 Unsupported Media Type」が返った**：`-H "Content-Type: application/json"` を付け忘れています。
- **ターミナルに「Failed to determine the https port for redirect」と出た**：この教材の進め方では出ない設定にしていますが、出ても動きには差し支えありません。

## 確かめよう

1. 社員を消す API を足す。`DELETE /api/employees/{id}` で、見つかったら消して204（`NoContent()`）、見つからなければ404を返す（ヒント：`[HttpDelete("{id}")]`、`Employees.Remove(employee)`）
2. curl の `-X DELETE` で、`/api/employees/1` を消す
3. `/api/employees` を呼んで、佐藤さんがいなくなったことを確かめる

2で `HTTP/1.1 204 No Content` が返り、もう一度同じ URL を消そうとすると `404` が返れば完了です。

## 今は知らなくてよいこと

- API の説明書を自動で作る仕組み（OpenAPI）
- 「コントローラー」を使わない、より短い書き方（Minimal API）

## 次のレッスン

次はこの API から PostgreSQL のデータベースを読み書きします。
