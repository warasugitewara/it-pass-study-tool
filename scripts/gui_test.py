#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GUI テスト スクリプト
アプリケーション起動と基本的な UI コンポーネント の動作確認
"""

import sys
import logging
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QTimer

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

print("\n")
print("╔═══════════════════════════════════════════════════════════╗")
print("║  ITパスポート学習ツール - GUI テスト                      ║")
print("╚═══════════════════════════════════════════════════════════╝")
print()

# テスト 1: モジュール読み込みテスト
print("=" * 61)
print("テスト 1: PySide6 モジュール読み込み")
print("=" * 61)

try:
    from src.db.database import DatabaseManager
    from src.utils.data_manager import DataManager
    from src.core.quiz_engine import QuizEngine
    from src.ui.main_window import MainWindow
    from src.utils.config import get_db_manager, get_quiz_engine
    
    logger.info("✓ すべての UI/コア モジュール読み込み成功")
    print()
except ImportError as e:
    logger.error(f"✗ モジュール読み込み失敗: {e}")
    sys.exit(1)

# テスト 2: QApplication 初期化
print("=" * 61)
print("テスト 2: QApplication 初期化")
print("=" * 61)

try:
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    logger.info("✓ QApplication 初期化成功")
    print()
except Exception as e:
    logger.error(f"✗ QApplication 初期化失敗: {e}")
    sys.exit(1)

# テスト 3: データベース初期化
print("=" * 61)
print("テスト 3: データベース初期化")
print("=" * 61)

try:
    db_manager = get_db_manager()
    logger.info(f"✓ データベース初期化成功")
    
    session = db_manager.get_session()
    logger.info(f"✓ セッション取得成功")
    
    # データベース状態確認
    from src.db.models import Question, Category, Year
    
    q_count = session.query(Question).count()
    c_count = session.query(Category).count()
    y_count = session.query(Year).count()
    
    logger.info(f"  - 問題数: {q_count}問")
    logger.info(f"  - カテゴリ数: {c_count}個")
    logger.info(f"  - 年度数: {y_count}個")
    
    print()
except Exception as e:
    logger.error(f"✗ データベース初期化失敗: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# テスト 4: MainWindow 作成テスト
print("=" * 61)
print("テスト 4: MainWindow 作成テスト")
print("=" * 61)

try:
    window = MainWindow()
    logger.info("✓ MainWindow 作成成功")
    
    # ウィンドウプロパティ確認
    logger.info(f"  - ウィンドウタイトル: {window.windowTitle()}")
    logger.info(f"  - ウィンドウサイズ: {window.width()} x {window.height()}")
    logger.info(f"  - ウィンドウ状態: {'表示可能' if window.isVisible() == False else '表示中'}")
    
    print()
except Exception as e:
    logger.error(f"✗ MainWindow 作成失敗: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# テスト 5: クイズエンジン連携テスト
print("=" * 61)
print("テスト 5: クイズエンジン連携テスト")
print("=" * 61)

try:
    quiz_engine = get_quiz_engine()
    
    logger.info("✓ クイズエンジン取得成功")
    
    # エンジン状態確認
    logger.info(f"  - クイズエンジン準備: OK")
    
    print()
except Exception as e:
    logger.error(f"✗ クイズエンジン連携失敗: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# テスト 6: スタイルシート読み込み
print("=" * 61)
print("テスト 6: スタイルシート読み込み")
print("=" * 61)

try:
    from src.ui.styles import get_stylesheet
    
    stylesheet = get_stylesheet()
    logger.info("✓ スタイルシート読み込み成功")
    logger.info(f"  - シート長: {len(stylesheet)} 文字")
    
    app.setStyle('Fusion')
    logger.info("✓ Fusion スタイル適用成功")
    
    print()
except Exception as e:
    logger.error(f"✗ スタイルシート読み込み失敗: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# テスト 7: ウィンドウ表示テスト（短時間）
print("=" * 61)
print("テスト 7: ウィンドウ表示テスト")
print("=" * 61)

try:
    window.show()
    logger.info("✓ ウィンドウ show() 呼び出し成功")
    
    # 1秒後に閉じる
    QTimer.singleShot(1000, window.close)
    logger.info("✓ 1秒後に自動クローズをスケジュール")
    
    # イベントループ実行（最大3秒）
    logger.info("ℹ️  イベントループ実行中...")
    
    start_time = app.sendPostedEvents.__self__().elapsedTimer() if hasattr(app, 'elapsedTimer') else 0
    app.exec()
    
    logger.info("✓ ウィンドウ表示テスト完了")
    print()
except Exception as e:
    logger.error(f"✗ ウィンドウ表示テスト失敗: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# テスト結果サマリー
print("=" * 61)
print("テスト結果サマリー")
print("=" * 61)

print("✓ テスト 1: PySide6 モジュール読み込み      成功")
print("✓ テスト 2: QApplication 初期化           成功")
print("✓ テスト 3: データベース初期化            成功")
print("✓ テスト 4: MainWindow 作成              成功")
print("✓ テスト 5: クイズエンジン連携           成功")
print("✓ テスト 6: スタイルシート読み込み        成功")
print("✓ テスト 7: ウィンドウ表示               成功")
print()
print(f"合計: 7/7 成功")
print()

print("╔═══════════════════════════════════════════════════════════╗")
print("║          ✅ GUI テスト完了 - すべて成功！               ║")
print("╚═══════════════════════════════════════════════════════════╝")
print()
print("✅ アプリケーション起動に必要なすべてのコンポーネント")
print("   が正常に初期化されました！")
print()
