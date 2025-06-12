# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
from playwright.sync_api import sync_playwright
import time

BROWSER_WS = "wss://brd-customer-hl_63f0835e-zone-scraping_browser4:1pncg92uga2s@brd.superproxy.io:9222"
INSTAGRAM_URL = "https://www.instagram.com/"
USERNAME = "Alx.trading>"  # ใส่ username ของคุณ
PASSWORD = "<Fleming654>"  # ใส่ password ของคุณ

def login_and_get_dms():
    with sync_playwright() as p:
        print("Connecting to Bright Data Browser API via Playwright...")
        browser = p.chromium.connect_over_cdp(BROWSER_WS)
        page = browser.new_page()
        page.goto(INSTAGRAM_URL)
        # รอ input username/password ให้พร้อม
        page.wait_for_selector('input[name="username"]', timeout=60000)
        page.wait_for_selector('input[name="password"]', timeout=60000)
        time.sleep(1)
        # กรอก username/password
        page.fill('input[name="username"]', USERNAME)
        page.fill('input[name="password"]', PASSWORD)
        page.click('button[type="submit"]')
        print("🔑 Logging in...")
        # รอ login สำเร็จหรือ error
        try:
            page.wait_for_url("https://www.instagram.com/", timeout=60000)
            print("✅ Login success!")
        except Exception as e:
            # ตรวจสอบ error message
            error_text = ""
            try:
                error_box = page.query_selector('div[role="alert"]')
                if error_box:
                    error_text = error_box.inner_text()
            except Exception:
                pass
            print(f"❌ Login failed: {e} {error_text}")
            browser.close()
            return
        # ข้าม popups (ถ้ามี)
        for _ in range(2):
            try:
                page.click('text=Not Now', timeout=5000)
            except Exception:
                pass
        # ไปหน้า DMs
        page.goto("https://www.instagram.com/direct/inbox/")
        print("📥 Navigated to DMs inbox!")
        page.screenshot(path="ig_dm_inbox.png")
        print("✅ Screenshot saved as ig_dm_inbox.png")
        # ดึงรายชื่อแชท (ตัวอย่าง)
        time.sleep(5)  # รอให้แชทโหลด
        chat_items = page.query_selector_all('div[role="row"]')
        dms = []
        for chat in chat_items:
            try:
                user = chat.query_selector('div[dir="auto"] span')
                username = user.inner_text() if user else "(unknown)"
                preview = chat.inner_text()
                dms.append({"username": username, "preview": preview})
            except Exception as e:
                continue
        # export DM preview เป็น JSON
        import json
        with open("ig_dm_preview.json", "w", encoding="utf-8") as f:
            json.dump(dms, f, ensure_ascii=False, indent=2)
        print(f"✅ Exported DM preview to ig_dm_preview.json ({len(dms)} chats)")
        browser.close()

if __name__ == "__main__":
    login_and_get_dms()
