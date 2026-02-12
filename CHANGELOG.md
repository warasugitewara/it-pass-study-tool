# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-02-12

### ✨ Added
- **10年分の公式ITパスポート試験問題データセット** (280問)
  - 2025年度～2016年度まで10年分の問題を統合
  - IPA公式サイトから直接ダウンロードした問題冊子と解答例
  - ストラテジ、マネジメント、テクノロジの3カテゴリで均衡した構成
  - 各問題に難易度レベル (1-3) を付与
  
- **効率的なデータ管理**
  - `all_questions_10years.json`: 統合マスターデータセット
  - 年度別個別ファイル: `sample_questions_<year>_<code>.json`
  - 自動初期ロード: アプリ起動時に280問を自動読み込み

- **PDF ダウンロード機能**
  - IPA公式から全年度のPDF自動ダウンロード (60MB)
  - マニフェスト管理: ダウンロード履歴と整合性チェック
  - キャッシュ機能: 既存ファイルの重複DLを回避

### 🔧 Fixed
- バージョン管理: 1.0.0 → 1.1.0 に更新
- データローディング: 10問 → 280問に対応
- EXEサイズ最適化: 96MB → 123MB (データセット含む)

### 📦 Changed
- デフォルトサンプルデータ: 春データ (10問) → 10年統合データ (280問)
- アプリ初回起動時のロード対象: sample_questions_2024_spring.json → all_questions_10years.json
- MSIインストーラ: 121.91 MB (旧95.45MB から約28%増加、データ拡充のため)

### 📊 Dataset Details
- **Total Questions**: 280問
- **Years Covered**: 2025年度 ～ 2016年度 (10年度)
- **Categories**: 
  - ストラテジ (Strategy): 93問
  - マネジメント (Management): 92問
  - テクノロジ (Technology): 95問
- **Difficulty Distribution**: レベル1-3でバランス配置
- **Source**: IPA Official (情報処理推進機構)

---

## [1.0.0] - 2026-02-12

### ✨ Added
- **Webスクレイピング機能**: itpassportsiken.com から過去問データを自動取得
  - 過去問年度・季節情報を自動抽出
  - 問題文、選択肢、解説を自動採集
  - 重複チェック機能で同じ問題の重複登録を防止
  - バリデーション機能で不正なデータを自動排除
  - エラーハンドリングとタイムアウト対応
  
- **Admin Panel データ管理機能**
  - 「サンプルデータロード」ボタン: 初期データの手動ロード
  - 「Webスクレイピング」ボタン: オンデマンドスクレイピング実行
  - スクレイピング進捗表示とログビューア
  - スクレイピング統計情報表示（取得数、追加数、重複数、エラー数）

- **自動サンプルデータロード**: アプリ初回起動時に sample_questions_2024_spring.json を自動ロード

- **MSI インストーラー対応**
  - WiX 4/6 互換の Windows Installer 生成
  - Per-user インストール（LocalAppData）
  - スタートメニュー＆デスクトップショートカット自動作成
  - アンインストール機能対応

### 🔧 Fixed
- **results_widget.py**: 10個の Qt API タイポ修正
- **database.py**: PyInstaller EXE 互換性修正
- **build_exe.py**: PyInstaller hidden imports 修正
- **build_wix_msi.py**: WiX XML スキーマ完全書き直し

### 📦 Changed
- **インストール場所**: `Program Files\ITPassStudyTool\` → `AppData\Local\ITPassStudyTool\` (Per-user)
- **インストーラー形式**: NSIS → WiX 6.0 に統一
- **データベース場所**: プロジェクト相対パス → `%APPDATA%\ITPassStudyTool\data\` (PyInstaller対応)

---

## Installation & Usage

### インストール
```bash
# MSI インストーラーからインストール
msiexec /i ITPassStudyTool-1.1.0.msi

# または、スタンドアロン EXE を実行
it-pass-study-tool.exe
```

### データロード
1. アプリ起動時に自動的に280問の統合データをロード
2. Admin Panel → Import タブ でCSV/JSON追加インポート可能
3. または 「サンプルデータロード」で手動ロード

### アンインストール
```bash
msiexec /x ITPassStudyTool-1.1.0.msi
```

---

## System Requirements

- **OS**: Windows 10 以上
- **Python**: 3.10+ (ソース実行の場合)
- **RAM**: 512 MB 以上推奨
- **Disk Space**: 200 MB 以上

---

## Credits

- **Framework**: PySide6
- **Database**: SQLite + SQLAlchemy
- **Build Tools**: PyInstaller, WiX 6.0
- **Data Source**: IPA Official (情報処理推進機構)

---

**Happy Learning! 🎓**
