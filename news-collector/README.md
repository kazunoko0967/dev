# 世界ビジネス・経済ニュース自動収集システム

## 概要
株探・Bloomberg・The Guardian・BBC Businessからニュースを自動収集し、
Claude Haiku 4.5で日本語要約してHTMLレポートをブラウザ表示するシステム。

## セットアップ

### 1. 依存パッケージのインストール
```bash
cd news-collector
pip install -r requirements.txt
```

### 2. 環境変数の設定
```bash
export ANTHROPIC_API_KEY="your-api-key-here"

# メール通知設定（SendGrid）
export RESEND_API_KEY="re_xxxxxxxxxxxxxxxx"      # Resend APIキー
export RESEND_FROM_EMAIL="your@email.com"         # 送信元（Resendで認証済みのアドレス）
export NOTIFY_EMAIL="recipient@example.com"       # 送信先メールアドレス
```

永続化する場合は `~/.zshrc` に追記:
```bash
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.zshrc
echo 'export RESEND_API_KEY="re_xxxxxxxxxxxxxxxx"' >> ~/.zshrc
echo 'export RESEND_FROM_EMAIL="your@email.com"' >> ~/.zshrc
echo 'export NOTIFY_EMAIL="recipient@example.com"' >> ~/.zshrc
source ~/.zshrc
```

#### Resend APIキーの取得方法
1. [resend.com](https://resend.com/) にアカウント登録（無料・100通/日）
2. API Keys → Create API Key
3. 生成されたキーを `RESEND_API_KEY` に設定
4. Domains → 送信元ドメインを認証（独自ドメインがない場合は `onboarding@resend.dev` が利用可能）

### 3. 手動実行
```bash
python main.py
```

### 4. cron自動実行（毎日午前4時）

crontabを編集:
```bash
crontab -e
```

以下を追記（パスは環境に合わせて変更）:
```
0 4 * * * cd /path/to/news-collector && ANTHROPIC_API_KEY=your-key /usr/bin/python3 main.py >> /tmp/news-collector.log 2>&1
```

## ディレクトリ構成
```
news-collector/
├── main.py          # エントリーポイント
├── fetcher.py       # RSS取得・重複排除
├── summarizer.py    # Claude Haiku 4.5 AI要約
├── reporter.py      # HTMLレポート生成
├── config.py        # 設定・ソース定義
├── data/
│   └── posted.json  # 取得済みURL管理
├── output/          # 生成HTMLの保存先
└── requirements.txt
```

## 出力
`output/` ディレクトリにHTMLファイルが日付付きで保存され、自動的にブラウザで開きます。
