#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ล็อคอิน Instagram เพื่อดึง session ใหม่
Login to Instagram to get fresh session
"""

import requests
import json
import time
import random
from datetime import datetime

class InstagramLogin:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.instagram.com"
        
        # Headers ที่จำลอง browser จริง
        self.headers = {
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
        
        self.session.headers.update(self.headers)
    
    def get_csrf_token(self):
        """ดึง CSRF token"""
        try:
            print("🔍 กำลังดึง CSRF token...")
            response = self.session.get(f"{self.base_url}/accounts/login/")
            
            if response.status_code == 200:
                # หา csrf token ใน cookies
                csrf_token = self.session.cookies.get('csrftoken')
                if csrf_token:
                    print(f"✅ ได้ CSRF token: {csrf_token[:20]}...")
                    return csrf_token
                else:
                    print("❌ ไม่พบ CSRF token ใน cookies")
                    return None
            else:
                print(f"❌ ไม่สามารถเข้าหน้า login ได้: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการดึง CSRF token: {e}")
            return None
    
    def login(self, username, password):
        """ล็อคอิน Instagram"""
        try:
            print(f"🔐 กำลังล็อคอินด้วย username: {username}")
            
            # ดึง CSRF token ก่อน
            csrf_token = self.get_csrf_token()
            if not csrf_token:
                return False
            
            # ข้อมูลสำหรับล็อคอิน
            login_data = {
                'username': username,
                'password': password,
                'queryParams': '{}',
                'optIntoOneTap': 'false',
                'trustedDeviceRecords': '{}',
            }
            
            # Headers สำหรับการล็อคอิน
            login_headers = self.headers.copy()
            login_headers.update({
                'X-CSRFToken': csrf_token,
                'X-Instagram-AJAX': '1',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': f"{self.base_url}/accounts/login/",
            })
            
            # ส่งคำขอล็อคอิน
            response = self.session.post(
                f"{self.base_url}/accounts/login/ajax/",
                data=login_data,
                headers=login_headers
            )
            
            print(f"📤 ส่งคำขอล็อคอิน... Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('authenticated', False):
                    print("✅ ล็อคอินสำเร็จ!")
                    
                    # บันทึก session
                    session_data = {
                        'sessionid': self.session.cookies.get('sessionid'),
                        'ds_user_id': self.session.cookies.get('ds_user_id'),
                        'csrf_token': csrf_token,
                        'login_time': datetime.now().isoformat(),
                        'username': username
                    }
                    
                    # บันทึกลงไฟล์
                    with open('new_session.json', 'w') as f:
                        json.dump(session_data, f, indent=2)
                    
                    print(f"💾 บันทึก session ใหม่ไว้ใน: new_session.json")
                    print(f"🆔 User ID: {session_data.get('ds_user_id')}")
                    print(f"🔑 Session ID: {session_data.get('sessionid', '')[:20]}...")
                    
                    return True
                    
                elif result.get('checkpoint_url'):
                    print("🚫 ต้องการ checkpoint verification")
                    print(f"URL: {result.get('checkpoint_url')}")
                    return False
                    
                elif result.get('two_factor_required'):
                    print("🔐 ต้องการ two-factor authentication")
                    return False
                    
                else:
                    print(f"❌ ล็อคอินไม่สำเร็จ: {result.get('message', 'Unknown error')}")
                    return False
            else:
                print(f"❌ การล็อคอินล้มเหลว: {response.status_code}")
                print(f"Response: {response.text[:200]}...")
                return False
                
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการล็อคอิน: {e}")
            return False
    
    def get_user_info(self):
        """ดึงข้อมูลผู้ใช้เพื่อทดสอบ session"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/users/web_profile_info/?username=alx.trading")
            
            if response.status_code == 200:
                data = response.json()
                user = data.get('data', {}).get('user', {})
                print(f"👤 ข้อมูลผู้ใช้: {user.get('full_name', 'N/A')}")
                print(f"📊 Followers: {user.get('edge_followed_by', {}).get('count', 'N/A')}")
                return True
            else:
                print(f"❌ ไม่สามารถดึงข้อมูลผู้ใช้ได้: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
            return False

def main():
    print("🔐 Instagram Login - ดึง Session ใหม่")
    print("=" * 50)
    
    # ข้อมูลล็อคอิน
    username = input("👤 Username: ").strip()
    password = input("🔑 Password: ").strip()
    
    if not username or not password:
        print("❌ กรุณากรอก username และ password")
        return
    
    # สร้าง Instagram login instance
    ig = InstagramLogin()
    
    # ล็อคอิน
    if ig.login(username, password):
        print("\n✅ ล็อคอินสำเร็จ!")
        
        # ทดสอบ session
        print("\n🔍 ทดสอบ session...")
        if ig.get_user_info():
            print("✅ Session ทำงานได้ปกติ!")
        else:
            print("⚠️ Session อาจมีปัญหา")
        
        print("\n🎯 ขั้นตอนต่อไป:")
        print("1. ใช้ new_session.json เพื่อดึงข้อมูลแชทจริง")
        print("2. รันโปรแกรมดึงข้อมูลแชทด้วย session ใหม่")
        
    else:
        print("❌ ล็อคอินไม่สำเร็จ")
        print("\n💡 เหตุผลที่อาจเป็นไปได้:")
        print("• Username หรือ Password ไม่ถูกต้อง")
        print("• บัญชีถูก lock หรือต้องการ verification")
        print("• Instagram ตรวจพบ automation")
        print("• ต้องการ two-factor authentication")

if __name__ == "__main__":
    main()
