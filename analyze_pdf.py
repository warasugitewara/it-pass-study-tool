import sys
from pathlib import Path

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    import PyPDF2
except ImportError:
    print("PyPDF2 インストール中...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
    import PyPDF2

def analyze_pdf_structure(pdf_path):
    """PDFの構造を詳しく分析"""
    
    print("=" * 70)
    print(f"PDF構造分析: {pdf_path.name}")
    print("=" * 70)
    
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            
            print(f"\nPDF情報:")
            print(f"   ページ数: {len(reader.pages)}")
            print(f"   版: {reader.metadata}")
            
            # 最初のページを詳しく分析
            page = reader.pages[0]
            print(f"\n最初のページの詳細:")
            print(f"   コンテンツタイプ: {page.mediabox}")
            
            # テキスト抽出を試みる
            try:
                text = page.extract_text()
                print(f"   テキスト抽出: {'成功' if text else '失敗（スキャン画像の可能性）'}")
                if text:
                    print(f"   テキスト長: {len(text)} 文字")
                    print(f"   プレビュー: {text[:200]}")
            except Exception as e:
                print(f"   テキスト抽出エラー: {e}")
            
            return True
    
    except Exception as e:
        print(f"エラー: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    pdf_dir = Path("./pdf_samples")
    pdf_file = pdf_dir / "2025r07_ip_qs.pdf"
    
    if pdf_file.exists():
        analyze_pdf_structure(pdf_file)
    else:
        print(f"ファイルが見つかりません: {pdf_file}")
