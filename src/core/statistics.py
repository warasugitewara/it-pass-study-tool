"""
統計・分析モジュール
学習進捗と成績の計算・分析
"""

from typing import Dict, List, Tuple
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

from src.db import get_db_manager, UserAnswer, Question, Category

logger = logging.getLogger(__name__)


class StatisticsEngine:
    """統計計算エンジン"""
    
    def __init__(self):
        self.db = get_db_manager()
    
    def calculate_session_stats(self, session_id: str) -> Dict:
        """セッション統計を計算"""
        session = self.db.get_session()
        try:
            answers = session.query(UserAnswer).filter_by(
                session_id=session_id
            ).all()
            
            if not answers:
                return {
                    "session_id": session_id,
                    "total_questions": 0,
                    "correct_count": 0,
                    "incorrect_count": 0,
                    "unanswered_count": 0,
                    "correct_rate": 0.0,
                    "elapsed_time": 0,
                    "average_time_per_question": 0
                }
            
            total = len(answers)
            correct = sum(1 for a in answers if a.is_correct == True)
            incorrect = sum(1 for a in answers if a.is_correct == False)
            unanswered = sum(1 for a in answers if a.is_correct is None)
            
            elapsed_time = sum(a.time_spent_seconds or 0 for a in answers)
            avg_time = elapsed_time / total if total > 0 else 0
            
            return {
                "session_id": session_id,
                "total_questions": total,
                "correct_count": correct,
                "incorrect_count": incorrect,
                "unanswered_count": unanswered,
                "correct_rate": (correct / total * 100) if total > 0 else 0,
                "elapsed_time": elapsed_time,
                "average_time_per_question": avg_time
            }
        finally:
            self.db.close_session(session)
    
    def calculate_category_stats(self, category_id: int = None) -> Dict:
        """
        分野別統計を計算
        
        Args:
            category_id: None の場合は全分野を集計
        
        Returns:
            {
                "category_name": "テクノロジ",
                "total_questions": 150,
                "correct_count": 120,
                "correct_rate": 80.0,
                "attempt_count": 5  # その分野を解いた回数
            }
        """
        session = self.db.get_session()
        try:
            query = session.query(UserAnswer).join(Question)
            
            if category_id:
                query = query.filter(Question.category_id == category_id)
            
            answers = query.all()
            
            if not answers:
                return {}
            
            stats_by_category = {}
            
            for answer in answers:
                cat_name = answer.question.category.name
                
                if cat_name not in stats_by_category:
                    stats_by_category[cat_name] = {
                        "category_name": cat_name,
                        "total_questions": 0,
                        "correct_count": 0,
                        "attempt_count": 0
                    }
                
                stats_by_category[cat_name]["total_questions"] += 1
                if answer.is_correct:
                    stats_by_category[cat_name]["correct_count"] += 1
            
            # 正答率を計算
            for cat_stats in stats_by_category.values():
                total = cat_stats["total_questions"]
                correct = cat_stats["correct_count"]
                cat_stats["correct_rate"] = (correct / total * 100) if total > 0 else 0
            
            return stats_by_category
        
        finally:
            self.db.close_session(session)
    
    def get_overall_stats(self) -> Dict:
        """全体統計を取得"""
        session = self.db.get_session()
        try:
            answers = session.query(UserAnswer).all()
            
            if not answers:
                return {
                    "total_questions_answered": 0,
                    "total_correct": 0,
                    "correct_rate": 0.0,
                    "total_study_time": 0,
                    "study_sessions": 0
                }
            
            total = len(answers)
            correct = sum(1 for a in answers if a.is_correct == True)
            total_time = sum(a.time_spent_seconds or 0 for a in answers)
            
            # セッション数
            sessions = set(a.session_id for a in answers if a.session_id)
            
            return {
                "total_questions_answered": total,
                "total_correct": correct,
                "correct_rate": (correct / total * 100) if total > 0 else 0,
                "total_study_time": total_time,
                "study_sessions": len(sessions)
            }
        finally:
            self.db.close_session(session)
    
    def get_weak_points(self, threshold_rate: float = 60.0) -> List[Dict]:
        """
        弱点を取得（正答率が低い問題）
        
        Args:
            threshold_rate: この正答率以下の問題を弱点と判定（%）
        
        Returns:
            [
                {"question_id": 1, "text": "...", "correct_rate": 30.0, "attempt_count": 10},
                ...
            ]
        """
        session = self.db.get_session()
        try:
            # 問題ごとの正答率を計算
            questions = session.query(Question).all()
            weak_points = []
            
            for question in questions:
                answers = session.query(UserAnswer).filter_by(
                    question_id=question.id
                ).all()
                
                if not answers:
                    continue
                
                total = len(answers)
                correct = sum(1 for a in answers if a.is_correct == True)
                correct_rate = (correct / total * 100) if total > 0 else 0
                
                if correct_rate < threshold_rate:
                    weak_points.append({
                        "question_id": question.id,
                        "text": question.text[:50],  # 最初の50文字
                        "category": question.category.name,
                        "correct_rate": correct_rate,
                        "attempt_count": total,
                        "correct_count": correct
                    })
            
            # 正答率でソート（低い順）
            weak_points.sort(key=lambda x: x['correct_rate'])
            
            return weak_points[:10]  # 上位10問の弱点
        
        finally:
            self.db.close_session(session)
    
    def get_learning_trend(self, days: int = 7) -> List[Dict]:
        """
        学習トレンドを取得（日別正答率推移）
        
        Args:
            days: 過去N日間のデータを取得
        
        Returns:
            [
                {"date": "2026-02-12", "correct_rate": 75.0, "questions": 10},
                ...
            ]
        """
        session = self.db.get_session()
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            answers = session.query(UserAnswer).filter(
                UserAnswer.answered_at >= cutoff_date
            ).all()
            
            if not answers:
                return []
            
            # 日付ごとにグループ化
            trend_by_date = {}
            
            for answer in answers:
                date_str = answer.answered_at.strftime("%Y-%m-%d")
                
                if date_str not in trend_by_date:
                    trend_by_date[date_str] = {
                        "date": date_str,
                        "total": 0,
                        "correct": 0
                    }
                
                trend_by_date[date_str]["total"] += 1
                if answer.is_correct:
                    trend_by_date[date_str]["correct"] += 1
            
            # 正答率を計算
            trend = []
            for date_str in sorted(trend_by_date.keys()):
                stats = trend_by_date[date_str]
                correct_rate = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
                
                trend.append({
                    "date": date_str,
                    "correct_rate": correct_rate,
                    "questions": stats["total"]
                })
            
            return trend
        
        finally:
            self.db.close_session(session)


# グローバルインスタンス
_stats_engine = None


def get_statistics_engine() -> StatisticsEngine:
    """グローバル統計エンジン取得"""
    global _stats_engine
    if _stats_engine is None:
        _stats_engine = StatisticsEngine()
    return _stats_engine
