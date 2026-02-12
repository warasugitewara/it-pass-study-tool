"""
UI モジュール初期化
"""

from src.ui.main_window import MainWindow
from src.ui.styles import MAIN_STYLESHEET

__all__ = ['MainWindow', 'MAIN_STYLESHEET']
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
"""
メインウィンドウ - アプリケーションのメイン UI
"""

from PySide6.Qt.idgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QPushButton, QLabel, Qt.bWidget, QMenuBar, QMenu, QMessageBox
)
from PySide6.Qt.ore import Qt. QSize
from PySide6.Qt.ui import QIcon, QFont

from src.ui.styles import MAIN_STYLESHEET, COLOR_PRIMARY, COLOR_TEXT_PRIMARY
from src.ui.quiz_widget import QuizWidget
from src.ui.admin_panel import AdminPanel
from src.ui.results_widget import ResultsWidget


class MainWindow(QMainWindow):
    """アプリケーションメインウィンドウ"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ITパスポート試験学習ツール")
        self.setWindowIcon(QIcon())  # ここにアイコンを設定可能
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(QSize(1000, 700))
        
        # スタイルシート適用
        self.setStyleSheet(MAIN_STYLESHEET)
        
        # UI構築
        self._setup_ui()
        self._setup_menu()
    
    def _setup_ui(self):
        """UI要素のセットアップ"""
        # 中央ウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ヘッダー
        header_widget = self._create_header()
        main_layout.addWidget(header_widget)
        
        # スタック: 異なるモード間の切り替え用
        self.stacked_widget = QStackedWidget()
        
        # メニュー/ダッシュボード画面
        self.dashboard_widget = self._create_dashboard()
        self.stacked_widget.addWidget(self.dashboard_widget)
        
        # クイズ画面
        self.quiz_widget = QuizWidget()
        self.quiz_widget.back_requested.connect(self._show_dashboard)
        self.stacked_widget.addWidget(self.quiz_widget)
        
        # 結果画面
        self.results_widget = ResultsWidget()
        self.results_widget.back_requested.connect(self._show_dashboard)
        self.stacked_widget.addWidget(self.results_widget)
        
        # 管理画面
        self.admin_panel = AdminPanel()
        self.admin_panel.back_requested.connect(self._show_dashboard)
        self.stacked_widget.addWidget(self.admin_panel)
        
        main_layout.addWidget(self.stacked_widget, 1)
        central_widget.setLayout(main_layout)
        
        # 最初はダッシュボード表示
        self.stacked_widget.setCurrentWidget(self.dashboard_widget)
    
    def _create_header(self) -> QWidget:
        """ヘッダー作成"""
        header = QWidget()
        header.setStyleSheet(f"background-color: {COLOR_PRIMARY}; padding: 15px;")
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        
        title_label = QLabel("📚 ITパスポート試験学習ツール")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY};")
        
        layout.addWidget(title_label)
        layout.addStretch()
        
        header.setLayout(layout)
        return header
    
    def _create_dashboard(self) -> QWidget:
        """ダッシュボード画面作成"""
        dashboard = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # タイトル
        title = QLabel("学習を始めましょう")
        title_font = QFont("Segoe UI", 24, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY};")
        layout.addWidget(title)
        
        # 説明
        description = QLabel(
            "以下から学習モードを選択してください:\n"
            "• ランダムモード: ランダムに問題が出題されます\n"
            "• 年度別: 特定年度の問題に絞って学習できます\n"
            "• 分野別: 特定分野を集中学習できます\n"
            "• 復習モード: 正答率が低い問題を優先的に出題します"
        )
        description.setStyleSheet(f"color: #CBD5E1; font-size: 13px; line-height: 1.6;")
        layout.addWidget(description)
        
        layout.addSpacing(30)
        
        # ボタングループ
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        # ランダムモード
        btn_random = QPushButton("🎲 ランダムモード\n出題問題数を指定")
        btn_random.setMinimumHeight(80)
        btn_random.clicked.connect(lambda: self._start_quiz("random"))
        button_layout.addWidget(btn_random)
        
        # 年度別
        btn_year = QPushButton("📅 年度別\n特定年度を選択")
        btn_year.setMinimumHeight(80)
        btn_year.clicked.connect(lambda: self._start_quiz("year"))
        button_layout.addWidget(btn_year)
        
        # 分野別
        btn_category = QPushButton("🏆 分野別\n得意・不得意を克服")
        btn_category.setMinimumHeight(80)
        btn_category.clicked.connect(lambda: self._start_quiz("category"))
        button_layout.addWidget(btn_category)
        
        # 復習モード
        btn_review = QPushButton("🔄 復習モード\n弱点集中学習")
        btn_review.setMinimumHeight(80)
        btn_review.clicked.connect(lambda: self._start_quiz("review"))
        button_layout.addWidget(btn_review)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        # 管理・設定ボタン
        admin_button_layout = QHBoxLayout()
        admin_button_layout.addStretch()
        
        btn_admin = QPushButton("⚙️ 問題管理・設定")
        btn_admin.setMinimumWidth(150)
        btn_admin.clicked.connect(self._show_admin)
        admin_button_layout.addWidget(btn_admin)
        
        layout.addLayout(admin_button_layout)
        
        dashboard.setLayout(layout)
        return dashboard
    
    def _start_quiz(self, mode: str):
        """クイズ開始"""
        self.quiz_widget.initialize(mode)
        self.stacked_widget.setCurrentWidget(self.quiz_widget)
    
    def show_results(self, session_stats: dict):
        """結果表示画面を表示"""
        self.results_widget.update_all_statistics(session_stats)
        self.stacked_widget.setCurrentWidget(self.results_widget)
    
    def _show_dashboard(self):
        """ダッシュボード表示"""
        self.stacked_widget.setCurrentWidget(self.dashboard_widget)
    
    def _show_admin(self):
        """管理画面表示"""
        self.stacked_widget.setCurrentWidget(self.admin_panel)
    
    def _setup_menu(self):
        """メニューバー作成"""
        menubar = self.menuBar()
        menubar.setStyleSheet(f"background-color: #1E293B; color: {COLOR_TEXT_PRIMARY};")
        
        # ファイルメニュー
        file_menu = menubar.addMenu("ファイル(&F)")
        exit_action = file_menu.addAction("終了(&E)")
        exit_action.triggered.connect(self.close)
        
        # 学習メニュー
        study_menu = menubar.addMenu("学習(&S)")
        random_action = study_menu.addAction("ランダム出題")
        random_action.triggered.connect(lambda: self._start_quiz("random"))
        
        year_action = study_menu.addAction("年度別")
        year_action.triggered.connect(lambda: self._start_quiz("year"))
        
        category_action = study_menu.addAction("分野別")
        category_action.triggered.connect(lambda: self._start_quiz("category"))
        
        # ツールメニュー
        tools_menu = menubar.addMenu("ツール(&T)")
        admin_action = tools_menu.addAction("問題管理・設定")
        admin_action.triggered.connect(self._show_admin)
        
        # ヘルプメニュー
        help_menu = menubar.addMenu("ヘルプ(&H)")
        about_action = help_menu.addAction("このアプリについて(&A)")
        about_action.triggered.connect(self._show_about)
    
    def _show_about(self):
        """アバウトダイアログ表示"""
        QMessageBox.about(
            self,
            "このアプリについて",
            "ITパスポート試験学習ツール v1.0\n\n"
            "ITパスポート試験の効率的な学習をサポートします。\n"
            "集中力を重視したシンプルなデザインで、\n"
            "快適な学習環境を提供します。\n\n"
            "© 2026 - Private Use"
        )
"""
クイズ設定ダイアログ - 出題モード・フィルター選択
"""

from PySide6.Qt.idgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSpinBox,
    QCheckBox, QGroupBox, QMessageBox, QScrollArea, QWidget
)
from PySide6.Qt.ore import Qt. Signal
from PySide6.Qt.ui import QFont

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
"""
クイズ画面ウィジェット
問題出題・回答・結果表示を担当
"""

from PySide6.Qt.idgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QRadioButton,
    QButtonGroup, QProgressBar, QSpinBox, QComboBox, QMessageBox, QDialog
)
from PySide6.Qt.ore import Qt. Signal, Qt.mer, Qt.me
from PySide6.Qt.ui import QFont

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
        self.timer = Qt.mer()
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
        
        # 最後の問題の場合は結果表示
        if self.engine.get_current_index() >= self.engine.get_question_count() - 1:
            self._show_results()
            return
        
        # 次の問題へ
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
        
        if results and self.parentWidget() and hasattr(self.parentWidget().parentWidget(), 'show_results'):
            # メインウィンドウの show_results メソッドを呼び出す
            self.parentWidget().parentWidget().show_results(results)
        else:
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
"""
UI スタイル・テーマ定義
集中力を重視したミニマルデザイン
"""

# カラーパレット（集中力重視：ダークモード・青系）
COLOR_PRIMARY = "#1E3A8A"        # 深い青（ヘッダー、強調色）
COLOR_SECONDARY = "#2D5AA8"      # 明るい青（サブヘッダー）
COLOR_BACKGROUND = "#0F172A"     # 深紺（背景）
COLOR_SURFACE = "#1E293B"        # 濃い灰色（カード・パネル背景）
COLOR_TEXT_PRIMARY = "#F1F5F9"   # ほぼ白（主要テキスト）
COLOR_TEXT_SECONDARY = "#CBD5E1" # 薄い灰色（サブテキスト）
COLOR_BORDER = "#334155"         # グレー（ボーダー）

# ステータスカラー
COLOR_CORRECT = "#10B981"        # 緑（正解）
COLOR_INCORRECT = "#EF4444"      # 赤（不正解）
COLOR_UNANSWERED = "#6B7280"     # 灰色（未回答）
COLOR_ACCENT = "#3B82F6"         # 鮮やかな青（アクセント）

# フォント設定
FONT_FAMILY = "Segoe UI, Arial, sans-serif"
FONT_SIZE_TITLE = 16
FONT_SIZE_HEADING = 14
FONT_SIZE_NORMAL = 12
FONT_SIZE_SMALL = 10

# 間隔・パディング
PADDING_LARGE = 20
PADDING_MEDIUM = 15
PADDING_SMALL = 10

MARGIN_LARGE = 20
MARGIN_MEDIUM = 15
MARGIN_SMALL = 10

# ボーダー
BORDER_RADIUS = 6
BORDER_WIDTH = 1

# PySide6 スタイルシート
MAIN_STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {COLOR_BACKGROUND};
    color: {COLOR_TEXT_PRIMARY};
}}

QLabel {{
    color: {COLOR_TEXT_PRIMARY};
    font-family: {FONT_FAMILY};
}}

QPushButton {{
    background-color: {COLOR_PRIMARY};
    color: {COLOR_TEXT_PRIMARY};
    border: none;
    border-radius: {BORDER_RADIUS}px;
    padding: 10px 15px;
    font-size: {FONT_SIZE_NORMAL}px;
    font-weight: bold;
    font-family: {FONT_FAMILY};
}}

QPushButton:hover {{
    background-color: {COLOR_SECONDARY};
}}

QPushButton:pressed {{
    background-color: #152E4D;
}}

QPushButton:disabled {{
    background-color: {COLOR_BORDER};
    color: {COLOR_TEXT_SECONDARY};
}}

QLineEdit, Qt.xtEdit, QComboBox {{
    background-color: {COLOR_SURFACE};
    color: {COLOR_TEXT_PRIMARY};
    border: {BORDER_WIDTH}px solid {COLOR_BORDER};
    border-radius: {BORDER_RADIUS}px;
    padding: 8px;
    font-family: {FONT_FAMILY};
    selection-background-color: {COLOR_PRIMARY};
}}

QLineEdit:focus, Qt.xtEdit:focus, QComboBox:focus {{
    border: {BORDER_WIDTH}px solid {COLOR_ACCENT};
}}

QCheckBox, QRadioButton {{
    color: {COLOR_TEXT_PRIMARY};
    font-family: {FONT_FAMILY};
}}

QCheckBox::indicator, QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    background-color: {COLOR_SURFACE};
    border: {BORDER_WIDTH}px solid {COLOR_BORDER};
    border-radius: 3px;
}}

QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
    background-color: {COLOR_PRIMARY};
}}

QGroupBox {{
    color: {COLOR_TEXT_PRIMARY};
    border: {BORDER_WIDTH}px solid {COLOR_BORDER};
    border-radius: {BORDER_RADIUS}px;
    margin-top: 10px;
    padding-top: 10px;
    font-family: {FONT_FAMILY};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
}}

Qt.bWidget::pane {{
    border: {BORDER_WIDTH}px solid {COLOR_BORDER};
}}

Qt.bBar::tab {{
    background-color: {COLOR_SURFACE};
    color: {COLOR_TEXT_SECONDARY};
    padding: 8px 15px;
    border: none;
    font-family: {FONT_FAMILY};
}}

Qt.bBar::tab:selected {{
    background-color: {COLOR_PRIMARY};
    color: {COLOR_TEXT_PRIMARY};
}}

Qt.bleWidget {{
    background-color: {COLOR_BACKGROUND};
    alternate-background-color: {COLOR_SURFACE};
    gridline-color: {COLOR_BORDER};
    border: none;
    font-family: {FONT_FAMILY};
}}

Qt.bleWidget::item {{
    padding: 5px;
}}

QHeaderView::section {{
    background-color: {COLOR_PRIMARY};
    color: {COLOR_TEXT_PRIMARY};
    padding: 5px;
    border: none;
    font-family: {FONT_FAMILY};
    font-weight: bold;
}}

QProgressBar {{
    background-color: {COLOR_SURFACE};
    border: {BORDER_WIDTH}px solid {COLOR_BORDER};
    border-radius: {BORDER_RADIUS}px;
    text-align: center;
    color: {COLOR_TEXT_PRIMARY};
}}

QProgressBar::chunk {{
    background-color: {COLOR_ACCENT};
    border-radius: 4px;
}}

QScrollBar:vertical {{
    background-color: {COLOR_BACKGROUND};
    width: 10px;
    border: none;
}}

QScrollBar::handle:vertical {{
    background-color: {COLOR_BORDER};
    border-radius: 5px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLOR_SECONDARY};
}}

QMenuBar {{
    background-color: {COLOR_SURFACE};
    color: {COLOR_TEXT_PRIMARY};
    border-bottom: {BORDER_WIDTH}px solid {COLOR_BORDER};
}}

QMenu {{
    background-color: {COLOR_SURFACE};
    color: {COLOR_TEXT_PRIMARY};
    border: {BORDER_WIDTH}px solid {COLOR_BORDER};
}}

QMenu::item:selected {{
    background-color: {COLOR_PRIMARY};
}}
"""

# 通知・ステータスメッセージのスタイル
NOTIFICATION_SUCCESS = f"background-color: {COLOR_CORRECT}; color: white; padding: 10px; border-radius: 5px;"
NOTIFICATION_ERROR = f"background-color: {COLOR_INCORRECT}; color: white; padding: 10px; border-radius: 5px;"
NOTIFICATION_WARNING = f"background-color: #F59E0B; color: white; padding: 10px; border-radius: 5px;"
NOTIFICATION_INFO = f"background-color: {COLOR_ACCENT}; color: white; padding: 10px; border-radius: 5px;"
