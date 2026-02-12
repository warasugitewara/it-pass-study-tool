@echo off
REM -*- coding: utf-8 -*-
REM ITパスポート試験学習ツール - ポストインストールスクリプト
REM インストール後に自動実行される

setlocal enabledelayedexpansion

:: カラー出力（Windows 10以降）
for /F %%A in ('echo prompt $H ^| cmd') do set "BS=%%A"

echo.
echo ============================================
echo ITパスポート試験学習ツール - セットアップ完了
echo ============================================
echo.

:: インストール先を検出
set "INSTALL_PATH=%ProgramFiles%\ITPassStudyTool"
set "EXE_PATH=%INSTALL_PATH%\it-pass-study-tool.exe"
set "SHORTCUT_DESKTOP=%USERPROFILE%\Desktop\ITパスポート試験学習ツール.lnk"
set "SHORTCUT_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs\ITPassStudyTool\ITパスポート試験学習ツール.lnk"

echo インストール先: %INSTALL_PATH%
echo 実行ファイル: %EXE_PATH%
echo.

:: ショートカット作成用 PowerShell スクリプト実行
echo PowerShell でショートカットを作成中...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$Shell = New-Object -COM WScript.Shell; ^
   $Shortcut = $Shell.CreateShortcut('%SHORTCUT_DESKTOP%'); ^
   $Shortcut.TargetPath = '%EXE_PATH%'; ^
   $Shortcut.WorkingDirectory = '%INSTALL_PATH%'; ^
   $Shortcut.Description = 'ITパスポート試験学習ツール v1.0.0'; ^
   $Shortcut.Save(); ^
   Write-Host 'デスクトップショートカット作成: OK'"

:: スタートメニュー用フォルダ作成
if not exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\ITPassStudyTool" (
  mkdir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\ITPassStudyTool"
)

:: スタートメニューショートカット作成
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$Shell = New-Object -COM WScript.Shell; ^
   $Shortcut = $Shell.CreateShortcut('%SHORTCUT_MENU%'); ^
   $Shortcut.TargetPath = '%EXE_PATH%'; ^
   $Shortcut.WorkingDirectory = '%INSTALL_PATH%'; ^
   $Shortcut.Description = 'ITパスポート試験学習ツール v1.0.0'; ^
   $Shortcut.Save(); ^
   Write-Host 'スタートメニューショートカット作成: OK'"

echo.
echo ============================================
echo ✅ セットアップ完了！
echo ============================================
echo.
echo 以下の場所にショートカットが作成されました：
echo   1. デスクトップ
echo   2. スタートメニュー (ITPassStudyTool)
echo.
echo 使用方法:
echo   - デスクトップのショートカットをダブルクリック
echo   - または スタートメニューから実行
echo.
pause
