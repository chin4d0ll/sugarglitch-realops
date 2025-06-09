# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Automated Fresh Session Extractor
Automatically captures and saves fresh Instagram session in JSON format
"""

import os
import json
import sys
import time
import requests
from datetime import datetime
from playwright.sync_api import sync_playwright
import threading
import signal

class AutoFreshSessionExtractor:
    def __init__(self):
        self.session_file = "tools/session_alx_trading.json"
        self.backup_dir = "sessions_fresh"
        self.target = "alx.trading"
        self.captured_session = None
        self.browser = None
        self.context = None
        self.page = None

        # Ensure directories exist
        os.makedirs("tools", exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)

    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(sig, frame):
            print("\n🛑 Shutting down gracefully...")
            self.cleanup()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def cleanup(self):
        """Clean up browser resources"""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
        except Exception:
            pass

    def validate_session(self, session_data):
        """Validate session by testing Instagram API"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        # Build cookie string
        cookies = []
        for key, value in session_data.items():
            if value and key in ['sessionid', 'csrftoken', 'ds_user_id', 'mid']:
                cookies.append(f"{key}={value}")

        if cookies:
            headers['Cookie'] = "; ".join(cookies)

        try:
            # Test main page
            response = requests.get('https://www.instagram.com/', headers=headers, timeout=10)

            if response.status_code == 200:
                if 'login' in response.url.lower() or '"is_logged_in":false' in response.text:
                    return False
                return True

        except Exception as e:
            print(f"❌ Validation error: {e}")

        return False

    def save_session(self, session_data):
        """Save session to JSON files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Main session data
        session_info = {
            'sessionid': session_data.get('sessionid', ''),
            'csrftoken': session_data.get('csrftoken', ''),
            'ds_user_id': session_data.get('ds_user_id', ''),
            'mid': session_data.get('mid', ''),
            'ig_did': session_data.get('ig_did', ''),
            'shbid': session_data.get('shbid', ''),
            'rur': session_data.get('rur', ''),
            'target': self.target,
            'created_at': datetime.now().isoformat(),
            'status': 'active',
            'extraction_method': 'automated_browser'
        }

        try:
            # Save main session file
            with open(self.session_file, 'w') as f:
                json.dump(session_info, f, indent=2)
            print(f"✅ Session saved to {self.session_file}")

            # Save backup with timestamp
            backup_file = f"{self.backup_dir}/session_{timestamp}.json"
            with open(backup_file, 'w') as f:
                json.dump(session_info, f, indent=2)
            print(f"✅ Backup saved to {backup_file}")

            # Save all cookies for debugging
            debug_file = f"{self.backup_dir}/all_cookies_{timestamp}.json"
            with open(debug_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            print(f"✅ Debug data saved to {debug_file}")

            return True

        except Exception as e:
            print(f"❌ Failed to save session: {e}")
            return False

    def extract_cookies_from_browser(self, page):
        """Extract all cookies from browser"""
        try:
            cookies = page.context.cookies()

            # Convert to dict
            cookie_dict = {}
            for cookie in cookies:
                if 'instagram.com' in cookie.get('domain', ''):
                    cookie_dict[cookie['name']] = cookie['value']

            return cookie_dict

        except Exception as e:
            print(f"❌ Failed to extract cookies: {e}")
            return {}

    def monitor_login_success(self, page):
        """Monitor for successful login"""
        print("🔍 Monitoring for login success...")

        max_attempts = 300  # 5 minutes timeout
        attempt = 0

        while attempt < max_attempts:
            try:
                current_url = page.url

                # Check if we're logged in
                if 'instagram.com' in current_url and 'login' not in current_url:
                    # Try to find logged-in indicators
                    try:
                        # Look for navigation elements that appear when logged in
                        if page.locator('[aria-label="Home"]').is_visible(timeout=1000):
                            print("✅ Login success detected!")
                            return True
                    except Exception:
                        pass

                    # Alternative check - look for user avatar or profile link
                    try:
                        if page.locator('[data-testid="user-avatar"]').is_visible(timeout=1000):
                            print("✅ Login success detected via avatar!")
                            return True
                    except Exception:
                        pass

                    # Check page content for logged-in state
                    try:
                        page_content = page.content()
                        if '"is_logged_in":true' in page_content or 'window._sharedData' in page_content:
                            print("✅ Login success detected via page content!")
                            return True
                    except Exception:
                        pass

                time.sleep(1)
                attempt += 1

                if attempt % 30 == 0:
                    print(f"⏳ Still waiting for login... ({attempt}/300)")

            except Exception as e:
                print(f"❌ Error monitoring login: {e}")
                time.sleep(1)
                attempt += 1

        print("⏰ Timeout waiting for login")
        return False

    def extract_session_headless(self):
        """Extract session using headless browser with manual intervention"""
        print("\n🤖 AUTOMATED SESSION EXTRACTION (HEADLESS)")
        print("="*60)

        try:
            with sync_playwright() as p:
                # Launch browser in headless mode
                self.browser = p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-dev-shm-usage']
                )

                self.context = self.browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )

                self.page = self.context.new_page()

                print("🌐 Loading Instagram...")
                self.page.goto('https://www.instagram.com/')

                print("\n📋 MANUAL LOGIN REQUIRED:")
                print("1. Open https://www.instagram.com/ in your regular browser")
                print("2. Log into your Instagram account")
                print("3. Copy the sessionid cookie value")
                print("4. Paste it when prompted below")

                # Get session manually
                sessionid = input("\n🔑 Paste your sessionid here: ").strip()

                if not sessionid:
                    print("❌ No sessionid provided")
                    return False

                # Test the session
                session_data = {'sessionid': sessionid}

                # Try to get additional cookies
                print("\n🍪 Getting additional cookies...")
                self.page.goto('https://www.instagram.com/')

                # Inject the sessionid
                self.context.add_cookies([{
                    'name': 'sessionid',
                    'value': sessionid,
                    'domain': '.instagram.com',
                    'path': '/'
                }])

                self.page.reload()

                # Extract all cookies
                all_cookies = self.extract_cookies_from_browser(self.page)
                session_data.update(all_cookies)

                print(f"✅ Extracted {len(session_data)} cookies")

                # Validate session
                if self.validate_session(session_data):
                    print("✅ Session is valid!")
                    self.save_session(session_data)
                    return True
                else:
                    print("❌ Session validation failed")
                    return False

        except Exception as e:
            print(f"❌ Headless extraction failed: {e}")
            return False
        finally:
            self.cleanup()

    def extract_session_gui(self):
        """Extract session using GUI browser"""
        print("\n🖥️ AUTOMATED SESSION EXTRACTION (GUI)")
        print("="*60)

        try:
            with sync_playwright() as p:
                # Launch browser with GUI
                self.browser = p.chromium.launch(
                    headless=False,
                    args=['--start-maximized']
                )

                self.context = self.browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )

                self.page = self.context.new_page()

                print("🌐 Opening Instagram...")
                self.page.goto('https://www.instagram.com/accounts/login/')

                print("\n📋 Please log into Instagram in the browser window that opened")
                print("⏳ Waiting for login success...")

                # Monitor for login success
                if self.monitor_login_success(self.page):
                    # Extract cookies
                    session_data = self.extract_cookies_from_browser(self.page)

                    if session_data.get('sessionid'):
                        print(f"✅ Extracted session with {len(session_data)} cookies")

                        # Validate session
                        if self.validate_session(session_data):
                            print("✅ Session validation successful!")
                            self.save_session(session_data)
                            self.captured_session = session_data
                            return True
                        else:
                            print("❌ Session validation failed")
                    else:
                        print("❌ No sessionid found in cookies")

                return False

        except Exception as e:
            print(f"❌ GUI extraction failed: {e}")
            return False
        finally:
            self.cleanup()

    def run_extraction(self):
        """Main extraction flow"""
        print("🚀 AUTOMATED FRESH SESSION EXTRACTOR")
        print("="*60)
        print(f"Target: {self.target}")
        print(f"Output: {self.session_file}")
        print()

        self.setup_signal_handlers()

        # Try GUI method first (more reliable)
        try:
            if self.extract_session_gui():
                print("\n🎉 SESSION EXTRACTION SUCCESSFUL!")
                print(f"✅ Session saved to: {self.session_file}")
                print(f"✅ Backup saved to: {self.backup_dir}/")
                return True
        except Exception as e:
            print(f"GUI method failed: {e}")

        # Fallback to headless method
        print("\n🔄 Trying headless method...")
        if self.extract_session_headless():
            print("\n🎉 SESSION EXTRACTION SUCCESSFUL!")
            print(f"✅ Session saved to: {self.session_file}")
            print(f"✅ Backup saved to: {self.backup_dir}/")
            return True

        print("\n❌ All extraction methods failed")
        return False

def main():
    """Main function"""
    try:
        extractor = AutoFreshSessionExtractor()

        if extractor.run_extraction():
            print("\n🎯 NEXT STEPS:")
            print("1. ✅ Fresh session extracted and saved")
            print("2. 🔄 Add working proxies to config/proxies.json")
            print("3. 🚀 Run DM extraction with interceptor protection")
            print("4. 📊 Monitor logs/requests.log")

            return True
        else:
            print("\n❌ Session extraction failed")
            return False

    except KeyboardInterrupt:
        print("\n\n🛑 Operation cancelled by user")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
