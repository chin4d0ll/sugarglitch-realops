# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
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
            except Exception:
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
        response = session.get(target_url, timeout = 15)

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
            json_match = re.search(r'window\._sharedData = ({.+?});', response.text)
            if json_match:
                try:
                    data = json.loads(json_match.group(1))

                    json_file = f"alx_trading_data_{timestamp}.json"
                    with open(json_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent = 2, ensure_ascii = False)

                    print(f"💾 บันทึก JSON: {json_file}")

                    # แสดงข้อมูลพื้นฐาน
                    if 'entry_data' in data:
                        entry_data = data['entry_data']
                        if 'ProfilePage' in entry_data:
                            profile = entry_data['ProfilePage'][0]
                            user = profile.get('graphql', {}).get('user', {})

                            print("\n👤 ข้อมูลบัญชี:")
                            print(f"   ชื่อผู้ใช้: {user.get('username', 'N/A')}")
                            print(f"   ชื่อเต็ม: {user.get('full_name', 'N/A')}")
                            print(f"   ผู้ติดตาม: {user.get('edge_followed_by', {}).get('count', 'N/A')}")
                            print(f"   กำลังติดตาม: {user.get('edge_follow', {}).get('count', 'N/A')}")
                            print(f"   โปรไฟล์ส่วนตัว: {user.get('is_private', 'N/A')}")

                except Exception as e:
                    print(f"⚠️ ไม่สามารถแปลง JSON: {e}")

            print("\n🎉 ดึงข้อมูลสำเร็จ!")
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
        print("\n🔧 วิธีแก้ปัญหา:")
        print("1. ใช้ VPN เปลี่ยน IP")
        print("2. สร้าง session ใหม่: python3 create_session.py")
        print("3. รอ 24 ชั่วโมงแล้วลองใหม่")
