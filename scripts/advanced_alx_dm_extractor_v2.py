# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🥷 ADVANCED ALX.TRADING DM EXTRACTOR V2 - 2025
Features:
- Cute Rate Limiting with exponential backoff and jitter
- Advanced session handling with rotation
- Enhanced error handling and retry logic
- Smart delay algorithms
- Multiple user-agent rotation
- Request header spoofing
- Comprehensive logging and monitoring
"""

import json
import os
import requests
import time
import random
import sqlite3
import sys
import logging
from datetime import datetime, timedelta
import urllib.parse
import hashlib
import base64
from typing import Dict, List, Optional, Tuple
import asyncio
import aiohttp
from fake_useragent import UserAgent
import backoff
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Set up logging
logging.basicConfig(
    level = logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/workspaces/sugarglitch-realops/logs/advanced_alx_extractor_v2.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class CuteRateLimitBypass:
    """Advanced rate limiting bypass with cute delays and intelligent timing"""

    def __init__(self):
        self.request_count = 0
        self.last_request_time = 0
        self.consecutive_errors = 0
        self.base_delay = 1.0  # Base delay in seconds
        self.max_delay = 300.0  # Maximum delay (5 minutes)
        self.jitter_factor = 0.3  # 30% jitter
        self.success_streak = 0

    def cute_sleep(self, request_type: str = "standard"):
        """Implement cute sleep with various delay strategies"""
        current_time = time.time()

        # Calculate base delay based on request type
        if request_type == "dm_fetch":
            base_delay = 2.5 + (self.consecutive_errors * 0.5)
        elif request_type == "profile_check":
            base_delay = 1.5 + (self.consecutive_errors * 0.3)
        elif request_type == "conversation_list":
            base_delay = 3.0 + (self.consecutive_errors * 0.7)
        else:
            base_delay = self.base_delay + (self.consecutive_errors * 0.4)

        # Apply exponential backoff for consecutive errors
        if self.consecutive_errors > 0:
            exponential_factor = min(2 ** self.consecutive_errors, 32)
            base_delay *= exponential_factor

        # Apply jitter (randomization)
        jitter = random.uniform(-self.jitter_factor, self.jitter_factor) * base_delay
        final_delay = max(0.1, base_delay + jitter)

        # Ensure we don't exceed max delay
        final_delay = min(final_delay, self.max_delay)

        # Smart timing based on request frequency
        time_since_last = current_time - self.last_request_time
        if time_since_last < final_delay:
            additional_wait = final_delay - time_since_last
            logger.info(f"😴 Cute sleep: {additional_wait:.2f}s ({request_type})")
            time.sleep(additional_wait)

        self.last_request_time = time.time()
        self.request_count += 1

        # Log cute sleep statistics
        if self.request_count % 10 == 0:
            logger.info(f"🌟 Request #{self.request_count} | Errors: {self.consecutive_errors} | Success streak: {self.success_streak}")

    def on_success(self):
        """Called when a request succeeds"""
        self.consecutive_errors = max(0, self.consecutive_errors - 1)
        self.success_streak += 1

    def on_error(self, error_type: str = "unknown"):
        """Called when a request fails"""
        self.consecutive_errors += 1
        self.success_streak = 0
        logger.warning(f"⚠️  Error detected: {error_type} | Consecutive errors: {self.consecutive_errors}")

class AdvancedSessionManager:
    """Advanced session management with rotation and validation"""

    def __init__(self):
        self.sessions = []
        self.current_session_index = 0
        self.ua = UserAgent()
        self.load_sessions()

    def load_sessions(self):
        """Load all available sessions"""
        session_files = [
            "/workspaces/sugarglitch-realops/session-alx.trading",
            "/workspaces/sugarglitch-realops/session.json",
            "/workspaces/sugarglitch-realops/sessions/session-alx.trading",
            "/workspaces/sugarglitch-realops/sessions/quick_bypass_session.json"
        ]

        for session_file in session_files:
            if os.path.exists(session_file):
                try:
                    with open(session_file, 'r') as f:
                        session_data = json.load(f)
                        if 'cookies' in session_data and 'sessionid' in session_data['cookies']:
                            self.sessions.append({
                                'file': session_file,
                                'data': session_data,
                                'valid': True,
                                'last_used': 0,
                                'error_count': 0
                            })
                            logger.info(f"✅ Loaded session from: {session_file}")
                except Exception as e:
                    logger.error(f"❌ Failed to load session from {session_file}: {e}")

        if not self.sessions:
            logger.error("❌ No valid sessions found!")
            return False

        logger.info(f"🎯 Loaded {len(self.sessions)} sessions for rotation")
        return True

    def get_current_session(self) -> Optional[Dict]:
        """Get the current active session"""
        if not self.sessions:
            return None
        return self.sessions[self.current_session_index]

    def rotate_session(self):
        """Rotate to the next session"""
        if len(self.sessions) > 1:
            self.current_session_index = (self.current_session_index + 1) % len(self.sessions)
            logger.info(f"🔄 Rotated to session #{self.current_session_index + 1}")

    def get_headers(self) -> Dict[str, str]:
        """Generate advanced headers with randomization"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': random.choice(['en-US,en;q = 0.9', 'en-GB,en;q = 0.8', 'en;q = 0.7']),
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Instagram-AJAX': hashlib.md5(str(time.time()).encode()).hexdigest()[:8],
            'X-CSRFToken': self.generate_csrf_token(),
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/direct/inbox/'
        }

    def generate_csrf_token(self) -> str:
        """Generate a realistic CSRF token"""
        timestamp = str(int(time.time()))
        random_str = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k = 8))
        return hashlib.md5(f"{timestamp}{random_str}".encode()).hexdigest()[:32]

class AdvancedALXExtractor:
    """Advanced ALX.Trading DM Extractor with cute rate limiting"""

    def __init__(self):
        self.rate_limiter = CuteRateLimitBypass()
        self.session_manager = AdvancedSessionManager()
        self.db_path = "/workspaces/sugarglitch-realops/data/alx_trading_dms_advanced.db"
        self.target_username = "alx.trading"
        self.extracted_dms = []
        self.conversation_threads = {}

        # Initialize database
        self.init_database()

    def init_database(self):
        """Initialize SQLite database for storing DMs"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok = True)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dm_conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    thread_id TEXT UNIQUE,
                    participant_username TEXT,
                    participant_full_name TEXT,
                    last_message_time INTEGER,
                    message_count INTEGER DEFAULT 0,
                    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dm_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    thread_id TEXT,
                    message_id TEXT UNIQUE,
                    sender_username TEXT,
                    message_text TEXT,
                    message_type TEXT,
                    timestamp INTEGER,
                    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (thread_id) REFERENCES dm_conversations (thread_id)
                )
            ''')

            conn.commit()
            logger.info("📊 Database initialized successfully")

    @retry(
        stop = stop_after_attempt(5),
        wait = wait_exponential(multiplier = 1, min = 4, max = 10),
        retry = retry_if_exception_type((requests.exceptions.RequestException, requests.exceptions.Timeout))
    )
    def make_request(self, url: str, request_type: str = "standard") -> Optional[requests.Response]:
        """Make a request with advanced retry logic and rate limiting"""
        session = self.session_manager.get_current_session()
        if not session:
            logger.error("❌ No valid session available")
            return None

        # Apply cute rate limiting
        self.rate_limiter.cute_sleep(request_type)

        headers = self.session_manager.get_headers()
        cookies = session['data']['cookies']

        try:
            response = requests.get(
                url,
                headers = headers,
                cookies = cookies,
                timeout = 30,
                allow_redirects = True
            )

            if response.status_code == 200:
                self.rate_limiter.on_success()
                logger.info(f"✅ Request successful: {url[:50]}...")
                return response
            elif response.status_code == 429:
                self.rate_limiter.on_error("rate_limit")
                logger.warning("⏱️  Rate limited - increasing delays")
                raise requests.exceptions.RequestException("Rate limited")
            elif response.status_code in [401, 403]:
                self.rate_limiter.on_error("auth_error")
                logger.warning("🔐 Authentication error - rotating session")
                self.session_manager.rotate_session()
                raise requests.exceptions.RequestException("Authentication error")
            else:
                self.rate_limiter.on_error(f"http_{response.status_code}")
                logger.warning(f"⚠️  HTTP {response.status_code}: {url}")
                raise requests.exceptions.RequestException(f"HTTP {response.status_code}")

        except requests.exceptions.RequestException as e:
            self.rate_limiter.on_error("connection_error")
            logger.error(f"❌ Request failed: {e}")
            raise

    def extract_dm_conversations(self) -> List[Dict]:
        """Extract DM conversation list"""
        logger.info("🔍 Starting DM conversation extraction...")

        # Instagram's inbox API endpoint
        inbox_url = "https://www.instagram.com/api/v1/direct_v2/inbox/"

        try:
            response = self.make_request(inbox_url, "conversation_list")
            if not response:
                return []

            data = response.json()

            if 'inbox' not in data:
                logger.error("❌ No inbox data found in response")
                return []

            threads = data['inbox'].get('threads', [])
            logger.info(f"📨 Found {len(threads)} conversation threads")

            conversations = []
            for thread in threads:
                # Extract participant info (excluding the target account)
                participants = []
                for user in thread.get('users', []):
                    username = user.get('username', '')
                    if username and username != self.target_username:
                        participants.append({
                            'username': username,
                            'full_name': user.get('full_name', ''),
                            'profile_pic_url': user.get('profile_pic_url', '')
                        })

                if participants:
                    conversation = {
                        'thread_id': thread.get('thread_id', ''),
                        'participants': participants,
                        'last_activity': thread.get('last_activity_at', 0),
                        'message_count': len(thread.get('items', [])),
                        'has_older': thread.get('has_older', False)
                    }
                    conversations.append(conversation)

                    # Store in database
                    self.store_conversation(conversation)

            logger.info(f"✅ Extracted {len(conversations)} conversations")
            return conversations

        except Exception as e:
            logger.error(f"❌ Failed to extract conversations: {e}")
            return []

    def extract_thread_messages(self, thread_id: str, participant_name: str) -> List[Dict]:
        """Extract messages from a specific thread"""
        logger.info(f"💬 Extracting messages from thread: {thread_id} ({participant_name})")

        # Instagram's thread messages API
        thread_url = f"https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/"

        messages = []
        cursor = None
        page_count = 0

        while page_count < 10:  # Limit to 10 pages to avoid infinite loops
            url = thread_url
            if cursor:
                url += f"?cursor={cursor}"

            try:
                response = self.make_request(url, "dm_fetch")
                if not response:
                    break

                data = response.json()
                thread_data = data.get('thread', {})
                items = thread_data.get('items', [])

                if not items:
                    logger.info(f"📭 No more messages in thread {thread_id}")
                    break

                for item in items:
                    message = self.parse_message_item(item, thread_id)
                    if message:
                        messages.append(message)
                        self.store_message(message)

                # Check for pagination
                cursor = thread_data.get('oldest_cursor')
                if not cursor or not thread_data.get('has_older'):
                    break

                page_count += 1
                logger.info(f"📄 Processed page {page_count} for thread {thread_id} - {len(items)} messages")

            except Exception as e:
                logger.error(f"❌ Failed to extract messages from thread {thread_id}: {e}")
                break

        logger.info(f"✅ Extracted {len(messages)} messages from {participant_name}")
        return messages

    def parse_message_item(self, item: Dict, thread_id: str) -> Optional[Dict]:
        """Parse a message item from Instagram API response"""
        try:
            message_id = item.get('item_id', '')
            timestamp = item.get('timestamp', 0)
            user_id = item.get('user_id', '')

            # Extract message text
            message_text = ""
            message_type = "unknown"

            if 'text' in item:
                message_text = item['text']
                message_type = "text"
            elif 'media' in item:
                media = item['media']
                message_type = media.get('media_type', 'media')
                if 'caption' in media:
                    message_text = media['caption']
                else:
                    message_text = f"[{message_type.upper()}]"
            elif 'story_share' in item:
                message_type = "story_share"
                message_text = "[STORY SHARE]"
            elif 'voice_media' in item:
                message_type = "voice"
                message_text = "[VOICE MESSAGE]"

            return {
                'thread_id': thread_id,
                'message_id': message_id,
                'sender_id': user_id,
                'message_text': message_text,
                'message_type': message_type,
                'timestamp': timestamp,
                'raw_data': item
            }

        except Exception as e:
            logger.error(f"❌ Failed to parse message item: {e}")
            return None

    def store_conversation(self, conversation: Dict):
        """Store conversation in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                for participant in conversation['participants']:
                    cursor.execute('''
                        INSERT OR REPLACE INTO dm_conversations
                        (thread_id, participant_username, participant_full_name,
                         last_message_time, message_count)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        conversation['thread_id'],
                        participant['username'],
                        participant['full_name'],
                        conversation['last_activity'],
                        conversation['message_count']
                    ))

                conn.commit()

        except Exception as e:
            logger.error(f"❌ Failed to store conversation: {e}")

    def store_message(self, message: Dict):
        """Store message in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO dm_messages
                    (thread_id, message_id, sender_username, message_text,
                     message_type, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    message['thread_id'],
                    message['message_id'],
                    message.get('sender_username', message.get('sender_id', '')),
                    message['message_text'],
                    message['message_type'],
                    message['timestamp']
                ))
                conn.commit()

        except Exception as e:
            logger.error(f"❌ Failed to store message: {e}")

    def run_extraction(self):
        """Run the complete DM extraction process"""
        logger.info("🚀 Starting Advanced ALX.Trading DM Extraction V2")
        logger.info(f"🎯 Target: {self.target_username}")

        # Check if we have valid sessions
        if not self.session_manager.sessions:
            logger.error("❌ No valid sessions available. Cannot proceed.")
            return False

        # Extract conversations
        conversations = self.extract_dm_conversations()
        if not conversations:
            logger.error("❌ No conversations found")
            return False

        # Extract messages from each conversation
        total_messages = 0
        for conversation in conversations:
            thread_id = conversation['thread_id']
            participants = conversation['participants']

            for participant in participants:
                participant_name = participant['username']
                logger.info(f"👤 Processing conversation with: {participant_name}")

                messages = self.extract_thread_messages(thread_id, participant_name)
                total_messages += len(messages)

                # Small delay between conversations
                time.sleep(random.uniform(2, 5))

        logger.info(f"🎉 Extraction completed! Total messages extracted: {total_messages}")

        # Generate summary report
        self.generate_report()
        return True

    def generate_report(self):
        """Generate extraction summary report"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Get conversation count
                cursor.execute("SELECT COUNT(*) FROM dm_conversations")
                conversation_count = cursor.fetchone()[0]

                # Get message count
                cursor.execute("SELECT COUNT(*) FROM dm_messages")
                message_count = cursor.fetchone()[0]

                # Get top participants
                cursor.execute('''
                    SELECT participant_username, COUNT(*) as msg_count
                    FROM dm_conversations c
                    JOIN dm_messages m ON c.thread_id = m.thread_id
                    GROUP BY participant_username
                    ORDER BY msg_count DESC
                    LIMIT 10
                ''')
                top_participants = cursor.fetchall()

                report = {
                    'extraction_time': datetime.now().isoformat(),
                    'target_account': self.target_username,
                    'total_conversations': conversation_count,
                    'total_messages': message_count,
                    'top_participants': [
                        {'username': p[0], 'message_count': p[1]}
                        for p in top_participants
                    ],
                    'database_path': self.db_path
                }

                # Save report
                report_path = f"/workspaces/sugarglitch-realops/reports/alx_extraction_report_{int(time.time())}.json"
                os.makedirs(os.path.dirname(report_path), exist_ok = True)

                with open(report_path, 'w') as f:
                    json.dump(report, f, indent = 2)

                logger.info(f"📊 Report generated: {report_path}")
                logger.info(f"📈 Summary: {conversation_count} conversations, {message_count} messages")

        except Exception as e:
            logger.error(f"❌ Failed to generate report: {e}")

def main():
    """Main function"""
    print("🥷 Advanced ALX.Trading DM Extractor V2 - 2025")
    print("=" * 50)

    extractor = AdvancedALXExtractor()
    success = extractor.run_extraction()

    if success:
        print("\n🎉 Extraction completed successfully!")
        print(f"📊 Database: {extractor.db_path}")
        print("📁 Check the reports folder for detailed results")
    else:
        print("\n❌ Extraction failed. Check logs for details.")

    return success

if __name__ == "__main__":
    main()
