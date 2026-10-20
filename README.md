# yachiyo-dev-school

Git や Docker のコマンドを打ったことがない人が、今の Web 開発の道具と技術を一から身につけるための教材です。

最後に、次の構成の小さな業務アプリを自分で作れるようになることを目指します。

- 画面：TypeScript、React、React Router
- API：C#、ASP.NET Core
- データベース：PostgreSQL
- 動かす環境：Docker

## サイトとして読む

教材は Astro Starlight のサイトとして読めます。Node.js が入っている環境で、次のように打ちます。

```bash
npm install
npm run dev
```

ブラウザで `http://localhost:4321` を開くと、目次が表示されます。

## フォルダの構成

```text
.
├── README.md
├── astro.config.mjs        … サイトの設定（タイトル、左のメニュー）
├── package.json
├── files/                  … レッスンで使う練習用のファイル
│   ├── webdemo.py          … 第3部の練習用のサーバー
│   └── sample.sql          … 第5部の練習用のデータ
└── src/content/docs/       … レッスン
    ├── index.md            … 目次
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
