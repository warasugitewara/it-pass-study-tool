"""
クイズ設定ダイアログ - 出題モード・フィルター選択
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSpinBox,
    QCheckBox, QGroupBox, QMessageBox, QScrollArea, QWidget
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from src.ui.styles import COLOR_PRIMARY, COLOR_TEXT_PRIMARY, PADDING_MEDIUM
from src.utils.data_manager import get_data_manager
from src.core import QuizMode


class QuizConfigDialog(QDialog):
    """クイズ設定ダイアログ"""
    
    quiz_started = Signal(str, dict)  # (mode, config)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("学習モード設定")
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)
        self.dm = get_data_manager()
        
        self._setup_ui()
    
    def _setup_ui(self):
        """UI構築"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # タイトル
        title = QLabel("学習モードを選択")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY};")
        layout.addWidget(title)
        
        # モード選択
        mode_group = QGroupBox("出題モード")
        mode_layout = QVBoxLayout()
        
        self.mode_buttons = {}
        modes = [
            (QuizMode.RANDOM.value, "🎲 ランダム", "ランダムに問題が出題されます"),
            (QuizMode.BY_YEAR.value, "📅 年度別", "特定年度の問題を出題します"),
            (QuizMode.BY_CATEGORY.value, "🏆 分野別", "特定分野の問題を出題します"),
            (QuizMode.REVIEW.value, "🔄 復習モード", "正答率が低い問題を優先出題します"),
            (QuizMode.MOCK_TEST.value, "📋 模擬試験", "100問の模擬試験を実施します")
        ]
        
        for mode_key, mode_label, mode_desc in modes:
            btn = QPushButton(f"{mode_label}\n{mode_desc}")
            btn.setMinimumHeight(50)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, m=mode_key: self._select_mode(m))
            self.mode_buttons[mode_key] = btn
            mode_layout.addWidget(btn)
        
        # 最初のモードを選択
        list(self.mode_buttons.values())[0].setChecked(True)
        self.selected_mode = QuizMode.RANDOM.value
        
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)
        
        # フィルター設定
        filter_group = QGroupBox("フィルター設定")
        filter_layout = QVBoxLayout()
        
        # 出題数
        count_layout = QHBoxLayout()
        count_layout.addWidget(QLabel("出題数:"))
        self.spin_count = QSpinBox()
        self.spin_count.setMinimum(1)
        self.spin_count.setMaximum(100)
        self.spin_count.setValue(10)
        count_layout.addWidget(self.spin_count)
        count_layout.addStretch()
        filter_layout.addLayout(count_layout)
        
        filter_layout.addSpacing(10)
        
        # 年度選択
        years_label = QLabel("年度を選択:")
        filter_layout.addWidget(years_label)
        
        year_scroll = QScrollArea()
        year_widget = QWidget()
        year_inner_layout = QVBoxLayout()
        year_inner_layout.setContentsMargins(0, 0, 0, 0)
        
        self.year_checkboxes = {}
        years = self.dm.get_years()
        for year in years[:10]:  # 最新10年度
            checkbox = QCheckBox(f"{year.year}年 {year.season or ''}")
            checkbox.setChecked(True)
            year_inner_layout.addWidget(checkbox)
            self.year_checkboxes[year.id] = checkbox
        
        year_widget.setLayout(year_inner_layout)
        year_scroll.setWidget(year_widget)
        year_scroll.setMaximumHeight(150)
        filter_layout.addWidget(year_scroll)
        
        filter_layout.addSpacing(10)
        
        # 分野選択
        category_label = QLabel("分野を選択:")
        filter_layout.addWidget(category_label)
        
        category_scroll = QScrollArea()
        category_widget = QWidget()
        category_inner_layout = QVBoxLayout()
        category_inner_layout.setContentsMargins(0, 0, 0, 0)
        
        self.category_checkboxes = {}
        categories = self.dm.get_categories()
        for category in categories:
            checkbox = QCheckBox(category.name)
            checkbox.setChecked(True)
            category_inner_layout.addWidget(checkbox)
            self.category_checkboxes[category.id] = checkbox
        
        category_widget.setLayout(category_inner_layout)
        category_scroll.setWidget(category_widget)
        category_scroll.setMaximumHeight(120)
        filter_layout.addWidget(category_scroll)
        
        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)
        
        layout.addStretch()
        
        # ボタン
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        btn_cancel = QPushButton("キャンセル")
        btn_cancel.clicked.connect(self.reject)
        button_layout.addWidget(btn_cancel)
        
        btn_start = QPushButton("✓ 学習を開始")
        btn_start.setStyleSheet(f"background-color: {COLOR_PRIMARY};")
        btn_start.clicked.connect(self._start_quiz)
        button_layout.addWidget(btn_start)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _select_mode(self, mode: str):
        """モード選択"""
        # 他のボタンを解除
        for btn in self.mode_buttons.values():
            btn.setChecked(False)
        # 選択したボタンをチェック
        self.mode_buttons[mode].setChecked(True)
        self.selected_mode = mode
    
    def _start_quiz(self):
        """クイズ開始"""
        # フィルター情報を収集
        selected_years = [
            year_id for year_id, checkbox in self.year_checkboxes.items()
            if checkbox.isChecked()
        ]
        selected_categories = [
            cat_id for cat_id, checkbox in self.category_checkboxes.items()
            if checkbox.isChecked()
        ]
        
        if not selected_years and self.selected_mode != QuizMode.REVIEW.value:
            QMessageBox.warning(self, "エラー", "年度を選択してください")
            return
        
        if not selected_categories and self.selected_mode != QuizMode.REVIEW.value:
            QMessageBox.warning(self, "エラー", "分野を選択してください")
            return
        
        config = {
            "mode": self.selected_mode,
            "question_count": self.spin_count.value(),
            "year_ids": selected_years,
            "category_ids": selected_categories
        }
        
        self.quiz_started.emit(self.selected_mode, config)
        self.accept()


