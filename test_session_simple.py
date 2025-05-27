#!/usr/bin/env python3
"""
Simple session test for ALX.trading
"""

import json
import requests
import os

def test_simple_session():
    print("🧪 Simple Session Test")
    print("=" * 30)
    
    # โหลด session data
    session_file = "alx_trading_active_session_20250527_050413.json"
    if not os.path.exists(session_file):
        print("❌ Session file not found")
        return
    
    with open(session_file, 'r') as f:
        session_data = json.load(f)
    
    sessionid = session_data.get('sessionid')
    ds_user_id = session_data.get('ds_user_id')
    
    print(f"📄 SessionID: {sessionid[:20]}...")
    print(f"👤 DS User ID: {ds_user_id}")
    
    # สร้าง session
    session = requests.Session()
    session.cookies.set('sessionid', sessionid, domain='.instagram.com')
    session.cookies.set('ds_user_id', ds_user_id, domain='.instagram.com')
    
    # Headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    session.headers.update(headers)
    
    # ทดสอบเข้าถึง Instagram
    try:
        print("🔄 Testing Instagram access...")
        response = session.get("https://www.instagram.com/", timeout=15)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📏 Content Length: {len(response.text)}")
        
        # ตรวจสอบ content
        content = response.text
        if 'is_logged_in":true' in content:
            print("✅ Logged in detected!")
        elif 'login' in content.lower() and 'password' in content.lower():
            print("❌ Login page detected")
        else:
            print("⚠️ Status unclear")
        
        # ค้นหา username
        import re
        username_match = re.search(r'"username":"([^"]+)"', content)
        if username_match:
            print(f"👤 Username found: {username_match.group(1)}")
        
        # ทดสอบ DM inbox
        print("\n🔄 Testing DM inbox access...")
        dm_response = session.get("https://www.instagram.com/direct/inbox/", timeout=15)
        print(f"📊 DM Status Code: {dm_response.status_code}")
        print(f"📏 DM Content Length: {len(dm_response.text)}")
        
        dm_content = dm_response.text
        if 'DirectInbox' in dm_content:
            print("✅ DM inbox accessible!")
        elif 'login' in dm_content.lower():
            print("❌ DM access redirected to login")
        else:
            print("⚠️ DM status unclear")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_simple_session()
