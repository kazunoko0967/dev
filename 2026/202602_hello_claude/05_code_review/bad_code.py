"""コードレビューHello World用 - 意図的に問題を含むコード"""
import sqlite3


def get_user(username):
    # SQLインジェクション脆弱性
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()
    # conn.close() が呼ばれない（リソースリーク）


def calculate_discount(price, discount):
    # 入力検証なし
    return price - (price * discount / 100)


def process_items(items):
    results = []
    for i in range(len(items)):  # Pythonicでない書き方
        item = items[i]
        if item != None:  # is not None を使うべき
            results.append(item)
    return results


PASSWORD = "admin123"  # ハードコードされた認証情報
