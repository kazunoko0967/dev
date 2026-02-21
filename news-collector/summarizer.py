"""Claude Haiku 4.5 によるAI要約モジュール"""

import anthropic
import os

from config import CLAUDE_MODEL, SUMMARY_MAX_CHARS

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise EnvironmentError("ANTHROPIC_API_KEY が設定されていません。export ANTHROPIC_API_KEY='your-key' を実行してください。")

client = anthropic.Anthropic(api_key=api_key)


def summarize_article(article: dict) -> str:
    """記事を日本語で要約する"""
    title = article["title"]
    raw = article["raw_summary"]
    source = article["source"]

    prompt = f"""以下のニュース記事を日本語で{SUMMARY_MAX_CHARS}文字以内に要約してください。
要約は簡潔に、読者にとって重要なポイントだけを伝えてください。
日本語以外の言語で書かれている場合は、日本語に翻訳して要約してください。
要約文のみを出力し、前置きや説明は不要です。

ソース: {source}
タイトル: {title}
本文: {raw[:1000]}
"""

    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


def summarize_all(articles: list) -> list:
    """全記事を要約する"""
    total = len(articles)
    for i, article in enumerate(articles, 1):
        print(f"[summarize] ({i}/{total}) {article['source']}: {article['title'][:40]}...")
        try:
            article["ai_summary"] = summarize_article(article)
        except Exception as e:
            print(f"  → エラー: {e}")
            article["ai_summary"] = article["title"]
    return articles
