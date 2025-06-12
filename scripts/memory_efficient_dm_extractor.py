# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Memory-Efficient Instagram DM Extractor
Optimized for Codespace environments with limited resources
"""

import os
import sys
import json
import time
import logging
import gc
from pathlib import Path
from datetime import datetime
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f'dm_extraction_{int(time.time())}.log')
    ]
)
logger = logging.getLogger(__name__)

class MemoryEfficientDMExtractor:
    def __init__(self):
        self.workspace_dir = Path("/workspaces/sugarglitch-realops")
        self.output_dir = self.workspace_dir / "real_extraction" / "alx_trading"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Instagram API endpoints
        self.base_url = "https://www.instagram.com"
        self.api_url = "https://www.instagram.com/api/v1"

        # Session management
        self.session = None
        self.user_id = None
        self.sessionid = None

        # Memory management
        self.batch_size = 10  # Process messages in small batches
        self.max_retries = 3

    def setup_session(self):
        """Setup requests session with retry strategy"""
        self.session = requests.Session()

        # Retry strategy
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        })

        logger.info("✅ Session setup complete")

    def load_session_from_file(self, session_file):
        """Load session from various file formats"""
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)

            # Handle different session formats
            if 'sessionid' in session_data:
                self.sessionid = session_data['sessionid']
            elif 'cookies' in session_data:
                cookies = session_data['cookies']
                if isinstance(cookies, list):
                    for cookie in cookies:
                        if cookie.get('name') == 'sessionid':
                            self.sessionid = cookie.get('value')
                            break
                elif isinstance(cookies, dict):
                    self.sessionid = cookies.get('sessionid')

            if not self.sessionid:
                logger.error("No sessionid found in session file")
                return False

            # Set session cookie
            self.session.cookies.set('sessionid', self.sessionid, domain='.instagram.com')
            logger.info(f"✅ Loaded session from {session_file}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to load session from {session_file}: {e}")
            return False

    def find_valid_session(self):
        """Find and load a valid session from available files"""
        session_files = [
            # Project sessions
            self.workspace_dir / "tools" / "session_alx_trading.json",
            self.workspace_dir / "config" / "sessions" / "session.json",

            # Hijacked sessions
            self.workspace_dir / "hijacked_sessions" / "fresh_hijacked_session_1749169370.json",
        ]

        # Add all hijacked session files
        hijacked_dir = self.workspace_dir / "hijacked_sessions"
        if hijacked_dir.exists():
            session_files.extend(hijacked_dir.glob("*.json"))

        logger.info(f"🔍 Searching for valid sessions in {len(session_files)} files...")

        for session_file in session_files:
            if session_file.exists():
                logger.info(f"Trying session file: {session_file}")
                if self.load_session_from_file(session_file):
                    if self.verify_session():
                        logger.info(f"✅ Valid session found: {session_file}")
                        return True
                    else:
                        logger.warning(f"⚠️ Session loaded but invalid: {session_file}")
                        # Clear invalid session
                        self.session.cookies.clear()
                        self.sessionid = None

        logger.error("❌ No valid session found")
        return False

    def verify_session(self):
        """Verify if the current session is valid"""
        try:
            # Test with a simple API call
            response = self.session.get(f"{self.base_url}/", timeout=10)

            if response.status_code == 200:
                # Check if we're redirected to login
                if 'login' in response.url:
                    logger.warning("Session expired - redirected to login")
                    return False

                # Try to get user info
                user_info_response = self.session.get(
                    f"{self.api_url}/accounts/edit/web_form_data/",
                    headers={'X-Requested-With': 'XMLHttpRequest'},
                    timeout=10
                )

                if user_info_response.status_code == 200:
                    user_data = user_info_response.json()
                    if 'form_data' in user_data:
                        self.user_id = user_data['form_data'].get('pk')
                        logger.info(f"✅ Session valid - User ID: {self.user_id}")
                        return True

            logger.warning(f"Session validation failed - Status: {response.status_code}")
            return False

        except Exception as e:
            logger.error(f"❌ Session verification error: {e}")
            return False

    def search_user(self, username):
        """Search for a user and get their ID"""
        try:
            search_url = f"{self.base_url}/web/search/topsearch/"
            params = {
                'context': 'blended',
                'query': username,
                'rank_token': f"{self.user_id}_{int(time.time())}"
            }

            response = self.session.get(search_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                users = data.get('users', [])

                for user in users:
                    if user.get('user', {}).get('username') == username:
                        user_id = user.get('user', {}).get('pk')
                        logger.info(f"✅ Found user {username} with ID: {user_id}")
                        return user_id

            logger.warning(f"User {username} not found")
            return None

        except Exception as e:
            logger.error(f"❌ Error searching for user {username}: {e}")
            return None

    def get_thread_id(self, target_user_id):
        """Get thread ID for direct conversation with target user"""
        try:
            inbox_url = f"{self.api_url}/direct_v2/inbox/"
            params = {'persistentBadging': 'true', 'folder': '', 'limit': 20}

            response = self.session.get(inbox_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                threads = data.get('inbox', {}).get('threads', [])

                for thread in threads:
                    users = thread.get('users', [])
                    for user in users:
                        if str(user.get('pk')) == str(target_user_id):
                            thread_id = thread.get('thread_id')
                            logger.info(f"✅ Found thread ID: {thread_id}")
                            return thread_id

            logger.warning("No thread found with target user")
            return None

        except Exception as e:
            logger.error(f"❌ Error getting thread ID: {e}")
            return None

    def extract_messages(self, thread_id, limit=50):
        """Extract messages from thread in memory-efficient batches"""
        messages = []
        cursor = None
        extracted_count = 0

        try:
            while extracted_count < limit:
                # Memory management - force garbage collection
                if extracted_count % self.batch_size == 0:
                    gc.collect()

                # Get messages batch
                thread_url = f"{self.api_url}/direct_v2/threads/{thread_id}/"
                params = {'limit': min(self.batch_size, limit - extracted_count)}

                if cursor:
                    params['cursor'] = cursor

                response = self.session.get(thread_url, params=params, timeout=15)

                if response.status_code != 200:
                    logger.error(f"Failed to get messages - Status: {response.status_code}")
                    break

                data = response.json()
                thread_data = data.get('thread', {})
                batch_messages = thread_data.get('items', [])

                if not batch_messages:
                    logger.info("No more messages to fetch")
                    break

                # Process batch
                for msg in batch_messages:
                    processed_msg = self.process_message(msg)
                    if processed_msg:
                        messages.append(processed_msg)
                        extracted_count += 1

                # Get next cursor
                cursor = thread_data.get('oldest_cursor')
                if not cursor:
                    break

                logger.info(f"Extracted {extracted_count} messages so far...")
                time.sleep(0.5)  # Rate limiting

        except Exception as e:
            logger.error(f"❌ Error extracting messages: {e}")

        return messages

    def process_message(self, message):
        """Process a single message efficiently"""
        try:
            processed = {
                'id': message.get('item_id'),
                'timestamp': message.get('timestamp'),
                'user_id': message.get('user_id'),
                'type': message.get('item_type'),
                'text': message.get('text'),
                'created_at': datetime.fromtimestamp(message.get('timestamp', 0) / 1000000).isoformat()
            }

            # Handle different message types
            if message.get('item_type') == 'text':
                processed['content'] = message.get('text', '')
            elif message.get('item_type') == 'media':
                media = message.get('media', {})
                processed['content'] = f"[Media: {media.get('media_type', 'unknown')}]"
            elif message.get('item_type') == 'link':
                link = message.get('link', {})
                processed['content'] = f"[Link: {link.get('url', 'unknown')}]"
            else:
                processed['content'] = f"[{message.get('item_type', 'unknown')}]"

            return processed

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return None

    def save_messages(self, messages, target_username):
        """Save messages to file efficiently"""
        timestamp = int(time.time())
        filename = f"dm_extraction_{target_username}_{timestamp}.json"
        filepath = self.output_dir / filename

        try:
            # Create summary
            summary = {
                'target_username': target_username,
                'extraction_timestamp': timestamp,
                'extraction_date': datetime.now().isoformat(),
                'total_messages': len(messages),
                'session_valid': True,
                'extraction_method': 'memory_efficient_api',
                'messages': messages
            }

            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)

            logger.info(f"✅ Saved {len(messages)} messages to {filepath}")

            # Also save a simple text version
            text_file = filepath.with_suffix('.txt')
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(f"Instagram DM Extraction - {target_username}\n")
                f.write(f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Messages: {len(messages)}\n")
                f.write("=" * 50 + "\n\n")

                for msg in messages:
                    f.write(f"[{msg['created_at']}] {msg.get('content', '')}\n")

            logger.info(f"✅ Also saved text version to {text_file}")
            return filepath

        except Exception as e:
            logger.error(f"❌ Error saving messages: {e}")
            return None

    def extract_dms(self, target_username="alx.trading", message_limit=100):
        """Main extraction method"""
        logger.info(f"🚀 Starting DM extraction for {target_username}")

        # Setup session
        self.setup_session()

        # Find valid session
        if not self.find_valid_session():
            logger.error("❌ No valid session available")
            return False

        # Search for target user
        target_user_id = self.search_user(target_username)
        if not target_user_id:
            logger.error(f"❌ Could not find user {target_username}")
            return False

        # Get thread ID
        thread_id = self.get_thread_id(target_user_id)
        if not thread_id:
            logger.error(f"❌ No conversation found with {target_username}")
            return False

        # Extract messages
        logger.info(f"📥 Extracting messages from thread {thread_id}")
        messages = self.extract_messages(thread_id, limit=message_limit)

        if not messages:
            logger.warning("⚠️ No messages extracted")
            return False

        # Save messages
        output_file = self.save_messages(messages, target_username)
        if output_file:
            logger.info(f"🎉 Extraction complete! {len(messages)} messages saved to {output_file}")
            return True
        else:
            logger.error("❌ Failed to save messages")
            return False

def main():
    extractor = MemoryEfficientDMExtractor()

    # Extract DMs
    success = extractor.extract_dms(
        target_username="alx.trading",
        message_limit=100
    )

    if success:
        print("\n🎉 DM extraction completed successfully!")
        print(f"📁 Check output directory: {extractor.output_dir}")
    else:
        print("\n❌ DM extraction failed")
        print("💡 Try running the session generation script first")

    # Memory cleanup
    gc.collect()

if __name__ == "__main__":
    main()
