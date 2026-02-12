import sys
from pathlib import Path
import json

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    import easyocr
    import pdf2image
    from PIL import Image
except ImportError:
    print("必要なライブラリをインストール中...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "easyocr", "pdf2image", "torch"])
    import easyocr
    import pdf2image
    from PIL import Image

def extract_pdf_with_easyocr(pdf_path, max_pages=10):
    """EasyOCRを使用してPDFから日本語テキストを抽出"""
    
    print("=" * 70)
    print(f"EasyOCR による PDF テキスト抽出")
    print("=" * 70)
    print(f"\nPDF: {pdf_path.name}")
    print(f"最初の {max_pages} ページを処理")
    
    try:
        # EasyOCR リーダーを初期化（日本語）
        print("\nOCRエンジンを初期化中（初回は時間がかかります）...")
        reader = easyocr.Reader(['ja', 'en'], gpu=False)
        print("✓ OCRエンジン準備完了")
        
        # PDFを画像に変換
        print(f"\nPDFを画像に変換中...")
        images = pdf2image.convert_from_path(pdf_path, first_page=1, last_page=max_pages)
        print(f"✓ {len(images)} ページを画像に変換")
        
        all_text = {}
        
        for page_idx, image in enumerate(images):
            print(f"\nページ {page_idx + 1} をOCR処理中...")
            
            try:
                # OCR実行
                results = reader.readtext(image)
                
                # 抽出テキストを結合
                text_lines = []
                for detection in results:
                    text = detection[1]
                    confidence = detection[2]
                    text_lines.append(text)
                
                full_text = '\n'.join(text_lines)
                all_text[f'page_{page_idx + 1}'] = {
                    'text': full_text,
                    'detections': len(results)
                }
                
                print(f"  ✓ {len(results)} 個のテキスト領域を検出")
                print(f"  テキスト長: {len(full_text)} 文字")
                
                # プレビュー表示
                preview = full_text[:300].replace('\n', '\n     ')
                print(f"  プレビュー: {preview}")
            
            except Exception as e:
                print(f"  エラー: {e}")
        
        return all_text
    
    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    pdf_dir = Path("./pdf_samples")
    pdf_file = pdf_dir / "2025r07_ip_qs.pdf"
    
    if not pdf_file.exists():
        print(f"ファイルが見つかりません: {pdf_file}")
        sys.exit(1)
    
    # 最初の3ページをOCR処理
    results = extract_pdf_with_easyocr(pdf_file, max_pages=3)
    
    if results:
        print("\n" + "=" * 70)
        print("✓ OCR 抽出完了")
        print("=" * 70)
        
        # 結果をJSONで保存
        output_file = Path("./ocr_results.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n結果を保存: {output_file}")
