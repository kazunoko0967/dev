# 10 MCP Servers

Claude CodeのMCP（Model Context Protocol）サーバー機能を体験する。
外部ツールやサービスをClaude Codeに接続できる。

## 設定方法

```bash
# MCPサーバーを追加（例: filesystem）
claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem /path/to/dir

# 設定確認
claude mcp list
```

または `~/.claude/settings.json` に直接記述。

## お題

1. **設定確認**: 「現在設定されているMCPサーバーを確認して」
2. **filesystemサーバー**: ローカルファイルシステムへのアクセスを拡張
3. **カスタムMCP**: `mcp_example.json` を参考に独自サーバーを設定

## 主なMCPサーバー例

| サーバー | 用途 |
|---|---|
| `@modelcontextprotocol/server-filesystem` | ファイルシステム操作 |
| `@modelcontextprotocol/server-github` | GitHub API |
| `@modelcontextprotocol/server-postgres` | PostgreSQL操作 |
| `@modelcontextprotocol/server-slack` | Slack連携 |

## 特徴

- MCPサーバーはClaude Codeのツールセットを拡張する
- プロジェクト固有・ユーザー共通の2種類のスコープで設定可能
