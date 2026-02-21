"""Claude Haiku 4.5 によるAI要約・材料分析モジュール"""

import json
import anthropic
import os

from config import CLAUDE_MODEL, SUMMARY_MAX_CHARS

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise EnvironmentError("ANTHROPIC_API_KEY が設定されていません。export ANTHROPIC_API_KEY='your-key' を実行してください。")

client = anthropic.Anthropic(api_key=api_key)


def analyze_article(article: dict) -> dict:
    """記事を要約し、好材料・悪材料・企業名を分析してJSONで返す"""
    title = article["title"]
    raw = article["raw_summary"]
    source = article["source"]

    prompt = f"""あなたはプロのトレーダー向けニュースアナリストです。
以下のニュース記事を分析して、必ずJSON形式のみで出力してください。

出力形式（JSONのみ・余計なテキスト不要）:
{{
  "summary": "日本語{SUMMARY_MAX_CHARS}文字以内の要約。数字・通貨・%を具体的に記載。",
  "sentiment": "positive / negative / neutral のいずれか",
  "companies": ["言及されている上場企業名（日本語）のリスト。なければ空リスト"],
  "tags": ["該当するタグのリスト: 株価上昇材料 / 株価下落材料 / 為替 / 金利 / 金融政策 / 地政学 / 決算 / M&A / 経済指標 / その他"]
}}

分析観点:
- 好材料（positive）: 業績好調・増配・自社株買い・好決算・買収・政策支援など
- 悪材料（negative）: 業績悪化・減配・リコール・制裁・地政学リスク・利上げ懸念など
- 中立（neutral）: 人事異動・一般的な政策発表・中立的な経済指標など

ルール:
- 日本語以外は日本語に翻訳して要約する
- トレーダーが即座に判断できる簡潔な表現にする
- 企業名は正式名称（例: トヨタ自動車、Apple Inc.）で記載

ソース: {source}
タイトル: {title}
本文: {raw[:1000]}
"""

    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )

    text = message.content[0].text.strip()

    # JSON部分を抽出してパース
    try:
        # コードブロックが含まれる場合に対応
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        result = json.loads(text)
    except Exception:
        # パース失敗時はフォールバック
        result = {
            "summary": text[:SUMMARY_MAX_CHARS],
            "sentiment": "neutral",
            "companies": [],
            "tags": [],
        }

    return result


def summarize_all(articles: list) -> list:
    """全記事を要約・分析する"""
    total = len(articles)
    for i, article in enumerate(articles, 1):
        print(f"[summarize] ({i}/{total}) {article['source']}: {article['title'][:40]}...")
        try:
            result = analyze_article(article)
            article["ai_summary"] = result.get("summary", article["title"])
            article["sentiment"] = result.get("sentiment", "neutral")
            article["companies"] = result.get("companies", [])
            article["tags"] = result.get("tags", [])
        except Exception as e:
            print(f"  → エラー: {e}")
            article["ai_summary"] = article["title"]
            article["sentiment"] = "neutral"
            article["companies"] = []
            article["tags"] = []
    return articles
