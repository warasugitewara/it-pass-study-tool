# Changelog

All notable changes to this project will be documented in this file.

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
  - `Qt.bWidget()` → `QTabWidget()`
  - `Qt.bleWidget()` → `QTableWidget()`
  - `Qt.bleWidgetItem()` → `QTableWidgetItem()`

- **database.py**: PyInstaller EXE 互換性修正
  - 相対パスから `%APPDATA%\ITPassStudyTool\data\` に変更
  - データベースが `C:\Users\<user>\AppData\Roaming\ITPassStudyTool\data\app.db` に永続化

- **build_exe.py**: PyInstaller hidden imports 修正
  - 25+ モジュール参照の修正
  - `src.utils.scraper`, `apscheduler` など実際に存在するモジュールを指定

- **build_wix_msi.py**: WiX XML スキーマ完全書き直し
  - WiX 3.x 形式 (Product) → WiX 4/6 形式 (Package) に変更
  - コンポーネント GUID の正確化
  - レジストリキー設定の修正

### 📦 Changed
- **インストール場所**: `Program Files\ITPassStudyTool\` → `AppData\Local\ITPassStudyTool\` (Per-user)
- **インストーラー形式**: NSIS → WiX 6.0 に統一
- **データベース場所**: プロジェクト相対パス → `%APPDATA%\ITPassStudyTool\data\` (PyInstaller対応)

### 🐛 Deprecated
- NSIS インストーラー生成スクリプト (WiX に統一)

### 📋 Known Issues
- Webスクレイピングは itpassportsiken.com の HTML 構造に依存
- 変更があった場合、スクレイパーのクラス名マッピングを調整が必要

---

## Installation & Usage

### インストール
```bash
# MSI インストーラーからインストール
msiexec /i ITPassStudyTool-1.0.0.msi

# または、スタンドアロン EXE を実行
it-pass-study-tool.exe
```

### データロード
1. アプリ起動時に自動的にサンプルデータ (5問) をロード
2. Admin Panel → Import タブ → 「Webスクレイピング」で追加データを取得
3. または 「サンプルデータロード」で手動ロード

### アンインストール
```bash
msiexec /x ITPassStudyTool-1.0.0.msi
```

---

## System Requirements

- **OS**: Windows 10 以上
- **Python**: 3.11+ (ソース実行の場合)
- **RAM**: 512 MB 以上推奨
- **Disk Space**: 150 MB 以上

---

## Migration from v0.x

データベースの場所が変更されました：
- **旧**: `<project>/data/app.db`
- **新**: `%APPDATA%\ITPassStudyTool\data\app.db`

既存のデータを移行する場合：
```bash
# 旧データベースをコピー
copy <old_project>\data\app.db %APPDATA%\ITPassStudyTool\data\app.db
```

---

## Credits

- **Framework**: PySide6
- **Database**: SQLite + SQLAlchemy
- **Build Tools**: PyInstaller, WiX 6.0
- **Data Source**: itpassportsiken.com

---

**Happy Learning! 🎓**
