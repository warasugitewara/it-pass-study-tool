import sys
from pathlib import Path

# エンコーディング設定
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    import pdfplumber
except ImportError:
    print("pdfplumber がインストールされていません。インストール中...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pdfplumber"])
    import pdfplumber

def extract_questions_from_pdf(pdf_path):
    """PDFから問題を抽出"""
    
    print("=" * 70)
    print(f"PDF分析: {pdf_path.name}")
    print("=" * 70)
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"\nPDF開封成功")
            print(f"   ページ数: {len(pdf.pages)}")
            
            # 最初の3ページを分析
            for page_idx in range(min(3, len(pdf.pages))):
                page = pdf.pages[page_idx]
                text = page.extract_text()
                
                print(f"\nページ {page_idx + 1}:")
                print(f"   テキスト長: {len(text)} 文字")
                
                # テキストの最初の 200 文字を表示
                preview = text[:300].replace('\n', '\n   ')
                print(f"\n   内容プレビュー:")
                print(f"   {preview}")
                
                # テーブルも確認
                tables = page.extract_tables()
                if tables:
                    print(f"\n   テーブル数: {len(tables)}")
                    for table_idx, table in enumerate(tables[:1]):
                        print(f"   テーブル {table_idx + 1}:")
                        for row_idx, row in enumerate(table[:3]):  # 最初の3行
                            print(f"      行 {row_idx + 1}: {str(row[:2])[:80]}")
                
                print("\n" + "-" * 70)
            
            return True
    
    except Exception as e:
        print(f"エラー: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    pdf_dir = Path("./pdf_samples")
    
    if not pdf_dir.exists():
        print("PDFディレクトリが見つかりません")
        sys.exit(1)
    
    # 問題冊子を分析
    pdf_file = pdf_dir / "2025r07_ip_qs.pdf"
    
    if pdf_file.exists():
        success = extract_questions_from_pdf(pdf_file)
        if success:
            print("\nPDF抽出成功 - 問題データの抽出が可能です！")
    else:
        print(f"ファイルが見つかりません: {pdf_file}")

