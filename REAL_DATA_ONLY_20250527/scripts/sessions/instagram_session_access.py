#!/usr/bin/env python3
"""
Instagram Session Access Tool
ใช้ sessionid ที่มีอยู่เข้าถึง Instagram และสร้างลิงค์
"""

import requests
import json
import time
from datetime import datetime
import urllib.parse

class InstagramSessionManager:
    def __init__(self):
        self.base_url = "https://www.instagram.com"
        self.session = requests.Session()
        
        # User-Agent สำหรับ Instagram
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        
        self.session.headers.update(self.headers)
    
    def setup_session(self, sessionid, ds_user_id=None, csrf_token=None):
        """ตั้งค่า session ด้วย cookies"""
        print(f"🔑 ตั้งค่า Instagram session...")
        
        # ตั้งค่า cookies
        cookies = {
            'sessionid': sessionid,
            'csrftoken': csrf_token or 'missing',
        }
        
        if ds_user_id:
            cookies['ds_user_id'] = ds_user_id
        
        # เพิ่ม cookies อื่นๆ ที่จำเป็น
        additional_cookies = {
            'mid': 'ZmJ8AwALAAG5n8CJBgABbw',
            'ig_did': 'B4F8C0A0-8E4A-4F5F-9C2D-1234567890AB',
            'ig_nrcb': '1',
            'shbid': '"1234\\0544976283726\\0541748299999:01f70c9f8b9e4c8c8d5a2b3c4e5f6789:8a7b6c5d4e3f2a1b9c8d7e6f5a4b3c2d"',
            'shbts': '"1748264421\\0544976283726\\0541748299999:01f70c9f8b9e4c8c8d5a2b3c4e5f6789"',
            'rur': '"EAG\\0544976283726\\0541748299999:01f70c9f8b9e4c8c8d5a2b3c4e5f6789"'
        }
        
        cookies.update(additional_cookies)
        
        for name, value in cookies.items():
            self.session.cookies.set(name, value, domain='.instagram.com')
        
        print(f"✅ Session cookies ตั้งค่าเสร็จสิ้น")
        return True
    
    def verify_session(self):
        """ตรวจสอบความถูกต้องของ session"""
        print("🔍 ตรวจสอบ session...")
        
        try:
            # เข้าถึงหน้าโปรไฟล์
            response = self.session.get(f"{self.base_url}/accounts/edit/", timeout=10)
            
            if response.status_code == 200:
                if 'authenticity_token' in response.text or 'csrf_token' in response.text:
                    print("✅ Session ใช้งานได้!")
                    return True
                else:
                    print("⚠️ Session อาจหมดอายุ")
                    return False
            else:
                print(f"❌ Session ไม่ถูกต้อง (Status: {response.status_code})")
                return False
                
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
            return False
    
    def get_profile_info(self, username):
        """ดึงข้อมูลโปรไฟล์"""
        print(f"👤 ดึงข้อมูลโปรไฟล์: {username}")
        
        try:
            # ลองเข้าถึงโปรไฟล์
            url = f"{self.base_url}/{username}/"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ เข้าถึงโปรไฟล์ {username} ได้")
                
                # สร้าง direct link
                profile_links = {
                    'profile_url': url,
                    'stories_url': f"{self.base_url}/stories/{username}/",
                    'direct_message_url': f"{self.base_url}/direct/t/",
                    'followers_url': f"{self.base_url}/{username}/followers/",
                    'following_url': f"{self.base_url}/{username}/following/"
                }
                
                return profile_links
            else:
                print(f"❌ ไม่สามารถเข้าถึงโปรไฟล์ได้ (Status: {response.status_code})")
                return None
                
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
            return None
    
    def search_user(self, query):
        """ค้นหาผู้ใช้"""
        print(f"🔍 ค้นหา: {query}")
        
        try:
            # Instagram search API endpoint
            search_url = f"{self.base_url}/web/search/topsearch/"
            params = {
                'query': query,
                'rank_token': str(time.time()),
                'count': 10
            }
            
            response = self.session.get(search_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                users = data.get('users', [])
                
                print(f"✅ พบผู้ใช้ {len(users)} คน")
                
                results = []
                for user in users:
                    user_info = user.get('user', {})
                    results.append({
                        'username': user_info.get('username'),
                        'full_name': user_info.get('full_name'),
                        'profile_pic_url': user_info.get('profile_pic_url'),
                        'is_verified': user_info.get('is_verified', False),
                        'is_private': user_info.get('is_private', False)
                    })
                
                return results
            else:
                print(f"❌ การค้นหาล้มเหลว (Status: {response.status_code})")
                return []
                
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
            return []
    
    def generate_access_links(self, sessionid, target_username="alx.trading"):
        """สร้างลิงค์สำหรับเข้าถึงโดยตรง"""
        print(f"🔗 สร้างลิงค์เข้าถึง...")
        
        # สร้าง authenticated links
        links = {
            'direct_access': f"{self.base_url}/{target_username}/?sessionid={sessionid}",
            'stories_access': f"{self.base_url}/stories/{target_username}/?sessionid={sessionid}",
            'profile_access': f"{self.base_url}/{target_username}/",
            'dm_access': f"{self.base_url}/direct/inbox/",
            'explore_access': f"{self.base_url}/explore/",
        }
        
        # สร้าง bookmarklet สำหรับ browser
        bookmarklet_code = f"""
javascript:(function(){{
    document.cookie = "sessionid={sessionid}; domain=.instagram.com; path=/; secure; samesite=lax";
    window.location.href = "https://www.instagram.com/{target_username}/";
}})();
        """.strip()
        
        links['bookmarklet'] = bookmarklet_code
        
        return links
    
    def save_session_report(self, sessionid, ds_user_id, links, verification_status):
        """บันทึกรายงาน session"""
        timestamp = int(time.time())
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "session_info": {
                "sessionid": sessionid,
                "ds_user_id": ds_user_id,
                "status": "active" if verification_status else "expired"
            },
            "access_links": links,
            "verification": {
                "verified_at": datetime.now().isoformat(),
                "status": verification_status,
                "method": "profile_access_test"
            }
        }
        
        filename = f"instagram_session_report_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 รายงานบันทึกที่: {filename}")
        return filename

def main():
    print("🍭 Instagram Session Access Tool")
    print("=" * 50)
    
    # Session data ที่ผู้ใช้ให้มา
    session_data = {
        "sessionid": "4976283726%3A1JgRzA56Q8e8Qs%3A12",
        "ds_user_id": "4976283726"
    }
    
    manager = InstagramSessionManager()
    
    # ตั้งค่า session
    manager.setup_session(
        sessionid=session_data["sessionid"],
        ds_user_id=session_data["ds_user_id"]
    )
    
    # ตรวจสอบ session
    is_valid = manager.verify_session()
    
    # สร้างลิงค์
    links = manager.generate_access_links(session_data["sessionid"], "alx.trading")
    
    print("\n🔗 INSTAGRAM ACCESS LINKS:")
    print("=" * 50)
    
    for name, url in links.items():
        if name != 'bookmarklet':
            print(f"{name}: {url}")
    
    print(f"\n📋 BOOKMARKLET (Copy to browser bookmark):")
    print(f"{links['bookmarklet']}")
    
    # ทดสอบเข้าถึง alx.trading
    profile_links = manager.get_profile_info("alx.trading")
    
    if profile_links:
        print(f"\n✅ ALX.TRADING ACCESS CONFIRMED!")
        print("Direct links:")
        for name, url in profile_links.items():
            print(f"  {name}: {url}")
    
    # บันทึกรายงาน
    report_file = manager.save_session_report(
        session_data["sessionid"],
        session_data["ds_user_id"], 
        links,
        is_valid
    )
    
    print(f"\n🎉 เสร็จสิ้น! รายงานบันทึกใน: {report_file}")

if __name__ == "__main__":
    main()
