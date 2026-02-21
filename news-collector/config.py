"""設定・ニュースソース定義"""

# ニュースソース定義
NEWS_SOURCES = [
    {
        "name": "NHK ビジネス",
        "url": "https://www.nhk.or.jp/rss/news/cat5.xml",
        "language": "ja",
        "category": "国内経済",
    },
    {
        "name": "東洋経済",
        "url": "https://toyokeizai.net/list/feed/rss",
        "language": "ja",
        "category": "日本ビジネス",
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
