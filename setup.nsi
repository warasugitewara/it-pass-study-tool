; ITパスポート試験学習ツール インストーラースクリプト
; NSIS (Nullsoft Scriptable Install System) version 3.08+

!include "MUI2.nsh"
!include "x64.nsh"

; ====================================================================
; 基本設定
; ====================================================================
Name "ITパスポート試験学習ツール"
OutFile "ITPassStudyTool-1.0.0-installer.exe"
InstallDir "$PROGRAMFILES\ITPassStudyTool"
InstallDirRegKey HKLM "Software\ITPassStudyTool" "InstallDir"

; リクエスト実行レベル
RequestExecutionLevel admin

; ====================================================================
; MUI2 設定
; ====================================================================
!define MUI_ABORTWARNING
!define MUI_ICON "resources\icons\app.ico"
!define MUI_UNICON "resources\icons\app.ico"

; インストーラーページ
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; アンインストーラーページ
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; 言語設定
!insertmacro MUI_LANGUAGE "Japanese"

; ====================================================================
; セクション定義
; ====================================================================

; メインインストールセクション
Section "ITパスポート試験学習ツール" SecMain
  SectionIn RO
  SetOutPath "$INSTDIR"
  
  ; アプリケーション実行ファイルをコピー
  File "dist\it-pass-study-tool.exe"
  
  ; サポートファイルをコピー
  SetOutPath "$INSTDIR\resources"
  File /r "resources\*.*"
  
  ; バージョン情報ファイル
  SetOutPath "$INSTDIR"
  File "version.txt"
  
  ; レジストリへの登録
  WriteRegStr HKLM "Software\ITPassStudyTool" "InstallDir" "$INSTDIR"
  WriteRegStr HKLM "Software\ITPassStudyTool" "Version" "1.0.0"
  
  ; アンインストール情報をレジストリに登録
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ITPassStudyTool" \
    "DisplayName" "ITパスポート試験学習ツール"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ITPassStudyTool" \
    "UninstallString" "$INSTDIR\uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ITPassStudyTool" \
    "DisplayVersion" "1.0.0"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ITPassStudyTool" \
    "Publisher" "ITPass Study Tool"
  
  ; アンインストーラーを作成
  WriteUninstaller "$INSTDIR\uninstall.exe"
  
SectionEnd

; スタートメニュー作成セクション（オプション）
Section "スタートメニューショートカット" SecStartMenu
  SetShellVarContext all
  CreateDirectory "$SMPROGRAMS\ITPassStudyTool"
  CreateShortcut "$SMPROGRAMS\ITPassStudyTool\ITパスポート試験学習ツール.lnk" \
    "$INSTDIR\it-pass-study-tool.exe" "" "$INSTDIR\it-pass-study-tool.exe" 0
  CreateShortcut "$SMPROGRAMS\ITPassStudyTool\アンインストール.lnk" \
    "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
SectionEnd

; デスクトップショートカット作成セクション（オプション）
Section "デスクトップショートカット" SecDesktop
  SetShellVarContext all
  CreateShortcut "$DESKTOP\ITパスポート試験学習ツール.lnk" \
    "$INSTDIR\it-pass-study-tool.exe" "" "$INSTDIR\it-pass-study-tool.exe" 0
SectionEnd

; セクション説明
LangString DESC_SecMain ${LANG_JAPANESE} "ITパスポート試験学習ツール - メインアプリケーション"
LangString DESC_SecStartMenu ${LANG_JAPANESE} "Windows スタートメニューにショートカットを作成します"
LangString DESC_SecDesktop ${LANG_JAPANESE} "デスクトップにショートカットを作成します"

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
!insertmacro MUI_DESCRIPTION_TEXT ${SecMain} $(DESC_SecMain)
!insertmacro MUI_DESCRIPTION_TEXT ${SecStartMenu} $(DESC_SecStartMenu)
!insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} $(DESC_SecDesktop)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; ====================================================================
; アンインストールセクション
; ====================================================================

Section "Uninstall"
  SetShellVarContext all
  
  ; スタートメニューショートカット削除
  RMDir /r "$SMPROGRAMS\ITPassStudyTool"
  
  ; デスクトップショートカット削除
  Delete "$DESKTOP\ITパスポート試験学習ツール.lnk"
  
  ; インストールディレクトリからファイル削除
  Delete "$INSTDIR\it-pass-study-tool.exe"
  Delete "$INSTDIR\version.txt"
  Delete "$INSTDIR\uninstall.exe"
  RMDir /r "$INSTDIR\resources"
  
  ; インストールディレクトリ削除
  RMDir "$INSTDIR"
  
  ; レジストリエントリー削除
  DeleteRegKey HKLM "Software\ITPassStudyTool"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ITPassStudyTool"
  
SectionEnd

; ====================================================================
; コールバック関数
; ====================================================================

Function .onInit
  ; Windows 7 以上かチェック
  ${If} ${AtMostWinVista}
    MessageBox MB_ICONEXCLAMATION|MB_OK "このアプリケーションは Windows 10 以上が必要です。"
    Quit
  ${EndIf}
FunctionEnd

Function .onInstSuccess
  MessageBox MB_ICONINFORMATION|MB_OK "インストールが完了しました。$\n$\nアプリケーションを起動できます。"
FunctionEnd

Function un.onUninstSuccess
  MessageBox MB_ICONINFORMATION|MB_OK "アンインストールが完了しました。"
FunctionEnd
