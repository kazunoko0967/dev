# 08 Hooks

Claude CodeのHooks機能を体験する。
ツール実行前後に自動でシェルコマンドを実行できる。

## 設定場所

`.claude/settings.json`（プロジェクト共有）または `~/.claude/settings.json`（個人）

## サンプル設定

`hooks_example.json` を参考に `.claude/settings.json` に追記する。

## お題

1. **ファイル保存後に自動lint**: Editツール実行後にflake8を走らせる
2. **コマンド実行のログ**: Bashツール実行前にコマンドをログに記録
3. **危険コマンドのブロック**: `rm -rf` を含むコマンドをブロック

## Hookのイベント種類

| イベント | タイミング |
|---|---|
| `PreToolUse` | ツール実行前 |
| `PostToolUse` | ツール実行後 |
| `Notification` | 通知発生時 |
| `Stop` | エージェント停止時 |
