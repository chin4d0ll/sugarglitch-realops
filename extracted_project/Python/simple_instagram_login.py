#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 SIMPLE INSTAGRAM LOGIN - API Only
ล็อกอินด้วย API requests เท่านั้น (ไม่ใช้ Chrome)
"""

import requests
import json
import time
import random
from datetime import datetime

class SimpleInstagramLogin:
    def __init__(self):
        self.session = requests.Session()
        self.username = "alx.trading"
        self.password = "Fleming654"
        self.csrf_token = None
        
        # Headers แบบปกติ
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/accounts/login/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
    
    def get_csrf_token(self):
        """🔑 ดึง CSRF token"""
        print("🔑 Getting CSRF token...")
        
        try:
            # ไปหน้า login เพื่อดึง CSRF
            response = self.session.get('https://www.instagram.com/accounts/login/')
            print(f"📡 Login page status: {response.status_code}")
            
            # หา CSRF จาก cookies
            print(f"🍪 Cookies found: {len(self.session.cookies)}")
            for cookie in self.session.cookies:
                print(f"   {cookie.name}: {cookie.value[:20]}...")
                if cookie.name == 'csrftoken':
                    self.csrf_token = cookie.value
                    print(f"✅ CSRF token: {self.csrf_token[:20]}...")
                    return True
            
            # หา CSRF จาก page source - multiple patterns
            import re
            csrf_patterns = [
                r'"csrf_token":"([^"]+)"',
                r'csrftoken=([^;]+)',
                r'csrf_token["\']:["\'](.*?)["\']',
                r'window\._sharedData.*?"csrf_token":"([^"]+)"',
                r'"config":.*?"csrf_token":"([^"]+)"'
            ]
            
            for pattern in csrf_patterns:
                csrf_match = re.search(pattern, response.text)
                if csrf_match:
                    self.csrf_token = csrf_match.group(1)
                    print(f"✅ CSRF from page: {self.csrf_token[:20]}...")
                    return True
            
            # ถ้าไม่เจอ ให้ดู response ตัวอย่าง
            print(f"📄 Page sample: {response.text[:500]}")
            print("❌ CSRF token not found")
            return False
            
        except Exception as e:
            print(f"❌ CSRF error: {e}")
            return False
    
    def login(self):
        """🎯 ล็อกอิน Instagram"""
        print(f"🎯 Logging in as {self.username}...")
        
        try:
            # ดึง CSRF token ก่อน
            if not self.get_csrf_token():
                print("❌ Cannot get CSRF token")
                return False
            
            # Update headers with CSRF
            self.headers['X-CSRFToken'] = self.csrf_token
            
            # Login data
            login_data = {
                'username': self.username,
                'password': self.password,
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }
            
            # ส่ง login request
            login_url = 'https://www.instagram.com/accounts/login/ajax/'
            response = self.session.post(login_url, data=login_data, headers=self.headers)
            
            print(f"📡 Response status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"📄 Response: {json.dumps(result, indent=2)}")
                    
                    if result.get('authenticated'):
                        print("✅ LOGIN SUCCESS!")
                        return self.save_session(result)
                    else:
                        print(f"❌ Login failed: {result}")
                        return False
                        
                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON response: {response.text[:200]}")
                    return False
            else:
                print(f"❌ HTTP error: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def save_session(self, login_result):
        """💾 บันทึก session"""
        print("💾 Saving session data...")
        
        try:
            session_data = {
                'timestamp': datetime.now().strftime('%Y%m%d_%H%M%S'),
                'username': self.username,
                'login_result': login_result,
                'cookies': {},
                'csrf_token': self.csrf_token
            }
            
            # ดึง cookies
            for cookie in self.session.cookies:
                session_data['cookies'][cookie.name] = cookie.value
            
            # บันทึกไฟล์
            filename = f"fresh_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Session saved: {filename}")
            
            # อัพเดต session.json หลัก
            with open('session.json', 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            print("✅ Main session.json updated!")
            return True
            
        except Exception as e:
            print(f"❌ Save session error: {e}")
            return False
    
    def test_session(self):
        """🧪 ทดสอบ session ที่ได้"""
        print("🧪 Testing session...")
        
        try:
            # ลองเข้าหน้า profile
            response = self.session.get('https://www.instagram.com/alx.trading/')
            
            if 'alx.trading' in response.text and 'login' not in response.url:
                print("✅ Session working! Can access profile")
                return True
            else:
                print("❌ Session not working")
                return False
                
        except Exception as e:
            print(f"❌ Session test error: {e}")
            return False

def main():
    print("🚀 SIMPLE INSTAGRAM LOGIN - API Only")
    print("=" * 50)
    print(f"👤 Target: alx.trading")
    print(f"🔑 Password: Fleming654")
    print()
    
    login = SimpleInstagramLogin()
    
    # ดำเนินการล็อกอิน
    if login.login():
        print("\n🎉 SUCCESS! Testing session...")
        login.test_session()
        
        print("\n📊 Next steps:")
        print("1. ✅ Fresh session created")
        print("2. 🔄 Ready to extract real chat data")
        print("3. 🔍 Find women contacts from real Instagram messages")
        
    else:
        print("\n❌ Login failed!")
        print("💡 Possible reasons:")
        print("- Wrong password")
        print("- Account locked/suspended")
        print("- Instagram security measures")
        print("- Rate limiting")

if __name__ == "__main__":
    main()
