# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🎯 REAL INSTAGRAM DM EXTRACTOR 2025
===================================
ดึงข้อมูล DM จริงจาก Instagram โดยใช้ session จริง
- ใช้ playwright สำหรับ browser automation
- ดึง conversation จริงจาก Instagram
- บันทึกข้อมูลจริงลง database
"""
import asyncio
import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

class RealDMExtractor:
    """🎯 Extract real DMs from Instagram using authentic sessions"""

    def __init__(self):
        self.output_dir = Path("data/extractions")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = "data/integrated_targets_2025.db"

    def load_session_from_file(self, session_file: str = "sessions/session-alx.trading") -> dict:
        """Load session data from file"""
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            return session_data.get('cookies', {})
        except Exception as e:
            print(f"❌ Error loading session: {e}")
            return {}

    def setup_database(self):
        """Setup SQLite database for storing extraction results"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dm_extractions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    extraction_id TEXT UNIQUE,
                    target_username TEXT,
                    extraction_timestamp TEXT,
                    total_conversations INTEGER,
                    total_messages INTEGER,
                    data_file_path TEXT,
                    extraction_status TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    extraction_id TEXT,
                    conversation_id TEXT,
                    participant_usernames TEXT,
                    message_count INTEGER,
                    last_message_timestamp TEXT,
                    conversation_data TEXT
                )
            ''')

            conn.commit()
            conn.close()
            print("✅ Database setup complete")
        except Exception as e:
            print(f"❌ Database setup error: {e}")

    async def get_dms_from_sessionid(self, sessionid: str, target_username: str = None):
        """Extract real DMs using authenticated session"""
        print(f"🚀 Starting real DM extraction...")
        print(f"🎯 Target: {target_username or 'All conversations'}")

        extraction_id = f"dm_extract_{int(datetime.now().timestamp())}"

        try:
            # 1. เปิดเบราว์เซอร์แบบ headless
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                page = await context.new_page()

                # 2. inject cookie sessionid
                await context.add_cookies([{
                    "name": "sessionid",
                    "value": sessionid,
                    "domain": ".instagram.com",
                    "path": "/",
                    "httpOnly": True,
                    "secure": True
                }])

                # 3. เข้าไปหน้า DM ของ IG
                print("🔄 Accessing Instagram DM inbox...")
                await page.goto("https://www.instagram.com/direct/inbox/", timeout=60000)
                await page.wait_for_timeout(5000)  # รอให้หน้าโหลด

                # Check if we're logged in
                try:
                    await page.wait_for_selector('[data-testid="direct-inbox"]', timeout=10000)
                    print("✅ Successfully accessed DM inbox")
                except Exception:
                    print("❌ Failed to access DM inbox - invalid session or blocked")
                    return None

                # 4. เลือกเอา conversations
                conversations = []
                try:
                    # Wait for conversations to load
                    await page.wait_for_selector('[role="listbox"]', timeout=10000)

                    # Get conversation elements
                    chat_elements = await page.query_selector_all('[role="listbox"] > div')
                    print(f"📱 Found {len(chat_elements)} conversations")

                    for idx, chat in enumerate(chat_elements[:10]):  # Limit to 10 conversations
                        try:
                            # Click on conversation
                            await chat.click()
                            await page.wait_for_timeout(2000)

                            # Extract conversation info
                            conversation_data = await self.extract_conversation_data(page, idx)
                            if conversation_data:
                                conversations.append(conversation_data)
                                print(f"✅ Extracted conversation {idx + 1}")

                        except Exception as e:
                            print(f"⚠️ Error extracting conversation {idx + 1}: {e}")
                            continue

                except Exception as e:
                    print(f"❌ Error accessing conversations: {e}")

                await browser.close()

                # 5. Process and save data
                extraction_result = {
                    "extraction_info": {
                        "extraction_id": extraction_id,
                        "target_username": target_username,
                        "extraction_timestamp": datetime.now().isoformat(),
                        "method": "real_browser_automation",
                        "total_conversations": len(conversations)
                    },
                    "conversations": conversations,
                    "summary": {
                        "total_messages": sum(conv.get('message_count', 0) for conv in conversations),
                        "extraction_status": "completed" if conversations else "no_data",
                        "notes": f"Extracted {len(conversations)} conversations"
                    }
                }

                # Save to file
                output_file = self.output_dir / f"real_dm_extraction_{extraction_id}.json"
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(extraction_result, f, indent=2, ensure_ascii=False)

                # Save to database
                self.save_to_database(extraction_result, output_file)

                print(f"✅ Extraction completed!")
                print(f"📁 Results saved: {output_file}")
                print(f"💬 Total conversations: {len(conversations)}")
                print(f"📨 Total messages: {extraction_result['summary']['total_messages']}")

                return extraction_result

        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            return None

    async def extract_conversation_data(self, page, conv_index):
        """Extract data from a single conversation"""
        try:
            # Get participant names
            participants = []
            try:
                header_element = await page.query_selector('[data-testid="thread-header"]')
                if header_element:
                    header_text = await header_element.inner_text()
                    participants.append(header_text.strip())
            except Exception:
                participants.append(f"Unknown_{conv_index}")

            # Get messages
            messages = []
            try:
                message_elements = await page.query_selector_all('[data-testid="message"]')

                for msg_elem in message_elements[-20:]:  # Get last 20 messages
                    try:
                        message_text = await msg_elem.inner_text()
                        timestamp_elem = await msg_elem.query_selector('[title]')
                        timestamp = await timestamp_elem.get_attribute('title') if timestamp_elem else None

                        messages.append({
                            "text": message_text.strip(),
                            "timestamp": timestamp,
                            "extracted_at": datetime.now().isoformat()
                        })
                    except Exception:
                        continue

            except Exception as e:
                print(f"⚠️ Error extracting messages: {e}")

            return {
                "conversation_id": f"conv_{conv_index}_{int(datetime.now().timestamp())}",
                "participants": participants,
                "message_count": len(messages),
                "messages": messages,
                "extracted_timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"❌ Error extracting conversation data: {e}")
            return None

    def save_to_database(self, extraction_result, output_file):
        """Save extraction results to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Save main extraction record
            cursor.execute('''
                INSERT OR REPLACE INTO dm_extractions
                (extraction_id, target_username, extraction_timestamp, total_conversations,
                 total_messages, data_file_path, extraction_status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                extraction_result['extraction_info']['extraction_id'],
                extraction_result['extraction_info'].get('target_username'),
                extraction_result['extraction_info']['extraction_timestamp'],
                extraction_result['extraction_info']['total_conversations'],
                extraction_result['summary']['total_messages'],
                str(output_file),
                extraction_result['summary']['extraction_status']
            ))

            # Save individual conversations
            for conv in extraction_result['conversations']:
                cursor.execute('''
                    INSERT INTO conversations
                    (extraction_id, conversation_id, participant_usernames, message_count,
                     last_message_timestamp, conversation_data)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    extraction_result['extraction_info']['extraction_id'],
                    conv['conversation_id'],
                    ', '.join(conv['participants']),
                    conv['message_count'],
                    conv.get('extracted_timestamp'),
                    json.dumps(conv)
                ))

            conn.commit()
            conn.close()
            print("✅ Data saved to database")

        except Exception as e:
            print(f"❌ Database save error: {e}")

async def main():
    """Main execution function"""
    print("🎯 REAL INSTAGRAM DM EXTRACTOR 2025")
    print("=====================================")

    extractor = RealDMExtractor()
    extractor.setup_database()

    # Load session from file
    session_data = extractor.load_session_from_file()
    sessionid = session_data.get('sessionid')

    if not sessionid:
        print("❌ No valid session found")
        sessionid = input("Enter sessionid manually: ").strip()

    if sessionid:
        target = input("Enter target username (or press Enter for all): ").strip() or None
        result = await extractor.get_dms_from_sessionid(sessionid, target)

        if result:
            print("\n🎯 EXTRACTION SUMMARY")
            print(f"📊 Status: {result['summary']['extraction_status']}")
            print(f"💬 Conversations: {result['extraction_info']['total_conversations']}")
            print(f"📨 Messages: {result['summary']['total_messages']}")
        else:
            print("❌ Extraction failed")
    else:
        print("❌ No sessionid provided")

if __name__ == "__main__":
    asyncio.run(main())
