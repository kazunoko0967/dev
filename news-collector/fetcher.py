"""RSSフィード取得モジュール"""

import json
import os
import re

import feedparser

from config import MAX_ARTICLES_PER_SOURCE, POSTED_FILE

# トレーダー向けキーワード（タイトル・本文にこれらが含まれる記事を優先）
FINANCE_KEYWORDS = [
    # 市場・相場
    "market", "stock", "shares", "equity", "index", "nasdaq", "s&p", "dow",
    "nikkei", "topix", "ftse", "dax", "投資", "株", "相場", "指数",
    # 為替・金利
    "forex", "currency", "dollar", "yen", "euro", "fx", "exchange rate",
    "interest rate", "yield", "bond", "treasury", "為替", "円", "金利", "債券",
    # 経済指標
    "gdp", "inflation", "cpi", "ppi", "unemployment", "jobs", "payroll",
    "recession", "growth", "economic", "economy", "景気", "物価", "雇用", "gdp",
    # 中央銀行・金融政策
    "fed", "federal reserve", "ecb", "boj", "bank of japan", "rate hike",
    "rate cut", "quantitative", "monetary policy", "日銀", "利上げ", "利下げ", "金融政策",
    # 企業・M&A
    "earnings", "revenue", "profit", "acquisition", "merger", "ipo", "buyback",
    "dividend", "forecast", "guidance", "決算", "増益", "減益", "買収", "合併", "配当",
    # 地政学・政治
    "tariff", "trade war", "sanction", "geopolit", "war", "conflict", "oil",
    "energy", "opec", "関税", "貿易", "制裁", "地政学", "石油", "エネルギー",
    # 企業名（主要）
    "apple", "microsoft", "google", "amazon", "nvidia", "tesla", "meta",
    "toyota", "sony", "softbank", "トヨタ", "ソニー", "ソフトバンク",
]

# 除外キーワード（これらが含まれる記事はスキップ）
EXCLUDE_KEYWORDS = [
    "recipe", "cooking", "food", "restaurant", "fashion", "sport", "soccer",
    "football", "basketball", "celebrity", "entertainment", "movie", "music",
    "travel", "tourism", "weather", "料理", "レシピ", "スポーツ", "芸能", "旅行",
    "グルメ", "映画", "音楽", "ファッション", "観光",
]


def _is_finance_relevant(title: str, summary: str) -> bool:
    """トレーダー向けに関連する記事かどうかを判定する"""
    text = (title + " " + summary).lower()

    # 除外キーワードが含まれる場合はスキップ
    for kw in EXCLUDE_KEYWORDS:
        if kw.lower() in text:
            return False

    # 金融キーワードが1つでも含まれる場合は採用
    for kw in FINANCE_KEYWORDS:
        if kw.lower() in text:
            return True

    # キーワードなしでも NHK・東洋経済は経済カテゴリなので通す
    return False


def load_posted_urls() -> set:
    """取得済みURLを読み込む"""
    if not os.path.exists(POSTED_FILE):
        return set()
    with open(POSTED_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return set(data.get("urls", []))


def save_posted_urls(urls: set) -> None:
    """取得済みURLを保存する"""
    os.makedirs(os.path.dirname(POSTED_FILE), exist_ok=True)
    with open(POSTED_FILE, "w", encoding="utf-8") as f:
        json.dump({"urls": list(urls)}, f, ensure_ascii=False, indent=2)


def fetch_articles(sources: list) -> list:
    """全ソースからRSS記事を取得する"""
    posted_urls = load_posted_urls()
    all_articles = []
    new_urls = set()

    for source in sources:
        print(f"[fetch] {source['name']} を取得中...")
        try:
            feed = feedparser.parse(source["url"])
            count = 0
            skipped = 0
            for entry in feed.entries:
                if count >= MAX_ARTICLES_PER_SOURCE:
                    break

                url = entry.get("link", "")
                if not url or url in posted_urls:
                    continue

                title = entry.get("title", "").strip()
                summary = entry.get("summary", entry.get("description", "")).strip()
                published = entry.get("published", "")

                # 金融・経済関連フィルタリング
                # NHK・東洋経済はカテゴリが経済なのでキーワードチェックを緩和
                if source["language"] == "en":
                    if not _is_finance_relevant(title, summary):
                        skipped += 1
                        new_urls.add(url)  # 除外済みとして記録
                        continue

                article = {
                    "source": source["name"],
                    "category": source["category"],
                    "language": source["language"],
                    "title": title,
                    "url": url,
                    "raw_summary": summary,
                    "published": published,
                    "ai_summary": None,
                    "sentiment": "neutral",
                    "companies": [],
                    "tags": [],
                }
                all_articles.append(article)
                new_urls.add(url)
                count += 1

            print(f"  → {count} 件取得（{skipped} 件除外）")
        except Exception as e:
            print(f"  → エラー: {e}")

    # 取得済みURLを更新
    posted_urls.update(new_urls)
    save_posted_urls(posted_urls)

    return all_articles
