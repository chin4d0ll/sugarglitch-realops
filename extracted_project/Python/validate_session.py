#!/usr/bin/env python3
"""
🔒 ตัวตรวจสอบ Session สำหรับการทดสอบที่มีจริยธรรม
ตรวจสอบ Instagram session ของคุณเองสำหรับการวิจัยความปลอดภัย
"""

import json
import requests
import sys

def load_session():
    """โหลด session จาก session.json"""
    try:
        with open('session.json', 'r') as f:
            data = json.load(f)
            return data.get('sessionid', '')
    except FileNotFoundError:
        print("❌ ไม่พบไฟล์ session.json!")
        print("💡 สร้างจาก session_template.json")
        return None
    except json.JSONDecodeError:
        print("❌ JSON ไม่ถูกต้องใน session.json")
        return None

def validate_session(session_id):
    """ตรวจสอบว่า session ID ทำงานได้หรือไม่ (สำหรับการทดสอบที่มีจริยธรรมเท่านั้น)"""
    if not session_id or len(session_id) < 10:
        print("❌ รูปแบบ session ID ไม่ถูกต้อง")
        return False
    
    if session_id == "SESSION_ID_บัญชีทดสอบของคุณ_ใส่ตรงนี้":
        print("❌ กรุณาแทนที่ด้วย session ID บัญชีทดสอบจริงของคุณ")
        print("📖 ดูคำแนะนำใน ETHICAL_TESTING_GUIDE.md")
        return False
    
    if session_id == "8675309-real-session-id-here-5551212":
        print("❌ นี่คือ session ID ตัวอย่าง")
        print("📖 กรุณาใช้ session ID บัญชีทดสอบของคุณเอง")
        return False
    
    # ตรวจสอบรูปแบบพื้นฐาน
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15',
        'Cookie': f'sessionid={session_id}'
    }
    
    try:
        print("🔍 กำลังตรวจสอบ session กับ Instagram...")
        response = requests.get('https://www.instagram.com/', headers=headers, timeout=10)
        
        if 'login' in response.url.lower():
            print("❌ Session ดูเหมือนจะไม่ถูกต้องหรือหมดอายุ")
            return False
        elif response.status_code == 200:
            print("✅ Session ดูเหมือนจะถูกต้อง!")
            return True
        else:
            print(f"⚠️ สถานะการตอบกลับที่ไม่คาดคิด: {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ ข้อผิดพลาดเครือข่าย: {e}")
        return False

def main():
    print("🔒 ตัวตรวจสอบ Session ของ SugarGlitch")
    print("=" * 50)
    print("⚠️  สำหรับการทดสอบที่มีจริยธรรมเท่านั้น!")
    print("📖 ใช้เฉพาะกับบัญชีทดสอบของคุณเอง")
    print("=" * 50)
    
    session_id = load_session()
    if not session_id:
        return 1
    
    if validate_session(session_id):
        print("✅ Session พร้อมสำหรับการทดสอบที่มีจริยธรรม!")
        print("🚀 คุณสามารถรันได้แล้ว: python main.py")
        return 0
    else:
        print("❌ กรุณาตรวจสอบ session ID ของคุณ")
        print("📖 ดู ETHICAL_TESTING_GUIDE.md เพื่อขอความช่วยเหลือ")
        return 1

if __name__ == "__main__":
    sys.exit(main())
