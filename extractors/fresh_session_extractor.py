# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Fresh Session ALX.Trading DM Extractor
=====================================
Use this script when fresh, valid session tokens become available.
This script will immediately attempt real DM extraction using new sessions.
"""

import json
import sqlite3
import requests
import os
from datetime import datetime
import time

class FreshSessionExtractor:
    def __init__(self):
        self.target_username = "alx.trading"
        self.base_url = "https://www.instagram.com"
        self.api_url = "https://i.instagram.com/api/v1"
        self.session = requests.Session()
        self.results = []

    def setup_session(self, session_data):
        """Setup session with fresh credentials"""
        print(f"🔑 Setting up fresh session...")

        # Set cookies from session data
        if 'cookies' in session_data:
            for cookie in session_data['cookies']:
                self.session.cookies.set(cookie['name'], cookie['value'])

        # Set headers
        headers = {
            'User-Agent': 'Instagram 219.0.0.12.117 Android',
            'X-IG-App-ID': '936619743392459',
            'X-ASBD-ID': '129477',
            'X-IG-WWW-Claim': '0',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }

        if 'csrf_token' in session_data:
            headers['X-CSRFToken'] = session_data['csrf_token']

        self.session.headers.update(headers)

    def verify_session(self):
        """Verify session is valid and active"""
        print(f"✅ Verifying session validity...")

        try:
            # Test with user info endpoint
            response = self.session.get(f"{self.base_url}/api/v1/users/web_profile_info/?username={self.target_username}")

            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'user' in data['data']:
                    print(f"✅ Session valid! Found user: {self.target_username}")
                    return True

            print(f"❌ Session verification failed: {response.status_code}")
            return False

        except Exception as e:
            print(f"❌ Session verification error: {e}")
            return False

    def get_user_id(self):
        """Get target user ID"""
        print(f"🔍 Getting user ID for {self.target_username}...")

        try:
            response = self.session.get(f"{self.base_url}/api/v1/users/web_profile_info/?username={self.target_username}")

            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'user' in data['data']:
                    user_id = data['data']['user']['id']
                    print(f"✅ Found user ID: {user_id}")
                    return user_id

            print(f"❌ Failed to get user ID: {response.status_code}")
            return None

        except Exception as e:
            print(f"❌ Error getting user ID: {e}")
            return None

    def extract_dm_threads(self, user_id):
        """Extract DM threads for the target user"""
        print(f"📨 Extracting DM threads...")

        try:
            # Get inbox threads
            response = self.session.get(f"{self.api_url}/direct_v2/inbox/")

            if response.status_code == 200:
                data = response.json()
                threads = data.get('inbox', {}).get('threads', [])

                target_threads = []
                for thread in threads:
                    # Check if thread involves target user
                    for user in thread.get('users', []):
                        if user.get('username') == self.target_username:
                            target_threads.append(thread)
                            break

                print(f"✅ Found {len(target_threads)} threads with {self.target_username}")
                return target_threads

            print(f"❌ Failed to get threads: {response.status_code}")
            return []

        except Exception as e:
            print(f"❌ Error extracting threads: {e}")
            return []

    def extract_thread_messages(self, thread_id):
        """Extract messages from a specific thread"""
        print(f"💬 Extracting messages from thread {thread_id}...")

        try:
            response = self.session.get(f"{self.api_url}/direct_v2/threads/{thread_id}/")

            if response.status_code == 200:
                data = response.json()
                messages = data.get('thread', {}).get('items', [])
                print(f"✅ Found {len(messages)} messages in thread")
                return messages

            print(f"❌ Failed to get messages: {response.status_code}")
            return []

        except Exception as e:
            print(f"❌ Error extracting messages: {e}")
            return []

    def save_results(self, extraction_data):
        """Save extracted data to JSON and SQLite"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create directories
        os.makedirs("/workspaces/sugarglitch-realops/data/fresh_extraction", exist_ok=True)

        # Save JSON
        json_file = f"/workspaces/sugarglitch-realops/data/fresh_extraction/alx_trading_dms_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(extraction_data, f, indent=2, ensure_ascii=False)

        # Save SQLite
        db_file = f"/workspaces/sugarglitch-realops/data/fresh_extraction/alx_trading_dms_{timestamp}.db"
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dm_threads (
                thread_id TEXT PRIMARY KEY,
                participants TEXT,
                last_activity TEXT,
                message_count INTEGER,
                extraction_timestamp TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dm_messages (
                message_id TEXT PRIMARY KEY,
                thread_id TEXT,
                sender_username TEXT,
                message_text TEXT,
                timestamp TEXT,
                message_type TEXT,
                extraction_timestamp TEXT
            )
        ''')

        # Insert data
        for thread_data in extraction_data.get('threads', []):
            cursor.execute('''
                INSERT OR REPLACE INTO dm_threads
                (thread_id, participants, last_activity, message_count, extraction_timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                thread_data.get('thread_id', ''),
                json.dumps(thread_data.get('participants', [])),
                thread_data.get('last_activity', ''),
                len(thread_data.get('messages', [])),
                timestamp
            ))

            for message in thread_data.get('messages', []):
                cursor.execute('''
                    INSERT OR REPLACE INTO dm_messages
                    (message_id, thread_id, sender_username, message_text, timestamp, message_type, extraction_timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    message.get('item_id', ''),
                    thread_data.get('thread_id', ''),
                    message.get('user', {}).get('username', ''),
                    message.get('text', ''),
                    message.get('timestamp', ''),
                    message.get('item_type', ''),
                    timestamp
                ))

        conn.commit()
        conn.close()

        print(f"✅ Results saved:")
        print(f"   JSON: {json_file}")
        print(f"   SQLite: {db_file}")

        return json_file, db_file

    def run_extraction(self, session_file_path):
        """Main extraction process"""
        print(f"🚀 FRESH SESSION ALX.TRADING DM EXTRACTION")
        print(f"=" * 50)
        print(f"Target: {self.target_username}")
        print(f"Session: {session_file_path}")
        print(f"Time: {datetime.now()}")
        print()

        # Load session data
        try:
            with open(session_file_path, 'r') as f:
                session_data = json.load(f)
            print(f"✅ Loaded session data from {session_file_path}")
        except Exception as e:
            print(f"❌ Failed to load session: {e}")
            return False

        # Setup session
        self.setup_session(session_data)

        # Verify session
        if not self.verify_session():
            print(f"❌ Session is invalid or expired")
            return False

        # Get user ID
        user_id = self.get_user_id()
        if not user_id:
            print(f"❌ Could not get user ID for {self.target_username}")
            return False

        # Extract DM threads
        threads = self.extract_dm_threads(user_id)
        if not threads:
            print(f"❌ No DM threads found with {self.target_username}")
            return False

        # Extract messages from each thread
        extraction_data = {
            'target_username': self.target_username,
            'extraction_timestamp': datetime.now().isoformat(),
            'total_threads': len(threads),
            'threads': []
        }

        for thread in threads:
            thread_id = thread.get('thread_id')
            messages = self.extract_thread_messages(thread_id)

            thread_data = {
                'thread_id': thread_id,
                'participants': [user.get('username') for user in thread.get('users', [])],
                'last_activity': thread.get('last_activity_at'),
                'messages': messages
            }

            extraction_data['threads'].append(thread_data)

        # Save results
        json_file, db_file = self.save_results(extraction_data)

        print(f"\n🎉 EXTRACTION COMPLETED SUCCESSFULLY!")
        print(f"📊 Summary:")
        print(f"   - Threads: {len(extraction_data['threads'])}")
        print(f"   - Total Messages: {sum(len(t['messages']) for t in extraction_data['threads'])}")
        print(f"   - JSON Output: {json_file}")
        print(f"   - Database: {db_file}")

        return True

def main():
    """Main function - run when fresh session becomes available"""
    print("🔄 FRESH SESSION DM EXTRACTOR")
    print("Waiting for fresh session file...")

    # Check for fresh session files
    session_dirs = [
        "/workspaces/sugarglitch-realops/hijacked_sessions",
        "/workspaces/sugarglitch-realops/config/sessions",
        "/workspaces/sugarglitch-realops/fresh_sessions"
    ]

    extractor = FreshSessionExtractor()

    # For now, just prepare the extractor
    print("✅ Fresh session extractor ready!")
    print("📝 To use:")
    print("   1. Place fresh session file in one of the session directories")
    print("   2. Call: extractor.run_extraction('/path/to/fresh/session.json')")
    print("   3. Real DM data will be extracted if session is valid")

    return extractor

if __name__ == "__main__":
    main()
