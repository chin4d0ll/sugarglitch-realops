# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🎯 REAL ALX.TRADING DM EXTRACTOR - NO SIMULATION
================================================
Extract REAL DMs using valid session credentials - NO MOCKUP DATA
"""

import json
import os
import requests
import time
import sqlite3
from datetime import datetime
import urllib.parse

class RealAlxDMExtractor:
    def __init__(self):
        self.target = "alx.trading"
        self.output_dir = "/workspaces/sugarglitch-realops/data/real_alx_dms"
        self.db_path = f"{self.output_dir}/real_dm_data.db"

        os.makedirs(self.output_dir, exist_ok=True)

        print("🎯 REAL ALX.TRADING DM EXTRACTOR")
        print("=" * 50)
        print("⚠️  NO SIMULATION - REAL DATA ONLY")
        print("⚠️  NO MOCKUP - ACTUAL DM EXTRACTION")
        print(f"Target: {self.target}")

    def load_real_session_credentials(self):
        """Load real session credentials from various sources"""
        print("\n🔍 Loading real session credentials...")

        session_sources = [
            "/workspaces/sugarglitch-realops/sessions/session-alx.trading",
            "/workspaces/sugarglitch-realops/sessions/quick_bypass_session.json",
            "/workspaces/sugarglitch-realops/hijacked_sessions/hijacked_session_1749156763.json",
            "/workspaces/sugarglitch-realops/hijacked_sessions/rotated_session_1749156592.json"
        ]

        valid_sessions = []

        for session_file in session_sources:
            try:
                if os.path.exists(session_file):
                    with open(session_file, 'r') as f:
                        session_data = json.load(f)

                    # Extract sessionid from different formats
                    sessionid = None
                    if 'cookies' in session_data and 'sessionid' in session_data['cookies']:
                        sessionid = session_data['cookies']['sessionid']
                    elif 'sessionid' in session_data:
                        sessionid = session_data['sessionid']
                    elif 'session_token' in session_data:
                        sessionid = session_data['session_token']

                    if sessionid:
                        # URL decode if needed
                        if '%3A' in sessionid:
                            sessionid = urllib.parse.unquote(sessionid)

                        valid_sessions.append({
                            'source': session_file,
                            'sessionid': sessionid,
                            'cookies': {'sessionid': sessionid}
                        })
                        print(f"✅ Session found: {os.path.basename(session_file)} - {sessionid[:20]}...")

            except Exception as e:
                print(f"❌ Error loading {session_file}: {e}")

        print(f"📊 Total sessions found: {len(valid_sessions)}")
        return valid_sessions

    def test_session_validity(self, session_info):
        """Test if session is valid for Instagram"""
        print(f"\n🧪 Testing session validity: {os.path.basename(session_info['source'])}")

        session = requests.Session()
        session.cookies.update(session_info['cookies'])

        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.instagram.com/',
        }
        session.headers.update(headers)

        # Test different endpoints to validate session
        test_endpoints = [
            'https://www.instagram.com/',
            'https://www.instagram.com/accounts/edit/',
            f'https://www.instagram.com/{self.target}/'
        ]

        for endpoint in test_endpoints:
            try:
                response = session.get(endpoint, timeout=10, allow_redirects=False)
                print(f"   {endpoint}: {response.status_code}")

                if response.status_code == 200:
                    # Check if actually logged in
                    if endpoint == 'https://www.instagram.com/accounts/edit/':
                        return True, session  # Can access account settings = valid session
                elif response.status_code == 302:
                    location = response.headers.get('location', '')
                    if 'login' in location.lower():
                        print(f"   ❌ Redirected to login")
                        return False, None

            except Exception as e:
                print(f"   ❌ Error: {e}")

        return False, None

    def extract_real_dms_with_api(self, session):
        """Extract real DMs using Instagram API endpoints"""
        print(f"\n📡 Attempting real DM extraction via API...")

        # Get CSRF token first
        try:
            response = session.get('https://www.instagram.com/')
            if response.status_code == 200:
                import re
                csrf_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
                if csrf_match:
                    csrf_token = csrf_match.group(1)
                    session.headers['X-CSRFToken'] = csrf_token
                    session.headers['X-Instagram-AJAX'] = '1'
                    print(f"✅ CSRF token: {csrf_token[:20]}...")
        except Exception:
            pass

        # Try different DM API endpoints
        dm_endpoints = [
            'https://www.instagram.com/api/v1/direct_v2/inbox/',
            'https://www.instagram.com/api/v1/direct_v2/threads/',
            'https://i.instagram.com/api/v1/direct_v2/inbox/',
            'https://i.instagram.com/api/v1/direct_v2/inbox/?visual_message_return_type=unseen&thread_message_limit=10&persistentBadging=true&limit=20',
        ]

        real_conversations = []

        for endpoint in dm_endpoints:
            try:
                print(f"🔍 Testing API: {endpoint}")
                response = session.get(endpoint, timeout=15)
                print(f"   Status: {response.status_code}")

                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"   Response type: JSON")

                        # Check for inbox data
                        if 'inbox' in data:
                            inbox = data['inbox']
                            threads = inbox.get('threads', [])
                            print(f"   ✅ Found {len(threads)} threads")

                            for thread in threads:
                                # Look for threads with target user
                                thread_users = thread.get('users', [])
                                for user in thread_users:
                                    if user.get('username') == self.target:
                                        print(f"   🎯 Found conversation with {self.target}!")
                                        real_conversations.append({
                                            'thread_id': thread.get('thread_id'),
                                            'thread_data': thread,
                                            'source_endpoint': endpoint
                                        })
                                        break

                        # Check for direct threads response
                        elif 'threads' in data:
                            threads = data['threads']
                            print(f"   ✅ Found {len(threads)} direct threads")
                            real_conversations.extend([{
                                'thread_id': t.get('thread_id'),
                                'thread_data': t,
                                'source_endpoint': endpoint
                            } for t in threads])

                        # Save raw response for analysis
                        debug_file = f"{self.output_dir}/api_response_{int(time.time())}.json"
                        with open(debug_file, 'w') as f:
                            json.dump(data, f, indent=2)
                        print(f"   📁 Raw response saved: {debug_file}")

                    except json.JSONDecodeError:
                        print(f"   ⚠️ Non-JSON response")
                        # Save HTML for debugging
                        debug_file = f"{self.output_dir}/api_html_{int(time.time())}.html"
                        with open(debug_file, 'w') as f:
                            f.write(response.text)
                        print(f"   📁 HTML saved: {debug_file}")

                else:
                    print(f"   ❌ Status {response.status_code}")

            except Exception as e:
                print(f"   ❌ Error: {e}")

        return real_conversations

    def extract_real_dms_from_profile(self, session):
        """Extract DMs by accessing user profile and DM endpoints"""
        print(f"\n👤 Attempting DM extraction via profile access...")

        try:
            # Access target profile
            profile_url = f'https://www.instagram.com/{self.target}/'
            response = session.get(profile_url, timeout=15)

            if response.status_code == 200:
                print(f"✅ Profile accessible: {response.status_code}")

                # Look for user ID in profile data
                import re
                user_id_match = re.search(r'"id":"(\d+)"', response.text)
                if user_id_match:
                    user_id = user_id_match.group(1)
                    print(f"✅ User ID found: {user_id}")

                    # Try to access DM thread with this user
                    dm_url = f'https://www.instagram.com/api/v1/direct_v2/threads/?recipient_users=[{user_id}]'
                    dm_response = session.get(dm_url, timeout=15)

                    if dm_response.status_code == 200:
                        try:
                            dm_data = dm_response.json()
                            print(f"✅ DM data retrieved!")

                            # Save real DM data
                            dm_file = f"{self.output_dir}/real_dm_data_{int(time.time())}.json"
                            with open(dm_file, 'w') as f:
                                json.dump(dm_data, f, indent=2)
                            print(f"📁 Real DM data saved: {dm_file}")

                            return [dm_data]

                        except json.JSONDecodeError:
                            print(f"❌ DM response not JSON")
                    else:
                        print(f"❌ DM request failed: {dm_response.status_code}")

                # Save profile HTML for analysis
                profile_file = f"{self.output_dir}/profile_analysis_{int(time.time())}.html"
                with open(profile_file, 'w') as f:
                    f.write(response.text)
                print(f"📁 Profile HTML saved: {profile_file}")

            else:
                print(f"❌ Profile not accessible: {response.status_code}")

        except Exception as e:
            print(f"❌ Profile extraction error: {e}")

        return []

    def setup_real_database(self):
        """Setup database for real DM data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS real_dm_threads (
                thread_id TEXT PRIMARY KEY,
                target_user TEXT,
                participants TEXT,
                last_activity TEXT,
                message_count INTEGER,
                extraction_method TEXT,
                raw_data TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS real_dm_messages (
                message_id TEXT PRIMARY KEY,
                thread_id TEXT,
                sender TEXT,
                recipient TEXT,
                content TEXT,
                timestamp TEXT,
                message_type TEXT,
                raw_message_data TEXT
            )
        ''')

        conn.commit()
        conn.close()
        print("✅ Real DM database setup complete")

    def save_real_dm_data(self, conversations):
        """Save real DM data to database and files"""
        if not conversations:
            print("❌ No real DM data to save")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save JSON
        json_file = f"{self.output_dir}/real_dm_extraction_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(conversations, f, indent=2)

        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        total_messages = 0
        for conv in conversations:
            thread_data = conv.get('thread_data', {})
            thread_id = conv.get('thread_id', f'thread_{int(time.time())}')

            # Extract messages from thread
            messages = thread_data.get('items', []) or thread_data.get('messages', [])
            total_messages += len(messages)

            # Save thread
            cursor.execute('''
                INSERT OR REPLACE INTO real_dm_threads
                (thread_id, target_user, participants, last_activity, message_count, extraction_method, raw_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                thread_id,
                self.target,
                json.dumps(thread_data.get('users', [])),
                datetime.now().isoformat(),
                len(messages),
                conv.get('source_endpoint', 'api_extraction'),
                json.dumps(thread_data)
            ))

            # Save messages
            for msg in messages:
                msg_id = msg.get('item_id') or msg.get('id') or f'msg_{int(time.time())}'
                sender = msg.get('user_id') or 'unknown'
                content = msg.get('text') or str(msg.get('item_type', 'unknown'))

                cursor.execute('''
                    INSERT OR REPLACE INTO real_dm_messages
                    (message_id, thread_id, sender, recipient, content, timestamp, message_type, raw_message_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    msg_id,
                    thread_id,
                    sender,
                    self.target,
                    content,
                    msg.get('timestamp') or datetime.now().isoformat(),
                    msg.get('item_type', 'text'),
                    json.dumps(msg)
                ))

        conn.commit()
        conn.close()

        print(f"\n📊 REAL DM EXTRACTION SUMMARY")
        print("=" * 50)
        print(f"✅ Conversations found: {len(conversations)}")
        print(f"✅ Real messages: {total_messages}")
        print(f"📁 JSON file: {json_file}")
        print(f"🗄️ Database: {self.db_path}")

        return json_file

    def run_real_extraction(self):
        """Run complete real DM extraction"""
        print("🚀 Starting REAL DM extraction - NO SIMULATION")

        # Load real sessions
        sessions = self.load_real_session_credentials()
        if not sessions:
            print("❌ No valid session credentials found")
            return None

        # Setup database
        self.setup_real_database()

        all_conversations = []

        # Test each session
        for session_info in sessions:
            is_valid, session_obj = self.test_session_validity(session_info)

            if is_valid:
                print(f"✅ Valid session found: {os.path.basename(session_info['source'])}")

                # Try API extraction
                api_conversations = self.extract_real_dms_with_api(session_obj)
                all_conversations.extend(api_conversations)

                # Try profile extraction
                profile_conversations = self.extract_real_dms_from_profile(session_obj)
                all_conversations.extend(profile_conversations)

                if api_conversations or profile_conversations:
                    print(f"✅ Real data found with this session!")
                    break
            else:
                print(f"❌ Invalid session: {os.path.basename(session_info['source'])}")

        # Save real results
        if all_conversations:
            result_file = self.save_real_dm_data(all_conversations)
            print(f"\n🎉 SUCCESS: Real DM data extracted!")
            return result_file
        else:
            print(f"\n❌ FAILED: No real DM data found")
            print("💡 All sessions may be expired or Instagram may have blocked access")
            return None

if __name__ == "__main__":
    extractor = RealAlxDMExtractor()
    result = extractor.run_real_extraction()

    if result:
        print(f"\n✅ Real DM extraction completed successfully")
        print(f"📁 Results: {result}")
    else:
        print(f"\n❌ Real DM extraction failed")
        print("🔧 May need fresh session credentials or different approach")
