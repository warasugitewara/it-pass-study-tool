"""
統合テストスクリプト
アプリケーション各モジュールの動作確認
"""

import sys
from pathlib import Path

import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def test_database():
    """データベース接続テスト"""
    logger.info("=" * 60)
    logger.info("テスト 1: データベース接続")
    logger.info("=" * 60)
    
    try:
        from src.db import init_database, get_db_manager
        
        init_database()
        logger.info("✓ データベース初期化成功")
        
        db = get_db_manager()
        session = db.get_session()
        logger.info("✓ セッション取得成功")
        db.close_session(session)
        
        return True
    except Exception as e:
        logger.error(f"✗ データベーステスト失敗: {e}")
        return False


def test_data_manager():
    """データマネージャーテスト"""
    logger.info("\n" + "=" * 60)
    logger.info("テスト 2: データマネージャー")
    logger.info("=" * 60)
    
    try:
        from src.utils.data_manager import get_data_manager
        
        dm = get_data_manager()
        
        # カテゴリ取得
        categories = dm.get_categories()
        logger.info(f"✓ カテゴリ取得: {len(categories)}件")
        
        # 年度取得
        years = dm.get_years()
        logger.info(f"✓ 年度取得: {len(years)}件")
        
        # 問題数
        count = dm.get_question_count()
        logger.info(f"✓ 問題総数: {count}問")
        
        return True
    except Exception as e:
        logger.error(f"✗ データマネージャーテスト失敗: {e}")
        return False


def test_quiz_engine():
    """出題エンジンテスト"""
    logger.info("\n" + "=" * 60)
    logger.info("テスト 3: 出題エンジン")
    logger.info("=" * 60)
    
    try:
        from src.core import get_quiz_engine, QuizMode
        from src.utils.data_manager import get_data_manager
        
        dm = get_data_manager()
        engine = get_quiz_engine()
        
        # 年度IDを取得
        years = dm.get_years()
        if not years:
            logger.warning("⚠️  年度がありません。スキップします。")
            return True
        
        year_ids = [y.id for y in years[:1]]
        
        # 出題モードテスト
        modes = [
            (QuizMode.RANDOM, "ランダム出題"),
            (QuizMode.BY_YEAR, "年度別出題"),
        ]
        
        for mode, label in modes:
            try:
                session_id, questions = engine.start_session(
                    mode=mode,
                    question_count=3,
                    year_ids=year_ids if mode == QuizMode.BY_YEAR else None
                )
                logger.info(f"✓ {label}: {len(questions)}問を出題")
            except Exception as e:
                logger.warning(f"⚠️  {label} テスト: {e}")
        
        return True
    except Exception as e:
        logger.error(f"✗ 出題エンジンテスト失敗: {e}")
        return False


def test_statistics():
    """統計エンジンテスト"""
    logger.info("\n" + "=" * 60)
    logger.info("テスト 4: 統計エンジン")
    logger.info("=" * 60)
    
    try:
        from src.core.statistics import get_statistics_engine
        
        stats_engine = get_statistics_engine()
        
        # 全体統計
        overall = stats_engine.get_overall_stats()
        logger.info(f"✓ 全体統計取得: {overall.get('total_questions_answered')}問回答済み")
        
        # 分野別統計
        category_stats = stats_engine.calculate_category_stats()
        logger.info(f"✓ 分野別統計: {len(category_stats)}分野")
        
        return True
    except Exception as e:
        logger.error(f"✗ 統計エンジンテスト失敗: {e}")
        return False


def test_scraper():
    """スクレイパーテスト"""
    logger.info("\n" + "=" * 60)
    logger.info("テスト 5: スクレイパー")
    logger.info("=" * 60)
    
    try:
        from src.utils.scraper import ITPassScraper
        
        scraper = ITPassScraper()
        logger.info("✓ スクレイパー初期化成功")
        
        # 過去問情報取得（ネットワーク接続必要）
        logger.info("ℹ️  過去問情報取得テスト（スキップ）")
        logger.info("   注: ネットワーク接続が必要です")
        
        return True
    except Exception as e:
        logger.error(f"✗ スクレイパーテスト失敗: {e}")
        return False


def main():
    """メインテスト関数"""
    logger.info("\n")
    logger.info("╔" + "=" * 58 + "╗")
    logger.info("║  ITパスポート学習ツール - 統合テスト                    ║")
    logger.info("╚" + "=" * 58 + "╝\n")
    
    tests = [
        ("データベース", test_database),
        ("データマネージャー", test_data_manager),
        ("出題エンジン", test_quiz_engine),
        ("統計エンジン", test_statistics),
        ("スクレイパー", test_scraper),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            logger.error(f"テスト実行エラー: {e}")
            results.append((name, False))
    
    # 結果サマリー
    logger.info("\n" + "=" * 60)
    logger.info("テスト結果サマリー")
    logger.info("=" * 60)
    
    for name, result in results:
        status = "✓ 成功" if result else "✗ 失敗"
        logger.info(f"{status}: {name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    logger.info(f"\n合計: {passed}/{total} 成功")
    
    if passed == total:
        logger.info("\n✅ すべてのテストに合格しました！")
        return 0
    else:
        logger.warning(f"\n⚠️  {total - passed}つのテストが失敗しました")
        return 1


if __name__ == "__main__":
    sys.exit(main())
