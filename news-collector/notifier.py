"""メール通知モジュール（Resend + HTML本文埋め込み）"""

import os
from datetime import datetime

import resend


def send_email(filepath: str, articles: list) -> None:
    """HTMLレポートをメール本文に埋め込んでResend経由で送信する"""

    api_key = os.environ.get("RESEND_API_KEY")
    from_email = os.environ.get("RESEND_FROM_EMAIL")
    to_email = os.environ.get("NOTIFY_EMAIL")

    if not api_key or not from_email or not to_email:
        print("[notifier] RESEND_API_KEY / RESEND_FROM_EMAIL / NOTIFY_EMAIL が未設定のためスキップします。")
        return

    resend.api_key = api_key

    date_str = datetime.now().strftime("%Y年%m月%d日")
    subject = f"📰 世界ビジネス・経済ニュース - {date_str}（{len(articles)}件）"

    # HTMLレポートをそのままメール本文として使用
    with open(filepath, "r", encoding="utf-8") as f:
        body_html = f.read()

    # 送信
    try:
        response = resend.Emails.send({
            "from": from_email,
            "to": [to_email],
            "subject": subject,
            "html": body_html,
        })
        print(f"[notifier] メールを送信しました → {to_email} (id: {response['id']})")
    except Exception as e:
        print(f"[notifier] メール送信エラー: {e}")
