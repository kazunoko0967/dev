"""設定・ニュースソース定義"""

# ニュースソース定義（トレーダー向け）
NEWS_SOURCES = [
    # ===== マーケット・金融 =====
    {
        "name": "Bloomberg",
        "url": "https://feeds.bloomberg.com/markets/news.rss",
        "language": "en",
        "category": "マーケット",
    },
    {
        "name": "FT Markets",
        "url": "https://www.ft.com/markets?format=rss",
        "language": "en",
        "category": "マーケット",
    },
    {
        "name": "MarketWatch",
        "url": "https://feeds.marketwatch.com/marketwatch/topstories/",
        "language": "en",
        "category": "マーケット",
    },
    {
        "name": "Investing.com",
        "url": "https://www.investing.com/rss/news.rss",
        "language": "en",
        "category": "マーケット",
    },
    # ===== 国際・政治 =====
    {
        "name": "BBC Business",
        "url": "https://feeds.bbci.co.uk/news/business/rss.xml",
        "language": "en",
        "category": "国際・政治",
    },
    {
        "name": "The Guardian",
        "url": "https://www.theguardian.com/business/rss",
        "language": "en",
        "category": "国際・政治",
    },
    # ===== 日本語ニュース =====
    {
        "name": "NHK 経済",
        "url": "https://www.nhk.or.jp/rss/news/cat5.xml",
        "language": "ja",
        "category": "国内経済",
    },
    {
        "name": "NHK 国際",
        "url": "https://www.nhk.or.jp/rss/news/cat6.xml",
        "language": "ja",
        "category": "国際・政治",
    },
    {
        "name": "東洋経済",
        "url": "https://toyokeizai.net/list/feed/rss",
        "language": "ja",
        "category": "国内経済",
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
