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

    prompt = f"""あなたはプロのトレーダー向けニュースアナリストです。
以下のニュース記事を日本語で{SUMMARY_MAX_CHARS}文字以内に要約してください。

要約に含めるべき観点（該当するもの）:
- 株価・為替・金利・商品価格への影響
- 中央銀行・金融政策の動向
- 地政学リスク・政治的イベント
- 主要企業の業績・M&A・経営動向
- マクロ経済指標（GDP・CPI・雇用など）

ルール:
- 日本語以外は日本語に翻訳して要約する
- トレーダーが即座に判断できる簡潔な表現にする
- 数字・通貨・パーセントは具体的に記載する
- 要約文のみを出力し、前置きや説明は不要

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
