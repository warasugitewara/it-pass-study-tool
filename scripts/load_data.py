"""
初期データロードスクリプト
サンプルデータまたはスクレイピングデータをDBに登録
"""

import json
import logging
from pathlib import Path
import sys

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.db import init_database
from src.utils.data_manager import get_data_manager
from src.utils.scraper import ITPassScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_sample_data():
    """サンプルデータを DB にロード"""
    
    dm = get_data_manager()
    
    # サンプルデータファイルパス
    sample_dir = Path(__file__).parent.parent / "resources" / "sample_data"
    json_file = sample_dir / "sample_questions_2024_spring.json"
    
    if not json_file.exists():
        logger.warning(f"サンプルファイルが見つかりません: {json_file}")
        return False
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        year = data.get('year', 2024)
        season = data.get('season', '春')
        
        logger.info(f"ロード対象: {year}年 {season} - {len(data.get('questions', []))}問")
        
        # 問題を追加
        questions_data = []
        for q in data.get('questions', []):
            question_data = {
                'year': year,
                'season': season,
                'question_number': q.get('question_number'),
                'category': q.get('category', 'テクノロジ'),
                'text': q.get('text'),
                'choices': q.get('choices', []),
                'correct_answer': q.get('correct_answer', 1),
                'explanation': q.get('explanation', ''),
                'difficulty': q.get('difficulty', 2)
            }
            questions_data.append(question_data)
        
        count = dm.bulk_add_questions(questions_data)
        logger.info(f"✓ {count}件の問題をロード完了")
        return True
    
    except Exception as e:
        logger.error(f"データロードエラー: {e}")
        return False


def scrape_and_load_data():
    """
    スクレイピングでデータをロード
    
    ⚠️ 注意: 利用規約を確認の上、実行してください
    """
    
    logger.warning("スクレイピングを開始します...")
    logger.warning("対象サイトの利用規約を確認してください")
    
    scraper = ITPassScraper()
    dm = get_data_manager()
    
    try:
        # 過去問情報を取得
        exams = scraper.get_past_exams()
        logger.info(f"取得した過去問試験: {len(exams)}件")
        
        # 最初の試験から問題を取得（テスト用）
        if not exams:
            logger.error("過去問情報が取得できません")
            return False
        
        exam = exams[0]
        logger.info(f"スクレイピング対象: {exam}")
        
        questions = scraper.get_questions_from_exam(exam['url'])
        logger.info(f"取得した問題: {len(questions)}件")
        
        # データ検証
        valid_questions = [q for q in questions if scraper.validate_question(q)]
        logger.info(f"検証済み問題: {len(valid_questions)}件")
        
        # DB に登録
        for q in valid_questions:
            q['year'] = exam.get('year', 2024)
            q['season'] = exam.get('season', '春')
        
        count = dm.bulk_add_questions(valid_questions)
        logger.info(f"✓ {count}件をロード完了")
        return True
    
    except Exception as e:
        logger.error(f"スクレイピングエラー: {e}")
        return False


if __name__ == "__main__":
    # データベース初期化
    init_database()
    
    if len(sys.argv) > 1 and sys.argv[1] == 'scrape':
        # スクレイピングモード
        scrape_and_load_data()
    else:
        # サンプルデータロードモード（デフォルト）
        load_sample_data()
    
    # ロード確認
    dm = get_data_manager()
    count = dm.get_question_count()
    logger.info(f"\n===== ロード完了 =====")
    logger.info(f"データベース内の問題総数: {count}問")
