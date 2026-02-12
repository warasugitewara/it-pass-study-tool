import requests
from bs4 import BeautifulSoup
import json

def test_ipa_scraping():
    """IPA公式サイトからのスクレイピングをテスト"""
    
    url = "https://www3.jitec.ipa.go.jp/JitesCbt/html/openinfo/questions.html"
    
    print("=" * 70)
    print("🔍 IPA公式サイト スクレイピング検証")
    print("=" * 70)
    print(f"\n📡 URL: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ja-JP,ja;q=0.9',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"\n✅ ステータス: {response.status_code}")
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            print(f"✅ ページ解析成功")
            print(f"   ページサイズ: {len(response.content):,} bytes")
            
            # タイトル確認
            if soup.title:
                print(f"   ページタイトル: {soup.title.string}")
            
            # リンク探索
            print(f"\n🔗 リンク探索...")
            all_links = soup.find_all('a', href=True)
            print(f"   全リンク数: {len(all_links)}")
            
            # PDF/データリンクを探す
            pdf_links = [link for link in all_links if '.pdf' in link.get('href', '').lower()]
            print(f"   PDFリンク: {len(pdf_links)}")
            
            if pdf_links:
                print(f"\n   最初の5つのPDFリンク:")
                for i, link in enumerate(pdf_links[:5]):
                    href = link.get('href', '')
                    text = link.get_text(strip=True)[:50]
                    print(f"      {i+1}. {text}")
                    print(f"         {href[:70]}")
            
            # テーブル探索
            print(f"\n📊 テーブル探索...")
            tables = soup.find_all('table')
            print(f"   テーブル数: {len(tables)}")
            
            for i, table in enumerate(tables[:3]):
                rows = table.find_all('tr')
                cols = table.find_all('td')
                print(f"      テーブル{i+1}: {len(rows)} 行, {len(cols)} セル")
                
                # 最初の行を表示
                if rows:
                    first_row_text = rows[0].get_text(strip=True)[:80]
                    print(f"         内容: {first_row_text}")
            
            # 問題リストの探索
            print(f"\n📝 問題コンテンツ探索...")
            
            # div や section で問題のようなコンテンツを探す
            content_divs = soup.find_all(['div', 'section', 'article'])
            print(f"   div/section/article: {len(content_divs)} 件")
            
            # テキストを見て問題らしいものを探す
            all_text = soup.get_text()
            if '過去問' in all_text:
                print(f"   ✓ '過去問' というテキストが含まれています")
            if 'ITパスポート' in all_text:
                print(f"   ✓ 'ITパスポート' というテキストが含まれています")
            if '問題' in all_text:
                print(f"   ✓ '問題' というテキストが含まれています")
            
            # 年号や季節を探す
            seasons = ['春', '秋', '冬', '夏']
            years = ['2024', '2025', '2026']
            
            found_seasons = [s for s in seasons if s in all_text]
            found_years = [y for y in years if y in all_text]
            
            if found_seasons:
                print(f"   ✓ 季節情報: {', '.join(found_seasons)}")
            if found_years:
                print(f"   ✓ 年号情報: {', '.join(found_years)}")
            
            # HTMLの概要を表示
            print(f"\n📄 ページの最初の 1000 文字:")
            print("   " + all_text[:1000].replace('\n', '\n   '))
            
            return True
        else:
            print(f"❌ ステータスエラー: {response.status_code}")
            return False
    
    except requests.Timeout:
        print(f"❌ タイムアウト")
        return False
    except Exception as e:
        print(f"❌ エラー: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ipa_scraping()
    print("\n" + "=" * 70)
    if success:
        print("✅ IPA公式サイトからのスクレイピングが可能です！")
    else:
        print("❌ スクレイピングに問題があります")
    print("=" * 70)
