"""HTMLレポート生成モジュール"""

import os
from datetime import datetime

from config import OUTPUT_DIR

# ソースごとのカラーマッピング
SOURCE_COLORS = {
    # マーケット系 - 赤系
    "Bloomberg": {"bg": "#b71c1c", "badge": "#e53935"},
    "FT Markets": {"bg": "#bf360c", "badge": "#f4511e"},
    "MarketWatch": {"bg": "#880e4f", "badge": "#d81b60"},
    "Investing.com": {"bg": "#4a148c", "badge": "#7b1fa2"},
    # 国際・政治系 - 緑系
    "BBC Business": {"bg": "#1b5e20", "badge": "#388e3c"},
    "The Guardian": {"bg": "#004d40", "badge": "#00796b"},
    # 日本語系 - 青系
    "NHK 経済": {"bg": "#1a237e", "badge": "#3949ab"},
    "NHK 国際": {"bg": "#0d47a1", "badge": "#1976d2"},
    "東洋経済": {"bg": "#e65100", "badge": "#f57c00"},
}
DEFAULT_COLOR = {"bg": "#37474f", "badge": "#607d8b"}

# センチメント表示設定
SENTIMENT_CONFIG = {
    "positive": {"label": "好材料", "color": "#2e7d32", "bg": "#e8f5e9", "icon": "▲"},
    "negative": {"label": "悪材料", "color": "#c62828", "bg": "#ffebee", "icon": "▼"},
    "neutral":  {"label": "中立",   "color": "#546e7a", "bg": "#eceff1", "icon": "―"},
}


def generate_html(articles: list) -> str:
    """HTMLレポートを生成して保存し、ファイルパスを返す"""
    now = datetime.now()
    date_str = now.strftime("%Y年%m月%d日")
    filename = now.strftime("%Y%m%d_%H%M") + "_news.html"

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, filename)

    # ソース別に記事をグループ化
    by_source: dict[str, list] = {}
    for article in articles:
        src = article["source"]
        by_source.setdefault(src, []).append(article)

    # TOP3（先頭3件）
    top3 = articles[:3]

    html = _build_html(date_str, top3, by_source, articles)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[report] レポートを保存しました: {filepath}")
    return filepath


def _source_badge(source: str) -> str:
    color = SOURCE_COLORS.get(source, DEFAULT_COLOR)["badge"]
    return f'<span class="badge" style="background:{color}">{source}</span>'


def _sentiment_badge(sentiment: str) -> str:
    cfg = SENTIMENT_CONFIG.get(sentiment, SENTIMENT_CONFIG["neutral"])
    return (
        f'<span class="sentiment-badge" '
        f'style="color:{cfg["color"]};background:{cfg["bg"]}">'
        f'{cfg["icon"]} {cfg["label"]}</span>'
    )


def _tag_chips(tags: list) -> str:
    if not tags:
        return ""
    chips = "".join(f'<span class="tag-chip">{t}</span>' for t in tags)
    return f'<div class="tag-row">{chips}</div>'


def _company_chips(companies: list) -> str:
    if not companies:
        return ""
    chips = "".join(f'<span class="company-chip">{c}</span>' for c in companies)
    return f'<div class="tag-row">{chips}</div>'


def _build_html(date_str: str, top3: list, by_source: dict, all_articles: list) -> str:

    # TOP3カード
    top3_cards = ""
    for article in top3:
        colors = SOURCE_COLORS.get(article["source"], DEFAULT_COLOR)
        top3_cards += f"""
        <a href="{article['url']}" target="_blank" class="top-card" style="border-top: 4px solid {colors['badge']};">
            {_source_badge(article['source'])}
            <p class="card-summary">{article.get('ai_summary') or article['title']}</p>
            {_company_chips(article.get('companies', []))}
            {_tag_chips(article.get('tags', []))}
            <p class="card-title">{article['title']}</p>
        </a>"""

    # ソース別タブ
    tab_buttons = '<button class="tab-btn active" onclick="showTab(\'all\', this)">すべて</button>'
    tab_contents = f'<div id="tab-all" class="tab-content active">{_article_list(all_articles)}</div>'
    for source, arts in by_source.items():
        tab_id = source.replace(" ", "_")
        tab_buttons += f'<button class="tab-btn" onclick="showTab(\'{tab_id}\', this)">{source} <span class="count">{len(arts)}</span></button>'
        tab_contents += f'<div id="tab-{tab_id}" class="tab-content">{_article_list(arts)}</div>'

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>トレーダー向けニュース - {date_str}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f0f2f5; color: #1a1a2e; }}
  header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; padding: 24px 32px; }}
  header h1 {{ font-size: 1.6rem; font-weight: 700; letter-spacing: 0.02em; }}
  header p {{ font-size: 0.9rem; opacity: 0.7; margin-top: 4px; }}
  .container {{ max-width: 1200px; margin: 0 auto; padding: 24px 16px; }}

  /* Stats */
  .stats {{ display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 24px; }}
  .stat-item {{ background: white; border-radius: 10px; padding: 12px 20px; font-size: 0.85rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }}
  .stat-item strong {{ font-size: 1.3rem; display: block; color: #1a1a2e; }}

  /* Section title */
  .section-title {{ font-size: 0.85rem; font-weight: 700; color: #666; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px; margin-top: 28px; }}

  /* TOP3 */
  .top3-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-bottom: 8px; }}
  .top-card {{ background: white; border-radius: 12px; padding: 18px; text-decoration: none; color: inherit; display: flex; flex-direction: column; gap: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: transform 0.2s, box-shadow 0.2s; }}
  .top-card:hover {{ transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,0.12); }}
  .card-summary {{ font-size: 0.93rem; line-height: 1.6; color: #222; flex: 1; }}
  .card-title {{ font-size: 0.75rem; color: #999; border-top: 1px solid #eee; padding-top: 8px; }}

  /* Badges */
  .badge {{ display: inline-block; padding: 2px 8px; border-radius: 20px; font-size: 0.7rem; font-weight: 600; color: white; }}
  .sentiment-badge {{ display: inline-block; padding: 2px 8px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; }}
  .tag-row {{ display: flex; flex-wrap: wrap; gap: 4px; margin-top: 4px; }}
  .tag-chip {{ display: inline-block; padding: 2px 7px; border-radius: 4px; font-size: 0.68rem; background: #e3f2fd; color: #1565c0; font-weight: 500; }}
  .company-chip {{ display: inline-block; padding: 2px 7px; border-radius: 4px; font-size: 0.68rem; background: #fff8e1; color: #e65100; font-weight: 600; }}

  /* Tabs */
  .tabs {{ background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); overflow: hidden; }}
  .tab-bar {{ display: flex; border-bottom: 2px solid #f0f2f5; overflow-x: auto; padding: 0 16px; }}
  .tab-btn {{ background: none; border: none; padding: 12px 16px; font-size: 0.85rem; font-weight: 600; color: #888; cursor: pointer; border-bottom: 3px solid transparent; margin-bottom: -2px; white-space: nowrap; transition: color 0.2s; }}
  .tab-btn:hover {{ color: #1a1a2e; }}
  .tab-btn.active {{ color: #1a1a2e; border-bottom-color: #3949ab; }}
  .count {{ display: inline-block; background: #f0f2f5; border-radius: 10px; padding: 1px 6px; font-size: 0.72rem; margin-left: 3px; }}
  .tab-content {{ display: none; }}
  .tab-content.active {{ display: block; }}

  /* Article rows */
  .article-row {{ display: flex; align-items: flex-start; gap: 16px; padding: 14px 20px; border-bottom: 1px solid #f5f5f5; text-decoration: none; color: inherit; transition: background 0.15s; }}
  .article-row:hover {{ background: #fafbff; }}
  .article-row:last-child {{ border-bottom: none; }}
  .article-body {{ flex: 1; min-width: 0; }}
  .article-meta {{ display: flex; gap: 6px; align-items: center; flex-wrap: wrap; margin-bottom: 4px; }}
  .article-summary {{ font-size: 0.9rem; line-height: 1.6; color: #222; }}
  .article-title {{ font-size: 0.75rem; color: #bbb; margin-top: 3px; }}
  .article-link {{ font-size: 0.78rem; color: #3949ab; font-weight: 600; white-space: nowrap; }}
</style>
</head>
<body>
<header>
  <h1>📈 トレーダー向けニュースレポート</h1>
  <p>{date_str} 自動収集・AI分析レポート</p>
</header>
<div class="container">

  <div class="stats">
    <div class="stat-item"><strong>{len(all_articles)}</strong>件 取得</div>
    {''.join(f'<div class="stat-item"><strong>{len(v)}</strong>{k}</div>' for k, v in by_source.items())}
  </div>

  <p class="section-title">注目ニュース TOP3</p>
  <div class="top3-grid">{top3_cards}</div>

  <p class="section-title">全ニュース一覧</p>
  <div class="tabs">
    <div class="tab-bar">{tab_buttons}</div>
    {tab_contents}
  </div>

</div>
<script>
function showTab(id, btn) {{
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  document.getElementById('tab-' + id).classList.add('active');
  btn.classList.add('active');
}}
</script>
</body>
</html>"""


def _article_list(articles: list) -> str:
    if not articles:
        return '<p style="padding:20px;color:#aaa;">記事がありません</p>'
    rows = ""
    for a in articles:
        rows += f"""
    <a href="{a['url']}" target="_blank" class="article-row">
      <div class="article-body">
        <div class="article-meta">
            {_source_badge(a['source'])}
            {_sentiment_badge(a.get('sentiment', 'neutral'))}
        </div>
        <p class="article-summary">{a.get('ai_summary') or a['title']}</p>
        {_company_chips(a.get('companies', []))}
        {_tag_chips(a.get('tags', []))}
        <p class="article-title">{a['title']}</p>
      </div>
      <span class="article-link">続きを読む →</span>
    </a>"""
    return rows
