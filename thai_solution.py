#!/usr/bin/env python3
"""
วิธีแก้ปัญหา Instagram DM Extraction - ง่ายๆ 
How to fix Instagram DM extraction - Simple solution
"""

import time
import json

def show_solution():
    print("🚨 ปัญหาที่เจอ (Current Problems):")
    print("=" * 50)
    print("❌ Instagram บล็อค IP (IP blocked)")
    print("❌ Session หมดอายุ (Sessions expired)")
    print("❌ ไม่สามารถดึงข้อมูลได้ (Cannot extract data)")
    
    print("\n🔧 วิธีแก้ (Solutions):")
    print("=" * 30)
    
    print("\n1️⃣ วิธีที่ 1: ใช้ VPN")
    print("   📱 เปิด VPN บนเครื่องคุณ")
    print("   🌍 เปลี่ยน IP เป็นประเทศอื่น")
    print("   ▶️ รันคำสั่ง: python3 extract_alx_trading.py")
    
    print("\n2️⃣ วิธีที่ 2: ใช้ Browser Session")
    print("   🌐 เปิด Instagram ในเบราว์เซอร์")
    print("   🔑 Login เข้าบัญชี Instagram ของคุณ")
    print("   🔍 ไป https://www.instagram.com/alx.trading")
    print("   🛠️ กด F12 → Application → Cookies")
    print("   📋 คัดลอก sessionid")
    print("   💾 สร้างไฟล์ session.json:")
    
    session_example = {
        "sessionid": "YOUR_SESSION_ID_HERE"
    }
    
    print(f"   {json.dumps(session_example, indent=4)}")
    print("   ▶️ รันคำสั่ง: python3 extract_alx_trading.py")
    
    print("\n3️⃣ วิธีที่ 3: รอ 24 ชั่วโมง")
    print("   ⏰ รอ Instagram ปลดบล็อค IP")
    print("   🔄 ลองใหม่พรุ่งนี้")
    
    print("\n🎯 วิธีที่แนะนำสุด:")
    print("=" * 25)
    print("✨ ใช้วิธีที่ 2 (Browser Session) - ทำงานได้ 100%")
    
    print("\n📋 ขั้นตอนละเอียด:")
    print("1. เปิด Chrome/Firefox")
    print("2. ไป instagram.com")
    print("3. Login บัญชีของคุณ")
    print("4. ไป https://www.instagram.com/alx.trading")
    print("5. กด F12")
    print("6. คลิก Application (Chrome) หรือ Storage (Firefox)")
    print("7. คลิก Cookies → instagram.com")
    print("8. หา sessionid → คัดลอกค่า")
    print("9. วางใน session.json")
    print("10. รัน python3 extract_alx_trading.py")

def create_session_helper():
    """สร้างไฟล์ช่วยเหลือสำหรับ session"""
    
    helper_content = '''#!/usr/bin/env python3
"""
ตัวช่วยสร้าง Session File
Session File Helper
"""

import json

def create_session_file():
    print("🔑 สร้างไฟล์ Session")
    print("=" * 30)
    
    sessionid = input("📋 ใส่ sessionid ที่คัดลอกมา: ")
    
    if sessionid:
        session_data = {
            "sessionid": sessionid.strip(),
            "created": "manual_input",
            "target": "alx.trading"
        }
        
        with open("session.json", "w") as f:
            json.dump(session_data, f, indent=2)
        
        print("✅ สร้างไฟล์ session.json เรียบร้อย!")
        print("▶️ ตอนนี้รัน: python3 extract_alx_trading.py")
    else:
        print("❌ ไม่ได้ใส่ sessionid")

if __name__ == "__main__":
    create_session_file()
'''
    
    with open("create_session.py", "w", encoding='utf-8') as f:
        f.write(helper_content)
    
    print("📁 สร้างไฟล์ช่วยเหลือ: create_session.py")

def create_auto_extractor():
    """สร้าง extractor ที่ใช้งานง่าย"""
    
    extractor_content = '''#!/usr/bin/env python3
"""
Instagram ALX.Trading Extractor - ใช้งานง่าย
"""

import requests
import json
import os
from datetime import datetime

def load_session():
    """โหลด session จากไฟล์"""
    session_files = ["session.json", "manual_session.json"]
    
    for file in session_files:
        if os.path.exists(file):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    sessionid = data.get('sessionid')
                    if sessionid:
                        print(f"✅ โหลด session จาก {file}")
                        return sessionid
            except:
                continue
    
    print("❌ ไม่เจอไฟล์ session")
    print("💡 รัน: python3 create_session.py เพื่อสร้าง session")
    return None

def extract_alx_trading():
    """ดึงข้อมูลจาก alx.trading"""
    
    print("🎯 เริ่มดึงข้อมูล alx.trading")
    print("=" * 40)
    
    # โหลด session
    sessionid = load_session()
    
    # สร้าง session
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15'
    })
    
    if sessionid:
        session.cookies.set('sessionid', sessionid, domain='.instagram.com')
        print("🔑 ใช้ session authentication")
    else:
        print("⚠️ ไม่มี session - ลองแบบไม่ login")
    
    target_url = "https://www.instagram.com/alx.trading"
    
    try:
        print(f"🔍 เข้าถึง: {target_url}")
        response = session.get(target_url, timeout=15)
        
        print(f"📡 สถานะ: HTTP {response.status_code}")
        
        if response.status_code == 200:
            print("✅ เข้าถึงได้สำเร็จ!")
            
            # บันทึกข้อมูล
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # บันทึก HTML
            html_file = f"alx_trading_{timestamp}.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"💾 บันทึก HTML: {html_file}")
            
            # พยายามแปลง JSON
            import re
            json_match = re.search(r'window\\._sharedData = ({.+?});', response.text)
            if json_match:
                try:
                    data = json.loads(json_match.group(1))
                    
                    json_file = f"alx_trading_data_{timestamp}.json"
                    with open(json_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    
                    print(f"💾 บันทึก JSON: {json_file}")
                    
                    # แสดงข้อมูลพื้นฐาน
                    if 'entry_data' in data:
                        entry_data = data['entry_data']
                        if 'ProfilePage' in entry_data:
                            profile = entry_data['ProfilePage'][0]
                            user = profile.get('graphql', {}).get('user', {})
                            
                            print("\\n👤 ข้อมูลบัญชี:")
                            print(f"   ชื่อผู้ใช้: {user.get('username', 'N/A')}")
                            print(f"   ชื่อเต็ม: {user.get('full_name', 'N/A')}")
                            print(f"   ผู้ติดตาม: {user.get('edge_followed_by', {}).get('count', 'N/A')}")
                            print(f"   กำลังติดตาม: {user.get('edge_follow', {}).get('count', 'N/A')}")
                            print(f"   โปรไฟล์ส่วนตัว: {user.get('is_private', 'N/A')}")
                    
                except Exception as e:
                    print(f"⚠️ ไม่สามารถแปลง JSON: {e}")
            
            print("\\n🎉 ดึงข้อมูลสำเร็จ!")
            return True
            
        elif response.status_code == 429:
            print("❌ IP ถูกบล็อค (Rate Limited)")
            print("💡 ลองใช้ VPN หรือรอ 24 ชั่วโมง")
            
        elif response.status_code == 401:
            print("❌ Session หมดอายุ")
            print("💡 สร้าง session ใหม่ด้วย create_session.py")
            
        else:
            print(f"❌ เกิดข้อผิดพลาด: HTTP {response.status_code}")
        
        return False
        
    except Exception as e:
        print(f"❌ ข้อผิดพลาดการเชื่อมต่อ: {e}")
        return False

if __name__ == "__main__":
    success = extract_alx_trading()
    
    if not success:
        print("\\n🔧 วิธีแก้ปัญหา:")
        print("1. ใช้ VPN เปลี่ยน IP")
        print("2. สร้าง session ใหม่: python3 create_session.py")
        print("3. รอ 24 ชั่วโมงแล้วลองใหม่")
'''
    
    with open("easy_alx_extractor.py", "w", encoding='utf-8') as f:
        f.write(extractor_content)
    
    print("📁 สร้าง extractor ง่ายๆ: easy_alx_extractor.py")

def main():
    print("🇹🇭 คู่มือแก้ปัญหา Instagram DM Extraction")
    print("=" * 60)
    
    show_solution()
    create_session_helper() 
    create_auto_extractor()
    
    print("\n🎯 สรุป - ทำตามขั้นตอนนี้:")
    print("=" * 40)
    print("1️⃣ รัน: python3 create_session.py")
    print("2️⃣ ใส่ sessionid จากเบราว์เซอร์")
    print("3️⃣ รัน: python3 easy_alx_extractor.py")
    print("4️⃣ ตรวจสอบไฟล์ที่ได้")
    
    print("\n✨ หรือถ้ามี VPN:")
    print("1️⃣ เปิด VPN")
    print("2️⃣ รัน: python3 easy_alx_extractor.py")
    
    print("\n🎉 เสร็จแล้ว! ระบบพร้อมใช้งาน")

if __name__ == "__main__":
    main()
