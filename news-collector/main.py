"""エントリーポイント"""

import subprocess
import sys

from config import NEWS_SOURCES
from fetcher import fetch_articles
from summarizer import summarize_all
from reporter import generate_html


def main():
    print("=== ニュース収集開始 ===")

    # 1. RSS取得
    articles = fetch_articles(NEWS_SOURCES)
    if not articles:
        print("新しい記事が見つかりませんでした。")
        return

    print(f"\n合計 {len(articles)} 件の新着記事を取得しました。")

    # 2. AI要約
    print("\n=== AI要約開始 ===")
    articles = summarize_all(articles)

    # 3. HTMLレポート生成
    print("\n=== レポート生成 ===")
    filepath = generate_html(articles)

    # 4. ブラウザで自動オープン
    print("\n=== ブラウザで表示 ===")
    try:
        subprocess.run(["open", filepath], check=True)
        print(f"ブラウザで開きました: {filepath}")
    except Exception as e:
        print(f"ブラウザを開けませんでした。手動で開いてください: {filepath}\nエラー: {e}")

    print("\n=== 完了 ===")


if __name__ == "__main__":
    main()
