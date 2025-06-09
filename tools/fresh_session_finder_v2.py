# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🎭 Fresh Session Finder - Instagram Session Hijack Tool
เปิด Playwright เพื่อให้เรา "ล็อกอินเอง" แล้วดึง sessionid กลับมาเก็บ
Based on Dreamy's suggestion for Session Hijack approach 💖
"""

from playwright.sync_api import sync_playwright
import json
import time
import os
import requests
from datetime import datetime

def capture_instagram_session(output_path="tools/session_alx_trading.json"):
    """
    เปิด Chromium แบบไม่ซ่อนหน้าจอ (headful) ให้เราเข้าสู่ระบบด้วยมือเอง
    แล้วดึง Cookie ที่ชื่อว่า 'sessionid' ออกมาเก็บเป็น JSON
    """
    print("🎭 Fresh Session Finder - Instagram Session Hijack")
    print("=" * 60)
    print("💖 Using Dreamy's Session Hijack approach!")
    print("🎯 Target: Get fresh sessionid for Instagram DM extraction")

    # สร้างโฟลเดอร์ถ้ายังไม่มี
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with sync_playwright() as p:
        print("\n🌐 Starting Playwright browser...")

        # 1. Launch Chromium - ปรับให้เหมาะกับ codespace
        try:
            # ลอง headful ก่อน (มี GUI)
            browser = p.chromium.launch(
                headless=False,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--start-maximized',
                    '--disable-dev-shm-usage'
                ]
            )
            print("✅ Browser launched in GUI mode")
        except Exception as e:
            print(f"⚠️ GUI mode failed: {e}")
            print("🔄 Trying headless mode...")
            # ถ้าไม่ได้ให้ใช้ headless
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-web-security'
                ]
            )
            print("✅ Browser launched in headless mode")
            print("📝 Note: You'll need to use manual session input method")

        # สร้าง context และ page
        context = browser.new_context(
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
        )
        page = context.new_page()

        try:
            # 2. ไปที่หน้า Login Instagram
            print("\n📱 Navigating to Instagram login page...")
            page.goto("https://www.instagram.com/accounts/login/", timeout=60000)

            print("\n" + "="*60)
            print("🔑 LOGIN INSTRUCTION")
            print("="*60)
            print("✨ โปรดล็อกอิน Instagram ให้เรียบร้อย")
            print("   (ผ่านเบราว์เซอร์ที่เปิดขึ้นมานี้)")
            print("")
            print("📋 Steps:")
            print("1. กรอก username และ password")
            print("2. รอให้หน้าโหลดเสร็จ (เข้าสู่หน้าหลัก)")
            print("3. หลังล็อกอินสำเร็จ ให้รอ 5-10 วินาที")
            print("4. กลับมากด Enter ใน Terminal นี้")
            print("")
            print("⚠️  สำคัญ: อย่าปิดเบราว์เซอร์จนกว่าจะเห็นข้อความสำเร็จ!")
            print("="*60)

            # 3. รอให้เรา Login ด้วยมือ
            input("\n🔑 กด Enter เมื่อคุณล็อกอินเสร็จแล้ว (ห้ามปิดเบราว์เซอร์): ")

            # 4. พักรอสักครู่ให้ Cookie เสร็จสมบูรณ์
            print("\n⏳ รอ 5 วินาทีให้ Cookie ตั้งค่าเรียบร้อย...")
            time.sleep(5)

            # 5. ดึง Cookie name='sessionid' จาก Context
            print("🍪 กำลังดึง Cookies...")
            cookies = context.cookies()

            # หา sessionid cookie
            session_cookie = None
            csrf_cookie = None
            all_ig_cookies = {}

            for c in cookies:
                if "instagram.com" in c.get("domain", ""):
                    all_ig_cookies[c["name"]] = c["value"]

                    if c["name"] == "sessionid":
                        session_cookie = c
                    elif c["name"] == "csrftoken":
                        csrf_cookie = c

            print(f"📊 พบ Instagram cookies: {len(all_ig_cookies)} ตัว")
            print(f"   Cookies: {list(all_ig_cookies.keys())}")

            if not session_cookie:
                print("\n❌ ไม่พบ Cookie ชื่อ 'sessionid'")
                print("💡 แนะนำ:")
                print("   - ลองล็อกอินใหม่แล้วรออีก 10 วินาที")
                print("   - ตรวจสอบว่าล็อกอินสำเร็จจริง (ไม่มี error)")
                print("   - ลองเปลี่ยนเบราว์เซอร์หรือล้าง cache")
                return False
            else:
                # 6. เตรียม JSON เก็บข้อมูล session
                print(f"\n✅ พบ sessionid: {session_cookie['value'][:30]}...")

                result = {
                    "sessionid": session_cookie["value"],
                    "csrftoken": csrf_cookie["value"] if csrf_cookie else "missing",
                    "user_agent": context.user_agent or page.evaluate("() => navigator.userAgent"),
                    "cookies": all_ig_cookies,
                    "created_at": datetime.now().isoformat(),
                    "method": "playwright_session_hijack",
                    "status": "extracted"
                }

                # 7. ทดสอบ session ก่อนเซฟ
                print("\n🧪 ทดสอบ session ที่ได้...")
                if test_session_validity(result):
                    result["status"] = "verified_working"

                    # 8. เซฟลงไฟล์
                    with open(output_path, "w", encoding="utf-8") as f:
                        json.dump(result, f, indent=2, ensure_ascii=False)

                    # สร้าง backup
                    timestamp = int(time.time())
                    backup_path = f"tools/session_backup_{timestamp}.json"
                    with open(backup_path, "w", encoding="utf-8") as f:
                        json.dump(result, f, indent=2, ensure_ascii=False)

                    print(f"\n🎉 เซฟ session เก็บไว้ที่: {output_path}")
                    print(f"💾 สำรอง: {backup_path}")
                    print(f"🔑 SessionID ที่ได้: {result['sessionid'][:30]}... (ยาวรวม {len(result['sessionid'])} ตัวอักษร)")
                    print(f"🔒 CSRF Token: {result['csrftoken'][:20]}...")
                    print(f"📱 User-Agent: {result['user_agent'][:50]}...")
                    print(f"🍪 Total Cookies: {len(all_ig_cookies)}")

                    return True
                else:
                    print("❌ Session ไม่ valid - ลองล็อกอินใหม่")
                    return False

        except Exception as e:
            print(f"\n❌ เกิดข้อผิดพลาด: {e}")
            return False
        finally:
            # 8. ปิดเบราว์เซอร์
            print("\n🔄 ปิดเบราว์เซอร์...")
            browser.close()
            print("✅ เสร็จสิ้น!")

def test_session_validity(session_data):
    """ทดสอบความถูกต้องของ session"""
    headers = {
        "User-Agent": session_data["user_agent"],
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": session_data["csrftoken"],
        "Cookie": f"sessionid={session_data['sessionid']}; csrftoken={session_data['csrftoken']};"
    }

    try:
        response = requests.get(
            "https://i.instagram.com/api/v1/accounts/current_user/",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            if 'user' in data:
                username = data['user'].get('username', 'Unknown')
                print(f"   ✅ Session valid! Username: {username}")
                return True

        print(f"   ❌ Session test failed: HTTP {response.status_code}")
        return False

    except Exception as e:
        print(f"   ❌ Session test error: {e}")
        return False

def show_usage_instructions():
    """แสดงวิธีใช้งานต่อ"""
    print("\n" + "="*60)
    print("🎯 NEXT STEPS - ขั้นตอนต่อไป")
    print("="*60)

    print("1. 🧪 ทดสอบ session:")
    print("   python3 tools/simple_dm_test.py")
    print("   → ต้องเห็น '✅ Request succeeded!'")

    print("\n2. 🚀 รัน DM extractors:")
    print("   python3 real_dm_extractor_fresh.py")
    print("   python3 enhanced_dm_extractor.py")
    print("   python3 final_dm_extractor.py")

    print("\n3. 🔄 ถ้า session หมดอายุ:")
    print("   python3 tools/fresh_session_finder_v2.py")
    print("   → รันเครื่องมือนี้ใหม่เพื่อได้ session ใหม่")

    print("\n4. 📁 ไฟล์ที่ได้:")
    print("   tools/session_alx_trading.json - ไฟล์หลัก")
    print("   tools/session_backup_*.json - ไฟล์สำรอง")

    print("\n💡 Tips:")
    print("   - เก็บ session ไว้ใช้ได้หลายวัน")
    print("   - อย่าใช้ session เดียวกันหลายเครื่อง")
    print("   - ถ้า rate limit ให้รอ 1-2 ชั่วโมง")

if __name__ == "__main__":
    print("🚀 เริ่มต้น Fresh Session Finder")
    print("💖 Dreamy's Session Hijack Approach")

    try:
        # ถ้าอยากให้เปลี่ยน path เก็บ session ให้แก้ argument ตอนเรียกใช้
        success = capture_instagram_session()

        if success:
            print("\n🎉 SESSION HIJACK สำเร็จ!")
            show_usage_instructions()
        else:
            print("\n❌ SESSION HIJACK ไม่สำเร็จ")
            print("\n💡 ลองใช้วิธีอื่น:")
            print("   python3 tools/simple_session_generator.py")
            print("   python3 tools/quick_session_creator.py")

    except KeyboardInterrupt:
        print("\n\n🛑 ยกเลิกโดยผู้ใช้")
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {e}")
        import traceback
        traceback.print_exc()
