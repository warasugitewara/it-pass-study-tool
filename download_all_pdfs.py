#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IPA公式ITパスポート試験 - 10年分データ取得・整理ツール
最新年度から10年分の問題と解答をダウンロード
"""
import sys
import json
from pathlib import Path
from urllib.request import urlopen, urlretrieve
from urllib.error import URLError, HTTPError
import time

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 年度データ定義: (ファイルコード, 年号, 日本語年度)
EXAM_YEARS = [
    ('2025r07', 2025, '令和7年度'),
    ('2024r06', 2024, '令和6年度'),
    ('2023r05', 2023, '令和5年度'),
    ('2022r04', 2022, '令和4年度'),
    ('2021r03', 2021, '令和3年度'),
    ('2020r02o', 2020, '令和2年度'),
    ('2019r01a', 2019, '令和元年度'),
    ('2018h30a', 2018, '平成30年度'),
    ('2017h29a', 2017, '平成29年度'),
    ('2016h28a', 2016, '平成28年度'),
]

BASE_URL = "https://www3.jitec.ipa.go.jp/JitesCbt/html/openinfo/pdf/questions"

def download_pdf(file_code, pdf_type):
    """PDFファイルをダウンロード"""
    filename = f"{file_code}_ip_{pdf_type}.pdf"
    url = f"{BASE_URL}/{filename}"
    
    output_dir = Path("./pdf_samples")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / filename
    
    if output_file.exists():
        print(f"  ✓ キャッシュ済み: {filename} ({output_file.stat().st_size / 1024 / 1024:.2f} MB)")
        return output_file
    
    print(f"  📥 ダウンロード中: {filename}", end='', flush=True)
    
    try:
        urlretrieve(url, output_file)
        size_mb = output_file.stat().st_size / 1024 / 1024
        print(f" ✓ ({size_mb:.2f} MB)")
        return output_file
    
    except (URLError, HTTPError) as e:
        print(f" ❌ エラー: {e}")
        if output_file.exists():
            output_file.unlink()
        return None
    
    except Exception as e:
        print(f" ❌ 予期しないエラー: {e}")
        if output_file.exists():
            output_file.unlink()
        return None

def download_all_pdfs():
    """全年度のPDFをダウンロード"""
    print("=" * 80)
    print("IPA公式試験問題 - 10年分データ取得ツール")
    print("=" * 80)
    print()
    
    total_size = 0
    downloaded_files = {
        'questions': [],
        'answers': []
    }
    
    for file_code, year, year_text in EXAM_YEARS:
        print(f"[{year}年度 {year_text}]")
        
        # 問題冊子
        qs_file = download_pdf(file_code, 'qs')
        if qs_file:
            downloaded_files['questions'].append({
                'year': year,
                'year_text': year_text,
                'file_code': file_code,
                'path': str(qs_file),
                'type': 'questions'
            })
            total_size += qs_file.stat().st_size
        
        # 解答例
        ans_file = download_pdf(file_code, 'ans')
        if ans_file:
            downloaded_files['answers'].append({
                'year': year,
                'year_text': year_text,
                'file_code': file_code,
                'path': str(ans_file),
                'type': 'answers'
            })
            total_size += ans_file.stat().st_size
        
        time.sleep(0.5)  # サーバー負荷軽減
        print()
    
    # 結果を保存
    manifest = {
        'download_date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_files': len(downloaded_files['questions']) + len(downloaded_files['answers']),
        'total_size_mb': total_size / 1024 / 1024,
        'years_covered': [y for _, y, _ in EXAM_YEARS],
        'files': downloaded_files
    }
    
    manifest_file = Path("./pdf_samples/manifest.json")
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print("=" * 80)
    print("✅ ダウンロード完了")
    print("=" * 80)
    print(f"総ファイル数: {manifest['total_files']}")
    print(f"合計サイズ: {manifest['total_size_mb']:.2f} MB")
    print(f"対象年度: {len(manifest['years_covered'])}年度")
    print(f"マニフェスト: {manifest_file}")
    print()
    
    return manifest

if __name__ == "__main__":
    manifest = download_all_pdfs()
