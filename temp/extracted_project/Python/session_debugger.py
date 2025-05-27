#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 INSTAGRAM SESSION DEBUGGER
แก้ปัญหา session โดยตรง + ทดสอบทุกวิธี
"""

import json
import requests
import time
from datetime import datetime
from instagrapi import Client

def test_current_session():
    """🔍 ทดสอบ session ปัจจุบันด้วยหลายวิธี"""
    print("🔍 ทดสอบ session ปัจจุบัน...")
    
    try:
        with open('session.json', 'r') as f:
            session_data = json.load(f)
        
        sessionid = session_data.get('sessionid', '')
        ds_user_id = session_data.get('ds_user_id', '')
        
        print(f"📄 Session ID: {sessionid}")
        print(f"👤 User ID: {ds_user_id}")
        
        # Method 1: ทดสอบด้วย requests
        print("\n🧪 Method 1: ทดสอบด้วย requests...")
        session = requests.Session()
        session.cookies.set('sessionid', sessionid, domain='.instagram.com')
        session.cookies.set('ds_user_id', ds_user_id, domain='.instagram.com')
        
        response = session.get('https://www.instagram.com/alx.trading/')
        print(f"   Status: {response.status_code}")
        print(f"   URL: {response.url}")
        print(f"   Contains login: {'login' in response.url}")
        
        if response.status_code == 200 and 'login' not in response.url:
            print("✅ Method 1: Session ใช้ได้!")
            return True, session_data
        else:
            print("❌ Method 1: Session หมดอายุ")
        
        # Method 2: ทดสอบด้วย instagrapi
        print("\n🧪 Method 2: ทดสอบด้วย instagrapi...")
        try:
            cl = Client()
            cl.login_by_sessionid(sessionid)
            account_info = cl.account_info()
            print(f"✅ Method 2: instagrapi ใช้ได้! Username: {account_info.username}")
            return True, session_data
        except Exception as e:
            print(f"❌ Method 2: instagrapi error: {e}")
        
        return False, None
        
    except Exception as e:
        print(f"❌ ทดสอบ session error: {e}")
        return False, None

def login_fresh_session():
    """🔄 Login ใหม่เพื่อได้ session ใหม่"""
    print("🔄 กำลัง login ใหม่...")
    
    try:
        # Method 1: ใช้ instagrapi login
        print("🧪 ลอง login ด้วย instagrapi...")
        cl = Client()
        
        # ลองใช้รหัสผ่านที่รู้
        success = cl.login("alx.trading", "Fleming654")
        
        if success:
            print("✅ instagrapi login สำเร็จ!")
            
            # ดึง session data
            session_data = cl.get_settings()
            
            # บันทึกแค่ข้อมูลสำคัญ
            new_session = {
                'sessionid': session_data.get('session_id'),
                'ds_user_id': session_data.get('user_id'),
                'full_session': session_data  # เก็บข้อมูลเต็ม
            }
            
            # บันทึกไฟล์
            with open('session.json', 'w') as f:
                json.dump(new_session, f, indent=2)
            
            print(f"💾 Session ใหม่บันทึกแล้ว!")
            return True, new_session
        else:
            print("❌ instagrapi login ล้มเหลว")
            
    except Exception as e:
        print(f"❌ instagrapi login error: {e}")
    
    # Method 2: ใช้ requests login
    print("\n🧪 ลอง login ด้วย requests...")
    try:
        session = requests.Session()
        
        # ไปหน้า login
        response = session.get('https://www.instagram.com/accounts/login/')
        
        # หา CSRF
        csrf_token = None
        for cookie in session.cookies:
            if cookie.name == 'csrftoken':
                csrf_token = cookie.value
                break
        
        if csrf_token:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'X-CSRFToken': csrf_token,
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/accounts/login/',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            
            login_data = {
                'username': 'alx.trading',
                'password': 'Fleming654',
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }
            
            login_response = session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=headers
            )
            
            print(f"   Login status: {login_response.status_code}")
            
            if login_response.status_code == 200:
                result = login_response.json()
                if result.get('authenticated'):
                    print("✅ requests login สำเร็จ!")
                    
                    # ดึง cookies
                    new_session = {}
                    for cookie in session.cookies:
                        if cookie.name == 'sessionid':
                            new_session['sessionid'] = cookie.value
                        elif cookie.name == 'ds_user_id':
                            new_session['ds_user_id'] = cookie.value
                    
                    with open('session.json', 'w') as f:
                        json.dump(new_session, f, indent=2)
                    
                    print(f"💾 Session จาก requests บันทึกแล้ว!")
                    return True, new_session
                else:
                    print(f"❌ requests login ไม่สำเร็จ: {result}")
            else:
                print(f"❌ requests login HTTP error: {login_response.status_code}")
        else:
            print("❌ ไม่เจอ CSRF token")
            
    except Exception as e:
        print(f"❌ requests login error: {e}")
    
    return False, None

def test_session_with_dm():
    """🧪 ทดสอบ session ด้วยการเข้า DM"""
    print("🧪 ทดสอบ session ด้วยการเข้า DM...")
    
    try:
        with open('session.json', 'r') as f:
            session_data = json.load(f)
        
        # ทดสอบด้วย requests
        session = requests.Session()
        session.cookies.set('sessionid', session_data['sessionid'], domain='.instagram.com')
        session.cookies.set('ds_user_id', session_data['ds_user_id'], domain='.instagram.com')
        
        # ลองเข้า DM
        dm_response = session.get('https://www.instagram.com/direct/inbox/')
        print(f"   DM page status: {dm_response.status_code}")
        
        if dm_response.status_code == 200 and 'direct' in dm_response.text:
            print("✅ เข้า DM ได้! Session ใช้งานได้")
            return True
        else:
            print("❌ เข้า DM ไม่ได้")
            return False
            
    except Exception as e:
        print(f"❌ ทดสอบ DM error: {e}")
        return False

def main():
    print("🔧 INSTAGRAM SESSION DEBUGGER")
    print("=" * 50)
    print("👤 Account: alx.trading")
    print("📅 " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print()
    
    # Step 1: ทดสอบ session ปัจจุบัน
    is_valid, current_session = test_current_session()
    
    if is_valid:
        print("\n✅ Session ยังใช้ได้!")
        if test_session_with_dm():
            print("🎉 Session พร้อมใช้งาน!")
            return
    
    # Step 2: ถ้า session หมดอายุ ให้ login ใหม่
    print("\n🔄 Session หมดอายุ กำลัง login ใหม่...")
    login_success, new_session = login_fresh_session()
    
    if login_success:
        print("\n🎉 LOGIN สำเร็จ!")
        if test_session_with_dm():
            print("✅ Session ใหม่พร้อมใช้งาน!")
        else:
            print("⚠️ Session ใหม่ยังมีปัญหา")
    else:
        print("\n❌ ไม่สามารถ login ได้")
        print("💡 ปัญหาที่เป็นไปได้:")
        print("   - รหัสผ่าน Fleming654 ไม่ถูกต้อง")
        print("   - Account ถูก lock/suspend")
        print("   - Instagram block IP")
        print("   - Need 2FA verification")

if __name__ == "__main__":
    main()
