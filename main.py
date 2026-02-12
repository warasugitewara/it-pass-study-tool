#!/usr/bin/env python3
"""
ITパスポート試験学習ツール - メインエントリーポイント
バージョン: 1.0.0
"""

import sys
import json
from pathlib import Path
from PySide6.QtWidgets import QApplication

from src.db.database import DatabaseManager
from src.db.models import Question
from src.ui.main_window import MainWindow
from src.utils.data_manager import get_data_manager

# バージョン情報
__version__ = "1.1.0"

def get_version() -> str:
    """アプリケーションバージョンを取得"""
    # PyInstaller 凍結EXE対応
    if getattr(sys, 'frozen', False):
        base_dir = Path(sys.executable).parent
    else:
        base_dir = Path(__file__).parent
    version_file = base_dir / "version.txt"
    if version_file.exists():
        return version_file.read_text().strip()
    return __version__


def get_sample_data_path() -> Path:
    """サンプルデータのパスを取得 - 10年分統合データ"""
    if getattr(sys, 'frozen', False):
        base_dir = Path(sys.executable).parent
        return base_dir / "resources" / "sample_data" / "all_questions_10years.json"
    else:
        return Path(__file__).parent / "resources" / "sample_data" / "all_questions_10years.json"


def load_sample_data():
    """サンプルデータをデータベースにロード"""
    db_manager = DatabaseManager()
    session = db_manager.get_session()
    
    try:
        existing_count = session.query(Question).count()
        if existing_count > 0:
            return
        
        sample_file = get_sample_data_path()
        if not sample_file.exists():
            print(f"⚠️  サンプルデータが見つかりません: {sample_file}")
            return
        
        print(f"📥 サンプルデータをロード中: {sample_file}")
        
        with open(sample_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        dm = get_data_manager()
        loaded_count = dm.bulk_add_questions(
            [q for q in data.get('questions', [])]
        )
        
        if loaded_count > 0:
            print(f"✅ {loaded_count}件の問題をロードしました")
    
    except Exception as e:
        print(f"⚠️  サンプルデータロードエラー: {e}")
    finally:
        db_manager.close_session(session)


def main():
    """アプリケーションメイン関数"""
    
    version = get_version()
    print(f"ITパスポート試験学習ツール v{version}")
    
    db_manager = DatabaseManager()
    db_manager.init_db()
    
    load_sample_data()
    
    app = QApplication(sys.argv)
    app.setApplicationVersion(version)
    app.setApplicationName("ITパスポート試験学習ツール")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
