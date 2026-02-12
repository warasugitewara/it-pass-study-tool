"""
管理パネル - 問題管理・データインポート
"""

import json
import csv
import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTabWidget,
    QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox, QSpinBox,
    QComboBox, QLineEdit, QTextEdit, QFormLayout, QGroupBox, QDialog,
    QDialogButtonBox, QScrollArea, QSpinBox as QtSpinBox, QTableWidgetSelectionRange,
    QTimeEdit
)
from PySide6.QtCore import Qt, Signal, QTime
from PySide6.QtGui import QFont, QTextCursor

from src.ui.styles import (
    COLOR_PRIMARY, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, PADDING_MEDIUM,
    COLOR_CORRECT, COLOR_INCORRECT, COLOR_SURFACE
)
from src.utils.data_manager import get_data_manager
from src.db import UserAnswer

logger = logging.getLogger(__name__)


class AdminPanel(QWidget):
    """管理パネル"""
    
    back_requested = Signal()
    
    def __init__(self):
        super().__init__()
        self.data_manager = get_data_manager()
        self.questions_table = None
        self.combo_category = None
        self.combo_year = None
        self.current_filtered_questions = []
        self.scheduler = None
        self.scheduler_running = False
        self._setup_ui()
        self._load_initial_data()
    
    def _setup_ui(self):
        """UI構築"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # ヘッダー
        header = QLabel("📋 問題管理・設定")
        header.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY};")
        layout.addWidget(header)
        
        # タブウィジェット
        tabs = QTabWidget()
        tabs.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY};")
        
        # タブ1: データインポート
        tab_import = self._create_import_tab()
        tabs.addTab(tab_import, "📥 データインポート")
        
        # タブ2: 問題一覧
        tab_questions = self._create_questions_tab()
        tabs.addTab(tab_questions, "📝 問題一覧")
        
        # タブ3: 統計情報
        tab_stats = self._create_stats_tab()
        tabs.addTab(tab_stats, "📊 統計情報")
        
        # タブ4: 設定
        tab_settings = self._create_settings_tab()
        tabs.addTab(tab_settings, "⚙️ 設定")
        
        layout.addWidget(tabs)
        
        # ボタン
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        btn_back = QPushButton("← 戻る")
        btn_back.clicked.connect(self.back_requested.emit)
        button_layout.addWidget(btn_back)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _load_initial_data(self):
        """初期化時のデータ読み込み"""
        try:
            # カテゴリを読み込み
            categories = self.data_manager.get_categories()
            years = self.data_manager.get_years()
            
            # UIに反映
            if self.combo_category:
                self.combo_category.clear()
                self.combo_category.addItem("すべて", None)
                for cat in categories:
                    self.combo_category.addItem(cat.name, cat.id)
            
            if self.combo_year:
                self.combo_year.clear()
                self.combo_year.addItem("すべて", None)
                for year in years:
                    year_text = f"{year.year}年"
                    if year.season:
                        year_text += f" {year.season}"
                    self.combo_year.addItem(year_text, year.id)
        except Exception as e:
            print(f"データ読み込みエラー: {e}")
    
    def _create_import_tab(self) -> QWidget:
        """データインポートタブ"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 説明
        desc = QLabel(
            "以下の形式でデータをインポートできます:\n"
            "• CSV ファイル\n"
            "• JSON ファイル\n"
            "• Excel ファイル\n"
            "• Webスクレイピング"
        )
        desc.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY};")
        layout.addWidget(desc)
        
        layout.addSpacing(15)
        
        # スクレイピングボタン
        btn_scrape = QPushButton("🌐 Webからスクレイピング")
        btn_scrape.clicked.connect(self._scrape_from_web)
        layout.addWidget(btn_scrape)
        
        # サンプルデータロードボタン
        btn_sample = QPushButton("📦 サンプルデータをロード")
        btn_sample.clicked.connect(self._load_sample_data)
        layout.addWidget(btn_sample)
        
        layout.addSpacing(10)
        
        # ファイル選択ボタン
        btn_csv = QPushButton("📂 CSVファイルをインポート")
        btn_csv.clicked.connect(self._import_csv)
        layout.addWidget(btn_csv)
        
        btn_json = QPushButton("📂 JSONファイルをインポート")
        btn_json.clicked.connect(self._import_json)
        layout.addWidget(btn_json)
        
        btn_excel = QPushButton("📂 Excelファイルをインポート")
        btn_excel.clicked.connect(self._import_excel)
        layout.addWidget(btn_excel)
        
        layout.addSpacing(15)
        
        # ステータス表示
        self.status_label = QLabel("準備完了")
        self.status_label.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY}; font-size: 11px;")
        layout.addWidget(self.status_label)
        
        layout.addSpacing(15)
        
        # サンプルフォーマット
        group = QGroupBox("CSVフォーマット例")
        group_layout = QVBoxLayout()
        sample = QTextEdit()
        sample.setReadOnly(True)
        sample.setText(
            "year,season,category,question_number,text,choice_a,choice_b,choice_c,choice_d,correct_answer\n"
            "2024,春,ストラテジ,1,\"問題文...\",\"選択肢A\",\"選択肢B\",\"選択肢C\",\"選択肢D\",1"
        )
        sample.setMaximumHeight(100)
        group_layout.addWidget(sample)
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
        
        # サンプルフォーマット
        group = QGroupBox("CSVフォーマット例")
        group_layout = QVBoxLayout()
        sample = QTextEdit()
        sample.setReadOnly(True)
        sample.setText(
            "year,season,category,question_number,text,choice_a,choice_b,choice_c,choice_d,correct_answer\n"
            "2024,春,ストラテジ,1,\"問題文...\",\"選択肢A\",\"選択肢B\",\"選択肢C\",\"選択肢D\",1"
        )
        sample.setMaximumHeight(100)
        group_layout.addWidget(sample)
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def _create_questions_tab(self) -> QWidget:
        """問題一覧タブ"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # フィルタレイアウト
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("分野:"))
        self.combo_category = QComboBox()
        self.combo_category.addItem("すべて")
        self.combo_category.currentIndexChanged.connect(self._apply_filters)
        filter_layout.addWidget(self.combo_category)
        
        filter_layout.addWidget(QLabel("年度:"))
        self.combo_year = QComboBox()
        self.combo_year.addItem("すべて")
        self.combo_year.currentIndexChanged.connect(self._apply_filters)
        filter_layout.addWidget(self.combo_year)
        
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)
        
        # 問題テーブル
        self.questions_table = QTableWidget()
        self.questions_table.setColumnCount(6)
        self.questions_table.setHorizontalHeaderLabels([
            "問題番号", "年度", "分野", "問題文 (最初50字)", "難易度", "操作"
        ])
        self.questions_table.setRowCount(0)
        self.questions_table.setColumnWidth(3, 250)
        layout.addWidget(self.questions_table)
        
        # ボタン
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        btn_add = QPushButton("➕ 追加")
        btn_add.clicked.connect(self._add_question)
        button_layout.addWidget(btn_add)
        
        btn_edit = QPushButton("✏️ 編集")
        btn_edit.clicked.connect(self._edit_question)
        button_layout.addWidget(btn_edit)
        
        btn_delete = QPushButton("🗑️ 削除")
        btn_delete.clicked.connect(self._delete_question)
        button_layout.addWidget(btn_delete)
        
        layout.addLayout(button_layout)
        
        widget.setLayout(layout)
        return widget
    
    def _create_stats_tab(self) -> QWidget:
        """統計情報タブ"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 統計情報表示
        stats_group = QGroupBox("学習統計")
        stats_layout = QFormLayout()
        
        # 登録問題数
        try:
            question_count = self.data_manager.get_question_count()
        except:
            question_count = 0
        
        self.label_question_count = QLabel(f"{question_count}問")
        stats_layout.addRow("登録問題数:", self.label_question_count)
        
        # 統計情報取得
        try:
            stats = self.data_manager.get_statistics()
            total_answers = stats.total_questions_answered if stats else 0
            correct_count = stats.total_correct if stats else 0
            correct_rate = stats.correct_rate if stats else 0.0
        except:
            total_answers = 0
            correct_count = 0
            correct_rate = 0.0
        
        self.label_total_answers = QLabel(f"{total_answers}問")
        stats_layout.addRow("総回答数:", self.label_total_answers)
        
        self.label_correct_count = QLabel(f"{correct_count}問")
        stats_layout.addRow("正答数:", self.label_correct_count)
        
        self.label_correct_rate = QLabel(f"{correct_rate:.1f}%")
        stats_layout.addRow("正答率:", self.label_correct_rate)
        
        # 総学習時間（秒から時間へ変換）
        try:
            # すべての回答から学習時間を集計
            session = self.data_manager.db.get_session()
            all_answers = session.query(UserAnswer).all()
            self.data_manager.db.close_session(session)
            total_time_sec = sum(a.time_spent_seconds or 0 for a in all_answers) if all_answers else 0
            hours = total_time_sec // 3600
            minutes = (total_time_sec % 3600) // 60
        except:
            hours = 0
            minutes = 0
        
        self.label_study_time = QLabel(f"{hours}時間 {minutes}分")
        stats_layout.addRow("総学習時間:", self.label_study_time)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # 分野別正答率
        chart_group = QGroupBox("分野別正答率")
        chart_layout = QVBoxLayout()
        
        self.category_stats_table = QTableWidget()
        self.category_stats_table.setColumnCount(4)
        self.category_stats_table.setHorizontalHeaderLabels([
            "分野", "回答数", "正答数", "正答率"
        ])
        self.category_stats_table.setMaximumHeight(300)
        
        try:
            categories = self.data_manager.get_categories()
            self.category_stats_table.setRowCount(len(categories))
            
            for idx, cat in enumerate(categories):
                cat_stats = self.data_manager.get_category_statistics(cat.id)
                
                self.category_stats_table.setItem(idx, 0, QTableWidgetItem(cat.name))
                self.category_stats_table.setItem(idx, 1, 
                    QTableWidgetItem(str(cat_stats.get("total", 0))))
                self.category_stats_table.setItem(idx, 2, 
                    QTableWidgetItem(str(cat_stats.get("correct", 0))))
                
                rate_item = QTableWidgetItem(f"{cat_stats.get('rate', 0):.1f}%")
                self.category_stats_table.setItem(idx, 3, rate_item)
        except Exception as e:
            print(f"分野別統計取得エラー: {e}")
        
        chart_layout.addWidget(self.category_stats_table)
        chart_group.setLayout(chart_layout)
        layout.addWidget(chart_group)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def _create_settings_tab(self) -> QWidget:
        """設定タブ"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 出題設定
        quiz_group = QGroupBox("出題設定")
        quiz_layout = QFormLayout()
        
        spin_default_questions = QSpinBox()
        spin_default_questions.setMinimum(1)
        spin_default_questions.setMaximum(100)
        spin_default_questions.setValue(10)
        quiz_layout.addRow("デフォルト出題数:", spin_default_questions)
        
        quiz_group.setLayout(quiz_layout)
        layout.addWidget(quiz_group)
        
        # 表示設定
        display_group = QGroupBox("表示設定")
        display_layout = QFormLayout()
        
        # テーマ選択は将来実装
        combo_theme = QComboBox()
        combo_theme.addItem("ダークモード（推奨）")
        display_layout.addRow("テーマ:", combo_theme)
        
        display_group.setLayout(display_layout)
        layout.addWidget(display_group)
        
        # スクレイピング自動更新設定
        scraper_group = QGroupBox("🔄 スクレイピング自動更新")
        scraper_layout = QVBoxLayout()
        
        # スケジューラー有効/無効
        scheduler_control_layout = QHBoxLayout()
        self.btn_scheduler_toggle = QPushButton("✅ スケジューラーを有効化")
        self.btn_scheduler_toggle.clicked.connect(self._toggle_scheduler)
        scheduler_control_layout.addWidget(self.btn_scheduler_toggle)
        scheduler_control_layout.addStretch()
        scraper_layout.addLayout(scheduler_control_layout)
        
        # 実行時刻設定
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("毎日実行時刻:"))
        self.time_edit_schedule = QTimeEdit()
        self.time_edit_schedule.setTime(QTime(23, 0))
        time_layout.addWidget(self.time_edit_schedule)
        time_change_btn = QPushButton("⏰ 時刻を変更")
        time_change_btn.clicked.connect(self._change_schedule_time)
        time_layout.addWidget(time_change_btn)
        time_layout.addStretch()
        scraper_layout.addLayout(time_layout)
        
        # 最終更新日時表示
        update_info_layout = QHBoxLayout()
        update_info_layout.addWidget(QLabel("最終更新:"))
        self.label_last_update = QLabel("未更新")
        self.label_last_update.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY};")
        update_info_layout.addWidget(self.label_last_update)
        update_info_layout.addStretch()
        scraper_layout.addLayout(update_info_layout)
        
        # ステータス表示
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("ステータス:"))
        self.label_scheduler_status = QLabel("停止中")
        self.label_scheduler_status.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY};")
        status_layout.addWidget(self.label_scheduler_status)
        status_layout.addStretch()
        scraper_layout.addLayout(status_layout)
        
        # 「今すぐ更新」ボタン
        btn_update_now = QPushButton("⚡ 今すぐ更新")
        btn_update_now.clicked.connect(self._run_scraping_now)
        scraper_layout.addWidget(btn_update_now)
        
        # 更新ログ表示エリア
        scraper_layout.addWidget(QLabel("📋 更新ログ:"))
        self.text_scraper_log = QTextEdit()
        self.text_scraper_log.setReadOnly(True)
        self.text_scraper_log.setMaximumHeight(150)
        scraper_layout.addWidget(self.text_scraper_log)
        
        scraper_group.setLayout(scraper_layout)
        layout.addWidget(scraper_group)
        
        # 保存ボタン
        btn_save = QPushButton("💾 設定を保存")
        btn_save.clicked.connect(self._save_settings)
        layout.addWidget(btn_save)
        
        layout.addStretch()
        
        # 初期化
        self._initialize_scheduler_ui()
        
        widget.setLayout(layout)
        return widget
    
    def _import_csv(self):
        """CSVインポート"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "CSVファイルを選択", "", "CSV Files (*.csv)"
        )
        if not file_path:
            return
        
        try:
            questions_data = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    questions_data.append({
                        'year': int(row.get('year', 2024)),
                        'season': row.get('season', '春'),
                        'category': row.get('category', 'テクノロジ'),
                        'question_number': int(row.get('question_number', 0)),
                        'text': row.get('text', ''),
                        'explanation': row.get('explanation', ''),
                        'choices': [
                            row.get('choice_a', ''),
                            row.get('choice_b', ''),
                            row.get('choice_c', ''),
                            row.get('choice_d', '')
                        ],
                        'correct_answer': int(row.get('correct_answer', 1)),
                        'difficulty': int(row.get('difficulty', 2))
                    })
            
            count = self.data_manager.bulk_add_questions(questions_data)
            self._load_initial_data()
            self._apply_filters()
            QMessageBox.information(
                self, 
                "インポート成功", 
                f"{count}/{len(questions_data)}件の問題をインポートしました。"
            )
        except Exception as e:
            QMessageBox.critical(self, "インポートエラー", f"エラーが発生しました:\n{str(e)}")
    
    def _import_json(self):
        """JSONインポート"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "JSONファイルを選択", "", "JSON Files (*.json)"
        )
        if not file_path:
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # リストまたは単一オブジェクト対応
            questions_data = data if isinstance(data, list) else [data]
            
            count = self.data_manager.bulk_add_questions(questions_data)
            self._load_initial_data()
            self._apply_filters()
            QMessageBox.information(
                self, 
                "インポート成功", 
                f"{count}/{len(questions_data)}件の問題をインポートしました。"
            )
        except Exception as e:
            QMessageBox.critical(self, "インポートエラー", f"エラーが発生しました:\n{str(e)}")
    
    def _import_excel(self):
        """Excelインポート"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Excelファイルを選択", "", "Excel Files (*.xlsx *.xls)"
        )
        if not file_path:
            return
        
        try:
            import pandas as pd
            df = pd.read_excel(file_path)
            questions_data = df.to_dict('records')
            
            count = self.data_manager.bulk_add_questions(questions_data)
            self._load_initial_data()
            self._apply_filters()
            QMessageBox.information(
                self, 
                "インポート成功", 
                f"{count}/{len(questions_data)}件の問題をインポートしました。"
            )
        except ImportError:
            QMessageBox.warning(
                self, 
                "ライブラリが見つかりません",
                "pandasライブラリが必要です。\npip install pandas openpyxl を実行してください。"
            )
        except Exception as e:
            QMessageBox.critical(self, "インポートエラー", f"エラーが発生しました:\n{str(e)}")
    
    def _add_question(self):
        """問題追加"""
        dialog = QuestionDialog(self, mode='add', data_manager=self.data_manager)
        if dialog.exec() == QDialog.Accepted:
            question_data = dialog.get_data()
            result = self.data_manager.add_question(question_data)
            if result:
                QMessageBox.information(self, "成功", "問題を追加しました。")
                self._load_initial_data()
                self._apply_filters()
            else:
                QMessageBox.warning(self, "エラー", "問題の追加に失敗しました。")
    
    def _edit_question(self):
        """問題編集"""
        current_row = self.questions_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "編集する問題を選択してください。")
            return
        
        # 選択された問題の情報を取得
        if current_row < len(self.current_filtered_questions):
            question = self.current_filtered_questions[current_row]
            dialog = QuestionDialog(self, mode='edit', question=question, data_manager=self.data_manager)
            if dialog.exec() == QDialog.Accepted:
                QMessageBox.information(self, "成功", "問題を更新しました。")
                self._apply_filters()
    
    def _delete_question(self):
        """問題削除"""
        current_row = self.questions_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "削除する問題を選択してください。")
            return
        
        if current_row < len(self.current_filtered_questions):
            question = self.current_filtered_questions[current_row]
            reply = QMessageBox.question(
                self,
                "確認",
                f"問題番号 {question.question_number} を削除してもよろしいですか？",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                try:
                    session = self.data_manager.db.get_session()
                    q = session.query(type(question)).filter_by(id=question.id).first()
                    if q:
                        q.is_active = False
                        session.commit()
                    self.data_manager.db.close_session(session)
                    QMessageBox.information(self, "成功", "問題を削除しました。")
                    self._apply_filters()
                except Exception as e:
                    QMessageBox.critical(self, "エラー", f"削除に失敗しました: {e}")
    
    def _apply_filters(self):
        """フィルターを適用してテーブルを更新"""
        try:
            # フィルターのクリア
            self.questions_table.setRowCount(0)
            
            category_id = self.combo_category.currentData() if self.combo_category else None
            year_id = self.combo_year.currentData() if self.combo_year else None
            
            # フィルター条件を作成
            category_ids = [category_id] if category_id else None
            year_ids = [year_id] if year_id else None
            
            # 問題取得
            questions = self.data_manager.get_questions(
                category_ids=category_ids,
                year_ids=year_ids,
                limit=1000
            )
            
            self.current_filtered_questions = questions
            
            # テーブルに追加
            self.questions_table.setRowCount(len(questions))
            
            for row, question in enumerate(questions):
                # 問題番号
                self.questions_table.setItem(row, 0, QTableWidgetItem(str(question.question_number)))
                
                # 年度
                year_text = f"{question.year.year}"
                if question.year.season:
                    year_text += f" {question.year.season}"
                self.questions_table.setItem(row, 1, QTableWidgetItem(year_text))
                
                # 分野
                self.questions_table.setItem(row, 2, QTableWidgetItem(question.category.name))
                
                # 問題文（最初50字）
                text_preview = question.text[:50] + "..." if len(question.text) > 50 else question.text
                self.questions_table.setItem(row, 3, QTableWidgetItem(text_preview))
                
                # 難易度
                difficulty_item = QTableWidgetItem(str(question.difficulty))
                self.questions_table.setItem(row, 4, difficulty_item)
                
                # 操作ボタン
                btn_edit = QPushButton("編集")
                btn_edit.clicked.connect(lambda checked, r=row: self._on_edit_button_clicked(r))
                self.questions_table.setCellWidget(row, 5, btn_edit)
        
        except Exception as e:
            print(f"フィルター適用エラー: {e}")
    
    def _on_edit_button_clicked(self, row):
        """テーブルのeditボタンクリック処理"""
        self.questions_table.setCurrentRow(row)
        self._edit_question()
    
    def _initialize_scheduler_ui(self):
        """スケジューラーUI初期化"""
        try:
            try:
                from src.utils.scraper_scheduler import get_scraper_scheduler
                self.scheduler = get_scraper_scheduler()
                self.scheduler.register_update_callback(self._on_scheduler_status_changed)
                self._update_scheduler_ui()
            except ImportError:
                # APScheduler がインストールされていない場合
                logger.warning("APScheduler がインストールされていません。スケジューラーは無効です。")
                self.btn_scheduler_toggle.setEnabled(False)
                self.btn_scheduler_toggle.setText("⚠️ スケジューラー無効（APScheduler未インストール）")
                self._add_log("⚠️ APScheduler がインストールされていません")
        except Exception as e:
            logger.error(f"スケジューラーUI初期化エラー: {e}")
            print(f"スケジューラーUI初期化エラー: {e}")
    
    def _toggle_scheduler(self):
        """スケジューラーの有効/無効を切り替え"""
        if not self.scheduler:
            QMessageBox.warning(self, "エラー", "スケジューラーが初期化されていません")
            return
        
        try:
            if self.scheduler_running:
                # 停止
                if self.scheduler.stop():
                    self.scheduler_running = False
                    self._add_log("✅ スケジューラーを停止しました")
                    self._update_scheduler_ui()
            else:
                # 開始
                if self.scheduler.start(hour=23, minute=0):
                    self.scheduler_running = True
                    self._add_log("✅ スケジューラーを有効化しました（毎日 23:00に実行）")
                    self._update_scheduler_ui()
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"スケジューラー制御エラー: {e}")
            logger.error(f"スケジューラー制御エラー: {e}")
    
    def _run_scraping_now(self):
        """即座にスクレイピングを実行"""
        if not self.scheduler:
            QMessageBox.warning(self, "エラー", "スケジューラーが初期化されていません")
            return
        
        try:
            self._add_log("⏳ スクレイピング実行中...")
            if self.scheduler.run_now():
                QMessageBox.information(self, "実行", "スクレイピングをバックグラウンドで実行中です")
            else:
                QMessageBox.warning(self, "警告", "スクレイピングは既に実行中です")
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"スクレイピング実行エラー: {e}")
            logger.error(f"スクレイピング実行エラー: {e}")
    
    def _save_settings(self):
        """設定を保存"""
        QMessageBox.information(self, "保存", "設定を保存しました。")
    
    def _update_scheduler_ui(self):
        """スケジューラーUIを更新"""
        try:
            status = self.scheduler.get_status()
            self.scheduler_running = status['is_running']
            
            # ボタンテキストを更新
            if self.scheduler_running:
                self.btn_scheduler_toggle.setText("❌ スケジューラーを無効化")
                self.btn_scheduler_toggle.setStyleSheet("background-color: #ff6b6b;")
            else:
                self.btn_scheduler_toggle.setText("✅ スケジューラーを有効化")
                self.btn_scheduler_toggle.setStyleSheet("")
            
            # ステータス表示
            status_text = status['last_status'] or "未実行"
            self.label_scheduler_status.setText(status_text)
            
            # 最終更新日時
            if status['last_update_time']:
                update_time = status['last_update_time'].strftime("%Y年%m月%d日 %H:%M:%S")
                self.label_last_update.setText(update_time)
            
            # 次回実行予定
            if status['next_run_time']:
                next_time = status['next_run_time'].strftime("%Y年%m月%d日 %H:%M:%S")
                self._add_log(f"📅 次回実行予定: {next_time}")
        
        except Exception as e:
            logger.error(f"UIアップデートエラー: {e}")
    
    def _on_scheduler_status_changed(self, status: dict):
        """スケジューラーステータス変更時のコールバック"""
        self._update_scheduler_ui()
        if status['last_status']:
            self._add_log(f"🔄 {status['last_status']}")
    
    def _add_log(self, message: str):
        """ログメッセージを表示エリアに追加"""
        if hasattr(self, 'text_scraper_log'):
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {message}"
            self.text_scraper_log.append(log_entry)
            # スクロールを最下部に移動
            cursor = self.text_scraper_log.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.text_scraper_log.setTextCursor(cursor)
    
    def _change_schedule_time(self):
        """スケジュール実行時刻を変更"""
        if not self.scheduler:
            QMessageBox.warning(self, "エラー", "スケジューラーが初期化されていません")
            return
        
        try:
            time = self.time_edit_schedule.time()
            hour = time.hour()
            minute = time.minute()
            
            if self.scheduler.set_schedule_time(hour, minute):
                self._add_log(f"✅ スケジュール時刻を {hour:02d}:{minute:02d} に変更しました")
                QMessageBox.information(self, "成功", f"スケジュール時刻を {hour:02d}:{minute:02d} に変更しました")
                self._update_scheduler_ui()
            else:
                QMessageBox.warning(self, "エラー", "スケジュール時刻の変更に失敗しました")
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"時刻変更エラー: {e}")
            logger.error(f"時刻変更エラー: {e}")
    
    def _scrape_from_web(self):
        """Webからスクレイピング実行またはフォールバックデータをロード"""
        try:
            reply = QMessageBox.question(
                self,
                "確認",
                "WebからITパスポート過去問をスクレイピングします。\n\n"
                "注意: サイトの構造が変わっている場合、自動フォールバック用の\n"
                "サンプルデータが代わりにロードされます。\n\n"
                "ネットワーク接続を確認してから実行してください。",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply != QMessageBox.Yes:
                return
            
            self.status_label.setText("スクレイピング実行中...")
            self._add_log("⏳ Webからスクレイピングを開始します...")
            
            from src.utils.scraper import ITPassScraper
            
            scraper = ITPassScraper(self.data_manager)
            stats = scraper.bulk_scrape_and_update()
            
            self._add_log(f"✅ スクレイピング結果:")
            self._add_log(f"   取得件数: {stats['fetched']}")
            self._add_log(f"   追加件数: {stats['added']}")
            self._add_log(f"   重複: {stats['duplicated']}")
            self._add_log(f"   エラー: {stats['errors']}")
            
            self.status_label.setText(f"最終更新: {stats['end_time'].strftime('%Y-%m-%d %H:%M:%S')}")
            
            if stats['added'] > 0:
                QMessageBox.information(
                    self,
                    "成功",
                    f"{stats['added']}件の新しい問題をデータベースに追加しました。"
                )
                self._load_initial_data()
                self._apply_filters()
            elif stats['fetched'] > 0:
                QMessageBox.information(
                    self,
                    "完了",
                    f"{stats['fetched']}件の問題を取得しましたが、重複のため追加されませんでした。"
                )
            else:
                # フォールバック: サンプルデータをロード
                self._add_log("⚠️  Webスクレイピングに失敗。フォールバックデータをロードします...")
                fallback_added = self._load_fallback_sample_data()
                
                if fallback_added > 0:
                    QMessageBox.information(
                        self,
                        "フォールバック",
                        f"Webからのデータ取得に失敗しました。\n\n"
                        f"代わりに {fallback_added} 件のサンプルデータ（2024年秋）を\n"
                        f"ロードしました。\n\n"
                        f"サイト構造が変わっている可能性があります。\n"
                        f"詳細は GitHub Issues で報告してください。"
                    )
                    self._load_initial_data()
                    self._apply_filters()
                else:
                    QMessageBox.warning(
                        self,
                        "警告",
                        "問題を取得できませんでした。\nサイトの構造が変わっている可能性があります。\n"
                        "GitHub Issues でご報告ください。"
                    )
        
        except ImportError:
            QMessageBox.warning(
                self,
                "ライブラリが見つかりません",
                "beautifulsoup4やrequestsライブラリが必要です。\n"
                "pip install beautifulsoup4 requests を実行してください。"
            )
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"スクレイピング中にエラーが発生しました:\n{str(e)}")
            self._add_log(f"❌ エラー: {str(e)}")
            self.status_label.setText("エラー: スクレイピング失敗")
    
    def _load_sample_data(self):
        """サンプルデータをロード"""
        try:
            reply = QMessageBox.question(
                self,
                "確認",
                "サンプルデータ (2024年春 5問) をデータベースにロードしますか?\n\n"
                "既に同じデータがある場合は重複として扱われます。",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply != QMessageBox.Yes:
                return
            
            sample_file = Path(__file__).parent.parent.parent / "resources" / "sample_data" / "sample_questions_2024_spring.json"
            
            if not sample_file.exists():
                QMessageBox.warning(self, "エラー", f"サンプルデータが見つかりません:\n{sample_file}")
                return
            
            self.status_label.setText("サンプルデータをロード中...")
            self._add_log("⏳ サンプルデータをロードしています...")
            
            with open(sample_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            questions = data.get('questions', [])
            count = self.data_manager.bulk_add_questions(questions)
            
            self.status_label.setText(f"最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self._add_log(f"✅ サンプルデータをロードしました: {count}件追加")
            
            QMessageBox.information(
                self,
                "成功",
                f"{count}/{len(questions)}件のサンプル問題を追加しました。"
            )
            
            self._load_initial_data()
            self._apply_filters()
        
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"サンプルデータロード中にエラーが発生しました:\n{str(e)}")
            self._add_log(f"❌ エラー: {str(e)}")
            self.status_label.setText("エラー: ロード失敗")
    
    def _load_fallback_sample_data(self) -> int:
        """フォールバック用サンプルデータをロード（秋データ）"""
        try:
            fallback_file = Path(__file__).parent.parent.parent / "resources" / "sample_data" / "sample_questions_2024_autumn.json"
            
            if not fallback_file.exists():
                self._add_log("⚠️  フォールバックデータも見つかりません")
                return 0
            
            with open(fallback_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            questions = data.get('questions', [])
            count = self.data_manager.bulk_add_questions(questions)
            
            self._add_log(f"✅ フォールバックデータ: {count}件追加")
            return count
        
        except Exception as e:
            self._add_log(f"❌ フォールバック失敗: {str(e)}")
            return 0





class QuestionDialog(QDialog):
    """問題追加/編集ダイアログ"""
    
    def __init__(self, parent=None, mode='add', question=None, data_manager=None):
        super().__init__(parent)
        self.mode = mode
        self.question = question
        self.data_manager = data_manager
        self.setWindowTitle("問題" + ("追加" if mode == 'add' else "編集"))
        self.setGeometry(100, 100, 600, 500)
        self._setup_ui()
    
    def _setup_ui(self):
        """ダイアログUIを構築"""
        layout = QVBoxLayout()
        
        # スクロール可能なフォーム
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        form_widget = QWidget()
        form_layout = QFormLayout()
        
        # 年度
        self.combo_year = QComboBox()
        try:
            years = self.data_manager.get_years()
            for year in years:
                year_text = f"{year.year}"
                if year.season:
                    year_text += f" {year.season}"
                self.combo_year.addItem(year_text, year.id)
        except:
            pass
        if self.question and self.mode == 'edit':
            for i in range(self.combo_year.count()):
                if self.combo_year.itemData(i) == self.question.year_id:
                    self.combo_year.setCurrentIndex(i)
                    break
        form_layout.addRow("年度:", self.combo_year)
        
        # 分野
        self.combo_category = QComboBox()
        try:
            categories = self.data_manager.get_categories()
            for cat in categories:
                self.combo_category.addItem(cat.name, cat.id)
        except:
            pass
        if self.question and self.mode == 'edit':
            for i in range(self.combo_category.count()):
                if self.combo_category.itemData(i) == self.question.category_id:
                    self.combo_category.setCurrentIndex(i)
                    break
        form_layout.addRow("分野:", self.combo_category)
        
        # 問題番号
        self.spin_number = QSpinBox()
        self.spin_number.setMinimum(1)
        self.spin_number.setMaximum(10000)
        if self.question and self.mode == 'edit':
            self.spin_number.setValue(self.question.question_number)
        form_layout.addRow("問題番号:", self.spin_number)
        
        # 問題文
        self.text_question = QTextEdit()
        self.text_question.setMinimumHeight(100)
        if self.question and self.mode == 'edit':
            self.text_question.setText(self.question.text)
        form_layout.addRow("問題文:", self.text_question)
        
        # 解説
        self.text_explanation = QTextEdit()
        self.text_explanation.setMinimumHeight(80)
        if self.question and self.mode == 'edit':
            self.text_explanation.setText(self.question.explanation or "")
        form_layout.addRow("解説:", self.text_explanation)
        
        # 選択肢
        self.line_choices = []
        if self.question and self.mode == 'edit':
            for i, choice in enumerate(self.question.choices):
                line = QLineEdit()
                line.setText(choice.text)
                self.line_choices.append(line)
                form_layout.addRow(f"選択肢{i+1}:", line)
        else:
            for i in range(4):
                line = QLineEdit()
                self.line_choices.append(line)
                form_layout.addRow(f"選択肢{i+1}:", line)
        
        # 正解
        self.spin_correct = QSpinBox()
        self.spin_correct.setMinimum(1)
        self.spin_correct.setMaximum(4)
        if self.question and self.mode == 'edit':
            for i, choice in enumerate(self.question.choices):
                if choice.is_correct:
                    self.spin_correct.setValue(i + 1)
                    break
        form_layout.addRow("正解:", self.spin_correct)
        
        # 難易度
        self.spin_difficulty = QSpinBox()
        self.spin_difficulty.setMinimum(1)
        self.spin_difficulty.setMaximum(5)
        if self.question and self.mode == 'edit':
            self.spin_difficulty.setValue(self.question.difficulty)
        form_layout.addRow("難易度:", self.spin_difficulty)
        
        form_widget.setLayout(form_layout)
        scroll.setWidget(form_widget)
        layout.addWidget(scroll)
        
        # ボタン
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.accept)
        button_layout.addWidget(btn_ok)
        
        btn_cancel = QPushButton("キャンセル")
        btn_cancel.clicked.connect(self.reject)
        button_layout.addWidget(btn_cancel)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_data(self) -> Dict:
        """フォームからデータを取得"""
        return {
            'year': self.combo_year.currentData() or 2024,
            'season': '春',
            'category': self.combo_category.currentText(),
            'question_number': self.spin_number.value(),
            'text': self.text_question.toPlainText(),
            'explanation': self.text_explanation.toPlainText(),
            'choices': [line.text() for line in self.line_choices],
            'correct_answer': self.spin_correct.value(),
            'difficulty': self.spin_difficulty.value()
        }
