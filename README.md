# yachiyo-dev-school

Git や Docker のコマンドを打ったことがない人が、今の Web 開発の道具と技術を一から身につけるための教材です。

公開しているサイト：https://ogo-js.github.io/yachiyo-dev-school/

最後に、次の構成の小さな業務アプリを自分で作れるようになることを目指します。

- 画面：TypeScript、React、React Router
- API：C#、ASP.NET Core
- データベース：PostgreSQL
- 動かす環境：Docker

## 誤りを見つけたら

誤字や、書いてあるとおりに動かない所を見つけたら、次のどちらかの方法で知らせてください。

### Issue で知らせる

直し方が分からないときや、まず相談したいときは、Issue を作ってください。

1. このリポジトリの「Issues」タブを開き、「New issue」を押す
2. 次のことを書いて、「Create」を押す
   - どのレッスンか（例：2-3 合流でぶつかったときに直す）
   - どこが、どう違うか
   - 動かないときは、打ったコマンドと、出たエラーの文

### プルリクエストで直し方を出す

直し方が分かっているときは、プルリクエストを出してください。教材の第2部で学んだ流れと同じです。

**誤字など、小さな直しのとき（GitHub の画面だけでできる）**

1. 直したいレッスンのファイルを、GitHub の画面で開く（`src/content/docs/` の下にあります）
2. 右上の鉛筆の形のボタンを押す。自分のアカウントにリポジトリの複製（フォーク）が自動で作られる
3. 直して、「Commit changes」を押す
4. 続けて出てくる画面で「Create pull request」を押す。説明の欄に、何をなぜ直したかを書く

**いくつかのファイルにまたがる直しのとき（手元で直す）**

1. GitHub の画面の右上の「Fork」を押して、自分のアカウントにリポジトリの複製を作る
2. 複製したリポジトリを手元にクローンし、ブランチを作る

   ```bash
   git clone git@github.com:自分のユーザー名/yachiyo-dev-school.git
   cd yachiyo-dev-school
   git switch -c fix-lesson-2-3
   ```

3. `src/content/docs/` の下のファイルを直し、サイトの見た目で確かめる（下の「手元でサイトとして読む」を見てください）
4. コミットして、自分の複製に送る

   ```bash
   git add .
   git commit -m "2-3 の手順の誤りを直す"
   git push -u origin fix-lesson-2-3
   ```

5. 自分の複製のリポジトリの画面で「Compare & pull request」を押し、このリポジトリの `main` に向けてプルリクエストを出す

プルリクエストの説明には次のことを書いてください。

- 何を直したか
- なぜ直したか（どこが誤っていたか）
- どう確かめたか（手元のサイトで表示を見た、書いてあるコマンドを打って結果を見た、など）

## 手元でサイトとして読む

Node.js が入っている環境で、次のように打ちます。

```bash
npm install
npm run dev
```

ブラウザで `http://localhost:4321/yachiyo-dev-school/` を開くと、目次が表示されます。

## 公開のしかた

`main` に push すると、GitHub Actions（`.github/workflows/deploy.yml`）がサイトを組み立てて、GitHub Pages に公開します。

## フォルダの構成

```text
.
├── README.md
├── astro.config.mjs        … サイトの設定（タイトル、公開する場所、左のメニュー）
├── package.json
├── .github/workflows/      … GitHub Pages に公開する設定
├── files/                  … レッスンで使う練習用のファイル
│   ├── webdemo.py          … 第3部の練習用のサーバー
│   └── sample.sql          … 第5部の練習用のデータ
└── src/content/docs/       … レッスン
    ├── index.md            … 目次
    ├── next-steps.md       … さらに学ぶ
    ├── 00-setup/           … 第0部 準備
    ├── 01-command-line/    … 第1部 コマンドライン
    ├── 02-git/             … 第2部 Git と GitHub
    ├── 03-web/             … 第3部 Web の仕組み
    ├── 04-docker/          … 第4部 Docker
    ├── 05-database/        … 第5部 データベース
    ├── 06-typescript/      … 第6部 TypeScript
    ├── 07-react/           … 第7部 React と React Router
    ├── 08-csharp/          … 第8部 C# と ASP.NET Core
    ├── 09-test/            … 第9部 テスト
    └── 10-final/           … 第10部 総仕上げ
```

レッスンを足すときは、部のフォルダに Markdown のファイルを置き、先頭の `sidebar.order` で並び順を決めます。
