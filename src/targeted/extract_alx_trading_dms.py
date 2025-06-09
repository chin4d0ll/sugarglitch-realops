# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🎯💀 ALX.TRADING DM EXTRACTOR 2025 💀🎯
===============================================
🚀 เฉพาะ target alx.trading กับ session whatilove1728
🛡️ ใช้เทคนิคขั้นสูงที่สุด + Stealth + Session management

Features:
- 🎯 Target-specific extraction for alx.trading
- 💀 Session whatilove1728 management
- 🔥 Advanced stealth techniques
- 🛡️ Bulletproof error handling
- 📊 Real-time progress tracking
- 💾 Comprehensive data storage
"""

import os
import gc
import json
import time
import random
import sqlite3
import hashlib
import getpass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Safe imports with fallbacks
try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, RateLimitError, ClientError, ChallengeRequired
    INSTAGRAPI_AVAILABLE = True
except ImportError:
    print("⚠️ instagrapi not available, install with: pip install instagrapi")
    INSTAGRAPI_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
class AlxTradingDMExtractor:
    """🎯 Specialized extractor for alx.trading target"""

    def __init__(self):
        self.target_username = "alx.trading"
        self.session_name = "whatilove1728"
        self.client = None
        self.session_loaded = False

        # Results storage
        self.results = {
            'extraction_id': f"ALX_TRADING_{int(time.time())}",
            'target': self.target_username,
            'session': self.session_name,
            'start_time': datetime.now().isoformat(),
            'extracted_messages': [],
            'thread_data': {},
            'total_messages': 0,
            'errors': [],
            'performance': {
                'requests_made': 0,
                'successful_extractions': 0,
                'errors_handled': 0
            }
        }

        # Database setup
        self.db_path = f"alx_trading_dms_{int(time.time())}.sqlite"
        self.setup_database()

        print("🎯💀 ALX.TRADING DM EXTRACTOR INITIALIZED 💀🎯")
        print(f"Target: {self.target_username}")
        print(f"Session: {self.session_name}")

    def setup_database(self):
        """Setup SQLite database for storing extracted data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create table for messages
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alx_trading_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id TEXT UNIQUE,
                    thread_id TEXT,
                    sender_username TEXT,
                    message_text TEXT,
                    timestamp TEXT,
                    message_type TEXT,
                    media_url TEXT,
                    extracted_at TEXT,
                    session_used TEXT
                )
            ''')

            # Create table for thread metadata
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS thread_metadata (
                    thread_id TEXT PRIMARY KEY,
                    participants TEXT,
                    created_at TEXT,
                    last_message_at TEXT,
                    message_count INTEGER,
                    extracted_at TEXT
                )
            ''')

            # Create table for extraction logs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS extraction_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    extraction_id TEXT,
                    action TEXT,
                    status TEXT,
                    details TEXT,
                    timestamp TEXT
                )
            ''')

            conn.commit()
            conn.close()
            print(f"📊 Database initialized: {self.db_path}")

        except Exception as e:
            print(f"❌ Database setup error: {e}")

    def log_action(self, action: str, status: str, details: str = ""):
        """Log action to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO extraction_logs
                (extraction_id, action, status, details, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                self.results['extraction_id'],
                action,
                status,
                details,
                datetime.now().isoformat()
            ))

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"⚠️ Logging error: {e}")

    def setup_client_stealth(self):
        """Setup Instagram client with stealth techniques"""
        try:
            if not INSTAGRAPI_AVAILABLE:
                print("❌ instagrapi not available!")
                return False

            self.client = Client()

            # Advanced stealth settings
            stealth_user_agents = [
                "Instagram 219.0.0.12.117 Android (29/10; 420dpi; 1080x2340; samsung; SM-G973F; beyond1; exynos9820; en_US; 336448643)",
                "Instagram 218.0.0.19.118 Android (28/9; 480dpi; 1080x2280; OnePlus; ONEPLUS A6000; OnePlus6; qcom; en_US; 336395456)",
                "Instagram 217.0.0.15.114 Android (30/11; 560dpi; 1440x3120; samsung; SM-G988B; x1s; exynos990; en_US; 336064204)"
            ]

            # Set random user agent
            selected_ua = random.choice(stealth_user_agents)
            self.client.set_user_agent(selected_ua)
            print(f"🎭 User agent set: {selected_ua[:50]}...")

            # Additional stealth settings
            self.client.delay_range = [2, 5]  # Random delay between requests

            return True

        except Exception as e:
            print(f"❌ Client setup error: {e}")
            self.log_action("client_setup", "error", str(e))
            return False

    def load_or_create_session(self):
        """Load existing session or create new one"""
        try:
            session_file = f"session_{self.session_name}.json"

            # Try to load existing session
            if os.path.exists(session_file):
                print(f"🔄 Loading session: {self.session_name}")
                try:
                    self.client.load_settings(session_file)

                    # Verify session
                    user_info = self.client.account_info()
                    print(f"✅ Session loaded! Logged in as: {user_info.username}")
                    self.session_loaded = True
                    self.log_action("session_load", "success", f"User: {user_info.username}")
                    return True

                except Exception as e:
                    print(f"⚠️ Session invalid: {e}")
                    self.log_action("session_load", "failed", str(e))

            # Create new session
            print(f"🔐 Creating new session: {self.session_name}")

            # For demo purposes, we'll use the session name as username
            # In real scenario, you'd have proper credentials
            username = self.session_name
            password = getpass.getpass(f"Enter password for {username}: ")

            login_success = self.client.login(username, password)

            if login_success:
                self.client.dump_settings(session_file)
                print("✅ New session created and saved!")
                self.session_loaded = True
                self.log_action("session_create", "success", f"User: {username}")
                return True
            else:
                print("❌ Login failed!")
                self.log_action("session_create", "failed", "Login failed")
                return False

        except Exception as e:
            print(f"❌ Session setup error: {e}")
            self.log_action("session_setup", "error", str(e))
            return False

    def find_target_thread(self) -> Optional[str]:
        """Find conversation thread with target user"""
        try:
            print(f"🔍 Searching for thread with {self.target_username}...")

            # Get direct message threads
            threads = self.client.direct_threads()

            for thread in threads:
                # Check if target is in thread participants
                participants = [user.username for user in thread.users]

                if self.target_username.lower() in [p.lower() for p in participants]:
                    print(f"✅ Found thread with {self.target_username}!")
                    print(f"   Thread ID: {thread.id}")
                    print(f"   Participants: {', '.join(participants)}")

                    self.log_action("thread_found", "success", f"Thread ID: {thread.id}")
                    return thread.id

            print(f"❌ No thread found with {self.target_username}")
            self.log_action("thread_search", "not_found", f"Target: {self.target_username}")
            return None

        except Exception as e:
            print(f"❌ Thread search error: {e}")
            self.log_action("thread_search", "error", str(e))
            return None

    def extract_thread_messages(self, thread_id: str, limit: int = 100):
        """Extract all messages from the thread"""
        try:
            print(f"📥 Extracting messages from thread {thread_id}...")

            # Get messages with pagination
            all_messages = []
            extracted_count = 0

            # Get messages in chunks
            messages = self.client.direct_messages(thread_id, amount=limit)

            for msg in messages:
                try:
                    # Extract message data
                    message_data = {
                        'message_id': msg.id,
                        'thread_id': thread_id,
                        'sender_username': msg.user_id,  # Will resolve to username
                        'message_text': msg.text or '',
                        'timestamp': msg.timestamp.isoformat() if msg.timestamp else '',
                        'message_type': msg.item_type or 'text',
                        'media_url': '',
                        'extracted_at': datetime.now().isoformat(),
                        'session_used': self.session_name
                    }

                    # Handle media messages
                    if hasattr(msg, 'media') and msg.media:
                        if hasattr(msg.media, 'image_versions2'):
                            message_data['media_url'] = msg.media.image_versions2.candidates[0].url
                        elif hasattr(msg.media, 'video_versions'):
                            message_data['media_url'] = msg.media.video_versions[0].url

                    # Resolve sender username
                    try:
                        user_info = self.client.user_info(msg.user_id)
                        message_data['sender_username'] = user_info.username
                    except Exception:
                        message_data['sender_username'] = str(msg.user_id)

                    all_messages.append(message_data)
                    self.save_message_to_db(message_data)
                    extracted_count += 1

                    # Progress update
                    if extracted_count % 10 == 0:
                        print(f"   📥 Extracted {extracted_count} messages...")

                    # Smart delay between message processing
                    time.sleep(random.uniform(0.5, 1.5))

                except Exception as msg_error:
                    print(f"⚠️ Message processing error: {msg_error}")
                    continue

            print(f"✅ Extraction complete! Total messages: {extracted_count}")

            self.results['extracted_messages'] = all_messages
            self.results['total_messages'] = extracted_count
            self.results['performance']['successful_extractions'] = extracted_count

            self.log_action("message_extraction", "success", f"Messages: {extracted_count}")

            return all_messages

        except Exception as e:
            print(f"❌ Message extraction error: {e}")
            self.log_action("message_extraction", "error", str(e))
            self.results['errors'].append({
                'type': 'message_extraction',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return []

    def save_message_to_db(self, message_data: Dict):
        """Save individual message to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT OR REPLACE INTO alx_trading_messages
                (message_id, thread_id, sender_username, message_text,
                 timestamp, message_type, media_url, extracted_at, session_used)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                message_data['message_id'],
                message_data['thread_id'],
                message_data['sender_username'],
                message_data['message_text'],
                message_data['timestamp'],
                message_data['message_type'],
                message_data['media_url'],
                message_data['extracted_at'],
                message_data['session_used']
            ))

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"⚠️ Message save error: {e}")

    def save_results_to_files(self):
        """Save extraction results to JSON and CSV files"""
        try:
            # Save JSON results
            json_file = f"alx_trading_extraction_{self.results['extraction_id']}.json"

            self.results['end_time'] = datetime.now().isoformat()

            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)

            print(f"💾 JSON results saved: {json_file}")

            # Save CSV for easy viewing
            csv_file = f"alx_trading_messages_{self.results['extraction_id']}.csv"

            if self.results['extracted_messages']:
                import csv

                with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=self.results['extracted_messages'][0].keys())
                    writer.writeheader()
                    writer.writerows(self.results['extracted_messages'])

                print(f"📊 CSV results saved: {csv_file}")

            print(f"🗄️ Database saved: {self.db_path}")

        except Exception as e:
            print(f"⚠️ Results save error: {e}")

    def run_extraction(self):
        """Main extraction process"""
        try:
            print("\n🚀 Starting ALX.TRADING DM extraction...")
            print("=" * 50)

            # Setup client with stealth
            if not self.setup_client_stealth():
                return False

            # Load or create session
            if not self.load_or_create_session():
                return False

            # Find target thread
            thread_id = self.find_target_thread()
            if not thread_id:
                return False

            # Extract messages
            messages = self.extract_thread_messages(thread_id)

            if messages:
                # Save results
                self.save_results_to_files()

                # Show summary
                print("\n🎉 EXTRACTION COMPLETED SUCCESSFULLY! 🎉")
                print("=" * 50)
                print(f"🎯 Target: {self.target_username}")
                print(f"💀 Session: {self.session_name}")
                print(f"📊 Messages extracted: {len(messages)}")
                print(f"🗄️ Database: {self.db_path}")
                print(f"⏱️ Duration: {datetime.now() - datetime.fromisoformat(self.results['start_time'])}")

                return True
            else:
                print("❌ No messages extracted!")
                return False

        except KeyboardInterrupt:
            print("\n🛑 Extraction cancelled by user")
            return False
        except Exception as e:
            print(f"\n❌ Extraction failed: {e}")
            self.log_action("extraction", "failed", str(e))
            return False
def main():
    """🚀 Main execution function"""
    print("🎯💀 ALX.TRADING DM EXTRACTOR 2025 💀🎯")
    print("=" * 50)
    print("Target: alx.trading")
    print("Session: whatilove1728")
    print("=" * 50)

    if not INSTAGRAPI_AVAILABLE:
        print("❌ Missing required packages!")
        print("📦 Install with: pip install instagrapi")
        return

    # Initialize extractor
    extractor = AlxTradingDMExtractor()

    # Run extraction
    success = extractor.run_extraction()

    if success:
        print("\n✅ Mission accomplished! Data extracted successfully.")
    else:
        print("\n❌ Mission failed! Check logs for details.")
if __name__ == "__main__":
    main()
