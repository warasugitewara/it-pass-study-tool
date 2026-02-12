"""
クイズ画面ウィジェット
問題出題・回答・結果表示を担当
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QRadioButton,
    QButtonGroup, QProgressBar, QSpinBox, QComboBox, QMessageBox, QDialog
)
from PySide6.QtCore import Qt, Signal, QTimer, QTime
from PySide6.QtGui import QFont

from src.ui.styles import (
    COLOR_PRIMARY, COLOR_CORRECT, COLOR_INCORRECT, COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY, COLOR_ACCENT, PADDING_MEDIUM
)
from src.core import get_quiz_engine, QuizMode
from src.ui.quiz_config_dialog import QuizConfigDialog


class QuizWidget(QWidget):
    """クイズ出題ウィジェット"""
    
    back_requested = Signal()
    
    def __init__(self):
        super().__init__()
        self.engine = get_quiz_engine()
        self.config_dialog = None
        self.elapsed_time = 0
        self.current_question_start_time = None
        
        self._setup_ui()
        self._setup_timer()
    
    def _setup_ui(self):
        """UI構築"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # ヘッダー: 進捗 + 時間表示
        header_layout = QHBoxLayout()
        
        self.progress_label = QLabel("問題 1 / 10")
        self.progress_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.progress_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY};")
        header_layout.addWidget(self.progress_label)
        
        header_layout.addStretch()
        
        self.timer_label = QLabel("⏱️ 00:00")
        self.timer_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.timer_label.setStyleSheet(f"color: {COLOR_ACCENT};")
        header_layout.addWidget(self.timer_label)
        
        layout.addLayout(header_layout)
        
        # プログレスバー
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumHeight(8)
        layout.addWidget(self.progress_bar)
        
        layout.addSpacing(10)
        
        # 問題文
        self.question_label = QLabel()
        self.question_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.question_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; line-height: 1.6;")
        self.question_label.setWordWrap(True)
        layout.addWidget(self.question_label)
        
        layout.addSpacing(20)
        
        # 選択肢
        self.choices_group = QButtonGroup()
        self.choice_buttons = []
        
        for i in range(4):
            radio = QRadioButton()
            radio.setFont(QFont("Segoe UI", 12))
            radio.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; padding: 8px;")
            self.choices_group.addButton(radio, i)
            self.choice_buttons.append(radio)
            layout.addWidget(radio)
        
        layout.addSpacing(20)
        
        # ボタンレイアウト
        button_layout = QHBoxLayout()
        
        btn_back = QPushButton("← 戻る")
        btn_back.clicked.connect(self._confirm_back)
        button_layout.addWidget(btn_back)
        
        button_layout.addStretch()
        
        btn_prev = QPushButton("◀ 前へ")
        btn_prev.clicked.connect(self._previous_question)
        button_layout.addWidget(btn_prev)
        
        self.btn_next = QPushButton("次へ ▶")
        self.btn_next.clicked.connect(self._next_question)
        button_layout.addWidget(self.btn_next)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _setup_timer(self):
        """タイマーセットアップ"""
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_timer)
    
    def _update_timer(self):
        """時間表示更新"""
        self.elapsed_time += 1
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        self.timer_label.setText(f"⏱️ {minutes:02d}:{seconds:02d}")
    
    def initialize(self, mode: str, num_questions: int = 10):
        """クイズ初期化（設定ダイアログを表示）"""
        self.config_dialog = QuizConfigDialog(self)
        self.config_dialog.quiz_started.connect(self._start_quiz_with_config)
        self.config_dialog.exec()
    
    def _start_quiz_with_config(self, mode: str, config: dict):
        """設定に基づいてクイズ開始"""
        try:
            mode_enum = QuizMode(mode)
            session_id, questions = self.engine.start_session(
                mode=mode_enum,
                question_count=config.get('question_count', 10),
                category_ids=config.get('category_ids', None),
                year_ids=config.get('year_ids', None)
            )
            
            if not questions:
                QMessageBox.warning(self, "エラー", "出題対象の問題がありません。\nまず問題を登録してください。")
                self.back_requested.emit()
                return
            
            self.elapsed_time = 0
            self.timer.start(1000)
            self._display_question()
        
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"クイズ開始に失敗しました:\n{e}")
            self.back_requested.emit()
    
    def _display_question(self):
        """現在の問題を表示"""
        question = self.engine.get_current_question()
        if not question:
            self._show_results()
            return
        
        # 進捗表示更新
        current = self.engine.get_current_index() + 1
        total = self.engine.get_question_count()
        self.progress_label.setText(f"問題 {current} / {total}")
        self.progress_bar.setValue(int((current / total) * 100))
        
        # 問題文表示
        self.question_label.setText(question.text)
        
        # 選択肢表示・リセット
        for i, choice in enumerate(question.choices):
            self.choice_buttons[i].setText(f"{chr(65+i)}. {choice.text}")
            self.choice_buttons[i].show()
        
        self.choices_group.setExclusive(False)
        for button in self.choice_buttons:
            button.setChecked(False)
        self.choices_group.setExclusive(True)
        
        # ボタンテキスト更新
        if current == total:
            self.btn_next.setText("完了 ✓")
        else:
            self.btn_next.setText("次へ ▶")
    
    def _next_question(self):
        """次の問題へ"""
        # 回答を記録
        selected_id = self.choices_group.checkedId()
        if selected_id != -1:
            question = self.engine.get_current_question()
            choice = question.choices[selected_id]
            self.engine.submit_answer(choice.id, 0)
        
        # 次の問題へ
        if self.engine.get_current_index() == self.engine.get_question_count() - 1:
            self._show_results()
            return
        
        self.engine.next_question()
        self._display_question()
    
    def _previous_question(self):
        """前の問題へ"""
        if self.engine.previous_question():
            self._display_question()
    
    def _show_results(self):
        """結果表示"""
        self.timer.stop()
        
        results = self.engine.finish_session()
        
        if results:
            correct_rate = results.get('correct_rate', 0)
            message = (
                f"クイズ完了！\n\n"
                f"正答数: {results.get('correct_count')}/{results.get('total_questions')}問\n"
                f"正答率: {correct_rate:.1f}%\n"
                f"学習時間: {results.get('elapsed_time', 0)}秒"
            )
            
            if correct_rate >= 70:
                QMessageBox.information(self, "✓ 良好です！", message)
            elif correct_rate >= 50:
                QMessageBox.information(self, "👍 お疲れ様でした", message)
            else:
                QMessageBox.information(self, "📚 もう一度チャレンジ", message)
        
        self.back_requested.emit()
    
    def _confirm_back(self):
        """戻る確認"""
        reply = QMessageBox.question(
            self,
            "確認",
            "学習を中止しますか？\n(進捗は保存されません)",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.timer.stop()
            self.back_requested.emit()


