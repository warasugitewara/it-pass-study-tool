# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\waras\\Projects\\it-pass-study-tool\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\waras\\Projects\\it-pass-study-tool\\resources', 'resources'), ('C:\\Users\\waras\\Projects\\it-pass-study-tool\\version.txt', '.')],
    hiddenimports=['PySide6', 'PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets', 'PySide6.QtSql', 'sqlalchemy', 'sqlalchemy.orm', 'sqlalchemy.sql', 'pandas', 'numpy', 'openpyxl', 'requests', 'bs4', 'lxml', 'matplotlib', 'apscheduler', 'apscheduler.schedulers.background', 'apscheduler.triggers.cron', 'apscheduler.triggers.interval', 'src', 'src.db', 'src.db.database', 'src.db.models', 'src.ui', 'src.ui.main_window', 'src.ui.quiz_widget', 'src.ui.quiz_config_dialog', 'src.ui.admin_panel', 'src.ui.results_widget', 'src.ui.styles', 'src.core', 'src.core.quiz_engine', 'src.core.statistics', 'src.utils', 'src.utils.config', 'src.utils.data_manager', 'src.utils.scraper', 'src.utils.scraper_scheduler'],
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
