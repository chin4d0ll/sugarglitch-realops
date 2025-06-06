#!/usr/bin/env python3
"""
Cute Rate Limit DM Extractor - Using CuteRateLimitBypass for Instagram DM Extraction
Enhanced with cute rate/cute sleep logic for ultimate bypass
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

# Import our cute rate limit bypass
try:
    from rate_limit_analyzer import CuteRateLimitBypass
    print("✅ CuteRateLimitBypass imported successfully!")
except ImportError:
    print("❌ Failed to import CuteRateLimitBypass")
    sys.exit(1)

class CuteRateDMExtractor:
    def __init__(self, session_file="session-alx.trading"):
        self.session_file = session_file
        self.session = None
        self.user_id = None
        self.username = None
        self.csrf_token = None
        
        # Initialize cute bypass with session file FIRST
        try:
            self.cute_bypass = CuteRateLimitBypass(session_file)
            print("✅ CuteRateLimitBypass initialized successfully!")
        except Exception as e:
            print(f"❌ Failed to initialize CuteRateLimitBypass: {e}")
            print("🔄 Creating fallback rate limiter...")
            self.cute_bypass = self.create_fallback_rate_limiter()
        
        # Initialize session and headers after bypass is ready
        self.init_session()
        
        # Database setup
        self.setup_database()
        
        print(f"🌟 CuteRateDMExtractor initialized for {self.username}")
    
    def create_fallback_rate_limiter(self):
        """Create a fallback rate limiter if CuteRateLimitBypass fails"""
        class FallbackRateLimiter:
            def __init__(self):
                self.last_request_time = 0
                self.request_count = 0
                
            def apply_cute_rate_limit(self):
                """Apply simple rate limiting"""
                current_time = time.time()
                if current_time - self.last_request_time < 2:
                    cute_sleep = random.uniform(2, 5)
                    print(f"😴 Cute sleep for {cute_sleep:.2f} seconds...")
                    time.sleep(cute_sleep)
                self.last_request_time = time.time()
                self.request_count += 1
                
            def adaptive_delay(self):
                """Adaptive delay based on request count"""
                if self.request_count > 10:
                    delay = random.uniform(5, 10)
                    print(f"🐌 Adaptive delay: {delay:.2f} seconds")
                    time.sleep(delay)
                    
        return FallbackRateLimiter()

    def init_session(self):
        """Initialize session with anti-redirect headers and authentication"""
        print("🚀 Initializing session with redirect fixes...")
        
        # Load session data
        try:
            with open(self.session_file, 'r') as f:
                content = f.read().strip()
                if content.startswith('{'):
                    session_data = json.loads(content)
                else:
                    # Handle raw sessionid format
                    session_data = {"cookies": {"sessionid": content}}
            print("✅ Session file loaded successfully")
        except Exception as e:
            print(f"❌ Failed to load session file: {e}")
            raise
        
        self.session = requests.Session()
        
        # Anti-redirect mobile headers for better compatibility
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'identity',  # Avoid compression issues
            'Connection': 'close',  # Close connection after use
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.instagram.com/',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://www.instagram.com',
            'X-CSRFToken': '',
            'X-IG-App-ID': '936619743392459',
            'X-IG-WWW-Claim': '0',
            'X-Instagram-AJAX': '1'
        }
        
        self.session.headers.update(headers)
        self.session.max_redirects = 3  # Limit redirects to prevent loops
        
        # Set cookies from session data with URL decoding
        cookies = session_data.get('cookies', {})
        for name, value in cookies.items():
            # Handle URL-encoded cookies
            if '%' in str(value):
                from urllib.parse import unquote
                value = unquote(str(value))
            self.session.cookies.set(name, value, domain='.instagram.com')
        print("🍪 Session cookies set successfully with redirect fixes")
        
        # Get user info and CSRF token
        self.get_user_info()
    
    def get_user_info(self):
        """Get user information and CSRF token with redirect handling"""
        try:
            print("🔍 Getting user info and CSRF token with redirect fixes...")
            
            # Apply cute rate limit before request
            self.cute_bypass.apply_cute_rate_limit()
            
            # Use safe request with timeout and redirect limits
            response = self.session.get(
                'https://www.instagram.com/',
                timeout=30,
                allow_redirects=True,
                verify=False
            )
            
            if response.status_code == 200:
                print("✅ Instagram main page accessed successfully")
                
                # Extract CSRF token
                content = response.text
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
                    
            elif response.status_code == 500:
                print("⚠️ Instagram returned HTTP 500 - retrying with different approach")
                # Fallback: try direct profile access
                self.cute_bypass.apply_cute_rate_limit()
                profile_response = self.session.get(
                    'https://www.instagram.com/alx.trading/',
                    timeout=25,
                    allow_redirects=True,
                    verify=False
                )
                if profile_response.status_code == 200:
                    print("✅ ALX Trading profile accessible as fallback")
                    
            else:
                print(f"⚠️ Unexpected status code: {response.status_code}")
                print(f"Response URL: {response.url}")
                
        except requests.exceptions.TooManyRedirects:
            print("⚠️ Too many redirects - using minimal session info")
            # Continue with minimal session setup
            
        except Exception as e:
            print(f"❌ Failed to get user info: {e}")
            # Continue with session anyway - some methods may still work
    
    def setup_database(self):
        """Setup SQLite database for storing DMs"""
        db_path = Path("data/cute_rate_dms.db")
        db_path.parent.mkdir(exist_ok=True)
        
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
    
    def get_dm_threads(self):
        """Get list of DM threads with cute rate limiting"""
        print("🔍 Fetching DM threads with cute rate limiting...")
        
        try:
            # Apply cute rate limit
            self.cute_bypass.apply_cute_rate_limit()
            
            url = "https://www.instagram.com/api/v1/direct_v2/inbox/"
            params = {
                'visual_message_return_type': 'unseen',
                'thread_message_limit': '10',
                'persistentBadging': 'true',
                'limit': '20'
            }
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                threads = data.get('inbox', {}).get('threads', [])
                print(f"✅ Found {len(threads)} DM threads")
                return threads
            else:
                print(f"❌ Failed to get threads: {response.status_code}")
                print(f"Response: {response.text[:200]}...")
                return []
                
        except Exception as e:
            print(f"❌ Error getting DM threads: {e}")
            return []
    
    def extract_thread_messages(self, thread_id, limit=50):
        """Extract messages from a specific thread with cute rate limiting"""
        print(f"📥 Extracting messages from thread {thread_id}...")
        
        try:
            # Apply cute rate limit before each thread extraction
            self.cute_bypass.apply_cute_rate_limit()
            
            url = f"https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/"
            params = {
                'visual_message_return_type': 'unseen',
                'limit': str(limit)
            }
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                thread = data.get('thread', {})
                messages = thread.get('items', [])
                print(f"✅ Found {len(messages)} messages in thread {thread_id}")
                return thread, messages
            else:
                print(f"❌ Failed to get thread {thread_id}: {response.status_code}")
                if response.status_code == 429:
                    print("⚠️ Rate limited! Applying emergency cute sleep...")
                    self.cute_bypass.emergency_cute_sleep()
                return None, []
                
        except Exception as e:
            print(f"❌ Error extracting thread {thread_id}: {e}")
            return None, []
    
    def save_conversation(self, thread):
        """Save conversation info to database"""
        try:
            thread_id = thread.get('thread_id')
            users = thread.get('users', [])
            
            if users:
                user = users[0]  # Get first user (assuming 1-on-1 conversation)
                
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
        """Main extraction function with cute rate limiting"""
        print("🚀 Starting cute rate DM extraction...")
        
        extraction_stats = {
            'total_threads': 0,
            'successful_extractions': 0,
            'failed_extractions': 0,
            'total_messages': 0,
            'start_time': datetime.now(),
            'rate_limit_bypasses': 0
        }
        
        try:
            # Get all DM threads
            threads = self.get_dm_threads()
            extraction_stats['total_threads'] = len(threads)
            
            if not threads:
                print("❌ No DM threads found")
                return extraction_stats
            
            # Process each thread
            for i, thread in enumerate(threads):
                thread_id = thread.get('thread_id')
                users = thread.get('users', [])
                user_name = users[0].get('username', 'Unknown') if users else 'Unknown'
                
                print(f"\n🔄 Processing thread {i+1}/{len(threads)}: {user_name} (ID: {thread_id})")
                
                # Extract messages from thread
                thread_detail, messages = self.extract_thread_messages(thread_id)
                
                if thread_detail and messages:
                    # Save to database
                    self.save_conversation(thread_detail)
                    self.save_messages(thread_id, messages)
                    
                    extraction_stats['successful_extractions'] += 1
                    extraction_stats['total_messages'] += len(messages)
                    extraction_stats['rate_limit_bypasses'] += 1
                    
                    print(f"✅ Successfully extracted {len(messages)} messages from {user_name}")
                else:
                    extraction_stats['failed_extractions'] += 1
                    print(f"❌ Failed to extract messages from {user_name}")
                
                # Cute sleep between threads
                print("💤 Applying cute sleep between threads...")
                time.sleep(random.uniform(2, 5))
            
            extraction_stats['end_time'] = datetime.now()
            extraction_stats['duration'] = extraction_stats['end_time'] - extraction_stats['start_time']
            
            # Save extraction report
            self.save_extraction_report(extraction_stats)
            
            print(f"\n🎉 Extraction complete!")
            print(f"📊 Total threads: {extraction_stats['total_threads']}")
            print(f"✅ Successful: {extraction_stats['successful_extractions']}")
            print(f"❌ Failed: {extraction_stats['failed_extractions']}")
            print(f"💬 Total messages: {extraction_stats['total_messages']}")
            print(f"⏱️ Duration: {extraction_stats['duration']}")
            
            return extraction_stats
            
        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            return extraction_stats
    
    def save_extraction_report(self, stats):
        """Save extraction report to JSON"""
        try:
            report_file = f"data/cute_rate_extraction_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # Convert datetime objects to strings
            stats_copy = stats.copy()
            for key, value in stats_copy.items():
                if isinstance(value, datetime):
                    stats_copy[key] = value.isoformat()
            
            with open(report_file, 'w') as f:
                json.dump(stats_copy, f, indent=2)
            
            print(f"📄 Extraction report saved: {report_file}")
            
        except Exception as e:
            print(f"❌ Failed to save report: {e}")
    
    def close(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    print("🎯 Cute Rate Limit DM Extractor Starting...")
    print("=" * 50)
    
    extractor = None
    try:
        # Initialize extractor
        extractor = CuteRateDMExtractor()
        
        # Start extraction
        stats = extractor.extract_all_dms()
        
        print("\n" + "=" * 50)
        print("🎊 Cute Rate Extraction Complete!")
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if extractor:
            extractor.close()

if __name__ == "__main__":
    main()
