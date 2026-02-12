# ITパスポート試験学習ツール

## 概要
Windows GUIアプリケーション。ITパスポート試験の過去問学習に特化した学習支援ツール。

**特徴:**
- 複数の出題方式（ランダム、年度別、分野別、復習モード）
- 学習進捗の可視化
- 集中力を重視したシンプルなUI設計

**技術スタック:**
- Python 3.11+
- PyQt6（GUI）
- SQLite + SQLAlchemy（データ管理）

---

## セットアップ

### 1. 環境準備
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. プロジェクト起動
```bash
python main.py
```

---

## ディレクトリ構造
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

## 開発進捗

### Phase 1: 基盤構築（進行中）
- [x] Git リポジトリ初期化
- [x] 依存ライブラリ固定
- [ ] プロジェクト構造作成
- [ ] データベーススキーマ実装
- [ ] 基本GUI フレームワーク
- [ ] 手動データ入力機能

### Phase 2: 出題エンジン
- [ ] 出題ロジック実装
- [ ] 統計・進捗表示
- [ ] 回答履歴管理

### Phase 3: データ取得自動化
- [ ] API検索
- [ ] スクレイピング実装

### Phase 4: UI/UX改善
- [ ] デザイン洗練
- [ ] テスト・デバッグ
- [ ] 実行ファイル化

---

## ライセンス
プライベート用途（個人使用）

## 注記
本ツールはITパスポート試験学習用です。著作権法の範囲内で使用してください。
