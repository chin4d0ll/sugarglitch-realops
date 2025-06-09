# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🎯 MANUAL DM EXTRACTOR - Interactive Session Input
Extract real Instagram DMs with fresh session input
"""

import json
import requests
import time
from datetime import datetime
import os

class ManualDMExtractor:
    def __init__(self):
        self.target = "alx.trading"
        self.output_dir = "/workspaces/sugarglitch-realops/data/manual_extraction"

        os.makedirs(self.output_dir, exist_ok=True)

        print("🎯 MANUAL DM EXTRACTOR - Interactive Session Input")
        print("=" * 60)
        print(f"Target: {self.target}")
        print()
        print("📋 Instructions:")
        print("1. Open Instagram in your browser")
        print("2. Login to your account")
        print("3. Open Developer Tools (F12)")
        print("4. Go to Application/Storage > Cookies > .instagram.com")
        print("5. Copy the 'sessionid' value")
        print()

    def get_session_input(self):
        """Get session input from user"""
        print("🔑 Please enter your Instagram sessionid:")
        print("(This should be a long string starting with numbers)")
        print()

        sessionid = input("Sessionid: ").strip()

        if not sessionid:
            print("❌ No sessionid provided")
            return None

        if len(sessionid) < 20:
            print("⚠️ Sessionid seems too short, but continuing anyway...")

        return sessionid

    def test_session(self, sessionid):
        """Test if session is valid"""
        print("\n🧪 Testing session validity...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        cookies = {
            'sessionid': sessionid
        }

        session = requests.Session()
        session.cookies.update(cookies)
        session.headers.update(headers)

        try:
            response = session.get('https://www.instagram.com/', timeout=10)
            print(f"Instagram main page: {response.status_code}")

            if response.status_code == 200:
                if 'login' in response.url.lower():
                    print("❌ Session expired - redirected to login")
                    return False
                elif '"viewer"' in response.text or '"user"' in response.text:
                    print("✅ Session appears valid")
                    return True
                else:
                    print("⚠️ Uncertain session status, but continuing...")
                    return True
            else:
                print(f"❌ Bad status code: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Session test failed: {e}")
            return False

    def get_user_id(self, sessionid):
        """Try to get current user ID"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'X-Requested-With': 'XMLHttpRequest',
        }

        cookies = {
            'sessionid': sessionid
        }

        session = requests.Session()
        session.cookies.update(cookies)
        session.headers.update(headers)

        try:
            # Try to get user info from accounts endpoint
            response = session.get('https://www.instagram.com/api/v1/accounts/edit/web_form_data/', timeout=10)

            if response.status_code == 200:
                data = response.json()
                if 'form_data' in data and 'username' in data['form_data']:
                    username = data['form_data']['username']
                    print(f"✅ Logged in as: {username}")
                    return username

            print("⚠️ Could not determine username")
            return "unknown_user"

        except Exception as e:
            print(f"⚠️ Could not get user info: {e}")
            return "unknown_user"

    def search_for_target_user(self, sessionid):
        """Search for target user"""
        print(f"\n🔍 Searching for {self.target}...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'X-Requested-With': 'XMLHttpRequest',
        }

        cookies = {
            'sessionid': sessionid
        }

        session = requests.Session()
        session.cookies.update(cookies)
        session.headers.update(headers)

        try:
            # Search for user
            search_url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={self.target}'
            response = session.get(search_url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'user' in data['data']:
                    user_info = data['data']['user']
                    user_id = user_info.get('id')
                    username = user_info.get('username')
                    print(f"✅ Found user: {username} (ID: {user_id})")
                    return user_id
                else:
                    print(f"❌ User {self.target} not found")
                    return None
            else:
                print(f"❌ Search failed: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Error searching for user: {e}")
            return None

    def extract_direct_messages(self, sessionid, target_user_id):
        """Extract direct messages"""
        print(f"\n📥 Extracting direct messages...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'X-Requested-With': 'XMLHttpRequest',
        }

        cookies = {
            'sessionid': sessionid
        }

        session = requests.Session()
        session.cookies.update(cookies)
        session.headers.update(headers)

        try:
            # Get inbox
            inbox_url = 'https://www.instagram.com/api/v1/direct_v2/inbox/'
            response = session.get(inbox_url, timeout=15)

            print(f"Inbox API response: {response.status_code}")

            if response.status_code == 200:
                inbox_data = response.json()
                threads = inbox_data.get('inbox', {}).get('threads', [])
                print(f"✅ Found {len(threads)} conversation threads")

                # Look for our target
                target_thread = None
                for thread in threads:
                    users = thread.get('users', [])
                    for user in users:
                        if user.get('pk') == target_user_id or user.get('username') == self.target:
                            target_thread = thread
                            print(f"🎯 Found target thread!")
                            break
                    if target_thread:
                        break

                if target_thread:
                    return self.extract_thread_messages(session, target_thread)
                else:
                    print(f"❌ No conversation found with {self.target}")

                    # Show available conversations for debugging
                    print("\n📋 Available conversations:")
                    for i, thread in enumerate(threads[:5]):  # Show first 5
                        users = thread.get('users', [])
                        usernames = [u.get('username', 'unknown') for u in users]
                        print(f"  {i+1}. {', '.join(usernames)}")

                    return None
            else:
                print(f"❌ Failed to get inbox: {response.status_code}")
                if response.status_code == 401:
                    print("Session may be expired or invalid")
                return None

        except Exception as e:
            print(f"❌ Error extracting DMs: {e}")
            return None

    def extract_thread_messages(self, session, thread):
        """Extract messages from thread"""
        thread_id = thread.get('thread_id')
        print(f"💬 Extracting messages from thread {thread_id}...")

        try:
            # Get thread messages
            messages_url = f'https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/'
            response = session.get(messages_url, timeout=15)

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
                        'created_at': datetime.fromtimestamp(msg.get('timestamp', 0) / 1000000).isoformat() if msg.get('timestamp') else None
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
        output_file = f"{self.output_dir}/manual_dm_extraction_{timestamp}.json"

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"\n✅ Results saved to: {output_file}")
            print(f"📊 Total messages extracted: {data.get('total_messages', 0)}")

            # Show sample messages
            messages = data.get('messages', [])
            if messages:
                print(f"\n📝 Sample messages (showing first 3):")
                for i, msg in enumerate(messages[:3]):
                    text = msg.get('text', '')[:50]
                    timestamp = msg.get('created_at', 'No timestamp')
                    print(f"  {i+1}. [{timestamp}] {text}...")

        except Exception as e:
            print(f"❌ Error saving results: {e}")

    def run(self):
        """Main extraction process"""
        # Get session from user
        sessionid = self.get_session_input()
        if not sessionid:
            return

        # Test session
        if not self.test_session(sessionid):
            print("❌ Session is not valid, please get a fresh sessionid")
            return

        # Get current user info
        current_user = self.get_user_id(sessionid)

        # Search for target user
        target_user_id = self.search_for_target_user(sessionid)
        if not target_user_id:
            print(f"❌ Could not find user {self.target}")
            return

        # Extract DMs
        results = self.extract_direct_messages(sessionid, target_user_id)

        # Save results
        self.save_results(results)

        if results and results.get('total_messages', 0) > 0:
            print("\n🎉 SUCCESS! Real DM data extracted!")
        else:
            print("\n❌ No messages found or extraction failed")

if __name__ == "__main__":
    extractor = ManualDMExtractor()
    extractor.run()
