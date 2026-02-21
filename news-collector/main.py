"""エントリーポイント"""

import glob
import os
import subprocess
import sys
from datetime import datetime, timedelta

from config import NEWS_SOURCES, OUTPUT_DIR
from fetcher import fetch_articles
from summarizer import summarize_all
from reporter import generate_html
from notifier import send_email

# アーカイブ保持日数
ARCHIVE_RETENTION_DAYS = 7


def cleanup_old_reports() -> None:
    """7日以上前のHTMLレポートを削除する"""
    cutoff = datetime.now() - timedelta(days=ARCHIVE_RETENTION_DAYS)
    files = glob.glob(os.path.join(OUTPUT_DIR, "*_news.html"))
    deleted = 0

    for filepath in files:
        try:
            # ファイル名から日時を取得（例: 20250220_0400_news.html）
            basename = os.path.basename(filepath)
            date_str = basename[:13]  # "YYYYMMDD_HHMM"
            file_date = datetime.strptime(date_str, "%Y%m%d_%H%M")
            if file_date < cutoff:
                os.remove(filepath)
                print(f"  [archive] 削除: {basename}")
                deleted += 1
        except (ValueError, OSError):
            # 日付パース失敗・削除失敗は無視
            continue

    if deleted:
        print(f"[archive] {deleted} 件の古いレポートを削除しました（{ARCHIVE_RETENTION_DAYS}日以上前）")
    else:
        print(f"[archive] 削除対象なし（保持期間: {ARCHIVE_RETENTION_DAYS}日）")


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

    # 4. メール通知
    print("\n=== メール通知 ===")
    send_email(filepath, articles)

    # 5. 古いレポートを削除
    print("\n=== アーカイブ整理 ===")
    cleanup_old_reports()

    # 6. ブラウザで自動オープン
    print("\n=== ブラウザで表示 ===")
    try:
        subprocess.run(["open", filepath], check=True)
        print(f"ブラウザで開きました: {filepath}")
    except Exception as e:
        print(f"ブラウザを開けませんでした。手動で開いてください: {filepath}\nエラー: {e}")

    print("\n=== 完了 ===")


if __name__ == "__main__":
    main()
