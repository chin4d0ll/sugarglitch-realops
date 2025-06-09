# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Real-time Session Interceptor
Captures Instagram sessionid immediately when login succeeds
"""

import os
import json
import time
import sys
from datetime import datetime
from playwright.sync_api import sync_playwright
import requests

class RealtimeSessionInterceptor:
    def __init__(self):
        self.target_username = "alx.trading"
        self.session_file = "tools/session_alx_trading.json"
        self.captured_session = None

        # Ensure directories exist
        os.makedirs("tools", exist_ok=True)
        os.makedirs("logs", exist_ok=True)

    def capture_session_on_login(self):
        """Capture session data immediately when login succeeds"""
        print("🚀 REAL-TIME SESSION INTERCEPTOR")
        print("="*50)
        print("This will open Instagram and capture session when you login")
        print("Please follow the instructions carefully...")

        with sync_playwright() as p:
            # Launch browser with visible UI
            browser = p.chromium.launch(
                headless=False,
                args=[
                    '--no-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor'
                ]
            )

            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )

            page = context.new_page()

            # Set up request/response interceptor
            def handle_response(response):
                if 'instagram.com' in response.url:
                    # Check for successful login indicators
                    if any(endpoint in response.url for endpoint in ['/api/v1/web/accounts/login/ajax/', '/accounts/login/ajax/']):
                        if response.status == 200:
                            print("✅ Login request detected!")
                            self.extract_session_from_context(context)

            page.on('response', handle_response)

            try:
                print("\n📱 Opening Instagram...")
                page.goto('https://www.instagram.com/accounts/login/')

                print("\n🔑 Please login manually in the browser window that opened")
                print("After successful login, I'll automatically capture your session")
                print("Press Ctrl+C here when session is captured or to exit")

                # Wait for login and monitor for session
                timeout_seconds = 300  # 5 minutes
                start_time = time.time()

                while time.time() - start_time < timeout_seconds:
                    # Check if we're on a logged-in page
                    current_url = page.url
                    if 'instagram.com' in current_url and '/accounts/login' not in current_url:
                        if self.extract_session_from_context(context):
                            print("🎉 Session captured successfully!")
                            break

                    time.sleep(2)
                else:
                    print("⏰ Timeout reached")

            except KeyboardInterrupt:
                print("\n🛑 Interrupted by user")
            finally:
                browser.close()

        return self.captured_session

    def extract_session_from_context(self, context):
        """Extract session data from browser context"""
        try:
            cookies = context.cookies()
            session_data = {}

            for cookie in cookies:
                if cookie['domain'] in ['.instagram.com', 'www.instagram.com', 'instagram.com']:
                    if cookie['name'] in ['sessionid', 'csrftoken', 'ds_user_id', 'mid', 'ig_did']:
                        session_data[cookie['name']] = cookie['value']

            if 'sessionid' in session_data:
                print(f"✅ Found sessionid: {session_data['sessionid'][:20]}...")

                # Test the session immediately
                if self.test_session_validity(session_data):
                    self.captured_session = session_data
                    self.save_session(session_data)
                    return True
                else:
                    print("❌ Captured session is not valid")

        except Exception as e:
            print(f"❌ Error extracting session: {e}")

        return False

    def test_session_validity(self, session_data):
        """Quick test to verify session works"""
        print("🔍 Testing captured session...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Cookie': '; '.join([f"{k}={v}" for k, v in session_data.items()])
        }

        try:
            response = requests.get('https://www.instagram.com/', headers=headers, timeout=10)

            if response.status_code == 200 and 'login' not in response.url.lower():
                print("✅ Session is valid!")
                return True
            else:
                print("❌ Session test failed")
                return False

        except Exception as e:
            print(f"❌ Session test error: {e}")
            return False

    def save_session(self, session_data):
        """Save captured session"""
        session_info = {
            'sessionid': session_data.get('sessionid', ''),
            'csrftoken': session_data.get('csrftoken', ''),
            'ds_user_id': session_data.get('ds_user_id', ''),
            'mid': session_data.get('mid', ''),
            'ig_did': session_data.get('ig_did', ''),
            'target': self.target_username,
            'created_at': datetime.now().isoformat(),
            'status': 'active',
            'method': 'realtime_intercept'
        }

        try:
            with open(self.session_file, 'w') as f:
                json.dump(session_info, f, indent=2)
            print(f"💾 Session saved to {self.session_file}")
            return True
        except Exception as e:
            print(f"❌ Failed to save session: {e}")
            return False

def main():
    print("🎯 REAL-TIME INSTAGRAM SESSION INTERCEPTOR")
    print("="*60)
    print("This tool will capture your session immediately when you login")
    print("No bruteforce needed - just login normally!")
    print()

    interceptor = RealtimeSessionInterceptor()

    try:
        session = interceptor.capture_session_on_login()

        if session:
            print("\n🎉 SUCCESS! Session captured and saved!")
            print(f"📄 Session file: {interceptor.session_file}")
            print("\nNext steps:")
            print("1. Add working proxies to config/proxies.json")
            print("2. Run DM extraction with interceptor protection")
            return True
        else:
            print("\n❌ Failed to capture session")
            return False

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Operation cancelled")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
