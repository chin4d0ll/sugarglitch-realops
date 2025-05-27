#!/usr/bin/env python3
"""
Advanced Instagram Access Tool
ใช้ sessionid เข้าถึง Instagram ด้วยการป้องกัน rate limiting
"""

import requests
import json
import time
import random
from datetime import datetime
import urllib.parse
import webbrowser
import sys

class AdvancedInstagramAccess:
    def __init__(self):
        self.sessionid = "4976283726%3A1JgRzA56Q8e8Qs%3A12"
        self.ds_user_id = "4976283726"
        self.target_username = "alx.trading"
        
        self.session = requests.Session()
        self.setup_session()
        
    def setup_session(self):
        """ตั้งค่า session และ headers"""
        # หมุนเวียน User-Agent
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        
        self.session.headers.update(headers)
        
        # ตั้งค่า cookies
        cookies = {
            'sessionid': self.sessionid,
            'ds_user_id': self.ds_user_id,
            'csrftoken': 'missing',
            'mid': f'Zm{random.randint(10000, 99999)}wALAAG5n8CJBgABbw',
            'ig_did': f'B4F8C0A0-8E4A-4F5F-9C2D-{random.randint(100000000000, 999999999999)}',
            'shbid': f'"12345\\0544976283726\\054{int(time.time()) + 604800}\\0541\\054"',
            'shbts': f'"{int(time.time())}\\0544976283726\\054{int(time.time()) + 604800}\\0541\\054"',
            'rur': f'"EAG\\0544976283726\\054{int(time.time()) + 1800}\\0540\\054"'
        }
        
        for name, value in cookies.items():
            self.session.cookies.set(name, value, domain='.instagram.com')
    
    def wait_random(self, min_sec=2, max_sec=5):
        """รอระยะเวลาสุ่มเพื่อหลีกเลี่ยง rate limiting"""
        wait_time = random.uniform(min_sec, max_sec)
        time.sleep(wait_time)
    
    def generate_access_urls(self):
        """สร้าง URLs สำหรับเข้าถึง"""
        base_urls = {
            'profile': f'https://www.instagram.com/{self.target_username}/',
            'stories': f'https://www.instagram.com/stories/{self.target_username}/',
            'tagged': f'https://www.instagram.com/{self.target_username}/tagged/',
            'reels': f'https://www.instagram.com/{self.target_username}/reels/',
            'following': f'https://www.instagram.com/{self.target_username}/following/',
            'followers': f'https://www.instagram.com/{self.target_username}/followers/',
            'dm_direct': f'https://www.instagram.com/direct/t/{self.ds_user_id}/',
            'explore': 'https://www.instagram.com/explore/',
            'activity': 'https://www.instagram.com/accounts/activity/',
            'feed': 'https://www.instagram.com/'
        }
        
        # เพิ่ม sessionid ใน URL parameter สำหรับบางลิงค์
        auth_urls = {}
        for key, url in base_urls.items():
            if key in ['profile', 'stories', 'tagged', 'reels']:
                auth_urls[f'{key}_auth'] = f"{url}?sessionid={urllib.parse.quote(self.sessionid)}"
            auth_urls[key] = url
        
        return auth_urls
    
    def create_bookmarklet(self):
        """สร้าง bookmarklet สำหรับใช้ใน browser"""
        bookmarklet = f'''javascript:(function(){{
    // ตั้งค่า cookies
    document.cookie = "sessionid={self.sessionid}; domain=.instagram.com; path=/; secure; samesite=lax";
    document.cookie = "ds_user_id={self.ds_user_id}; domain=.instagram.com; path=/; secure; samesite=lax";
    document.cookie = "csrftoken=missing; domain=.instagram.com; path=/; secure; samesite=lax";
    
    // รอให้ cookies ตั้งค่าเสร็จ
    setTimeout(function() {{
        window.location.href = "https://www.instagram.com/{self.target_username}/";
    }}, 1000);
}})();'''
        return bookmarklet
    
    def create_browser_script(self):
        """สร้าง JavaScript script สำหรับ console"""
        script = f'''
// Instagram Session Setup Script
// Copy และ paste ใน browser console ของ Instagram

// 1. ตั้งค่า cookies
document.cookie = "sessionid={self.sessionid}; domain=.instagram.com; path=/; secure; samesite=lax";
document.cookie = "ds_user_id={self.ds_user_id}; domain=.instagram.com; path=/; secure; samesite=lax";
document.cookie = "csrftoken=missing; domain=.instagram.com; path=/; secure; samesite=lax";

// 2. ไปยังโปรไฟล์
setTimeout(() => {{
    window.location.href = "https://www.instagram.com/{self.target_username}/";
}}, 2000);

console.log("✅ Instagram session cookies ตั้งค่าเสร็จสิ้น!");
console.log("🔄 กำลังไปยังโปรไฟล์...");
'''
        return script
    
    def test_access_gentle(self):
        """ทดสอบการเข้าถึงแบบระมัดระวัง"""
        print("🧪 ทดสอบการเข้าถึงแบบระมัดระวัง...")
        
        # ทดสอบหน้าแรก
        try:
            self.wait_random(1, 3)
            response = self.session.get('https://www.instagram.com/')
            print(f"✅ หน้าแรก: {response.status_code}")
            
            if response.status_code == 200:
                if 'Instagram' in response.text:
                    print("✅ เข้าถึง Instagram ได้")
                    return True
                else:
                    print("⚠️  ได้รับหน้าเพจแต่ไม่ใช่ Instagram")
            else:
                print(f"❌ ไม่สามารถเข้าถึงได้: {response.status_code}")
                
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
            
        return False
    
    def open_in_browser(self, url):
        """เปิด URL ใน browser"""
        try:
            webbrowser.open(url)
            return True
        except:
            return False
    
    def main_menu(self):
        """เมนูหลัก"""
        print("🍭 Advanced Instagram Access Tool")
        print("=" * 50)
        
        urls = self.generate_access_urls()
        bookmarklet = self.create_bookmarklet()
        browser_script = self.create_browser_script()
        
        print("\n🔗 ACCESS METHODS:")
        print("1. Direct Browser Access (Recommended)")
        print("2. Show All URLs")
        print("3. Generate Browser Script")
        print("4. Create Bookmarklet")
        print("5. Test Connection")
        print("6. Auto-Open Profile")
        print("0. Exit")
        
        while True:
            choice = input("\n👉 เลือกตัวเลือก (1-6, 0=exit): ").strip()
            
            if choice == '1':
                print(f"\n🌐 เปิด browser และไปที่:")
                print(f"https://www.instagram.com/{self.target_username}/")
                print(f"\n📋 แล้วเปิด Developer Console (F12) และ paste:")
                print("=" * 60)
                print(browser_script)
                print("=" * 60)
                
            elif choice == '2':
                print("\n🔗 ALL ACCESS URLS:")
                print("=" * 40)
                for name, url in urls.items():
                    print(f"{name}: {url}")
                    
            elif choice == '3':
                print("\n📜 BROWSER CONSOLE SCRIPT:")
                print("=" * 60)
                print(browser_script)
                print("=" * 60)
                print("\n💡 วิธีใช้:")
                print("1. เปิด browser ไปที่ instagram.com")
                print("2. กด F12 เปิด Developer Tools")
                print("3. ไปที่ tab Console")
                print("4. Copy script ข้างบนแล้ว paste")
                print("5. กด Enter")
                
            elif choice == '4':
                print("\n🔖 BOOKMARKLET:")
                print("=" * 60)
                print(bookmarklet)
                print("=" * 60)
                print("\n💡 วิธีใช้:")
                print("1. Copy โค้ดข้างบน")
                print("2. สร้าง bookmark ใหม่ใน browser")
                print("3. ใส่โค้ดใน URL field")
                print("4. Save แล้วคลิก bookmark เมื่อต้องการใช้")
                
            elif choice == '5':
                self.test_access_gentle()
                
            elif choice == '6':
                print("🚀 เปิดโปรไฟล์ใน browser...")
                if self.open_in_browser(f"https://www.instagram.com/{self.target_username}/"):
                    print("✅ เปิดแล้ว! ใช้ script จากตัวเลือก 3 ใน console")
                else:
                    print("❌ ไม่สามารถเปิด browser ได้")
                    
            elif choice == '0':
                print("👋 ขอบคุณที่ใช้งาน!")
                break
                
            else:
                print("❌ กรุณาเลือก 1-6 หรือ 0")

def main():
    """ฟังก์ชันหลัก"""
    try:
        app = AdvancedInstagramAccess()
        
        # ทดสอบการเชื่อมต่อ
        print("🔍 กำลังทดสอบการเชื่อมต่อ...")
        if app.test_access_gentle():
            print("✅ พร้อมใช้งาน!")
            app.main_menu()
        else:
            print("⚠️  การเชื่อมต่อมีปัญหา แต่ยังสามารถใช้ browser method ได้")
            app.main_menu()
            
    except KeyboardInterrupt:
        print("\n\n👋 ขอบคุณที่ใช้งาน!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
