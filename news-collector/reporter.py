"""HTMLレポート生成モジュール"""

import os
from datetime import datetime

from config import OUTPUT_DIR

# ソースごとのカラーマッピング
SOURCE_COLORS = {
    "NHK ビジネス": {"bg": "#1a237e", "badge": "#3949ab"},
    "東洋経済": {"bg": "#e65100", "badge": "#f57c00"},
    "Bloomberg": {"bg": "#b71c1c", "badge": "#e53935"},
    "The Guardian": {"bg": "#1b5e20", "badge": "#43a047"},
    "BBC Business": {"bg": "#880e4f", "badge": "#e91e8c"},
}
DEFAULT_COLOR = {"bg": "#37474f", "badge": "#607d8b"}


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

    # TOP3（全ソースから先頭3件）
    top3 = articles[:3]

    html = _build_html(date_str, top3, by_source, articles)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[report] レポートを保存しました: {filepath}")
    return filepath


def _source_badge(source: str) -> str:
    color = SOURCE_COLORS.get(source, DEFAULT_COLOR)["badge"]
    return f'<span class="badge" style="background:{color}">{source}</span>'


def _build_html(date_str: str, top3: list, by_source: dict, all_articles: list) -> str:
    top3_cards = ""
    for article in top3:
        colors = SOURCE_COLORS.get(article["source"], DEFAULT_COLOR)
        top3_cards += f"""
        <a href="{article['url']}" target="_blank" class="top-card" style="border-top: 4px solid {colors['badge']};">
            {_source_badge(article['source'])}
            <p class="card-summary">{article['ai_summary'] or article['title']}</p>
            <p class="card-title">{article['title']}</p>
        </a>"""

    # ソース別タブコンテンツ
    tab_buttons = '<button class="tab-btn active" onclick="showTab(\'all\')">すべて</button>'
    tab_contents = f'<div id="tab-all" class="tab-content active">{_article_list(all_articles)}</div>'

    for source, arts in by_source.items():
        tab_id = source.replace(" ", "_")
        tab_buttons += f'<button class="tab-btn" onclick="showTab(\'{tab_id}\')">{source} <span class="count">{len(arts)}</span></button>'
        tab_contents += f'<div id="tab-{tab_id}" class="tab-content">{_article_list(arts)}</div>'

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>世界ビジネス・経済ニュース - {date_str}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f0f2f5; color: #1a1a2e; }}
  header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; padding: 24px 32px; }}
  header h1 {{ font-size: 1.6rem; font-weight: 700; letter-spacing: 0.02em; }}
  header p {{ font-size: 0.9rem; opacity: 0.7; margin-top: 4px; }}
  .container {{ max-width: 1100px; margin: 0 auto; padding: 24px 16px; }}

  /* TOP3 */
  .section-title {{ font-size: 1rem; font-weight: 700; color: #555; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 16px; }}
  .top3-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-bottom: 32px; }}
  .top-card {{ background: white; border-radius: 12px; padding: 20px; text-decoration: none; color: inherit; display: flex; flex-direction: column; gap: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: transform 0.2s, box-shadow 0.2s; }}
  .top-card:hover {{ transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,0.12); }}
  .card-summary {{ font-size: 0.95rem; line-height: 1.6; color: #222; flex: 1; }}
  .card-title {{ font-size: 0.78rem; color: #888; border-top: 1px solid #eee; padding-top: 10px; }}

  /* Badge */
  .badge {{ display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.72rem; font-weight: 600; color: white; }}

  /* Tabs */
  .tabs {{ background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); overflow: hidden; }}
  .tab-bar {{ display: flex; gap: 0; border-bottom: 2px solid #f0f2f5; overflow-x: auto; padding: 0 16px; }}
  .tab-btn {{ background: none; border: none; padding: 14px 18px; font-size: 0.88rem; font-weight: 600; color: #888; cursor: pointer; border-bottom: 3px solid transparent; margin-bottom: -2px; white-space: nowrap; transition: color 0.2s; }}
  .tab-btn:hover {{ color: #1a1a2e; }}
  .tab-btn.active {{ color: #1a1a2e; border-bottom-color: #3949ab; }}
  .count {{ display: inline-block; background: #f0f2f5; border-radius: 10px; padding: 1px 7px; font-size: 0.75rem; margin-left: 4px; }}
  .tab-content {{ display: none; padding: 8px 0; }}
  .tab-content.active {{ display: block; }}

  /* Article rows */
  .article-row {{ display: flex; align-items: flex-start; gap: 16px; padding: 16px 20px; border-bottom: 1px solid #f5f5f5; text-decoration: none; color: inherit; transition: background 0.15s; }}
  .article-row:hover {{ background: #fafbff; }}
  .article-row:last-child {{ border-bottom: none; }}
  .article-body {{ flex: 1; }}
  .article-summary {{ font-size: 0.92rem; line-height: 1.65; color: #222; margin-top: 6px; }}
  .article-title {{ font-size: 0.78rem; color: #aaa; margin-top: 4px; }}
  .article-link {{ font-size: 0.8rem; color: #3949ab; font-weight: 600; white-space: nowrap; padding-top: 4px; }}

  /* Stats bar */
  .stats {{ display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 20px; }}
  .stat-item {{ background: white; border-radius: 10px; padding: 12px 20px; font-size: 0.85rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }}
  .stat-item strong {{ font-size: 1.3rem; display: block; color: #1a1a2e; }}
</style>
</head>
<body>
<header>
  <h1>世界ビジネス・経済ニュース</h1>
  <p>{date_str} 自動収集レポート</p>
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
function showTab(id) {{
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  document.getElementById('tab-' + id).classList.add('active');
  event.target.classList.add('active');
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
        {_source_badge(a['source'])}
        <p class="article-summary">{a['ai_summary'] or a['title']}</p>
        <p class="article-title">{a['title']}</p>
      </div>
      <span class="article-link">続きを読む →</span>
    </a>"""
    return rows
