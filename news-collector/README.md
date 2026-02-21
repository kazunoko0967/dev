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

### 2. APIキーの設定
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

永続化する場合は `~/.zshrc` または `~/.bash_profile` に追記:
```bash
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

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
