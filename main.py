#!/usr/bin/env python3
"""
ITパスポート試験学習ツール - メインエントリーポイント
バージョン: 1.0.0
"""

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

from src.db.database import DatabaseManager
from src.ui.main_window import MainWindow

# バージョン情報
__version__ = "1.0.0"

def get_version() -> str:
    """アプリケーションバージョンを取得"""
    version_file = Path(__file__).parent / "version.txt"
    if version_file.exists():
        return version_file.read_text().strip()
    return __version__


def main():
    """アプリケーションメイン関数"""
    
    # バージョン情報を表示（オプション）
    version = get_version()
    print(f"ITパスポート試験学習ツール v{version}")
    
    # データベース初期化
    db_manager = DatabaseManager()
    
    # PySide6アプリケーション作成
    app = QApplication(sys.argv)
    app.setApplicationVersion(version)
    app.setApplicationName("ITパスポート試験学習ツール")
    
    # メインウィンドウ作成・表示
    window = MainWindow()
    window.show()
    
    # アプリケーション実行
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
