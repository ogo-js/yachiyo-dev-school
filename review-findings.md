# 教材のチェック結果

教材の正しさと抜けを確かめた結果です。A-1〜A-5 と B-9 の6件は直しました（2026-10-27）。それぞれの「対応」に、直したことと確かめた結果を書いています。ほかはまだ直していません。直すときに、ここから選んで Issue にするかを決めます。

## 結果のまとめ

第1部〜第10部の本文と「確かめよう」を、新しい Ubuntu で順に打ちました。ほとんどの手順は書いてあるとおりに動きました。React Router は v8、TypeScript は 7 と、原稿を書いたころより新しい版が入りましたが、本文のコードはそのまま動きました。

指摘は次の数です。

| 重さ | 数 | 意味 |
| --- | --- | --- |
| A | 5 | 動かない、または事実と違う |
| B | 11 | 分かりにくい、つまずく、本文の結果と違って見える |
| C | 10 | 型の決まりからのずれ、小さな提案 |
| 抜け | 2 | 業務アプリを作るのに要るのに、扱っていないもの |

先に直したいのは次の5つです。

1. A-5：10-1 の `npm run typecheck` が、7-4 の「確かめよう」をした人では必ず失敗する
2. A-2：データベースを起動した直後に `psql` を打つとエラーになる（4-3、10-1）。4-3 ではボリュームが効いていないように見える
3. A-3：8-1 の「1行目を書き換える」でエラーが3つ出る（正しくは2行目）
4. A-4：8-2 の「何も設定しないと日本語が `\uXXXX` になる」は、今の ASP.NET Core では事実と違う
5. B-9：10-2 で、Docker の API が動いたままだと `dotnet run` が起動しない

## 部ごとの結果

| 部 | 打って確かめたか | 結果 |
| --- | --- | --- |
| 段階1（サイト） | ビルドとリンクを確かめた | 問題なし（C-1〜C-3） |
| 第0部 | 打てない（Windows の操作）。公式の説明と照らした | B-11（要確認） |
| 第1部 | 打った | A-1、B-1、B-2 |
| 第2部 | 2-1〜2-3 は打った。2-4、2-5 は原稿を読んだ | B-1、B-3、C-4 |
| 第3部 | 打った | B-4 |
| 第4部 | 打った | A-2、B-6、C-5 |
| 第5部 | 打った | B-5 |
| 第6部 | 打った | C-6 |
| 第7部 | 打った | B-7 |
| 第8部 | 打った | A-3、A-4 |
| 第9部 | 打った | 問題なし |
| 第10部 | 10-1 は打った。10-2 は GitHub への書き込みを除いて打った | A-2、A-5、B-8、B-9、B-10 |

## 進め方

- 段階1：ビルド、リンク、レッスンの型を、機械的に確かめる
- 段階2：本文と「確かめよう」のコマンドを、新しい Ubuntu で実際に打つ
- 段階3：部ごとに中身を読み、事実の誤り、古い書き方、つまずく所を探す
- 段階4：全体を通して、レッスン間のつながりと言葉の揺れを確かめる
- 段階5：業務アプリを作るのに要るのに、抜けているものを探す

付録（Claude Code）は対象外です。足すとよいものだけ、最後に挙げます。

根拠を確かめきれていないものには「要確認」と付けます。

## 確かめた環境

- 打って確かめた環境：Docker のコンテナの中の Ubuntu 24.04（`ubuntu-wsl` を入れて WSL の Ubuntu に近づけたもの）。ユーザー名は `yachiyo`
- 道具は本文の手順どおりに入れた。Docker は公式の apt の手順、Node.js は nvm、.NET は `apt install dotnet-sdk-10.0`
- systemd がないので、Docker は `dockerd` を手で起動した
- 打てないもの：Windows 側の操作（第0部）、VS Code とブラウザの画面の操作、GitHub への書き込み（2-4、2-5、10-2 の一部）。画面の操作は curl で代わりに確かめた
- VS Code で書いて保存する手順は、VS Code の既定（ファイルの最後に改行を付けない）に合わせて再現した

入ったバージョン（2026-10-27 時点）：

| 道具 | バージョン |
| --- | --- |
| Git | 2.43.0 |
| Python | 3.12.3 |
| Docker Engine / Compose | 29.9.2 / v5.6.1 |
| PostgreSQL | 17（`postgres:17`） |
| Node.js / npm | 24.22.1 / 11.19.1 |
| TypeScript（6-2 の `js1`） | 7.0.2 |
| React Router（`create-react-router@latest`） | 8.5.0（Vite 8、TypeScript 5.9.3） |
| Vitest | 5.0.5 |
| .NET SDK | 10.0.113 |
| Npgsql | 10.0.3 |
| xUnit（`dotnet new xunit`） | 2.9.3 |

---

## A　動かない、または事実と違う

### A-1 1-1 の「次のレッスン」が第2部を指している（対応済み）

- 場所：[01-command-line/terminal.md:192](src/content/docs/01-command-line/terminal.md#L192)
- 観点：つながり
- 内容：「次は Git です。今日作った `practice` フォルダを使って、ファイルの変更の履歴を残してみます。」とあるが、次のレッスンは 1-2（ファイルを扱う）
- 直し方の案：「次は、ファイルのコピー・移動・削除と、パスの書き方を覚えます。」のように 1-2 の内容にする
- 対応（2026-10-27）：案のとおり、1-2 の内容（コピー・移動・削除、パスの書き方）に直した

### A-2 データベースを起動した直後に `psql` を打つとエラーになる（対応済み）

- 場所：
  - [04-docker/volume.md:30-43](src/content/docs/04-docker/volume.md#L30-L43)、[04-docker/volume.md:87-89](src/content/docs/04-docker/volume.md#L87-L89)、[04-docker/volume.md:125-130](src/content/docs/04-docker/volume.md#L125-L130)
  - [10-final/business-app.md:88-92](src/content/docs/10-final/business-app.md#L88-L92)
- 観点：正しさ
- 内容：`docker compose up -d` は、コンテナを起動した時点で戻ってくる。データベースの準備には、新しいボリュームで初めて起動するときに約3秒かかる。そのあいだに `psql` を打つとエラーになる
  - 4-3 の「データが残ることを確かめる」は、`up -d` と `CREATE TABLE` と `INSERT` が1つのコードブロックに入っている。コピーのボタンで貼り付けると、`CREATE TABLE` と `INSERT` が失敗する。その後の `SELECT` で「表がない」と出るので、ボリュームが効いていないように見える。「確かめよう」も同じ理由で失敗する
  - 10-1 の `SELECT count(*)` も、起動の直後に打つと失敗する
  - 4-3 の note は、出るエラーを「could not connect to server」としている。これは古い PostgreSQL の文言で、PostgreSQL 17 では次の2種類の文が出る
- 根拠：コンテナで本文どおりに打った結果

  ```text
  psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: FATAL:  the database system is starting up
  ```

  ```text
  psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: No such file or directory
  	Is the server running locally and accepting connections on that socket?
  ```

  準備が終わるのを待ってから同じ手順を打つと、本文どおりにデータが残った（準備にかかった時間は、初回が約3秒、2回目からは約1秒）
- 直し方の案：
  - `docker compose up -d` と `psql` のコードブロックを分け、「`docker compose logs db` に `database system is ready to accept connections` が出るまで待つ」と書く
  - note のエラーの文を、上の2つに直す
  - 手間をかけるなら、compose.yaml に `healthcheck`（`pg_isready`）を足して `docker compose up -d --wait` を使う。ただし覚えることが増える
- 対応（2026-10-27）：
  - 4-3：最初の `up -d` の直後に「数秒待ってから次へ進む」と書いた。note をそこへ移し、エラーの文を PostgreSQL 17 の2種類に直した。「データが残ることを確かめる」のブロックは、`down`・`up -d` と `psql` に分け、あいだに「数秒待ってから」を入れた。「確かめよう」の1と3にも「数秒待ってから」を足した
  - 10-1：`up -d db` と `SELECT count(*)` を分けた。初回は `sample.sql` を流し込むので10秒ほど待つこと、エラーが出たら 4-3 を見ることを書いた
  - 案の「ログに `ready to accept connections` が出るまで待つ」は採らなかった。新しいボリュームで初めて動かすと、この行が2回出る（初期化のための一時的な起動と、本番の起動）。1回目で進むと失敗しうる
  - 5-2、5-3 の、`up -d` の直後に `psql` を打つブロックは直していない。既存のボリュームでは5回とも通った。失敗しても 4-3 の note で対処できる
  - 確かめ：4-3 を空のフォルダから新しい本文どおりに打ち、「確かめよう」まで本文どおりの結果になった。10-1 は新しいボリュームで10秒待って `6` が出た

### A-3 8-1 の「1行目を書き換える」と、エラーが3つ出る（対応済み）

- 場所：[08-csharp/csharp.md:78-90](src/content/docs/08-csharp/csharp.md#L78-L90)
- 観点：正しさ
- 内容：「`count` に文字列を入れてみます。1行目を次のように書き換えて」とあるが、1行目は `var name = "やちよ";` で、`int count = 1;` は2行目。本文どおり1行目を書き換えると、`count` が2回作られ、`name` もなくなるので、エラーが3つ出る
- 根拠：

  ```text
  Program.cs(1,13): error CS0029: Cannot implicitly convert type 'string' to 'int'
  Program.cs(2,5): error CS0128: A local variable or function named 'count' is already defined in this scope
  Program.cs(4,28): error CS0103: The name 'name' does not exist in the current context
  ```

  2行目を書き換えると、本文の意図どおり1つだけになる（位置は `(2,13)`）
- 直し方の案：「2行目を次のように書き換えて」にする。出力の例を `Program.cs(2,13)` に、説明を「`(2,13)` は2行目の13文字目」に直す
- 対応（2026-10-27）：案のとおり直した。どの行かが分かるように「2行目の `int count = 1;` を」と書き添えた

### A-4 8-2 の「何も設定しないと日本語が `\uXXXX` になる」は事実と違う（対応済み）

- 場所：[08-csharp/webapi.md:85-107](src/content/docs/08-csharp/webapi.md#L85-L107)（[08-csharp/database.md:95-115](src/content/docs/08-csharp/database.md#L95-L115) の `Program.cs` も同じ設定を引き継いでいる）
- 観点：正しさ
- 内容：
  - 「ASP.NET Core は何も設定しないと、JSON の中の日本語を `\u4F50\u85E4` のような記号の並びに置き換えて返します」とある。ASP.NET Core の MVC（コントローラー）は、エンコーダーを設定しないと `JavaScriptEncoder.UnsafeRelaxedJsonEscaping` を使うので、日本語はそのまま返る
  - 本文の設定 `JavaScriptEncoder.Create(UnicodeRanges.All)` は日本語をそのまま返すが、`<`、`>`、`&`、`'` はエスケープする。既定より厳しくなるだけで、日本語のために要る設定ではない
- 根拠：
  - 既定のままの `Program.cs`（ひな形）で `/api/employees` を呼ぶと、`[{"id":1,"name":"佐藤",…}]` と日本語のまま返った
  - 別に確かめた既定の出力：`{"name":"佐藤","lt":"<a>&'"}`
  - ASP.NET Core のソース：[SystemTextJsonOutputFormatter.cs](https://source.dot.net/Microsoft.AspNetCore.Mvc.Core/Formatters/SystemTextJsonOutputFormatter.cs.html) に「If the user hasn't explicitly configured the encoder, use the less strict encoder that does not encode all non-ASCII characters.」とある
- 直し方の案：
  - 「日本語をそのまま返す設定」の節を消す
  - `Program.cs` を書き換える理由は、「ひな形の `UseHttpsRedirection` と `UseAuthorization` を外して、短くする」とする（8-2 の「困ったとき」の https の警告とも合う）
  - 8-3 と 10-1 の `Program.cs` からも `AddJsonOptions` と2つの `using` を消す
- 対応（2026-10-27）：
  - 8-2：節を「Program.cs を短くする」に替えた。ひな形から、HTTPS に移す設定とログインを確かめる設定を外す、という理由で書き換え、残る3行の意味を書いた
  - 8-3：`AddJsonOptions` と2つの `using` を消した。本文の「増えたのは、`using Npgsql;` と、`connectionString` から始まる2行です」はそのまま合う
  - 10-1 には `Program.cs` が出てこないので、直すところはなかった
  - 確かめ：8-2 を新しいフォルダで作り直した。日本語がそのまま返ること、200・404・201・400 が本文どおりなこと、https の警告が出ないことを確かめた。8-3 の `Program.cs` は business-app の `api1` に入れ、手で動かしたときと Docker で動かしたときの両方で確かめた

### A-5 10-1 の `npm run typecheck` が、7-4 の「確かめよう」をした人では失敗する（対応済み）

- 場所：[10-final/business-app.md:254-262](src/content/docs/10-final/business-app.md#L254-L262)、[10-final/business-app.md:436-444](src/content/docs/10-final/business-app.md#L436-L444)
- 観点：つながり
- 内容：10-1 では `rm app/data/employees.server.ts` で、メモリの中のデータのファイルを消す。7-4 の「確かめよう」では `departments/:name` のページを作り、このファイルの `getEmployeesByDepartment` を使っている。10-1 にはこのページの扱いが書かれていないので、「つないで確かめる」の `npm run typecheck` が必ず失敗する。開発用のサーバーでも、このページを開くとエラーになる
- 根拠：7-3、7-4、9-3 の「確かめよう」の答えを入れた `rr1` で、本文どおりに打った結果

  ```text
  app/routes/department.tsx(3,42): error TS2307: Cannot find module '../data/employees.server' or its corresponding type declarations.
  ```

  このページを外すと、型の検査、テスト、画面のすべてが本文どおりに動いた
- 直し方の案：10-1 の `rm` の後に、「7-4 の『確かめよう』で作った部署のページは、`routes.ts` の行とファイルを消してください（または `api.server.ts` を使う形に直してください）」と書く。`routes.ts` の中身も、10-1 の時点のものを全部見せると確実
- 対応（2026-10-27）：
  - 10-1 の「登録のページ」の後に「部署ごとの一覧のページを外す」を足した。`routes.ts` から `departments/:name` の行を消すことと、ページのファイルを消すことを書いた
  - 案の「`routes.ts` の中身を全部見せる」は採らなかった。第7部の本文の `routes.ts` には `about` の行がなく、7-3 の「確かめよう」で足すだけになっている。全部を見せると、そこを飛ばした人では `about.tsx` が見つからなくなる。そのため、消す1行だけを見せた
  - 「困ったとき」に「Cannot find module '../data/employees.server'」の行を足した
  - 確かめ：7-4 のページを戻した `rr1` で TS2307 が出ること、本文どおりに外すと `npm run typecheck` と `npx vitest run` が通ることを確かめた

---

## B　分かりにくい、つまずく、本文の結果と違って見える

### B-1 VS Code の既定では最後に改行が付かず、本文の結果と違って見える

- 場所：
  - [01-command-line/terminal.md:140-146](src/content/docs/01-command-line/terminal.md#L140-L146)（`cat memo.txt`）
  - [02-git/commit.md:194-213](src/content/docs/02-git/commit.md#L194-L213)（`git diff`）
- 観点：正しさ
- 内容：VS Code は既定で、ファイルの最後に改行を付けずに保存する（`files.insertFinalNewline` が `false`）。このため次のようになる
  - 1-1：`cat memo.txt` の結果のすぐ後ろにプロンプトが続く（`こんにちはyachiyo@pc:~/practice$`）。この現象の説明は 3-3 まで出てこない
  - 2-1：`git diff` の結果が本文と違う。1行目の「牛乳を買う」も、消した行（`-`）と足した行（`+`）として出る。本文の「`+` で始まる行が足した行です。消した行には `-` が付きます」と合わせて読むと、1行目を消したように見える
- 根拠：コンテナで再現した `git diff` の結果

  ```text
  @@ -1 +1,2 @@
  -牛乳を買う
  \ No newline at end of file
  +牛乳を買う
  +本を返す
  \ No newline at end of file
  ```

  本文の `index 4d4d760..27f841e` は、最後に改行がある場合の値。改行がない場合は `index 3d27819..1e50f48` になる
- 直し方の案：0-2 で VS Code の設定「Files: Insert Final Newline」を有効にする手順を足す。これで 1-1 と 2-1 の両方が本文どおりになる。足さない場合は、2-1 の note を「1行目にも `-` と `+` が付くことがある」まで広げる

### B-2（要確認）WSL につないだ VS Code で消したファイルは、ごみ箱に入らない可能性がある

- 場所：[01-command-line/terminal.md:186-188](src/content/docs/01-command-line/terminal.md#L186-L188)
- 観点：正しさ
- 内容：「`rm` は元に戻せません。それまでは、要らないファイルは VS Code の画面から消してください」とある。この書き方だと、VS Code から消せば戻せるように読める。WSL につないだ VS Code では、ファイルは Ubuntu の中にあるので、Windows のごみ箱には入らず、完全に消える可能性がある
- 根拠：公式の説明は見つからなかった。実際の VS Code で、消すときの確認の画面の文言を見る必要がある
- 直し方の案：確かめたうえで、「VS Code から消すときも、確認の画面で『完全に削除』と出たら戻せません」のように書く

### B-3 2-3 の `git merge --abort` を本文の流れで打つとエラーになる

- 場所：[02-git/conflict.md:176-184](src/content/docs/02-git/conflict.md#L176-L184)
- 観点：正しさ
- 内容：合流を終えた後に、打つコマンドの形で `git merge --abort` が出てくる。本文どおりに打つと、合流の途中ではないので次のエラーになる。index.md の決まり「打つものと出てくる結果を、必ず対にして見せる」にも合っていない

  ```text
  fatal: There is no merge to abort (MERGE_HEAD missing).
  ```

- 直し方の案：「コンフリクトが起きている途中でだけ使えます。今は打たなくてかまいません」と書き添える。または「確かめよう」に、わざとコンフリクトを起こしてから取りやめる手順を入れる

### B-4 3-4 の「サーバーが状態を覚える作り」の説明が一面的

- 場所：[03-web/cookie.md:276-286](src/content/docs/03-web/cookie.md#L276-L286)、[03-web/cookie.md:298-300](src/content/docs/03-web/cookie.md#L298-L300)
- 観点：正しさ
- 内容：
  - 表では、サーバーが状態を覚える作り（セッション）について、「再起動すると全員がログアウトする」「2台に増やすとうまく動かない」と書いている。これは、状態をサーバーのメモリに置いた場合だけの話。実務では、セッションをデータベースや Redis に置くのがふつうで、その場合は再起動しても台数を増やしても動く。業務アプリでは、セッションを使う作りも多い
  - caution では、署名付きの Cookie の「代表的なものが JWT」と書いている。JWT は API を呼ぶときに `Authorization` ヘッダーで送る使い方が中心。ASP.NET Core で Cookie にログインの状態を持たせる場合は、ASP.NET Core が暗号化した Cookie（Cookie 認証）を使うのがふつう
- 直し方の案：表の「サーバーが覚える作り」の列に「（メモリに置いた場合）」と書き添え、「データベースなどに置けば、この問題は避けられる」と1文足す。caution は「署名や暗号化を付ける。ASP.NET Core の Cookie 認証や JWT が、その例です」のようにする

### B-5 5-1 の `\dt` に、4-3 で作った `memo` の表も出る

- 場所：[05-database/select.md:94-107](src/content/docs/05-database/select.md#L94-L107)
- 観点：つながり
- 内容：4-3 の「確かめよう」で「データは次の部で使うので、`-v` は付けないでください」としているので、`memo` の表が残っている。`\dt` の結果は本文の2行ではなく、`memo` を含む3行になる
- 直し方の案：本文の結果に `memo` の行を足し、「4-3 で作った `memo` も並びます」と書く

### B-6 4-3 の `docker volume ls` に、名前のないボリュームがいくつも並ぶ

- 場所：[04-docker/volume.md:64-85](src/content/docs/04-docker/volume.md#L64-L85)、[04-docker/volume.md:149-155](src/content/docs/04-docker/volume.md#L149-L155)
- 観点：正しさ
- 内容：`postgres` のイメージは、データの置き場所に名前のないボリュームを自動で作る。このため、4-2 と 4-3 で `down` と `up` をするたびに、長い英数字の名前のボリュームが増える。`docker volume ls` には、`compose1_db-data` のほかにこれらも並ぶ（コンテナでは3つ並んだ）。「表もデータも、消したコンテナと一緒に消えています」も正確ではない。古いデータは名前のないボリュームに残り、新しいコンテナが新しい空の置き場所を使うので、見えなくなっている
- 直し方の案：`docker volume ls` の説明に、「長い英数字の名前のものは、名前を付けずに使っていた置き場所の残りです。今は気にしなくてかまいません」と足す

### B-7 7-2 の「確かめよう」の結果が、7-1 で足した田中さんを残すと変わる

- 場所：[07-react/state.md:217-219](src/content/docs/07-react/state.md#L217-L219)、[07-react/state.md:344-350](src/content/docs/07-react/state.md#L344-L350)
- 観点：つながり
- 内容：7-1 の「確かめよう」で田中さん（営業部）を足している。7-2 の「足した人は残したままでかまいません」は、「入社年を足した人」とも「足した田中さん」とも読める。田中さんを残すと、「営業部を選ぶと鈴木さんだけになり『1人表示中』」が「2人表示中」になる
- 直し方の案：「この先の例は、7-1 の『確かめよう』で足した田中さんと入社年を省いて、3人で書いています」とはっきり書く。または「確かめよう」の結果を、田中さんがいる場合といない場合の両方で書く

### B-8 10-1 の API のログに `Error:` の行が出る

- 場所：[10-final/business-app.md:549-554](src/content/docs/10-final/business-app.md#L549-L554)
- 観点：つまずき
- 内容：Docker で動かした API のログに、次の行が出る。動きには影響しないが、「困ったとき」で `docker compose logs api` を見るよう案内しているので、受講者が原因と取り違えやすい

  ```text
  api-1  | Error: libgssapi_krb5.so.2: cannot open shared object file: No such file or directory
  ```

  Npgsql が GSS の暗号化を試そうとして、`aspnet` のイメージにないライブラリを読みにいくために出る（要確認：原因の説明は Npgsql の既定の動きからの推測）
- 直し方の案：「困ったとき」に「この行は気にしなくてかまいません」と足す。または接続文字列に `Gss Encryption Mode=Disable` を足す

### B-9 10-2 で、Docker の API が動いたままだと `dotnet run` が起動しない（対応済み）

- 場所：[10-final/pull-request.md:122-129](src/content/docs/10-final/pull-request.md#L122-L129)
- 観点：つながり
- 内容：10-1 の「確かめよう」の最後は、3つのコンテナが動いた状態で終わる。10-2 の「手で動かして、curl で確かめます」では、Docker の `api` が 5080 番を使っているので、`dotnet run --urls http://localhost:5080` が起動しない。そのまま curl で PUT を送ると、Docker の古い API に届いて `405` が返る
- 根拠：

  ```text
  System.IO.IOException: Failed to bind to address http://127.0.0.1:5080: address already in use.
  ```

  `docker compose stop api web` で止めると、PUT は本文どおり `200` と `404` を返した
- 直し方の案：「1. ブランチを作る」の前に、「Docker の画面と API を止めて、データベースだけを動かしておきます」として、`docker compose stop api web`（または `docker compose down` の後に `docker compose up -d db`）を書く
- 対応（2026-10-27）：
  - 案のとおり、「1. ブランチを作る」の前に「手で動かす準備」の節を足した。コマンドは、本文にまだ出てこない `docker compose stop` ではなく、4-3 と 10-1 で使った `docker compose down` と `docker compose up -d db` にした
  - 「6. 合流させる」の `docker compose up -d --build` の前に、手で動かしている API と画面を Ctrl+C で止めることを足した
  - 確かめ：3つのコンテナが動いた状態から、新しい本文どおりに打った。手で動かした API で、PUT が `200` と `404` を返した。その後 `docker compose up -d --build` で3つが動き、Docker の API でも PUT が `200` を返した

### B-10 10-2 で、パスワードの入ったファイルを GitHub に送る

- 場所：[10-final/pull-request.md:54-67](src/content/docs/10-final/pull-request.md#L54-L67)、[10-final/pull-request.md:207-216](src/content/docs/10-final/pull-request.md#L207-L216)
- 観点：つながり
- 内容：
  - `git add .` で、`api1/appsettings.json` と `compose.yaml`（どちらも `Password=secret` を含む）が記録される
  - 「5. 出す前に、自分で見直す」では「パスワードなどの、人に見せてはいけない情報が入っていない」ことを確かめさせるので、受講者は練習用のパスワードをどう扱えばよいか迷う
  - 2-4 では公開範囲を「Private」と指定しているが、10-2 の `business-app` のリポジトリでは指定していない。8-3 の caution（「本物のアプリではパスワードを Git に入れない」）とも食い違う
- 直し方の案：リポジトリを作る手順に「Private を選ぶ」と書く。「5. 見直す」に「`secret` は練習用のパスワードなので、この教材ではそのままにします。本物のアプリでは入れません」と書き添える

### B-11（要確認）0-1 の、ユーザー名を聞く画面の文言

- 場所：[00-setup/wsl2.md:51-55](src/content/docs/00-setup/wsl2.md#L51-L55)
- 観点：正しさ
- 内容：本文は `Enter new UNIX username:` と出るとしている。新しい形式の Ubuntu の WSL 版では、`Create a default Unix user account:` と出るという例がある。どちらが出るかは、今の Windows で `wsl --install` を打って確かめる必要がある。Microsoft の説明（[Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install)）とは、前提の Windows のバージョン、再起動が要ること、既定で Ubuntu が入ることが一致した
- 直し方の案：確かめたうえで文言を合わせる。または「ユーザー名を聞かれます（表示の文は版によって少し違います）」と書く

---

## C　型の決まりからのずれ、小さな提案

### C-1 10-2 に「困ったとき」がない

- 場所：[10-final/pull-request.md](src/content/docs/10-final/pull-request.md)
- 観点：型
- 内容：レッスンの型の5「困ったとき」の見出しがない。他のレッスンにはすべてある
- 直し方の案：B-9 のポートのぶつかりや、プッシュやプルリクエストでよく出るエラー（2-4、2-5 と同じもの）への案内を足す。または、型の例外として index.md に書く

### C-2 「元に戻せない操作」ではない所に danger を使っている

- 場所：[02-git/github.md:87](src/content/docs/02-git/github.md#L87)（秘密鍵を見せない）、[08-csharp/database.md:228](src/content/docs/08-csharp/database.md#L228)（パラメーターで渡す）
- 観点：型
- 内容：index.md では、danger は「元に戻せない操作。この種類は本当に戻せないときだけ使う」と決めている。この2か所は操作ではなく、安全のための決まり
- 直し方の案：caution にする。または、index.md の決まりに「安全に関わる決まり」も足す

### C-3 ファビコンがない

- 場所：サイト全体（`public/favicon.svg` がない）
- 観点：サイト
- 内容：すべてのページが `/yachiyo-dev-school/favicon.svg` を読みにいくが、ファイルがないので 404 になる。ブラウザのタブのアイコンが出ないだけで、本文には影響しない。ほかに、ビルドの警告が1つ出る（`The collection "i18n" does not exist or is empty`）。表示には影響しない
- 直し方の案：`public/favicon.svg` を置く

### C-4 コミットの番号の例が、レッスンごとに違う

- 場所：[02-git/commit.md](src/content/docs/02-git/commit.md)（`1a8cbd0`、`9159aa5`）、[02-git/branch.md](src/content/docs/02-git/branch.md)（`d2e4a7c`、`da25ccd`）
- 観点：つながり
- 内容：同じコミットを指しているのに、2-1 と 2-2 で番号の例が違う。「人によって違う」と書いてあるので、誤りではない
- 直し方の案：そろえるなら 2-1 の番号に合わせる。そろえなくてもよい

### C-5 4-1 の `docker ps` の PORTS の例が、今の表示と少し違う

- 場所：[04-docker/run.md:109-112](src/content/docs/04-docker/run.md#L109-L112)
- 観点：正しさ
- 内容：今の Docker では、IPv6 の分も並ぶ（`0.0.0.0:8080->80/tcp, [::]:8080->80/tcp`）
- 直し方の案：例を今の表示に合わせる

### C-6 6-3 でサーバーを止めたときのエラーの形が、本文の例と違う

- 場所：[06-typescript/async.md:296-303](src/content/docs/06-typescript/async.md#L296-L303)
- 観点：正しさ
- 内容：Node.js 24 では、`localhost` を IPv6 と IPv4 の両方で試すので、`[cause]: AggregateError [ECONNREFUSED]` の中に `connect ECONNREFUSED ::1:8000` と `connect ECONNREFUSED 127.0.0.1:8000` が並ぶ。本文の「このような行が出て」の範囲なので、読み取れる
- 直し方の案：例を今の形に合わせるか、「`ECONNREFUSED` という文字を探してください」と書く

### C-7 第5部の題が「テーブル」、本文が「表」

- 場所：[05-database/join.md:2](src/content/docs/05-database/join.md#L2)、[index.md:72](src/content/docs/index.md#L72)
- 観点：言葉の揺れ
- 内容：5-3 の題と目次は「テーブル」、本文は第5部から第10部まで「表」（53か所）
- 直し方の案：題を「表をつなぐ」にする。または初出で「表（テーブル）」と書く

### C-8 10-1 で `rm -rf` の `-f` を説明していない

- 場所：[10-final/business-app.md:47-50](src/content/docs/10-final/business-app.md#L47-L50)
- 観点：つながり
- 内容：1-2 では `rm -r` と「消す前に `ls` で確かめる」順番を教えている。10-1 では、説明のない `-f` を付けて、6つの場所をまとめて消す
- 直し方の案：「`-f` は、ないものがあっても止めずに進める指定です」と足し、打つ前に `pwd` で `business-app` にいることを確かめるよう書く

### C-9 「必要になったレッスンで扱います」としたのに、扱っていないもの

- 場所：[02-git/commit.md:279-284](src/content/docs/02-git/commit.md#L279-L284)、[01-command-line/files.md:395-401](src/content/docs/01-command-line/files.md#L395-L401)
- 観点：つながり
- 内容：
  - 2-1 では「コミットした後に、そのコミットを取り消す方法」を「必要になったレッスンで扱います」としているが、どのレッスンでも扱っていない（[next-steps.md](src/content/docs/next-steps.md) は「後回しにした」としている）
  - 1-2 の `*` とファイルの権限も、後のレッスンでは出てこない
- 直し方の案：「この教材では扱いません」または「さらに学ぶで紹介します」に直す

### C-10 動作を確かめたバージョンを書いておく

- 場所：[README.md](README.md)、または [index.md](src/content/docs/index.md)
- 観点：提案
- 内容：今回、React Router は v8、TypeScript は 7、Vitest は 5 が入った。本文はどれでもそのまま動いたが、将来は合わなくなることがある。どのバージョンで確かめたかが書いてあれば、受講者が「書いてあるとおりに動かない」ときに、原因の見当をつけやすい
- 直し方の案：README の「誤りを見つけたら」の近くに、上の「確かめた環境」の表を置く

---

## 抜け　業務アプリを作るのに要るのに、扱っていないもの

「業務アプリを作るのに要るもの」に絞って挙げます。

### G-1 自分のアプリの表を作る（`CREATE TABLE` と、番号の自動の振り方）

- 場所：第5部（[05-database/select.md:261-264](src/content/docs/05-database/select.md#L261-L264) で「表の作り方の細かい書き方」を後回しにしている）、[08-csharp/database.md:272-274](src/content/docs/08-csharp/database.md#L272-L274)
- 内容：
  - 表はいつも `sample.sql` で用意されているので、受講者は自分で表を作ったことがないまま終わる。最後の目標は「小さな業務アプリを自分で作れるようになる」なので、扱う表を自分で決めて作る手順が要る
  - 8-3 では「本物のアプリではデータベースに自動で番号を振らせる仕組みを使います」と書いているが、その仕組み（`GENERATED ALWAYS AS IDENTITY`）はどこにも出てこない
- 直し方の案：5-2 か 10-1 に、`CREATE TABLE` と `id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY` の書き方を足す。`sample.sql` を自動の番号にすれば、8-3 と 10-1 の `MAX(id) + 1` もなくせる

### G-2 VS Code の C# の拡張機能

- 場所：[00-setup/vscode.md:186-188](src/content/docs/00-setup/vscode.md#L186-L188)、第8部
- 内容：0-2 では「必要なものは使うレッスンでそのつど紹介します」としているが、WSL 以外の拡張機能はどのレッスンにも出てこない。TypeScript は VS Code が最初から対応しているので、第6部と第7部では赤い波線が出る。C# は拡張機能を入れないと、入力の補いもエラーの波線も出ないので、第8部と第9部は手がかりのない状態で書くことになる
- 直し方の案：8-1 の「.NET を入れる」の後に、Microsoft の「C#」の拡張機能を入れる手順を足す。「C# Dev Kit」は会社の規模によって有料のライセンスが要る（要確認）ので、4-1 の Docker Desktop と同じように一言添える

---

## 付録に足すとよいもの（検討用）

付録はチェックの対象から外したので、中身は読んでいません。扱っている話題を検索で確かめた範囲での提案です。

- **`/rewind`（Claude の変更を巻き戻す）**：付録の「安全に使う」では、思っていない所まで直されたときの戻し方として `git restore` を挙げている。Claude Code にはコミットの前の変更も会話ごと巻き戻せる `/rewind`（Esc キーを2回）があり、初心者には安心材料になる。plan のモードはすでに扱っている

---

## 人にしかできない確かめ

今回の方法では確かめられなかったものです。

- 新しい Windows で、第0部を通す（B-11 の文言、再起動の要否）
- WSL につないだ VS Code で、ファイルを消したときの確認の画面を見る（B-2）
- GitHub の画面の操作（2-4、2-5、10-2）。原稿を読んだ範囲では、ボタンの名前などに古いものは見つからなかった
- 「かかる時間の目安」が合っているか。対象の人（Git を使ったことがない業務アプリの開発者）に、どこか1部を試してもらうのがよい
