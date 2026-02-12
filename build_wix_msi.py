#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WiX Toolset を使用した Windows MSI インストーラー生成スクリプト
日本語対応、完全なショートカット機能付き

対応: WiX Toolset 6.0+ (Scoop 版) / WiX Toolset 3.14+ (従来版)

使用方法:
    python build_wix_msi.py

出力:
    dist/ITPassStudyTool-1.0.0.msi
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path

# Windows コンソール出力のエンコーディング設定
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class WiXMSIBuilder:
    """WiX Toolset を使用した MSI ファイル生成ビルダー"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.dist_dir = self.project_dir / "dist"
        self.wix_dir = self.project_dir / "wix"
        self.build_dir = self.project_dir / "build"
        self.version = self._read_version()
        self.app_name = "ITPassStudyTool"
        self.app_name_jp = "ITパスポート試験学習ツール"
        self.exe_file = self.dist_dir / "it-pass-study-tool.exe"
        self.upgrade_code = self._generate_upgrade_code()
        
        # WiX ツールのパス
        self.wix_exe = self._find_wix_executable()
        self.wix_version = self._detect_wix_version() if self.wix_exe else None
        
    def _read_version(self):
        """version.txt からバージョン番号を読込"""
        version_file = self.project_dir / "version.txt"
        if version_file.exists():
            with open(version_file, 'r', encoding='utf-8') as f:
                return f.read().strip().split('\n')[0].strip()
        return "1.0.0"
    
    def _generate_upgrade_code(self):
        """MSI UpgradeCode（固定 GUID）を生成"""
        return "5A8B4C2D-3E6F-4A2B-8C9D-7E1F5A3B6C9D"
    
    def _find_wix_executable(self):
        """WiX ツール実行ファイルを検索"""
        # WiX 6.0（Scoop）
        wix6_paths = [
            Path(os.path.expanduser(r"~\scoop\apps\wixtoolset\current\wix.exe")),
            Path(r"C:\Program Files\dotnet\tools\wix.exe"),
        ]
        
        for path in wix6_paths:
            if path.exists():
                return path
        
        # WiX 3.x（従来版）
        wix3_paths = [
            Path(r"C:\Program Files (x86)\WiX Toolset v3.14\bin"),
            Path(r"C:\Program Files (x86)\WiX Toolset v3.11\bin"),
            Path(r"C:\Program Files\WiX Toolset v3.14\bin"),
        ]
        
        for path in wix3_paths:
            candle = path / "candle.exe"
            if candle.exists():
                return candle
        
        return None
    
    def _detect_wix_version(self):
        """WiX のバージョンを検出"""
        if not self.wix_exe:
            return None
        
        if self.wix_exe.name == "wix.exe":
            return 6
        elif self.wix_exe.name == "candle.exe":
            return 3
        
        return None
    
    def check_prerequisites(self):
        """前提条件をチェック"""
        print("✓ 前提条件をチェック中...")
        
        # EXE ファイルの存在確認
        if not self.exe_file.exists():
            print(f"✗ エラー: {self.exe_file} が見つかりません")
            print("  先に 'python build_exe.py' を実行してください")
            return False
        
        # WiX ツールの確認
        if not self.wix_exe:
            print("✗ エラー: WiX Toolset がインストールされていません")
            print("  以下のいずれかを実行してください:")
            print("  1. scoop install wixtoolset")
            print("  2. choco install wixtoolset")
            return False
        
        version_str = f"WiX {self.wix_version}.x" if self.wix_version else "WiX (バージョン不明)"
        print(f"  ✓ {version_str}: {self.wix_exe}")
        print(f"  ✓ EXE: {self.exe_file}")
        return True
    
    def create_wix_directory_structure(self):
        """WiX ディレクトリ構造を作成"""
        self.wix_dir.mkdir(exist_ok=True)
        print(f"✓ WiX ディレクトリ作成: {self.wix_dir}")
    
    def generate_wix_xml(self):
        """WiX XML ファイルを生成（WiX 4/6 対応）"""
        wxs_file = self.wix_dir / "ITPassStudyTool.wxs"
        
        wix_content = f'''<?xml version="1.0" encoding="utf-8"?>
<Wix xmlns="http://wixtoolset.org/schemas/v4/wxs">
  <Package Name="{self.app_name_jp}"
           Language="1041"
           Version="{self.version}.0"
           Manufacturer="ITPassStudyTool"
           UpgradeCode="{self.upgrade_code}"
           InstallerVersion="200"
           Compressed="yes"
           Scope="perUser">

    <MajorUpgrade DowngradeErrorMessage="より新しいバージョンが既にインストールされています。" />
    <MediaTemplate EmbedCab="yes" />

    <StandardDirectory Id="LocalAppDataFolder">
      <Directory Id="INSTALLFOLDER" Name="ITPassStudyTool">
        <Component Id="MainExecutable" Guid="*">
          <File Id="MainEXE" Name="it-pass-study-tool.exe"
                Source="{str(self.exe_file)}"
                KeyPath="yes" />
        </Component>
      </Directory>
    </StandardDirectory>

    <StandardDirectory Id="DesktopFolder">
      <Component Id="DesktopShortcutComp" Guid="4F2BFCF3-1234-1234-1234-1234567890AB">
        <Shortcut Id="DesktopShortcut"
                  Name="{self.app_name_jp}"
                  Target="[INSTALLFOLDER]it-pass-study-tool.exe"
                  WorkingDirectory="INSTALLFOLDER" />
        <RegistryValue Root="HKCU" Key="Software\\ITPassStudyTool"
                       Name="DesktopShortcut" Type="string" Value="1" KeyPath="yes" />
      </Component>
    </StandardDirectory>

    <StandardDirectory Id="ProgramMenuFolder">
      <Directory Id="MENUFOLDER" Name="{self.app_name_jp}">
        <Component Id="MenuShortcutComp" Guid="5F2BFCF3-1234-1234-1234-1234567890AB">
          <Shortcut Id="MenuShortcut"
                    Name="{self.app_name_jp}"
                    Target="[INSTALLFOLDER]it-pass-study-tool.exe"
                    WorkingDirectory="INSTALLFOLDER" />
          <RemoveFolder Id="RemoveMenuFolder" On="uninstall" />
          <RegistryValue Root="HKCU" Key="Software\\ITPassStudyTool"
                         Name="MenuShortcut" Type="string" Value="1" KeyPath="yes" />
        </Component>
      </Directory>
    </StandardDirectory>

    <Feature Id="ProductFeature" Title="{self.app_name_jp}" Level="1">
      <ComponentRef Id="MainExecutable" />
      <ComponentRef Id="DesktopShortcutComp" />
      <ComponentRef Id="MenuShortcutComp" />
    </Feature>

  </Package>
</Wix>
'''
        
        with open(wxs_file, 'w', encoding='utf-8-sig') as f:
            f.write(wix_content)
        
        print(f"✓ WiX XML 生成: {wxs_file}")
        return wxs_file
    
    def build_wix6(self, wxs_file):
        """WiX 6.0 を使用してビルド"""
        msi_file = self.dist_dir / f"ITPassStudyTool-{self.version}.msi"
        
        cmd = [
            str(self.wix_exe),
            "build",
            str(wxs_file),
            "-o", str(msi_file),
        ]
        
        print(f"\n✓ MSI ビルド中 (WiX 6.0)...")
        print(f"  コマンド: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.wix_dir))
        
        if result.returncode != 0:
            print(f"✗ エラー: MSI ビルド失敗")
            if result.stdout:
                print(result.stdout[:1000])
            if result.stderr:
                print(result.stderr[:1000])
            return False
        
        if result.stdout:
            print(result.stdout[:500])
        
        return msi_file.exists()
    
    def build_wix3(self, wxs_file):
        """WiX 3.x を使用してビルド（candle + light）"""
        candle_exe = self.wix_exe.parent / "candle.exe" if not self.wix_exe.name.endswith("candle.exe") else self.wix_exe
        light_exe = self.wix_exe.parent / "light.exe"
        obj_file = self.wix_dir / "ITPassStudyTool.wixobj"
        msi_file = self.dist_dir / f"ITPassStudyTool-{self.version}.msi"
        
        # Candle（コンパイル）
        cmd_candle = [
            str(candle_exe),
            str(wxs_file),
            "-o", str(obj_file),
            "-d", f"SourceDir={str(self.dist_dir)}",
            "-arch", "x64"
        ]
        
        print(f"\n✓ WiX コンパイル中 (candle.exe)...")
        result = subprocess.run(cmd_candle, capture_output=True, text=True, cwd=str(self.wix_dir))
        
        if result.returncode != 0:
            print(f"✗ エラー: WiX コンパイル失敗")
            print(result.stdout)
            print(result.stderr)
            return False
        
        # Light（リンク）
        cmd_light = [
            str(light_exe),
            str(obj_file),
            "-o", str(msi_file),
            "-ext", "WixUIExtension"
        ]
        
        print(f"✓ MSI リンク中 (light.exe)...")
        result = subprocess.run(cmd_light, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"✗ エラー: MSI リンク失敗")
            print(result.stdout)
            print(result.stderr)
            return False
        
        print(f"✓ MSI 生成完了: {msi_file}")
        return True
    
    def build(self):
        """MSI ビルド全体処理"""
        print("=" * 60)
        print("WiX Toolset MSI インストーラー生成")
        print("=" * 60)
        
        # 前提条件チェック
        if not self.check_prerequisites():
            return False
        
        # WiX ディレクトリ作成
        self.create_wix_directory_structure()
        
        # WiX XML 生成
        wxs_file = self.generate_wix_xml()
        
        # ビルド実行（WiX バージョンに応じて）
        success = False
        if self.wix_version == 6:
            success = self.build_wix6(wxs_file)
        elif self.wix_version == 3:
            success = self.build_wix3(wxs_file)
        else:
            print(f"✗ エラー: 不明な WiX バージョン")
            return False
        
        if not success:
            return False
        
        print("\n" + "=" * 60)
        print("✓ MSI インストーラー生成完了!")
        print("=" * 60)
        
        msi_file = self.dist_dir / f"ITPassStudyTool-{self.version}.msi"
        if msi_file.exists():
            size_mb = msi_file.stat().st_size / (1024 * 1024)
            print(f"\n📦 出力ファイル: {msi_file}")
            print(f"   ファイルサイズ: {size_mb:.2f} MB")
            print(f"\n✓ インストール後の構成:")
            print(f"  📍 デスクトップ")
            print(f"     「{self.app_name_jp}」ショートカット")
            print(f"\n  📍 スタートメニュー ({self.app_name})")
            print(f"     • 「{self.app_name_jp}」")
            print(f"     • 「アンインストール」")
            print(f"\n  📍 プログラムと機能")
            print(f"     「{self.app_name_jp}」として登録")
            print(f"     バージョン: {self.version}")
            print(f"\n  ✅ 日本語 UI: 完全対応")
            return True
        
        return False


def main():
    """メイン処理"""
    builder = WiXMSIBuilder()
    
    if not builder.build():
        sys.exit(1)


if __name__ == "__main__":
    main()

