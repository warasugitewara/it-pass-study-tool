import requests
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_ipa_pdf():
    """IPA公式サイトから最新のPDFをダウンロード"""
    
    print("=" * 70)
    print("📥 IPA公式PDFダウンロードテスト")
    print("=" * 70)
    
    # 最新版：令和7年度（2025年）
    base_url = "https://www3.jitec.ipa.go.jp/JitesCbt/html/openinfo/pdf/questions"
    
    files_to_download = [
        ("2025r07_ip_qs.pdf", "問題冊子"),
        ("2025r07_ip_ans.pdf", "解答例"),
    ]
    
    download_dir = Path("./pdf_samples")
    download_dir.mkdir(exist_ok=True)
    
    for filename, description in files_to_download:
        url = f"{base_url}/{filename}"
        output_path = download_dir / filename
        
        print(f"\n📡 ダウンロード: {description}")
        print(f"   URL: {url}")
        print(f"   保存先: {output_path}")
        
        try:
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                size_mb = len(response.content) / (1024 * 1024)
                print(f"   ✅ ダウンロード成功: {size_mb:.2f} MB")
            else:
                print(f"   ❌ ステータスエラー: {response.status_code}")
        
        except Exception as e:
            print(f"   ❌ エラー: {str(e)}")
    
    # PDFの存在確認
    print(f"\n📂 ダウンロード済みファイル:")
    for pdf_file in download_dir.glob("*.pdf"):
        size_mb = pdf_file.stat().st_size / (1024 * 1024)
        print(f"   ✓ {pdf_file.name}: {size_mb:.2f} MB")
    
    return download_dir

if __name__ == "__main__":
    pdf_dir = download_ipa_pdf()
    
    print("\n" + "=" * 70)
    print("✅ PDFダウンロード完了")
    print("=" * 70)
