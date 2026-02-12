# PowerShell スクリプト: デスクトップ＆スタートメニューショートカット自動作成
# 実行: powershell -ExecutionPolicy Bypass -File create_shortcuts.ps1

[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "ITパスポート試験学習ツール" -ForegroundColor Cyan
Write-Host "ショートカット自動作成" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# パス設定
$InstallPath = "C:\Program Files\ITPassStudyTool"
$ExePath = "$InstallPath\it-pass-study-tool.exe"
$DesktopPath = [Environment]::GetFolderPath('Desktop')
$StartMenuPath = [Environment]::GetFolderPath('StartMenu')
$ProgramsPath = Join-Path $StartMenuPath "Programs\ITPassStudyTool"

# ショートカット名
$ShortcutName = "ITパスポート試験学習ツール.lnk"

Write-Host "📂 パス情報:" -ForegroundColor Yellow
Write-Host "   インストール先: $InstallPath"
Write-Host "   実行ファイル: $ExePath"
Write-Host "   デスクトップ: $DesktopPath"
Write-Host "   スタートメニュー: $ProgramsPath`n"

# 実行ファイルの存在確認
if (-not (Test-Path $ExePath)) {
    Write-Host "❌ エラー: 実行ファイルが見つかりません" -ForegroundColor Red
    Write-Host "   パス: $ExePath"
    exit 1
}

Write-Host "✅ 実行ファイル確認: OK`n"

# WScript.Shell オブジェクト作成
try {
    $WshShell = New-Object -ComObject WScript.Shell
    Write-Host "✅ WScript.Shell オブジェクト作成: OK"
} catch {
    Write-Host "❌ エラー: WScript.Shell が利用不可です" -ForegroundColor Red
    exit 1
}

# 1. デスクトップショートカット作成
Write-Host "`n📌 デスクトップショートカット作成中..." -ForegroundColor Green
try {
    $DesktopShortcut = Join-Path $DesktopPath $ShortcutName
    $Shortcut = $WshShell.CreateShortcut($DesktopShortcut)
    $Shortcut.TargetPath = $ExePath
    $Shortcut.WorkingDirectory = $InstallPath
    $Shortcut.Description = "ITパスポート試験学習ツール v1.0.0"
    $Shortcut.IconLocation = "$ExePath,0"
    $Shortcut.Save()
    Write-Host "   ✅ 作成完了: $DesktopShortcut"
} catch {
    Write-Host "   ❌ エラー: $_" -ForegroundColor Red
}

# 2. スタートメニュー用フォルダ作成
Write-Host "`n📌 スタートメニュー準備中..." -ForegroundColor Green
try {
    if (-not (Test-Path $ProgramsPath)) {
        New-Item -ItemType Directory -Path $ProgramsPath -Force | Out-Null
        Write-Host "   ✅ フォルダ作成: $ProgramsPath"
    } else {
        Write-Host "   ℹ️  フォルダ既存: $ProgramsPath"
    }
} catch {
    Write-Host "   ❌ エラー: $_" -ForegroundColor Red
}

# 3. スタートメニューショートカット作成
Write-Host "`n📌 スタートメニューショートカット作成中..." -ForegroundColor Green
try {
    $MenuShortcut = Join-Path $ProgramsPath $ShortcutName
    $Shortcut = $WshShell.CreateShortcut($MenuShortcut)
    $Shortcut.TargetPath = $ExePath
    $Shortcut.WorkingDirectory = $InstallPath
    $Shortcut.Description = "ITパスポート試験学習ツール v1.0.0"
    $Shortcut.IconLocation = "$ExePath,0"
    $Shortcut.Save()
    Write-Host "   ✅ 作成完了: $MenuShortcut"
} catch {
    Write-Host "   ❌ エラー: $_" -ForegroundColor Red
}

# 4. アンインストーラショートカット作成（オプション）
Write-Host "`n📌 アンインストールショートカット作成中..." -ForegroundColor Green
try {
    $UninstallPath = "C:\Windows\System32\msiexec.exe"
    $UninstallShortcut = Join-Path $ProgramsPath "アンインストール.lnk"
    $Shortcut = $WshShell.CreateShortcut($UninstallShortcut)
    $Shortcut.TargetPath = $UninstallPath
    $Shortcut.Arguments = "/x {Your-Product-Code} /qn"
    $Shortcut.Description = "ITパスポート試験学習ツール をアンインストール"
    $Shortcut.Save()
    Write-Host "   ✅ 作成完了: $UninstallShortcut"
} catch {
    Write-Host "   ⚠️  スキップ（アンインストーラは手動削除で対応）"
}

# 完了メッセージ
Write-Host "`n========================================" -ForegroundColor Green
Write-Host "✅ ショートカット作成完了！" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Write-Host "📍 作成されたショートカット:" -ForegroundColor Cyan
Write-Host "   1. デスクトップ: $ShortcutName"
Write-Host "   2. スタートメニュー: Programs\ITPassStudyTool\$ShortcutName`n"

Write-Host "🚀 使用方法:" -ForegroundColor Cyan
Write-Host "   1. デスクトップのショートカットをダブルクリック"
Write-Host "   2. または スタートメニュー → すべてのプログラム → ITPassStudyTool"
Write-Host ""

# クリーンアップ
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($WshShell) | Out-Null
[System.GC]::Collect()

Write-Host "操作完了 - このウィンドウを閉じてください"
