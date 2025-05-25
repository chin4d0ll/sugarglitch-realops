#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔓 Instagram Account Recovery Helper
เครื่องมือช่วยกู้คืนข้อมูล Instagram จากเครื่องคุณ
สำหรับกรณีที่ลืม password หรือเข้าไม่ได้
"""

import os
import json
import sqlite3
import platform
from pathlib import Path
import base64
import shutil
from datetime import datetime

class InstagramRecoveryHelper:
    def __init__(self):
        self.system = platform.system()
        self.found_data = []
        self.recovery_options = []
        
    def search_browser_saved_passwords(self):
        """ค้นหา saved passwords ใน browser"""
        print("🔍 ค้นหา saved passwords ใน browser...")
        
        password_locations = self.get_password_storage_locations()
        
        for browser, path in password_locations.items():
            if os.path.exists(path):
                print(f"✅ พบ {browser} password storage: {path}")
                try:
                    self.extract_saved_passwords(browser, path)
                except Exception as e:
                    print(f"❌ ไม่สามารถอ่าน {browser} passwords: {e}")
    
    def get_password_storage_locations(self):
        """หาตำแหน่งที่เก็บ saved passwords"""
        locations = {}
        
        if self.system == "Windows":
            locations = {
                "Chrome": os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"),
                "Edge": os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Login Data"),
                "Firefox": os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles")
            }
        elif self.system == "Darwin":  # macOS
            locations = {
                "Chrome": os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/Login Data"),
                "Safari": os.path.expanduser("~/Library/Keychains"),
                "Firefox": os.path.expanduser("~/Library/Application Support/Firefox/Profiles")
            }
        else:  # Linux
            locations = {
                "Chrome": os.path.expanduser("~/.config/google-chrome/Default/Login Data"),
                "Chromium": os.path.expanduser("~/.config/chromium/Default/Login Data"),
                "Firefox": os.path.expanduser("~/.mozilla/firefox")
            }
        
        return locations
    
    def extract_saved_passwords(self, browser, path):
        """แยก saved passwords จาก browser"""
        if "Chrome" in browser or "Edge" in browser or "Chromium" in browser:
            self.extract_chrome_passwords(browser, path)
        elif "Firefox" in browser:
            self.extract_firefox_passwords(browser, path)
    
    def extract_chrome_passwords(self, browser, login_data_path):
        """แยก passwords จาก Chrome-based browsers"""
        try:
            # Copy file เพื่อหลีกเลี่ยง lock
            temp_path = login_data_path + ".temp"
            shutil.copy2(login_data_path, temp_path)
            
            conn = sqlite3.connect(temp_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT origin_url, username_value, password_value 
                FROM logins 
                WHERE origin_url LIKE '%instagram%'
            """)
            
            results = cursor.fetchall()
            
            for result in results:
                url, username, encrypted_password = result
                if username:
                    self.found_data.append({
                        'type': 'saved_login',
                        'browser': browser,
                        'url': url,
                        'username': username,
                        'password_encrypted': bool(encrypted_password),
                        'note': 'พบ saved login ใน browser'
                    })
            
            conn.close()
            os.remove(temp_path)
            
        except Exception as e:
            print(f"❌ Error extracting {browser} passwords: {e}")
    
    def search_session_cache_files(self):
        """ค้นหาไฟล์ cache ที่อาจมี session data"""
        print("🔍 ค้นหา session cache files...")
        
        cache_locations = [
            "~/.cache",
            "~/Library/Caches", 
            "~\\AppData\\Local\\Temp",
            "~\\AppData\\Roaming",
            "/tmp"
        ]
        
        for location in cache_locations:
            expanded_path = os.path.expanduser(location)
            if os.path.exists(expanded_path):
                self.search_instagram_cache(expanded_path)
    
    def search_instagram_cache(self, cache_dir):
        """ค้นหาไฟล์ cache ของ Instagram"""
        try:
            for root, dirs, files in os.walk(cache_dir):
                for file in files:
                    if any(keyword in file.lower() for keyword in ['instagram', 'session', 'login', 'cookie']):
                        file_path = os.path.join(root, file)
                        if os.path.getsize(file_path) < 10*1024*1024:  # < 10MB
                            self.analyze_cache_file(file_path)
        except Exception as e:
            print(f"❌ Error searching cache: {e}")
    
    def analyze_cache_file(self, file_path):
        """วิเคราะห์ไฟล์ cache หา session data"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read(1024)  # อ่านแค่ 1KB แรก
                
            # หา session patterns
            if b'sessionid' in content or b'instagram' in content:
                self.found_data.append({
                    'type': 'cache_file',
                    'path': file_path,
                    'size': os.path.getsize(file_path),
                    'note': 'พบไฟล์ cache ที่อาจมี session data'
                })
        except:
            pass
    
    def search_local_backup_files(self):
        """ค้นหาไฟล์ backup ในเครื่อง"""
        print("🔍 ค้นหาไฟล์ backup...")
        
        backup_patterns = [
            "*.json",
            "*.txt", 
            "*.log",
            "*.bak",
            "*session*",
            "*instagram*",
            "*cookie*"
        ]
        
        search_locations = [
            "~/Desktop",
            "~/Documents", 
            "~/Downloads",
            os.getcwd()
        ]
        
        for location in search_locations:
            expanded_path = os.path.expanduser(location)
            if os.path.exists(expanded_path):
                self.search_backup_in_directory(expanded_path)
    
    def search_backup_in_directory(self, directory):
        """ค้นหาไฟล์ backup ในไดเรกทอรี"""
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if any(keyword in file.lower() for keyword in ['session', 'instagram', 'cookie', 'login']):
                        file_path = os.path.join(root, file)
                        if file.endswith(('.json', '.txt', '.log')):
                            self.analyze_backup_file(file_path)
        except Exception as e:
            print(f"❌ Error searching backup: {e}")
    
    def analyze_backup_file(self, file_path):
        """วิเคราะห์ไฟล์ backup"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(1024)
                
            if 'sessionid' in content.lower() or 'instagram' in content.lower():
                self.found_data.append({
                    'type': 'backup_file',
                    'path': file_path,
                    'note': 'พบไฟล์ backup ที่อาจมีข้อมูล Instagram'
                })
        except:
            pass
    
    def generate_recovery_options(self):
        """สร้างตัวเลือกการกู้คืน"""
        print("\n🛠️ วิเคราะห์ตัวเลือกการกู้คืน...")
        
        if not self.found_data:
            self.recovery_options = [
                {
                    'method': 'create_new_account',
                    'title': 'สร้างบัญชีใหม่',
                    'description': 'สร้างบัญชี Instagram ใหม่สำหรับการทดสอบ',
                    'difficulty': 'ง่าย',
                    'time': '5 นาที'
                },
                {
                    'method': 'instagram_recovery',
                    'title': 'กู้คืนผ่าน Instagram',
                    'description': 'ใช้ email/phone กู้คืน password',
                    'difficulty': 'ปานกลาง',
                    'time': '10-30 นาที'
                }
            ]
        else:
            self.recovery_options = [
                {
                    'method': 'use_found_data',
                    'title': 'ใช้ข้อมูลที่พบ',
                    'description': f'พบข้อมูล {len(self.found_data)} รายการในเครื่อง',
                    'difficulty': 'ง่าย',
                    'time': '2 นาที'
                },
                {
                    'method': 'create_new_account',
                    'title': 'สร้างบัญชีใหม่',
                    'description': 'สร้างบัญชีทดสอบใหม่',
                    'difficulty': 'ง่าย',
                    'time': '5 นาที'
                }
            ]
    
    def show_recovery_guide(self):
        """แสดงคู่มือการกู้คืน"""
        print("\n" + "="*60)
        print("🔓 Instagram Account Recovery Guide")
        print("="*60)
        
        if self.found_data:
            print(f"\n✅ พบข้อมูล {len(self.found_data)} รายการในเครื่องคุณ:")
            for i, data in enumerate(self.found_data, 1):
                print(f"\n📄 ข้อมูลที่ {i}:")
                print(f"   ประเภท: {data['type']}")
                if 'username' in data:
                    print(f"   Username: {data['username']}")
                if 'path' in data:
                    print(f"   ไฟล์: {data['path']}")
                print(f"   หมายเหตุ: {data['note']}")
        
        print(f"\n🛠️ ตัวเลือกการกู้คืน ({len(self.recovery_options)} วิธี):")
        for i, option in enumerate(self.recovery_options, 1):
            print(f"\n{i}️⃣  {option['title']}")
            print(f"    📝 {option['description']}")
            print(f"    🎯 ความยาก: {option['difficulty']}")
            print(f"    ⏱️  เวลา: {option['time']}")
    
    def create_demo_session(self):
        """สร้าง demo session สำหรับการทดสอบ"""
        demo_session = {
            "sessionid": "demo_session_for_testing_only_not_real",
            "account_info": {
                "type": "demo_account",
                "created_at": datetime.now().isoformat(),
                "note": "Demo session สำหรับทดสอบระบบ - ไม่ใช่ข้อมูลจริง",
                "recovery_status": "no_password_access"
            }
        }
        
        with open('session.json', 'w', encoding='utf-8') as f:
            json.dump(demo_session, f, indent=4, ensure_ascii=False)
        
        print("✅ สร้าง demo session สำหรับทดสอบระบบแล้ว")
        return demo_session

def main():
    print("🔓 Instagram Account Recovery Helper")
    print("="*50)
    print("💡 เครื่องมือนี้จะช่วยคุณกู้คืนข้อมูล Instagram")
    print("   เมื่อไม่สามารถเข้าถึงบัญชีได้")
    print()
    
    helper = InstagramRecoveryHelper()
    
    # ค้นหาข้อมูลในเครื่อง
    helper.search_browser_saved_passwords()
    helper.search_session_cache_files()
    helper.search_local_backup_files()
    
    # สร้างตัวเลือกการกู้คืน
    helper.generate_recovery_options()
    
    # แสดงผลการค้นหา
    helper.show_recovery_guide()
    
    print("\n" + "🔑"*20)
    choice = input("🤔 เลือกวิธีการ (1-2): ").strip()
    
    if choice == "1" and helper.found_data:
        print("🔄 กำลังประมวลผลข้อมูลที่พบ...")
        # วิเคราะห์ข้อมูลที่พบ
        for data in helper.found_data:
            print(f"📄 วิเคราะห์: {data['note']}")
    
    # สร้าง demo session สำหรับการทดสอบ
    print("\n💡 สร้าง demo session สำหรับทดสอบระบบ...")
    helper.create_demo_session()
    
    print("\n🎯 ตัวเลือกต่อไป:")
    print("1. 🆕 สร้างบัญชี Instagram ใหม่")
    print("2. 📱 กู้คืนผ่าน email/phone")
    print("3. 🧪 ทดสอบระบบด้วย demo session")
    
    next_choice = input("\n🚀 เลือกการดำเนินการต่อไป (1-3): ").strip()
    
    if next_choice == "3":
        print("🔄 กำลังทดสอบระบบ...")
        os.system('python validate_session.py')

if __name__ == "__main__":
    main()
