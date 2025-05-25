#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ QUICK CHAT EXTRACTOR
ดึงข้อมูลแชทจริงเร็ว ๆ ด้วย session ที่ work
"""

import json
import requests
from datetime import datetime

def extract_real_chats():
    print("⚡ QUICK CHAT EXTRACTOR")
    print("=" * 40)
    
    # โหลด session
    try:
        with open('session.json', 'r') as f:
            session_data = json.load(f)
        
        session = requests.Session()
        session.cookies.set('sessionid', session_data['sessionid'], domain='.instagram.com')
        session.cookies.set('ds_user_id', session_data['ds_user_id'], domain='.instagram.com')
        
        print("✅ Session loaded")
        
    except Exception as e:
        print(f"❌ Session error: {e}")
        return
    
    # ดึงหน้า DM
    print("📱 ดึงหน้า Direct Messages...")
    
    try:
        response = session.get('https://www.instagram.com/direct/inbox/')
        
        if response.status_code == 200:
            print(f"✅ ได้หน้า DM แล้ว ({len(response.text):,} characters)")
            
            # บันทึกหน้า DM
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"real_dm_page_{timestamp}.html"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"💾 บันทึกแล้ว: {filename}")
            
            # หาข้อมูลผู้หญิงในหน้า
            text = response.text.lower()
            
            female_keywords = ['girl', 'woman', 'lady', 'princess', 'queen', 'baby', 'cute', 'pretty']
            women_found = []
            
            for keyword in female_keywords:
                if keyword in text:
                    women_found.append(keyword)
            
            if women_found:
                print(f"👩 เจอ keywords ผู้หญิง: {', '.join(women_found)}")
            else:
                print("❌ ไม่เจอ keywords ผู้หญิงในหน้า DM")
            
            # หา JSON data ในหน้า
            import re
            json_matches = re.findall(r'({[^{}]*"username"[^{}]*})', response.text)
            
            if json_matches:
                print(f"🔍 เจอ JSON patterns: {len(json_matches)} รายการ")
                
                json_filename = f"dm_json_data_{timestamp}.json"
                with open(json_filename, 'w', encoding='utf-8') as f:
                    json.dump(json_matches, f, indent=2, ensure_ascii=False)
                
                print(f"💾 JSON data บันทึกแล้ว: {json_filename}")
            else:
                print("❌ ไม่เจอ JSON patterns")
            
        else:
            print(f"❌ ไม่สามารถเข้าหน้า DM ได้: {response.status_code}")
    
    except Exception as e:
        print(f"❌ DM extraction error: {e}")

if __name__ == "__main__":
    extract_real_chats()
