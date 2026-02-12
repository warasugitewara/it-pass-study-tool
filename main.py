#!/usr/bin/env python3
"""
ITパスポート試験学習ツール - メインエントリーポイント
"""

import sys
from PyQt6.QtWidgets import QApplication

from src.db import init_database
from src.ui import MainWindow


def main():
    """アプリケーションメイン関数"""
    
    # データベース初期化
    init_database()
    
    # PyQt6アプリケーション作成
    app = QApplication(sys.argv)
    
    # メインウィンドウ作成・表示
    window = MainWindow()
    window.show()
    
    # アプリケーション実行
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
