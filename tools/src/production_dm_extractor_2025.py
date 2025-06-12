# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🎯 PRODUCTION DM EXTRACTOR 2025 - REAL DATA ONLY
================================================
Production-ready Instagram DM extractor using REAL data and sessions
- No mockup, no simulation, only real extraction
- Uses authentic session cookies
- Extracts real conversations and messages
- Professional database logging
- Error handling and recovery
"""
import asyncio
import json
import os
import sqlite3
import requests
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

class ProductionDMExtractor:
    """🎯 Production-ready DM extractor for real Instagram data"""

    def __init__(self, target_username: str = "alx.trading"):
        self.target = target_username
        self.output_dir = Path("data/extractions")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = "data/integrated_targets_2025.db"
        self.session_data = None

    def setup_database(self):
        """Setup SQLite database for production use"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS production_extractions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    extraction_id TEXT UNIQUE,
                    target_username TEXT,
                    extraction_timestamp TEXT,
                    method TEXT,
                    status TEXT,
                    total_conversations INTEGER,
                    total_messages INTEGER,
                    data_file_path TEXT,
                    error_message TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS real_conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    extraction_id TEXT,
                    conversation_id TEXT,
                    participants TEXT,
                    message_count INTEGER,
                    last_activity TEXT,
                    conversation_data TEXT
                )
            ''')

            conn.commit()
            conn.close()
            print("✅ Production database ready")
        except Exception as e:
            print(f"❌ Database error: {e}")

    def load_production_session(self):
        """Load production session data"""
        session_files = [
            "sessions/session-alx.trading",
            "data/sessions/session_example.json",
            "sessions/quick_bypass_session.json"
        ]

        for session_file in session_files:
            try:
                if os.path.exists(session_file):
                    with open(session_file, 'r') as f:
                        data = json.load(f)

                    # Handle different session formats
                    if 'cookies' in data:
                        self.session_data = data['cookies']
                    elif 'sessionid' in data:
                        self.session_data = data
                    else:
                        continue

                    print(f"✅ Loaded session from {session_file}")
                    return True

            except Exception as e:
                print(f"⚠️ Error loading {session_file}: {e}")
                continue

        print("❌ No valid session found")
        return False

    async def extract_via_browser_automation(self):
        """Extract DMs using Playwright browser automation"""
        print("🤖 Starting browser automation extraction...")

        if not self.session_data or 'sessionid' not in self.session_data:
            print("❌ No valid sessionid for browser automation")
            return None

        extraction_id = f"browser_extract_{int(datetime.now().timestamp())}"

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-blink-features=AutomationControlled']
                )
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    viewport={'width': 1920, 'height': 1080}
                )
                page = await context.new_page()

                # Set session cookie
                await context.add_cookies([{
                    "name": "sessionid",
                    "value": self.session_data['sessionid'],
                    "domain": ".instagram.com",
                    "path": "/",
                    "httpOnly": True,
                    "secure": True
                }])

                # Navigate to Instagram DMs
                print("🔄 Accessing Instagram...")
                await page.goto("https://www.instagram.com/direct/inbox/", timeout=30000)
                await page.wait_for_timeout(3000)

                # Check authentication
                current_url = page.url
                if "accounts/login" in current_url:
                    print("❌ Session expired or invalid")
                    await browser.close()
                    return None

                print("✅ Successfully authenticated")

                # Extract conversations
                conversations = await self.extract_conversations_from_page(page)
                await browser.close()

                result = {
                    "extraction_id": extraction_id,
                    "method": "browser_automation",
                    "target": self.target,
                    "timestamp": datetime.now().isoformat(),
                    "conversations": conversations,
                    "total_conversations": len(conversations),
                    "total_messages": sum(c.get('message_count', 0) for c in conversations)
                }

                return result

        except Exception as e:
            print(f"❌ Browser extraction failed: {e}")
            return None

    async def extract_conversations_from_page(self, page):
        """Extract conversation data from Instagram page"""
        conversations = []

        try:
            # Wait for inbox to load
            await page.wait_for_selector('[aria-label="Primary"]', timeout=10000)

            # Get conversation list
            conversation_elements = await page.query_selector_all('[role="listbox"] > div')
            print(f"📱 Found {len(conversation_elements)} conversations")

            for idx, conv_elem in enumerate(conversation_elements[:5]):  # Limit to 5
                try:
                    await conv_elem.click()
                    await page.wait_for_timeout(2000)

                    # Extract conversation data
                    conv_data = await self.extract_single_conversation(page, idx)
                    if conv_data:
                        conversations.append(conv_data)
                        print(f"✅ Extracted conversation {idx + 1}")

                    # Go back to inbox
                    await page.keyboard.press('Escape')
                    await page.wait_for_timeout(1000)

                except Exception as e:
                    print(f"⚠️ Error with conversation {idx + 1}: {e}")
                    continue

        except Exception as e:
            print(f"❌ Error extracting conversations: {e}")

        return conversations

    async def extract_single_conversation(self, page, conv_index):
        """Extract data from a single conversation"""
        try:
            # Get participant info
            participants = []
            try:
                header = await page.query_selector('[data-testid="thread-header"] h1')
                if header:
                    header_text = await header.inner_text()
                    participants.append(header_text.strip())
            except Exception:
                participants.append(f"User_{conv_index}")

            # Get messages
            messages = []
            try:
                message_elements = await page.query_selector_all('[data-testid="message"]')

                for msg_elem in message_elements[-10:]:  # Last 10 messages
                    try:
                        msg_text = await msg_elem.inner_text()

                        # Try to get timestamp
                        timestamp = None
                        time_elem = await msg_elem.query_selector('[title]')
                        if time_elem:
                            timestamp = await time_elem.get_attribute('title')

                        messages.append({
                            "text": msg_text.strip(),
                            "timestamp": timestamp,
                            "extracted_at": datetime.now().isoformat()
                        })
                    except Exception:
                        continue

            except Exception as e:
                print(f"⚠️ Error extracting messages: {e}")

            return {
                "conversation_id": f"real_conv_{conv_index}_{int(datetime.now().timestamp())}",
                "participants": participants,
                "message_count": len(messages),
                "messages": messages,
                "target_involved": any(self.target.lower() in p.lower() for p in participants),
                "extracted_at": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"❌ Error extracting conversation: {e}")
            return None

    def extract_via_api_requests(self):
        """Extract using direct API requests"""
        print("🌐 Starting API request extraction...")

        if not self.session_data:
            print("❌ No session data for API requests")
            return None

        try:
            session = requests.Session()

            # Set headers
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/'
            })

            # Set cookies
            for key, value in self.session_data.items():
                session.cookies.set(key, value, domain='.instagram.com')

            # Test profile access
            profile_url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={self.target}"
            response = session.get(profile_url)

            if response.status_code == 200:
                profile_data = response.json()
                print(f"✅ Successfully accessed {self.target} profile")

                result = {
                    "extraction_id": f"api_extract_{int(datetime.now().timestamp())}",
                    "method": "api_requests",
                    "target": self.target,
                    "timestamp": datetime.now().isoformat(),
                    "profile_data": profile_data,
                    "status": "profile_accessible"
                }

                return result
            else:
                print(f"❌ API request failed: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ API extraction failed: {e}")
            return None

    def save_extraction_result(self, result):
        """Save extraction result to file and database"""
        if not result:
            print("❌ No result to save")
            return

        try:
            # Save to file
            timestamp = int(datetime.now().timestamp())
            filename = f"production_extraction_{self.target}_{timestamp}.json"
            output_file = self.output_dir / filename

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            print(f"📁 Saved results: {output_file}")

            # Save to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO production_extractions
                (extraction_id, target_username, extraction_timestamp, method, status,
                 total_conversations, total_messages, data_file_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                result.get('extraction_id'),
                self.target,
                result.get('timestamp'),
                result.get('method'),
                'completed',
                result.get('total_conversations', 0),
                result.get('total_messages', 0),
                str(output_file)
            ))

            conn.commit()
            conn.close()
            print("✅ Saved to database")

        except Exception as e:
            print(f"❌ Save error: {e}")

    async def run_production_extraction(self):
        """Run production extraction with multiple methods"""
        print("🎯 PRODUCTION DM EXTRACTOR 2025")
        print("=" * 40)
        print(f"Target: {self.target}")
        print("Methods: Browser automation + API requests")
        print()

        self.setup_database()

        if not self.load_production_session():
            print("❌ Cannot proceed without valid session")
            return

        # Try browser automation first
        print("\n🤖 Method 1: Browser Automation")
        browser_result = await self.extract_via_browser_automation()

        if browser_result:
            self.save_extraction_result(browser_result)
            print(f"✅ Browser extraction successful: {browser_result['total_conversations']} conversations")
        else:
            print("❌ Browser extraction failed")

        # Try API requests
        print("\n🌐 Method 2: API Requests")
        api_result = self.extract_via_api_requests()

        if api_result:
            self.save_extraction_result(api_result)
            print(f"✅ API extraction successful")
        else:
            print("❌ API extraction failed")

        # Summary
        print(f"\n🎯 EXTRACTION SUMMARY")
        print(f"Target: {self.target}")
        print(f"Browser method: {'✅ Success' if browser_result else '❌ Failed'}")
        print(f"API method: {'✅ Success' if api_result else '❌ Failed'}")

        if browser_result:
            print(f"Conversations extracted: {browser_result.get('total_conversations', 0)}")
            print(f"Messages extracted: {browser_result.get('total_messages', 0)}")

async def main():
    """Main execution"""
    target = input("Enter target username [alx.trading]: ").strip() or "alx.trading"

    extractor = ProductionDMExtractor(target)
    await extractor.run_production_extraction()

if __name__ == "__main__":
    asyncio.run(main())
