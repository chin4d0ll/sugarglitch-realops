from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
🔍 INSTAGRAM ACCESS DEBUGGER 🔍
ตรวจสอบสาเหตุที่ไม่สามารถดึงรูปภาพได้
"""

import requests
import json
import os
from fake_useragent import UserAgent


def debug_instagram_access():
    print("🔍 DEBUGGING INSTAGRAM ACCESS")
    print("=" * 40)
    
    # โหลด session data
    session_files = [
        "/workspaces/sugarglitch-realops/extracted_project/Python/success_whatilove1728_20250525_153247.json",
    ]
    
    session_data = None
    for file in session_files:
        if os.path.exists(file):
            try:
                with open(file, 'r') as f:
                    session_data = json.load(f)
                print(f"✅ Loaded session from: {file}")
                break
            except Exception as e:
                print(f"❌ Error loading {file}: {e}")
    
    # ทดสอบการเข้าถึง
    session = requests.Session()
    
    # ตั้งค่า headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    session.headers.update(headers)
    
    # ตั้งค่า cookies ถ้ามี
    if session_data and 'cookies' in session_data:
        for cookie in session_data['cookies']:
            if isinstance(cookie, dict) and 'name' in cookie and 'value' in cookie:
                session.cookies.set(cookie['name'], cookie['value'])
        print(f"🍪 Set {len(session_data['cookies'])} cookies")
    
    # ทดสอบการเข้าถึง
    url = "https://www.instagram.com/whatilove1728/"
    
    try:
        print(f"\n🌐 Testing access to: {url}")
        response = session.get(url, timeout=30, allow_redirects=False)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📏 Content Length: {len(response.text)}")
        print(f"🔗 Redirect Location: {response.headers.get('Location', 'None')}")
        
        # ตรวจสอบ content
        content_snippet = response.text[:500] if response.text else "No content"
        print(f"\n📄 Content Preview:")
        print(content_snippet)
        print("...")
        
        # บันทึกเพื่อการวิเคราะห์
        with open("/workspaces/sugarglitch-realops/debug_response.html", 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"\n💾 Saved response to: /workspaces/sugarglitch-realops/debug_response.html")
        
        # ถ้าถูก redirect ลองตามไป
        if response.status_code in [301, 302, 303, 307, 308]:
            redirect_url = response.headers.get('Location')
            if redirect_url:
                print(f"\n🔄 Following redirect to: {redirect_url}")
                response2 = session.get(redirect_url, timeout=30)
                print(f"📊 Redirect Status: {response2.status_code}")
                print(f"📏 Redirect Content: {len(response2.text)}")
                
                with open("/workspaces/sugarglitch-realops/debug_redirect.html", 'w', encoding='utf-8') as f:
                    f.write(response2.text)
        
        # ทดสอบเข้าถึงหน้า login
        print(f"\n🔐 Testing login page access...")
        login_response = session.get("https://www.instagram.com/accounts/login/", timeout=30)
        print(f"📊 Login page status: {login_response.status_code}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"\n🔍 Debug completed!")


if __name__ == "__main__":
    debug_instagram_access()
