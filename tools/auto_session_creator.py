# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🤖 Auto Session Creator - Using Browser Automation
สร้าง Instagram session ใหม่โดยอัตโนมัติ
"""

import asyncio
import json
import time
from datetime import datetime
from playwright.async_api import async_playwright
import os
import requests

async def create_automated_session():
    """สร้าง session โดยอัตโนมัติ"""
    print("🤖 Auto Session Creator")
    print("=" * 50)

    # ตรวจสอบ Playwright
    try:
        playwright = await async_playwright().start()
        print("✅ Playwright ready")
    except Exception as e:
        print(f"❌ Playwright error: {e}")
        print("💡 Try: pip install playwright && playwright install")
        return None

    browser = None
    context = None

    try:
        # Launch browser - ใช้ headless mode สำหรับ codespace
        print("🌐 Launching browser...")
        browser = await playwright.chromium.launch(
            headless=True,  # ใช้ headless mode ใน codespace
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        )

        # Create context with realistic settings
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1366, 'height': 768},
            locale='en-US',
            timezone_id='America/New_York'
        )

        page = await context.new_page()

        # Navigate to Instagram
        print("📱 Opening Instagram...")
        await page.goto('https://www.instagram.com/', timeout=30000)
        await page.wait_for_load_state('networkidle')

        print("🔐 MANUAL LOGIN REQUIRED")
        print("=" * 50)
        print("👆 Please login to Instagram in the browser window")
        print("⏳ Waiting for you to complete login...")
        print("📝 After login, press Enter here to continue")

        # Wait for user to login manually
        input("\n🔑 Press Enter after you've logged in successfully...")

        # Wait a bit for page to stabilize
        await asyncio.sleep(3)

        # Extract cookies
        print("\n🍪 Extracting session cookies...")
        cookies = await context.cookies()

        instagram_cookies = {}
        for cookie in cookies:
            if 'instagram.com' in cookie.get('domain', ''):
                instagram_cookies[cookie['name']] = cookie['value']

        sessionid = instagram_cookies.get('sessionid')
        csrftoken = instagram_cookies.get('csrftoken', 'missing')

        if not sessionid:
            print("❌ No sessionid found in cookies")
            return None

        print(f"✅ Session ID extracted: {sessionid[:20]}...")
        print(f"✅ CSRF Token: {csrftoken[:20]}...")

        # Test the session
        session_data = {
            'sessionid': sessionid,
            'csrftoken': csrftoken,
            'all_cookies': instagram_cookies
        }

        return session_data

    except Exception as e:
        print(f"❌ Browser automation error: {e}")
        return None

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        await playwright.stop()

def test_extracted_session(session_data):
    """ทดสอบ session ที่ได้จาก browser"""
    print("\n🧪 Testing extracted session...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": session_data['csrftoken'],
        "Cookie": f"sessionid={session_data['sessionid']}; csrftoken={session_data['csrftoken']};"
    }

    # Test current user endpoint
    print("📱 Testing Current User API...")
    try:
        response = requests.get(
            "https://i.instagram.com/api/v1/accounts/current_user/",
            headers=headers,
            timeout=15
        )

        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if 'user' in data:
                user = data['user']
                user_info = {
                    'username': user.get('username', 'Unknown'),
                    'full_name': user.get('full_name', 'Unknown'),
                    'user_id': str(user.get('pk', 'Unknown'))
                }
                print(f"   ✅ SUCCESS!")
                print(f"   👤 Username: {user_info['username']}")
                print(f"   📝 Full Name: {user_info['full_name']}")

                return True, user_info
            else:
                print(f"   ❌ No user data in response")
        else:
            print(f"   ❌ API Error: {response.status_code}")

    except Exception as e:
        print(f"   ❌ Request failed: {e}")

    return False, {}

def save_session(session_data, user_info):
    """บันทึก session ที่ใช้งานได้"""
    final_session = {
        "sessionid": session_data['sessionid'],
        "csrftoken": session_data['csrftoken'],
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "cookies": session_data['all_cookies'],
        "user_info": user_info,
        "created_at": datetime.now().isoformat(),
        "method": "browser_automation",
        "status": "verified_working"
    }

    output_file = "/workspaces/sugarglitch-realops/tools/session_alx_trading.json"

    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_session, f, indent=2, ensure_ascii=False)

        # Backup
        timestamp = int(datetime.now().timestamp())
        backup_file = f"/workspaces/sugarglitch-realops/tools/session_backup_{timestamp}.json"
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(final_session, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Session saved:")
        print(f"   Main: {output_file}")
        print(f"   Backup: {backup_file}")

        return True

    except Exception as e:
        print(f"\n❌ Save failed: {e}")
        return False

async def main():
    print("🚀 Starting automated session creation...")
    print("⚠️  IMPORTANT: Browser window will open")
    print("   You need to login manually when it opens")

    # Get session through browser automation
    session_data = await create_automated_session()

    if not session_data:
        print("\n❌ Failed to extract session from browser")
        print("💡 Try the manual method instead:")
        print("   python3 tools/simple_session_generator.py")
        return

    # Test the extracted session
    is_valid, user_info = test_extracted_session(session_data)

    if is_valid:
        print("\n🎉 Session is working!")

        # Save it
        if save_session(session_data, user_info):
            print("\n✅ Fresh session created successfully!")
            print("\n🎯 Next steps:")
            print("1. Run: python3 tools/simple_dm_test.py")
            print("2. If successful: Run your DM extractors")
        else:
            print("\n❌ Failed to save session")
    else:
        print("\n❌ Extracted session is not working")
        print("💡 Try logging out and back in, then run this script again")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Process cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
