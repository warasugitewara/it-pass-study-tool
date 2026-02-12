#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Scraper Site Analysis Tool
Analyze HTML structure of itpassportsiken.com for data extraction
"""

import requests
from bs4 import BeautifulSoup
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def analyze_kakomon_index():
    """Analyze /kakomon/ index page structure"""
    print("\n=== Analyzing itpassportsiken.com/ipkakomon.php ===\n")
    
    try:
        url = "https://www.itpassportsiken.com/ipkakomon.php"
        print(f"Fetching: {url}")
        
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.encoding = 'utf-8'
        print(f"Status: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all links
        print("\n--- All Links ---")
        links = soup.find_all('a', href=True)
        print(f"Total links: {len(links)}")
        
        exam_links = []
        for link in links[:30]:  # First 30 links
            href = link.get('href', '')
            text = link.get_text(strip=True)[:50]
            if text:
                print(f"  - {text}: {href}")
            
            # Collect exam links
            if 'ipquestion' in href or 'mondai' in href or 'question' in href:
                exam_links.append((text, href))
        
        print(f"\n--- Exam-like links found: {len(exam_links)} ---")
        for text, href in exam_links[:10]:
            print(f"  {text}: {href}")
        
        # Find tables
        print("\n--- Tables ---")
        tables = soup.find_all('table')
        print(f"Total tables: {len(tables)}")
        
        if tables:
            for idx, table in enumerate(tables[:2]):
                print(f"\nTable {idx}:")
                rows = table.find_all('tr')[:5]
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    print(f"  Row: {[c.get_text(strip=True)[:30] for c in cells[:3]]}")
        
        # Check for divs with questions
        print("\n--- Divs with question-like content ---")
        divs = soup.find_all('div', class_=lambda x: x and ('question' in x.lower() or 'mondai' in x.lower() or 'kakomon' in x.lower()))
        print(f"Question-like divs: {len(divs)}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def fetch_sample_question_page():
    """Try to fetch a sample question page"""
    print("\n=== Attempting to fetch sample question page ===\n")
    
    try:
        # Try common URL patterns
        urls = [
            "https://www.itpassportsiken.com/ipquestion01.html",
            "https://www.itpassportsiken.com/ipquestion.php?id=1",
            "https://www.itpassportsiken.com/mondai/2024_haru/q1.html",
        ]
        
        for url in urls:
            print(f"\nTrying: {url}")
            try:
                response = requests.get(url, headers=HEADERS, timeout=5)
                print(f"  Status: {response.status_code}")
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Get title
                    title = soup.find('title')
                    if title:
                        print(f"  Title: {title.get_text()[:80]}")
                    
                    # Find question text
                    text_elements = soup.find_all(['p', 'div'], string=lambda x: x and len(x) > 50)
                    if text_elements:
                        print(f"  Found {len(text_elements)} text elements")
                        print(f"  Sample: {text_elements[0].get_text()[:100]}")
                    
                    break
                    
            except Exception as e:
                print(f"  Failed: {e}")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    print("IT Passport Scraper - Site Analysis Tool")
    print("=" * 60)
    
    analyze_kakomon_index()
    fetch_sample_question_page()
    
    print("\n" + "=" * 60)
    print("\nAnalysis complete. Use results to configure scraper patterns.")
