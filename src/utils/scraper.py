"""
ITパスポート過去問スクレイパー
複数ソースからの過去問データ自動取得
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging
from datetime import datetime

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
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
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
                    past_exams.append(self._parse_exam_url(href))
            
        except Exception as e:
            logger.error(f"過去問情報取得エラー: {e}")
        
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
            
        except Exception as e:
            logger.error(f"問題取得エラー ({exam_url}): {e}")
        
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
