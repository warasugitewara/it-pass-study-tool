#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyInstaller ビルドスクリプト
Python アプリケーションを単一の EXE ファイルに変換
"""

import os
import sys
import subprocess
from pathlib import Path

# Windows コンソール出力のエンコーディング設定
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# プロジェクトディレクトリ
PROJECT_DIR = Path(__file__).parent
MAIN_SCRIPT = PROJECT_DIR / "main.py"
SRC_DIR = PROJECT_DIR / "src"
DIST_DIR = PROJECT_DIR / "dist"
BUILD_DIR = PROJECT_DIR / "build"
ICON_PATH = PROJECT_DIR / "resources" / "icons" / "app.ico"
APP_NAME = "it-pass-study-tool"

def get_hidden_imports():
    """
    PyInstaller で検出されない隠れたインポートを指定
    """
    hidden_imports = [
        # PySide6 関連
        "PySide6",
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtWidgets",
        "PySide6.QtSql",
        
        # SQLAlchemy 関連
        "sqlalchemy",
        "sqlalchemy.orm",
        "sqlalchemy.sql",
        
        # その他の依存ライブラリ
        "pandas",
        "numpy",
        "openpyxl",
        "requests",
        "bs4",
        "lxml",
        "matplotlib",
        "apscheduler",
        "apscheduler.schedulers.background",
        "apscheduler.triggers.cron",
        "apscheduler.triggers.interval",
        
        # プロジェクトの src モジュール
        "src",
        "src.db",
        "src.db.database",
        "src.db.models",
        "src.ui",
        "src.ui.main_window",
        "src.ui.quiz_widget",
        "src.ui.quiz_config_dialog",
        "src.ui.admin_panel",
        "src.ui.results_widget",
        "src.ui.styles",
        "src.core",
        "src.core.quiz_engine",
        "src.core.statistics",
        "src.utils",
        "src.utils.config",
        "src.utils.data_manager",
        "src.utils.scraper",
        "src.utils.scraper_scheduler",
    ]
    return hidden_imports


def build_exe():
    """
    PyInstaller を実行して EXE ファイルをビルド
    """
    print(f"🔨 {APP_NAME} の EXE ビルドを開始します...\n")
    
    # ビルドディレクトリのクリーンアップ（オプション）
    if BUILD_DIR.exists():
        print(f"  • 既存のビルドディレクトリをクリーンアップ中...")
        import shutil
        shutil.rmtree(BUILD_DIR)
    
    # PyInstaller コマンド構築
    pyinstaller_cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name", APP_NAME,
        "--onefile",           # 単一の EXE ファイルに統合
        "--windowed",          # コンソール非表示
        "--distpath", str(DIST_DIR),
        "--workpath", str(BUILD_DIR),
        "--specpath", str(PROJECT_DIR),
    ]
    
    # hidden imports を追加
    for hidden_import in get_hidden_imports():
        pyinstaller_cmd.extend(["--hidden-import", hidden_import])
    
    # アイコンを追加（存在する場合）
    if ICON_PATH.exists():
        pyinstaller_cmd.extend(["--icon", str(ICON_PATH)])
        print(f"  • アイコンを使用: {ICON_PATH}")
    else:
        print(f"  ⚠️  アイコンが見つかりません (オプション): {ICON_PATH}")
    
    # リソースディレクトリを追加
    if (PROJECT_DIR / "resources").exists():
        pyinstaller_cmd.extend(["--add-data", f"{PROJECT_DIR / 'resources'};resources"])
        print(f"  • リソースディレクトリを追加")
    
    # version.txt を追加
    if (PROJECT_DIR / "version.txt").exists():
        pyinstaller_cmd.extend(["--add-data", f"{PROJECT_DIR / 'version.txt'};."])
        print(f"  • version.txt を追加")
    
    # メインスクリプトを追加
    pyinstaller_cmd.append(str(MAIN_SCRIPT))
    
    print(f"\n📦 PyInstaller コマンドを実行中...")
    print(f"  コマンド: {' '.join(pyinstaller_cmd)}\n")
    
    try:
        # PyInstaller を実行
        result = subprocess.run(
            pyinstaller_cmd,
            cwd=str(PROJECT_DIR),
            capture_output=False,
            text=True,
        )
        
        if result.returncode != 0:
            print(f"\n❌ PyInstaller ビルドが失敗しました (Exit Code: {result.returncode})")
            return False
        
        print(f"\n✅ PyInstaller ビルドが完了しました")
        return True
        
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        return False


def verify_build():
    """
    ビルド結果の検証
    """
    exe_path = DIST_DIR / f"{APP_NAME}.exe"
    
    print(f"\n🔍 ビルド結果を検証中...\n")
    
    if exe_path.exists():
        file_size = exe_path.stat().st_size / (1024 * 1024)  # MB
        print(f"✅ EXE ファイルが正常に生成されました")
        print(f"   場所: {exe_path}")
        print(f"   サイズ: {file_size:.2f} MB")
        return True
    else:
        print(f"❌ EXE ファイルが見つかりません")
        print(f"   予想パス: {exe_path}")
        
        # dist ディレクトリの内容を表示
        if DIST_DIR.exists():
            print(f"\n   {DIST_DIR} の内容:")
            for item in DIST_DIR.iterdir():
                print(f"   - {item.name}")
        
        return False


def main():
    """
    メイン処理
    """
    print("=" * 60)
    print(f"PyInstaller EXE ビルドスクリプト")
    print("=" * 60)
    
    # プロジェクトディレクトリの確認
    if not MAIN_SCRIPT.exists():
        print(f"\n❌ エラー: main.py が見つかりません")
        print(f"   パス: {MAIN_SCRIPT}")
        sys.exit(1)
    
    print(f"\nプロジェクト情報:")
    print(f"  プロジェクトディレクトリ: {PROJECT_DIR}")
    print(f"  メインスクリプト: {MAIN_SCRIPT.name}")
    print(f"  出力ディレクトリ: {DIST_DIR}\n")
    
    # EXE のビルド
    if not build_exe():
        sys.exit(1)
    
    # ビルド結果の検証
    if not verify_build():
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✨ ビルドが成功しました！")
    print("=" * 60)
    sys.exit(0)


if __name__ == "__main__":
    main()
