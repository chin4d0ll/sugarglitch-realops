#!/usr/bin/env python3
"""
Instagram DM Extractor - iPad Compatible Solution
ทางแก้สำหรับผู้ใช้ iPad และไม่มี sessionid
"""

import os
import json
import requests
import time
from datetime import datetime

class iPadInstagramSolution:
    def __init__(self):
        self.target = "alx.trading"
        
        # สร้างโฟลเดอร์ผลลัพธ์
        os.makedirs("ipad_extractions", exist_ok=True)
        os.makedirs("ipad_logs", exist_ok=True)
    
    def get_session_from_ipad(self):
        """วิธีการ get session จาก iPad"""
        print("📱 วิธีการ GET SESSION จาก iPad")
        print("=" * 40)
        print()
        print("🔧 วิธีที่ 1: ใช้ Safari บน iPad")
        print("1. เปิด Safari → ไป instagram.com")
        print("2. Login เข้าบัญชี")
        print("3. ที่ address bar พิมพ์: javascript:alert(document.cookie)")
        print("4. กด Enter → จะขึ้น popup แสดง cookies")
        print("5. หา sessionid= แล้วคัดลอกส่วนหลัง = จนถึง ;")
        print()
        print("🔧 วิธีที่ 2: ใช้ Chrome บน iPad")
        print("1. เปิด Chrome → ไป instagram.com/accounts/login")
        print("2. Login เข้าบัญชี")
        print("3. กดที่ ... (menu) → More tools → Developer tools")
        print("4. กด Console tab")
        print("5. พิมพ์: document.cookie")
        print("6. หา sessionid แล้วคัดลอก")
        print()
        print("🔧 วิธีที่ 3: ใช้ Shortcut (iOS)")
        print("1. สร้าง Shortcut ใหม่")
        print("2. เพิ่ม action 'Get Contents of Web Page'")
        print("3. URL: https://instagram.com")
        print("4. เพิ่ม action 'Get Text from Input'")
        print("5. รัน Shortcut หลังจาก login Instagram")
        
        return None
    
    def extract_without_session(self):
        """สกัดข้อมูลโดยไม่ต้องใช้ session (ข้อมูลสาธารณะ)"""
        print("\n🚀 สกัดข้อมูลแบบไม่ต้อง Session")
        print("=" * 40)
        
        # ลอง scrape ข้อมูลสาธารณะ
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
        }
        
        target_url = f"https://www.instagram.com/{self.target}/"
        
        try:
            print(f"🔍 เข้าถึง: {target_url}")
            response = requests.get(target_url, headers=headers, timeout=15)
            
            print(f"📡 สถานะ: HTTP {response.status_code}")
            
            if response.status_code == 200:
                print("✅ เข้าถึงหน้าได้สำเร็จ!")
                
                # บันทึกข้อมูลที่ได้
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # บันทึก HTML
                html_file = f"ipad_extractions/{self.target}_public_{timestamp}.html"
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                print(f"💾 บันทึก HTML: {html_file}")
                
                # ลองหาข้อมูลพื้นฐาน
                self.extract_public_info(response.text, timestamp)
                
                return True
                
            elif response.status_code == 429:
                print("❌ ถูก rate limit - ลองใช้ VPN")
                
            else:
                print(f"❌ ไม่สามารถเข้าถึงได้: HTTP {response.status_code}")
            
        except Exception as e:
            print(f"❌ ข้อผิดพลาด: {e}")
        
        return False
    
    def extract_public_info(self, html_content, timestamp):
        """สกัดข้อมูลสาธารณะจาก HTML"""
        print("\n📊 วิเคราะห์ข้อมูลสาธารณะ")
        print("=" * 30)
        
        import re
        
        # หาข้อมูล JSON จาก HTML
        json_match = re.search(r'window\._sharedData = ({.+?});', html_content)
        
        if json_match:
            try:
                data = json.loads(json_match.group(1))
                
                # บันทึกข้อมูล JSON
                json_file = f"ipad_extractions/{self.target}_data_{timestamp}.json"
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"💾 บันทึก JSON: {json_file}")
                
                # แสดงข้อมูลพื้นฐาน
                if 'entry_data' in data and 'ProfilePage' in data['entry_data']:
                    profile_data = data['entry_data']['ProfilePage'][0]
                    user = profile_data.get('graphql', {}).get('user', {})
                    
                    print("\n👤 ข้อมูลบัญชีที่พบ:")
                    print(f"   ชื่อผู้ใช้: {user.get('username', 'N/A')}")
                    print(f"   ชื่อเต็ม: {user.get('full_name', 'N/A')}")
                    print(f"   ผู้ติดตาม: {user.get('edge_followed_by', {}).get('count', 'N/A'):,}")
                    print(f"   กำลังติดตาม: {user.get('edge_follow', {}).get('count', 'N/A'):,}")
                    print(f"   โพสต์: {user.get('edge_owner_to_timeline_media', {}).get('count', 'N/A'):,}")
                    print(f"   เป็นบัญชีส่วนตัว: {'ใช่' if user.get('is_private') else 'ไม่'}")
                    print(f"   ได้รับการยืนยัน: {'ใช่' if user.get('is_verified') else 'ไม่'}")
                    
                    # ข้อมูลเพิ่มเติม
                    bio = user.get('biography', '')
                    if bio:
                        print(f"   ประวัติ: {bio}")
                    
                    external_url = user.get('external_url', '')
                    if external_url:
                        print(f"   เว็บไซต์: {external_url}")
                
                print(f"\n✅ สกัดข้อมูลสาธารณะสำเร็จ!")
                return True
                
            except Exception as e:
                print(f"❌ ไม่สามารถแปลง JSON: {e}")
        
        # ลองหาข้อมูลด้วยวิธีอื่น
        self.extract_basic_info(html_content)
        return False
    
    def extract_basic_info(self, html_content):
        """สกัดข้อมูลพื้นฐานจาก HTML"""
        import re
        
        print("🔍 หาข้อมูลพื้นฐานจาก HTML")
        
        # หา username
        username_match = re.search(r'"username":"([^"]+)"', html_content)
        if username_match:
            print(f"   👤 Username: {username_match.group(1)}")
        
        # หา full name
        fullname_match = re.search(r'"full_name":"([^"]+)"', html_content)
        if fullname_match:
            print(f"   📝 Full name: {fullname_match.group(1)}")
        
        # หาจำนวน followers
        followers_match = re.search(r'"edge_followed_by":{"count":(\d+)}', html_content)
        if followers_match:
            followers = int(followers_match.group(1))
            print(f"   👥 Followers: {followers:,}")
        
        # หาจำนวน following
        following_match = re.search(r'"edge_follow":{"count":(\d+)}', html_content)
        if following_match:
            following = int(following_match.group(1))
            print(f"   ➡️ Following: {following:,}")
    
    def create_demo_session(self):
        """สร้าง demo session สำหรับทดสอบ"""
        print("\n🔧 สร้าง Demo Session สำหรับทดสอบ")
        print("=" * 40)
        
        # สร้าง session file ปลอมสำหรับ demo
        demo_session = {
            "sessionid": "demo_session_for_ipad_testing",
            "note": "นี่คือ session demo สำหรับทดสอบระบบ",
            "status": "demo",
            "platform": "iPad",
            "created": datetime.now().isoformat()
        }
        
        with open("demo_session.json", "w") as f:
            json.dump(demo_session, f, indent=2, ensure_ascii=False)
        
        print("✅ สร้าง demo_session.json")
        print("💡 ไฟล์นี้ใช้สำหรับทดสอบระบบเท่านั้น")
    
    def show_alternatives(self):
        """แสดงทางเลือกอื่นๆ สำหรับ iPad"""
        print("\n🎯 ทางเลือกสำหรับผู้ใช้ iPad")
        print("=" * 35)
        
        print("📱 ตัวเลือกที่ 1: ใช้เครื่องคอมพิวเตอร์")
        print("   - เข้า instagram.com ด้วย Chrome/Firefox")
        print("   - กด F12 เพื่อเปิด Developer Tools")
        print("   - หา sessionid ใน Cookies")
        print()
        
        print("🌐 ตัวเลือกที่ 2: ใช้ VPN + Public Data")
        print("   - เปิด VPN บน iPad")
        print("   - ใช้ระบบสกัดข้อมูลสาธารณะ")
        print("   - ได้ข้อมูลพื้นฐานของบัญชี")
        print()
        
        print("🤝 ตัวเลือกที่ 3: ขอความช่วยเหลือ")
        print("   - ขอให้เพื่อนที่มีคอมช่วยหา sessionid")
        print("   - ส่ง sessionid มาทาง chat")
        print("   - ใช้ระบบสกัด DM ได้เต็มรูปแบบ")
        print()
        
        print("⚡ ตัวเลือกที่ 4: รอการพัฒนา")
        print("   - เรากำลังพัฒนาระบบใหม่ที่ไม่ต้องใช้ session")
        print("   - จะใช้ browser automation แทน")
        print("   - คาดว่าจะเสร็จในไม่ช้า")

def main():
    """Main function สำหรับผู้ใช้ iPad"""
    
    solution = iPadInstagramSolution()
    
    print("📱 INSTAGRAM DM EXTRACTOR - iPad SOLUTION")
    print("=" * 50)
    print("ทางแก้ไขสำหรับผู้ใช้ iPad และไม่มี sessionid")
    print()
    
    # แสดงวิธีการ get session
    solution.get_session_from_ipad()
    
    # ลองสกัดข้อมูลสาธารณะ
    print("\n" + "="*50)
    solution.extract_without_session()
    
    # สร้าง demo session
    solution.create_demo_session()
    
    # แสดงทางเลือกอื่น
    solution.show_alternatives()
    
    print("\n" + "="*50)
    print("📝 สรุป:")
    print("1. ลองเข้าถึงข้อมูลสาธารณะแล้ว")
    print("2. สร้าง demo session สำหรับทดสอบ")
    print("3. มีทางเลือกหลายแบบให้เลือก")
    print("4. ระบบพร้อมรองรับเมื่อมี sessionid")
    print()
    print("🎯 แนะนำ: ลองใช้ VPN แล้วสกัดข้อมูลสาธารณะ")
    print("   หรือหา sessionid ด้วยวิธีที่แสดงข้างบน")

if __name__ == "__main__":
    main()
