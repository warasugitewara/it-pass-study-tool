"""
クイズ画面ウィジェット
問題出題・回答・結果表示を担当
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QRadioButton,
    QButtonGroup, QProgressBar, QSpinBox, QComboBox, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont

from src.ui.styles import (
    COLOR_PRIMARY, COLOR_CORRECT, COLOR_INCORRECT, COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY, COLOR_ACCENT, PADDING_MEDIUM
)


class QuizWidget(QWidget):
    """クイズ出題ウィジェット"""
    
    back_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.current_question_index = 0
        self.questions = []
        self.user_answers = {}
        self.quiz_mode = None
        self.elapsed_time = 0
        
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
        """クイズ初期化"""
        self.quiz_mode = mode
        self.current_question_index = 0
        self.user_answers = {}
        self.elapsed_time = 0
        self.questions = self._get_questions(mode, num_questions)
        
        if not self.questions:
            QMessageBox.warning(self, "エラー", "出題対象の問題がありません。\nまず問題を登録してください。")
            self.back_requested.emit()
            return
        
        self.timer.start(1000)
        self._display_question()
    
    def _get_questions(self, mode: str, num_questions: int) -> list:
        """出題モードに応じた問題取得"""
        # TODO: データベースから問題を取得する実装
        # 現在はダミーデータ
        return []
    
    def _display_question(self):
        """現在の問題を表示"""
        if not self.questions:
            return
        
        question = self.questions[self.current_question_index]
        
        # 進捗表示更新
        total = len(self.questions)
        current = self.current_question_index + 1
        self.progress_label.setText(f"問題 {current} / {total}")
        self.progress_bar.setValue(int((current / total) * 100))
        
        # 問題文表示
        self.question_label.setText(question.get("text", "問題読み込みエラー"))
        
        # 選択肢表示・リセット
        choices = question.get("choices", [])
        for i, button in enumerate(self.choice_buttons):
            if i < len(choices):
                button.setText(f"{chr(65+i)}. {choices[i]}")  # A, B, C, D
                button.show()
            else:
                button.hide()
        
        self.choices_group.setExclusive(False)
        for button in self.choice_buttons:
            button.setChecked(False)
        self.choices_group.setExclusive(True)
        
        # 前回の回答を復元
        if self.current_question_index in self.user_answers:
            self.choice_buttons[self.user_answers[self.current_question_index]].setChecked(True)
        
        # ボタンテキスト更新
        if self.current_question_index == len(self.questions) - 1:
            self.btn_next.setText("完了 ✓")
        else:
            self.btn_next.setText("次へ ▶")
    
    def _save_current_answer(self):
        """現在の回答を保存"""
        selected_id = self.choices_group.checkedId()
        if selected_id != -1:
            self.user_answers[self.current_question_index] = selected_id
    
    def _next_question(self):
        """次の問題へ"""
        self._save_current_answer()
        
        if self.current_question_index == len(self.questions) - 1:
            self._show_results()
            return
        
        self.current_question_index += 1
        self._display_question()
    
    def _previous_question(self):
        """前の問題へ"""
        if self.current_question_index > 0:
            self._save_current_answer()
            self.current_question_index -= 1
            self._display_question()
    
    def _show_results(self):
        """結果表示"""
        self.timer.stop()
        # TODO: 結果画面実装
        QMessageBox.information(self, "クイズ完了", "クイズを完了しました！")
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
