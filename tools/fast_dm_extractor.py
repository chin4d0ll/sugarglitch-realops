#!/usr/bin/env python3
"""
Fast DM Extractor - รันเร็ว ไม่ค้าง
"""
import requests
import json
import os
from datetime import datetime

def load_session():
    """โหลด session เร็วๆ"""
    try:
        with open('tools/session_alx_trading.json', 'r') as f:
            return json.load(f)
    except:
        return None

def load_proxies():
    """โหลด proxies เร็วๆ"""
    try:
        with open('config/proxies.json', 'r') as f:
            proxies = json.load(f)
            return proxies if isinstance(proxies, list) else []
    except:
        return []

def extract_dms_fast():
    """ดึง DMs เร็วๆ ไม่ค้าง"""
    print("🚀 Fast DM extraction...")
    
    session = load_session()
    if not session:
        print("❌ No session found")
        return False
    
    proxies = load_proxies()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Cookie': f'sessionid={session.get("sessionid", "")}',
        'x-csrftoken': session.get('csrftoken', ''),
        'x-ig-app-id': '936619743392459'
    }
    
    # ลอง 3 proxy แรก
    for i, proxy in enumerate(proxies[:3]):
        try:
            print(f"Trying proxy {i+1}...")
            proxy_dict = {'http': proxy, 'https': proxy}
            
            # ทดสอบ DM access
            response = requests.get(
                'https://www.instagram.com/api/v1/direct_v2/inbox/',
                headers=headers,
                proxies=proxy_dict,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                threads = data.get('inbox', {}).get('threads', [])
                
                print(f"✅ Found {len(threads)} DM threads")
                
                # บันทึกผลลัพธ์
                result = {
                    'extraction_time': datetime.now().isoformat(),
                    'total_threads': len(threads),
                    'proxy_used': proxy,
                    'threads': threads[:5]  # เก็บแค่ 5 อันแรก
                }
                
                os.makedirs('results', exist_ok=True)
                with open('results/fast_dm_extraction.json', 'w') as f:
                    json.dump(result, f, indent=2)
                
                print("✅ Extraction completed!")
                return True
                
            elif response.status_code in [401, 403]:
                print("❌ Session expired")
                return False
            else:
                print(f"❌ HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error with proxy {i+1}: {str(e)[:50]}...")
            continue
    
    print("❌ All proxies failed")
    return False

def main():
    print("⚡ FAST DM EXTRACTOR - NO HANG!")
    print("="*40)
    
    success = extract_dms_fast()
    if success:
        print("🎉 DM extraction successful!")
    else:
        print("❌ DM extraction failed")

if __name__ == "__main__":
    main()
