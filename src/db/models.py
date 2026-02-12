"""
SQLAlchemy ORM モデル定義
ITパスポート試験データベーススキーマ
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class Category(Base):
    """出題分野/科目"""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # リレーション
    questions = relationship("Question", back_populates="category")
    
    def __repr__(self):
        return f"<Category id={self.id} name={self.name}>"


class Year(Base):
    """試験年度"""
    __tablename__ = "years"
    
    id = Column(Integer, primary_key=True)
    year = Column(Integer, unique=True, nullable=False)  # 2023, 2024 など
    season = Column(String(20))  # 春、秋など
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # リレーション
    questions = relationship("Question", back_populates="year")
    
    def __repr__(self):
        return f"<Year id={self.id} year={self.year}>"


class Question(Base):
    """試験問題"""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True)
    question_number = Column(Integer)  # 問題番号
    text = Column(Text, nullable=False)  # 問題文
    explanation = Column(Text)  # 解説
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    year_id = Column(Integer, ForeignKey("years.id"), nullable=False)
    difficulty = Column(Integer, default=1)  # 難易度: 1-5
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # リレーション
    category = relationship("Category", back_populates="questions")
    year = relationship("Year", back_populates="questions")
    choices = relationship("Choice", back_populates="question", cascade="all, delete-orphan")
    user_answers = relationship("UserAnswer", back_populates="question", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Question id={self.id} number={self.question_number} year={self.year_id}>"


class Choice(Base):
    """選択肢"""
    __tablename__ = "choices"
    
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    choice_number = Column(Integer)  # 1, 2, 3, 4
    text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)  # 正解フラグ
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # リレーション
    question = relationship("Question", back_populates="choices")
    
    def __repr__(self):
        return f"<Choice id={self.id} choice_number={self.choice_number} correct={self.is_correct}>"


class UserAnswer(Base):
    """ユーザーの回答履歴"""
    __tablename__ = "user_answers"
    
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    selected_choice_id = Column(Integer, ForeignKey("choices.id"), nullable=True)  # None = 未回答
    is_correct = Column(Boolean, nullable=True)  # None = 未判定
    answered_at = Column(DateTime, default=datetime.utcnow)
    time_spent_seconds = Column(Integer)  # 回答に費やした時間（秒）
    session_id = Column(String(50))  # セッションID（学習セッション識別用）
    
    # リレーション
    question = relationship("Question", back_populates="user_answers")
    
    def __repr__(self):
        return f"<UserAnswer id={self.id} question_id={self.question_id} correct={self.is_correct}>"


class Statistics(Base):
    """学習統計"""
    __tablename__ = "statistics"
    
    id = Column(Integer, primary_key=True)
    total_questions_answered = Column(Integer, default=0)
    total_correct = Column(Integer, default=0)
    correct_rate = Column(Float, default=0.0)  # 正答率
    total_study_time_seconds = Column(Integer, default=0)  # 総学習時間
    last_studied_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Statistics correct_rate={self.correct_rate}%>"


class StudySession(Base):
    """学習セッション（1回の学習記録）"""
    __tablename__ = "study_sessions"
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(50), unique=True, nullable=False)
    mode = Column(String(30))  # ランダム、年度別、分野別、復習など
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    year_id = Column(Integer, ForeignKey("years.id"), nullable=True)
    total_questions = Column(Integer)
    correct_count = Column(Integer, default=0)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    
    def __repr__(self):
        return f"<StudySession id={self.session_id} mode={self.mode}>"
