"""
メインウィンドウ - アプリケーションのメイン UI
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QPushButton, QLabel, QTabWidget, QMenuBar, QMenu, QMessageBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont

from src.ui.styles import MAIN_STYLESHEET, COLOR_PRIMARY, COLOR_TEXT_PRIMARY
from src.ui.quiz_widget import QuizWidget
from src.ui.admin_panel import AdminPanel


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


