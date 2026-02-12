# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\waras\\Projects\\it-pass-study-tool\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\waras\\Projects\\it-pass-study-tool\\resources', 'resources')],
    hiddenimports=['PySide6', 'PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets', 'PySide6.QtSql', 'sqlalchemy', 'sqlalchemy.orm', 'sqlalchemy.sql', 'pandas', 'numpy', 'openpyxl', 'requests', 'bs4', 'lxml', 'matplotlib', 'src', 'src.db', 'src.db.database', 'src.db.models', 'src.ui', 'src.ui.main_window', 'src.ui.widgets', 'src.ui.dialogs', 'src.core', 'src.core.question_manager', 'src.core.statistics', 'src.utils', 'src.utils.helpers', 'src.utils.validators'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='it-pass-study-tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
