"""設定・ニュースソース定義"""

# ニュースソース定義
NEWS_SOURCES = [
    {
        "name": "株探",
        "url": "https://kabutan.jp/rss/news",
        "language": "ja",
        "category": "日本株・経済",
    },
    {
        "name": "Bloomberg",
        "url": "https://feeds.bloomberg.com/markets/news.rss",
        "language": "en",
        "category": "グローバル金融",
    },
    {
        "name": "The Guardian",
        "url": "https://www.theguardian.com/business/rss",
        "language": "en",
        "category": "ビジネス",
    },
    {
        "name": "BBC Business",
        "url": "https://feeds.bbci.co.uk/news/business/rss.xml",
        "language": "en",
        "category": "世界経済",
    },
]

# 1ソースあたりの最大取得記事数
MAX_ARTICLES_PER_SOURCE = 5

# AI要約の最大文字数（日本語）
SUMMARY_MAX_CHARS = 150

# 使用モデル
CLAUDE_MODEL = "claude-haiku-4-5-20251001"

# 出力ディレクトリ
OUTPUT_DIR = "output"

# 取得済みURL管理ファイル
POSTED_FILE = "data/posted.json"
