"""
データベース接続・操作モジュール
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.db.models import Base
from pathlib import Path


class DatabaseManager:
    """データベース管理クラス"""
    
    def __init__(self, db_path: str = None):
        """
        Args:
            db_path: SQLiteデータベースファイルパス
                    デフォルト: プロジェクトルート/data/app.db
        """
        if db_path is None:
            data_dir = Path(__file__).parent.parent.parent / "data"
            data_dir.mkdir(exist_ok=True)
            db_path = str(data_dir / "app.db")
        
        self.db_path = db_path
        self.engine = None
        self.SessionLocal = None
        self._initialize()
    
    def _initialize(self):
        """データベースエンジン初期化"""
        db_url = f"sqlite:///{self.db_path}"
        self.engine = create_engine(
            db_url,
            connect_args={"check_same_thread": False},
            echo=False  # Trueでデバッグログ出力
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def init_db(self):
        """テーブル作成（初回実行時）"""
        Base.metadata.create_all(bind=self.engine)
        print(f"✓ Database initialized: {self.db_path}")
    
    def get_session(self) -> Session:
        """セッション取得"""
        return self.SessionLocal()
    
    def close_session(self, session: Session):
        """セッション終了"""
        if session:
            session.close()


# グローバルデータベースマネージャー
_db_manager = None


def get_db_manager() -> DatabaseManager:
    """グローバルデータベースマネージャー取得"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


def init_database():
    """データベース初期化（アプリケーション起動時実行）"""
    db = get_db_manager()
    db.init_db()
