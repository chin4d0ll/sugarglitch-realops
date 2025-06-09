# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Super Simple Session Capture
วิธีที่ง่ายที่สุดในการจับ sessionid หลัง login สำเร็จ
"""

import json
import os
from datetime import datetime

def simple_session_capture():
    """วิธีง่ายๆ ในการได้ sessionid"""
    print("🎯 SUPER SIMPLE SESSION CAPTURE")
    print("="*50)
    print()
    print("📋 ขั้นตอน (ง่ายมาก!):")
    print()
    print("1. เปิด Instagram ใน browser ปกติ")
    print("2. Login เสร็จแล้วกด F12")
    print("3. ไป Console แล้ววาง code นี้:")
    print()
    print("   " + "="*40)
    print("   document.cookie.split(';').find(c => c.includes('sessionid')).split('=')[1]")
    print("   " + "="*40)
    print()
    print("4. คัดลอกผลลัพธ์ที่ได้มาใส่ด้านล่าง")
    print()

    # รับ sessionid
    sessionid = input("🔑 ใส่ sessionid ที่ได้: ").strip()

    if not sessionid:
        print("❌ ต้องใส่ sessionid!")
        return False

    # บันทึก session
    session_data = {
        'sessionid': sessionid,
        'target': 'alx.trading',
        'created_at': datetime.now().isoformat(),
        'status': 'active',
        'capture_method': 'simple_manual'
    }

    os.makedirs('tools', exist_ok=True)
    session_file = 'tools/session_alx_trading.json'

    try:
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)

        print(f"✅ บันทึก session เรียบร้อย!")
        print(f"📁 ไฟล์: {session_file}")
        print(f"🔑 Session: {sessionid[:20]}...")

        return True

    except Exception as e:
        print(f"❌ บันทึกไม่ได้: {e}")
        return False

def create_bookmarklet():
    """สร้าง bookmarklet สำหรับจับ session"""
    bookmarklet_code = """
javascript:(function(){
    try {
        const sessionid = document.cookie.split(';').find(c => c.includes('sessionid'));
        if (sessionid) {
            const value = sessionid.split('=')[1];
            prompt('SessionID ของคุณ (คัดลอกไปใช้):', value);
        } else {
            alert('ไม่พบ sessionid - กรุณา login ก่อน');
        }
    } catch(e) {
        alert('เกิดข้อผิดพลาด: ' + e.message);
    }
})();
    """.strip()

    print("\n🔖 BOOKMARKLET (วิธีที่เร็วที่สุด)")
    print("="*50)
    print("1. คัดลอก code ด้านล่างนี้:")
    print()
    print(bookmarklet_code)
    print()
    print("2. ใน browser ให้สร้าง bookmark ใหม่")
    print("3. ใส่ code ด้านบนเป็น URL")
    print("4. เมื่อ login Instagram แล้วกด bookmark")
    print("5. จะแสดง sessionid ให้คัดลอก")

def auto_test_session(sessionid):
    """ทดสอบ session ว่าใช้งานได้หรือไม่"""
    import requests

    print(f"\n🔍 ทดสอบ session: {sessionid[:20]}...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Cookie': f'sessionid={sessionid}'
    }

    try:
        response = requests.get('https://www.instagram.com/', headers=headers, timeout=10)

        if response.status_code == 200:
            if 'login' in response.url.lower():
                print("❌ Session หมดอายุ")
                return False
            else:
                print("✅ Session ใช้งานได้!")
                return True
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ ทดสอบไม่ได้: {e}")
        return False

def main():
    print("🚀 INSTAGRAM SESSION CAPTURE TOOLKIT")
    print("="*60)
    print("เลือกวิธีที่ชอบ:")
    print()
    print("1. Simple Manual (ง่ายที่สุด)")
    print("2. Bookmarklet Code (เร็วที่สุด)")
    print("3. Exit")
    print()

    choice = input("เลือก (1-3): ").strip()

    if choice == '1':
        if simple_session_capture():
            print("\n🎉 สำเร็จ! ขั้นตอนถัดไป:")
            print("1. เพิ่ม proxies ใน config/proxies.json")
            print("2. รัน: python tools/dm_extraction_with_interceptor.py")
            print("3. ดู logs: tail -f logs/requests.log")

    elif choice == '2':
        create_bookmarklet()

    elif choice == '3':
        print("👋 ลาก่อน!")

    else:
        print("❌ เลือกไม่ถูกต้อง")

if __name__ == "__main__":
    main()
