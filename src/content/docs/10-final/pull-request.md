---
title: プルリクエストで出す
description: 業務アプリに更新の機能をブランチで足し、プルリクエストで出して、見直してから合流させる
sidebar:
  order: 2
---

## このページでできるようになること

- パスワードを記録から外して、アプリ全体を1つのリポジトリにし、GitHub に置ける
- 機能を足す作業を、ブランチ・テスト・プルリクエストの流れで進められる
- 何を変えたか、どう確かめたかを、プルリクエストに書ける

かかる時間の目安は2時間半〜3時間半です。

## 始める前に

レッスン10-1（小さな業務アプリを作る）を「確かめよう」まで終えている必要があります。

## これまでの総まとめ

このレッスンではこれまでの部で覚えたことを、すべて使います。

| 使うこと | 部 |
| --- | --- |
| コマンドで移動し、ファイルを扱う | 第1部 |
| ブランチ、コミット、プッシュ、プルリクエスト | 第2部 |
| GET と POST、ステータスコード | 第3部 |
| Docker でまとめて動かす | 第4部 |
| `UPDATE` の SQL | 第5部 |
| 型を付けて書く | 第6部 |
| `loader` と `action` | 第7部 |
| API のコントローラー、パラメーター | 第8部 |
| テストを先に書く | 第9部 |

手順は要点とヒントだけを書いています。分からないときは、書いてある部のレッスンに戻って確かめてください。

## 手で動かす準備

このレッスンでは API と画面を手で動かして確かめながら進めます。レッスン10-1の「確かめよう」を終えたままだと、Docker の API が5080番のポートを使っています。そのため、API を手で動かそうとすると「address already in use」と出て動きません。Docker で動いている3つをいったん止めて、データベースだけを動かしておきます。

```bash
cd ~/practice/business-app
docker compose down
docker compose up -d db
```

データはボリュームに残っているので、10-1で登録した社員も消えません。

## パスワードを記録から外す

この後、`business-app` 全体を Git のリポジトリにして、GitHub に送ります。今のままだと、データベースのパスワード（`secret`）が書かれた `compose.yaml` と `api1/appsettings.json` も一緒に送られます。レッスン4-2と8-3で「本物のアプリではパスワードを Git に入れない」と書きました。ここでその方法を使います。

### Docker には .env で渡す

`business-app` に `.env` というファイルを作ります。

```bash
cd ~/practice/business-app
touch .env
code .env
```

次の1行を書いて保存します。

```text
DB_PASSWORD=secret
```

`compose.yaml` で `secret` と書いてある2か所を、`${DB_PASSWORD}` に書き換えて保存します。

```yaml
  db:
    image: postgres:17
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: ${DB_PASSWORD}
```

```yaml
  api:
    build: ./api1
    environment:
      ConnectionStrings__Default: "Host=db;Port=5432;Database=practice;Username=app;Password=${DB_PASSWORD}"
```

`docker compose` は `compose.yaml` と同じフォルダにある `.env` を自動で読みます。そして `${DB_PASSWORD}` の所に `.env` に書いた値を入れて動かします。`.env` を Git の記録から外せば、パスワードは GitHub に送られません。

`.env` が読めているかを確かめます。

```bash
docker compose up -d db
```

`Running` と出れば、`.env` が読めています。データベースの設定は前と同じなので、動いているコンテナがそのまま使われます。「The "DB_PASSWORD" variable is not set」と出たときは、`.env` の場所か中身が違います（このレッスンの「困ったとき」）。

### 手で動かす API にはユーザーシークレットで渡す

`dotnet run` で手で動かす API は、`appsettings.json` の接続文字列を読んでいます。こちらは .NET の「ユーザーシークレット」で渡します。値をプロジェクトのフォルダの外（`~/.microsoft/usersecrets`）にしまっておき、開発中に動かすときだけ読み込む仕組みです。

```bash
cd ~/practice/business-app/api1
dotnet user-secrets init
dotnet user-secrets set "ConnectionStrings:Default" "Host=localhost;Port=5432;Database=practice;Username=app;Password=secret"
```

- `dotnet user-secrets init`：この API でユーザーシークレットを使う準備をする。`api1.csproj` に、しまう場所の目印（`UserSecretsId`）が書き足される
- `dotnet user-secrets set "名前" "値"`：値をしまう。`ConnectionStrings:Default` の `:` は `appsettings.json` の階層の区切りを表す（`compose.yaml` の `__` と同じ意味）

しまったら、`appsettings.json` から8-3で足した `ConnectionStrings` の3行を消して保存します。

```json
  "ConnectionStrings": {
    "Default": "Host=localhost;Port=5432;Database=practice;Username=app;Password=secret"
  },
```

API を動かして、データベースにつながることを確かめます。

```bash
dotnet run --urls http://localhost:5080
```

2つ目のターミナルで呼びます。

```bash
curl http://localhost:5080/api/employees/1
```

佐藤さんが返れば、ユーザーシークレットから接続文字列を読めています。確かめたら、Ctrl+C で API を止めます。

:::note
ユーザーシークレットは `dotnet run` で開発中に動かすときだけ読まれます。Docker で動かす API は、これまでどおり `compose.yaml` の `ConnectionStrings__Default` で受け取ります。しまった値は暗号化されないので、ユーザーシークレットは開発のときだけに使う仕組みです。
:::

`.env` とユーザーシークレットは GitHub に送られません。このリポジトリをクローンした人は、自分で `.env` を作り、`dotnet user-secrets set` を打つ必要があります。チームで使うときは、README に「`.env` に `DB_PASSWORD` を書く」のように、要る名前と手順だけを書いておきます。

## リポジトリにする

`business-app` 全体を、1つのリポジトリにします。

まず、記録しないファイルを決めます。`business-app` に `.gitignore` を作ります。

```text
node_modules/
build/
.react-router/
bin/
obj/
.env
```

`.gitignore` に書いた名前のファイルやフォルダは、Git の記録の対象から外れます。`node_modules` や `bin` は `npm install` や `dotnet build` で作り直せるので、記録しません。`.env` はさっきパスワードを書いたファイルです。

```bash
cd ~/practice/business-app
git init
git add .
git status
```

`git status` の「Changes to be committed」に `.env` が並んでいないことを確かめてから、コミットします。

```bash
git commit -m "画面・API・データベースをつないだ業務アプリ"
```

GitHub に `business-app` という名前で、README を作らない空のリポジトリを作ります。公開範囲はレッスン2-4と同じく「Private」を選びます。作った後の画面に、手元のリポジトリを GitHub につなぐコマンドが表示されるので、「…or push an existing repository from the command line」の欄のコマンドを打ちます。

```bash
git remote add origin git@github.com:yachiyo/business-app.git
git branch -M main
git push -u origin main
```

`git remote add origin …` は、レッスン2-4ではクローンで自動で行われていた「GitHub のリポジトリを `origin` という名前で覚える」設定を、手で行うコマンドです。

## 作るもの：社員の更新

社員の詳しく見るページに「直す」のリンクを置き、名前・部署・給料を直せるようにします。

| 部分 | 作るもの |
| --- | --- |
| API | `PUT /api/employees/{id}` で社員を更新する。見つからなければ404、入力に誤りがあれば400 |
| 画面 | `/employees/:id/edit` のページ。今の値が入った状態のフォームを出し、送ると更新して、詳しく見るページに戻る |

`PUT` は、レッスン3-2の「今は知らなくてよいこと」で出てきたメソッドの1つで、「この内容で置き換えて」というお願いです。

## 1. ブランチを作る

```bash
git switch -c edit-employee
```

## 2. API に更新を足す

`EmployeesController` に、次のメソッドを足します。

```csharp
    [HttpPut("{id}")]
    public async Task<ActionResult<Employee>> Update(int id, NewEmployee input)
    {
        await using var command = dataSource.CreateCommand(
            """
            UPDATE employees
            SET name = @name, department_id = @departmentId, salary = @salary
            WHERE id = @id
            """);
        command.Parameters.AddWithValue("id", id);
        command.Parameters.AddWithValue("name", input.Name);
        command.Parameters.AddWithValue("departmentId", (object?)input.DepartmentId ?? DBNull.Value);
        command.Parameters.AddWithValue("salary", input.Salary);

        await command.ExecuteNonQueryAsync();

        var employee = await FindAsync(id);
        if (employee is null)
        {
            return NotFound();
        }
        return employee;
    }
```

- `UPDATE … WHERE id = @id`：第5部の `UPDATE` と同じ。`WHERE` を忘れないこと（レッスン5-2）
- `ExecuteNonQueryAsync()`：結果の行を受け取らずに SQL を送る。`UPDATE` のように、データを変えるだけの SQL で使う
- 更新した後に `FindAsync` で社員を探し直し、部署の名前の付いた社員を返す。見つからなければ、その `id` の社員はいなかったので404を返す

手で動かして、curl で確かめます。

```bash
curl -i -X PUT -H "Content-Type: application/json" -d '{"name":"佐藤","departmentId":2,"salary":290000}' http://localhost:5080/api/employees/1
curl -i -X PUT -H "Content-Type: application/json" -d '{"name":"佐藤","departmentId":2,"salary":290000}' http://localhost:5080/api/employees/99
```

1つ目で `200` と営業部に変わった佐藤さんが、2つ目で `404` が返れば、API はできています。確かめたら、いったんコミットします。

```bash
git add .
git commit -m "API に社員の更新を足す"
```

## 3. 画面に更新を足す

### API を呼ぶ関数

`api.server.ts` に `updateEmployee(id: number, input: NewEmployee): Promise<Employee>` を足します。中身は `addEmployee` とほとんど同じで、URL を `/api/employees/${id}`、`method` を `"PUT"` にします。

### 入力の確かめ

登録と更新で、確かめる決まりは同じです。登録のページの `action` に書いた給料の確かめを、`validation.ts` に移して、両方から使えるようにしてください。

ここは第9部のやり方で、テストを先に書きます。

1. `validation.test.ts` に、給料についてのテストを書く（給料が0なら知らせる、数でなければ知らせる、など）
2. `npx vitest run` で失敗することを確かめる
3. `validation.ts` を直して、テストを通す
4. 登録のページの `action` を、直した関数を使う形にする

### 直すページ

`routes.ts` に `route("employees/:id/edit", "routes/employee-edit.tsx")` を足し、`app/routes/employee-edit.tsx` を作ります。登録のページ（`employee-new.tsx`）を写して、次の所を変えます。

- `loader`：部署の一覧に加えて、`params.id` の社員も取る。見つからなければ404（レッスン7-4）
- 入力欄：今の値が最初から入っているように、`defaultValue` に社員の値を渡す。例：`<input name="name" defaultValue={loaderData.employee.name} />`
- `action`：`params.id` と入力を `updateEmployee` に渡し、終わったら ``redirect(`/employees/${params.id}`)`` で詳しく見るページに戻る

最後に、詳しく見るページ（`employee.tsx`）に、直すページへの `Link` を足します。

### 確かめる

```bash
npm run typecheck
npx vitest run
npm run dev
```

型の検査とテストが通り、画面で次のことができれば完成です。

- 詳しく見るページから「直す」へ移ると、今の値が入ったフォームが出る
- 給料を変えて送ると、詳しく見るページに戻り、変えた給料が表示される
- 名前を空にして送ると、知らせが出て、更新されない

確かめたら、コミットしてプッシュします。

```bash
git add .
git commit -m "画面に社員の更新を足す"
git push -u origin edit-employee
```

## 4. プルリクエストを出す

GitHub でプルリクエストを出します（レッスン2-5）。説明の欄には、見る人が知りたいことを、次の4つに分けて書きます。

```markdown
## 何を変えたか
社員の名前・部署・給料を直せるようにしました。

## なぜ
登録した後に、異動や昇給を反映する方法がなかったため。

## どう確かめたか
- API：curl で、更新できること、ない社員は404になることを確かめた
- 画面：今の値が入ったフォームが出ること、更新できること、名前が空なら知らせが出ることを確かめた
- `npm run typecheck`、`npx vitest run`、`dotnet test api1.Tests` がすべて通る

## 見てほしい点
入力の確かめを、登録と更新で共通の関数にまとめました。まとめ方に違和感がないか見てください。
```

特に「どう確かめたか」が大事です。見る人はこの欄を読んで、自分でも確かめるべきかどうかを判断します。

## 5. 出す前に、自分で見直す

人に見てもらう前に、プルリクエストの「Files changed」で、自分の変更を上から読み直します。手元のエディタで見るのとは違う画面で見ると、見落としに気づきやすくなります。

次のことを確かめてください。

- 確かめるために足した `console.log` が残っていない
- パスワードなどの、人に見せてはいけない情報が入っていない。パスワードは `.env` とユーザーシークレットに置き、コードや設定のファイルには書かない
- 使わなくなったコードやファイルが残っていない
- 今回の機能と関係のない変更が混ざっていない

見つけたら、手元で直して、コミットしてプッシュします。プルリクエストに自動で加わります（レッスン2-5）。

## 6. 合流させる

一緒に学んでいる人や、先輩に見てもらえるなら、レビューを頼みます。指摘を受けたら直してプッシュし、また見てもらいます。1人で進めているときは、1日おいてから「Files changed」をもう一度読み直すと、レビューの代わりになります。

問題がなければ合流させ、手元の `main` を最新にします。

```bash
git switch main
git pull
git branch -d edit-employee
```

最後に、手で動かしている API と画面を Ctrl+C で止めます。そのあと Docker でまとめて動かして、更新ができることを確かめます。

```bash
docker compose up -d --build
```

## 困ったとき

- **`docker compose` で「The "DB_PASSWORD" variable is not set」と出た**：`.env` が `compose.yaml` と同じフォルダにないか、中の名前が違います。`business-app/.env` に `DB_PASSWORD=secret` と書いてあるか確かめてください。
- **`dotnet run` で「System.ArgumentNullException: Value cannot be null. (Parameter 'Host')」と出た**：接続文字列が読めていません。`api1` のフォルダで `dotnet user-secrets list` を打ち、`ConnectionStrings:Default` が出るか確かめてください。出なければ、`dotnet user-secrets set` をもう一度打ちます。
- **`dotnet run` で「address already in use」と出た**：Docker の API が5080番のポートを使っています。「手で動かす準備」の `docker compose down` と `docker compose up -d db` を打ってください。
- **`git push` やプルリクエストでうまくいかない**：レッスン2-4と2-5の「困ったとき」を見てください。

## 確かめよう

次の5つがそろえば、この教材の総仕上げは完了です。

1. GitHub の `business-app` の `main` に、更新の機能が合流している
2. プルリクエストに、「何を変えたか」「なぜ」「どう確かめたか」「見てほしい点」が書かれている
3. `docker compose up -d --build` で動かしたアプリ（`http://localhost:3000/employees`）で、社員を登録し、直せる
4. `npm run typecheck`、`npx vitest run`、`dotnet test api1.Tests` がすべて通る
5. GitHub の `business-app` に `.env` がなく、`compose.yaml` と `api1/appsettings.json` にパスワード（`secret`）が書かれていない

## ここまで来たら

お疲れさまでした。コマンドを1つも打ったことがないところから始めて、画面・API・データベースのそろったアプリを、チームの開発と同じ流れで作れるようになりました。

ここから先は、仕事のコードを読むことが一番の勉強になります。分からない書き方に出会ったら、この教材のどの部の話かを考えると、調べる手がかりが見つかるはずです。

もう一歩進みたいときに読む資料は、[さらに学ぶ](../../next-steps/)に部ごとにまとめています。

## 今は知らなくてよいこと

- プルリクエストを出したときに、テストを自動で動かす仕組み（CI）。[さらに学ぶ](../../next-steps/)で資料を紹介しています
- アプリを本番のサーバーに置く方法
