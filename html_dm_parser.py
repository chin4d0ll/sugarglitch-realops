#!/usr/bin/env python3
"""
HTML DM Parser - แยก DM data จาก Instagram HTML
"""
import re
import json
import requests
from datetime import datetime
import os

def extract_dm_data_from_html():
    print("🔍 HTML DM DATA EXTRACTOR")
    print("="*40)
    
    # โหลด session
    try:
        with open('tools/session_alx_trading.json', 'r') as f:
            session = json.load(f)
        sessionid = session.get('sessionid', '')
        print(f"✅ Session: {sessionid[:15]}...")
    except:
        print("❌ No session file")
        return
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': f'sessionid={sessionid}; ig_did=94BD1C3E-8B5D-4C91-9F61-25C4E6A0A4EC',
        'Referer': 'https://www.instagram.com/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    print("🌐 Getting Instagram DM page...")
    
    try:
        response = requests.get('https://www.instagram.com/direct/inbox/', headers=headers, timeout=15)
        
        if response.status_code == 200:
            html = response.text
            print(f"✅ Got HTML page ({len(html)} chars)")
            
            # แยก window._sharedData
            shared_data_match = re.search(r'window\._sharedData\s*=\s*({.*?});', html)
            if shared_data_match:
                try:
                    shared_data = json.loads(shared_data_match.group(1))
                    print("✅ Found window._sharedData")
                    
                    # หา DM data
                    entry_data = shared_data.get('entry_data', {})
                    print(f"📊 entry_data keys: {list(entry_data.keys())}")
                    
                    # เช็ค DirectPage
                    if 'DirectPage' in entry_data:
                        direct_page = entry_data['DirectPage'][0]
                        print("🎯 Found DirectPage data!")
                        
                        # บันทึกผลลัพธ์
                        output_file = f'results/dm_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                        os.makedirs('results', exist_ok=True)
                        
                        with open(output_file, 'w') as f:
                            json.dump(direct_page, f, indent=2)
                        
                        print(f"💾 DM data saved to: {output_file}")
                        
                        # แสดงข้อมูลสำคัญ
                        graphql = direct_page.get('graphql', {})
                        viewer = graphql.get('viewer', {})
                        
                        if viewer:
                            print(f"👤 User: {viewer.get('username', 'Unknown')}")
                            print(f"📱 User ID: {viewer.get('id', 'Unknown')}")
                        
                        return True
                        
                except json.JSONDecodeError as e:
                    print(f"❌ JSON decode error: {e}")
            
            # แยก window.__additionalDataLoaded
            additional_data_matches = re.findall(r'window\.__additionalDataLoaded\([^,]+,\s*({.*?})\);', html)
            if additional_data_matches:
                print(f"✅ Found {len(additional_data_matches)} additional data chunks")
                
                for i, match in enumerate(additional_data_matches):
                    try:
                        data = json.loads(match)
                        if 'inbox' in str(data).lower() or 'direct' in str(data).lower():
                            print(f"🎯 Found potential DM data in chunk {i}")
                            
                            output_file = f'results/additional_dm_data_{i}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                            with open(output_file, 'w') as f:
                                json.dump(data, f, indent=2)
                            
                            print(f"💾 Chunk {i} saved to: {output_file}")
                    except:
                        continue
            
            # บันทึก HTML สำหรับการวิเคราะห์
            html_file = f'results/dm_page_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"💾 Full HTML saved to: {html_file}")
            
            return True
            
        else:
            print(f"❌ HTTP error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    extract_dm_data_from_html()
