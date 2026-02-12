# WiX Toolset MSI インストーラー生成ガイド

## 概要

`build_wix_msi.py` スクリプトは、WiX Toolset を使用して Windows MSI インストーラーを生成します。

**対応環境:**
- Windows 10/11
- PowerShell 5.0 以上
- Python 3.8 以上

## 前提条件

### 1. WiX Toolset のインストール

#### Scoop を使用（推奨）
```powershell
scoop install wixtoolset
```

#### Chocolatey を使用
```powershell
choco install wixtoolset
```

#### 公式サイトからダウンロード
https://wixtoolset.org/releases/

### 2. EXE ファイルのビルド

MSI を生成する前に、PyInstaller で EXE をビルドしておく必要があります：

```powershell
python build_exe.py
```

これにより、`dist\it-pass-study-tool.exe` が生成されます。

## 使用方法

### 基本的な実行

```powershell
python build_wix_msi.py
```

## ビルド出力

ビルドが成功すると、以下のファイルが生成されます：

```
dist/ITPassStudyTool-1.0.0.msi   # メインインストーラー
wix/ITPassStudyTool.wxs           # WiX ソースコード
```

## インストール後の構成

### デスクトップ
✓ 「ITパスポート試験学習ツール」ショートカット

### スタートメニュー
✓ `ITPassStudyTool` フォルダ
  - 「ITパスポート試験学習ツール」ショートカット
  - 「アンインストール」ショートカット

### プログラムと機能
✓ 「ITパスポート試験学習ツール」として登録
  - バージョン: 1.0.0
  - 発行者: ITPassStudyTool
  - アンインストール機能搭載

### レジストリ登録
✓ `HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\ITPassStudyTool`
  - DisplayName
  - DisplayVersion
  - Manufacturer
  - UninstallString

## WiX XML カスタマイズ

`ITPassStudyTool.wxs` ファイルを編集することで、インストーラーをカスタマイズできます。

### 主な変更点

#### アプリケーション名の変更
```xml
<Product Name="新しい名前" ...>
```

#### インストール先の変更
```xml
<Directory Id="INSTALLFOLDER" Name="新しいフォルダ名" />
```

#### バージョンの変更
```xml
<Product Version="2.0.0.0" ...>
```

## トラブルシューティング

### WiX Toolset が見つからない

エラー:
```
✗ エラー: WiX Toolset がインストールされていません
```

対策:
1. Scoop で再インストール:
   ```powershell
   scoop install wixtoolset
   ```

2. 環境変数の確認:
   ```powershell
   $env:PATH
   ```

### EXE ファイルが見つからない

エラー:
```
✗ エラー: ... が見つかりません
```

対策:
1. `python build_exe.py` を実行
2. `dist\it-pass-study-tool.exe` が存在することを確認

### MSI ビルド失敗

エラー:
```
✗ エラー: MSI ビルド失敗
```

対策:
1. `ITPassStudyTool.wxs` が有効な XML であることを確認
2. WiX バージョンを確認:
   ```powershell
   wix --version
   ```

## セキュリティに関する注意

- MSI はテストマシンでしっかりテストしてから配布してください
- デジタル署名の追加をお勧めします
- インストールは管理者権限で実行されます

## 参考資料

- [WiX Toolset 公式サイト](https://wixtoolset.org/)
- [WiX ドキュメント](https://wixtoolset.org/docs/)
- [MSI インストーラー設定ガイド](../MSI_BUILD_GUIDE.md)
