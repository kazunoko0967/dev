"""メール通知モジュール（Resend + HTML添付）"""

import os
import base64
from datetime import datetime

import resend


def send_email(filepath: str, articles: list) -> None:
    """HTMLファイルを添付してResend経由でメールを送信する"""

    api_key = os.environ.get("RESEND_API_KEY")
    from_email = os.environ.get("RESEND_FROM_EMAIL")
    to_email = os.environ.get("NOTIFY_EMAIL")

    if not api_key or not from_email or not to_email:
        print("[notifier] RESEND_API_KEY / RESEND_FROM_EMAIL / NOTIFY_EMAIL が未設定のためスキップします。")
        return

    resend.api_key = api_key

    date_str = datetime.now().strftime("%Y年%m月%d日")
    subject = f"📰 世界ビジネス・経済ニュース - {date_str}（{len(articles)}件）"

    # ソース別件数集計
    by_source: dict[str, int] = {}
    for a in articles:
        by_source[a["source"]] = by_source.get(a["source"], 0) + 1
    source_summary = "　".join([f"{src}: {cnt}件" for src, cnt in by_source.items()])

    # TOP3カード
    top3_rows = ""
    for a in articles[:3]:
        summary = a.get("ai_summary") or a["title"]
        top3_rows += f"""
        <tr>
          <td style="padding:12px 16px;border-bottom:1px solid #f0f0f0;">
            <span style="background:#3949ab;color:white;padding:2px 8px;border-radius:10px;font-size:12px;">{a['source']}</span>
            <p style="margin:8px 0 4px;font-size:15px;color:#222;">{summary}</p>
            <a href="{a['url']}" style="font-size:12px;color:#3949ab;text-decoration:none;">続きを読む →</a>
          </td>
        </tr>"""

    # メール本文HTML
    body_html = f"""<!DOCTYPE html>
<html lang="ja">
<head><meta charset="UTF-8"></head>
<body style="font-family:-apple-system,sans-serif;background:#f0f2f5;margin:0;padding:20px;">
  <div style="max-width:600px;margin:0 auto;background:white;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.1);">
    <div style="background:linear-gradient(135deg,#1a1a2e,#16213e);color:white;padding:24px 32px;">
      <h1 style="margin:0;font-size:20px;">世界ビジネス・経済ニュース</h1>
      <p style="margin:6px 0 0;opacity:0.7;font-size:13px;">{date_str}　{source_summary}</p>
    </div>
    <div style="padding:20px 24px;">
      <p style="font-size:13px;color:#888;margin:0 0 16px;">📌 注目ニュース TOP3</p>
      <table width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #eee;border-radius:8px;overflow:hidden;">
        {top3_rows}
      </table>
      <p style="margin:20px 0 0;font-size:13px;color:#888;">
        全{len(articles)}件のニュースは添付のHTMLファイルをブラウザで開いてご確認ください。
      </p>
    </div>
    <div style="background:#f8f9fa;padding:12px 24px;text-align:center;">
      <p style="margin:0;font-size:12px;color:#aaa;">このメールは自動送信されています</p>
    </div>
  </div>
</body>
</html>"""

    # HTMLファイルをBase64エンコードして添付
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    # 送信
    try:
        response = resend.Emails.send({
            "from": from_email,
            "to": [to_email],
            "subject": subject,
            "html": body_html,
            "attachments": [
                {
                    "filename": filename,
                    "content": encoded,
                    "type": "text/html",
                }
            ],
        })
        print(f"[notifier] メールを送信しました → {to_email} (id: {response['id']})")
    except Exception as e:
        print(f"[notifier] メール送信エラー: {e}")
