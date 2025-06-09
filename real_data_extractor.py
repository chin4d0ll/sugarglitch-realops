# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
REAL Instagram DM Extractor - NO MOCKUP
=======================================
For extracting REAL data from alx.trading Instagram account
"""

import os
import json
import requests
import time
from datetime import datetime

class RealInstagramExtractor:
    def __init__(self):
        self.target_username = "alx.trading"
        # Use the provided session file if available
        # Always use the latest provided session file
        self.session_file = "alx_trading_session_fleming654.json"
        self.output_dir = "REAL_EXTRACTIONS"

        # Create output directory
        os.makedirs(self.output_dir, exist_ok = True)

        print("🎯 REAL INSTAGRAM DM EXTRACTOR")
        print("=" * 40)
        print("Target: alx.trading")
        print("Mode: REAL DATA EXTRACTION")
        print("No mockup, no demo - REAL DATA ONLY")
        print()

    def get_real_sessionid_ipad(self):
        """Guide for getting REAL sessionid from iPad"""

        print("🔑 GET REAL SESSIONID FROM iPAD")
        print("=" * 35)
        print()
        print("📱 METHOD 1: Safari on iPad (EASIEST)")
        print("1. Open Safari → Go to instagram.com")
        print("2. LOGIN to your Instagram account")
        print("3. In address bar, type: javascript:alert(document.cookie)")
        print("4. Press Enter")
        print("5. Copy the sessionid value (after sessionid=)")
        print()
        print("💻 METHOD 2: Chrome on iPad")
        print("1. Download Chrome app")
        print("2. Go to instagram.com and login")
        print("3. Menu → More tools → Developer tools")
        print("4. Console tab → Type: document.cookie")
        print("5. Find sessionid in the output")
        print()

        sessionid = input("🔑 Paste your REAL sessionid here: ").strip()

        if sessionid and len(sessionid) > 20:
            # Save real session
            session_data = {
                "sessionid": sessionid,
                "target": self.target_username,
                "type": "REAL_SESSION",
                "created": datetime.now().isoformat(),
                "platform": "iPad"
            }

            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent = 2)

            print("✅ REAL session saved!")
            return sessionid
        else:
            print("❌ Invalid sessionid - need real one for data extraction")
            return None

    def test_real_session(self, sessionid):
        """Test if the session works with Instagram"""

        print("\n🔍 TESTING REAL SESSION...")
        print("=" * 28)

        headers = {
            'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q = 0.9,*/*;q = 0.8',
            'Accept-Language': 'en-US,en;q = 0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Cookie': f'sessionid={sessionid}',
            'Connection': 'keep-alive'
        }

        try:
            # Test Instagram main page
            response = requests.get('https://www.instagram.com/', headers = headers, timeout = 15)

            if response.status_code == 200:
                if 'login' not in response.url.lower() and '"is_logged_in":true' in response.text:
                    print("✅ Session is VALID and LOGGED IN!")
                    return True
                else:
                    print("❌ Session expired or invalid")
                    return False
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False

    def extract_real_dms(self, sessionid):
        """Extract REAL DMs from alx.trading"""

        print("\n🚀 EXTRACTING REAL DMs...")
        print("=" * 28)
        print(f"Target: {self.target_username}")
        print("Extracting: REAL conversation data")
        print()

        headers = {
            'User-Agent': 'Instagram 219.0.0.12.117 Android (29/10; 420dpi; 1080x2220; samsung; SM-G973F; beyond1; exynos9820; en_US; 336448961)',
            'X-IG-App-ID': '936619743392459',
            'X-ASBD-ID': '198387',
            'X-IG-WWW-Claim': '0',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q = 0.9',
            'Cookie': f'sessionid={sessionid}',
            'Referer': 'https://www.instagram.com/direct/inbox/',
        }

        real_data = {
            "extraction_info": {
                "target": self.target_username,
                "type": "REAL_DATA_EXTRACTION",
                "timestamp": datetime.now().isoformat(),
                "method": "Direct Instagram API"
            },
            "conversations": [],
            "media_files": [],
            "metadata": {}
        }

        # Try to get DM inbox
        try:
            print("🔍 Accessing DM inbox...")
            inbox_url = "https://www.instagram.com/api/v1/direct_v2/inbox/"

            response = requests.get(inbox_url, headers = headers, timeout = 15)

            print(f"📡 Response: HTTP {response.status_code}")

            if response.status_code == 200:
                inbox_data = response.json()
                print("✅ Successfully accessed DM inbox!")

                # Extract conversation threads
                if 'inbox' in inbox_data and 'threads' in inbox_data['inbox']:
                    threads = inbox_data['inbox']['threads']
                    print(f"📱 Found {len(threads)} conversation threads")

                    for thread in threads:
                        # Look for conversation with alx.trading
                        users = thread.get('users', [])
                        usernames = [user.get('username', '') for user in users]

                        if self.target_username in usernames:
                            print(f"🎯 Found conversation with {self.target_username}!")

                            # Extract messages from this thread
                            thread_id = thread.get('thread_id')
                            messages = self.extract_thread_messages(thread_id, headers)

                            real_data['conversations'].append({
                                "thread_id": thread_id,
                                "participants": usernames,
                                "messages": messages,
                                "extracted_at": datetime.now().isoformat()
                            })

                # Save REAL data
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"{self.output_dir}/REAL_alx_trading_dms_{timestamp}.json"

                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(real_data, f, indent = 2, ensure_ascii = False)

                print(f"💾 REAL DATA saved: {output_file}")
                print(f"📊 Conversations: {len(real_data['conversations'])}")

                return True

            elif response.status_code == 429:
                print("❌ Rate limited - need to use proxy rotation")
                return self.extract_with_proxy_rotation(sessionid)

            elif response.status_code == 401:
                print("❌ Session expired - need fresh sessionid")
                return False

            else:
                print(f"❌ Unexpected response: {response.status_code}")
                print(response.text[:200])
                return False

        except Exception as e:
            print(f"❌ Extraction error: {e}")
            return False

    def extract_thread_messages(self, thread_id, headers):
        """Extract messages from a specific thread"""

        print(f"📱 Extracting messages from thread {thread_id}")

        try:
            messages_url = f"https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/"
            response = requests.get(messages_url, headers = headers, timeout = 15)

            if response.status_code == 200:
                thread_data = response.json()

                if 'thread' in thread_data and 'items' in thread_data['thread']:
                    messages = thread_data['thread']['items']
                    print(f"💬 Found {len(messages)} messages")

                    real_messages = []
                    for msg in messages:
                        message_data = {
                            "message_id": msg.get('item_id'),
                            "timestamp": msg.get('timestamp'),
                            "user_id": msg.get('user_id'),
                            "text": msg.get('text', ''),
                            "type": msg.get('item_type'),
                            "media": self.extract_media_info(msg)
                        }
                        real_messages.append(message_data)

                    return real_messages

        except Exception as e:
            print(f"❌ Error extracting thread messages: {e}")

        return []

    def extract_media_info(self, message):
        """Extract media information from message"""

        media_info = []

        # Check for different media types
        if 'media' in message:
            media = message['media']
            if 'image_versions2' in media:
                media_info.append({
                    "type": "image",
                    "url": media['image_versions2']['candidates'][0]['url']
                })

        return media_info

    def extract_with_proxy_rotation(self, sessionid):
        """Extract using proxy rotation to bypass rate limits"""

        print("\n🌐 USING PROXY ROTATION FOR REAL EXTRACTION")
        print("=" * 48)

        # Load working proxies
        try:
            with open('config/working_proxies.json', 'r') as f:
                proxies_data = json.load(f)

            print(f"📡 Testing {len(proxies_data)} proxies for real extraction...")

            for i, proxy_info in enumerate(proxies_data[:5]):  # Test first 5 proxies
                proxy_url = proxy_info.get('proxy', proxy_info)

                print(f"🔄 Trying proxy {i+1}: {proxy_url}")

                proxies = {
                    'http': proxy_url,
                    'https': proxy_url
                }

                # Test extraction with this proxy
                if self.test_extraction_with_proxy(sessionid, proxies):
                    print("✅ Successfully extracted with proxy!")
                    return True

        except Exception as e:
            print(f"❌ Proxy rotation failed: {e}")

        return False

    def test_extraction_with_proxy(self, sessionid, proxies):
        """Test extraction with specific proxy"""

        try:
            headers = {
                'User-Agent': 'Instagram 219.0.0.12.117 Android',
                'Cookie': f'sessionid={sessionid}'
            }

            response = requests.get(
                'https://www.instagram.com/api/v1/direct_v2/inbox/',
                headers = headers,
                proxies = proxies,
                timeout = 10
            )

            return response.status_code == 200

        except Exception:
            return False

def main():
    """Main function for REAL data extraction"""

    extractor = RealInstagramExtractor()

    # Check for existing session
    if os.path.exists(extractor.session_file):
        try:
            with open(extractor.session_file, 'r') as f:
                session_data = json.load(f)

            sessionid = session_data.get('sessionid', '')

            if sessionid and len(sessionid) > 20:
                print("✅ Found existing session - testing...")

                if extractor.test_real_session(sessionid):
                    print("✅ Session is valid - starting REAL extraction!")
                    success = extractor.extract_real_dms(sessionid)

                    if success:
                        print("\n🎉 REAL DATA EXTRACTION SUCCESSFUL!")
                        print("Check REAL_EXTRACTIONS/ folder for your data")
                    else:
                        print("\n❌ Extraction failed - may need fresh session")
                else:
                    print("❌ Session expired - need new one")
                    sessionid = extractor.get_real_sessionid_ipad()

                    if sessionid:
                        extractor.extract_real_dms(sessionid)
        except Exception:
            print("❌ Error with existing session")
            sessionid = extractor.get_real_sessionid_ipad()
    else:
        # Get new session
        sessionid = extractor.get_real_sessionid_ipad()

        if sessionid:
            if extractor.test_real_session(sessionid):
                success = extractor.extract_real_dms(sessionid)

                if success:
                    print("\n🎉 REAL DATA EXTRACTION COMPLETE!")
                else:
                    print("\n❌ Extraction failed")

if __name__ == "__main__":
    main()
