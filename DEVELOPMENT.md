# ITパスポート試験学習ツール - 開発ガイド

## 📖 目次
1. [開発環境構築](#開発環境構築)
2. [プロジェクト構造](#プロジェクト構造)
3. [コード規約](#コード規約)
4. [ビルド手順](#ビルド手順)
5. [テスト方法](#テスト方法)
6. [デプロイメント](#デプロイメント)

---

## 開発環境構築

### 前提条件

- **OS**: Windows 10 以上
- **Python**: 3.11 以上
- **Git**: 最新版
- **エディタ**: Visual Studio Code（推奨）

### ステップ1: リポジトリをクローン

```bash
git clone https://github.com/yourusername/it-pass-study-tool.git
cd it-pass-study-tool
```

### ステップ2: 仮想環境を構築

```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
venv\Scripts\activate

# 有効化確認（ターミナルに (venv) が表示される）
```

### ステップ3: 依存ライブラリをインストール

```bash
# 必須ライブラリ
pip install -r requirements.txt

# 開発用ツール（オプション）
pip install pytest pytest-cov pylint black isort flake8
```

### ステップ4: エディタの設定（VS Code）

#### 拡張機能をインストール
- Python（Microsoft）
- Pylance（Microsoft）
- Black Formatter（ms-python.black-formatter）
- Pylint（ms-python.pylint）

#### .vscode/settings.json を作成

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.linting.pylintPath": "${workspaceFolder}/venv/bin/pylint",
  "python.formatting.provider": "black",
  "python.formatting.blackPath": "${workspaceFolder}/venv/bin/black",
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

### ステップ5: 開発環境確認

```bash
# Python バージョン確認
python --version

# パッケージ一覧確認
pip list

# アプリケーション起動テスト
python main.py
```

---

## プロジェクト構造

### ディレクトリツリー

```
it-pass-study-tool/
├─ main.py                      # アプリケーション エントリーポイント
├─ build_exe.py                 # PyInstaller ビルドスクリプト
├─ setup.nsi                     # NSIS インストーラー スクリプト
├─ requirements.txt              # Python 依存ライブラリ
├─ version.txt                   # バージョン情報
│
├─ .git/                         # Git リポジトリ
├─ .gitignore                    # Git 無視ファイル設定
│
├─ src/                          # ソースコード
│  ├─ __init__.py
│  ├─ ui/                        # UI モジュール
│  │  ├─ __init__.py
│  │  ├─ main_window.py          # メインウィンドウ
│  │  ├─ quiz_widget.py          # クイズウィジェット
│  │  ├─ admin_panel.py          # 管理パネル
│  │  └─ styles.py               # スタイル定義
│  │
│  ├─ db/                        # データベース モジュール
│  │  ├─ __init__.py
│  │  ├─ database.py             # DB 接続・操作
│  │  ├─ models.py               # SQLAlchemy ORM モデル
│  │  └─ schema.py               # スキーマ定義
│  │
│  ├─ core/                      # ビジネスロジック モジュール
│  │  ├─ __init__.py
│  │  ├─ quiz_engine.py          # 出題エンジン
│  │  ├─ statistics.py           # 統計計算
│  │  └─ data_manager.py         # データ管理
│  │
│  └─ utils/                     # ユーティリティ モジュール
│     ├─ __init__.py
│     ├─ importer.py             # CSV/JSON インポート
│     └─ config.py               # 設定管理
│
├─ tests/                        # ユニットテスト
│  ├─ __init__.py
│  ├─ conftest.py                # pytest 設定
│  ├─ test_quiz_engine.py        # 出題エンジン テスト
│  ├─ test_database.py           # データベース テスト
│  └─ test_ui.py                 # UI テスト
│
├─ resources/                    # リソース
│  ├─ icons/                     # アイコンファイル
│  │  └─ app.ico
│  ├─ sample_data/               # サンプルデータ
│  └─ docs/                      # ドキュメント
│
├─ build/                        # PyInstaller ビルドディレクトリ（生成）
├─ dist/                         # 実行ファイル出力ディレクトリ（生成）
│
├─ README.md                     # プロジェクト概要
├─ INSTALL.md                    # インストール手順
├─ USER_GUIDE.md                 # ユーザーガイド
├─ DEVELOPMENT.md                # 開発ガイド（このファイル）
└─ LICENSE                       # MIT ライセンス
```

---

## コード規約

### Python コード規約

本プロジェクトは **PEP 8** に準拠しています。

#### 命名規則

```python
# モジュール名: 小文字 + アンダースコア
my_module.py

# クラス名: パスカルケース
class QuizEngine:
    pass

# 関数・メソッド名: 小文字 + アンダースコア
def get_quiz_question():
    pass

# 定数: 大文字 + アンダースコア
MAX_QUESTIONS = 100
DEFAULT_TIMEOUT = 3600

# インスタンス変数: 小文字 + アンダースコア
self.quiz_manager = QuizManager()
```

#### ドキュメンテーション

すべてのモジュール、クラス、関数にはドキュメンテーション文を記述します。

```python
def get_quiz_by_category(category: str) -> list:
    """
    指定したカテゴリのクイズを取得します。
    
    Args:
        category (str): クイズのカテゴリ（例: 'IT', '経営'）
    
    Returns:
        list: クイズオブジェクトのリスト
    
    Raises:
        ValueError: カテゴリが無効な場合
    
    Example:
        >>> quizzes = get_quiz_by_category('IT')
        >>> len(quizzes) > 0
        True
    """
    pass
```

#### 型ヒント

```python
# 関数の型ヒント
def calculate_score(correct: int, total: int) -> float:
    return (correct / total) * 100

# 変数の型ヒント
questions: list[dict] = []
user_name: str = "John Doe"
```

#### インポート順序

```python
# 標準ライブラリ
import os
import sys
from pathlib import Path

# サードパーティ
import requests
from PySide6.QtWidgets import QMainWindow

# ローカルモジュール
from src.db.database import DatabaseManager
from src.core.quiz_engine import QuizEngine
```

### コード品質チェック

#### pylint でチェック

```bash
# 全ファイルをチェック
pylint src/

# 特定ファイルをチェック
pylint src/ui/main_window.py

# 設定ファイル付きでチェック
pylint --rcfile=.pylintrc src/
```

#### black でフォーマット

```bash
# 全ファイルをフォーマット
black src/ tests/

# 特定ファイルをフォーマット
black src/ui/main_window.py

# 変更を確認（実行しない）
black --diff src/
```

#### flake8 で検証

```bash
# チェック実行
flake8 src/ tests/
```

---

## ビルド手順

### EXEファイルの生成（PyInstaller）

```bash
# ビルド実行
python build_exe.py

# または、直接 PyInstaller を実行
pyinstaller --onefile --windowed \
  --icon=resources/icons/app.ico \
  --name=it-pass-study-tool \
  main.py
```

**出力:**
```
dist/
├─ it-pass-study-tool.exe
└─ _internal/（内部ファイル）
```

### インストーラーの生成（NSIS）

#### 前提条件

NSIS をインストール：
```
https://nsis.sourceforge.io/Download
```

#### ビルド手順

```bash
# NSIS インストール先へ移動
cd "C:\Program Files (x86)\NSIS\bin"

# インストーラー生成
makensis.exe C:\path\to\it-pass-study-tool\setup.nsi
```

**出力:**
```
ITPassStudyTool-1.0.0-installer.exe
```

---

## テスト方法

### テスト実行

#### 全テストを実行

```bash
pytest
```

#### 覆率レポート付きで実行

```bash
pytest --cov=src --cov-report=html
```

#### 特定のテストファイルを実行

```bash
pytest tests/test_quiz_engine.py
```

#### 特定のテストを実行

```bash
pytest tests/test_quiz_engine.py::test_get_random_quiz
```

#### verbose モード

```bash
pytest -v
```

### テスト構造

```python
# tests/test_quiz_engine.py
import pytest
from src.core.quiz_engine import QuizEngine

class TestQuizEngine:
    @pytest.fixture
    def engine(self):
        """テスト用エンジンのフィクスチャ"""
        return QuizEngine()
    
    def test_get_random_quiz(self, engine):
        """ランダムクイズ取得のテスト"""
        quiz = engine.get_random_quiz()
        assert quiz is not None
        assert 'question' in quiz
    
    def test_calculate_score(self, engine):
        """スコア計算のテスト"""
        score = engine.calculate_score(8, 10)
        assert score == 80.0
```

### CI/CD パイプライン（オプション）

GitHub Actions を使用した自動テスト：

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - run: pip install -r requirements.txt
    - run: pytest --cov=src
```

---

## デプロイメント

### リリースプロセス

#### ステップ1: バージョン更新

```bash
# version.txt を更新
echo "1.0.1" > version.txt

# main.py のバージョン表示を更新
```

#### ステップ2: EXEビルド

```bash
python build_exe.py
```

#### ステップ3: インストーラー生成

```bash
cd "C:\Program Files (x86)\NSIS\bin"
makensis.exe C:\path\to\setup.nsi
```

#### ステップ4: テスト

```bash
# インストーラーで実際にインストール＆起動確認
# dist\it-pass-study-tool.exe で動作確認
```

#### ステップ5: リリースノート作成

```markdown
# リリースノート v1.0.1

## 新機能
- 復習モード改善

## バグ修正
- データベース接続エラーを修正

## インストーラー
- ITPassStudyTool-1.0.1-installer.exe
```

#### ステップ6: Git コミット・タグ

```bash
git add version.txt README.md
git commit -m "Release v1.0.1"
git tag -a v1.0.1 -m "Release version 1.0.1"
git push origin main --tags
```

#### ステップ7: GitHub Releases へアップロード

1. GitHub でリポジトリを開く
2. "Releases" タブをクリック
3. "Draft a new release" をクリック
4. タグを選択
5. リリースノートを入力
6. インストーラーと EXE をアップロード
7. "Publish release" をクリック

---

## デバッグとトラブルシューティング

### デバッグモードで実行

```python
# main.py に debug フラグを追加
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 関数内で
logger.debug(f"Variable value: {variable}")
```

### VS Code でのデバッグ

`.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Debug",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```

### よくある問題と解決策

#### ImportError: モジュールが見つからない

```bash
# 依存ライブラリを再インストール
pip install -r requirements.txt --force-reinstall
```

#### PySide6 が起動しない

```bash
# Visual C++ 再配布可能ファイルをインストール
# https://support.microsoft.com/downloads/

# または、仮想環境を再構築
deactivate
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### データベースロック

```bash
# 全ての Python プロセスを終了
taskkill /F /IM python.exe

# または、data.db を削除
del %APPDATA%\ITPassStudyTool\data.db
```

---

## 参考リソース

- **PEP 8**: https://www.python.org/dev/peps/pep-0008/
- **PySide6**: https://doc.qt.io/qtforpython/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **pytest**: https://docs.pytest.org/
- **PyInstaller**: https://pyinstaller.readthedocs.io/
- **NSIS**: https://nsis.sourceforge.io/

---

## 📞 開発サポート

質問や提案がある場合：
- GitHub Issues で報告
- Discussions で相談
- Pull Request で提案

**ご質問ありがとうございます。皆様の貢献をお待ちしています！** 🚀
