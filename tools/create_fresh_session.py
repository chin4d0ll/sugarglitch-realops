# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🎭 Fresh Session Creator - สร้าง session ใหม่ด้วย Playwright
เนื่องจาก session ทั้งหมดหมดอายุแล้ว
"""

import asyncio
import json
import os
from datetime import datetime
from playwright.async_api import async_playwright
import time

class SessionCreator:
    def __init__(self):
        self.target = "alx.trading"
        self.output_file = "/workspaces/sugarglitch-realops/tools/session_alx_trading.json"

    async def create_fresh_session(self):
        """สร้าง session ใหม่ด้วย Playwright"""
        print("🎭 เริ่มสร้าง Fresh Session ด้วย Playwright...")

        playwright = await async_playwright().start()

        # เปิด browser (headless สำหรับ codespace)
        browser = await playwright.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding'
            ]
        )

        context = await browser.new_context(
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            viewport={'width': 375, 'height': 812},  # iPhone X size
            device_scale_factor=3,
            is_mobile=True,
            has_touch=True
        )

        page = await context.new_page()

        try:
            print("🌐 กำลังเปิด Instagram...")
            await page.goto("https://www.instagram.com/", wait_until="networkidle")

            print("📱 รอหน้าเว็บโหลด...")
            await page.wait_for_timeout(3000)

            # เช็คว่าต้อง login ไหม
            login_button = await page.query_selector('a[href="/accounts/login/"]')
            if login_button:
                print("🔑 ต้องล็อกอิน - คลิกที่ปุ่ม Login")
                await login_button.click()
                await page.wait_for_timeout(2000)

            # รอให้ผู้ใช้ล็อกอินเอง (ใน browser ที่เปิดอยู่)
            print("\n" + "="*60)
            print("📋 คำแนะนำสำหรับผู้ใช้:")
            print("1. ระบบจะเปิด browser ให้")
            print("2. กรุณาล็อกอินด้วยบัญชี Instagram ของคุณ")
            print("3. หลังล็อกอินสำเร็จ ระบบจะดึง cookies อัตโนมัติ")
            print("4. รอประมาณ 30 วินาที...")
            print("="*60)

            # รอให้ user ล็อกอิน (ใน production จริงจะต้องมีวิธีอื่น)
            # ตอนนี้เราจำลองด้วยการรอ
            await page.wait_for_timeout(30000)  # รอ 30 วินาที

            # ลองไปหน้า inbox เพื่อเช็คว่า login แล้วหรือยัง
            print("🔍 ตรวจสอบสถานะล็อกอิน...")
            await page.goto("https://www.instagram.com/direct/inbox/", wait_until="networkidle")

            current_url = page.url
            if "/accounts/login/" in current_url:
                print("❌ ยังไม่ได้ล็อกอิน - ต้องล็อกอินก่อน")
                return False

            if "/direct/inbox/" in current_url or "/direct/" in current_url:
                print("✅ ล็อกอินสำเร็จ!")

                # ดึง cookies
                cookies = await context.cookies()

                # สร้างข้อมูล session
                session_data = {
                    "sessionid": "",
                    "csrftoken": "",
                    "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15",
                    "cookies": {},
                    "created": datetime.now().isoformat(),
                    "method": "playwright_fresh",
                    "target": self.target
                }

                # แยก cookies สำคัญ
                for cookie in cookies:
                    session_data["cookies"][cookie["name"]] = cookie["value"]

                    if cookie["name"] == "sessionid":
                        session_data["sessionid"] = cookie["value"]
                    elif cookie["name"] == "csrftoken":
                        session_data["csrftoken"] = cookie["value"]

                # บันทึกไฟล์
                with open(self.output_file, 'w', encoding='utf-8') as f:
                    json.dump(session_data, f, indent=2)

                print(f"✅ บันทึก session ใหม่แล้ว: {self.output_file}")
                print(f"🍪 พบ cookies: {len(session_data['cookies'])} ตัว")
                print(f"🔑 Session ID: {session_data['sessionid'][:20]}...")

                return True
            else:
                print(f"⚠️ URL ไม่ถูกต้อง: {current_url}")
                return False

        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
            return False

        finally:
            await browser.close()
            await playwright.stop()

async def main():
    """สร้าง session ใหม่"""
    creator = SessionCreator()

    # ตรวจสอบว่ามี playwright ไหม
    try:
        playwright = await async_playwright().start()
        await playwright.stop()
        print("✅ Playwright พร้อมใช้งาน")
    except Exception as e:
        print(f"❌ Playwright ไม่พร้อม: {e}")
        print("💡 ติดตั้งด้วย: pip install playwright && playwright install chromium")
        return

    success = await creator.create_fresh_session()

    if success:
        print("\n🎉 สร้าง session ใหม่สำเร็จ!")
        print("🔄 ลองทดสอบด้วย: python3 tools/simple_dm_test.py")
    else:
        print("\n❌ สร้าง session ไม่สำเร็จ")
        print("💡 ต้องล็อกอินด้วยตนเองใน browser หรือใช้วิธีอื่น")

if __name__ == "__main__":
    asyncio.run(main())
