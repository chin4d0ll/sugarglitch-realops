#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 SESSION REFRESHER - แก้ปัญหา session หมดอายุทันที
Dream's Instagram Session Recovery System
"""

import json
import requests
import time
from datetime import datetime

class SessionRefresher:
    def __init__(self):
        self.username = "alx.trading"
        self.password = "Fleming654"
        self.session = requests.Session()
        
    def check_current_session(self):
        """🔍 ตรวจสอบ session ปัจจุบัน"""
        print("🔍 ตรวจสอบ session ปัจจุบัน...")
        
        try:
            with open('session.json', 'r') as f:
                session_data = json.load(f)
            
            sessionid = session_data.get('sessionid', '')
            ds_user_id = session_data.get('ds_user_id', '')
            
            print(f"📄 Session ID: {sessionid[:20]}...")
            print(f"👤 User ID: {ds_user_id}")
            
            # ทดสอบ session
            self.session.cookies.set('sessionid', sessionid, domain='.instagram.com')
            self.session.cookies.set('ds_user_id', ds_user_id, domain='.instagram.com')
            
            # ลองเข้า profile
            response = self.session.get('https://www.instagram.com/alx.trading/')
            
            if response.status_code == 200 and 'login' not in response.url:
                print("✅ Session ยังใช้ได้!")
                return True
            else:
                print("❌ Session หมดอายุแล้ว!")
                return False
                
        except Exception as e:
            print(f"❌ ตรวจสอบ session error: {e}")
            return False
    
    def get_fresh_session(self):
        """🔄 ดึง session ใหม่"""
        print("🔄 กำลังดึง session ใหม่...")
        
        try:
            # ไปหน้า login
            response = self.session.get('https://www.instagram.com/accounts/login/')
            
            # หา CSRF token
            csrf_token = None
            for cookie in self.session.cookies:
                if cookie.name == 'csrftoken':
                    csrf_token = cookie.value
                    break
            
            if not csrf_token:
                print("❌ ไม่เจอ CSRF token")
                return False
            
            # Headers สำหรับ login
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'X-CSRFToken': csrf_token,
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/accounts/login/',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            
            # Login data
            login_data = {
                'username': self.username,
                'password': self.password,
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }
            
            # ส่ง login request
            login_response = self.session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=headers
            )
            
            print(f"📡 Login response: {login_response.status_code}")
            
            if login_response.status_code == 200:
                try:
                    result = login_response.json()
                    
                    if result.get('authenticated'):
                        print("✅ Login สำเร็จ!")
                        
                        # ดึง session data ใหม่
                        new_session = {}
                        for cookie in self.session.cookies:
                            if cookie.name == 'sessionid':
                                new_session['sessionid'] = cookie.value
                            elif cookie.name == 'ds_user_id':
                                new_session['ds_user_id'] = cookie.value
                        
                        # บันทึก session ใหม่
                        with open('session.json', 'w') as f:
                            json.dump(new_session, f, indent=2)
                        
                        print(f"💾 Session ใหม่บันทึกแล้ว: {new_session['sessionid'][:20]}...")
                        return True
                    else:
                        print(f"❌ Login ไม่สำเร็จ: {result}")
                        return False
                        
                except json.JSONDecodeError:
                    print(f"❌ Response ไม่ใช่ JSON: {login_response.text[:200]}")
                    return False
            else:
                print(f"❌ Login HTTP error: {login_response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Fresh session error: {e}")
            return False
    
    def test_new_session(self):
        """🧪 ทดสอบ session ใหม่"""
        print("🧪 ทดสอบ session ใหม่...")
        
        try:
            # ลองเข้า DM
            dm_response = self.session.get('https://www.instagram.com/direct/inbox/')
            
            if dm_response.status_code == 200 and 'direct' in dm_response.text:
                print("✅ Session ใหม่ใช้ได้! เข้า DM ได้")
                return True
            else:
                print("❌ Session ใหม่ยังไม่ work")
                return False
                
        except Exception as e:
            print(f"❌ ทดสอบ session error: {e}")
            return False

def main():
    print("🔄 INSTAGRAM SESSION REFRESHER")
    print("=" * 50)
    print("👤 Account: alx.trading")
    print("🔑 Password: Fleming654")
    print()
    
    refresher = SessionRefresher()
    
    # Step 1: ตรวจ session ปัจจุบัน
    if refresher.check_current_session():
        print("✅ Session ยังใช้ได้ ไม่ต้องแก้!")
        return
    
    # Step 2: ดึง session ใหม่
    print("\n🔄 Session หมดอายุ กำลังดึงใหม่...")
    if refresher.get_fresh_session():
        # Step 3: ทดสอบ session ใหม่
        if refresher.test_new_session():
            print("\n🎉 SESSION REFRESH สำเร็จ!")
            print("✅ พร้อมใช้งาน script อื่น ๆ ได้แล้ว")
        else:
            print("\n⚠️ Session ใหม่ยังมีปัญหา")
    else:
        print("\n❌ ไม่สามารถดึง session ใหม่ได้")
        print("💡 อาจต้องใช้วิธีอื่น หรือรอสักครู่")

if __name__ == "__main__":
    main()
