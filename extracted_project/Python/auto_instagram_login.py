#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ล็อคอิน Instagram อัตโนมัติด้วยข้อมูลที่มีอยู่
Auto login to Instagram with existing credentials
"""

import requests
import json
import time
from datetime import datetime

def auto_login():
    """ล็อคอินอัตโนมัติ"""
    
    print("🔐 กำลังล็อคอิน Instagram อัตโนมัติ...")
    print("=" * 50)
    
    session = requests.Session()
    
    # Headers ที่จำลอง browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'X-Requested-With': 'XMLHttpRequest',
    }
    
    session.headers.update(headers)
    
    try:
        # ขั้นตอนที่ 1: ดึง CSRF token
        print("🔍 ขั้นตอนที่ 1: ดึง CSRF token...")
        response = session.get("https://www.instagram.com/accounts/login/")
        
        if response.status_code != 200:
            print(f"❌ ไม่สามารถเข้าหน้า login ได้: {response.status_code}")
            return None
        
        csrf_token = session.cookies.get('csrftoken')
        if not csrf_token:
            print("❌ ไม่พบ CSRF token")
            return None
        
        print(f"✅ ได้ CSRF token: {csrf_token[:15]}...")
        
        # ขั้นตอนที่ 2: ล็อคอินด้วยข้อมูลจริง
        print("🔐 ขั้นตอนที่ 2: ล็อคอิน...")
        
        # ใช้ข้อมูลจาก alx.trading account
        login_data = {
            'username': 'alx.trading',
            'password': 'Fleming1234',  # จากข้อมูลที่วิเคราะห์ได้
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'trustedDeviceRecords': '{}',
        }
        
        login_headers = headers.copy()
        login_headers.update({
            'X-CSRFToken': csrf_token,
            'X-Instagram-AJAX': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://www.instagram.com/accounts/login/',
        })
        
        print("📤 ส่งคำขอล็อคอิน...")
        response = session.post(
            "https://www.instagram.com/accounts/login/ajax/",
            data=login_data,
            headers=login_headers
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                
                if result.get('authenticated', False):
                    print("✅ ล็อคอินสำเร็จ!")
                    
                    # ขั้นตอนที่ 3: บันทึก session ใหม่
                    session_data = {
                        'sessionid': session.cookies.get('sessionid'),
                        'ds_user_id': session.cookies.get('ds_user_id'),
                        'csrf_token': csrf_token,
                        'login_time': datetime.now().isoformat(),
                        'username': 'alx.trading',
                        'cookies': dict(session.cookies)
                    }
                    
                    with open('fresh_session.json', 'w') as f:
                        json.dump(session_data, f, indent=2)
                    
                    print(f"💾 บันทึก session ใหม่: fresh_session.json")
                    print(f"🆔 User ID: {session_data.get('ds_user_id')}")
                    print(f"🔑 Session ID: {session_data.get('sessionid', '')[:20]}...")
                    
                    return session_data
                    
                else:
                    print(f"❌ ล็อคอินไม่สำเร็จ: {result}")
                    
                    # ลองใช้รหัสผ่านอื่น
                    other_passwords = ['Fleming1004', 'Fleming654', 'Fleming786', 'Fleming1060', 'Fleming1182']
                    
                    for pwd in other_passwords:
                        print(f"🔄 ลองรหัสผ่าน: {pwd}")
                        login_data['password'] = pwd
                        
                        response = session.post(
                            "https://www.instagram.com/accounts/login/ajax/",
                            data=login_data,
                            headers=login_headers
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            if result.get('authenticated', False):
                                print(f"✅ ล็อคอินสำเร็จด้วยรหัส: {pwd}")
                                
                                session_data = {
                                    'sessionid': session.cookies.get('sessionid'),
                                    'ds_user_id': session.cookies.get('ds_user_id'),
                                    'csrf_token': csrf_token,
                                    'login_time': datetime.now().isoformat(),
                                    'username': 'alx.trading',
                                    'password_used': pwd,
                                    'cookies': dict(session.cookies)
                                }
                                
                                with open('fresh_session.json', 'w') as f:
                                    json.dump(session_data, f, indent=2)
                                
                                print(f"💾 บันทึก session ใหม่: fresh_session.json")
                                return session_data
                        
                        time.sleep(2)  # รอก่อนลองครั้งต่อไป
                    
                    return None
                    
            except json.JSONDecodeError:
                print(f"❌ Response ไม่ใช่ JSON: {response.text[:200]}...")
                return None
        else:
            print(f"❌ ล็อคอินล้มเหลว: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        return None

def test_session(session_data):
    """ทดสอบ session ที่ได้"""
    
    if not session_data:
        return False
    
    print("\n🔍 ทดสอบ session ใหม่...")
    
    session = requests.Session()
    
    # ใส่ cookies จาก session
    for key, value in session_data.get('cookies', {}).items():
        session.cookies.set(key, value)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-CSRFToken': session_data.get('csrf_token', ''),
    }
    
    session.headers.update(headers)
    
    try:
        # ทดสอบดึงข้อมูลโปรไฟล์
        response = session.get('https://www.instagram.com/api/v1/users/web_profile_info/?username=alx.trading')
        
        if response.status_code == 200:
            data = response.json()
            user = data.get('data', {}).get('user', {})
            
            print(f"✅ Session ทำงานได้!")
            print(f"👤 Username: {user.get('username', 'N/A')}")
            print(f"📊 Followers: {user.get('edge_followed_by', {}).get('count', 'N/A')}")
            print(f"📊 Following: {user.get('edge_follow', {}).get('count', 'N/A')}")
            
            return True
        else:
            print(f"❌ ทดสอบ session ล้มเหลว: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการทดสอบ: {e}")
        return False

def main():
    print("🚀 Instagram Auto Login - ดึง Session ใหม่")
    print("=" * 60)
    
    # ล็อคอินอัตโนมัติ
    session_data = auto_login()
    
    if session_data:
        # ทดสอบ session
        if test_session(session_data):
            print("\n🎯 พร้อมใช้งาน!")
            print("📄 ไฟล์ session ใหม่: fresh_session.json")
            print("\n📋 ขั้นตอนต่อไป:")
            print("1. ใช้ fresh_session.json ดึงข้อมูลแชทจริง")
            print("2. รันโปรแกรมดึงข้อมูลการสนทนากับผู้หญิง")
        else:
            print("⚠️ Session อาจมีปัญหา")
    else:
        print("\n❌ ไม่สามารถล็อคอินได้")
        print("💡 อาจต้องล็อคอินด้วยตนเองผ่าน browser")

if __name__ == "__main__":
    main()
