"""
結果表示ウィジェット
セッション終了後の成績・統計表示
"""

from PySide6.Qt.idgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, Qt.bWidget,
    Qt.bleWidget, Qt.bleWidgetItem, QScrollArea
)
from PySide6.Qt.ore import Qt. Signal
from PySide6.Qt.ui import QFont, QColor

from src.ui.styles import (
    COLOR_PRIMARY, COLOR_CORRECT, COLOR_INCORRECT, COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY, COLOR_ACCENT
)
from src.core.statistics import get_statistics_engine


class ResultsWidget(QWidget):
    """結果表示ウィジェット"""
    
    back_requested = Signal()
    
    def __init__(self):
        super().__init__()
        self.stats_engine = get_statistics_engine()
        self._setup_ui()
    
    def _setup_ui(self):
        """UI構築"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # ヘッダー
        header = QLabel("📊 成績表")
        header.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY};")
        layout.addWidget(header)
        
        # タブ
        tabs = Qt.bWidget()
        
        # タブ1: セッション結果
        tab_session = self._create_session_results_tab()
        tabs.addTab(tab_session, "🎯 セッション結果")
        
        # タブ2: 分野別統計
        tab_category = self._create_category_stats_tab()
        tabs.addTab(tab_category, "📚 分野別統計")
        
        # タブ3: 全体統計
        tab_overall = self._create_overall_stats_tab()
        tabs.addTab(tab_overall, "📈 全体統計")
        
        # タブ4: 弱点
        tab_weak = self._create_weak_points_tab()
        tabs.addTab(tab_weak, "⚠️ 弱点克服")
        
        layout.addWidget(tabs)
        
        # ボタン
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        btn_retry = QPushButton("🔄 もう一度")
        btn_retry.clicked.connect(self.back_requested.emit)
        button_layout.addWidget(btn_retry)
        
        btn_back = QPushButton("← ダッシュボードへ")
        btn_back.clicked.connect(self.back_requested.emit)
        button_layout.addWidget(btn_back)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _create_session_results_tab(self) -> QWidget:
        """セッション結果タブ"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.session_result_label = QLabel()
        self.session_result_label.setWordWrap(True)
        self.session_result_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 14px;")
        layout.addWidget(self.session_result_label)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def _create_category_stats_tab(self) -> QWidget:
        """分野別統計タブ"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        table = Qt.bleWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["分野", "正答数", "総問題数", "正答率"])
        
        self.category_table = table
        layout.addWidget(table)
        
        widget.setLayout(layout)
        return widget
    
    def _create_overall_stats_tab(self) -> QWidget:
        """全体統計タブ"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.overall_label = QLabel()
        self.overall_label.setWordWrap(True)
        self.overall_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 12px; line-height: 1.8;")
        layout.addWidget(self.overall_label)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def _create_weak_points_tab(self) -> QWidget:
        """弱点タブ"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        table = Qt.bleWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["問題（最初50文字）", "分野", "正答率", "出題数"])
        
        self.weak_points_table = table
        layout.addWidget(table)
        
        widget.setLayout(layout)
        return widget
    
    def show_session_results(self, session_stats: dict):
        """セッション結果を表示"""
        stats = session_stats
        
        message = (
            f"正答数: {stats.get('correct_count', 0)} / {stats.get('total_questions', 0)} 問\n"
            f"正答率: {stats.get('correct_rate', 0):.1f}%\n"
            f"学習時間: {self._format_time(stats.get('elapsed_time', 0))}\n"
            f"1問当たり: {stats.get('average_time_per_question', 0):.1f} 秒\n"
            f"\n"
        )
        
        # 評価を追加
        rate = stats.get('correct_rate', 0)
        if rate >= 80:
            message += "🌟 素晴らしい！合格ラインを超えています！"
        elif rate >= 70:
            message += "👍 良好です！もう少し頑張りましょう。"
        elif rate >= 60:
            message += "📚 平均的なできです。復習が大切です。"
        else:
            message += "💪 もう一度チャレンジしてみてください。"
        
        self.session_result_label.setText(message)
    
    def show_category_statistics(self):
        """分野別統計を表示"""
        stats = self.stats_engine.calculate_category_stats()
        
        self.category_table.setRowCount(len(stats))
        
        for row, (cat_name, cat_stats) in enumerate(sorted(stats.items())):
            self.category_table.setItem(row, 0, Qt.bleWidgetItem(cat_name))
            self.category_table.setItem(row, 1, Qt.bleWidgetItem(
                str(cat_stats.get('correct_count', 0))
            ))
            self.category_table.setItem(row, 2, Qt.bleWidgetItem(
                str(cat_stats.get('total_questions', 0))
            ))
            
            rate = cat_stats.get('correct_rate', 0)
            rate_item = Qt.bleWidgetItem(f"{rate:.1f}%")
            
            # 正答率に応じて色を変更
            if rate >= 70:
                rate_item.setForeground(QColor(COLOR_CORRECT))
            else:
                rate_item.setForeground(QColor(COLOR_INCORRECT))
            
            self.category_table.setItem(row, 3, rate_item)
        
        self.category_table.resizeColumnsToContents()
    
    def show_overall_statistics(self):
        """全体統計を表示"""
        stats = self.stats_engine.get_overall_stats()
        
        total_time_str = self._format_time(stats.get('total_study_time', 0))
        
        message = (
            f"総学習回数: {stats.get('study_sessions', 0)} セッション\n"
            f"総出題数: {stats.get('total_questions_answered', 0)} 問\n"
            f"総正答数: {stats.get('total_correct', 0)} 問\n"
            f"総正答率: {stats.get('correct_rate', 0):.1f}%\n"
            f"総学習時間: {total_time_str}\n"
        )
        
        self.overall_label.setText(message)
    
    def show_weak_points(self):
        """弱点を表示"""
        weak_points = self.stats_engine.get_weak_points()
        
        self.weak_points_table.setRowCount(len(weak_points))
        
        for row, point in enumerate(weak_points):
            self.weak_points_table.setItem(row, 0, Qt.bleWidgetItem(point.get('text', '...')))
            self.weak_points_table.setItem(row, 1, Qt.bleWidgetItem(point.get('category', '')))
            
            rate_item = Qt.bleWidgetItem(f"{point.get('correct_rate', 0):.1f}%")
            rate_item.setForeground(QColor(COLOR_INCORRECT))
            self.weak_points_table.setItem(row, 2, rate_item)
            
            self.weak_points_table.setItem(row, 3, Qt.bleWidgetItem(
                str(point.get('attempt_count', 0))
            ))
        
        self.weak_points_table.resizeColumnsToContents()
    
    def update_all_statistics(self, session_stats: dict):
        """全ての統計を更新"""
        self.show_session_results(session_stats)
        self.show_category_statistics()
        self.show_overall_statistics()
        self.show_weak_points()
    
    def _format_time(self, seconds: int) -> str:
        """秒を時間:分:秒に変換"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}時間 {minutes}分 {secs}秒"
        elif minutes > 0:
            return f"{minutes}分 {secs}秒"
        else:
            return f"{secs}秒"
