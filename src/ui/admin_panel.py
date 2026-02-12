"""
管理パネル - 問題管理・データインポート
"""

from PySide6.Qt.idgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, Qt.bWidget,
    Qt.bleWidget, Qt.bleWidgetItem, QFileDialog, QMessageBox, QSpinBox,
    QComboBox, QLineEdit, Qt.xtEdit, QFormLayout, QGroupBox
)
from PySide6.Qt.ore import Qt. Signal
from PySide6.Qt.ui import QFont

from src.ui.styles import (
    COLOR_PRIMARY, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, PADDING_MEDIUM
)


class AdminPanel(QWidget):
    """管理パネル"""
    
    back_requested = Signal()
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
    
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
        tabs = Qt.bWidget()
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
    
    def _create_import_tab(self) -> QWidget:
        """データインポートタブ"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 説明
        desc = QLabel(
            "以下の形式でデータをインポートできます:\n"
            "• CSV ファイル\n"
            "• JSON ファイル\n"
            "• Excel ファイル"
        )
        desc.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY};")
        layout.addWidget(desc)
        
        layout.addSpacing(15)
        
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
        
        # サンプルフォーマット
        group = QGroupBox("CSVフォーマット例")
        group_layout = QVBoxLayout()
        sample = Qt.xtEdit()
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
        combo_category = QComboBox()
        combo_category.addItem("すべて")
        filter_layout.addWidget(combo_category)
        
        filter_layout.addWidget(QLabel("年度:"))
        combo_year = QComboBox()
        combo_year.addItem("すべて")
        filter_layout.addWidget(combo_year)
        
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)
        
        # 問題テーブル
        table = Qt.bleWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "問題番号", "年度", "分野", "問題文 (最初50字)", "難易度", "操作"
        ])
        table.setRowCount(0)
        layout.addWidget(table)
        
        # ボタン
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        btn_add = QPushButton("➕ 追加")
        btn_add.clicked.connect(self._add_question)
        button_layout.addWidget(btn_add)
        
        btn_edit = QPushButton("✏️ 編集")
        button_layout.addWidget(btn_edit)
        
        btn_delete = QPushButton("🗑️ 削除")
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
        
        stats_layout.addRow("総回答数:", QLabel("0問"))
        stats_layout.addRow("正答数:", QLabel("0問"))
        stats_layout.addRow("正答率:", QLabel("0%"))
        stats_layout.addRow("総学習時間:", QLabel("0時間 0分"))
        stats_layout.addRow("登録問題数:", QLabel("0問"))
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # グラフ（将来実装）
        chart_group = QGroupBox("分野別正答率")
        chart_layout = QVBoxLayout()
        chart_label = QLabel("グラフはここに表示されます\n(実装予定)")
        chart_label.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY}; text-align: center;")
        chart_layout.addWidget(chart_label)
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
        
        # 保存ボタン
        btn_save = QPushButton("💾 設定を保存")
        btn_save.clicked.connect(lambda: QMessageBox.information(self, "保存", "設定を保存しました。"))
        layout.addWidget(btn_save)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def _import_csv(self):
        """CSVインポート"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "CSVファイルを選択", "", "CSV Files (*.csv)"
        )
        if file_path:
            QMessageBox.information(self, "インポート", f"ファイルを読み込みました: {file_path}\n実装予定")
    
    def _import_json(self):
        """JSONインポート"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "JSONファイルを選択", "", "JSON Files (*.json)"
        )
        if file_path:
            QMessageBox.information(self, "インポート", f"ファイルを読み込みました: {file_path}\n実装予定")
    
    def _import_excel(self):
        """Excelインポート"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Excelファイルを選択", "", "Excel Files (*.xlsx *.xls)"
        )
        if file_path:
            QMessageBox.information(self, "インポート", f"ファイルを読み込みました: {file_path}\n実装予定")
    
    def _add_question(self):
        """問題追加"""
        QMessageBox.information(self, "問題追加", "問題追加ダイアログ\n実装予定")
    
    def _edit_question(self):
        """問題編集"""
        QMessageBox.information(self, "問題編集", "問題編集ダイアログ\n実装予定")
