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
