"""
ITパスポート過去問スクレイパー（非実装）

注意: itpassportsiken.com はスクレイピングをブロックしているため、
Web自動取得機能は実装されていません。

このモジュールは、ユーザーがCSVやJSON形式でインポートするための
ユーティリティとして機能します。
"""

import logging

logger = logging.getLogger(__name__)


class ITPassScraper:
    """
    ITパスポート過去問スクレイパー（非実装）
    
    itpassportsiken.com はスクレイピングをブロックしているため、
    このクラスは使用されません。代わりにサンプルデータとファイルインポートを使用してください。
    """
    
    def __init__(self, data_manager=None):
        self.data_manager = data_manager
        self.stats = {
            'fetched': 0,
            'added': 0,
            'duplicated': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }
        logger.info("Webスクレイピングは実装されていません。サンプルデータまたはファイルインポートを使用してください。")
    
    def bulk_scrape_and_update(self, exams=None):
        """実装されていない"""
        logger.warning("bulk_scrape_and_update: 実装されていません")
        return self.stats

    
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
            
            # 複数のセレクタをを試す（サイト構造の変更に対応）
            selectors = [
                ('a[href*="/kakomon/"][href$="/"]', 'href'),  # /kakomon/##_season/ パターン
                ('a.kakomon-link', 'href'),                   # kakomon-link クラス
                ('a[title*="問題"]', 'href'),                 # タイトルに「問題」
            ]
            
            for selector, attr in selectors:
                try:
                    if selector.startswith('a['):
                        links = soup.select(selector)
                    else:
                        links = soup.find_all('a', class_=selector.split('.')[1])
                    
                    for link in links:
                        href = link.get(attr, '')
                        if href and '/kakomon/' in href:
                            exam = self._parse_exam_url(href)
                            if exam and exam not in past_exams:
                                past_exams.append(exam)
                    
                    if past_exams:
                        break  # 見つかったら他のセレクタは試さない
                except Exception as selector_error:
                    logger.debug(f"セレクタ試行失敗 ({selector}): {selector_error}")
                    continue
            
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
            # 複数の可能なセレクタをを試す
            text_selectors = [
                ('p', 'question_text'),
                ('div', 'question_text'),
                ('p', 'mondai'),
                ('span', 'question'),
                ('div', 'mondai_text'),
            ]
            
            text = None
            for tag, cls in text_selectors:
                elem = element.find(tag, class_=cls)
                if elem:
                    text = elem.get_text(strip=True)
                    break
            
            # タグがない場合、直接テキスト取得
            if not text:
                text_elem = element.find(['p', 'div'])
                if text_elem:
                    text = text_elem.get_text(strip=True)
            
            if not text or len(text) < 5:
                return None
            
            # 選択肢（A, B, C, D）複数のセレクタをを試す
            choices = []
            choice_selectors = [
                ('div', 'choice'),
                ('li', 'choice'),
                ('div', 'sentaku'),
                ('p', 'sentaku'),
                ('label', 'option'),
            ]
            
            for tag, cls in choice_selectors:
                choice_elems = element.find_all(tag, class_=cls)
                if choice_elems:
                    choices = [ce.get_text(strip=True) for ce in choice_elems]
                    if choices:
                        break
            
            if len(choices) < 4:
                # セレクタがない場合、汎用で探索
                choice_elems = element.find_all(['div', 'li', 'p'])
                choices = [ce.get_text(strip=True) for ce in choice_elems[1:5]]  # 最初の要素を除いた最初の4つ
            
            if len(choices) < 4:
                return None
            
            choices = choices[:4]  # 最初の4つを採用
            
            # 正答（複数パターンに対応）
            correct_answer = 1  # デフォルト
            correct_selectors = [
                ('div', 'correct'),
                ('span', 'seitan'),
                ('span', 'ans'),
                ('div', 'answer'),
            ]
            
            for tag, cls in correct_selectors:
                correct_elem = element.find(tag, class_=cls)
                if correct_elem:
                    correct_text = correct_elem.get_text(strip=True)
                    # "1", "A", "①" などのパターンに対応
                    if correct_text and correct_text[0] in ['1', 'A', '①']:
                        correct_answer = 1
                    elif correct_text and correct_text[0] in ['2', 'B', '②']:
                        correct_answer = 2
                    elif correct_text and correct_text[0] in ['3', 'C', '③']:
                        correct_answer = 3
                    elif correct_text and correct_text[0] in ['4', 'D', '④']:
                        correct_answer = 4
                    break
            
            # 解説（複数パターンに対応）
            explanation = ""
            explanation_selectors = [
                ('div', 'explanation'),
                ('div', 'kaisetsu'),
                ('p', 'kaisetsu'),
                ('div', 'setumei'),
            ]
            
            for tag, cls in explanation_selectors:
                explanation_elem = element.find(tag, class_=cls)
                if explanation_elem:
                    explanation = explanation_elem.get_text(strip=True)
                    break
            
            # 分野（複数パターンに対応）
            category = "テクノロジ"  # デフォルト
            category_selectors = [
                ('span', 'category'),
                ('span', 'bunya'),
                ('div', 'category'),
                ('p', 'category'),
            ]
            
            for tag, cls in category_selectors:
                category_elem = element.find(tag, class_=cls)
                if category_elem:
                    category_text = category_elem.get_text(strip=True)
                    for cat_name, cat_code in self.CATEGORIES.items():
                        if cat_name in category_text:
                            category = cat_name
                            break
                    break
            
            return {
                "question_number": question_number,
                "text": text,
                "choices": choices,
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
        
        注意: itpassportsiken.com はスクレイピングを禁止しているため、
        この機能は実装されていません。代わりにサンプルデータを使用してください。
        
        Args:
            exams: 取得対象の試験情報リスト（Noneの場合は自動取得）
        Returns: スクレイピング統計情報
        """
        self.stats['start_time'] = datetime.now()
        self.stats['end_time'] = datetime.now()
        
        logger.warning("Webスクレイピング: itpassportsiken.com はbot をブロックしているため、"
                      "この機能は実装されていません。サンプルデータを使用してください。")
        
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
