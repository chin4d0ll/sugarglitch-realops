#!/usr/bin/env python3
"""
🎯 SIMPLE INSTAGRAM API TESTER
ใช้ session ที่มีอยู่ + manual CSRF เพื่อหลีกเลี่ยง rate limit
"""

import requests
import json
import time
import random
from datetime import datetime

class SimpleInstagramTester:
    def __init__(self):
        # ใช้ session ที่มี
        self.session_file = "/workspaces/sugarglitch-realops/sessions/alx_trading_sessionid_1748519715.json"
        self.session_data = {}
        self.load_session()
        
        # Instagram API endpoints ที่ใช้ได้
        self.endpoints = {
            'profile': 'https://www.instagram.com/api/v1/users/web_profile_info/?username={}',
            'user_info': 'https://i.instagram.com/api/v1/users/{}/info/',
            'search': 'https://www.instagram.com/web/search/topsearch/?context=blended&query={}'
        }
        
    def load_session(self):
        """โหลด session ที่มี"""
        try:
            with open(self.session_file, 'r') as f:
                self.session_data = json.load(f)
            print(f"✅ Loaded session: {list(self.session_data.keys())}")
        except Exception as e:
            print(f"❌ Session load error: {e}")
    
    def create_headers(self, csrf_token=None):
        """สร้าง headers ที่จำเป็น"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.instagram.com/',
            'X-Requested-With': 'XMLHttpRequest',
            'X-IG-App-ID': '936619743392459',
            'X-Instagram-AJAX': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }
        
        if csrf_token:
            headers['X-CSRFToken'] = csrf_token
            
        return headers
    
    def create_cookies(self):
        """สร้าง cookies จาก session"""
        cookies = {}
        
        if 'sessionid' in self.session_data:
            cookies['sessionid'] = self.session_data['sessionid']
        
        # เพิ่ม cookies ที่จำเป็นอื่น ๆ ถ้ามี
        for key in ['ds_user_id', 'csrftoken', 'mid', 'rur']:
            if key in self.session_data:
                cookies[key] = self.session_data[key]
        
        # มีแค่ sessionid ให้เพิ่ม basic cookies
        if len(cookies) == 1 and 'sessionid' in cookies:
            # Extract user_id จาก sessionid ถ้าเป็นไปได้
            cookies['mid'] = 'Y-kNmQALAAFl6YK9ZTaRyOVt5_1q'  # dummy mid
            
        return cookies
    
    def get_csrf_token(self):
        """ดึง CSRF token จาก Instagram"""
        print("🔑 Getting CSRF token...")
        
        try:
            response = requests.get(
                'https://www.instagram.com/',
                headers=self.create_headers(),
                cookies=self.create_cookies(),
                timeout=15
            )
            
            # หา CSRF token ใน response
            if 'csrf_token' in response.text:
                import re
                csrf_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
                if csrf_match:
                    csrf_token = csrf_match.group(1)
                    print(f"✅ CSRF token found: {csrf_token[:20]}...")
                    return csrf_token
            
            print("❌ CSRF token not found in response")
            return None
            
        except Exception as e:
            print(f"❌ CSRF token error: {e}")
            return None
    
    def test_profile_api(self, username, csrf_token=None):
        """ทดสอบ profile API"""
        print(f"📱 Testing profile API for: {username}")
        
        url = self.endpoints['profile'].format(username)
        
        try:
            response = requests.get(
                url,
                headers=self.create_headers(csrf_token),
                cookies=self.create_cookies(),
                timeout=15,
                allow_redirects=False  # ไม่ให้ redirect
            )
            
            print(f"📊 Response code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'data' in data and 'user' in data['data']:
                        user_data = data['data']['user']
                        print(f"✅ Profile found: {user_data.get('username', 'unknown')}")
                        print(f"👥 Followers: {user_data.get('edge_followed_by', {}).get('count', 0)}")
                        print(f"👤 Following: {user_data.get('edge_follow', {}).get('count', 0)}")
                        print(f"📷 Posts: {user_data.get('edge_owner_to_timeline_media', {}).get('count', 0)}")
                        return data
                    else:
                        print("❌ No user data in response")
                except json.JSONDecodeError:
                    print("❌ Invalid JSON response")
            elif response.status_code == 302:
                print("🔄 Redirected - possibly need login")
            elif response.status_code == 401:
                print("🔐 Unauthorized - session expired")
            elif response.status_code == 429:
                print("⏰ Rate limited - wait before retry")
            else:
                print(f"❌ Unexpected response: {response.status_code}")
            
        except Exception as e:
            print(f"❌ API test error: {e}")
        
        return None
    
    def test_search_api(self, query):
        """ทดสอบ search API"""
        print(f"🔍 Testing search API for: {query}")
        
        url = self.endpoints['search'].format(query)
        
        try:
            response = requests.get(
                url,
                headers=self.create_headers(),
                cookies=self.create_cookies(),
                timeout=15
            )
            
            print(f"📊 Search response: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                users = data.get('users', [])
                print(f"👥 Found {len(users)} users")
                
                for user in users[:3]:  # แสดง 3 คนแรก
                    username = user.get('user', {}).get('username', 'unknown')
                    full_name = user.get('user', {}).get('full_name', '')
                    print(f"  • {username} ({full_name})")
                
                return data
            else:
                print(f"❌ Search failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Search error: {e}")
        
        return None
    
    def run_tests(self):
        """รันการทดสอบทั้งหมด"""
        print("🔥 SIMPLE INSTAGRAM API TESTER")
        print("=" * 50)
        
        # Test 1: Get CSRF token
        csrf_token = self.get_csrf_token()
        
        # Test 2: Test profiles
        target_accounts = ['alx.trading', 'whatilove1728']
        
        for account in target_accounts:
            print(f"\n📱 Testing: {account}")
            self.test_profile_api(account, csrf_token)
            time.sleep(random.uniform(2, 4))  # พัก random 2-4 วินาที
        
        # Test 3: Search API
        print(f"\n🔍 Testing search...")
        self.test_search_api('alx')
        
        print("\n✅ Testing completed!")

if __name__ == "__main__":
    tester = SimpleInstagramTester()
    tester.run_tests()
