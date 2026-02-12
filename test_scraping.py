import requests
from bs4 import BeautifulSoup
import json
import time

# itpassportsiken.com のスクレイピングをテスト
def test_scraping():
    """サイトスクレイピングをテストする"""
    
    # 複数のユーザーエージェントを試す
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    ]
    
    print("=" * 60)
    print("🔍 itpassportsiken.com スクレイピング検証")
    print("=" * 60)
    
    # Step 1: 過去問ページにアクセス
    url = "https://www.itpassportsiken.com/kakomon/"
    
    for i, ua in enumerate(user_agents, 1):
        print(f"\n📡 試行 {i}: アクセス {url}")
        print(f"   UA: {ua[:50]}...")
        
        try:
            headers = {
                'User-Agent': ua,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'ja-JP,ja;q=0.9',
                'Referer': 'https://www.google.com/',
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            print(f"   ✅ ステータス: {response.status_code}")
            
            if response.status_code == 200:
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # HTML の構造を確認
                print(f"   📋 ページサイズ: {len(response.content)} bytes")
                print(f"   ✅ HTML パース成功")
                
                # リンク探索
                print(f"\n   🔗 過去問リンク探索...")
                all_links = soup.find_all('a', href=True)
                kakomon_links = [link for link in all_links if 'kakomon' in link.get('href', '')]
                
                print(f"      全リンク数: {len(all_links)}")
                print(f"      kakomon リンク数: {len(kakomon_links)}")
                
                if kakomon_links:
                    print(f"\n      最初の 5 個のリンク:")
                    for j, link in enumerate(kakomon_links[:5]):
                        href = link.get('href', '')
                        text = link.get_text(strip=True)[:50]
                        print(f"         {j+1}. {text[:40]}")
                        print(f"            href={href}")
                
                # ページのタイトルを表示
                print(f"\n      📄 ページのタイトル: {soup.title.string if soup.title else 'N/A'}")
                
                # 問題のようなコンテンツを探す
                print(f"\n      🔎 問題コンテンツの検索...")
                
                selectors = [
                    ('div', 'kakomon'),
                    ('div', 'question'),
                    ('div', 'mondai'),
                    ('article', None),
                    ('section', None),
                ]
                
                found_any = False
                for tag, cls in selectors:
                    if cls:
                        elements = soup.find_all(tag, class_=cls)
                    else:
                        elements = soup.find_all(tag)
                    
                    if elements and len(elements) > 0:
                        found_any = True
                        print(f"         ✓ <{tag} class=\"{cls if cls else '(any)'}\">: {len(elements)} 件")
                
                if not found_any:
                    print(f"         ⚠️  問題コンテンツが見つかりません")
                    print(f"\n         ページの最初の 500 文字:")
                    print(f"         {soup.get_text()[:500]}")
                
                return True
            elif response.status_code == 403:
                print(f"   ❌ 403 Forbidden - アクセス拒否")
                time.sleep(1)  # 少し待機
                continue
            else:
                print(f"   ❌ ステータスエラー: {response.status_code}")
                continue
                
        except requests.Timeout:
            print(f"   ❌ タイムアウト")
            time.sleep(1)
            continue
        except Exception as e:
            print(f"   ❌ エラー: {str(e)}")
            time.sleep(1)
            continue
    
    return False

if __name__ == "__main__":
    success = test_scraping()
    print("\n" + "=" * 60)
    if success:
        print("✅ スクレイピング可能です")
    else:
        print("❌ スクレイピングに問題があります")
        print("\n💡 対策:")
        print("  1. サイトが bot をブロックしている可能性")
        print("  2. robots.txt でスクレイピングが禁止されている可能性")
        print("  3. API の利用を検討")
        print("  4. サンプルデータで代替")
    print("=" * 60)

