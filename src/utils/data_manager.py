"""
データマネージャー - DB操作・問題管理
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import logging

from src.db import (
    get_db_manager, Question, Choice, Category, Year, 
    UserAnswer, Statistics, StudySession
)

logger = logging.getLogger(__name__)


class DataManager:
    """データベース操作管理クラス"""
    
    def __init__(self):
        self.db = get_db_manager()
    
    # ========================
    # Category 操作
    # ========================
    
    def get_or_create_category(self, name: str, description: str = None) -> Category:
        """カテゴリ取得または作成"""
        session = self.db.get_session()
        try:
            category = session.query(Category).filter_by(name=name).first()
            if not category:
                category = Category(name=name, description=description)
                session.add(category)
                session.commit()
                logger.info(f"カテゴリ作成: {name}")
            return category
        finally:
            self.db.close_session(session)
    
    def get_categories(self) -> List[Category]:
        """全カテゴリ取得"""
        session = self.db.get_session()
        try:
            return session.query(Category).all()
        finally:
            self.db.close_session(session)
    
    # ========================
    # Year 操作
    # ========================
    
    def get_or_create_year(self, year: int, season: str = None) -> Year:
        """年度取得または作成"""
        session = self.db.get_session()
        try:
            year_obj = session.query(Year).filter_by(year=year).first()
            if not year_obj:
                year_obj = Year(year=year, season=season)
                session.add(year_obj)
                session.commit()
                logger.info(f"年度作成: {year} {season}")
            return year_obj
        finally:
            self.db.close_session(session)
    
    def get_years(self) -> List[Year]:
        """全年度取得"""
        session = self.db.get_session()
        try:
            return session.query(Year).order_by(Year.year.desc()).all()
        finally:
            self.db.close_session(session)
    
    # ========================
    # Question 操作
    # ========================
    
    def add_question(self, question_data: Dict) -> Optional[Question]:
        """問題追加"""
        session = self.db.get_session()
        try:
            # カテゴリ・年度を別途セッションで取得/作成（セッション分離）
            category = self._get_or_create_category_internal(
                session, 
                question_data.get('category', 'テクノロジ')
            )
            year = self._get_or_create_year_internal(
                session,
                question_data.get('year', 2024),
                question_data.get('season', '春')
            )
            
            # 重複チェック
            existing = session.query(Question).filter(
                and_(
                    Question.category_id == category.id,
                    Question.year_id == year.id,
                    Question.question_number == question_data.get('question_number')
                )
            ).first()
            
            if existing:
                logger.warning(f"問題重複: {question_data.get('question_number')}")
                return None
            
            # 問題作成
            question = Question(
                question_number=question_data.get('question_number'),
                text=question_data.get('text'),
                explanation=question_data.get('explanation', ''),
                category_id=category.id,
                year_id=year.id,
                difficulty=question_data.get('difficulty', 2)
            )
            session.add(question)
            session.flush()  # IDを取得するためフラッシュ
            
            # 選択肢追加
            for idx, choice_text in enumerate(question_data.get('choices', []), 1):
                choice = Choice(
                    question_id=question.id,
                    choice_number=idx,
                    text=choice_text,
                    is_correct=(idx == question_data.get('correct_answer', 1))
                )
                session.add(choice)
            
            session.commit()
            logger.info(f"問題追加: {question.id}")
            return question
            
        except Exception as e:
            session.rollback()
            logger.error(f"問題追加エラー: {e}")
            return None
        finally:
            self.db.close_session(session)
    
    def _get_or_create_category_internal(self, session, name: str, description: str = None) -> Category:
        """セッション内でカテゴリ取得/作成"""
        category = session.query(Category).filter_by(name=name).first()
        if not category:
            category = Category(name=name, description=description)
            session.add(category)
            session.flush()
        return category
    
    def _get_or_create_year_internal(self, session, year: int, season: str = None) -> Year:
        """セッション内で年度取得/作成"""
        year_obj = session.query(Year).filter_by(year=year).first()
        if not year_obj:
            year_obj = Year(year=year, season=season)
            session.add(year_obj)
            session.flush()
        return year_obj
    
    def bulk_add_questions(self, questions_data: List[Dict]) -> int:
        """大量問題追加（Bulk Insert）"""
        count = 0
        for question_data in questions_data:
            if self.add_question(question_data):
                count += 1
        logger.info(f"大量追加完了: {count}/{len(questions_data)}件")
        return count
    
    def get_question_count(self) -> int:
        """問題総数取得"""
        session = self.db.get_session()
        try:
            return session.query(Question).count()
        finally:
            self.db.close_session(session)
    
    def get_questions(
        self,
        category_ids: List[int] = None,
        year_ids: List[int] = None,
        difficulty_min: int = 1,
        difficulty_max: int = 5,
        limit: int = 10
    ) -> List[Question]:
        """問題取得（フィルター付き）"""
        session = self.db.get_session()
        try:
            query = session.query(Question).filter(
                Question.is_active == True,
                Question.difficulty >= difficulty_min,
                Question.difficulty <= difficulty_max
            )
            
            if category_ids:
                query = query.filter(Question.category_id.in_(category_ids))
            
            if year_ids:
                query = query.filter(Question.year_id.in_(year_ids))
            
            return query.limit(limit).all()
        finally:
            self.db.close_session(session)
    
    def get_random_questions(
        self,
        count: int = 10,
        category_ids: List[int] = None,
        year_ids: List[int] = None
    ) -> List[Question]:
        """ランダムに問題取得"""
        import random
        session = self.db.get_session()
        try:
            query = session.query(Question).filter(Question.is_active == True)
            
            if category_ids:
                query = query.filter(Question.category_id.in_(category_ids))
            
            if year_ids:
                query = query.filter(Question.year_id.in_(year_ids))
            
            all_questions = query.all()
            return random.sample(all_questions, min(count, len(all_questions)))
        finally:
            self.db.close_session(session)
    
    # ========================
    # UserAnswer 操作
    # ========================
    
    def record_answer(
        self,
        question_id: int,
        selected_choice_id: int,
        session_id: str,
        time_spent_seconds: int = 0
    ) -> bool:
        """回答を記録"""
        session = self.db.get_session()
        try:
            # 選択肢が正解かチェック
            choice = session.query(Choice).filter_by(id=selected_choice_id).first()
            if not choice:
                return False
            
            user_answer = UserAnswer(
                question_id=question_id,
                selected_choice_id=selected_choice_id,
                is_correct=choice.is_correct,
                session_id=session_id,
                time_spent_seconds=time_spent_seconds
            )
            session.add(user_answer)
            session.commit()
            return True
        except Exception as e:
            logger.error(f"回答記録エラー: {e}")
            session.rollback()
            return False
        finally:
            self.db.close_session(session)
    
    def get_user_answers(self, session_id: str) -> List[UserAnswer]:
        """セッション内の回答取得"""
        session = self.db.get_session()
        try:
            return session.query(UserAnswer).filter_by(session_id=session_id).all()
        finally:
            self.db.close_session(session)
    
    # ========================
    # Statistics 操作
    # ========================
    
    def update_statistics(self, session_id: str) -> Optional[Statistics]:
        """統計情報を更新"""
        session = self.db.get_session()
        try:
            answers = session.query(UserAnswer).filter_by(session_id=session_id).all()
            
            if not answers:
                return None
            
            correct_count = sum(1 for a in answers if a.is_correct)
            total_count = len(answers)
            correct_rate = (correct_count / total_count * 100) if total_count > 0 else 0
            
            # グローバル統計更新
            stats = session.query(Statistics).first()
            if not stats:
                stats = Statistics()
            
            stats.total_questions_answered = total_count
            stats.total_correct = correct_count
            stats.correct_rate = correct_rate
            stats.last_studied_at = datetime.utcnow()
            
            session.add(stats)
            session.commit()
            return stats
        except Exception as e:
            logger.error(f"統計更新エラー: {e}")
            session.rollback()
            return None
        finally:
            self.db.close_session(session)
    
    def get_statistics(self) -> Optional[Statistics]:
        """統計情報取得"""
        session = self.db.get_session()
        try:
            stats = session.query(Statistics).first()
            if not stats:
                stats = Statistics()
                session.add(stats)
                session.commit()
            return stats
        finally:
            self.db.close_session(session)
    
    def get_category_statistics(self, category_id: int) -> Dict:
        """分野別統計"""
        session = self.db.get_session()
        try:
            answers = session.query(UserAnswer).join(Question).filter(
                Question.category_id == category_id
            ).all()
            
            if not answers:
                return {"total": 0, "correct": 0, "rate": 0}
            
            correct = sum(1 for a in answers if a.is_correct)
            total = len(answers)
            
            return {
                "total": total,
                "correct": correct,
                "rate": (correct / total * 100) if total > 0 else 0
            }
        finally:
            self.db.close_session(session)


# グローバルインスタンス
_data_manager = None


def get_data_manager() -> DataManager:
    """グローバルデータマネージャー取得"""
    global _data_manager
    if _data_manager is None:
        _data_manager = DataManager()
    return _data_manager
