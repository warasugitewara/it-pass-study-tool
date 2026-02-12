# WiX Toolset MSI インストーラー生成システム

## 概要

このプロジェクトは、WiX Toolset を使用して Windows MSI インストーラーを生成するシステムです。
**日本語対応**で、**完全なショートカット機能**を備えています。

## ファイル一覧

### スクリプト

- **`build_wix_msi.py`** - WiX Toolset MSI ビルダー
  - WiX v3.x, v6.0 の両対応
  - 日本語 UI サポート
  - 完全なショートカット機能
  - 自動 EXE 検出

### テンプレート

- **`ITPassStudyTool.wxs`** - WiX XML テンプレート
  - WiX v3.x 互換スキーマ
  - デスクトップショートカット
  - スタートメニューショートカット
  - アンインストール機能
  - レジストリ登録

### ドキュメント

- **`WIX_SETUP_GUIDE.md`** - 導入・使用ガイド
- **`README.md`** (本ファイル)

## クイックスタート

### 1. WiX Toolset インストール

```powershell
# Scoop (推奨)
scoop install wixtoolset

# Chocolatey
choco install wixtoolset

# または公式サイトからダウンロード
https://wixtoolset.org/releases/
```

### 2. EXE ビルド

```powershell
python build_exe.py
# 出力: dist\it-pass-study-tool.exe
```

### 3. MSI 生成

```powershell
python build_wix_msi.py
# 出力: dist\ITPassStudyTool-1.0.0.msi
```

## 主な機能

### ✅ デスクトップショートカット

![デスクトップ](https://img.shields.io/badge/Desktop-ShortCut-green)

インストール直後、デスクトップに「ITパスポート試験学習ツール」ショートカットが作成されます。

### ✅ スタートメニュー統合

![スタートメニュー](https://img.shields.io/badge/Start%20Menu-Folder-blue)

スタートメニューに `ITPassStudyTool` フォルダが作成され、以下が含まれます:
- 「ITパスポート試験学習ツール」ショートカット
- 「アンインストール」ショートカット

### ✅ プログラムと機能登録

![プログラムと機能](https://img.shields.io/badge/Programs%20%26%20Features-Registered-orange)

Windows の「プログラムと機能」に登録され、以下の情報が表示されます:
- アプリケーション名: 「ITパスポート試験学習ツール」
- バージョン: 1.0.0
- 発行者: ITPassStudyTool
- アンインストール機能

### ✅ 日本語 UI 対応

![日本語](https://img.shields.io/badge/UI-Japanese-red)

すべてのショートカット名やメニュー項目が日本語で表示されます。

### ✅ レジストリ登録

![レジストリ](https://img.shields.io/badge/Registry-Registered-purple)

Windows レジストリに以下が自動登録されます:
- `HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\ITPassStudyTool`
  - DisplayName
  - DisplayVersion
  - Manufacturer
  - UninstallString

## WiX XML 構造

### Product定義

```xml
<Product Id="*" 
         Name="ITパスポート試験学習ツール" 
         Language="1041"
         Version="1.0.0.0"
         Manufacturer="ITPassStudyTool"
         UpgradeCode="5A8B4C2D-3E6F-4A2B-8C9D-7E1F5A3B6C9D">
```

- `Language="1041"` - 日本語コード
- `UpgradeCode` - 同じアプリの更新を検出

### ディレクトリ構造

```
ProgramFiles/
  └─ ITPassStudyTool/
     └─ it-pass-study-tool.exe

Desktop/
  └─ ITパスポート試験学習ツール (ショートカット)

ProgramMenu/
  └─ ITPassStudyTool/
     ├─ ITパスポート試験学習ツール (ショートカット)
     └─ アンインストール (ショートカット)
```

### コンポーネント

| コンポーネント | 目的 |
|---|---|
| `MainExecutable` | 実行ファイル (`it-pass-study-tool.exe`) |
| `DesktopShortcut` | デスクトップショートカット |
| `MenuShortcut` | スタートメニューショートカット |
| `UninstallShortcut` | アンインストールショートカット |
| `RegistryEntries` | Windows レジストリ登録 |

## カスタマイズ

### アプリケーション情報の変更

`ITPassStudyTool.wxs` を編集:

```xml
<!-- アプリ名 -->
<Product Name="新しい名前" ...>

<!-- バージョン -->
<Product Version="2.0.0.0" ...>

<!-- インストール先フォルダ -->
<Directory Id="INSTALLFOLDER" Name="新しいフォルダ" />
```

### スクリプト修正

`build_wix_msi.py` を編集:

```python
self.app_name_jp = "新しいアプリケーション名"
self.version = "2.0.0"
```

## トラブルシューティング

### エラー: WiX がインストールされていない

```powershell
# 再インストール
scoop uninstall wixtoolset
scoop install wixtoolset
```

### エラー: EXE が見つからない

```powershell
# EXE をビルド
python build_exe.py

# 確認
Test-Path "dist\it-pass-study-tool.exe"
```

### エラー: MSI ビルド失敗

1. `ITPassStudyTool.wxs` の XML 構文を確認
2. `dist/` ディレクトリが存在することを確認
3. WiX のバージョン互換性を確認

```powershell
wix --version
```

## 開発環境

- **OS**: Windows 10/11
- **Python**: 3.8+
- **WiX Toolset**: v3.14+ または v6.0+
- **エディタ**: Visual Studio Code (拡張機能: WiX Toolset 推奨)

## セキュリティと配布

### テスト

配布前に、テスト マシンで MSI をインストール・アンインストール・動作確認してください。

```powershell
# インストール
msiexec /i "ITPassStudyTool-1.0.0.msi"

# アンインストール
msiexec /x "ITPassStudyTool-1.0.0.msi"
```

### デジタル署名（推奨）

```powershell
# 証明書での署名
signtool sign /f cert.pfx /p password /t http://timestamp.server.com ITPassStudyTool-1.0.0.msi
```

### チェックリスト

- [ ] ローカル環境でテスト
- [ ] 他のマシンでテスト
- [ ] アンインストール確認
- [ ] レジストリ登録確認
- [ ] ショートカット確認
- [ ] デジタル署名（オプション）
- [ ] 配布

## ライセンス

このスクリプト・テンプレートはプロジェクトのライセンスに準拠します。

## 参考資料

- [WiX Toolset 公式](https://wixtoolset.org/)
- [WiX ドキュメント](https://wixtoolset.org/docs/)
- [Windows インストーラー ガイド](https://learn.microsoft.com/windows/win32/msi/windows-installer-start-page)

---

**作成日**: 2025年2月12日  
**WiX バージョン対応**: v3.x, v6.0+  
**日本語対応**: ✅ 完全対応
