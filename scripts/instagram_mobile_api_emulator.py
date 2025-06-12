# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Instagram Mobile API Emulator 2025
Emulates Instagram mobile app to access DM content
"""

import requests
import json
import time
import hashlib
import hmac
import uuid
import random
import logging
from datetime import datetime
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/mobile_api_emulator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class InstagramMobileAPIEmulator:
    def __init__(self):
        self.session = requests.Session()
        self.results_dir = "results/mobile_api"
        self.proxies_file = "config/proxies.json"

        # Create directories
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs("logs", exist_ok=True)

        # Instagram mobile API constants
        self.api_url = "https://i.instagram.com/api/v1"
        self.app_version = "302.0.0.23.108"
        self.android_version = "28"
        self.android_release = "9"
        self.dpi = "480dpi"
        self.resolution = "1080x2340"
        self.manufacturer = "samsung"
        self.device = "SM-G973F"
        self.model = "galaxy_s10"
        self.cpu = "exynos9820"

        # Generate device ID
        self.device_id = self.generate_device_id()
        self.uuid = str(uuid.uuid4())
        self.phone_id = str(uuid.uuid4())
        self.family_device_id = str(uuid.uuid4())

        # User agents
        self.user_agent = f"Instagram {self.app_version} Android ({self.android_version}/{self.android_release}; {self.dpi}; {self.resolution}; {self.manufacturer}; {self.device}; {self.model}; {self.cpu}; en_US; 458229237)"

        # Headers
        self.headers = {
            'User-Agent': self.user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'X-IG-Capabilities': '3brTvw==',
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Bandwidth-Speed-Kbps': str(random.randint(2000, 5000)),
            'X-IG-Bandwidth-TotalBytes-B': str(random.randint(5000000, 50000000)),
            'X-IG-Bandwidth-TotalTime-MS': str(random.randint(200, 1000)),
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
        }

        self.session.headers.update(self.headers)
        self.proxies = self.load_proxies()

    def generate_device_id(self):
        """Generate a fake device ID"""
        return 'android-' + hashlib.md5(str(random.random()).encode()).hexdigest()[:16]

    def load_proxies(self):
        """Load proxy configuration"""
        try:
            with open(self.proxies_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load proxies: {e}")
            return []

    def get_random_proxy(self):
        """Get a random working proxy"""
        if not self.proxies:
            return None

        working_proxies = [p for p in self.proxies if p.get('status') == 'working']
        if not working_proxies:
            working_proxies = self.proxies

        proxy = random.choice(working_proxies)
        return {
            'http': f"http://{proxy['ip']}:{proxy['port']}",
            'https': f"http://{proxy['ip']}:{proxy['port']}"
        }

    def generate_signature(self, data):
        """Generate Instagram signature"""
        try:
            body = json.dumps(data, separators=(',', ':'))
            key = '4f8732eb9ba7d1c8e8897a75d6474d4eb3f5279137431b2aafb71fcc6b769b2d'
            signature = hmac.new(key.encode(), body.encode(), hashlib.sha256).hexdigest()
            return f"ig_sig_key_version=4&signed_body={signature}.{body}"
        except Exception as e:
            logger.error(f"Failed to generate signature: {e}")
            return ""

    def login(self, username, password):
        """Login to Instagram using mobile API"""
        try:
            logger.info(f"Attempting login for user: {username}")

            # Set proxy
            proxy = self.get_random_proxy()
            if proxy:
                self.session.proxies.update(proxy)
                logger.info(f"Using proxy: {proxy}")

            # Pre-login request
            pre_login_data = {
                'phone_id': self.phone_id,
                '_csrftoken': 'missing',
                'username': username,
                'adid': str(uuid.uuid4()),
                'guid': self.uuid,
                'device_id': self.device_id,
                'google_tokens': '[]',
                'login_attempt_count': 0,
            }

            pre_login_payload = self.generate_signature(pre_login_data)

            pre_login_response = self.session.post(
                f"{self.api_url}/accounts/read_msisdn_header/",
                data=pre_login_payload,
                headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
            )

            logger.info(f"Pre-login response: {pre_login_response.status_code}")

            # Main login request
            login_data = {
                'phone_id': self.phone_id,
                '_csrftoken': 'missing',
                'username': username,
                'adid': str(uuid.uuid4()),
                'guid': self.uuid,
                'device_id': self.device_id,
                'password': password,
                'login_attempt_count': 0,
                'country_codes': '[{"country_code":"1","source":["default"]}]',
                'jazoest': '22328',
            }

            login_payload = self.generate_signature(login_data)

            login_response = self.session.post(
                f"{self.api_url}/accounts/login/",
                data=login_payload,
                headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
            )

            logger.info(f"Login response: {login_response.status_code}")

            if login_response.status_code == 200:
                response_data = login_response.json()
                if response_data.get('status') == 'ok':
                    logger.info("Login successful!")

                    # Extract session info
                    self.logged_in_user = response_data.get('logged_in_user', {})
                    self.user_id = self.logged_in_user.get('pk')

                    # Update headers with session token
                    self.session.headers.update({
                        'X-CSRFToken': login_response.cookies.get('csrftoken', ''),
                        'X-Instagram-AJAX': '1',
                    })

                    return True
                else:
                    logger.error(f"Login failed: {response_data}")
                    return False
            else:
                logger.error(f"Login request failed: {login_response.status_code}")
                return False

        except Exception as e:
            logger.error(f"Login error: {e}")
            return False

    def get_inbox(self):
        """Get DM inbox"""
        try:
            logger.info("Fetching DM inbox")

            response = self.session.get(f"{self.api_url}/direct_v2/inbox/")

            if response.status_code == 200:
                data = response.json()
                logger.info(f"Inbox response status: {data.get('status')}")
                return data
            else:
                logger.error(f"Inbox request failed: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Failed to get inbox: {e}")
            return None

    def get_thread_messages(self, thread_id):
        """Get messages from a specific thread"""
        try:
            logger.info(f"Fetching messages for thread: {thread_id}")

            response = self.session.get(f"{self.api_url}/direct_v2/threads/{thread_id}/")

            if response.status_code == 200:
                data = response.json()
                logger.info(f"Thread response status: {data.get('status')}")
                return data
            else:
                logger.error(f"Thread request failed: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Failed to get thread messages: {e}")
            return None

    def extract_all_dms(self):
        """Extract all DM conversations and messages"""
        try:
            logger.info("Starting DM extraction")

            # Get inbox
            inbox_data = self.get_inbox()
            if not inbox_data or inbox_data.get('status') != 'ok':
                logger.error("Failed to get inbox")
                return None

            threads = inbox_data.get('inbox', {}).get('threads', [])
            logger.info(f"Found {len(threads)} threads")

            all_conversations = []

            for i, thread in enumerate(threads[:10]):  # Limit to first 10 threads
                try:
                    thread_id = thread.get('thread_id')
                    thread_title = thread.get('thread_title', 'Unknown')

                    logger.info(f"Processing thread {i+1}: {thread_title}")

                    # Get thread messages
                    thread_data = self.get_thread_messages(thread_id)
                    if thread_data and thread_data.get('status') == 'ok':

                        # Extract messages
                        messages = []
                        thread_items = thread_data.get('thread', {}).get('items', [])

                        for item in thread_items:
                            try:
                                message_data = self.parse_message_item(item)
                                if message_data:
                                    messages.append(message_data)
                            except Exception as e:
                                logger.debug(f"Failed to parse message: {e}")

                        conversation = {
                            'thread_id': thread_id,
                            'thread_title': thread_title,
                            'users': thread.get('users', []),
                            'message_count': len(messages),
                            'messages': messages[:50],  # Limit to 50 messages per thread
                            'extracted_at': datetime.now().isoformat()
                        }

                        all_conversations.append(conversation)
                        logger.info(f"Extracted {len(messages)} messages from {thread_title}")

                    time.sleep(random.uniform(1, 3))  # Rate limiting

                except Exception as e:
                    logger.error(f"Failed to process thread {i+1}: {e}")

            return all_conversations

        except Exception as e:
            logger.error(f"DM extraction failed: {e}")
            return None

    def parse_message_item(self, item):
        """Parse individual message item"""
        try:
            user_id = item.get('user_id')
            timestamp = item.get('timestamp')
            item_type = item.get('item_type')

            # Handle different message types
            content = ""
            message_type = "unknown"

            if item_type == "text":
                content = item.get('text', '')
                message_type = "text"
            elif item_type == "media":
                media = item.get('media', {})
                content = f"[Media: {media.get('media_type', 'unknown')}]"
                message_type = "media"
            elif item_type == "link":
                link = item.get('link', {})
                content = f"[Link: {link.get('text', 'unknown')}]"
                message_type = "link"
            elif item_type == "like":
                content = "[Like]"
                message_type = "like"
            else:
                content = f"[{item_type}]"
                message_type = item_type

            return {
                'user_id': user_id,
                'timestamp': timestamp,
                'content': content,
                'type': message_type,
                'item_type': item_type
            }

        except Exception as e:
            logger.debug(f"Failed to parse message item: {e}")
            return None

    def run_extraction(self, username, password):
        """Run complete mobile API extraction"""
        logger.info("Starting Instagram Mobile API Extraction")

        try:
            # Login
            if not self.login(username, password):
                logger.error("Login failed, cannot continue")
                return None

            # Extract DMs
            conversations = self.extract_all_dms()
            if not conversations:
                logger.error("Failed to extract DMs")
                return None

            # Prepare results
            results = {
                'extraction_type': 'Instagram Mobile API Emulation',
                'timestamp': datetime.now().isoformat(),
                'user_id': self.user_id,
                'total_conversations': len(conversations),
                'conversations': conversations
            }

            # Save results
            filename = f"{self.results_dir}/mobile_api_extraction_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)

            logger.info(f"Extraction complete! Results saved to: {filename}")
            logger.info(f"Extracted {len(conversations)} conversations")

            # Log summary of real DM content
            total_messages = sum(len(conv.get('messages', [])) for conv in conversations)
            text_messages = sum(1 for conv in conversations for msg in conv.get('messages', [])
                              if msg.get('type') == 'text' and msg.get('content'))

            if text_messages > 0:
                logger.info(f"REAL DM CONTENT FOUND: {text_messages} text messages out of {total_messages} total!")
            else:
                logger.warning("No real text DM content found")

            return results

        except Exception as e:
            logger.error(f"Mobile API extraction failed: {e}")
            return None

def main():
    """Main execution function"""
    emulator = InstagramMobileAPIEmulator()

    # You need to provide valid Instagram credentials
    username = input("Enter Instagram username: ").strip()
    password = input("Enter Instagram password: ").strip()

    if username and password:
        emulator.run_extraction(username, password)
    else:
        logger.error("Username and password are required")

if __name__ == "__main__":
    main()
