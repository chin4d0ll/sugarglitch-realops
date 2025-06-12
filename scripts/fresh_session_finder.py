# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Fresh Session Finder for Instagram
This script helps you get a fresh sessionid from Instagram
"""

import os
import json
import sys
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
import requests

class FreshSessionFinder:
    def __init__(self):
        self.target_username = "alx.trading"
        self.session_file = "tools/session_alx_trading.json"
        self.output_dir = "real_extraction/alx_trading"

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok = True)
        os.makedirs("tools", exist_ok = True)

    def manual_session_input(self):
        """Allow user to manually input session data"""
        print("\n" + "="*60)
        print("MANUAL SESSION INPUT")
        print("="*60)
        print("Please provide your Instagram session information:")
        print("You can get this from your browser's developer tools > Application > Cookies")
        print("\nRequired cookies from instagram.com:")
        print("- sessionid (most important)")
        print("- csrftoken")
        print("- ds_user_id")
        print("\nOptional but helpful:")
        print("- mid, ig_did, shbid, rur")

        session_data = {}

        # Get sessionid (required)
        while True:
            sessionid = input("\nEnter sessionid: ").strip()
            if sessionid:
                session_data['sessionid'] = sessionid
                break
            print("Sessionid is required!")

        # Get other cookies
        csrftoken = input("Enter csrftoken (optional): ").strip()
        if csrftoken:
            session_data['csrftoken'] = csrftoken

        ds_user_id = input("Enter ds_user_id (optional): ").strip()
        if ds_user_id:
            session_data['ds_user_id'] = ds_user_id

        mid = input("Enter mid (optional): ").strip()
        if mid:
            session_data['mid'] = mid

        return session_data

    def test_session_validity(self, session_data):
        """Test if session is valid and can access DMs"""
        print(f"\n🔍 Testing session validity...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q = 0.9,image/webp,*/*;q = 0.8',
            'Accept-Language': 'en-US,en;q = 0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        # Convert session data to cookie string
        cookie_parts = []
        for key, value in session_data.items():
            cookie_parts.append(f"{key}={value}")
        cookie_string = "; ".join(cookie_parts)
        headers['Cookie'] = cookie_string

        try:
            # Test 1: Check if we can access Instagram main page
            print("Testing main page access...")
            response = requests.get('https://www.instagram.com/', headers = headers, timeout = 10)

            if response.status_code == 200:
                if 'login' in response.url.lower():
                    print("❌ Session expired - redirected to login")
                    return False
                else:
                    print("✅ Main page accessible")
            else:
                print(f"❌ Main page access failed: {response.status_code}")
                return False

            # Test 2: Check if we can access direct messages
            print("Testing DM access...")
            dm_response = requests.get('https://www.instagram.com/direct/inbox/', headers = headers, timeout = 10)

            if dm_response.status_code == 200:
                if 'login' in dm_response.url.lower():
                    print("❌ Cannot access DMs - redirected to login")
                    return False
                else:
                    print("✅ DM access successful")
                    return True
            else:
                print(f"❌ DM access failed: {dm_response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"❌ Network error during session test: {e}")
            return False

    def save_session(self, session_data):
        """Save session data to file"""
        session_info = {
            'sessionid': session_data.get('sessionid', ''),
            'csrftoken': session_data.get('csrftoken', ''),
            'ds_user_id': session_data.get('ds_user_id', ''),
            'mid': session_data.get('mid', ''),
            'ig_did': session_data.get('ig_did', ''),
            'shbid': session_data.get('shbid', ''),
            'rur': session_data.get('rur', ''),
            'created_at': datetime.now().isoformat(),
            'target': self.target_username,
            'status': 'active'
        }

        try:
            with open(self.session_file, 'w') as f:
                json.dump(session_info, f, indent = 2)
            print(f"✅ Session saved to {self.session_file}")
            return True
        except Exception as e:
            print(f"❌ Failed to save session: {e}")
            return False

    def playwright_session_capture(self):
        """Use Playwright to help capture session (requires manual login)"""
        print("\n" + "="*60)
        print("PLAYWRIGHT SESSION CAPTURE")
        print("="*60)
        print("This will open Instagram in a browser window.")
        print("Please log in manually, then press Enter in this terminal.")

        input("Press Enter to continue...")

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless = False, args=['--no-sandbox'])
                context = browser.new_context()
                page = context.new_page()

                print("Opening Instagram...")
                page.goto('https://www.instagram.com/')

                print("\n" + "="*50)
                print("MANUAL LOGIN REQUIRED")
                print("="*50)
                print("1. Log in to your Instagram account in the browser")
                print("2. Navigate to instagram.com/direct/inbox/")
                print("3. Make sure you can see your DMs")
                print("4. Come back to this terminal and press Enter")

                input("\nPress Enter after you've logged in and can see DMs...")

                # Extract cookies
                cookies = context.cookies()
                session_data = {}

                for cookie in cookies:
                    if cookie['name'] in ['sessionid', 'csrftoken', 'ds_user_id', 'mid', 'ig_did', 'shbid', 'rur']:
                        session_data[cookie['name']] = cookie['value']

                browser.close()

                if 'sessionid' in session_data:
                    print(f"✅ Captured sessionid: {session_data['sessionid'][:20]}...")
                    return session_data
                else:
                    print("❌ No sessionid found in cookies")
                    return None

        except Exception as e:
            print(f"❌ Playwright session capture failed: {e}")
            return None

    def extract_dms_with_session(self, session_data):
        """Extract DMs using the valid session"""
        print(f"\n🔄 Extracting DMs from {self.target_username}...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q = 0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-CSRFToken': session_data.get('csrftoken', ''),
            'X-IG-App-ID': '936619743392459',
            'X-IG-WWW-Claim': '0',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Referer': 'https://www.instagram.com/direct/inbox/',
        }

        # Convert session data to cookie string
        cookie_parts = []
        for key, value in session_data.items():
            cookie_parts.append(f"{key}={value}")
        headers['Cookie'] = "; ".join(cookie_parts)

        try:
            # First, get the user ID of the target
            print(f"Looking up user ID for {self.target_username}...")
            user_url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={self.target_username}'
            user_response = requests.get(user_url, headers = headers, timeout = 10)

            if user_response.status_code == 200:
                user_data = user_response.json()
                if 'data' in user_data and 'user' in user_data['data']:
                    target_user_id = user_data['data']['user']['id']
                    print(f"✅ Found user ID: {target_user_id}")
                else:
                    print("❌ Could not find user data")
                    return False
            else:
                print(f"❌ Failed to get user info: {user_response.status_code}")
                return False

            # Get threads (conversations)
            print("Fetching DM threads...")
            threads_url = 'https://www.instagram.com/api/v1/direct_v2/inbox/?persistentBadging = true&folder=&limit = 20'
            threads_response = requests.get(threads_url, headers = headers, timeout = 10)

            if threads_response.status_code == 200:
                threads_data = threads_response.json()
                print(f"✅ Found {len(threads_data.get('inbox', {}).get('threads', []))} threads")

                # Look for conversation with target user
                target_thread = None
                for thread in threads_data.get('inbox', {}).get('threads', []):
                    for user in thread.get('users', []):
                        if user.get('pk') == target_user_id:
                            target_thread = thread
                            break
                    if target_thread:
                        break

                if target_thread:
                    thread_id = target_thread['thread_id']
                    print(f"✅ Found conversation thread: {thread_id}")

                    # Get messages from this thread
                    messages_url = f'https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/?limit = 50'
                    messages_response = requests.get(messages_url, headers = headers, timeout = 10)

                    if messages_response.status_code == 200:
                        messages_data = messages_response.json()
                        messages = messages_data.get('thread', {}).get('items', [])

                        print(f"✅ Extracted {len(messages)} messages!")

                        # Save results
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_file = os.path.join(self.output_dir, f"real_dms_{timestamp}.json")

                        extraction_result = {
                            'target': self.target_username,
                            'target_user_id': target_user_id,
                            'thread_id': thread_id,
                            'extraction_time': datetime.now().isoformat(),
                            'message_count': len(messages),
                            'messages': messages,
                            'status': 'success'
                        }

                        with open(output_file, 'w', encoding='utf-8') as f:
                            json.dump(extraction_result, f, indent = 2, ensure_ascii = False)

                        print(f"✅ Results saved to: {output_file}")

                        # Print summary
                        print(f"\n📊 EXTRACTION SUMMARY:")
                        print(f"Target: {self.target_username}")
                        print(f"Messages: {len(messages)}")
                        print(f"Thread ID: {thread_id}")
                        print(f"File: {output_file}")

                        return True
                    else:
                        print(f"❌ Failed to get messages: {messages_response.status_code}")
                        return False
                else:
                    print(f"❌ No conversation found with {self.target_username}")
                    return False
            else:
                print(f"❌ Failed to get threads: {threads_response.status_code}")
                return False

        except Exception as e:
            print(f"❌ DM extraction failed: {e}")
            return False

    def run(self):
        """Main execution flow"""
        print("🔍 FRESH SESSION FINDER FOR INSTAGRAM DM EXTRACTION")
        print("="*60)
        print(f"Target: {self.target_username}")
        print(f"Output: {self.output_dir}")
        print()

        while True:
            print("Choose an option:")
            print("1. Manual session input (recommended)")
            print("2. Playwright session capture (opens browser)")
            print("3. Exit")

            choice = input("\nEnter choice (1-3): ").strip()

            if choice == '1':
                session_data = self.manual_session_input()
                if session_data and self.test_session_validity(session_data):
                    if self.save_session(session_data):
                        print("\n🎉 Session is valid and saved!")
                        if input("Extract DMs now? (y/n): ").lower().startswith('y'):
                            self.extract_dms_with_session(session_data)
                        break

            elif choice == '2':
                session_data = self.playwright_session_capture()
                if session_data and self.test_session_validity(session_data):
                    if self.save_session(session_data):
                        print("\n🎉 Session captured and saved!")
                        if input("Extract DMs now? (y/n): ").lower().startswith('y'):
                            self.extract_dms_with_session(session_data)
                        break

            elif choice == '3':
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        finder = FreshSessionFinder()
        finder.run()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
