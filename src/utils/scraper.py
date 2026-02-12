"""
ITパスポート過去問スクレイパー
複数ソースからの過去問データ自動取得
重複チェック・バッチ更新・エラーハンドリング機能搭載
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Tuple
import logging
from datetime import datetime
from hashlib import md5

logger = logging.getLogger(__name__)


class ITPassScraper:
    """ITパスポート過去問スクレイパー"""
    
    BASE_URL_SIKEN = "https://www.itpassportsiken.com"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # 出題分野マッピング
    CATEGORIES = {
        "ストラテジ": "strategy",
        "マネジメント": "management", 
        "テクノロジ": "technology"
    }
    
    def __init__(self, data_manager=None):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
        self.data_manager = data_manager
        self.stats = {
            'fetched': 0,
            'added': 0,
            'duplicated': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }
    
    def get_past_exams(self) -> List[Dict]:
        """
        過去問情報を取得
        Returns: [{"year": 2024, "season": "春", "category": "ストラテジ", "url": "..."}, ...]
        """
        past_exams = []
        try:
            # itpassportsiken.com から過去問URLを抽出
            url = f"{self.BASE_URL_SIKEN}/kakomon/"
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # ディレクトリリストを取得（構造に応じて調整）
            # 例: /kakomon/07_haru/ (令和7年春)
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                if '/kakomon/' in href and href.endswith('/'):
                    exam = self._parse_exam_url(href)
                    if exam:
                        past_exams.append(exam)
            
            logger.info(f"過去問情報取得: {len(past_exams)}件")
        except requests.Timeout:
            logger.error(f"過去問情報取得タイムアウト: {url}")
        except Exception as e:
            logger.error(f"過去問情報取得エラー: {e}", exc_info=True)
        
        return past_exams
    
    def _parse_exam_url(self, url: str) -> Optional[Dict]:
        """URLから年度・季節情報を抽出"""
        # 例: /kakomon/07_haru/ → {year: 2024, season: "春", ...}
        import re
        match = re.search(r'/kakomon/(\d+)_(haru|aki|toku)/', url)
        if match:
            year_code = int(match.group(1))
            season_code = match.group(2)
            
            # 令和 = 2018+
            # 令和7年 = 2024
            # 令和6年 = 2023
            year = 2018 + year_code
            
            season_map = {"haru": "春", "aki": "秋", "toku": "特別"}
            season = season_map.get(season_code, "不明")
            
            return {
                "year": year,
                "season": season,
                "url": url,
                "source": "itpassportsiken"
            }
        return None
    
    def get_questions_from_exam(self, exam_url: str) -> List[Dict]:
        """
        特定の年度・季節の問題を取得
        Args:
            exam_url: 例) /kakomon/07_haru/
        Returns: [{"question_number": 1, "text": "...", "choices": [...], "correct": 1, ...}, ...]
        """
        questions = []
        try:
            url = f"{self.BASE_URL_SIKEN}{exam_url}"
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 問題の HTML 構造に応じて抽出
            # itpassportsiken.com の構造を分析必要
            problem_divs = soup.find_all('div', class_='kakomon')
            
            for idx, problem_div in enumerate(problem_divs, 1):
                question = self._extract_question(problem_div, idx)
                if question:
                    questions.append(question)
            
            logger.info(f"問題取得: {url} → {len(questions)}件")
        except requests.Timeout:
            logger.error(f"問題取得タイムアウト: {exam_url}")
        except Exception as e:
            logger.error(f"問題取得エラー ({exam_url}): {e}", exc_info=True)
        
        return questions
    
    def _extract_question(self, element, question_number: int) -> Optional[Dict]:
        """HTML要素から問題情報を抽出"""
        try:
            # 問題文
            text_elem = element.find('p', class_='question_text')
            if not text_elem:
                return None
            text = text_elem.get_text(strip=True)
            
            # 選択肢（A, B, C, D）
            choices = []
            choice_elems = element.find_all('div', class_='choice')
            for choice_elem in choice_elems:
                choice_text = choice_elem.get_text(strip=True)
                choices.append(choice_text)
            
            if len(choices) < 4:
                return None
            
            # 正答
            correct_elem = element.find('div', class_='correct')
            correct_answer = 1  # デフォルト
            if correct_elem:
                # 正答マーク位置から判定
                correct_text = correct_elem.get_text(strip=True)
                # 構造に応じて解析
            
            # 解説
            explanation_elem = element.find('div', class_='explanation')
            explanation = explanation_elem.get_text(strip=True) if explanation_elem else ""
            
            # 分野（テキストから推測または属性から取得）
            category = "テクノロジ"  # デフォルト
            category_elem = element.find('span', class_='category')
            if category_elem:
                category_text = category_elem.get_text(strip=True)
                for cat_name, cat_code in self.CATEGORIES.items():
                    if cat_name in category_text:
                        category = cat_name
                        break
            
            return {
                "question_number": question_number,
                "text": text,
                "choices": choices[:4],  # 最初の4つを採用
                "correct_answer": correct_answer,
                "explanation": explanation,
                "category": category,
                "difficulty": 2  # 難易度は後で調整可能
            }
        
        except Exception as e:
            logger.error(f"問題抽出エラー: {e}")
            return None
    
    def validate_question(self, question: Dict) -> bool:
        """問題データの妥当性チェック"""
        required_fields = ['text', 'choices', 'correct_answer']
        
        # 必須フィールド確認
        if not all(field in question for field in required_fields):
            return False
        
        # 選択肢が4つか確認
        if len(question['choices']) != 4:
            return False
        
        # 正答が1-4の範囲か確認
        if not (1 <= question['correct_answer'] <= 4):
            return False
        
        # テキストが空でないか確認
        if not question['text'] or len(question['text']) < 10:
            return False
        
        return True
    
    def get_question_hash(self, year: int, category: str, question_number: int) -> str:
        """問題の重複チェック用ハッシュを生成（年度+分野+問題番号で一意判定）"""
        unique_key = f"{year}:{category}:{question_number}"
        return md5(unique_key.encode()).hexdigest()
    
    def check_duplicate(self, year: int, category: str, question_number: int) -> bool:
        """問題が既に登録されているか確認"""
        if not self.data_manager:
            return False
        
        try:
            from sqlalchemy import and_
            session = self.data_manager.db.get_session()
            from src.db import Question, Category, Year
            
            result = session.query(Question).join(Category).join(Year).filter(
                and_(
                    Year.year == year,
                    Category.name == category,
                    Question.question_number == question_number
                )
            ).first()
            
            self.data_manager.db.close_session(session)
            return result is not None
        except Exception as e:
            logger.error(f"重複チェックエラー: {e}")
            return False
    
    def bulk_scrape_and_update(self, exams: List[Dict] = None) -> Dict:
        """
        複数の試験からスクレイピングしてDBに一括更新（差分抽出）
        Args:
            exams: 取得対象の試験情報リスト（Noneの場合は自動取得）
        Returns: スクレイピング統計情報
        """
        self.stats['start_time'] = datetime.now()
        
        try:
            if exams is None:
                exams = self.get_past_exams()
            
            if not exams:
                logger.warning("スクレイピング対象の試験情報がありません")
                self.stats['end_time'] = datetime.now()
                return self.stats
            
            logger.info(f"スクレイピング開始: {len(exams)}試験")
            
            # 差分データ収集
            new_questions = []
            
            for exam in exams:
                try:
                    questions = self.get_questions_from_exam(exam.get('url', ''))
                    
                    for question in questions:
                        # 重複チェック
                        if self.check_duplicate(
                            exam.get('year'),
                            question.get('category'),
                            question.get('question_number')
                        ):
                            self.stats['duplicated'] += 1
                            logger.debug(f"重複: {exam.get('year')} {question.get('category')} 問{question.get('question_number')}")
                            continue
                        
                        # 妥当性チェック
                        if not self.validate_question(question):
                            self.stats['errors'] += 1
                            logger.warning(f"不正な問題データ: {question}")
                            continue
                        
                        # 試験情報をマージ
                        question.update({
                            'year': exam.get('year'),
                            'season': exam.get('season')
                        })
                        new_questions.append(question)
                        self.stats['fetched'] += 1
                
                except Exception as e:
                    self.stats['errors'] += 1
                    logger.error(f"試験スクレイピング失敗 ({exam}): {e}")
                    continue
            
            # DB に一括追加
            if new_questions and self.data_manager:
                try:
                    self.stats['added'] = self.data_manager.bulk_add_questions(new_questions)
                    logger.info(f"スクレイピング完了: 新規追加 {self.stats['added']}件")
                except Exception as e:
                    logger.error(f"DB追加エラー: {e}")
                    self.stats['errors'] += len(new_questions)
            
        except Exception as e:
            logger.error(f"スクレイピング処理エラー: {e}", exc_info=True)
        
        finally:
            self.stats['end_time'] = datetime.now()
        
        return self.stats
    
    def get_last_update_time(self) -> Optional[datetime]:
        """最終更新日時を取得"""
        try:
            if not self.data_manager:
                return None
            
            session = self.data_manager.db.get_session()
            from src.db import Question
            
            latest = session.query(Question).order_by(Question.created_at.desc()).first()
            self.data_manager.db.close_session(session)
            
            return latest.created_at if latest else None
        except Exception as e:
            logger.error(f"最終更新日時取得エラー: {e}")
            return None



# 使用例
if __name__ == "__main__":
    scraper = ITPassScraper()
    
    # 過去問情報取得
    exams = scraper.get_past_exams()
    print(f"取得した過去問: {len(exams)}件")
    for exam in exams[:5]:
        print(f"  {exam}")
    
    # 特定年度の問題取得
    if exams:
        questions = scraper.get_questions_from_exam(exams[0]['url'])
        print(f"問題: {len(questions)}件")
