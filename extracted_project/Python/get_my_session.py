#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🍪 Instagram Session ID Hunter - สำหรับบัญชีของคุณเอง
เครื่องมือช่วยหา Session ID จากข้อมูลส่วนตัวของคุณ
"""

import os
import json
import sqlite3
import base64
from pathlib import Path
import platform
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class MySessionHunter:
    def __init__(self):
        self.system = platform.system()
        self.found_sessions = []
        
    def get_chrome_cookie_paths(self):
        """หา path ของ Chrome cookies ตาม OS"""
        paths = []
        
        if self.system == "Windows":
            # Windows paths
            base_paths = [
                os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data"),
                os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default"),
                os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default"),
            ]
        elif self.system == "Darwin":  # macOS
            base_paths = [
                os.path.expanduser("~/Library/Application Support/Google/Chrome/Default"),
                os.path.expanduser("~/Library/Application Support/Google/Chrome/Profile 1"),
                os.path.expanduser("~/Library/Application Support/Microsoft Edge/Default"),
            ]
        else:  # Linux
            base_paths = [
                os.path.expanduser("~/.config/google-chrome/Default"),
                os.path.expanduser("~/.config/google-chrome/Profile 1"),
                os.path.expanduser("~/.config/chromium/Default"),
                os.path.expanduser("~/.config/microsoft-edge/Default"),
            ]
        
        for base_path in base_paths:
            cookie_path = os.path.join(base_path, "Cookies")
            if os.path.exists(cookie_path):
                paths.append(cookie_path)
                
        return paths
    
    def get_firefox_cookie_paths(self):
        """หา path ของ Firefox cookies"""
        paths = []
        
        if self.system == "Windows":
            base_path = os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles")
        elif self.system == "Darwin":
            base_path = os.path.expanduser("~/Library/Application Support/Firefox/Profiles")
        else:
            base_path = os.path.expanduser("~/.mozilla/firefox")
            
        if os.path.exists(base_path):
            for profile in os.listdir(base_path):
                profile_path = os.path.join(base_path, profile)
                if os.path.isdir(profile_path):
                    cookie_file = os.path.join(profile_path, "cookies.sqlite")
                    if os.path.exists(cookie_file):
                        paths.append(cookie_file)
                        
        return paths
    
    def search_chrome_cookies(self, cookie_path):
        """ค้นหา Instagram session ID ใน Chrome cookies"""
        try:
            # Copy cookie file เพื่อหลีกเลี่ยง lock
            import shutil
            temp_path = cookie_path + ".temp"
            shutil.copy2(cookie_path, temp_path)
            
            conn = sqlite3.connect(temp_path)
            cursor = conn.cursor()
            
            # Query Instagram cookies
            cursor.execute("""
                SELECT name, value, host_key, path, expires_utc 
                FROM cookies 
                WHERE host_key LIKE '%instagram.com%' 
                AND name = 'sessionid'
            """)
            
            results = cursor.fetchall()
            
            for result in results:
                name, value, host, path, expires = result
                if value and len(value) > 10:  # Session ID ต้องยาวกว่า 10 ตัวอักษร
                    session_info = {
                        'sessionid': value,
                        'host': host,
                        'path': path,
                        'expires': expires,
                        'source': f'Chrome: {cookie_path}',
                        'browser': 'Chrome/Chromium'
                    }
                    self.found_sessions.append(session_info)
                    
            conn.close()
            os.remove(temp_path)
            
        except Exception as e:
            print(f"❌ Error reading Chrome cookies: {e}")
    
    def search_firefox_cookies(self, cookie_path):
        """ค้นหา Instagram session ID ใน Firefox cookies"""
        try:
            import shutil
            temp_path = cookie_path + ".temp"
            shutil.copy2(cookie_path, temp_path)
            
            conn = sqlite3.connect(temp_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name, value, host, path, expiry 
                FROM moz_cookies 
                WHERE host LIKE '%instagram.com%' 
                AND name = 'sessionid'
            """)
            
            results = cursor.fetchall()
            
            for result in results:
                name, value, host, path, expires = result
                if value and len(value) > 10:
                    session_info = {
                        'sessionid': value,
                        'host': host,
                        'path': path,
                        'expires': expires,
                        'source': f'Firefox: {cookie_path}',
                        'browser': 'Firefox'
                    }
                    self.found_sessions.append(session_info)
                    
            conn.close()
            os.remove(temp_path)
            
        except Exception as e:
            print(f"❌ Error reading Firefox cookies: {e}")
    
    def hunt_sessions(self):
        """หา Session ID จากทุก browser ที่ติดตั้ง"""
        print("🔍 กำลังค้นหา Instagram Session ID ของคุณ...")
        print("="*50)
        
        # ค้นหาใน Chrome/Chromium
        chrome_paths = self.get_chrome_cookie_paths()
        print(f"📁 พบ Chrome cookie files: {len(chrome_paths)} ไฟล์")
        
        for path in chrome_paths:
            print(f"🔍 กำลังตรวจสอบ: {path}")
            self.search_chrome_cookies(path)
        
        # ค้นหาใน Firefox
        firefox_paths = self.get_firefox_cookie_paths()
        print(f"📁 พบ Firefox cookie files: {len(firefox_paths)} ไฟล์")
        
        for path in firefox_paths:
            print(f"🔍 กำลังตรวจสอบ: {path}")
            self.search_firefox_cookies(path)
        
        return self.found_sessions
    
    def save_session_to_config(self, session_info):
        """บันทึก Session ID ลงไฟล์ config"""
        config_data = {
            "sessionid": session_info['sessionid'],
            "account_info": {
                "browser": session_info['browser'],
                "host": session_info['host'],
                "expires": session_info['expires'],
                "extracted_at": "2025-05-25",
                "source": session_info['source']
            }
        }
        
        # บันทึกลง session.json
        with open('session.json', 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
        
        print(f"✅ บันทึก Session ID ลง session.json แล้ว")
        return config_data

def main():
    print("🌸 SugarGlitch Session Hunter - หา Session ID ของคุณเอง")
    print("="*60)
    print("⚠️  เครื่องมือนี้จะค้นหา Session ID จากบัญชี Instagram ของคุณเอง")
    print("⚠️  ปิด browser ทั้งหมดก่อนเรียกใช้เพื่อหลีกเลี่ยง file lock")
    print()
    
    # ขอความยินยอม
    consent = input("🤔 ยืนยันว่าต้องการหา Session ID ของบัญชีตัวเอง? (y/n): ")
    if consent.lower() != 'y':
        print("❌ ยกเลิกการดำเนินการ")
        return
    
    hunter = MySessionHunter()
    sessions = hunter.hunt_sessions()
    
    print("\n" + "="*50)
    print("📊 ผลการค้นหา:")
    
    if not sessions:
        print("❌ ไม่พบ Instagram Session ID ในเครื่องของคุณ")
        print("\n💡 แนะนำ:")
        print("1. Login Instagram ใน browser ของคุณ")
        print("2. ปิด browser แล้วรันสคริปต์นี้อีกครั้ง")
        print("3. หรือใช้วิธีแยก Session ID ด้วยตนเอง")
        return
    
    print(f"✅ พบ {len(sessions)} Session ID")
    
    for i, session in enumerate(sessions, 1):
        print(f"\n📱 Session #{i}:")
        print(f"   Browser: {session['browser']}")
        print(f"   Host: {session['host']}")
        print(f"   Session ID: {session['sessionid'][:20]}...")
        print(f"   Source: {session['source']}")
    
    # เลือก session ที่จะใช้
    if len(sessions) == 1:
        selected = sessions[0]
        print(f"\n🎯 ใช้ Session ID เดียวที่พบ")
    else:
        try:
            choice = int(input(f"\n🎯 เลือก Session ID ที่จะใช้ (1-{len(sessions)}): ")) - 1
            selected = sessions[choice]
        except (ValueError, IndexError):
            print("❌ เลือกไม่ถูกต้อง ใช้ Session แรก")
            selected = sessions[0]
    
    # บันทึกลง config
    config = hunter.save_session_to_config(selected)
    
    print("\n🎉 สำเร็จ! Session ID ของคุณพร้อมใช้งาน")
    print(f"📁 ไฟล์: session.json")
    print(f"🔑 Session ID: {selected['sessionid'][:30]}...")
    
    # ทดสอบ session
    test = input("\n🧪 ต้องการทดสอบ Session ID นี้เลยไหม? (y/n): ")
    if test.lower() == 'y':
        print("🔄 กำลังทดสอบ Session ID...")
        os.system('python validate_session.py')

if __name__ == "__main__":
    main()
