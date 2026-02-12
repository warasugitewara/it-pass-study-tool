import sys
from pathlib import Path

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Tesseract OCR をテスト
try:
    import pytesseract
    from PIL import Image
    import pdf2image
except ImportError:
    print("必要なライブラリをインストール中...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pytesseract", "pdf2image", "Pillow"])
    import pytesseract
    from PIL import Image
    import pdf2image

def test_ocr_setup():
    """OCRセットアップをテスト"""
    
    print("=" * 70)
    print("OCR セットアップテスト")
    print("=" * 70)
    
    # Tesseract が インストール されているか確認
    try:
        result = pytesseract.get_tesseract_version()
        print(f"\nTesseract OCR: インストール済み")
        print(f"   バージョン: {result}")
    except pytesseract.TesseractNotFoundError:
        print("\nTesseract OCR: インストールされていません")
        print("Tesseract をインストールしてください:")
        print("  Windows: https://github.com/UB-Mannheim/tesseract/wiki")
        print("  Linux: sudo apt-get install tesseract-ocr")
        print("  macOS: brew install tesseract")
        return False
    
    return True

def convert_pdf_to_images(pdf_path, output_dir, first_n_pages=None):
    """PDFを画像に変換"""
    
    print(f"\nPDF を画像に変換中...")
    print(f"   入力: {pdf_path.name}")
    print(f"   出力先: {output_dir}")
    
    output_dir.mkdir(exist_ok=True)
    
    try:
        images = pdf2image.convert_from_path(pdf_path, first_page=1, last_page=first_n_pages)
        
        for i, image in enumerate(images):
            output_file = output_dir / f"page_{i+1:03d}.png"
            image.save(output_file)
            print(f"   ✓ ページ {i+1}: {output_file.name}")
        
        return images
    
    except Exception as e:
        print(f"   エラー: {e}")
        return None

def extract_text_from_image(image_path):
    """画像からテキストを OCR で抽出"""
    
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='jpn+eng')
        return text
    except Exception as e:
        print(f"   OCR エラー: {e}")
        return None

if __name__ == "__main__":
    # OCR セットアップをテスト
    if not test_ocr_setup():
        sys.exit(1)
    
    # PDF を画像に変換（最初の5ページのみテスト）
    pdf_dir = Path("./pdf_samples")
    pdf_file = pdf_dir / "2025r07_ip_qs.pdf"
    
    if not pdf_file.exists():
        print(f"\nファイルが見つかりません: {pdf_file}")
        sys.exit(1)
    
    image_dir = Path("./pdf_images")
    
    print("\n" + "=" * 70)
    print("PDFからの画像抽出")
    print("=" * 70)
    
    images = convert_pdf_to_images(pdf_file, image_dir, first_n_pages=5)
    
    if images:
        print(f"\n✓ {len(images)} ページを画像に変換しました")
        
        # 最初の1ページで OCR テスト
        print("\n" + "=" * 70)
        print("OCR テスト（ページ 1）")
        print("=" * 70)
        
        first_image = image_dir / "page_001.png"
        text = extract_text_from_image(first_image)
        
        if text:
            print(f"\nOCR 抽出成功")
            print(f"   テキスト長: {len(text)} 文字")
            print(f"\n   抽出テキスト（最初の 500 文字）:")
            print(f"   {text[:500]}")
        else:
            print("\nOCR 抽出失敗")
