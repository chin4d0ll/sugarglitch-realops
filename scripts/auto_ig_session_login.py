# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_PATH = "tools/session_alx_trading.json"

async def ig_login_and_get_sessionid(username, password):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.instagram.com/accounts/login/")
        await page.wait_for_selector("input[name='username']")
        await page.fill("input[name='username']", username)
        await page.fill("input[name='password']", password)
        await page.click("button[type='submit']")
        # Wait for either error or main page
        try:
            await page.wait_for_selector("nav, [data-testid='user-avatar']", timeout=15000)
        except Exception:
            print("[ERROR] Login failed or took too long.")
            await browser.close()
            return None
        cookies = await context.cookies()
        sessionid = None
        for cookie in cookies:
            if cookie.get('name') == 'sessionid':
                sessionid = cookie.get('value')
        await browser.close()
        return sessionid, cookies

def save_session(sessionid, cookies):
    Path("tools").mkdir(exist_ok=True)
    data = {
        "sessionid": sessionid,
        "cookies": cookies
    }
    with open(OUTPUT_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[OK] sessionid saved to {OUTPUT_PATH}")

def main():
    import getpass
    print("=== IG Auto Login & Sessionid Extractor ===")
    username = input("IG Username: ").strip()
    password = getpass.getpass("IG Password: ")
    sessionid, cookies = asyncio.run(ig_login_and_get_sessionid(username, password))
    if sessionid:
        print(f"[SUCCESS] sessionid: {sessionid}")
        save_session(sessionid, cookies)
    else:
        print("[FAIL] Could not get sessionid. Check credentials or try again.")

if __name__ == "__main__":
    main()
