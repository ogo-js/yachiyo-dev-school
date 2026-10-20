---
title: データベースにつなぐ
description: API から PostgreSQL につなぎ、SQL でデータを読み書きする
sidebar:
  order: 3
---

## このページでできるようになること

- API から、Docker で動かしている PostgreSQL につなげられる
- 第5部で覚えた SQL を、C# から送って結果を受け取れる
- 値を SQL に埋め込むときに、パラメーターを使う理由を説明できる

かかる時間の目安は60分です。

## 始める前に

レッスン8-2（Web API を作る）と、第5部（データベース）を終えている必要があります。このレッスンでは第5部で使った `~/practice/compose1` のデータベースを使います。

## なぜこれを覚えるのか

8-2の API は社員の一覧をプログラムのメモリに持っていたので、止めると登録した社員が消えました。実際のアプリでは、データはデータベースに保存します。

API とデータベースのやり取りは第5部で手で打った SQL を、プログラムから送るだけです。新しく覚えることは、つなぎ方と、値の渡し方の2つです。

## データベースに外からつなげるようにする

レッスン4-2では、データベースはコンテナどうしでつながれば足りたので、ポートを開けていませんでした。今回はパソコンで動かす API からつなぐので、ポートを開けます。

`~/practice/compose1/compose.yaml` の `db` に、`ports` の2行を足して保存します。

```yaml
services:
  db:
    image: postgres:17
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: practice
    ports:
      - "5432:5432"
    volumes:
      - db-data:/var/lib/postgresql/data
  adminer:
    image: adminer
    ports:
      - "8080:8080"
    depends_on:
      - db

volumes:
  db-data:
```

設定を変えたので、作り直して動かします。データはボリュームにあるので消えません。

```bash
cd ~/practice/compose1
docker compose up -d
```

## Npgsql を入れる

C# から PostgreSQL につなぐには、Npgsql という部品（パッケージ）を使います。8-2の `api1` に入れます。

```bash
cd ~/practice/api1
dotnet add package Npgsql
```

`dotnet add package` は、インターネットからパッケージを取ってきて、プロジェクトに足すコマンドです。npm の `npm install` にあたります。

## つなぎ先を設定に書く

`appsettings.json` を開き、最初の `{` のすぐ下に、`ConnectionStrings` の3行を足して保存します。

```json
{
  "ConnectionStrings": {
    "Default": "Host=localhost;Port=5432;Database=practice;Username=app;Password=secret"
  },
  "Logging": {
```

`Logging` から下はもとのままにしておきます。この1行の文字列を「接続文字列」と呼び、どのサーバーの、どのデータベースに、誰としてつなぐかを書きます。

:::caution
パスワードを設定のファイルに直接書くのは、練習だからです。本物のアプリではパスワードを Git に入れないように、別の方法で渡します。
:::

## つなぐ準備：Program.cs

`Program.cs` を、次のように書き換えて保存します。増えたのは、`using Npgsql;` と、`connectionString` から始まる2行です。

```csharp
using System.Text.Encodings.Web;
using System.Text.Unicode;
using Npgsql;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers().AddJsonOptions(options =>
{
    options.JsonSerializerOptions.Encoder = JavaScriptEncoder.Create(UnicodeRanges.All);
});

var connectionString = builder.Configuration.GetConnectionString("Default");
builder.Services.AddSingleton(NpgsqlDataSource.Create(connectionString!));

var app = builder.Build();

app.MapControllers();

app.Run();
```

- `GetConnectionString("Default")`：`appsettings.json` の `ConnectionStrings` から、`Default` の値を読む
- `NpgsqlDataSource.Create(…)`：データベースへのつなぎ口を作る
- `builder.Services.AddSingleton(…)`：作ったつなぎ口を ASP.NET Core に預ける。預けたものは、コントローラーが必要なときに受け取れる

## データベースから読む

`Controllers/EmployeesController.cs` を、次のように書き換えて保存します。社員の型を、第5部の `employees` の表に合わせています。

```csharp
using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Mvc;
using Npgsql;

namespace api1.Controllers;

public record Employee(int Id, string Name, int? DepartmentId, int Salary);

[ApiController]
[Route("api/employees")]
public class EmployeesController(NpgsqlDataSource dataSource) : ControllerBase
{
    [HttpGet]
    public async Task<List<Employee>> GetAll()
    {
        await using var command = dataSource.CreateCommand(
            "SELECT id, name, department_id, salary FROM employees ORDER BY id");
        await using var reader = await command.ExecuteReaderAsync();

        var employees = new List<Employee>();
        while (await reader.ReadAsync())
        {
            employees.Add(ReadEmployee(reader));
        }
        return employees;
    }

    private static Employee ReadEmployee(NpgsqlDataReader reader)
    {
        return new Employee(
            reader.GetInt32(0),
            reader.GetString(1),
            reader.IsDBNull(2) ? null : reader.GetInt32(2),
            reader.GetInt32(3));
    }
}
```

- `EmployeesController(NpgsqlDataSource dataSource)`：コントローラーを作るときに、`Program.cs` で預けたつなぎ口を受け取る
- `CreateCommand("SELECT …")`：送る SQL を用意する。第5部で打った SQL と同じもの
- `ExecuteReaderAsync()`：SQL を送り、結果を1行ずつ読む準備をする。データベースとのやり取りは待つ処理なので、`await` を付ける（レッスン6-3と同じ考え方）
- `while (await reader.ReadAsync())`：結果の行がある間、1行ずつ読む
- `reader.GetInt32(0)`：その行の0番目（`id`）の列を整数として読む。`GetString(1)` は1番目（`name`）を文字列として読む
- `int?`：`?` が付いた型は、値がない（`null`）こともある。部署のない渡辺さんのために、`DepartmentId` を `int?` にしている
- `await using var`：使い終わったら、つなぎを自動で片付ける

動かして呼びます。

```bash
dotnet run --urls http://localhost:5080
```

```bash
curl http://localhost:5080/api/employees
```

```text
[{"id":1,"name":"佐藤","departmentId":1,"salary":280000},{"id":2,"name":"鈴木","departmentId":2,"salary":320000},…,{"id":6,"name":"渡辺","departmentId":null,"salary":230000}]
```

途中を省いています。第5部で入れた社員が API から返ってきます。給料の値は第5部で変えたとおりになっています。

## 1人分を読む：パラメーター

`GetAll` の下に、次のメソッドを足します。

```csharp
    [HttpGet("{id}")]
    public async Task<ActionResult<Employee>> GetOne(int id)
    {
        await using var command = dataSource.CreateCommand(
            "SELECT id, name, department_id, salary FROM employees WHERE id = @id");
        command.Parameters.AddWithValue("id", id);
        await using var reader = await command.ExecuteReaderAsync();

        if (!await reader.ReadAsync())
        {
            return NotFound();
        }
        return ReadEmployee(reader);
    }
```

SQL の中の `@id` は「ここに値が入る」という印です。`Parameters.AddWithValue("id", id)` で、その印に入れる値を渡しています。このように値を別に渡す仕組みを「パラメーター」と呼びます。

## なぜ値を SQL の文字に直接つなげないのか

次のように、SQL の文字に値を直接つなげても、動きはします。

```csharp
// してはいけない書き方
var sql = $"SELECT id, name FROM employees WHERE name = '{name}'";
```

ところが、`name` に `' OR '1'='1` という文字が送られてくると、SQL は次のようになります。

```sql
SELECT id, name FROM employees WHERE name = '' OR '1'='1'
```

`'1'='1'` は必ず正しいので、全員のデータが返ってしまいます。送られてきた文字で SQL を書き換えられてしまうこの攻撃を「SQL インジェクション」と呼びます。

:::danger[利用者から受け取った値は、必ずパラメーターで渡す]
パラメーターで渡した値は、SQL の一部ではなく、ただの値として扱われます。どんな文字が送られてきても、SQL を書き換えられることはありません。
:::

## 登録する

ファイルの先頭近くの `public record Employee` の行の下に、登録で受け取る型を足します。

```csharp
public record NewEmployee(
    [Required(ErrorMessage = "名前を入れてください")] string Name,
    int? DepartmentId,
    [Range(1, 10000000, ErrorMessage = "給料は1以上で入れてください")] int Salary);
```

`GetOne` の下に、次のメソッドを足します。

```csharp
    [HttpPost]
    public async Task<ActionResult<Employee>> Create(NewEmployee input)
    {
        await using var command = dataSource.CreateCommand(
            """
            INSERT INTO employees (id, name, department_id, salary, hired_on)
            VALUES ((SELECT COALESCE(MAX(id), 0) + 1 FROM employees), @name, @departmentId, @salary, CURRENT_DATE)
            RETURNING id
            """);
        command.Parameters.AddWithValue("name", input.Name);
        command.Parameters.AddWithValue("departmentId", (object?)input.DepartmentId ?? DBNull.Value);
        command.Parameters.AddWithValue("salary", input.Salary);

        var id = (int)(await command.ExecuteScalarAsync())!;
        var employee = new Employee(id, input.Name, input.DepartmentId, input.Salary);
        return CreatedAtAction(nameof(GetOne), new { id }, employee);
    }
```

- `"""` で囲むと、何行にもわたる文字列を、そのまま書ける
- `(SELECT COALESCE(MAX(id), 0) + 1 FROM employees)`：今ある一番大きい `id` に1を足して、新しい `id` にする
- `CURRENT_DATE`：入社日は今日の日付にする
- `RETURNING id`：登録した行の `id` を返してもらう
- `ExecuteScalarAsync()`：結果の1つの値だけを受け取る
- `(object?)input.DepartmentId ?? DBNull.Value`：部署が空（`null`）なら、データベースの「値がない」（`NULL`）として渡す

:::note
`MAX(id) + 1` で番号を決める方法は、2人が同時に登録すると同じ番号になることがあります。練習なのでこの形にしていますが、本物のアプリではデータベースに自動で番号を振らせる仕組みを使います。
:::

動かし直して、登録します。

```bash
curl -i -X POST -H "Content-Type: application/json" -d '{"name":"中村","departmentId":3,"salary":270000}' http://localhost:5080/api/employees
```

`HTTP/1.1 201 Created` と、`"id":7` の中村さんが返れば登録できています。

API を止めて動かし直しても、`/api/employees/7` で中村さんが返ります。データベースに保存されているからです。Adminer（`http://localhost:8080`）や psql で、`employees` の表を見て確かめることもできます。

## 困ったとき

- **「Failed to connect to 127.0.0.1:5432」のように出た**：データベースが動いていないか、ポートを開けていません。`compose.yaml` に `ports` を足したか、`docker compose up -d` を打ったか確かめてください。
- **「password authentication failed for user "app"」と出た**：接続文字列のユーザー名かパスワードが、`compose.yaml` と違います。
- **「relation "employees" does not exist」と出た**：第5部の練習用のデータが入っていません。レッスン5-1の手順で `sample.sql` を流し込んでください。
- **「Unable to cast object of type 'System.DBNull'」と出た**：`NULL` の入った列を、`IsDBNull` で確かめずに読んでいます。

## 確かめよう

1. 部署の番号を受け取り、その部署の社員だけを返す API を足す。`GET /api/departments/{id}/employees` で呼べるようにする（ヒント：コントローラーに `[HttpGet("/api/departments/{id}/employees")]` のメソッドを足し、`WHERE department_id = @id` で絞る）
2. curl で `/api/departments/3/employees` を呼ぶ

高橋さん、伊藤さん、さっき登録した中村さんの3人が返れば完了です。

## 今は知らなくてよいこと

- SQL を書かずに、C# のクラスからデータベースを扱う仕組み（Entity Framework Core など）
- パスワードを設定のファイルに書かずに渡す方法

## 次のレッスン

これで第8部は終わりです。画面、API、データベースの3つがそろいました。次からは第9部です。作ったものが正しく動き続けることを、自動のテストで確かめます。
