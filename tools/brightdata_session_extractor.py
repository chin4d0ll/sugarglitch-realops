# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Bright Data Remote Browser Session Extractor
Automatically extract Instagram session using Bright Data's remote browser
"""

import os
import json
import sys
import time
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright
import requests

class BrightDataSessionExtractor:
    def __init__(self):
        # Bright Data Browser endpoint
        self.browser_endpoint = "wss://brd-customer-hl_63f0835e-zone-scraping_agent:o5wnk3ws1r04@brd.superproxy.io:9222"
        self.target_username = "alx.trading"
        self.session_file = "tools/session_alx_trading.json"
        self.logs_dir = "logs"

        # Ensure directories exist
        os.makedirs("tools", exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)

    def log_message(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)

        # Also save to log file
        with open(f"{self.logs_dir}/session_extraction.log", "a", encoding="utf-8") as f:
            f.write(log_msg + "\n")

    async def extract_session_with_playwright(self):
        """Extract session using Playwright with Bright Data remote browser"""
        self.log_message("🚀 Starting Playwright session extraction with Bright Data")

        try:
            async with async_playwright() as p:
                self.log_message("🔗 Connecting to Bright Data browser endpoint...")

                # Connect to remote browser
                browser = await p.chromium.connect_over_cdp(self.browser_endpoint)

                self.log_message("✅ Connected to remote browser successfully")

                # Create new page
                page = await browser.new_page()

                # Set user agent to avoid detection
                await page.set_extra_http_headers({
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                })

                self.log_message("📱 Navigating to Instagram...")

                # Navigate to Instagram
                await page.goto('https://www.instagram.com/', wait_until='networkidle')

                self.log_message("🔍 Checking current login status...")

                # Check if already logged in
                try:
                    # Look for login indicators
                    login_button = await page.wait_for_selector('button[type="submit"]', timeout=5000)
                    if login_button:
                        self.log_message("❌ Not logged in - need to login first")
                        await self.auto_login_process(page)
                except Exception:
                    # No login button found, might be logged in
                    self.log_message("🔍 No login form found, checking if logged in...")

                # Check for existing session
                session_data = await self.extract_cookies(page)

                if session_data and session_data.get('sessionid'):
                    self.log_message("✅ Session found!")

                    # Test the session
                    if await self.test_session_validity(session_data):
                        self.log_message("✅ Session is valid!")
                        self.save_session(session_data)
                        return session_data
                    else:
                        self.log_message("❌ Session is invalid, attempting fresh login...")
                        await self.auto_login_process(page)
                        session_data = await self.extract_cookies(page)

                await browser.close()
                return session_data

        except Exception as e:
            self.log_message(f"❌ Error during extraction: {e}")
            return None

    async def auto_login_process(self, page):
        """Attempt automated login process"""
        self.log_message("🔐 Attempting automated login process...")

        try:
            # Wait for login form
            await page.wait_for_selector('input[name="username"]', timeout=10000)

            self.log_message("⚠️  Login form detected.")
            self.log_message("⚠️  Automated login not implemented for security reasons.")
            self.log_message("📋 Manual steps required:")
            self.log_message("1. The browser should be open with Instagram login page")
            self.log_message("2. Please login manually in the browser")
            self.log_message("3. After successful login, session will be extracted automatically")

            # Wait for manual login (check for profile icon or home page)
            self.log_message("⏳ Waiting for manual login completion...")

            # Wait for login completion indicators
            try:
                await page.wait_for_selector('svg[aria-label="Home"]', timeout=300000)  # 5 minutes
                self.log_message("✅ Login detected successful!")
            except Exception:
                await page.wait_for_selector('a[href="/direct/inbox/"]', timeout=300000)
                self.log_message("✅ Login detected via inbox link!")

        except Exception as e:
            self.log_message(f"❌ Error during login process: {e}")

    async def extract_cookies(self, page):
        """Extract cookies from the page"""
        self.log_message("🍪 Extracting cookies...")

        try:
            cookies = await page.context.cookies()

            session_data = {}
            for cookie in cookies:
                if cookie['domain'] in ['.instagram.com', 'instagram.com']:
                    if cookie['name'] in ['sessionid', 'csrftoken', 'ds_user_id', 'mid', 'ig_did', 'shbid', 'rur']:
                        session_data[cookie['name']] = cookie['value']
                        self.log_message(f"✅ Found {cookie['name']}: {cookie['value'][:20]}...")

            return session_data

        except Exception as e:
            self.log_message(f"❌ Error extracting cookies: {e}")
            return {}

    async def test_session_validity(self, session_data):
        """Test if extracted session is valid"""
        self.log_message("🔍 Testing extracted session validity...")

        if not session_data.get('sessionid'):
            self.log_message("❌ No sessionid found")
            return False

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        # Build cookie string
        cookies = []
        for key, value in session_data.items():
            if value:
                cookies.append(f"{key}={value}")

        if cookies:
            headers['Cookie'] = "; ".join(cookies)

        try:
            response = requests.get('https://www.instagram.com/', headers=headers, timeout=10)

            if response.status_code == 200:
                if 'login' not in response.url.lower() and '"is_logged_in":false' not in response.text:
                    self.log_message("✅ Session validation successful!")
                    return True
                else:
                    self.log_message("❌ Session validation failed - not logged in")
                    return False
            else:
                self.log_message(f"❌ Session validation failed - HTTP {response.status_code}")
                return False

        except Exception as e:
            self.log_message(f"❌ Error testing session: {e}")
            return False

    def save_session(self, session_data):
        """Save session data to JSON file"""
        self.log_message("💾 Saving session to file...")

        session_info = {
            'sessionid': session_data.get('sessionid', ''),
            'csrftoken': session_data.get('csrftoken', ''),
            'ds_user_id': session_data.get('ds_user_id', ''),
            'mid': session_data.get('mid', ''),
            'ig_did': session_data.get('ig_did', ''),
            'shbid': session_data.get('shbid', ''),
            'rur': session_data.get('rur', ''),
            'target': self.target_username,
            'created_at': datetime.now().isoformat(),
            'status': 'active',
            'extraction_method': 'bright_data_remote_browser'
        }

        try:
            with open(self.session_file, 'w') as f:
                json.dump(session_info, f, indent=2)
            self.log_message(f"✅ Session saved to {self.session_file}")

            # Also save backup
            backup_file = f"sessions/session_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            os.makedirs("sessions", exist_ok=True)

            with open(backup_file, 'w') as f:
                json.dump(session_info, f, indent=2)
            self.log_message(f"✅ Backup saved to {backup_file}")

            return True

        except Exception as e:
            self.log_message(f"❌ Failed to save session: {e}")
            return False

    async def run(self):
        """Main execution flow"""
        self.log_message("🚀 BRIGHT DATA REMOTE BROWSER SESSION EXTRACTOR")
        self.log_message("="*60)
        self.log_message(f"Target: {self.target_username}")
        self.log_message(f"Browser Endpoint: {self.browser_endpoint}")
        self.log_message(f"Session File: {self.session_file}")
        self.log_message("")

        try:
            session_data = await self.extract_session_with_playwright()

            if session_data and session_data.get('sessionid'):
                self.log_message("🎉 SUCCESS! Fresh session extracted and saved!")
                self.log_message(f"📄 Session ID: {session_data['sessionid'][:20]}...")
                self.log_message(f"📁 Saved to: {self.session_file}")

                return True
            else:
                self.log_message("❌ Failed to extract valid session")
                return False

        except Exception as e:
            self.log_message(f"❌ Critical error: {e}")
            return False

def main():
    """Main function"""
    try:
        extractor = BrightDataSessionExtractor()
        result = asyncio.run(extractor.run())

        if result:
            print("\n🎉 Session extraction completed successfully!")
            print("Next steps:")
            print("1. Session is saved in tools/session_alx_trading.json")
            print("2. Run DM extraction with interceptor protection")
            print("3. Check logs/session_extraction.log for details")
        else:
            print("\n❌ Session extraction failed")
            print("Check logs/session_extraction.log for details")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
