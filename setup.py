#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setuptools 設定ファイル（MSI 対応版）
パッケージのビルド・配布用メタデータを定義
"""

from setuptools import setup, find_packages
from pathlib import Path

# プロジェクトディレクトリ
PROJECT_DIR = Path(__file__).parent

# バージョンを読込
def get_version():
    version_file = PROJECT_DIR / "version.txt"
    if version_file.exists():
        with open(version_file, 'r', encoding='utf-8') as f:
            return f.read().strip().split('\n')[0].strip()
    return "1.0.0"

# README を読込
def read_readme():
    readme_file = PROJECT_DIR / "README.md"
    if readme_file.exists():
        with open(readme_file, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

setup(
    name="ITPassStudyTool",
    version=get_version(),
    description="ITパスポート試験学習ツール",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="学習ツール開発チーム",
    author_email="support@example.com",
    url="https://github.com/example/it-pass-study-tool",
    license="MIT",
    
    # パッケージ構成
    packages=find_packages(include=["src", "src.*"]),
    include_package_data=True,
    
    # 依存パッケージ
    install_requires=[
        "PySide6>=6.0.0",
        "sqlalchemy>=2.0.0",
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "openpyxl>=3.6.0",
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.0",
        "lxml>=4.6.0",
        "matplotlib>=3.3.0",
        "apscheduler>=3.10.0",
    ],
    
    # Python バージョン
    python_requires=">=3.8",
    
    # 分類
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
    ],
    
    # キーワード
    keywords=[
        "ITパスポート",
        "学習ツール",
        "試験対策",
        "PySide6",
    ],
)
