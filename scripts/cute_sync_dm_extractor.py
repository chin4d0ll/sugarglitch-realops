# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Cute Rate DM Extractor - Sync version with cute rate limiting principles
"""

import json
import time
import random
import os
import sys
from datetime import datetime
import requests
from urllib.parse import quote
import sqlite3
from pathlib import Path
import logging
from typing import Dict, List, Optional

class CuteSyncRateLimiter:
    """Synchronous cute rate limiter based on CuteRateLimitBypass principles"""

    def __init__(self):
        self.request_count = 0
        self.rate_limit_count = 0
        self.last_request_time = 0
        self.success_count = 0

        # Cute strategies
        self.strategies = [
            {"name": "🐌 Ultra Safe", "min_delay": 25, "max_delay": 45, "backoff": 2.0},
            {"name": "🌊 Wave Pattern", "min_delay": 15, "max_delay": 35, "backoff": 1.5},
            {"name": "⚡ Quick Burst", "min_delay": 8, "max_delay": 20, "backoff": 1.2},
        ]
        self.current_strategy = 0

        # User agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
        ]
        self.current_ua = 0

    def cute_sleep(self, attempt = 1):
        """Apply cute sleep with current strategy"""
        strategy = self.strategies[self.current_strategy]

        # Base delay
        base_delay = random.uniform(strategy["min_delay"], strategy["max_delay"])

        # Adaptive delay based on rate limits
        if self.rate_limit_count > 5:
            base_delay *= 1.5

        # Exponential backoff
        backoff_delay = base_delay * (strategy["backoff"] ** (attempt - 1))

        # Human-like jitter
        jitter = random.uniform(0.8, 1.3)
        final_delay = backoff_delay * jitter

        # Cap at 2 minutes
        final_delay = min(final_delay, 120.0)

        print(f"💤 Cute sleep: {final_delay:.2f}s (strategy: {strategy['name']})")
        time.sleep(final_delay)

        self.last_request_time = time.time()

    def emergency_sleep(self):
        """Emergency sleep when rate limited"""
        self.rate_limit_count += 1
        emergency_delay = random.uniform(60, 120)  # 1-2 minutes
        print(f"🚨 EMERGENCY cute sleep: {emergency_delay:.2f}s (rate limits: {self.rate_limit_count})")
        time.sleep(emergency_delay)

        # Switch strategy after rate limit
        self.current_strategy = (self.current_strategy + 1) % len(self.strategies)
        print(f"🔄 Switched to strategy: {self.strategies[self.current_strategy]['name']}")

    def rotate_user_agent(self):
        """Rotate user agent"""
        self.current_ua = (self.current_ua + 1) % len(self.user_agents)
        return self.user_agents[self.current_ua]

class CuteDMExtractor:
    def __init__(self, session_file="session-alx.trading"):
        self.session_file = session_file
        self.session = None
        self.user_id = None
        self.username = None
        self.csrf_token = None
        self.rate_limiter = CuteSyncRateLimiter()

        # Setup logging
        logging.basicConfig(level = logging.INFO, format='🌸 %(asctime)s - %(message)s')
        self.logger = logging.getLogger(__name__)

        # Initialize
        self.init_session()
        self.setup_database()

        print(f"🌟 CuteDMExtractor initialized for {self.username}")

    def init_session(self):
        """Initialize session with cute headers"""
        try:
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)

            self.session = requests.Session()

            # Set cookies
            cookies = session_data.get('cookies', {})
            for name, value in cookies.items():
                self.session.cookies.set(name, value)

            # Set initial headers
            self.update_headers()

            # Get user info and CSRF token
            self.get_user_info()

        except Exception as e:
            print(f"❌ Session initialization failed: {e}")
            raise

    def update_headers(self):
        """Update headers with cute rotation"""
        self.session.headers.update({
            'User-Agent': self.rate_limiter.rotate_user_agent(),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q = 0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest',
            'X-IG-App-ID': '936619743392459',
            'X-IG-WWW-Claim': '0',
            'X-Instagram-AJAX': '1',
            'Referer': 'https://www.instagram.com/',
            'Origin': 'https://www.instagram.com'
        })

    def get_user_info(self):
        """Get user information and CSRF token with cute rate limiting"""
        try:
            print("🔍 Getting user info with cute rate limiting...")

            # Apply cute sleep
            self.rate_limiter.cute_sleep()

            # Update headers
            self.update_headers()

            response = self.session.get('https://www.instagram.com/')

            if response.status_code == 200:
                content = response.text

                # Extract CSRF token
                if 'csrf_token' in content:
                    import re
                    csrf_match = re.search(r'"csrf_token":"([^"]+)"', content)
                    if csrf_match:
                        self.csrf_token = csrf_match.group(1)
                        self.session.headers['X-CSRFToken'] = self.csrf_token
                        print(f"✅ CSRF token acquired: {self.csrf_token[:20]}...")

                # Extract user info
                user_match = re.search(r'"username":"([^"]+)"', content)
                if user_match:
                    self.username = user_match.group(1)
                    print(f"✅ Username: {self.username}")

                user_id_match = re.search(r'"id":"([^"]+)"', content)
                if user_id_match:
                    self.user_id = user_id_match.group(1)
                    print(f"✅ User ID: {self.user_id}")

                self.rate_limiter.success_count += 1

            elif response.status_code == 429:
                print("⚠️ Rate limited during user info fetch!")
                self.rate_limiter.emergency_sleep()

        except Exception as e:
            print(f"❌ Failed to get user info: {e}")

    def setup_database(self):
        """Setup SQLite database"""
        db_path = Path("data/cute_sync_dms.db")
        db_path.parent.mkdir(exist_ok = True)

        self.conn = sqlite3.connect(str(db_path))
        self.cursor = self.conn.cursor()

        # Create tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                is_verified INTEGER,
                profile_pic_url TEXT,
                last_activity TIMESTAMP,
                thread_title TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                conversation_id TEXT,
                sender_id TEXT,
                sender_username TEXT,
                message_text TEXT,
                timestamp TIMESTAMP,
                message_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations (id)
            )
        ''')

        self.conn.commit()
        print("✅ Database setup complete")

    def cute_request(self, url, params = None, attempt = 1, max_attempts = 5):
        """Make cute request with rate limiting"""
        for current_attempt in range(attempt, max_attempts + 1):
            try:
                # Apply cute sleep
                self.rate_limiter.cute_sleep(current_attempt)

                # Update headers
                self.update_headers()

                # Make request
                self.rate_limiter.request_count += 1
                response = self.session.get(url, params = params)

                if response.status_code == 200:
                    self.rate_limiter.success_count += 1
                    return response
                elif response.status_code == 429:
                    print(f"⚠️ Rate limited on attempt {current_attempt}/{max_attempts}")
                    self.rate_limiter.emergency_sleep()
                    continue
                else:
                    print(f"❌ Request failed: {response.status_code}")
                    if current_attempt == max_attempts:
                        break

            except Exception as e:
                print(f"❌ Request error on attempt {current_attempt}: {e}")
                if current_attempt == max_attempts:
                    break

        return None

    def get_dm_threads(self):
        """Get DM threads with cute rate limiting"""
        print("🔍 Fetching DM threads with cute rate limiting...")

        url = "https://www.instagram.com/api/v1/direct_v2/inbox/"
        params = {
            'visual_message_return_type': 'unseen',
            'thread_message_limit': '10',
            'persistentBadging': 'true',
            'limit': '20'
        }

        response = self.cute_request(url, params)

        if response:
            try:
                data = response.json()
                threads = data.get('inbox', {}).get('threads', [])
                print(f"✅ Found {len(threads)} DM threads")
                return threads
            except Exception as e:
                print(f"❌ Error parsing threads: {e}")
                return []
        else:
            print("❌ Failed to get threads")
            return []

    def extract_thread_messages(self, thread_id, limit = 50):
        """Extract messages from thread with cute rate limiting"""
        print(f"📥 Extracting messages from thread {thread_id} with cute rate limiting...")

        url = f"https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/"
        params = {
            'visual_message_return_type': 'unseen',
            'limit': str(limit)
        }

        response = self.cute_request(url, params)

        if response:
            try:
                data = response.json()
                thread = data.get('thread', {})
                messages = thread.get('items', [])
                print(f"✅ Found {len(messages)} messages in thread {thread_id}")
                return thread, messages
            except Exception as e:
                print(f"❌ Error parsing thread {thread_id}: {e}")
                return None, []
        else:
            print(f"❌ Failed to get thread {thread_id}")
            return None, []

    def save_conversation(self, thread):
        """Save conversation to database"""
        try:
            thread_id = thread.get('thread_id')
            users = thread.get('users', [])

            if users:
                user = users[0]

                self.cursor.execute('''
                    INSERT OR REPLACE INTO conversations
                    (id, username, full_name, is_verified, profile_pic_url, thread_title)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    thread_id,
                    user.get('username', ''),
                    user.get('full_name', ''),
                    1 if user.get('is_verified') else 0,
                    user.get('profile_pic_url', ''),
                    thread.get('thread_title', '')
                ))

                self.conn.commit()

        except Exception as e:
            print(f"❌ Error saving conversation: {e}")

    def save_messages(self, thread_id, messages):
        """Save messages to database"""
        try:
            saved_count = 0

            for message in messages:
                message_id = message.get('item_id')
                sender_id = message.get('user_id')
                timestamp = message.get('timestamp')

                # Get message text
                message_text = ""
                if 'text' in message:
                    message_text = message['text']
                elif 'media' in message:
                    message_text = "[Media]"
                elif 'link' in message:
                    message_text = f"[Link: {message['link'].get('text', 'Link')}]"

                # Convert timestamp
                if timestamp:
                    timestamp = datetime.fromtimestamp(int(timestamp) / 1000000)

                self.cursor.execute('''
                    INSERT OR REPLACE INTO messages
                    (id, conversation_id, sender_id, message_text, timestamp, message_type)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    message_id,
                    thread_id,
                    sender_id,
                    message_text,
                    timestamp,
                    message.get('item_type', 'text')
                ))

                saved_count += 1

            self.conn.commit()
            print(f"✅ Saved {saved_count} messages from thread {thread_id}")

        except Exception as e:
            print(f"❌ Error saving messages: {e}")

    def extract_all_dms(self):
        """Main extraction with cute rate limiting"""
        print("🚀 Starting cute DM extraction...")

        stats = {
            'total_threads': 0,
            'successful_extractions': 0,
            'failed_extractions': 0,
            'total_messages': 0,
            'start_time': datetime.now(),
            'requests_made': 0,
            'rate_limits_hit': 0
        }

        try:
            # Get threads
            threads = self.get_dm_threads()
            stats['total_threads'] = len(threads)

            if not threads:
                print("❌ No DM threads found")
                return stats

            # Process each thread
            for i, thread in enumerate(threads):
                thread_id = thread.get('thread_id')
                users = thread.get('users', [])
                user_name = users[0].get('username', 'Unknown') if users else 'Unknown'

                print(f"\n🔄 Processing thread {i+1}/{len(threads)}: {user_name}")

                # Extract messages
                thread_detail, messages = self.extract_thread_messages(thread_id)

                if thread_detail and messages:
                    self.save_conversation(thread_detail)
                    self.save_messages(thread_id, messages)

                    stats['successful_extractions'] += 1
                    stats['total_messages'] += len(messages)

                    print(f"✅ Successfully extracted {len(messages)} messages from {user_name}")
                else:
                    stats['failed_extractions'] += 1
                    print(f"❌ Failed to extract from {user_name}")

            # Final stats
            stats['end_time'] = datetime.now()
            stats['duration'] = stats['end_time'] - stats['start_time']
            stats['requests_made'] = self.rate_limiter.request_count
            stats['rate_limits_hit'] = self.rate_limiter.rate_limit_count

            # Save report
            self.save_extraction_report(stats)

            print(f"\n🎉 Cute extraction complete!")
            print(f"📊 Threads: {stats['total_threads']}")
            print(f"✅ Successful: {stats['successful_extractions']}")
            print(f"❌ Failed: {stats['failed_extractions']}")
            print(f"💬 Messages: {stats['total_messages']}")
            print(f"🚀 Requests: {stats['requests_made']}")
            print(f"⚠️ Rate limits: {stats['rate_limits_hit']}")
            print(f"⏱️ Duration: {stats['duration']}")

            return stats

        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            return stats

    def save_extraction_report(self, stats):
        """Save extraction report"""
        try:
            report_file = f"data/cute_sync_extraction_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            # Convert datetime objects
            stats_copy = stats.copy()
            for key, value in stats_copy.items():
                if isinstance(value, datetime):
                    stats_copy[key] = value.isoformat()

            with open(report_file, 'w') as f:
                json.dump(stats_copy, f, indent = 2)

            print(f"📄 Report saved: {report_file}")

        except Exception as e:
            print(f"❌ Failed to save report: {e}")

    def close(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    print("🎯 Cute Sync DM Extractor Starting...")
    print("=" * 50)

    extractor = None
    try:
        extractor = CuteDMExtractor()
        stats = extractor.extract_all_dms()

        print("\n" + "=" * 50)
        print("🎊 Cute Sync Extraction Complete!")

    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        if extractor:
            extractor.close()

if __name__ == "__main__":
    main()
