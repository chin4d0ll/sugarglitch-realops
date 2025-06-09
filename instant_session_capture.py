# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Instagram Login Session Capture
จับ sessionid ขณะ login สำเร็จ - ไม่ต้อง bruteforce
"""

import json
import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
import asyncio

class InstagramLoginCapture:
    def __init__(self):
        self.session_file = "tools/session_alx_trading.json"
        self.target_username = "alx.trading"
        self.captured_session = None

    def setup_browser(self, playwright):
        """ตั้งค่า browser สำหรับจับ session"""
        browser = playwright.chromium.launch(
            headless = False,  # แสดง browser
            args=[
                '--disable-web-security',
                '--disable-features = VizDisplayCompositor',
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ]
        )

        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1280, 'height': 720}
        )

        return browser, context

    def capture_cookies_on_login(self, page):
        """จับ cookies เมื่อ login สำเร็จ"""
        print("🔍 กำลังรอการ login...")

        # รอให้ login สำเร็จ (เช็คจาก URL หรือ element)
        try:
            # รอให้เข้าสู่หน้าหลักของ Instagram
            page.wait_for_url("**/", timeout = 60000)  # รอ 60 วินาที

            # ตรวจสอบว่า login สำเร็จแล้ว
            if "instagram.com" in page.url and "login" not in page.url:
                print("✅ Login สำเร็จ! กำลังจับ session...")

                # ดึง cookies ทั้งหมด
                cookies = page.context.cookies()

                session_data = {}
                for cookie in cookies:
                    if cookie['name'] in ['sessionid', 'csrftoken', 'ds_user_id', 'mid', 'ig_did']:
                        session_data[cookie['name']] = cookie['value']

                if 'sessionid' in session_data:
                    self.captured_session = session_data
                    print(f"🎉 จับ sessionid สำเร็จ: {session_data['sessionid'][:20]}...")
                    return True
                else:
                    print("❌ ไม่พบ sessionid ใน cookies")
                    return False
            else:
                print("❌ ยังไม่ได้ login หรือ login ไม่สำเร็จ")
                return False

        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
            return False

    def save_captured_session(self):
        """บันทึก session ที่จับได้"""
        if not self.captured_session:
            return False

        session_info = {
            'sessionid': self.captured_session.get('sessionid', ''),
            'csrftoken': self.captured_session.get('csrftoken', ''),
            'ds_user_id': self.captured_session.get('ds_user_id', ''),
            'mid': self.captured_session.get('mid', ''),
            'ig_did': self.captured_session.get('ig_did', ''),
            'target': self.target_username,
            'created_at': datetime.now().isoformat(),
            'status': 'active',
            'capture_method': 'login_intercept'
        }

        os.makedirs('tools', exist_ok = True)

        try:
            with open(self.session_file, 'w') as f:
                json.dump(session_info, f, indent = 2)
            print(f"✅ บันทึก session ไปที่ {self.session_file}")
            return True
        except Exception as e:
            print(f"❌ ไม่สามารถบันทึก session: {e}")
            return False

    def auto_capture_mode(self):
        """โหมดจับ session อัตโนมัติ"""
        print("\n" + "="*60)
        print("🎯 AUTO SESSION CAPTURE MODE")
        print("="*60)
        print("การทำงาน:")
        print("1. เปิด Instagram ใน browser")
        print("2. คุณ login ด้วยตนเอง")
        print("3. เมื่อ login สำเร็จ จะจับ sessionid อัตโนมัติ")
        print("4. บันทึก session และใช้งานได้ทันที")
        print()

        with sync_playwright() as playwright:
            browser, context = self.setup_browser(playwright)
            page = context.new_page()

            try:
                print("🌐 เปิด Instagram...")
                page.goto("https://www.instagram.com/accounts/login/")

                print("📱 กรุณา login ใน browser ที่เปิดขึ้นมา...")
                print("⏳ รอการ login... (กด Ctrl+C เพื่อยกเลิก)")

                # ลูปรอการ login
                login_success = False
                for attempt in range(120):  # รอสูงสุด 2 นาที
                    try:
                        current_url = page.url

                        # เช็คว่า login สำเร็จหรือยัง
                        if ("instagram.com" in current_url and
                            "login" not in current_url and
                            "accounts" not in current_url):

                            print("✅ ตรวจพบการ login สำเร็จ!")

                            # รอสักครู่ให้ cookies โหลดเสร็จ
                            time.sleep(2)

                            if self.capture_cookies_on_login(page):
                                login_success = True
                                break

                        time.sleep(1)  # เช็คทุกวินาที

                    except Exception as e:
                        print(f"⚠️ ข้อผิดพลาดขณะตรวจสอบ: {e}")
                        time.sleep(1)
                        continue

                if login_success:
                    if self.save_captured_session():
                        print("\n🎉 SUCCESS! Session จับและบันทึกเรียบร้อย!")
                        return True
                    else:
                        print("❌ จับ session ได้แต่บันทึกไม่สำเร็จ")
                        return False
                else:
                    print("❌ ไม่สามารถจับ session ได้ (login ไม่สำเร็จหรือหมดเวลา)")
                    return False

            except KeyboardInterrupt:
                print("\n⚠️ ผู้ใช้ยกเลิกการทำงาน")
                return False
            except Exception as e:
                print(f"❌ เกิดข้อผิดพลาด: {e}")
                return False
            finally:
                browser.close()

    def manual_intercept_mode(self):
        """โหมดจับ session แบบ manual"""
        print("\n" + "="*60)
        print("🔧 MANUAL SESSION INTERCEPT")
        print("="*60)
        print("วิธีการ:")
        print("1. เปิด Instagram ใน browser ปกติ")
        print("2. Login เสร็จแล้วเปิด Developer Tools (F12)")
        print("3. ไป Application > Cookies > instagram.com")
        print("4. คัดลอก sessionid มาใส่ที่นี่")
        print()

        sessionid = input("กรุณาใส่ sessionid: ").strip()

        if not sessionid:
            print("❌ ต้องมี sessionid")
            return False

        # เก็บ session data
        self.captured_session = {'sessionid': sessionid}

        # ถาม optional cookies
        print("\nCookies เพิ่มเติม (กด Enter เพื่อข้าม):")
        csrftoken = input("csrftoken: ").strip()
        if csrftoken:
            self.captured_session['csrftoken'] = csrftoken

        ds_user_id = input("ds_user_id: ").strip()
        if ds_user_id:
            self.captured_session['ds_user_id'] = ds_user_id

        return self.save_captured_session()

    def run(self):
        """เรียกใช้งานหลัก"""
        print("🚀 INSTAGRAM SESSION CAPTURE TOOL")
        print("="*60)
        print("จับ sessionid ขณะ login สำเร็จ - ไม่ต้อง bruteforce!")
        print()

        while True:
            print("เลือกโหมด:")
            print("1. Auto Capture (เปิด browser และจับ session อัตโนมัติ)")
            print("2. Manual Intercept (คัดลอก sessionid เอง)")
            print("3. ออกจากโปรแกรม")

            choice = input("\nเลือก (1-3): ").strip()

            if choice == '1':
                if self.auto_capture_mode():
                    print("\n🎉 เสร็จสิ้น! Session พร้อมใช้งาน")
                    print("ขั้นตอนถัดไป:")
                    print("1. เพิ่ม working proxies ใน config/proxies.json")
                    print("2. รัน DM extraction ด้วย tools/dm_extraction_with_interceptor.py")
                    break
                else:
                    print("❌ ไม่สำเร็จ กรุณาลองใหม่")

            elif choice == '2':
                if self.manual_intercept_mode():
                    print("\n✅ Session บันทึกเรียบร้อย!")
                    break
                else:
                    print("❌ ไม่สำเร็จ กรุณาลองใหม่")

            elif choice == '3':
                print("👋 ลาก่อน!")
                break

            else:
                print("❌ เลือกไม่ถูกต้อง")

if __name__ == "__main__":
    try:
        capture = InstagramLoginCapture()
        capture.run()
    except KeyboardInterrupt:
        print("\n\n⚠️ ผู้ใช้ยกเลิกการทำงาน")
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {e}")
