#!/usr/bin/env python3
"""
Thai Solution - ระบบสกัด DM อัตโนมัติ
Real-time session capture + DM extraction with interceptor
"""

import os
import json
import time
import sys
import requests
import subprocess
from datetime import datetime

class ThaiSolution:
    def __init__(self):
        self.target = "alx.trading"
        self.session_file = "tools/session_alx_trading.json"
        self.proxy_file = "config/proxies.json"
        self.log_file = "logs/requests.log"
        
        # สร้างโฟลเดอร์
        for folder in ["tools", "config", "logs", "extractions"]:
            os.makedirs(folder, exist_ok=True)
    
    def capture_session_realtime(self):
        """จับ sessionid แบบ real-time ตอน login สำเร็จ"""
        print("🚀 จับ SESSION แบบ REAL-TIME")
        print("="*40)
        print("จะรัน realtime session interceptor")
        
        try:
            script_path = "tools/realtime_session_interceptor.py"
            result = subprocess.run([sys.executable, script_path], 
                                 capture_output=False, text=True)
            return result.returncode == 0
        except Exception as e:
            print(f"❌ ข้อผิดพลาด: {e}")
            return False
    
    def setup_proxies(self):
        """ตั้งค่า proxies"""
        print("\n🔧 ตั้งค่า PROXIES")
        print("="*25)
        
        # รายการ proxy ฟรี
        free_proxies = [
            "http://173.245.49.63:80",
            "http://172.67.254.149:80",
            "http://188.114.97.8:80",
            "http://141.101.122.54:80",
            "http://104.21.48.84:80"
        ]
        
        print("ทดสอบ proxies...")
        working_proxies = []
        
        for proxy in free_proxies:
            try:
                response = requests.get(
                    'http://httpbin.org/ip',
                    proxies={'http': proxy, 'https': proxy},
                    timeout=5
                )
                if response.status_code == 200:
                    working_proxies.append(proxy)
                    print(f"✅ {proxy}")
                else:
                    print(f"❌ {proxy}")
            except:
                print(f"❌ {proxy}")
        
        # บันทึก proxies ที่ใช้งานได้
        with open(self.proxy_file, 'w') as f:
            json.dump(working_proxies, f, indent=2)
        
        print(f"💾 บันทึก {len(working_proxies)} proxies ที่ใช้งานได้")
        return len(working_proxies) > 0
    
    def run_dm_extraction(self):
        """รัน DM extraction ด้วย interceptor"""
        print("\n📱 สกัด DM ด้วย INTERCEPTOR")
        print("="*35)
        
        extractor_script = "tools/dm_extraction_with_interceptor.py"
        
        if not os.path.exists(extractor_script):
            print(f"❌ ไม่พบไฟล์ {extractor_script}")
            return False
        
        try:
            print("🚀 เริ่มสกัด DM...")
            result = subprocess.run([sys.executable, extractor_script], 
                                 capture_output=False, text=True)
            return result.returncode == 0
        except Exception as e:
            print(f"❌ ข้อผิดพลาด: {e}")
            return False
    
    def check_logs(self):
        """ตรวจสอบ logs"""
        print("\n📊 ตรวจสอบ LOGS")
        print("="*20)
        
        if not os.path.exists(self.log_file):
            print("❌ ไม่พบไฟล์ log")
            return
        
        try:
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
            
            print(f"📄 พบ {len(lines)} รายการ log")
            
            # แสดง log ล่าสุด
            if lines:
                print("\nLog ล่าสุด:")
                for line in lines[-5:]:
                    print(f"  {line.strip()}")
            
            # นับสถิติ
            total = len(lines)
            blocked = sum(1 for line in lines if any(code in line for code in ['429', '403', '401']))
            success = sum(1 for line in lines if '200' in line)
            
            print(f"\n📈 สถิติ:")
            print(f"  รวม: {total} requests")
            print(f"  สำเร็จ: {success}")
            print(f"  ถูกบล็อก: {blocked}")
            
        except Exception as e:
            print(f"❌ อ่าน log ไม่ได้: {e}")
    
    def run_complete_process(self):
        """รันกระบวนการทั้งหมด"""
        print("🎯 ระบบสกัด DM INSTAGRAM อัตโนมัติ")
        print("="*50)
        print("by Thai Solution - Real-time Session Capture")
        print()
        
        # เช็คสถานะปัจจุบัน
        session_exists = os.path.exists(self.session_file)
        proxy_exists = os.path.exists(self.proxy_file)
        
        print("📋 สถานะปัจจุบัน:")
        print(f"  Session: {'✅' if session_exists else '❌'}")
        print(f"  Proxies: {'✅' if proxy_exists else '❌'}")
        print()
        
        # ขั้นตอนที่ 1: จับ Session
        if not session_exists:
            print("🔑 ต้องการ Session ใหม่!")
            if input("จับ session ตอนนี้? (y/n): ").lower().startswith('y'):
                if not self.capture_session_realtime():
                    print("❌ จับ session ไม่สำเร็จ")
                    return False
        else:
            print("✅ มี Session แล้ว")
        
        # ขั้นตอนที่ 2: ตั้งค่า Proxies
        if not proxy_exists:
            print("\n🔧 ต้องการ Proxies!")
            if input("ตั้งค่า proxies ตอนนี้? (y/n): ").lower().startswith('y'):
                if not self.setup_proxies():
                    print("❌ ตั้งค่า proxies ไม่สำเร็จ")
                    return False
        else:
            print("✅ มี Proxies แล้ว")
        
        # ขั้นตอนที่ 3: สกัด DM
        print("\n🚀 พร้อมสกัด DM!")
        if input("เริ่มสกัด DM ตอนนี้? (y/n): ").lower().startswith('y'):
            self.run_dm_extraction()
        
        # ขั้นตอนที่ 4: ตรวจสอบผลลัพธ์
        self.check_logs()
        
        print("\n🎉 เสร็จสิ้นกระบวนการ!")
        print("ตรวจสอบโฟลเดอร์ extractions/ สำหรับผลลัพธ์")

def main():
    print("🇹🇭 THAI SOLUTION - INSTAGRAM DM EXTRACTOR")
    print("Real-time Session Capture + Auto Extraction")
    print("="*60)
    
    solution = ThaiSolution()
    
    try:
        solution.run_complete_process()
    except KeyboardInterrupt:
        print("\n\n🛑 ยกเลิกการทำงาน")
    except Exception as e:
        print(f"\n❌ ข้อผิดพลาด: {e}")

if __name__ == "__main__":
    main()
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
