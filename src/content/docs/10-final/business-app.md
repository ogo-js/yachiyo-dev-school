---
title: 小さな業務アプリを作る
description: 画面・API・データベースを1つにつなぎ、Docker でまとめて動かす
sidebar:
  order: 1
---

## このページでできるようになること

- 画面の `loader` と `action` から、自分で作った API を呼べる
- 画面・API・データベースの3つを、手元で別々に動かしてつなげられる
- 3つを Docker でまとめて、コマンド1つで動かせる

かかる時間の目安は2〜3時間です。いくつかに分けて進めてかまいません。

## 始める前に

第7部（React と React Router）、第8部（C# と ASP.NET Core）、第9部（テスト）を終えている必要があります。このレッスンでは次の3つを使います。

- `~/practice/rr1`：第7部と第9部で作った画面
- `~/practice/api1` と `~/practice/api1.Tests`：第8部と第9部で作った API とテスト
- `~/practice/compose1/sample.sql`：第5部の練習用のデータ

## 何を作るか

これまで別々に作ってきたものを、1本につなぎます。

```text
ブラウザ → 画面（React Router） → API（ASP.NET Core） → データベース（PostgreSQL）
```

- 画面の `loader` は社員のデータを自分のメモリからではなく、API から取る
- 画面の `action` は登録するときに API に送る
- API はデータベースを読み書きする

一覧・詳しく見る・登録の3つの画面が、データベースのデータで動くようになれば完成です。

## 1つのフォルダにまとめる

3つを1つのフォルダにまとめます。

```bash
mkdir -p ~/practice/business-app
cd ~/practice/business-app
cp -r ../rr1 ../api1 ../api1.Tests .
cp ../compose1/sample.sql .
rm -rf rr1/node_modules rr1/.git api1/bin api1/obj api1.Tests/bin api1.Tests/obj
```

最後の行ではコピーしなくてよいもの（あとで作り直せるもの）と、`rr1` を作ったときにできた Git の記録を消しています。Git の記録は次のレッスンで、このフォルダ全体で作り直します。

```text
~/practice/business-app
├── api1          … API
├── api1.Tests    … API のテスト
├── rr1           … 画面
└── sample.sql    … 練習用のデータ
```

## データベースを用意する

`business-app` に `compose.yaml` を作ります。

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
      - ./sample.sql:/docker-entrypoint-initdb.d/sample.sql

volumes:
  db-data:
```

`./sample.sql:/docker-entrypoint-initdb.d/sample.sql` は、`sample.sql` をコンテナの中の決まった場所に置く指定です。PostgreSQL のイメージはデータベースを初めて作るときに、この場所にある SQL を自動で流し込みます。レッスン5-1で手で流し込んだ手順が要らなくなります。

:::note
`compose1` で使っていた8080番のポートや5432番のポートを使ったままだと、ぶつかります。先に `~/practice/compose1` で `docker compose down` を打って止めておいてください。
:::

```bash
cd ~/practice/business-app
docker compose up -d db
```

`docker compose up -d db` のように、サービスの名前を付けると、そのサービスだけを動かせます。

初めて動かすときは、`sample.sql` を流し込むので、データベースの準備にいつもより少し時間がかかります。10秒ほど待ってから、データが入ったかを確かめます。

```bash
docker compose exec db psql -U app -d practice -c "SELECT count(*) FROM employees;"
```

`6` と出れば、練習用のデータが入っています。「the database system is starting up」などと出たときは、準備がまだ終わっていません（レッスン4-3）。数秒待ってから打ち直してください。

## API を直す

画面に部署の名前を出せるように、API を直します。

### 社員に部署の名前を付ける

`api1/Controllers/EmployeesController.cs` を、次のように書き換えます。レッスン5-3の `LEFT JOIN` を使って、部署の名前も一緒に返します。

```csharp
using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Mvc;
using Npgsql;

namespace api1.Controllers;

public record Employee(int Id, string Name, int? DepartmentId, string? DepartmentName, int Salary);

public record NewEmployee(
    [Required(ErrorMessage = "名前を入れてください")] string Name,
    int? DepartmentId,
    [Range(1, 10000000, ErrorMessage = "給料は1以上で入れてください")] int Salary);

[ApiController]
[Route("api/employees")]
public class EmployeesController(NpgsqlDataSource dataSource) : ControllerBase
{
    private const string SelectEmployees = """
        SELECT e.id, e.name, e.department_id, d.name, e.salary
        FROM employees AS e
        LEFT JOIN departments AS d ON e.department_id = d.id
        """;

    [HttpGet]
    public async Task<List<Employee>> GetAll(string? name)
    {
        await using var command = dataSource.CreateCommand(
            SelectEmployees + " WHERE e.name LIKE @pattern ORDER BY e.id");
        command.Parameters.AddWithValue("pattern", $"%{name}%");
        await using var reader = await command.ExecuteReaderAsync();

        var employees = new List<Employee>();
        while (await reader.ReadAsync())
        {
            employees.Add(ReadEmployee(reader));
        }
        return employees;
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<Employee>> GetOne(int id)
    {
        var employee = await FindAsync(id);
        if (employee is null)
        {
            return NotFound();
        }
        return employee;
    }

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
        var employee = await FindAsync(id);
        return CreatedAtAction(nameof(GetOne), new { id }, employee);
    }

    private async Task<Employee?> FindAsync(int id)
    {
        await using var command = dataSource.CreateCommand(SelectEmployees + " WHERE e.id = @id");
        command.Parameters.AddWithValue("id", id);
        await using var reader = await command.ExecuteReaderAsync();

        if (!await reader.ReadAsync())
        {
            return null;
        }
        return ReadEmployee(reader);
    }

    private static Employee ReadEmployee(NpgsqlDataReader reader)
    {
        return new Employee(
            reader.GetInt32(0),
            reader.GetString(1),
            reader.IsDBNull(2) ? null : reader.GetInt32(2),
            reader.IsDBNull(3) ? null : reader.GetString(3),
            reader.GetInt32(4));
    }
}
```

8-3からの主な違いは次のとおりです。

- 社員の型に `DepartmentName`（部署の名前）を足した
- 一覧と1人分で同じ `SELECT` を使うので、`SelectEmployees` という定数にまとめた
- 1人分を探す処理を `FindAsync` にまとめ、`GetOne` と `Create` の両方から使うようにした。登録した後も、部署の名前の付いた社員を返せる
- 一覧の `GetAll(string? name)`：`/api/employees?name=藤` のように、クエリ文字列の `name` を受け取る。`?name=` が付いていないときは `null` になる
- `LIKE @pattern`：名前に `name` を含む社員だけを返す（レッスン5-1の `LIKE`）。前後に `%` を付けた値もパラメーターで渡す（レッスン8-3）。`name` が `null` のときは `%%` になり、全員を返す

### 部署の一覧を返す

登録の画面で部署を選べるように、部署の一覧の API を足します。`api1/Controllers/DepartmentsController.cs` を作ります。

```csharp
using Microsoft.AspNetCore.Mvc;
using Npgsql;

namespace api1.Controllers;

public record Department(int Id, string Name);

[ApiController]
[Route("api/departments")]
public class DepartmentsController(NpgsqlDataSource dataSource) : ControllerBase
{
    [HttpGet]
    public async Task<List<Department>> GetAll()
    {
        await using var command = dataSource.CreateCommand("SELECT id, name FROM departments ORDER BY id");
        await using var reader = await command.ExecuteReaderAsync();

        var departments = new List<Department>();
        while (await reader.ReadAsync())
        {
            departments.Add(new Department(reader.GetInt32(0), reader.GetString(1)));
        }
        return departments;
    }
}
```

API を動かして、確かめます。

```bash
cd ~/practice/business-app/api1
dotnet run --urls http://localhost:5080
```

2つ目のターミナルで呼びます。

```bash
curl http://localhost:5080/api/employees/6
curl http://localhost:5080/api/departments
curl -G --data-urlencode "name=藤" http://localhost:5080/api/employees
```

3つ目の `-G --data-urlencode "name=藤"` は、`?name=藤` を URL に付けて GET で送る指定です。「藤」のような日本語は URL にそのまま書けないので、`%E8%97%A4` のような形に直して付けてくれます（レッスン3-2のサーバーのログと同じ形）。

渡辺さんの `"departmentName":null` と、3つの部署と、佐藤さん・伊藤さんの2人が返れば、API はできています。API は動かしたままにしておきます。

## 画面を API につなぐ

### API を呼ぶ関数

`rr1` で、第7部で作ったメモリの中のデータのファイルを消し、API を呼ぶファイルを作ります。

```bash
cd ~/practice/business-app/rr1
npm install
rm app/data/employees.server.ts
touch app/data/api.server.ts
code app/data/api.server.ts
```

`npm install` は、さっき消した `node_modules` を、`package.json` を見て入れ直すコマンドです。

```typescript
const API_URL = process.env.API_URL ?? "http://localhost:5080";

export type Employee = {
  id: number;
  name: string;
  departmentId: number | null;
  departmentName: string | null;
  salary: number;
};

export type Department = {
  id: number;
  name: string;
};

export type NewEmployee = {
  name: string;
  departmentId: number;
  salary: number;
};

export async function getEmployees(name: string): Promise<Employee[]> {
  const response = await fetch(`${API_URL}/api/employees?name=${encodeURIComponent(name)}`);
  if (!response.ok) {
    throw new Error(`社員の一覧を取れませんでした（${response.status}）`);
  }
  return response.json();
}

export async function getEmployee(id: number): Promise<Employee | undefined> {
  const response = await fetch(`${API_URL}/api/employees/${id}`);
  if (response.status === 404) {
    return undefined;
  }
  if (!response.ok) {
    throw new Error(`社員を取れませんでした（${response.status}）`);
  }
  return response.json();
}

export async function getDepartments(): Promise<Department[]> {
  const response = await fetch(`${API_URL}/api/departments`);
  if (!response.ok) {
    throw new Error(`部署の一覧を取れませんでした（${response.status}）`);
  }
  return response.json();
}

export async function addEmployee(input: NewEmployee): Promise<Employee> {
  const response = await fetch(`${API_URL}/api/employees`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  if (!response.ok) {
    throw new Error(`社員を登録できませんでした（${response.status}）`);
  }
  return response.json();
}
```

- `process.env.API_URL ?? "http://localhost:5080"`：API の URL を、「環境変数」の `API_URL` から読む。決められていなければ、手元で動かしている API の URL を使う。環境変数はプログラムの外から設定を渡す仕組みで、後で Docker で動かすときに使う
- `response.ok`：ステータスコードが200番台なら `true`。うまくいかなかったときは、エラーを投げて止める
- `encodeURIComponent(name)`：検索の文字を URL に載せられる形（`%E8%97%A4` など）に直す。curl の `--data-urlencode` と同じ働き
- 型の名前は、API が返す JSON の形（8-3）と合わせている。API の `departmentName` が `null` のこともあるので、`string | null` にしている

`.server` を付けた名前にしているので、このファイルはブラウザに送られません（レッスン7-4）。API の URL のような情報を、ブラウザに見せずに済みます。

### 一覧と、詳しく見るページ

`app/routes/employees.tsx` は `import` の1行と、`loader` と、`EmployeeCard` に渡す部署を直します。

```tsx
import { getEmployees } from "../data/api.server";
```

```tsx
export async function loader({ request }: Route.LoaderArgs) {
  const url = new URL(request.url);
  const q = url.searchParams.get("q") ?? "";
  const employees = await getEmployees(q);
  return { employees, q };
}
```

```tsx
<EmployeeCard name={employee.name} department={employee.departmentName ?? "（部署なし）"} />
```

7-4では全員を取ってから `filter` で絞っていました。今度は検索の文字を API に渡し、データベースで絞った結果だけを受け取ります。社員が増えても、要る人の分だけが届きます。

`app/routes/employee.tsx` も、`import` の1行を `api.server` に変え、部署と給料を表示します。

```tsx
import { getEmployee } from "../data/api.server";
```

```tsx
      <p>部署：{employee.departmentName ?? "（部署なし）"}</p>
      <p>給料：{employee.salary.toLocaleString()}円</p>
```

`toLocaleString()` は、`280000` を `280,000` のように、3桁ごとに区切って表示します。

### 登録のページ

`app/routes/employee-new.tsx` を、次のように書き換えます。部署の選択肢を API から取り、給料の入力欄を足しています。

```tsx
import { Form, data, redirect } from "react-router";
import type { Route } from "./+types/employee-new";
import { addEmployee, getDepartments } from "../data/api.server";
import { validateEmployee, type EmployeeErrors } from "../data/validation";

export async function loader() {
  const departments = await getDepartments();
  return { departments };
}

export async function action({ request }: Route.ActionArgs) {
  const formData = await request.formData();
  const name = String(formData.get("name") ?? "").trim();
  const departmentId = String(formData.get("departmentId") ?? "");
  const salary = Number(formData.get("salary"));

  const errors: EmployeeErrors & { salary?: string } = validateEmployee(name, departmentId);
  if (!(salary > 0)) {
    errors.salary = "給料は1以上の数で入れてください";
  }
  if (errors.name || errors.department || errors.salary) {
    return data({ errors }, { status: 400 });
  }

  await addEmployee({ name, departmentId: Number(departmentId), salary });
  return redirect("/employees");
}

export default function EmployeeNew({ loaderData, actionData }: Route.ComponentProps) {
  return (
    <main>
      <h1>社員の登録</h1>
      <Form method="post">
        <p>
          <label>
            名前：<input name="name" />
          </label>
        </p>
        {actionData?.errors.name && <p>{actionData.errors.name}</p>}
        <p>
          <label>
            部署：
            <select name="departmentId" defaultValue="">
              <option value="">選んでください</option>
              {loaderData.departments.map((department) => (
                <option key={department.id} value={department.id}>
                  {department.name}
                </option>
              ))}
            </select>
          </label>
        </p>
        {actionData?.errors.department && <p>{actionData.errors.department}</p>}
        <p>
          <label>
            給料：<input name="salary" type="number" />
          </label>
        </p>
        {actionData?.errors.salary && <p>{actionData.errors.salary}</p>}
        <button type="submit">登録する</button>
      </Form>
    </main>
  );
}
```

- 部署の選択肢は `loader` で API から取った一覧を `map` で並べている。部署を増やしても、画面を直さずに済む
- 入力の確かめは9-3で作った `validateEmployee` をそのまま使い、給料の確かめだけを足している
- `EmployeeErrors & { salary?: string }`：「`EmployeeErrors` の項目に、`salary` も足した型」という意味

### 部署ごとの一覧のページを外す

レッスン7-4の「確かめよう」で作った部署ごとの一覧のページ（`departments/:name`）は、さっき消した `employees.server` を使っています。このアプリでは使わないので、外します。

`app/routes.ts` から、次のような `departments/:name` の行を消します。ファイルの名前は7-4で自分で付けたものになっています。

```ts
  route("departments/:name", "routes/department.tsx"),
```

その行に書いてあるページのファイルも消します。`department.tsx` という名前なら、次のように打ちます。

```bash
rm app/routes/department.tsx
```

### つないで確かめる

型の検査とテストが通ることを確かめてから、画面を動かします。

```bash
npm run typecheck
npx vitest run
npm run dev
```

ブラウザで `http://localhost:5173/employees` を開き、次のことを確かめます。

- 第5部のデータの社員が並び、渡辺さんは「（部署なし）」と表示される
- 検索欄に「藤」と入れて「探す」を押すと、URL が `/employees?q=藤` になり、佐藤さんと伊藤さんだけが表示される
- 「詳しく見る」で、部署と給料が表示される
- 登録のページで、部署の選択肢が3つ出る。登録すると一覧に増える
- 画面と API を止めて動かし直しても、登録した社員が残っている

最後の点が第7部との一番の違いです。データは画面のメモリではなく、データベースにあります。

## Docker でまとめて動かす

ここまでは、データベースだけを Docker で動かし、API と画面は手で動かしていました。最後に、3つとも Docker で動かします。確かめたら、API と画面は Ctrl+C で止めておきます。

### API のイメージの作り方を書く

自分で作ったアプリをコンテナで動かすには、イメージの作り方を書いた「Dockerfile」が要ります。`api1/Dockerfile` を作ります。

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src
COPY api1.csproj .
RUN dotnet restore
COPY . .
RUN dotnet publish -c Release -o /app

FROM mcr.microsoft.com/dotnet/aspnet:10.0
WORKDIR /app
COPY --from=build /app .
ENTRYPOINT ["dotnet", "api1.dll"]
```

- 前半（`sdk`）：.NET の開発の道具が入ったイメージの中で、API をビルドする
- 後半（`aspnet`）：動かすのに必要なものだけが入った小さなイメージに、ビルドの結果だけを写して動かす

イメージを作るときに、手元の `bin` や `obj` を写さないように、`api1/.dockerignore` も作ります。

```text
bin/
obj/
```

画面の `rr1` には、プロジェクトを作ったときに `Dockerfile` と `.dockerignore` が最初から入っています。

### compose.yaml に API と画面を足す

`business-app/compose.yaml` を、次のように書き換えます。

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
      - ./sample.sql:/docker-entrypoint-initdb.d/sample.sql
  api:
    build: ./api1
    environment:
      ConnectionStrings__Default: "Host=db;Port=5432;Database=practice;Username=app;Password=secret"
    ports:
      - "5080:8080"
    depends_on:
      - db
  web:
    build: ./rr1
    environment:
      API_URL: "http://api:8080"
    ports:
      - "3000:3000"
    depends_on:
      - api

volumes:
  db-data:
```

- `build: ./api1`：イメージを Docker Hub から取ってくる代わりに、`api1` の `Dockerfile` から作る
- `ConnectionStrings__Default`：`appsettings.json` の `ConnectionStrings` の `Default` を、環境変数で上書きする。`__`（アンダースコア2つ）が JSON の階層の区切りを表す。コンテナの中から見ると、データベースは `localhost` ではなく `db` という名前の相手なので（レッスン4-2）、`Host=db` にしている
- `API_URL: "http://api:8080"`：画面から見た API の URL。API のコンテナは中では8080番で待っている
- `"3000:3000"`：画面のコンテナは3000番で待っている

### 動かす

```bash
cd ~/practice/business-app
docker compose up -d --build
```

`--build` は「イメージを作り直してから動かす」という意味です。初めてのときは、イメージを作るのに数分かかります。

```bash
docker compose ps
```

`db`、`api`、`web` の3つが動いていれば、ブラウザで `http://localhost:3000/employees` を開きます。手で動かしたときと同じように、一覧・詳しく見る・登録ができれば完成です。

これで、`compose.yaml` のあるフォルダで `docker compose up -d --build` を打つだけで、誰のパソコンでも同じアプリが動くようになりました。

## 困ったとき

- **`npm run typecheck` で「Cannot find module '../data/employees.server'」と出た**：消したファイルをまだ読み込んでいるファイルがあります。表示されたファイルの `import` を `../data/api.server` に直すか、使っていないファイルなら消してください。
- **画面に「社員の一覧を取れませんでした」や、接続のエラーが出た**：API が動いているか確かめてください。手で動かしているときは `dotnet run`、Docker のときは `docker compose ps` で `api` が動いているかを見ます。
- **Docker で動かすと API が「Failed to connect to 127.0.0.1:5432」のように出る**：接続文字列が `localhost` のままです。`compose.yaml` の `ConnectionStrings__Default` の `Host=db` を確かめてください。
- **curl で `?name=藤` のように日本語を直接書くと、`400` が返る**：URL には日本語をそのまま書けません。`curl -G --data-urlencode "name=藤" …` のように送ってください。
- **`docker compose logs api` や `docker compose logs web` でエラーを見たい**：サービスの名前を付けてログを見ると、どのコンテナで何が起きたかが分かります。
- **データベースに練習用のデータが入らない**：`sample.sql` は、データベースを初めて作るときにだけ流し込まれます。入れ直すときは、`docker compose down -v` でボリュームごと消してから動かします（データはすべて消えます）。

## 確かめよう

1. `docker compose up -d --build` で3つを動かし、`http://localhost:3000/employees` から「中村、開発部、270000」の社員を登録する
2. `docker compose down` で止めてから、もう一度 `docker compose up -d` で動かす
3. 中村さんが一覧に残っていることを確かめる
4. `curl http://localhost:5080/api/employees` でも、中村さんが返ることを確かめる

3と4で中村さんが確かめられれば完了です。画面・API・データベースが、1本につながっています。

## 今は知らなくてよいこと

- 本番のサーバーに置くための設定（HTTPS、パスワードの渡し方など）
- 検索の文字に入った `%` や `_` を、ただの文字として扱う方法。今は「何文字でもよい」「どれか1文字」の印として働くので、`_` で探すと全員が返る
- 画面のテストを Docker の中で動かす方法

## 次のレッスン

次はこのアプリに「更新」の機能を足します。足すときは、チームの開発と同じように、ブランチを作ってプルリクエストで出し、レビューを受けてから合流させます。
