# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Automated Session Hijacker using Bright Data Proxy
Fully automated session extraction without manual input
"""

import requests
import json
import time
import random
import os
from datetime import datetime
import re

class AutoSessionHijacker:
    def __init__(self):
        # Bright Data proxy credentials
        self.proxy_host = "brd.superproxy.io"
        self.proxy_port = "22225"  # HTTP proxy port
        self.proxy_user = "brd-customer-hl_63f0835e-zone-scraping_agent"
        self.proxy_pass = "o5wnk3ws1r04"

        self.proxy_url = f"http://{self.proxy_user}:{self.proxy_pass}@{self.proxy_host}:{self.proxy_port}"

        self.proxies = {
            'http': self.proxy_url,
            'https': self.proxy_url
        }

        self.session_file = "tools/session_alx_trading.json"

    def get_random_user_agent(self):
        """Get random user agent"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]
        return random.choice(user_agents)

    def generate_session_from_public_endpoints(self):
        """Try to generate session using public Instagram endpoints"""
        print("🔍 Attempting to generate session from public endpoints...")

        headers = {
            'User-Agent': self.get_random_user_agent(),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }

        try:
            # Method 1: Try to get session from Instagram's public API
            session = requests.Session()
            session.proxies.update(self.proxies)

            # Get initial page to get csrf token
            print("Getting initial Instagram page...")
            response = session.get('https://www.instagram.com/', headers=headers, timeout=10)

            if response.status_code == 200:
                # Extract csrf token
                csrf_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
                if csrf_match:
                    csrf_token = csrf_match.group(1)
                    print(f"✅ Got CSRF token: {csrf_token[:20]}...")

                    # Check if there are any session cookies
                    cookies = session.cookies.get_dict()
                    print(f"🍪 Cookies received: {list(cookies.keys())}")

                    if cookies:
                        return self.process_cookies(cookies, csrf_token)

            return None

        except Exception as e:
            print(f"❌ Error generating session: {e}")
            return None

    def hijack_existing_sessions(self):
        """Try to hijack existing sessions from common sources"""
        print("🕵️ Attempting to hijack existing sessions...")

        # Method 1: Check for existing session files
        session_patterns = [
            "session*.json",
            "*session*.json",
            "ig_session*.json",
            "instagram_session*.json"
        ]

        for pattern in session_patterns:
            try:
                import glob
                files = glob.glob(pattern, recursive=True)
                files.extend(glob.glob(f"**/{pattern}", recursive=True))

                for file_path in files:
                    if os.path.exists(file_path) and file_path != self.session_file:
                        print(f"Found session file: {file_path}")
                        try:
                            with open(file_path, 'r') as f:
                                session_data = json.load(f)
                                if self.validate_session_data(session_data):
                                    return session_data
                        except Exception:
                            continue
            except Exception:
                continue

        return None

    def extract_session_from_browser_cache(self):
        """Try to extract session from browser cache/storage"""
        print("🌐 Attempting to extract from browser cache...")

        # Common browser cache locations
        cache_paths = [
            "~/.cache/google-chrome/Default/Local Storage/leveldb",
            "~/.mozilla/firefox/*/storage/default/https+++www.instagram.com",
            "~/Library/Caches/Google/Chrome/Default/Local Storage/leveldb",
            "/tmp/chrome_debug_*"
        ]

        for cache_path in cache_paths:
            expanded_path = os.path.expanduser(cache_path)
            if os.path.exists(expanded_path):
                print(f"Found cache: {expanded_path}")
                # This would require more complex parsing
                # For now, we'll skip this method

        return None

    def generate_dummy_session(self):
        """Generate a dummy session for testing (last resort)"""
        print("🎭 Generating dummy session for testing...")

        # This creates a session that will likely fail but can be used for testing
        dummy_session = {
            'sessionid': f"dummy_{int(time.time())}:{random.randint(1000000, 9999999)}:test",
            'csrftoken': f"csrf_{random.randint(100000, 999999)}",
            'ds_user_id': str(random.randint(10000000, 99999999)),
            'created_at': datetime.now().isoformat(),
            'target': 'alx.trading',
            'status': 'testing',
            'source': 'dummy_generator'
        }

        return dummy_session

    def process_cookies(self, cookies, csrf_token=None):
        """Process cookies into session format"""
        session_data = {
            'created_at': datetime.now().isoformat(),
            'target': 'alx.trading',
            'status': 'active',
            'source': 'auto_hijacker'
        }

        # Map cookies to session data
        cookie_mapping = {
            'sessionid': 'sessionid',
            'csrftoken': 'csrftoken',
            'ds_user_id': 'ds_user_id',
            'mid': 'mid',
            'ig_did': 'ig_did'
        }

        for cookie_name, session_key in cookie_mapping.items():
            if cookie_name in cookies:
                session_data[session_key] = cookies[cookie_name]

        if csrf_token and 'csrftoken' not in session_data:
            session_data['csrftoken'] = csrf_token

        return session_data

    def validate_session_data(self, session_data):
        """Validate session data"""
        required_fields = ['sessionid']
        return all(field in session_data and session_data[field] for field in required_fields)

    def test_session(self, session_data):
        """Test if session works"""
        if not session_data or not session_data.get('sessionid'):
            return False

        headers = {
            'User-Agent': self.get_random_user_agent(),
            'Cookie': f"sessionid={session_data['sessionid']}"
        }

        try:
            response = requests.get('https://www.instagram.com/',
                                  headers=headers,
                                  proxies=self.proxies,
                                  timeout=10)

            if response.status_code == 200:
                if 'login' not in response.url.lower() and '"is_logged_in":false' not in response.text:
                    return True
            return False
        except Exception:
            return False

    def save_session(self, session_data):
        """Save session to file"""
        try:
            os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            print(f"✅ Session saved to {self.session_file}")
            return True
        except Exception as e:
            print(f"❌ Failed to save session: {e}")
            return False

    def run(self):
        """Main execution"""
        print("🚀 AUTOMATED SESSION HIJACKER - BRIGHT DATA EDITION")
        print("="*60)

        methods = [
            ("Public Endpoints", self.generate_session_from_public_endpoints),
            ("Existing Sessions", self.hijack_existing_sessions),
            ("Browser Cache", self.extract_session_from_browser_cache),
            ("Dummy Session", self.generate_dummy_session)
        ]

        for method_name, method_func in methods:
            print(f"\n🔍 Trying method: {method_name}")
            try:
                session_data = method_func()
                if session_data:
                    print(f"✅ Got session data from {method_name}")

                    # Test the session
                    if self.test_session(session_data):
                        print("✅ Session is valid!")
                        if self.save_session(session_data):
                            print(f"🎉 SUCCESS! Valid session saved from {method_name}")
                            return True
                    else:
                        print("❌ Session failed validation")
                        # Save anyway for debugging
                        session_data['status'] = 'invalid'
                        self.save_session(session_data)
                else:
                    print(f"❌ No session data from {method_name}")
            except Exception as e:
                print(f"❌ Error in {method_name}: {e}")

        print("\n❌ All methods failed to get valid session")
        return False

if __name__ == "__main__":
    hijacker = AutoSessionHijacker()
    hijacker.run()
