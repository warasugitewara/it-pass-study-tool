#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MSI インストーラー生成用 setup.py
"""

from setuptools import setup

setup(
    name="ITPassStudyTool",
    version="1.0.0",
    description="ITパスポート試験学習ツール",
    author="学習ツール開発チーム",
    author_email="support@example.com",
    url="https://github.com/example/it-pass-study-tool",
    license="MIT",
    
    # MSI 固有の設定
    options={
        'bdist_msi': {
            'add_to_path': False,
        },
    },
    
    # スクリプト/エントリーポイント
    entry_points={},
)
