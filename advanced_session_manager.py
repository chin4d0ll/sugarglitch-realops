#!/usr/bin/env python3
"""
🔥 ADVANCED SESSION MANAGER 🔥
ระบบจัดการ session สำหรับ Instagram extraction
- Session Reuse: ใช้ session เดิมที่ยังใช้งานได้
- Session Refresh: รีเฟรช session เมื่อหมดอายุ
- Session Storage: เก็บ session แบบปลอดภัย
"""

import json
import os
import pickle
import time
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Any
import hashlib
import requests
from cryptography.fernet import Fernet
import keyring
from fake_useragent import UserAgent


class AdvancedSessionManager:
    def __init__(self, username: str = "whatilove1728"):
        self.username = username
        self.session_dir = "/workspaces/sugarglitch-realops/sessions"
        self.session_file = f"{self.session_dir}/{username}_session.json"
        self.encrypted_session_file = f"{self.session_dir}/{username}_session.enc"
        self.session_backup_dir = f"{self.session_dir}/backups"
        
        # สร้างโฟลเดอร์
        Path(self.session_dir).mkdir(exist_ok=True)
        Path(self.session_backup_dir).mkdir(exist_ok=True)
        
        # Session data
        self.current_session = None
        self.session_metadata = {}
        
        # User Agent
        self.ua = UserAgent()
        
        # ตั้งค่า encryption key
        self.setup_encryption()
        
        print(f"🔧 Session Manager initialized for: {username}")
    
    def setup_encryption(self):
        """ตั้งค่า encryption key สำหรับเก็บ session ปลอดภัย"""
        try:
            # ลองโหลด key จาก keyring
            key = keyring.get_password("instagram_session", "encryption_key")
            if not key:
                # สร้าง key ใหม่
                key = Fernet.generate_key().decode()
                keyring.set_password("instagram_session", "encryption_key", key)
                print("🔐 Generated new encryption key")
            
            self.encryption_key = key.encode()
            self.cipher = Fernet(self.encryption_key)
            print("✅ Encryption setup complete")
            
        except Exception as e:
            print(f"⚠️ Encryption setup failed: {e}")
            print("📋 Sessions will be stored unencrypted")
            self.encryption_key = None
            self.cipher = None
    
    def save_session(self, session_data: Dict, metadata: Dict = None) -> bool:
        """บันทึก session แบบปลอดภัย"""
        try:
            # เพิ่ม metadata
            if metadata is None:
                metadata = {}
            
            metadata.update({
                'saved_at': datetime.now().isoformat(),
                'username': self.username,
                'user_agent': self.ua.random,
                'expires_estimate': (datetime.now() + timedelta(days=30)).isoformat()
            })
            
            session_package = {
                'session_data': session_data,
                'metadata': metadata
            }
            
            # บันทึกแบบ encrypted
            if self.cipher:
                try:
                    encrypted_data = self.cipher.encrypt(json.dumps(session_package).encode())
                    with open(self.encrypted_session_file, 'wb') as f:
                        f.write(encrypted_data)
                    print(f"🔐 Session saved (encrypted): {self.encrypted_session_file}")
                except Exception as e:
                    print(f"⚠️ Encryption failed: {e}")
                    # Fallback to unencrypted
                    with open(self.session_file, 'w') as f:
                        json.dump(session_package, f, indent=2)
                    print(f"💾 Session saved (unencrypted): {self.session_file}")
            else:
                # บันทึกแบบ unencrypted
                with open(self.session_file, 'w') as f:
                    json.dump(session_package, f, indent=2)
                print(f"💾 Session saved: {self.session_file}")
            
            # สร้าง backup
            self.create_session_backup(session_package)
            
            self.current_session = session_data
            self.session_metadata = metadata
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to save session: {e}")
            return False
    
    def load_session(self) -> Optional[Dict]:
        """โหลด session จากไฟล์"""
        session_package = None
        
        # ลอง load encrypted file ก่อน
        if os.path.exists(self.encrypted_session_file) and self.cipher:
            try:
                with open(self.encrypted_session_file, 'rb') as f:
                    encrypted_data = f.read()
                
                decrypted_data = self.cipher.decrypt(encrypted_data)
                session_package = json.loads(decrypted_data.decode())
                print(f"🔓 Loaded encrypted session: {self.encrypted_session_file}")
                
            except Exception as e:
                print(f"⚠️ Failed to decrypt session: {e}")
        
        # ถ้าไม่มี encrypted หรือ decrypt ไม่ได้ ลอง unencrypted
        if not session_package and os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r') as f:
                    session_package = json.load(f)
                print(f"📂 Loaded unencrypted session: {self.session_file}")
            except Exception as e:
                print(f"❌ Failed to load session: {e}")
                return None
        
        if session_package:
            self.current_session = session_package.get('session_data')
            self.session_metadata = session_package.get('metadata', {})
            
            # ตรวจสอบความใหม่ของ session
            self.check_session_validity()
            
            return self.current_session
        
        return None
    
    def check_session_validity(self) -> bool:
        """ตรวจสอบว่า session ยังใช้งานได้หรือไม่"""
        if not self.current_session or not self.session_metadata:
            print("❌ No session data to check")
            return False
        
        # ตรวจสอบอายุของ session
        saved_at = self.session_metadata.get('saved_at')
        if saved_at:
            try:
                saved_time = datetime.fromisoformat(saved_at)
                age = datetime.now() - saved_time
                
                print(f"📅 Session age: {age.days} days, {age.seconds//3600} hours")
                
                # ถือว่า session หมดอายุหลัง 7 วัน
                if age.days > 7:
                    print("⚠️ Session may be expired (> 7 days old)")
                    return False
                elif age.days > 3:
                    print("⚠️ Session is getting old (> 3 days), consider refreshing")
                else:
                    print("✅ Session is fresh")
                
            except Exception as e:
                print(f"❌ Error checking session age: {e}")
        
        return True
    
    def test_session_validity(self) -> bool:
        """ทดสอบ session กับ Instagram จริง"""
        if not self.current_session:
            print("❌ No session to test")
            return False
        
        print("🧪 Testing session validity with Instagram...")
        
        try:
            session = requests.Session()
            
            # ตั้งค่า headers
            headers = {
                'User-Agent': self.session_metadata.get('user_agent', self.ua.random),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            session.headers.update(headers)
            
            # ตั้งค่า cookies
            if 'cookies' in self.current_session:
                for cookie in self.current_session['cookies']:
                    if isinstance(cookie, dict) and 'name' in cookie and 'value' in cookie:
                        session.cookies.set(cookie['name'], cookie['value'])
            
            # ทดสอบเข้าถึง profile
            test_url = f"https://www.instagram.com/{self.username}/"
            response = session.get(test_url, timeout=15, allow_redirects=False)
            
            print(f"📊 Test result: Status {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Session is valid - direct access successful")
                return True
            elif response.status_code in [301, 302]:
                redirect_url = response.headers.get('Location', '')
                if 'login' in redirect_url:
                    print("❌ Session expired - redirected to login")
                    return False
                else:
                    print("🔄 Redirected but not to login - session may be valid")
                    return True
            else:
                print(f"⚠️ Unexpected status code: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Session test failed: {e}")
            return False
    
    def refresh_session(self) -> bool:
        """รีเฟรช session (placeholder - ต้องใช้ browser automation)"""
        print("🔄 Session refresh functionality")
        print("⚠️ This requires browser automation to login again")
        print("💡 Recommendations:")
        print("   1. Use Selenium/Playwright to automate login")
        print("   2. Manually login and export cookies")
        print("   3. Use Instagram API for authorized access")
        
        return False
    
    def create_session_backup(self, session_package: Dict):
        """สร้าง backup ของ session"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{self.session_backup_dir}/{self.username}_backup_{timestamp}.json"
            
            with open(backup_file, 'w') as f:
                json.dump(session_package, f, indent=2)
            
            print(f"💾 Session backup created: {backup_file}")
            
            # ลบ backup เก่าที่เกิน 10 ไฟล์
            self.cleanup_old_backups()
            
        except Exception as e:
            print(f"⚠️ Backup creation failed: {e}")
    
    def cleanup_old_backups(self, keep_count: int = 10):
        """ลบ backup เก่า"""
        try:
            backup_files = []
            for file in os.listdir(self.session_backup_dir):
                if file.startswith(f"{self.username}_backup_") and file.endswith('.json'):
                    file_path = os.path.join(self.session_backup_dir, file)
                    backup_files.append((file_path, os.path.getctime(file_path)))
            
            # เรียงตามวันที่
            backup_files.sort(key=lambda x: x[1], reverse=True)
            
            # ลบไฟล์เก่า
            for file_path, _ in backup_files[keep_count:]:
                os.remove(file_path)
                print(f"🗑️ Removed old backup: {os.path.basename(file_path)}")
                
        except Exception as e:
            print(f"⚠️ Backup cleanup failed: {e}")
    
    def import_session_from_file(self, file_path: str) -> bool:
        """นำเข้า session จากไฟล์อื่น"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # ตรวจสอบรูปแบบข้อมูล
            if 'cookies' in data or 'session_data' in data:
                session_data = data.get('session_data', data)
                metadata = {
                    'imported_from': file_path,
                    'imported_at': datetime.now().isoformat()
                }
                
                return self.save_session(session_data, metadata)
            else:
                print("❌ Invalid session file format")
                return False
                
        except Exception as e:
            print(f"❌ Failed to import session: {e}")
            return False
    
    def list_available_sessions(self):
        """แสดงรายการ session ที่มีอยู่"""
        print("📋 AVAILABLE SESSIONS:")
        print("=" * 30)
        
        # Current session
        if os.path.exists(self.session_file) or os.path.exists(self.encrypted_session_file):
            if self.session_metadata:
                saved_at = self.session_metadata.get('saved_at', 'Unknown')
                print(f"📄 Current session: {saved_at}")
            else:
                print(f"📄 Current session: Available")
        
        # Backups
        if os.path.exists(self.session_backup_dir):
            backups = [f for f in os.listdir(self.session_backup_dir) 
                      if f.startswith(f"{self.username}_backup_")]
            
            if backups:
                print(f"💾 Backups: {len(backups)} files")
                for backup in sorted(backups, reverse=True)[:5]:  # Show latest 5
                    print(f"   - {backup}")
            else:
                print("💾 No backups found")
        
        # Sessions from extracted_project
        session_sources = [
            "/workspaces/sugarglitch-realops/extracted_project/Python/success_whatilove1728_20250525_153247.json",
            "/workspaces/sugarglitch-realops/extracted_project/Python/PRIVATE_BYPASS_SUCCESS_whatilove1728_20250525_234142.json"
        ]
        
        print("🔍 Source sessions:")
        for source in session_sources:
            if os.path.exists(source):
                print(f"   ✅ {os.path.basename(source)}")
            else:
                print(f"   ❌ {os.path.basename(source)}")
    
    def get_session_for_requests(self) -> requests.Session:
        """สร้าง requests.Session ที่พร้อมใช้งาน"""
        session = requests.Session()
        
        if not self.current_session:
            print("⚠️ No session data available")
            return session
        
        # ตั้งค่า headers
        headers = {
            'User-Agent': self.session_metadata.get('user_agent', self.ua.random),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.instagram.com/'
        }
        
        session.headers.update(headers)
        
        # ตั้งค่า cookies
        if 'cookies' in self.current_session:
            for cookie in self.current_session['cookies']:
                if isinstance(cookie, dict) and 'name' in cookie and 'value' in cookie:
                    session.cookies.set(cookie['name'], cookie['value'], 
                                      domain=cookie.get('domain', '.instagram.com'))
        
        print("✅ Session configured for requests")
        return session


def main():
    print("🔥💀 ADVANCED SESSION MANAGER 💀🔥")
    print("=" * 50)
    
    # สร้าง Session Manager
    manager = AdvancedSessionManager("whatilove1728")
    
    # แสดงรายการ session ที่มี
    manager.list_available_sessions()
    
    print("\n🔄 Loading existing session...")
    session = manager.load_session()
    
    if session:
        print("✅ Session loaded successfully")
        
        # ทดสอบความใช้งานได้
        print("\n🧪 Testing session validity...")
        is_valid = manager.test_session_validity()
        
        if is_valid:
            print("🎉 Session is working!")
        else:
            print("❌ Session needs refresh")
            print("💡 Try importing a fresh session or use browser automation")
    else:
        print("❌ No session found")
        print("💡 Try importing a session from extracted_project")
        
        # ลองนำเข้า session จากไฟล์ที่มี
        source_files = [
            "/workspaces/sugarglitch-realops/extracted_project/Python/success_whatilove1728_20250525_153247.json"
        ]
        
        for source in source_files:
            if os.path.exists(source):
                print(f"\n📥 Importing session from: {os.path.basename(source)}")
                if manager.import_session_from_file(source):
                    print("✅ Session imported successfully")
                    break


if __name__ == "__main__":
    main()
