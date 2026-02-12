# MSI インストーラー生成ガイド

このドキュメントでは、ITパスポート試験学習ツール用の Windows MSI インストーラーを生成する方法について説明します。

## 概要

`build_msi.py` スクリプトは、Python アプリケーションを Windows 環境でインストール可能な MSI ファイル（Microsoft Installer）に変換します。

**対応環境:**
- Windows 7 以上
- Windows 10 / 11（推奨）

**出力ファイル:**
- `ITPassStudyTool-1.0.0.msi` （サイズ: 15-50 MB）

## 前提条件

### 1. Python 環境
```powershell
python --version  # Python 3.8 以上が必要
```

### 2. PyInstaller でのビルド完了
MSI を生成する前に、EXE ファイルをビルドしておく必要があります：

```powershell
python build_exe.py
```

これにより、`dist\it-pass-study-tool.exe` が生成されます。

## 使用方法

### 基本的な使用方法

```powershell
python build_msi.py
```

このコマンドは以下の処理を自動的に実行します：
1. EXE ファイルの存在確認
2. バージョン情報の読込（`version.txt` から）
3. setuptools または WiX Toolset を使用して MSI を生成
4. 生成結果の検証

### EXE ビルドから MSI 生成まで一括実行

```powershell
python build_msi.py --build-exe
```

このコマンドは以下の処理を実行します：
1. `build_exe.py` で EXE ファイルをビルド
2. `build_msi.py` で MSI ファイルを生成

## ビルド方法の選択

### 方法 1: setuptools bdist_msi（デフォルト・推奨）

WiX Toolset がインストールされていない場合、自動的に setuptools の簡易版を使用します。

```powershell
python build_msi.py
```

**メリット:**
- 依存ツール不要
- セットアップが簡単
- すぐに MSI ファイルを生成可能

**デメリット:**
- カスタマイズ性が低い
- ライセンス情報などが限定的

### 方法 2: WiX Toolset（フル機能・オプション）

より詳細なカスタマイズが必要な場合は、WiX Toolset を使用します。

#### 2.1 WiX Toolset のインストール

WiX Toolset のインストール手順を表示：

```powershell
python build_msi.py --install-wix-info
```

**Chocolatey を使用（推奨）:**
```powershell
choco install wixtoolset
```

**直接ダウンロード:**
1. https://github.com/wixtoolset/wix3/releases から最新版をダウンロード
2. `wix311.exe` などのインストーラーを実行
3. インストール後、PATH に追加されることを確認

#### 2.2 WiX で MSI 生成

WiX がインストール済みの場合：

```powershell
python build_msi.py
```

自動的に WiX Toolset が使用されます。

## MSI ファイルの生成後

### インストール方法

1. **生成されたファイルの確認:**
   ```powershell
   ls dist\*.msi
   ```

2. **MSI ファイルの実行:**
   - ファイルエクスプローラーで `dist\ITPassStudyTool-1.0.0.msi` をダブルクリック
   - または以下のコマンドで実行：
   ```powershell
   msiexec /i "dist\ITPassStudyTool-1.0.0.msi"
   ```

3. **インストール時の画面:**
   - インストール先を確認
   - スタートメニューにのショートカット作成を確認
   - 「次へ」をクリックしてインストール完了

### インストール後

- **デスクトップ**: 「ITパスポート試験学習ツール」ショートカットが作成されます
- **スタートメニュー**: アプリケーション一覧に登録されます
- **アンインストール**: 「プログラムの追加と削除」から可能

### アンインストール方法

```powershell
msiexec /x "dist\ITPassStudyTool-1.0.0.msi"
```

または Windows の「プログラムの追加と削除」から「ITパスポート試験学習ツール」を選択して削除

## トラブルシューティング

### 問題 1: "EXE ファイルが見つかりません" エラー

**原因:** `build_exe.py` がまだ実行されていない

**解決方法:**
```powershell
python build_exe.py
python build_msi.py
```

### 問題 2: setuptools bdist_msi の失敗

**原因:** 必要なパッケージが不足している

**解決方法:**
```powershell
pip install wheel setuptools
python build_msi.py
```

### 問題 3: インストール時にアクセス拒否エラー

**原因:** 管理者権限がない

**解決方法:**
- PowerShell を「管理者として実行」で開く
- または MSI ファイルを右クリック → 「管理者として実行」

### 問題 4: 同じバージョンの再インストール

**原因:** 同じバージョンが既にインストール済み

**解決方法:**
1. アンインストール:
   ```powershell
   msiexec /x "dist\ITPassStudyTool-1.0.0.msi"
   ```
2. 再度インストール

## ビルド出力ファイル

`build_msi.py` 実行後、以下のファイルが生成されます：

```
dist/
├── ITPassStudyTool-1.0.0.msi       # ← メイン出力ファイル
├── it-pass-study-tool.exe          # ← 実行ファイル（build_exe.py から）
└── ...

build/
├── lib/
├── bdist.win-amd64/
├── msi/
│   ├── ITPassStudyTool-1.0.0.msi   # ← setuptools 出力（コピーされる）
│   └── ...
└── ...

setup.wxs                            # ← WiX XML ソース（WiX 使用時）
setup.wixobj                         # ← WiX オブジェクトファイル（WiX 使用時）
```

## カスタマイズ

### MSI の設定変更

#### setuptools 版の場合

`build_msi.py` の `MSIBuilder` クラスを編集：

```python
class MSIBuilder:
    def __init__(self):
        self.app_name = "ITPassStudyTool"         # アプリ名
        self.app_name_jp = "ITパスポート試験学習ツール"  # 日本語名
        self.version = self._read_version()       # バージョン
```

#### WiX 版の場合

`setup.wxs` ファイルを直接編集（XML）

**主な変更項目:**
- `Name`: アプリケーション名
- `Version`: バージョン番号
- `Manufacturer`: 開発者名
- `INSTALLFOLDER`: インストール先フォルダ

## バージョン更新時の手順

1. `version.txt` を更新:
   ```
   1.0.1
   ```

2. ソースコードを更新

3. EXE をビルド:
   ```powershell
   python build_exe.py
   ```

4. MSI を生成:
   ```powershell
   python build_msi.py
   ```

新しいバージョンの MSI ファイルが生成されます。

## 技術詳細

### setuptools bdist_msi の仕組み

1. `setup.py` に基づいて MSI メタデータを生成
2. Windows Installer SDK を使用して MSI パッケージを作成
3. Python アプリケーション・リソースを MSI に埋め込み

### WiX Toolset の仕組み

1. `setup.wxs` (XML) で MSI の構造を定義
2. `candle.exe` で XML をオブジェクトコード (.wixobj) に変換
3. `light.exe` でオブジェクトコードを MSI ファイルにリンク

## 参考リンク

- **PyInstaller**: https://pyinstaller.org/
- **setuptools**: https://setuptools.pypa.io/
- **WiX Toolset**: https://wixtoolset.org/
- **Microsoft Installer**: https://docs.microsoft.com/en-us/windows/win32/msi/

## ライセンス

このスクリプト・ツールは MIT ライセンスの下で提供されます。

## サポート

問題が発生した場合は、以下の方法でサポートを受けてください：

1. トラブルシューティングセクションを確認
2. ログファイルを確認：`build_output.log`
3. GitHub Issues でレポート

## 更新履歴

### バージョン 1.0.0
- 初回リリース
- setuptools bdist_msi 対応
- WiX Toolset 対応
- 日本語ローカライズ対応
