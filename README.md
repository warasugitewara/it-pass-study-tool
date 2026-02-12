# ITパスポート試験学習ツール

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Windows](https://img.shields.io/badge/platform-Windows%2010%2B-blue.svg)

## 📋 概要

**ITパスポート試験学習ツール** は、ITパスポート試験の合格を支援する Windows GUIアプリケーションです。複数の出題方式と学習進捗の可視化により、効率的で継続的な学習をサポートします。

**特徴:**
- ✅ **複数出題方式**: ランダム出題、年度別、分野別、復習モード
- 📊 **進捗可視化**: リアルタイムの成績追跡と統計表示
- 🎯 **集中学習**: シンプルで直感的なUI設計
- 💾 **データ管理**: テスト結果の自動保存とエクスポート機能
- ⚡ **高速動作**: ローカルデータベースによるレスポンス

**技術スタック:**
- Python 3.11+
- PySide6（モダンなGUIフレームワーク）
- SQLite + SQLAlchemy（データベース管理）
- PyInstaller（実行ファイル生成）

---

## 🚀 インストール・セットアップ

### 方法1: インストーラーを使用（推奨）

Windows用スタンドアロン実行ファイル：

```bash
# インストーラーをダウンロード
ITPassStudyTool-1.0.0-installer.exe

# ダブルクリックして実行
```

詳細は [INSTALL.md](INSTALL.md) を参照してください。

### 方法2: ソースコードから実行

**前提条件:**
- Python 3.11 以上
- pip パッケージマネージャー

**セットアップ手順:**

```bash
# 1. リポジトリをクローン
git clone https://github.com/yourusername/it-pass-study-tool.git
cd it-pass-study-tool

# 2. 仮想環境を構築
python -m venv venv
venv\Scripts\activate

# 3. 依存ライブラリをインストール
pip install -r requirements.txt

# 4. アプリケーション起動
python main.py
```

### 方法3: 実行ファイルから起動

```bash
# EXEファイルのビルド（PyInstaller必要）
python build_exe.py

# 生成されたEXEを実行
dist\it-pass-study-tool.exe
```

---

## 📚 ドキュメント

| ドキュメント | 説明 |
|---|---|
| [INSTALL.md](INSTALL.md) | インストール・セットアップの詳細手順 |
| [USER_GUIDE.md](USER_GUIDE.md) | UI操作ガイドと機能チュートリアル |
| [DEVELOPMENT.md](DEVELOPMENT.md) | 開発環境構築とコード構造 |
| [version.txt](version.txt) | バージョン情報（v1.0.0） |

---

## ⌨️ クイックスタート

### アプリケーション起動後

1. **デフォルト設定で開始**
   - 「ランダム出題」を選択
   - 「テスト開始」をクリック

2. **問題に回答**
   - 選択肢をクリック、または A/B/C/D キーで選択
   - 「次へ」で次問題へ進む

3. **結果確認**
   - テスト完了後、成績と分野別成績が表示される
   - 「詳細結果」で詳しい分析を確認

詳細なガイドは [USER_GUIDE.md](USER_GUIDE.md) を参照。

---

## ✨ 主要機能

### 1. 複数出題方式

| 方式 | 説明 | 用途 |
|---|---|---|
| **ランダム出題** | 全問題からランダムに出題 | 全体実力確認 |
| **年度別** | 特定の年度の問題を出題 | 過去問演習 |
| **分野別** | 特定分野の問題を出題 | 苦手分野克服 |
| **復習モード** | 間違えた問題を再出題 | 弱点強化 |

### 2. 学習進捗管理

- 正答率の自動計算と履歴管理
- 分野別成績の可視化
- テスト結果の自動保存
- 学習時間の追跡

### 3. データ管理

- **エクスポート**: CSV/JSON形式で結果出力
- **インポート**: 外部データの取り込み
- **バックアップ**: 学習データの保護

### 4. ユーザー設定

- ダークモード対応
- フォントサイズ調整
- テスト時間制限設定
- 自動保存機能

---

## 📊 画面構成

### メイン画面
```
├─ 学習状況パネル（正答率・解答数・進捗）
├─ 出題方式選択
└─ テスト開始ボタン
```

### テスト画面
```
├─ 問題表示エリア
├─ 選択肢表示（A～D）
└─ ナビゲーションボタン（前へ・次へ・終了）
```

### 結果画面
```
├─ 成績サマリー（正答数・正答率）
├─ 分野別成績グラフ
└─ アクション（詳細結果・解き直す・メニューへ）
```

---

## 🎨 ディレクトリ構造
```
it-pass-study-tool/
├── main.py                 # アプリケーションエントリーポイント
├── requirements.txt        # 依存ライブラリ
├── README.md              # このファイル
├── src/
│   ├── ui/                # GUI 関連モジュール
│   │   ├── main_window.py
│   │   ├── quiz_widget.py
│   │   ├── admin_panel.py
│   │   └── styles.py      # テーマ・スタイル定義
│   ├── db/                # データベース関連
│   │   ├── models.py      # SQLAlchemy ORM モデル
│   │   ├── database.py    # DB接続・操作
│   │   └── schema.py      # スキーマ定義
│   ├── core/              # ビジネスロジック
│   │   ├── quiz_engine.py # 出題エンジン
│   │   ├── statistics.py  # 統計計算
│   │   └── data_manager.py # データ管理
│   ├── utils/             # ユーティリティ
│   │   ├── importer.py    # CSV/JSON インポート
│   │   └── config.py      # 設定ファイル
│   └── __init__.py
├── resources/             # リソース（アイコン、データ等）
│   ├── icons/
│   ├── sample_data/       # サンプル問題データ
│   └── docs/
├── tests/                 # ユニットテスト
│   ├── test_quiz_engine.py
│   ├── test_database.py
│   └── conftest.py
├── .gitignore
└── build/                 # ビルド・配布ファイル（.gitignore）
```

---

## 🔧 開発・ビルド

### 開発環境構築

```bash
# 仮想環境の作成
python -m venv venv
venv\Scripts\activate

# 依存ライブラリのインストール
pip install -r requirements.txt

# 開発用パッケージのインストール
pip install pytest pytest-cov pylint black
```

### テストの実行

```bash
# 全テストを実行
pytest

# 覆率レポート付き実行
pytest --cov=src

# 特定のテストファイルを実行
pytest tests/test_quiz_engine.py
```

### EXEファイルの生成

```bash
# PyInstallerでビルド
python build_exe.py

# 生成されたEXE
dist\it-pass-study-tool.exe
```

### NSISインストーラーの生成

```bash
# NSIS がインストール済みの場合
cd "C:\Program Files (x86)\NSIS"
makensis.exe C:\path\to\setup.nsi

# 生成されたインストーラー
ITPassStudyTool-1.0.0-installer.exe
```

詳細は [DEVELOPMENT.md](DEVELOPMENT.md) を参照。

---

## 📈 バージョン情報

**最新バージョン**: 1.0.0  
**リリース日**: 2026/2/16  
**Python**: 3.11+

詳細は [version.txt](version.txt) と [release_notes.md](release_notes.md) を参照。

---

## 🤝 貢献ガイドライン

本プロジェクトへの貢献を歓迎します。

### 手順

1. Fork してリポジトリをクローン
2. 機能ブランチを作成（`git checkout -b feature/amazing-feature`）
3. 変更をコミット（`git commit -m 'Add amazing feature'`）
4. ブランチにプッシュ（`git push origin feature/amazing-feature`）
5. Pull Request を作成

### コード規約

- PEP 8 に準拠
- 関数・クラスにはドキュメンテーション文を記述
- テストコードを含める（覆率 80% 以上）

---

## 🐛 バグ報告・機能リクエスト

Issues タブからお願いします。

- **バグ報告**: `[Bug]` タグを付けて、再現手順を記述
- **機能リクエスト**: `[Feature]` タグを付けて、用途と期待動作を記述

---

## 📝 ライセンス

MIT License

本プロジェクトはMITライセンスの下で公開されています。
詳細は [LICENSE](LICENSE) ファイルを参照。

### 免責事項

本ツールはITパスポート試験学習支援を目的としています。著作権法の範囲内で使用してください。

---

## 📞 お問い合わせ

- **GitHub Issues**: https://github.com/yourusername/it-pass-study-tool/issues
- **Discussions**: https://github.com/yourusername/it-pass-study-tool/discussions

---

**ITパスポート試験合格を応援します。頑張ってください！** 🎓
