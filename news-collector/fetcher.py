"""RSSフィード取得モジュール"""

import json
import os
from datetime import datetime, timezone

import feedparser

from config import MAX_ARTICLES_PER_SOURCE, POSTED_FILE


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
            for entry in feed.entries:
                if count >= MAX_ARTICLES_PER_SOURCE:
                    break

                url = entry.get("link", "")
                if not url or url in posted_urls:
                    continue

                title = entry.get("title", "").strip()
                summary = entry.get("summary", entry.get("description", "")).strip()
                published = entry.get("published", "")

                article = {
                    "source": source["name"],
                    "category": source["category"],
                    "language": source["language"],
                    "title": title,
                    "url": url,
                    "raw_summary": summary,
                    "published": published,
                    "ai_summary": None,
                }
                all_articles.append(article)
                new_urls.add(url)
                count += 1

            print(f"  → {count} 件取得")
        except Exception as e:
            print(f"  → エラー: {e}")

    # 取得済みURLを更新
    posted_urls.update(new_urls)
    save_posted_urls(posted_urls)

    return all_articles
