"""
出題エンジン - 各種出題モードの実装
"""

from typing import List, Tuple, Optional
from enum import Enum
import random
import uuid
from datetime import datetime
import logging

from src.utils.data_manager import get_data_manager
from src.db import Question, StudySession, UserAnswer

logger = logging.getLogger(__name__)


class QuizMode(Enum):
    """出題モード"""
    RANDOM = "random"          # ランダム出題
    BY_YEAR = "by_year"        # 年度別
    BY_CATEGORY = "by_category"  # 分野別
    REVIEW = "review"          # 復習モード
    MOCK_TEST = "mock_test"    # 模擬試験


class QuizEngine:
    """出題エンジン"""
    
    DEFAULT_QUESTION_COUNT = 10
    MOCK_TEST_QUESTION_COUNT = 100  # ITパスポート試験の標準問題数
    
    def __init__(self):
        self.dm = get_data_manager()
        self.current_session_id = None
        self.current_questions: List[Question] = []
        self.current_question_index = 0
    
    def start_session(
        self,
        mode: QuizMode,
        question_count: int = None,
        category_ids: List[int] = None,
        year_ids: List[int] = None,
        difficulty_range: Tuple[int, int] = (1, 5)
    ) -> Tuple[str, List[Question]]:
        """
        学習セッション開始
        
        Args:
            mode: 出題モード
            question_count: 出題数（Noneの場合はモードのデフォルト値）
            category_ids: 対象分野ID リスト
            year_ids: 対象年度ID リスト
            difficulty_range: 難易度範囲 (最小, 最大)
        
        Returns:
            (session_id, questions)
        """
        # セッションID生成
        self.current_session_id = str(uuid.uuid4())
        
        # 出題数決定
        if question_count is None:
            question_count = (
                self.MOCK_TEST_QUESTION_COUNT
                if mode == QuizMode.MOCK_TEST
                else self.DEFAULT_QUESTION_COUNT
            )
        
        # モードに応じて問題取得
        if mode == QuizMode.RANDOM:
            self.current_questions = self._get_random_questions(
                question_count, category_ids, year_ids, difficulty_range
            )
        
        elif mode == QuizMode.BY_YEAR:
            self.current_questions = self._get_questions_by_year(
                question_count, year_ids, difficulty_range
            )
        
        elif mode == QuizMode.BY_CATEGORY:
            self.current_questions = self._get_questions_by_category(
                question_count, category_ids, difficulty_range
            )
        
        elif mode == QuizMode.REVIEW:
            self.current_questions = self._get_review_questions(
                question_count, category_ids, difficulty_range
            )
        
        elif mode == QuizMode.MOCK_TEST:
            self.current_questions = self._get_mock_test_questions(
                difficulty_range
            )
        
        # セッション情報をDBに記録
        self._create_study_session(mode, category_ids, year_ids)
        
        self.current_question_index = 0
        logger.info(
            f"セッション開始: {self.current_session_id} "
            f"(モード: {mode.value}, 問題数: {len(self.current_questions)})"
        )
        
        return self.current_session_id, self.current_questions
    
    def _get_random_questions(
        self,
        count: int,
        category_ids: List[int],
        year_ids: List[int],
        difficulty_range: Tuple[int, int]
    ) -> List[Question]:
        """ランダム出題"""
        return self.dm.get_random_questions(
            count=count,
            category_ids=category_ids,
            year_ids=year_ids
        )
    
    def _get_questions_by_year(
        self,
        count: int,
        year_ids: List[int],
        difficulty_range: Tuple[int, int]
    ) -> List[Question]:
        """年度別出題"""
        return self.dm.get_random_questions(
            count=count,
            year_ids=year_ids
        )
    
    def _get_questions_by_category(
        self,
        count: int,
        category_ids: List[int],
        difficulty_range: Tuple[int, int]
    ) -> List[Question]:
        """分野別出題"""
        return self.dm.get_random_questions(
            count=count,
            category_ids=category_ids
        )
    
    def _get_review_questions(
        self,
        count: int,
        category_ids: List[int],
        difficulty_range: Tuple[int, int]
    ) -> List[Question]:
        """
        復習モード - 正答率が低い問題を優先出題
        
        実装方針:
        1. ユーザーが回答した問題を取得
        2. 正答率が低い順にソート
        3. 下位N件を復習問題として出題
        """
        # TODO: 実装予定
        # 暫定的にランダムで返す
        return self.dm.get_random_questions(count=count)
    
    def _get_mock_test_questions(
        self,
        difficulty_range: Tuple[int, int]
    ) -> List[Question]:
        """模擬試験形式（100問）"""
        return self.dm.get_random_questions(
            count=self.MOCK_TEST_QUESTION_COUNT
        )
    
    def _create_study_session(
        self,
        mode: QuizMode,
        category_ids: List[int],
        year_ids: List[int]
    ):
        """学習セッション情報を DB に記録"""
        session = self.dm.db.get_session()
        try:
            study_session = StudySession(
                session_id=self.current_session_id,
                mode=mode.value,
                category_id=category_ids[0] if category_ids else None,
                year_id=year_ids[0] if year_ids else None,
                total_questions=len(self.current_questions),
                start_time=datetime.utcnow()
            )
            session.add(study_session)
            session.commit()
        except Exception as e:
            logger.error(f"セッション記録エラー: {e}")
            session.rollback()
        finally:
            self.dm.db.close_session(session)
    
    def get_current_question(self) -> Optional[Question]:
        """現在の問題を取得"""
        if self.current_question_index < len(self.current_questions):
            return self.current_questions[self.current_question_index]
        return None
    
    def get_question_count(self) -> int:
        """総問題数"""
        return len(self.current_questions)
    
    def get_current_index(self) -> int:
        """現在の問題番号（0ベース）"""
        return self.current_question_index
    
    def next_question(self) -> bool:
        """次の問題へ（成功時 True）"""
        if self.current_question_index < len(self.current_questions) - 1:
            self.current_question_index += 1
            return True
        return False
    
    def previous_question(self) -> bool:
        """前の問題へ（成功時 True）"""
        if self.current_question_index > 0:
            self.current_question_index -= 1
            return True
        return False
    
    def submit_answer(
        self,
        choice_id: int,
        time_spent_seconds: int = 0
    ) -> bool:
        """
        回答を提出
        
        Args:
            choice_id: 選択した選択肢ID
            time_spent_seconds: 回答に費やした時間（秒）
        
        Returns: 成功時 True
        """
        if not self.current_session_id:
            logger.error("セッションが開始されていません")
            return False
        
        question = self.get_current_question()
        if not question:
            logger.error("問題が見つかりません")
            return False
        
        return self.dm.record_answer(
            question.id,
            choice_id,
            self.current_session_id,
            time_spent_seconds
        )
    
    def finish_session(self) -> dict:
        """
        セッション終了・結果を取得
        
        Returns:
            {
                "session_id": "...",
                "total_questions": 10,
                "correct_count": 7,
                "correct_rate": 70.0,
                "elapsed_time": 300  # 秒
            }
        """
        if not self.current_session_id:
            return {}
        
        # 回答情報を集計
        session = self.dm.db.get_session()
        try:
            answers = session.query(UserAnswer).filter_by(
                session_id=self.current_session_id
            ).all()
            
            if not answers:
                return {}
            
            correct_count = sum(1 for a in answers if a.is_correct)
            total_count = len(answers)
            correct_rate = (correct_count / total_count * 100) if total_count > 0 else 0
            
            # セッション情報を更新
            study_session = session.query(StudySession).filter_by(
                session_id=self.current_session_id
            ).first()
            
            if study_session:
                study_session.correct_count = correct_count
                study_session.end_time = datetime.utcnow()
                session.commit()
            
            # 統計を更新
            self.dm.update_statistics(self.current_session_id)
            
            return {
                "session_id": self.current_session_id,
                "total_questions": total_count,
                "correct_count": correct_count,
                "correct_rate": correct_rate,
                "elapsed_time": sum(a.time_spent_seconds or 0 for a in answers)
            }
        
        except Exception as e:
            logger.error(f"セッション終了エラー: {e}")
            return {}
        finally:
            self.dm.db.close_session(session)


# グローバルインスタンス
_quiz_engine = None


def get_quiz_engine() -> QuizEngine:
    """グローバル出題エンジン取得"""
    global _quiz_engine
    if _quiz_engine is None:
        _quiz_engine = QuizEngine()
    return _quiz_engine
