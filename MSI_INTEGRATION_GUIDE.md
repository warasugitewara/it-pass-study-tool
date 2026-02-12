# MSI インストーラー生成 - 統合ガイド

## 概要

プロジェクトには 2 つの MSI 生成方式があります:

| 方式 | ファイル | 技術 | 推奨 | 習得曲線 |
|------|---------|------|------|---------|
| **setuptools ベース** | `build_msi.py` | Python setuptools | ✅ 初心者 | 低 |
| **WiX Toolset ベース** | `build_wix_msi.py` | WiX Toolset | ✅ 高度 | 中 |

## 方式 1: setuptools ベース（既存）

### 特徴
- ✅ Python のみで完結
- ✅ WiX 不要
- ✅ セットアップが簡単
- ⚠️ カスタマイズ性が低い

### 使用方法

```powershell
# EXE ビルド
python build_exe.py

# MSI 生成
python build_msi.py

# 出力
# dist\ITPassStudyTool-1.0.0.msi
```

### 詳細
- ドキュメント: `MSI_BUILD_GUIDE.md`, `MSI_IMPLEMENTATION_REPORT.md`
- 実装: `build_msi.py`, `setup_msi.py`

---

## 方式 2: WiX Toolset ベース（新規）

### 特徴
- ✅ 高度なカスタマイズが可能
- ✅ プロフェッショナルな MSI 作成
- ✅ 日本語完全対応
- ✅ 複数のショートカット自動生成
- ⚠️ WiX Toolset インストール必須

### 使用方法

```powershell
# WiX Toolset インストール
scoop install wixtoolset
# または
choco install wixtoolset

# EXE ビルド
python build_exe.py

# MSI 生成
python build_wix_msi.py

# 出力
# dist\ITPassStudyTool-1.0.0.msi
```

### 詳細
- ドキュメント: `WIX_README.md`, `WIX_SETUP_GUIDE.md`
- 実装: `build_wix_msi.py`
- テンプレート: `ITPassStudyTool.wxs`

---

## 方式の選択

### setuptools を選ぶべき場合
- ❌ WiX をインストールしたくない
- ❌ シンプルな MSI で十分
- ✅ 最小限の依存関係
- ✅ 迅速なビルド

### WiX Toolset を選ぶべき場合
- ✅ プロフェッショナルな MSI を作成したい
- ✅ 複数のショートカットが必要
- ✅ 日本語完全対応が必須
- ✅ レジストリを細かくカスタマイズしたい

---

## インストール後の違い

### setuptools 版

```
✓ インストールディレクトリ: Program Files\ITPassStudyTool
✓ デスクトップショートカット: あり
✓ スタートメニュー: 基本的なエントリのみ
✓ 日本語対応: 部分的
```

### WiX Toolset 版

```
✓ インストールディレクトリ: Program Files\ITPassStudyTool
✓ デスクトップショートカット: 「ITパスポート試験学習ツール」
✓ スタートメニュー: 
  ├─ 「ITパスポート試験学習ツール」
  └─ 「アンインストール」
✓ プログラムと機能: 日本語名で登録
✓ 日本語対応: 完全対応
```

---

## 比較表

| 機能 | setuptools | WiX |
|------|-----------|-----|
| インストール依存 | ❌ 不要 | ⚠️ 必要 |
| 習得曲線 | ✅ 低 | 中 |
| カスタマイズ性 | 中 | ✅ 高 |
| 日本語対応 | ⚠️ 部分 | ✅ 完全 |
| ショートカット | 基本 | ✅ 複数/高度 |
| レジストリ制御 | 基本 | ✅ 詳細 |
| プロフェッショナル度 | 中 | ✅ 高 |
| ビルド速度 | ✅ 高速 | 中程度 |

---

## 分岐フロー

```
EXE ビルド
    ↓
    └─→ [方式 1] setuptools MSI
    │   python build_msi.py
    │   → シンプル・迅速
    │
    └─→ [方式 2] WiX Toolset MSI
        python build_wix_msi.py
        → 高度・プロフェッショナル
```

---

## セットアップシーケンス

### 初回セットアップ（WiX 版を推奨）

```powershell
# 1. 環境構築
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. WiX インストール
scoop install wixtoolset
# 検証
wix --version

# 3. EXE ビルド
python build_exe.py
# 出力確認: dist\it-pass-study-tool.exe

# 4. MSI 生成
python build_wix_msi.py
# 出力確認: dist\ITPassStudyTool-1.0.0.msi

# 5. テスト
msiexec /i "dist\ITPassStudyTool-1.0.0.msi"

# 6. アンインストール確認
# Windows → 設定 → プログラム → プログラムと機能
# 「ITパスポート試験学習ツール」を探してアンインストール
```

---

## トラブルシューティング

### WiX インストール失敗

```powershell
# Scoop が見つからない場合
# スコープをインストール
iwr -useb get.scoop.sh | iex
scoop install wixtoolset

# Chocolatey を使用
choco install wixtoolset -y
```

### EXE ビルド失敗

```powershell
# PyInstaller で EXE ビルド
pip install pyinstaller
python build_exe.py

# エラーが出る場合はログ確認
python build_exe.py > build.log 2>&1
type build.log
```

### MSI ビルド失敗

```powershell
# WiX インストール確認
wix --version

# EXE 確認
Test-Path "dist\it-pass-study-tool.exe"

# WiX XML 検証
wix build --help  # help は動作確認

# 手動コンパイル（WiX 3.x の場合）
candle.exe wix\ITPassStudyTool.wxs -o wix\ITPassStudyTool.wixobj -d SourceDir=dist
light.exe wix\ITPassStudyTool.wixobj -o dist\ITPassStudyTool.msi
```

---

## ベストプラクティス

### 1. 常に EXE をテストしてから MSI 化

```powershell
# EXE 直接実行でテスト
.\dist\it-pass-study-tool.exe

# 正常動作を確認してから MSI 化
python build_wix_msi.py
```

### 2. MSI テストは管理者権限で

```powershell
# PowerShell を管理者権限で実行してから
msiexec /i "dist\ITPassStudyTool-1.0.0.msi"
```

### 3. アンインストールもテスト

```powershell
# 設定 → アプリ → プログラムと機能
# または
msiexec /x "dist\ITPassStudyTool-1.0.0.msi"
```

### 4. バージョン管理

```powershell
# version.txt を更新してからビルド
"2.0.0" | Out-File "version.txt" -Encoding UTF8

# MSI ファイル名に反映される
# dist\ITPassStudyTool-2.0.0.msi
```

---

## CI/CD パイプライン（参考）

### GitHub Actions 例

```yaml
name: Build MSI

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          choco install wixtoolset -y
      
      - name: Build EXE
        run: python build_exe.py
      
      - name: Build MSI
        run: python build_wix_msi.py
      
      - name: Upload artifact
        uses: actions/upload-artifact@v2
        with:
          name: msi-installer
          path: dist/*.msi
```

---

## まとめ

- **シンプル重視**: `python build_msi.py` → setuptools ベース
- **品質・プロ重視**: `python build_wix_msi.py` → WiX Toolset ベース

どちらでも正常に動作する MSI が生成されます。
プロジェクトの要件に応じて選択してください。

---

**最終更新**: 2025年2月12日
