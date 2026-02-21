"""ファイル操作Hello World用サンプル"""


def add(a, b):
    """2つの数を足す（バグあり）"""
    return a - b  # BUG: should be a + b


def greet():
    """挨拶を返す（未実装: name引数を追加してほしい）"""
    return "Hello, World!"


def multiply(a, b):
    """2つの数を掛ける"""
    return a * b
