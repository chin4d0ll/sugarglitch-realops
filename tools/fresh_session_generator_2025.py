# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔥 FRESH SESSION GENERATOR 2025 - REAL INSTAGRAM ACCESS
====================================================
Generate and validate fresh Instagram sessions for real DM extraction.
Uses advanced browser automation and bypass techniques.
"""

import os
import sys
import json
import time
import random
import requests
import sqlite3
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Browser automation imports
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    from webdriver_manager.chrome import ChromeDriverManager
    import undetected_chromedriver as uc
except ImportError:
    print("Installing selenium and undetected-chromedriver...")
    os.system("pip install selenium webdriver-manager undetected-chromedriver")
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    from webdriver_manager.chrome import ChromeDriverManager
    import undetected_chromedriver as uc

try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes, BadPassword
except ImportError:
    print("Installing instagrapi...")
    os.system("pip install instagrapi")
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes, BadPassword

class FreshSessionGenerator:
    """🔥 Generate fresh Instagram sessions for real DM extraction"""

    def __init__(self):
        self.target = "alx.trading"
        self.project_root = "/workspaces/sugarglitch-realops"

        # Credentials from profile
        self.username = "alx.trading"
        self.password = "Alx54321"  # Based on previous analysis

        # Alternative credentials to try
        self.backup_credentials = [
            {"username": "alx.trading", "password": "Alx54321"},
            {"username": "alx.trading", "password": "alx54321"},
            {"username": "alx.trading", "password": "Alx12345"},
            {"username": "alx.trading", "password": "ALX54321"},
            {"username": "alx.trading", "password": "AlxTrading123"},
            {"username": "alx.trading", "password": "trading123"},
        ]

        # Output directories
        self.sessions_dir = Path(f"{self.project_root}/fresh_sessions_2025")
        self.sessions_dir.mkdir(exist_ok=True)

        self.output_dir = Path(f"{self.project_root}/fresh_extraction_2025")
        self.output_dir.mkdir(exist_ok=True)

        # Setup logging
        self.setup_logging()

        # Browser driver
        self.browser_driver = None

        # InstagrAPI client
        self.instagrapi_client = None

        print(f"🔥 Fresh Session Generator 2025 initialized")
        print(f"🎯 Target: {self.target}")
        print(f"📂 Sessions dir: {self.sessions_dir}")
        print(f"📂 Output dir: {self.output_dir}")

    def setup_logging(self):
        """Setup comprehensive logging"""
        log_file = self.output_dir / f"fresh_session_generation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def method_1_browser_fresh_login(self) -> Optional[Dict]:
        """Method 1: Fresh browser login with maximum stealth"""
        self.logger.info("🌐 Method 1: Browser fresh login starting...")

        try:
            # Setup maximum stealth Chrome
            chrome_options = uc.ChromeOptions()

            # Stealth options
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")  # Faster loading
            chrome_options.add_argument("--disable-javascript")  # Initially disable JS
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            # Mobile user agent for better success rate
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36")

            # Unique user data directory
            chrome_options.add_argument(f"--user-data-dir=/tmp/chrome_fresh_{int(time.time())}")

            # Initialize driver
            self.browser_driver = uc.Chrome(options=chrome_options)

            # Execute stealth scripts
            self.browser_driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.browser_driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            self.browser_driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")

            self.logger.info("✅ Stealth browser initialized")

            # Navigate to Instagram login
            self.browser_driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(random.uniform(3, 6))

            # Try credentials
            for i, creds in enumerate(self.backup_credentials):
                try:
                    self.logger.info(f"🔐 Trying credentials {i+1}/{len(self.backup_credentials)}: {creds['username']}")

                    # Find login fields
                    wait = WebDriverWait(self.browser_driver, 15)
                    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
                    password_field = self.browser_driver.find_element(By.NAME, "password")

                    # Clear fields
                    username_field.clear()
                    password_field.clear()

                    # Human-like typing
                    self.human_type(username_field, creds['username'])
                    time.sleep(random.uniform(1, 2))
                    self.human_type(password_field, creds['password'])
                    time.sleep(random.uniform(1, 2))

                    # Submit login
                    login_button = self.browser_driver.find_element(By.XPATH, "//button[@type='submit']")
                    login_button.click()

                    # Wait for response
                    time.sleep(random.uniform(5, 8))

                    # Check if login successful
                    current_url = self.browser_driver.current_url
                    self.logger.info(f"📍 Current URL after login: {current_url}")

                    if "accounts/login" not in current_url and "challenge" not in current_url:
                        self.logger.info("✅ Browser login successful!")

                        # Extract session data
                        session_data = self.extract_session_from_browser()
                        if session_data:
                            return session_data

                    elif "challenge" in current_url:
                        self.logger.warning("⚠️ Instagram challenge detected - account may be restricted")
                        # Try to handle challenge automatically
                        self.handle_instagram_challenge()

                    else:
                        self.logger.warning(f"❌ Login failed for {creds['username']}")
                        # Wait before trying next credentials
                        time.sleep(random.uniform(3, 5))

                except Exception as e:
                    self.logger.error(f"❌ Error with credentials {creds['username']}: {e}")
                    continue

            self.logger.error("❌ All browser login attempts failed")
            return None

        except Exception as e:
            self.logger.error(f"❌ Browser method failed: {e}")
            return None

        finally:
            if self.browser_driver:
                try:
                    self.browser_driver.quit()
                except Exception:
                    pass

    def human_type(self, element, text, delay_range=(0.05, 0.2)):
        """Simulate human typing patterns"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(*delay_range))

    def handle_instagram_challenge(self):
        """Attempt to handle Instagram challenge automatically"""
        try:
            self.logger.info("🛡️ Attempting to handle Instagram challenge...")

            # Look for "Send Security Code" button
            security_buttons = self.browser_driver.find_elements(By.XPATH, "//*[contains(text(), 'Send Security Code')]")
            if security_buttons:
                security_buttons[0].click()
                time.sleep(3)
                self.logger.info("📱 Security code request sent")

            # Look for alternative verification methods
            alt_methods = self.browser_driver.find_elements(By.XPATH, "//*[contains(text(), 'Try Another Way')]")
            if alt_methods:
                alt_methods[0].click()
                time.sleep(3)
                self.logger.info("🔄 Trying alternative verification")

            # Wait for manual intervention or auto-resolution
            time.sleep(10)

        except Exception as e:
            self.logger.warning(f"⚠️ Challenge handling error: {e}")

    def extract_session_from_browser(self) -> Optional[Dict]:
        """Extract session data from browser cookies"""
        try:
            cookies = self.browser_driver.get_cookies()
            session_data = {
                'extraction_timestamp': datetime.now().isoformat(),
                'method': 'browser_fresh_login',
                'cookies': {},
                'user_agent': self.browser_driver.execute_script("return navigator.userAgent;"),
                'url': self.browser_driver.current_url
            }

            for cookie in cookies:
                session_data['cookies'][cookie['name']] = cookie['value']

            # Validate essential cookies
            if 'sessionid' in session_data['cookies'] and 'ds_user_id' in session_data['cookies']:
                session_file = self.sessions_dir / f"fresh_browser_session_{int(time.time())}.json"
                with open(session_file, 'w') as f:
                    json.dump(session_data, f, indent=2)

                self.logger.info(f"✅ Fresh session extracted and saved: {session_file}")
                return session_data
            else:
                self.logger.warning("❌ Essential cookies missing from browser session")
                return None

        except Exception as e:
            self.logger.error(f"❌ Session extraction error: {e}")
            return None

    def method_2_instagrapi_fresh_login(self) -> Optional[Dict]:
        """Method 2: Fresh InstagrAPI login with device simulation"""
        self.logger.info("📱 Method 2: InstagrAPI fresh login starting...")

        try:
            self.instagrapi_client = Client()

            # Advanced device simulation
            device_settings = {
                "app_version": "240.0.0.17.112",  # Latest version
                "android_version": 31,
                "android_release": "12.0",
                "dpi": "420dpi",
                "resolution": "1080x2340",
                "manufacturer": "samsung",
                "device": "SM-G991B",
                "model": "galaxy_s21_5g",
                "cpu": "exynos2100",
                "version_code": "354678416",
                "locale": "en_US",
                "timezone": "America/New_York"
            }

            self.instagrapi_client.set_device(device_settings)
            self.instagrapi_client.delay_range = [1, 3]

            # Try credentials
            for i, creds in enumerate(self.backup_credentials):
                try:
                    self.logger.info(f"🔐 InstagrAPI trying credentials {i+1}: {creds['username']}")

                    # Attempt login
                    success = self.instagrapi_client.login(creds['username'], creds['password'])

                    if success:
                        self.logger.info("✅ InstagrAPI login successful!")

                        # Extract session data
                        session_data = {
                            'extraction_timestamp': datetime.now().isoformat(),
                            'method': 'instagrapi_fresh_login',
                            'username': creds['username'],
                            'sessionid': self.instagrapi_client.sessionid,
                            'csrftoken': self.instagrapi_client.csrftoken,
                            'ds_user_id': self.instagrapi_client.user_id,
                            'device_settings': device_settings,
                            'user_info': self.instagrapi_client.account_info().dict()
                        }

                        # Save session
                        session_file = self.sessions_dir / f"fresh_instagrapi_session_{int(time.time())}.json"
                        with open(session_file, 'w') as f:
                            json.dump(session_data, f, indent=2, default=str)

                        # Save InstagrAPI settings
                        settings_file = self.sessions_dir / f"instagrapi_settings_{int(time.time())}.json"
                        self.instagrapi_client.dump_settings(str(settings_file))

                        self.logger.info(f"✅ InstagrAPI session saved: {session_file}")
                        return session_data

                except BadPassword:
                    self.logger.warning(f"❌ Bad password for {creds['username']}")
                    continue
                except PleaseWaitFewMinutes:
                    self.logger.warning("⏳ Rate limited - waiting...")
                    time.sleep(300)
                    continue
                except Exception as e:
                    self.logger.error(f"❌ InstagrAPI error for {creds['username']}: {e}")
                    continue

            self.logger.error("❌ All InstagrAPI login attempts failed")
            return None

        except Exception as e:
            self.logger.error(f"❌ InstagrAPI method failed: {e}")
            return None

    def validate_fresh_session(self, session_data: Dict) -> bool:
        """Validate if fresh session is working"""
        self.logger.info("🧪 Validating fresh session...")

        try:
            session = requests.Session()

            # Set cookies
            if 'cookies' in session_data:
                for name, value in session_data['cookies'].items():
                    session.cookies.set(name, value, domain='.instagram.com')
            elif 'sessionid' in session_data:
                session.cookies.set('sessionid', session_data['sessionid'], domain='.instagram.com')
                if 'csrftoken' in session_data:
                    session.cookies.set('csrftoken', session_data['csrftoken'], domain='.instagram.com')

            # Test headers
            headers = {
                'User-Agent': session_data.get('user_agent', 'Instagram 240.0.0.17.112 Android'),
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'X-Requested-With': 'XMLHttpRequest',
                'X-Instagram-AJAX': '1',
                'Referer': 'https://www.instagram.com/',
            }

            session.headers.update(headers)

            # Test endpoints
            test_endpoints = [
                'https://www.instagram.com/',
                'https://www.instagram.com/accounts/edit/',
                'https://www.instagram.com/api/v1/accounts/current_user/',
                f'https://www.instagram.com/{self.target}/'
            ]

            for endpoint in test_endpoints:
                try:
                    response = session.get(endpoint, timeout=10, allow_redirects=False)
                    self.logger.info(f"📡 {endpoint}: {response.status_code}")

                    if response.status_code == 200:
                        # Check if logged in
                        if 'accounts/edit' in endpoint:
                            self.logger.info("✅ Session validation successful - can access account settings")
                            return True
                        elif 'current_user' in endpoint:
                            self.logger.info("✅ Session validation successful - API access confirmed")
                            return True

                except Exception as e:
                    self.logger.warning(f"⚠️ Test error for {endpoint}: {e}")

            self.logger.warning("❌ Session validation failed")
            return False

        except Exception as e:
            self.logger.error(f"❌ Session validation error: {e}")
            return False

    def extract_dms_with_fresh_session(self, session_data: Dict) -> Optional[Dict]:
        """Extract DMs using fresh session"""
        self.logger.info("📨 Extracting DMs with fresh session...")

        if not self.validate_fresh_session(session_data):
            self.logger.error("❌ Session validation failed - cannot extract DMs")
            return None

        try:
            # Use InstagrAPI if available
            if session_data.get('method') == 'instagrapi_fresh_login' and self.instagrapi_client:
                return self.extract_dms_with_instagrapi()

            # Otherwise use requests-based extraction
            return self.extract_dms_with_requests(session_data)

        except Exception as e:
            self.logger.error(f"❌ DM extraction error: {e}")
            return None

    def extract_dms_with_instagrapi(self) -> Optional[Dict]:
        """Extract DMs using InstagrAPI client"""
        try:
            self.logger.info("📱 Extracting DMs with InstagrAPI...")

            # Get direct threads
            threads = self.instagrapi_client.direct_threads()

            conversations = []
            for thread in threads[:10]:  # Limit to first 10
                try:
                    thread_data = {
                        'thread_id': thread.id,
                        'thread_title': thread.title or f"Thread {thread.id}",
                        'participants': [user.username for user in thread.users],
                        'messages': [],
                        'last_activity': thread.last_activity_at.isoformat() if thread.last_activity_at else None
                    }

                    # Get messages from thread
                    messages = self.instagrapi_client.direct_messages(thread.id, amount=50)

                    for msg in messages:
                        message_data = {
                            'id': msg.id,
                            'text': msg.text or '',
                            'timestamp': msg.timestamp.isoformat(),
                            'user_id': msg.user_id,
                            'item_type': msg.item_type
                        }
                        thread_data['messages'].append(message_data)

                    thread_data['message_count'] = len(thread_data['messages'])
                    conversations.append(thread_data)

                    self.logger.info(f"✅ Extracted thread: {thread_data['thread_title']} ({thread_data['message_count']} messages)")

                except Exception as e:
                    self.logger.warning(f"⚠️ Error extracting thread {thread.id}: {e}")
                    continue

            # Prepare result
            result = {
                'extraction_info': {
                    'target': self.target,
                    'extraction_timestamp': datetime.now().isoformat(),
                    'method': 'instagrapi_fresh_session',
                    'total_conversations': len(conversations),
                    'total_messages': sum(c.get('message_count', 0) for c in conversations)
                },
                'conversations': conversations
            }

            # Save result
            output_file = self.output_dir / f"fresh_dm_extraction_{int(time.time())}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            self.logger.info(f"✅ DM extraction completed: {output_file}")
            self.logger.info(f"📊 Total conversations: {result['extraction_info']['total_conversations']}")
            self.logger.info(f"📨 Total messages: {result['extraction_info']['total_messages']}")

            return result

        except Exception as e:
            self.logger.error(f"❌ InstagrAPI DM extraction error: {e}")
            return None

    def extract_dms_with_requests(self, session_data: Dict) -> Optional[Dict]:
        """Extract DMs using requests session"""
        self.logger.info("🌐 Extracting DMs with requests session...")

        try:
            session = requests.Session()

            # Set cookies and headers
            if 'cookies' in session_data:
                for name, value in session_data['cookies'].items():
                    session.cookies.set(name, value, domain='.instagram.com')

            headers = {
                'User-Agent': session_data.get('user_agent', 'Instagram 240.0.0.17.112 Android'),
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'X-Requested-With': 'XMLHttpRequest',
                'X-Instagram-AJAX': '1',
                'Referer': 'https://www.instagram.com/',
            }

            session.headers.update(headers)

            # Try DM endpoints
            dm_endpoints = [
                'https://www.instagram.com/api/v1/direct_v2/inbox/',
                'https://i.instagram.com/api/v1/direct_v2/inbox/',
                'https://www.instagram.com/api/v1/direct_v2/threads/'
            ]

            conversations = []

            for endpoint in dm_endpoints:
                try:
                    response = session.get(endpoint, timeout=15)
                    self.logger.info(f"📡 {endpoint}: {response.status_code}")

                    if response.status_code == 200:
                        data = response.json()

                        # Process inbox data
                        if 'inbox' in data:
                            threads = data['inbox'].get('threads', [])

                            for thread in threads[:10]:  # Limit to first 10
                                thread_data = {
                                    'thread_id': thread.get('thread_id', ''),
                                    'thread_title': thread.get('thread_title', f"Thread {thread.get('thread_id', '')}"),
                                    'participants': [user.get('username', '') for user in thread.get('users', [])],
                                    'messages': [],
                                    'last_activity': thread.get('last_activity_at', None)
                                }

                                # Extract messages from thread
                                for item in thread.get('items', [])[:20]:  # Limit messages
                                    message_data = {
                                        'id': item.get('item_id', ''),
                                        'text': item.get('text', ''),
                                        'timestamp': item.get('timestamp', ''),
                                        'user_id': item.get('user_id', ''),
                                        'item_type': item.get('item_type', '')
                                    }
                                    thread_data['messages'].append(message_data)

                                thread_data['message_count'] = len(thread_data['messages'])
                                conversations.append(thread_data)

                        if conversations:
                            break  # Found data, stop trying other endpoints

                except Exception as e:
                    self.logger.warning(f"⚠️ Error with endpoint {endpoint}: {e}")
                    continue

            # Prepare result
            result = {
                'extraction_info': {
                    'target': self.target,
                    'extraction_timestamp': datetime.now().isoformat(),
                    'method': 'requests_fresh_session',
                    'total_conversations': len(conversations),
                    'total_messages': sum(c.get('message_count', 0) for c in conversations)
                },
                'conversations': conversations
            }

            # Save result
            output_file = self.output_dir / f"fresh_requests_extraction_{int(time.time())}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            self.logger.info(f"✅ Requests DM extraction completed: {output_file}")
            self.logger.info(f"📊 Total conversations: {result['extraction_info']['total_conversations']}")
            self.logger.info(f"📨 Total messages: {result['extraction_info']['total_messages']}")

            return result

        except Exception as e:
            self.logger.error(f"❌ Requests DM extraction error: {e}")
            return None

    def execute_complete_fresh_extraction(self):
        """Execute complete fresh session generation and DM extraction"""
        self.logger.info("🚀 Starting complete fresh extraction process...")

        extraction_results = {
            'session_generation': [],
            'dm_extraction': None,
            'success': False,
            'timestamp': datetime.now().isoformat()
        }

        # Method 1: Browser login
        self.logger.info("=" * 60)
        self.logger.info("🌐 ATTEMPTING BROWSER FRESH LOGIN")
        self.logger.info("=" * 60)

        browser_session = self.method_1_browser_fresh_login()
        if browser_session:
            extraction_results['session_generation'].append({
                'method': 'browser',
                'success': True,
                'session_data': browser_session
            })

            # Try DM extraction
            dm_result = self.extract_dms_with_fresh_session(browser_session)
            if dm_result:
                extraction_results['dm_extraction'] = dm_result
                extraction_results['success'] = True
                self.logger.info("🎉 BROWSER METHOD SUCCESS - REAL DMs EXTRACTED!")
                return extraction_results
        else:
            extraction_results['session_generation'].append({
                'method': 'browser',
                'success': False,
                'error': 'Browser login failed'
            })

        # Method 2: InstagrAPI login
        self.logger.info("=" * 60)
        self.logger.info("📱 ATTEMPTING INSTAGRAPI FRESH LOGIN")
        self.logger.info("=" * 60)

        instagrapi_session = self.method_2_instagrapi_fresh_login()
        if instagrapi_session:
            extraction_results['session_generation'].append({
                'method': 'instagrapi',
                'success': True,
                'session_data': instagrapi_session
            })

            # Try DM extraction
            dm_result = self.extract_dms_with_fresh_session(instagrapi_session)
            if dm_result:
                extraction_results['dm_extraction'] = dm_result
                extraction_results['success'] = True
                self.logger.info("🎉 INSTAGRAPI METHOD SUCCESS - REAL DMs EXTRACTED!")
                return extraction_results
        else:
            extraction_results['session_generation'].append({
                'method': 'instagrapi',
                'success': False,
                'error': 'InstagrAPI login failed'
            })

        # Final result
        if not extraction_results['success']:
            self.logger.error("❌ ALL FRESH SESSION METHODS FAILED")
            self.logger.info("🔍 POSSIBLE REASONS:")
            self.logger.info("   - Account credentials are incorrect or changed")
            self.logger.info("   - Account is locked or restricted")
            self.logger.info("   - Instagram has enhanced security measures")
            self.logger.info("   - Network/IP restrictions")
            self.logger.info("   - Account requires 2FA or additional verification")

        return extraction_results

def main():
    """Main execution function"""
    print("🔥 FRESH SESSION GENERATOR 2025 - REAL INSTAGRAM DM EXTRACTION")
    print("=" * 70)

    generator = FreshSessionGenerator()
    results = generator.execute_complete_fresh_extraction()

    print("\n" + "=" * 70)
    print("📊 FINAL EXTRACTION RESULTS")
    print("=" * 70)

    print(f"🕒 Timestamp: {results['timestamp']}")
    print(f"✅ Success: {results['success']}")
    print(f"🔧 Methods tried: {len(results['session_generation'])}")

    for i, method_result in enumerate(results['session_generation'], 1):
        status = "✅" if method_result['success'] else "❌"
        print(f"   {i}. {method_result['method']}: {status}")

    if results['dm_extraction']:
        dm_info = results['dm_extraction']['extraction_info']
        print(f"📨 DM Extraction: ✅ SUCCESS")
        print(f"   - Conversations: {dm_info['total_conversations']}")
        print(f"   - Total Messages: {dm_info['total_messages']}")
        print(f"   - Method: {dm_info['method']}")
    else:
        print(f"📨 DM Extraction: ❌ FAILED")

    print("=" * 70)

    return results

if __name__ == "__main__":
    main()
