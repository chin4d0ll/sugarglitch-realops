# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔑 Manual Session Input
รับ sessionid และ csrftoken จาก user แล้วสร้างไฟล์ session
"""

import json
import requests
from datetime import datetime
import os

def get_session_from_user():
    """รับ session จาก user"""
    print("🔑 Manual Instagram Session Creator")
    print("=" * 50)
    print("📱 วิธีการ:")
    print("1. เปิด Instagram ในเบราว์เซอร์")
    print("2. ล็อกอินเข้าบัญชีที่ต้องการ")
    print("3. เปิด Developer Tools (F12)")
    print("4. ไปที่ Application/Storage > Cookies > instagram.com")
    print("5. คัดลอก sessionid และ csrftoken")
    print("=" * 50)

    # รับข้อมูลจาก user
    sessionid = input("\n📋 ใส่ sessionid: ").strip()
    if not sessionid:
        print("❌ ต้องใส่ sessionid")
        return None, None

    csrftoken = input("📋 ใส่ csrftoken (หรือ Enter เพื่อข้าม): ").strip()
    if not csrftoken:
        csrftoken = "missing"

    return sessionid, csrftoken

def test_session(sessionid, csrftoken):
    """ทดสอบ session ที่ได้รับ"""
    print("\n🧪 ทดสอบ session...")

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrftoken,
        "Cookie": f"sessionid={sessionid}; csrftoken={csrftoken};"
    }

    # URLs ทดสอบ
    test_urls = [
        {
            "name": "Current User",
            "url": "https://i.instagram.com/api/v1/accounts/current_user/",
            "key": "user"
        },
        {
            "name": "DM Inbox",
            "url": "https://i.instagram.com/api/v1/direct_v2/inbox/?limit=10",
            "key": "inbox"
        }
    ]

    success_count = 0
    user_info = {}

    for test in test_urls:
        print(f"🌐 ทดสอบ: {test['name']}")

        try:
            response = requests.get(test['url'], headers=headers, timeout=15)
            print(f"📊 Status: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    if test['key'] in data:
                        print(f"✅ สำเร็จ!")
                        success_count += 1

                        # เก็บข้อมูล user
                        if test['key'] == 'user':
                            user_info = {
                                'username': data['user'].get('username', 'N/A'),
                                'full_name': data['user'].get('full_name', 'N/A'),
                                'user_id': data['user'].get('pk', 'N/A')
                            }
                            print(f"   👤 User: {user_info['username']}")
                            print(f"   📝 Name: {user_info['full_name']}")

                        elif test['key'] == 'inbox':
                            threads = data['inbox'].get('threads', [])
                            print(f"   💬 พบ {len(threads)} threads")
                    else:
                        print(f"⚠️ ไม่พบ key '{test['key']}'")
                        print(f"   Keys: {list(data.keys())}")

                except json.JSONDecodeError:
                    print(f"⚠️ Response ไม่ใช่ JSON")

            elif response.status_code in [400, 401, 403]:
                print(f"❌ ไม่มีสิทธิ์ - Session อาจผิดหรือหมดอายุ")

            elif response.status_code == 429:
                print(f"❌ Rate limited")

            else:
                print(f"⚠️ Status {response.status_code}")

        except Exception as e:
            print(f"❌ เชื่อมต่อไม่ได้: {e}")

    print(f"\n📊 ผลทดสอบ: {success_count}/2 สำเร็จ")

    return success_count >= 1, user_info

def save_session(sessionid, csrftoken, user_info):
    """บันทึก session ลงไฟล์"""
    session_data = {
        "sessionid": sessionid,
        "csrftoken": csrftoken,
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "cookies": {
            "sessionid": sessionid,
            "csrftoken": csrftoken
        },
        "user_info": user_info,
        "created": datetime.now().isoformat(),
        "method": "manual_input"
    }

    # ไฟล์หลัก
    output_file = "/workspaces/sugarglitch-realops/tools/session_alx_trading.json"

    try:
        # สร้างโฟลเดอร์ถ้ายังไม่มี
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # บันทึกไฟล์หลัก
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)

        # สำรองไฟล์
        timestamp = int(datetime.now().timestamp())
        backup_file = f"/workspaces/sugarglitch-realops/tools/session_backup_{timestamp}.json"
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)

        print(f"\n✅ บันทึกแล้ว: {output_file}")
        print(f"💾 สำรอง: {backup_file}")

        return True

    except Exception as e:
        print(f"\n❌ ไม่สามารถบันทึกไฟล์: {e}")
        return False

def main():
    print("🚀 เริ่มสร้าง Fresh Instagram Session...")

    # รับ session จาก user
    sessionid, csrftoken = get_session_from_user()
    if not sessionid:
        print("❌ ต้องมี sessionid")
        return

    # ทดสอบ session
    is_valid, user_info = test_session(sessionid, csrftoken)

    if not is_valid:
        print("\n❌ Session ไม่ถูกต้องหรือไม่สามารถใช้งานได้")
        print("💡 กรุณาตรวจสอบ sessionid/csrftoken อีกครั้ง")
        return

    # บันทึก session
    if save_session(sessionid, csrftoken, user_info):
        print("\n🎉 สร้าง Fresh Session สำเร็จ!")
        print("\n📋 ขั้นตอนต่อไป:")
        print("1. รัน: python3 tools/simple_dm_test.py")
        print("2. หากสำเร็จ จะแสดง '✅ Request succeeded!'")
        print("3. จากนั้นสามารถรัน DM extractor ได้")
    else:
        print("\n❌ ไม่สามารถบันทึก session")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 ยกเลิกโดยผู้ใช้")
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {e}")
