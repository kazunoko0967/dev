# 📈 トレーダー向けニュース自動収集システム

世界の主要経済メディア（Bloomberg、BBC、NHKなど）からニュースを自動収集し、Claude AI が日本語で要約してHTMLレポートを生成するシステムです。毎朝4時に自動実行し、結果をブラウザ表示＆メール通知します。

---

## 機能

- **自動収集**: 9つのRSSフィードからビジネス・経済ニュースを取得
- **フィルタリング**: 料理・スポーツ・芸能など無関係な記事を自動除外
- **AI要約**: Claude Haiku 4.5 が日本語150文字で要約＋センチメント分析
- **HTMLレポート**: タブ切替・ソース別カラーのビジュアルレポートをブラウザ表示
- **メール通知**: Resend 経由でHTMLレポートをメール送信
- **自動実行**: cron で毎日午前4時に実行

---

## ニュースソース

| カテゴリ | ソース |
|----------|--------|
| マーケット | Bloomberg, FT Markets, MarketWatch, Investing.com |
| 国際・政治 | BBC Business, The Guardian |
| 国内経済 | NHK 経済, 東洋経済 |
| 国際・政治（日本語） | NHK 国際 |

---

## セットアップ

### 前提条件

- Python 3.11 以上
- [Anthropic API キー](https://console.anthropic.com/) （Claude AI 利用）
- [Resend アカウント](https://resend.com/) （メール通知 ※任意）

---

### 1. パッケージインストール

```bash
cd news-collector
pip install -r requirements.txt
```

---

### 2. 環境変数の設定

#### 必須

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

#### メール通知を使う場合（任意）

```bash
export RESEND_API_KEY="re_xxxxxxxxxxxxxxxx"   # Resend APIキー
export RESEND_FROM_EMAIL="your@yourdomain.com" # 送信元アドレス（Resendで認証済み）
export NOTIFY_EMAIL="you@example.com"          # 受信先アドレス
```

> **メール通知を使わない場合**はこれらを設定しなくても動作します。ブラウザ表示のみになります。

#### 永続化（再起動後も有効にする）

```bash
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.zshrc
echo 'export RESEND_API_KEY="re_xxxxxxxxxxxxxxxx"' >> ~/.zshrc
echo 'export RESEND_FROM_EMAIL="your@yourdomain.com"' >> ~/.zshrc
echo 'export NOTIFY_EMAIL="you@example.com"' >> ~/.zshrc
source ~/.zshrc
```

#### Resend APIキーの取得手順

1. [resend.com](https://resend.com/) にアクセスして無料登録（100通/日まで無料）
2. ダッシュボード → **API Keys** → **Create API Key**
3. **Domains** → 送信元ドメインを認証
   - 独自ドメインがない場合は `onboarding@resend.dev` を `RESEND_FROM_EMAIL` に設定すれば即使用可能

---

### 3. 手動実行

```bash
python main.py
```

実行すると `output/` フォルダにHTMLレポートが保存され、自動的にブラウザで開きます。

---

### 4. cron で毎日自動実行（午前4時）

crontab を開く:

```bash
crontab -e
```

以下を追記（パスとAPIキーは自分の環境に合わせて変更）:

```
0 4 * * * cd /path/to/news-collector && ANTHROPIC_API_KEY=your-key RESEND_API_KEY=your-key RESEND_FROM_EMAIL=your@email.com NOTIFY_EMAIL=you@email.com /usr/bin/python3 main.py >> /tmp/news-collector.log 2>&1
```

ログの確認:

```bash
tail -f /tmp/news-collector.log
```

---

## ディレクトリ構成

```
news-collector/
├── main.py          # エントリーポイント（全体の実行フロー）
├── config.py        # ニュースソース・設定定義
├── fetcher.py       # RSS取得・重複排除・フィルタリング
├── summarizer.py    # Claude Haiku 4.5 によるAI要約
├── reporter.py      # HTMLレポート生成
├── notifier.py      # Resend メール通知
├── requirements.txt # 依存パッケージ
├── data/
│   └── posted.json  # 取得済みURLの管理（重複防止）
└── output/          # 生成されたHTMLレポートの保存先
```

---

## 実行フロー

```
RSS取得 → フィルタリング → AI要約 → HTMLレポート生成 → メール送信 → ブラウザ表示
```

---

## メール通知について

環境変数を設定すると、レポート生成のたびに自動でメールが届きます。

### メールの仕様

| 項目 | 内容 |
|------|------|
| 件名 | `📰 世界ビジネス・経済ニュース - YYYY年MM月DD日（N件）` |
| 本文 | 生成したHTMLレポートをそのままメール本文に埋め込み |
| 表示 | ブラウザと同じデザイン（カード・タブUI）でメールクライアント上に表示 |
| 送信タイミング | `main.py` 実行のたびに送信（cron設定時は毎朝4時） |

### Resend の無料枠

- 無料プラン: **100通/日・3,000通/月**
- 毎日1通送信する場合は無料枠内で十分運用可能
- 詳細: [resend.com/pricing](https://resend.com/pricing)

### メール通知をスキップしたい場合

以下の3つの環境変数がいずれか未設定の場合、メール送信はスキップされ、ブラウザ表示のみになります（エラーにはなりません）。

```
RESEND_API_KEY / RESEND_FROM_EMAIL / NOTIFY_EMAIL
```

---

## 出力レポートについて

### ブラウザ表示

`output/` フォルダに `YYYYMMDD_HHMM_news.html` という形式で保存されます。実行のたびに新しいファイルが作成されます。

### レポートの構成

| セクション | 内容 |
|------------|------|
| **統計バー** | 総取得件数・ソース別件数を表示 |
| **注目ニュース TOP3** | 最新3件を大きなカードで強調表示 |
| **全ニュース一覧** | ソース別タブで絞り込み可能な記事リスト |

### 各記事に表示される情報

- **ソースバッジ**: メディア名をカラーバッジで表示
- **センチメント**: `▲ 好材料` / `▼ 悪材料` / `― 中立` を色分け表示
- **AI要約**: Claude Haiku 4.5 による日本語150文字の要約
- **企業名チップ**: 記事に登場する上場企業名（オレンジ色）
- **タグチップ**: 株価上昇材料・為替・金融政策・地政学など分類タグ（青色）
- **元記事タイトル**: 原文タイトルをグレーで表示
- **続きを読む**: クリックで元記事をブラウザで開く
