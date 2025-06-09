# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🎭 Enhanced Session Hijacker - Codespace Compatible
ใช้ Playwright ดึง sessionid แบบ headless mode สำหรับ codespace
"""

import json
import time
import os
from datetime import datetime
from playwright.sync_api import sync_playwright
import requests

class EnhancedSessionHijacker:
    def __init__(self):
        self.output_path = "/workspaces/sugarglitch-realops/tools/session_alx_trading.json"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    def capture_session_with_manual_input(self):
        """วิธีที่ 1: รับ cookies จาก user แล้วสร้าง session"""
        print("🔑 Enhanced Session Hijacker - Manual Input Mode")
        print("=" * 60)
        print("📱 INSTRUCTIONS:")
        print("1. Open Instagram in your browser")
        print("2. Login to your target account")
        print("3. Press F12 → Application → Cookies → instagram.com")
        print("4. Copy sessionid and csrftoken values")
        print("5. Paste them below")
        print("=" * 60)

        sessionid = input("\n🔑 Paste sessionid: ").strip()
        if not sessionid or len(sessionid) < 20:
            print("❌ Invalid sessionid")
            return False

        csrftoken = input("🛡️ Paste csrftoken (or Enter to skip): ").strip()
        if not csrftoken:
            csrftoken = "missing"

        # Test the session immediately
        print("\n🧪 Testing session...")
        if self.test_and_save_session(sessionid, csrftoken, "manual_input"):
            return True
        else:
            print("❌ Session test failed")
            return False

    def capture_session_with_headless_browser(self):
        """วิธีที่ 2: ใช้ headless browser (สำหรับ codespace)"""
        print("🤖 Enhanced Session Hijacker - Headless Mode")
        print("=" * 60)
        print("⚠️ This method needs manual login steps in external browser")
        print("📝 Follow the instructions carefully")

        try:
            with sync_playwright() as p:
                # Launch headless browser
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-dev-shm-usage'
                    ]
                )

                context = browser.new_context(
                    user_agent=self.user_agent,
                    viewport={'width': 1366, 'height': 768}
                )

                page = context.new_page()

                print("🌐 Navigating to Instagram...")
                page.goto("https://www.instagram.com/accounts/login/", timeout=30000)
                page.wait_for_load_state('networkidle')

                print("📋 MANUAL STEP REQUIRED:")
                print("1. Open Instagram in your browser: https://www.instagram.com/accounts/login/")
                print("2. Login to your account")
                print("3. After login, copy the full cookie string from Developer Tools")
                print("4. Format: sessionid=VALUE; csrftoken=VALUE; ...")

                cookie_string = input("\n🍪 Paste full cookie string: ").strip()

                if cookie_string and 'sessionid=' in cookie_string:
                    sessionid = self.extract_cookie_value(cookie_string, 'sessionid')
                    csrftoken = self.extract_cookie_value(cookie_string, 'csrftoken')

                    browser.close()

                    if sessionid:
                        print(f"✅ Extracted sessionid: {sessionid[:30]}...")
                        return self.test_and_save_session(sessionid, csrftoken or "missing", "headless_browser")

                browser.close()
                print("❌ Failed to extract valid sessionid")
                return False

        except Exception as e:
            print(f"❌ Browser automation error: {e}")
            return False

    def capture_session_with_curl_extraction(self):
        """วิธีที่ 3: ดึงจาก cURL command"""
        print("🌐 Enhanced Session Hijacker - cURL Mode")
        print("=" * 60)
        print("📋 INSTRUCTIONS:")
        print("1. Open Instagram in browser and login")
        print("2. Open Network tab (F12)")
        print("3. Refresh the page or navigate to any IG page")
        print("4. Find any request to i.instagram.com")
        print("5. Right-click → Copy → Copy as cURL")
        print("6. Paste the cURL command below")
        print("=" * 60)

        curl_command = input("\n📝 Paste cURL command: ").strip()

        if curl_command and 'sessionid=' in curl_command:
            sessionid = self.extract_from_curl(curl_command, 'sessionid=')
            csrftoken = self.extract_from_curl(curl_command, 'csrftoken=')

            if sessionid:
                print(f"✅ Extracted sessionid: {sessionid[:30]}...")
                return self.test_and_save_session(sessionid, csrftoken or "missing", "curl_extraction")

        print("❌ Failed to extract sessionid from cURL")
        return False

    def extract_cookie_value(self, cookie_string, name):
        """ดึงค่า cookie จาก string"""
        try:
            parts = cookie_string.split(';')
            for part in parts:
                if f'{name}=' in part:
                    return part.split(f'{name}=')[1].strip()
        except Exception:
            pass
        return None

    def extract_from_curl(self, curl_command, key):
        """ดึงค่าจาก cURL command"""
        try:
            if f'{key}' in curl_command:
                start = curl_command.find(key) + len(key)
                end = curl_command.find(';', start)
                if end == -1:
                    end = curl_command.find("'", start)
                if end == -1:
                    end = curl_command.find('"', start)
                if end == -1:
                    end = len(curl_command)

                value = curl_command[start:end].strip()
                return value if value else None
        except Exception:
            pass
        return None

    def test_and_save_session(self, sessionid, csrftoken, method):
        """ทดสอบและบันทึก session"""
        print(f"\n🧪 Testing session from {method}...")

        headers = {
            "User-Agent": self.user_agent,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrftoken,
            "Cookie": f"sessionid={sessionid}; csrftoken={csrftoken};"
        }

        # Test with Instagram API
        test_urls = [
            {
                "name": "Current User",
                "url": "https://i.instagram.com/api/v1/accounts/current_user/",
                "key": "user"
            },
            {
                "name": "DM Inbox",
                "url": "https://i.instagram.com/api/v1/direct_v2/inbox/?limit=5",
                "key": "inbox"
            }
        ]

        success_count = 0
        user_info = {}

        for test in test_urls:
            print(f"   🌐 Testing {test['name']}...")

            try:
                response = requests.get(test['url'], headers=headers, timeout=10)
                status = response.status_code

                print(f"      📊 Status: {status}")

                if status == 200:
                    try:
                        data = response.json()
                        if test['key'] in data:
                            print(f"      ✅ SUCCESS!")
                            success_count += 1

                            if test['key'] == 'user':
                                user = data['user']
                                user_info = {
                                    'username': user.get('username', 'Unknown'),
                                    'full_name': user.get('full_name', 'Unknown'),
                                    'user_id': str(user.get('pk', 'Unknown'))
                                }
                                print(f"      👤 Username: {user_info['username']}")

                            elif test['key'] == 'inbox':
                                threads = data['inbox'].get('threads', [])
                                print(f"      💬 Threads: {len(threads)}")
                        else:
                            print(f"      ⚠️ Missing {test['key']} key")
                    except Exception:
                        print(f"      ❌ Invalid JSON")
                elif status in [400, 401, 403]:
                    print(f"      ❌ Unauthorized")
                else:
                    print(f"      ❌ HTTP {status}")

            except Exception as e:
                print(f"      ❌ Error: {str(e)[:30]}...")

        print(f"\n📊 Test Results: {success_count}/2 passed")

        if success_count >= 1:
            # Save the working session
            session_data = {
                "sessionid": sessionid,
                "csrftoken": csrftoken,
                "user_agent": self.user_agent,
                "cookies": {
                    "sessionid": sessionid,
                    "csrftoken": csrftoken
                },
                "user_info": user_info,
                "created_at": datetime.now().isoformat(),
                "method": method,
                "status": "verified_working"
            }

            try:
                os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

                with open(self.output_path, 'w', encoding='utf-8') as f:
                    json.dump(session_data, f, indent=2, ensure_ascii=False)

                # Create backup
                timestamp = int(datetime.now().timestamp())
                backup_path = f"/workspaces/sugarglitch-realops/tools/session_backup_{timestamp}.json"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    json.dump(session_data, f, indent=2, ensure_ascii=False)

                print(f"\n💾 Session saved successfully!")
                print(f"   Main: {self.output_path}")
                print(f"   Backup: {backup_path}")
                print(f"   Username: {user_info.get('username', 'Unknown')}")

                return True

            except Exception as e:
                print(f"\n❌ Failed to save session: {e}")
                return False
        else:
            print("\n❌ Session test failed - not working")
            return False

    def run_enhanced_hijacker(self):
        """รันเครื่องมือหลัก"""
        print("🎭 Enhanced Session Hijacker")
        print("=" * 60)
        print("💡 Multiple methods to capture Instagram sessionid")
        print(f"🎯 Target file: {self.output_path}")

        methods = [
            ("1", "Manual Input", self.capture_session_with_manual_input),
            ("2", "Headless Browser", self.capture_session_with_headless_browser),
            ("3", "cURL Extraction", self.capture_session_with_curl_extraction)
        ]

        print("\n🔧 Available methods:")
        for num, name, _ in methods:
            print(f"   {num}. {name}")

        choice = input("\n📋 Choose method (1-3) or Enter for auto-try: ").strip()

        if choice in ['1', '2', '3']:
            # Run specific method
            _, name, method_func = methods[int(choice)-1]
            print(f"\n🚀 Running {name}...")
            return method_func()
        else:
            # Try all methods in order
            print("\n🔄 Trying all methods...")
            for num, name, method_func in methods:
                print(f"\n🚀 Trying Method {num}: {name}")
                if method_func():
                    print(f"✅ Success with {name}!")
                    return True
                else:
                    print(f"❌ {name} failed, trying next...")

            print("\n❌ All methods failed")
            return False

def main():
    hijacker = EnhancedSessionHijacker()

    try:
        success = hijacker.run_enhanced_hijacker()

        if success:
            print("\n🎉 Session hijack successful!")
            print("\n🎯 Next steps:")
            print("1. Run: python3 tools/simple_dm_test.py")
            print("2. If successful: Run DM extractors")
            print("\n🔧 Available extractors:")
            print("   python3 real_dm_extractor_fresh.py")
            print("   python3 enhanced_dm_extractor.py")
            print("   python3 final_dm_extractor.py")
        else:
            print("\n❌ Session hijack failed")
            print("💡 Try a different method or check your Instagram login")

    except KeyboardInterrupt:
        print("\n🛑 Session hijack cancelled")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
