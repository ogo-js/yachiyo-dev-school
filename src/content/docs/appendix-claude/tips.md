---
title: 使いこなしのヒント
description: プルリクエストのレビュー、公式の説明の読ませ方など、慣れてきたら試したい頼み方
sidebar:
  order: 7
---

付録のレッスンを終えて、Claude Code に慣れてきたら試したい頼み方を集めました。どれも、必要になったときに読めば十分です。

## プルリクエストをレビューさせる

GitHub のプルリクエストを読ませて、レビューさせられます。先に、GitHub をコマンドで扱う道具（GitHub CLI）を入れて、ログインしておきます。

```bash
sudo apt install gh
gh auth login
```

あとはプルリクエストの URL を渡して頼みます。

```text
https://github.com/yachiyo/business-app/pull/1 これをレビューして。
指摘はサブエージェントに検証させて、確かな指摘だけを残して。
```

出てきた指摘はそのままプルリクエストに貼りません。自分で読んで、本当に直すべきものを選び、自分の言葉でコメントします（レッスン2-5）。レビューの責任を持つのは、自分です。

## 公式の説明を読ませてから答えさせる

AI は、ない書き方をあるかのように答えることがあります（付録の「安全に使う」）。新しい道具や、バージョンで書き方が変わるものを聞くときは、公式の説明のページを読ませてから答えさせます。

```text
React Router の公式の説明を読んでから、loader でエラーを返す書き方を教えて。
読んだページの URL も書いて。
```

読んだページの URL を書かせておくと、自分でも開いて確かめられます。

## 先に質問させる

頼みたいことがまだはっきりしていないときは、作業を始める前に質問させます。

```text
社員の一覧に絞り込みの機能を足したい。始める前に、決めておくべきことを質問して。
```

AI が勝手に決めて進めるのを防げますし、自分でも何を決めていなかったのかに気づけます。

## 図にして説明させる

仕組みが分かりにくいときは、図にさせると理解が早くなります。図を文字で書ける書き方（Mermaid）を指定すると、そのまま Markdown のファイルに貼れます。

```text
画面から API、データベースまで、社員を登録するときの流れを Mermaid の図にして。
```

## 外の道具につなぐ

MCP という仕組みを使うと、Claude Code をデータベースや課題の管理の道具などにつなげられます。たとえば、データベースにつなぐと、表の中身を見ながら SQL を考えさせられます。

ただし、つないだ先のデータは AI のサービスに送られます。仕事で使うときは、つないでよいか、組織の決まりを必ず確かめてください（付録の「安全に使う」）。使い方は公式の説明の「Connect Claude Code to tools via MCP」を見てください。

## 返事が終わったら Windows の通知を出す

この節は、やりたい人だけが試せば十分です。

時間のかかる作業を頼むと、終わるまで別のことをしたくなります。拡張機能では、Claude のタブを見ていないあいだに返事が終わると、Claude のマークにオレンジの点が付きます。それでも、VS Code の画面そのものを見ていなければ気づけません。そこで、返事が終わるたびに Windows の通知を出すようにします。

使うのは、決まった時に自動でコマンドを動かす、フック（hooks）という仕組みです。付録の「安全に使う」で「今は知らなくてよいこと」に入れたものです。フックに登録したコマンドは、確かめなしに毎回動きます。何をするか分かっているものだけを登録します。

:::caution[会社の PC で使うとき]
このやり方は、Ubuntu から Windows の PowerShell を呼んで通知を出します。会社の PC では、PowerShell の使い方が制限されていたり、セキュリティソフトが止めたりして、動かないことがあります。動かないときは無理に使わず、下の「元に戻す」のとおりに消してください。使ってよいか分からないときは、組織の決まりを確かめてください。
:::

### 通知を出すスクリプトを置く

Claude Code の設定のフォルダ（`~/.claude`）の中に、スクリプトを置くフォルダを作り、ファイルを開きます。

```bash
mkdir -p ~/.claude/hooks
code ~/.claude/hooks/notify-windows.sh
```

開いたファイルに次の内容を貼り付けて、保存します。5行目はとても長いですが、途中で改行せず、1行のまま貼ります。枠の右上のボタンを押すと、まとめてコピーできます。

```bash
#!/bin/bash
# Claude Code の Stop フックから呼び、Windows の通知を出す
cat >/dev/null
ps=$(cat <<'EOF'
$t = [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02); $n = $t.GetElementsByTagName('text'); $n.Item(0).AppendChild($t.CreateTextNode('Claude Code')) | Out-Null; $n.Item(1).AppendChild($t.CreateTextNode('返事が届きました')) | Out-Null; [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe').Show([Windows.UI.Notifications.ToastNotification]::new($t))
EOF
)
cd /mnt/c && powershell.exe -NoProfile -NonInteractive -Command "$ps" >/dev/null 2>&1
exit 0
```

- `cat >/dev/null`：Claude Code が渡してくる情報を読んで、使わずに捨てる
- `ps=$(...)` の所：Windows の通知を出す PowerShell の命令。「Claude Code」と「返事が届きました」の2行の通知を作る
- `cd /mnt/c && powershell.exe ...`：Windows の C ドライブに移ってから、Windows の PowerShell にこの命令を渡して動かす
- `exit 0`：通知に失敗しても、成功として終わる。失敗がエラーとして Claude Code に伝わらないようにしている

保存したら、このファイルを命令として動かせるようにします。`chmod +x` は、ファイルに「動かしてよい」という印を付ける指定です。

```bash
chmod +x ~/.claude/hooks/notify-windows.sh
```

フックに登録する前に、手で動かして通知が出るか確かめます。

```bash
~/.claude/hooks/notify-windows.sh < /dev/null
```

画面の右下に「Claude Code」「返事が届きました」という通知が出れば、動いています。通知の送り主には Windows PowerShell の名前が出ます。PowerShell の名前を借りて通知を出しているためです。

`/dev/null` は、中身が空の特別なファイルです。このスクリプトは最初に Claude Code からの情報を読もうとするので、手で動かすときは `<`（レッスン5-1）で空の入力を渡します。付け忘れると、入力を待ったまま止まります。そのときは Ctrl+C で止めて、打ち直してください。

:::tip[中身を説明させる]
スクリプトの中身が気になったら、Claude Code に説明させます。

```text
~/.claude/hooks/notify-windows.sh が何をしているか、1行ずつ説明して。
```
:::

### フックに登録する

`~/.claude/settings.json` を開きます。

```bash
code ~/.claude/settings.json
```

一番外側の `{` のすぐ下に、次の行を足して保存します。

```json
  "hooks": {
    "Stop": [
      { "hooks": [ { "type": "command", "command": "$HOME/.claude/hooks/notify-windows.sh", "async": true } ] }
    ]
  },
```

- `Stop`：Claude が返事を終えたときに動かす
- `command`：動かすコマンド。`$HOME` は自分のホームフォルダ（`~` と同じ場所）を表す
- `async`：`true` にすると、通知が出るのを待たずに返事を終える。PowerShell が立ち上がるまでに少し時間がかかるため

ファイルがなかったときや、中身が `{}` だけのときは、ファイル全体を次の内容にします。後ろにほかの設定が続かないので、`"hooks"` の欄の最後の `}` にはカンマを付けません。

```json
{
  "hooks": {
    "Stop": [
      { "hooks": [ { "type": "command", "command": "$HOME/.claude/hooks/notify-windows.sh", "async": true } ] }
    ]
  }
}
```

settings.json は JSON なので、カンマや引用符を1つ間違えると、設定のエラーが出ます。そのときは足した行を見直してください。保存した内容は、ふつうは動いている Claude Code にそのまま読み込まれます。

### 確かめる

Claude Code に、何か短いことを頼みます。

```text
こんにちは、とだけ返して
```

返事が終わって少しすると、手で動かしたときと同じ通知が出ます。通知は返事のたびに出るので、画面を見ているときにも出ます。返事の途中で、許可を求めて止まったときには出ません。

### 困ったとき

- **手で動かしても通知が出ない**：Windows の設定の「システム」→「通知」で、通知が止められていないか（応答不可や集中モードになっていないか）を確かめてください。それでも出ないときは、会社の PC の制限かもしれません。無理に使わず、元に戻してください。
- **手で動かすと出るのに、返事が終わっても出ない**：settings.json の書き間違いか、パスの違いが考えられます。拡張機能では、`/hooks` と打つと開く画面の Stop の欄に、このフックが出ているかを確かめられます。足した行を見直してから、Claude Code を起動し直してください。拡張機能で使っているときは、VS Code を閉じて開き直します。

### 元に戻す

settings.json から、足した `"hooks"` の欄を消して保存します。拡張機能で使っているときは、`/hooks` と打つと開く画面で、Stop の欄にあるこのフックを選び、「Remove」を押しても消せます。

スクリプトも要らなければ、消します。

```bash
rm ~/.claude/hooks/notify-windows.sh
```

:::tip[しばらく止めたいとき]
消さずに止めたいときは、settings.json の一番外側の `{` のすぐ下に、次の行を足します。登録したフックがすべて止まります。また動かすときは、この行を消します。

```json
  "disableAllHooks": true,
```
:::
