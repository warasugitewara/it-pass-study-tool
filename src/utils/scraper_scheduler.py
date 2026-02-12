"""
スクレイピング自動更新スケジューラー
APScheduler を使用した定期実行機能
"""

import logging
from datetime import datetime
from typing import Optional, Callable
from threading import Thread, Lock

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from src.utils.scraper import ITPassScraper
from src.utils.data_manager import get_data_manager

logger = logging.getLogger(__name__)


class ScraperScheduler:
    """スクレイピング自動更新スケジューラー"""
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        self.scheduler = BackgroundScheduler()
        self.scraper = None
        self.data_manager = get_data_manager()
        self.is_running = False
        self.last_update_time = None
        self.last_status = "未実行"
        self.last_error = None
        self.update_callbacks = []
        
        logger.info("ScraperScheduler 初期化完了")
    
    def start(self, hour: int = 23, minute: int = 0, interval_hours: Optional[int] = None):
        """
        スケジューラーを開始
        Args:
            hour: 毎日実行する時間（24時間形式）
            minute: 実行する分
            interval_hours: 指定時間ごとの実行（Noneの場合は毎日指定時刻のみ）
        """
        if self.is_running:
            logger.warning("スケジューラーは既に実行中です")
            return False
        
        try:
            # 既存ジョブをクリア
            self.scheduler.remove_all_jobs()
            
            # メインジョブ: 定時実行（毎日指定時刻）
            self.scheduler.add_job(
                self._run_scraping,
                trigger=CronTrigger(hour=hour, minute=minute),
                id='daily_scrape',
                name='Daily scraping at ' + f'{hour:02d}:{minute:02d}',
                replace_existing=True,
                misfire_grace_time=300
            )
            logger.info(f"定時スクレイピングジョブ登録: 毎日 {hour:02d}:{minute:02d}")
            
            # オプション: 定期実行
            if interval_hours and interval_hours > 0:
                self.scheduler.add_job(
                    self._run_scraping,
                    trigger=IntervalTrigger(hours=interval_hours),
                    id='interval_scrape',
                    name=f'Scraping every {interval_hours} hours',
                    replace_existing=True
                )
                logger.info(f"定期スクレイピングジョブ登録: {interval_hours}時間ごと")
            
            if not self.scheduler.running:
                self.scheduler.start()
            
            self.is_running = True
            self.last_status = "実行中"
            logger.info("スケジューラー開始")
            self._notify_callbacks()
            return True
        
        except Exception as e:
            logger.error(f"スケジューラー開始エラー: {e}", exc_info=True)
            self.last_error = str(e)
            return False
    
    def stop(self):
        """スケジューラーを停止"""
        try:
            if self.scheduler.running:
                self.scheduler.shutdown()
            self.is_running = False
            self.last_status = "停止中"
            logger.info("スケジューラー停止")
            self._notify_callbacks()
            return True
        except Exception as e:
            logger.error(f"スケジューラー停止エラー: {e}")
            return False
    
    def run_now(self):
        """即座にスクレイピングを実行（バックグラウンドスレッド）"""
        if self._is_scraping():
            logger.warning("スクレイピングは既に実行中です")
            return False
        
        try:
            # バックグラウンドスレッドで実行
            thread = Thread(target=self._run_scraping, daemon=True)
            thread.start()
            return True
        except Exception as e:
            logger.error(f"スクレイピング即座実行エラー: {e}")
            self.last_error = str(e)
            return False
    
    def _is_scraping(self) -> bool:
        """スクレイピングが実行中か確認"""
        jobs = self.scheduler.get_jobs()
        for job in jobs:
            if job.next_run_time is not None:
                # ジョブが実行予定されている
                pass
        return False
    
    def _run_scraping(self):
        """スクレイピング実行（内部メソッド）"""
        logger.info("スクレイピング実行開始")
        self.last_status = "実行中..."
        self._notify_callbacks()
        
        try:
            self.scraper = ITPassScraper(data_manager=self.data_manager)
            stats = self.scraper.bulk_scrape_and_update()
            
            self.last_update_time = datetime.now()
            self.last_error = None
            self.last_status = (
                f"成功: 新規{stats.get('added', 0)}件, "
                f"重複{stats.get('duplicated', 0)}件, "
                f"エラー{stats.get('errors', 0)}件"
            )
            
            logger.info(f"スクレイピング完了: {self.last_status}")
        
        except Exception as e:
            self.last_error = str(e)
            self.last_status = f"失敗: {e}"
            logger.error(f"スクレイピング実行エラー: {e}", exc_info=True)
        
        finally:
            self._notify_callbacks()
    
    def _notify_callbacks(self):
        """登録されているコールバック関数を実行"""
        for callback in self.update_callbacks:
            try:
                callback(self.get_status())
            except Exception as e:
                logger.error(f"コールバック実行エラー: {e}")
    
    def register_update_callback(self, callback: Callable):
        """
        UI更新用コールバックを登録
        Args:
            callback: 引数にステータス辞書を受け取る関数
        """
        if callback and callable(callback):
            self.update_callbacks.append(callback)
            logger.debug(f"コールバック登録: {callback.__name__}")
    
    def get_status(self) -> dict:
        """現在のスケジューラーステータスを取得"""
        jobs = self.scheduler.get_jobs() if self.scheduler.running else []
        return {
            'is_running': self.is_running,
            'last_update_time': self.last_update_time,
            'last_status': self.last_status,
            'last_error': self.last_error,
            'jobs': len(jobs),
            'next_run_time': jobs[0].next_run_time if jobs else None
        }
    
    def set_schedule_time(self, hour: int, minute: int):
        """スケジュール実行時刻を変更"""
        if not (0 <= hour < 24 and 0 <= minute < 60):
            logger.error(f"不正な時刻: {hour}:{minute}")
            return False
        
        try:
            was_running = self.is_running
            if was_running:
                self.stop()
            
            self.start(hour=hour, minute=minute)
            logger.info(f"スケジュール時刻変更: {hour:02d}:{minute:02d}")
            return True
        except Exception as e:
            logger.error(f"スケジュール時刻変更エラー: {e}")
            return False


# グローバルインスタンス
_scheduler = None


def get_scraper_scheduler() -> ScraperScheduler:
    """グローバルスケジューラーインスタンス取得"""
    global _scheduler
    if _scheduler is None:
        _scheduler = ScraperScheduler()
    return _scheduler


# ユーティリティ関数
def start_scraper_scheduler(hour: int = 23, minute: int = 0) -> bool:
    """スケジューラー開始（簡易版）"""
    scheduler = get_scraper_scheduler()
    return scheduler.start(hour=hour, minute=minute)


def stop_scraper_scheduler() -> bool:
    """スケジューラー停止（簡易版）"""
    scheduler = get_scraper_scheduler()
    return scheduler.stop()


def run_scraping_now() -> bool:
    """スクレイピング即座実行（簡易版）"""
    scheduler = get_scraper_scheduler()
    return scheduler.run_now()
