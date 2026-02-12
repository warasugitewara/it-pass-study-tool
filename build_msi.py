#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows MSI インストーラー生成スクリプト
setuptools + bdist_msi を使用して MSI ファイルを生成

使用方法:
    python build_msi.py

出力:
    dist/ITPassStudyTool-1.0.0.msi
"""

import os
import sys
import subprocess
from pathlib import Path
from configparser import ConfigParser

# Windows コンソール出力のエンコーディング設定
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class MSIBuilder:
    """MSI ファイル生成ビルダー"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.dist_dir = self.project_dir / "dist"
        self.build_dir = self.project_dir / "build"
        self.version = self._read_version()
        self.app_name = "ITPassStudyTool"
        self.app_name_jp = "ITパスポート試験学習ツール"
        
    def _read_version(self):
        """version.txt からバージョン番号を読込"""
        version_file = self.project_dir / "version.txt"
        if version_file.exists():
            with open(version_file, 'r', encoding='utf-8') as f:
                return f.read().strip().split('\n')[0].strip()
        return "1.0.0"
    
    def _create_setup_py(self):
        """setuptools 用の setup.py を生成"""
        setup_py_content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MSI インストーラー生成用 setup.py
"""

from setuptools import setup

setup(
    name="{self.app_name}",
    version="{self.version}",
    description="{self.app_name_jp}",
    author="学習ツール開発チーム",
    author_email="support@example.com",
    url="https://github.com/example/it-pass-study-tool",
    license="MIT",
    
    # MSI 固有の設定
    options={{
        'bdist_msi': {{
            'add_to_path': False,
        }},
    }},
    
    # スクリプト/エントリーポイント
    entry_points={{}},
)
'''
        setup_py_path = self.project_dir / "setup_msi.py"
        with open(setup_py_path, 'w', encoding='utf-8') as f:
            f.write(setup_py_content)
        return setup_py_path

    def _create_wix_xml(self):
        """WiX ツールセット用の .wxs XML ファイルを生成"""
        exe_path = self.dist_dir / "it-pass-study-tool.exe"
        
        if not exe_path.exists():
            print(f"⚠️  警告: EXE ファイルが見つかりません: {exe_path}")
            print(f"   先に build_exe.py でビルドしてください")
            return None
        
        # wxs XML 内容を作成
        wxs_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
    <Product 
        Id="*" 
        Name="{self.app_name_jp}" 
        Language="1041" 
        Version="{self.version}.0" 
        UpgradeCode="12345678-1234-1234-1234-123456789012" 
        Manufacturer="学習ツール開発チーム">
        
        <Package 
            InstallerVersion="200" 
            Compressed="yes" 
            InstallScope="perMachine" 
            Description="{self.app_name_jp} インストーラー"
            Manufacturer="学習ツール開発チーム"/>
        
        <MajorUpgrade 
            DowngradeErrorMessage="より新しいバージョンが既にインストールされています"/>
        
        <Media Id="1" Cabinet="Media1.cab" EmbedCab="yes"/>
        
        <Directory Id="TARGETDIR" Name="SourceDir">
            <Directory Id="ProgramFilesFolder">
                <Directory Id="INSTALLFOLDER" Name="{self.app_name}"/>
            </Directory>
            <Directory Id="ProgramMenuFolder">
                <Directory Id="ApplicationProgramsFolder" Name="{self.app_name_jp}"/>
            </Directory>
            <Directory Id="DesktopFolder" Name="Desktop"/>
        </Directory>
        
        <Feature Id="ProductFeature" Title="{self.app_name_jp}" Level="1">
            <ComponentRef Id="MainExecutableComponent"/>
            <ComponentRef Id="StartMenuShortcutComponent"/>
            <ComponentRef Id="DesktopShortcutComponent"/>
        </Feature>
        
        <!-- メイン実行ファイル -->
        <DirectoryRef Id="INSTALLFOLDER">
            <Component Id="MainExecutableComponent" Guid="*">
                <File 
                    Id="MainExecutable" 
                    Source="{exe_path}" 
                    KeyPath="yes" 
                    Checksum="yes"/>
            </Component>
        </DirectoryRef>
        
        <!-- スタートメニュー ショートカット -->
        <DirectoryRef Id="ApplicationProgramsFolder">
            <Component Id="StartMenuShortcutComponent" Guid="*">
                <Shortcut 
                    Id="StartMenuShortcut" 
                    Target="[INSTALLFOLDER]it-pass-study-tool.exe" 
                    Name="{self.app_name_jp}" 
                    Description="{self.app_name_jp}"/>
                <RemoveFolder Id="ApplicationProgramsFolderRemove" On="uninstall"/>
                <RegistryValue 
                    Root="HKCU" 
                    Key="Software\\{self.app_name}" 
                    Name="StartMenuShortcut" 
                    Type="string" 
                    Value="1" 
                    KeyPath="yes"/>
            </Component>
        </DirectoryRef>
        
        <!-- デスクトップ ショートカット -->
        <DirectoryRef Id="DesktopFolder">
            <Component Id="DesktopShortcutComponent" Guid="*">
                <Shortcut 
                    Id="DesktopShortcut" 
                    Target="[INSTALLFOLDER]it-pass-study-tool.exe" 
                    Name="{self.app_name_jp}" 
                    Description="{self.app_name_jp}"/>
                <RegistryValue 
                    Root="HKCU" 
                    Key="Software\\{self.app_name}" 
                    Name="Installed" 
                    Type="integer" 
                    Value="1" 
                    KeyPath="yes"/>
            </Component>
        </DirectoryRef>
        
        <!-- UI -->
        <UIRef Id="WixUI_InstallDir"/>
        <WixVariable Id="WixUILicenseRtf" Value="License.rtf"/>
    </Product>
</Wix>
'''
        wxs_path = self.project_dir / "setup.wxs"
        with open(wxs_path, 'w', encoding='utf-8') as f:
            f.write(wxs_content)
        print(f"✅ WiX XML ファイルを生成しました: {wxs_path}")
        return wxs_path
    
    def _check_wix_tools(self):
        """WiX ツールセットがインストール済みか確認"""
        try:
            result = subprocess.run(
                ["where", "candle"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False
    
    def _install_wix(self):
        """WiX Toolset のインストール手順を表示"""
        print("\n" + "=" * 70)
        print("📦 WiX Toolset のインストール手順")
        print("=" * 70)
        print("""
WiX Toolset がインストールされていません。以下の方法でインストールしてください：

【方法 1】Chocolatey を使用（推奨）:
    choco install wixtoolset

【方法 2】直接ダウンロード:
    1. https://github.com/wixtoolset/wix3/releases から最新版をダウンロード
    2. wix311.exe などのインストーラーを実行
    3. インストール後、コマンドラインツール（candle.exe, light.exe）が
       PATH に追加されることを確認

【方法 3】代替案：setuptools の簡易版 MSI 生成:
    python build_msi.py --setuptools-only
""")
        print("=" * 70 + "\n")
    
    def _build_msi_with_setuptools(self):
        """setuptools bdist_msi で MSI を生成（簡易版）"""
        print("\n🔧 setuptools bdist_msi を使用して MSI を生成中...\n")
        
        # 必要なパッケージをインストール
        print("📦 必要なパッケージをインストール中...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "wheel"],
            cwd=str(self.project_dir)
        )
        
        # メインの setup.py を使用（setup_msi.py は生成しない）
        setup_py = self.project_dir / "setup.py"
        
        # MSI を生成
        print(f"\n🔨 MSI ファイルを生成中...\n")
        cmd = [
            sys.executable,
            str(setup_py),
            "bdist_msi"
        ]
        
        result = subprocess.run(
            cmd,
            cwd=str(self.project_dir),
            capture_output=False
        )
        
        if result.returncode == 0:
            # setuptools が build/msi に生成したファイルをコピー
            build_msi_dir = self.build_dir / "bdist.win-amd64" / "msi"
            if build_msi_dir.exists():
                import shutil
                for msi_file in build_msi_dir.glob("*.msi"):
                    target = self.dist_dir / msi_file.name
                    if not target.exists():
                        shutil.copy2(msi_file, target)
        
        return result.returncode == 0
    
    def _build_msi_with_wix(self):
        """WiX Toolset を使用して MSI を生成"""
        print("\n🔧 WiX Toolset を使用して MSI を生成中...\n")
        
        # WiX XML を生成
        wxs_path = self._create_wix_xml()
        if not wxs_path:
            return False
        
        # candle コマンドでオブジェクトファイルにコンパイル
        print("🔨 candle.exe で WiX XML をコンパイル中...")
        wixobj_path = self.project_dir / "setup.wixobj"
        
        cmd_candle = [
            "candle",
            "-out", str(wixobj_path),
            str(wxs_path)
        ]
        
        result = subprocess.run(cmd_candle, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ candle.exe でのコンパイルが失敗しました:")
            print(result.stderr)
            return False
        
        # light コマンドで MSI にリンク
        print("🔨 light.exe で MSI にリンク中...")
        msi_path = self.dist_dir / f"{self.app_name}-{self.version}.msi"
        
        # dist ディレクトリがない場合は作成
        self.dist_dir.mkdir(parents=True, exist_ok=True)
        
        cmd_light = [
            "light",
            "-out", str(msi_path),
            str(wixobj_path)
        ]
        
        result = subprocess.run(cmd_light, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ light.exe での MSI 生成が失敗しました:")
            print(result.stderr)
            return False
        
        print(f"✅ MSI ファイルを生成しました: {msi_path}")
        return True
    
    def build(self, force_setuptools=False):
        """MSI ファイルを生成"""
        print("=" * 70)
        print(f"Windows MSI インストーラー生成ツール")
        print("=" * 70)
        print(f"\nプロジェクト情報:")
        print(f"  アプリ名: {self.app_name_jp}")
        print(f"  バージョン: {self.version}")
        print(f"  プロジェクトディレクトリ: {self.project_dir}")
        
        # EXE ファイルの確認
        exe_path = self.dist_dir / "it-pass-study-tool.exe"
        if not exe_path.exists():
            print(f"\n⚠️  警告: EXE ファイルが見つかりません")
            print(f"   先に以下のコマンドでビルドしてください:")
            print(f"   python build_exe.py")
            print(f"   または")
            print(f"   python build_msi.py --build-exe")
            return False
        
        print(f"  EXE ファイル: {exe_path}")
        
        # ビルド方法を決定
        has_wix = self._check_wix_tools()
        
        if force_setuptools or not has_wix:
            if not force_setuptools and not has_wix:
                print(f"\n⚠️  WiX Toolset がインストールされていません")
                print(f"   setuptools の簡易版で MSI を生成します\n")
            
            if not self._build_msi_with_setuptools():
                print(f"\n❌ MSI 生成に失敗しました")
                return False
        else:
            if not self._build_msi_with_wix():
                print(f"\n❌ MSI 生成に失敗しました")
                return False
        
        # 生成結果の確認
        return self._verify_build()
    
    def _verify_build(self):
        """生成された MSI ファイルを検証"""
        print(f"\n🔍 MSI ファイルを検証中...\n")
        
        # setuptools bdist_msi で生成された MSI を探す
        possible_paths = [
            self.dist_dir / f"{self.app_name}-{self.version}.msi",
            self.dist_dir / f"{self.app_name}.msi",
            self.project_dir / "dist" / f"{self.app_name}-{self.version}.msi",
            self.project_dir / "dist" / f"{self.app_name}.msi",
        ]
        
        # build/msi ディレクトリも確認
        build_msi_dir = self.build_dir / "msi"
        if build_msi_dir.exists():
            for msi_file in build_msi_dir.glob("*.msi"):
                possible_paths.append(msi_file)
        
        # dist ディレクトリを確認（setuptools のデフォルト出力も含む）
        if self.dist_dir.exists():
            for msi_file in self.dist_dir.glob("*.msi"):
                possible_paths.append(msi_file)
        
        # 見つかったファイルを整理
        found_msi = None
        for msi_path in possible_paths:
            if msi_path.exists():
                found_msi = msi_path
                break
        
        # setuptools のデフォルト形式のファイルをリネーム
        default_pattern = self.dist_dir / f"{self.app_name}-{self.version}.win-amd64.msi"
        target_name = self.dist_dir / f"{self.app_name}-{self.version}.msi"
        
        if default_pattern.exists() and not target_name.exists():
            default_pattern.rename(target_name)
            found_msi = target_name
        
        if found_msi:
            file_size = found_msi.stat().st_size / (1024 * 1024)  # MB
            print(f"✅ MSI ファイルが正常に生成されました")
            print(f"   ファイル: {found_msi.name}")
            print(f"   パス: {found_msi}")
            print(f"   サイズ: {file_size:.2f} MB")
            print(f"\n🎉 インストール方法:")
            print(f"   1. MSI ファイルをダブルクリック")
            print(f"   2. インストールウィザードに従ってインストール")
            print(f"   3. インストール完了後、デスクトップのショートカットから起動")
            return True
        
        print(f"❌ MSI ファイルが見つかりません")
        print(f"\n生成されたファイル:")
        if self.dist_dir.exists():
            for item in self.dist_dir.iterdir():
                print(f"   - {item.name}")
        return False


def main():
    """メイン処理"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Windows MSI インストーラー生成ツール"
    )
    parser.add_argument(
        "--setuptools-only",
        action="store_true",
        help="setuptools bdist_msi を強制使用"
    )
    parser.add_argument(
        "--build-exe",
        action="store_true",
        help="先に EXE をビルド"
    )
    parser.add_argument(
        "--install-wix-info",
        action="store_true",
        help="WiX Toolset のインストール手順を表示"
    )
    
    args = parser.parse_args()
    
    if args.install_wix_info:
        builder = MSIBuilder()
        builder._install_wix()
        return 0
    
    # EXE をビルド
    if args.build_exe:
        print("🔨 先に EXE をビルド中...\n")
        result = subprocess.run(
            [sys.executable, "build_exe.py"],
            cwd=str(Path(__file__).parent)
        )
        if result.returncode != 0:
            print("❌ EXE ビルドが失敗しました")
            return 1
    
    # MSI を生成
    builder = MSIBuilder()
    success = builder.build(force_setuptools=args.setuptools_only)
    
    if success:
        print("\n" + "=" * 70)
        print("✨ MSI ファイルの生成が成功しました！")
        print("=" * 70)
        return 0
    else:
        print("\n" + "=" * 70)
        print("❌ MSI ファイルの生成に失敗しました")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
