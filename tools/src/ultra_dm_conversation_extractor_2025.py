# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
💬🔓 ULTRA DM CONVERSATION EXTRACTOR 2025 🔓💬
==============================================
- Extract Instagram DMs with BOTH conversation sides
- Fresh cookie injection system
- Real-time conversation mapping
- Personal message recovery
- Thread-based extraction

ระบบดึงข้อความ DM ทั้งสองฝั่งแบบสมบูรณ์!

Created by: น้องจิน (chin4d0ll) ♥️
For: Advanced Instagram Intelligence Operations
"""

import asyncio
import aiohttp
import json
import time
import random
import re
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
import base64
import hashlib
import warnings
warnings.filterwarnings("ignore")

class UltraDMConversationExtractor:
    """💬 ระบบดึง DM แบบสมบูรณ์ทั้งสองฝั่ง"""

    def __init__(self, db_path="instagram_sessions_2025.db"):
        self.db_path = db_path
        self.session_data = {}
        self.conversation_cache = {}
        self.extraction_stats = {
            'conversations_found': 0,
            'messages_extracted': 0,
            'media_extracted': 0,
            'participants_mapped': 0
        }

        # Instagram API endpoints
        self.api_endpoints = {
            'inbox': 'https://www.instagram.com/api/v1/direct_v2/inbox/',
            'thread': 'https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/',
            'thread_items': 'https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/items/',
            'user_info': 'https://www.instagram.com/api/v1/users/{user_id}/info/',
        }

        # Headers for requests
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Mobile/15E148 Safari/604.1',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': '',
            'X-Instagram-AJAX': '1',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        print("💬 Ultra DM Conversation Extractor สร้างเสร็จแล้ว!")

    def load_fresh_session(self, session_file_path: str = None) -> bool:
        """โหลด session ใหม่จากไฟล์"""
        try:
            if session_file_path is None:
                # หา session file ล่าสุด
                session_files = list(Path('.').glob('*session*.json'))
                if not session_files:
                    print("❌ ไม่พบ session files!")
                    return False
                session_file_path = max(session_files, key=lambda f: f.stat().st_mtime)

            with open(session_file_path, 'r') as f:
                session_data = json.load(f)

            if 'sessionid' in session_data:
                self.session_data = session_data
                self.base_headers['Cookie'] = f"sessionid={session_data['sessionid']}"
                self.base_headers['X-CSRFToken'] = session_data.get('csrf_token', 'missing')

                print(f"✅ โหลด session สำเร็จจาก {session_file_path}")
                return True
            else:
                print("❌ Session data ไม่ถูกต้อง!")
                return False

        except Exception as e:
            print(f"❌ Error loading session: {e}")
            return False

    async def inject_fresh_cookies(self, target_username: str) -> bool:
        """ฉีดคุกกี้ใหม่เพื่อเข้าถึง Instagram"""
        try:
            # สร้าง session ใหม่
            async with aiohttp.ClientSession() as session:
                # ขั้นตอน 1: ไปหน้า Instagram login
                login_url = "https://www.instagram.com/accounts/login/"
                async with session.get(login_url, headers=self.base_headers) as response:
                    if response.status == 200:
                        text = await response.text()

                        # Extract CSRF token
                        csrf_match = re.search(r'"csrf_token":"([^"]+)"', text)
                        if csrf_match:
                            csrf_token = csrf_match.group(1)
                            self.base_headers['X-CSRFToken'] = csrf_token

                        print(f"✅ ได้ CSRF token แล้ว: {csrf_token[:20]}...")

                        # อัพเดต cookies
                        cookies = session.cookie_jar.filter_cookies(login_url)
                        cookie_str = "; ".join([f"{c.key}={c.value}" for c in cookies])
                        self.base_headers['Cookie'] = cookie_str

                        return True

        except Exception as e:
            print(f"❌ Cookie injection failed: {e}")
            return False

    async def get_dm_inbox(self) -> Optional[Dict]:
        """ดึงรายการ DM ทั้งหมด"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.api_endpoints['inbox'],
                    headers=self.base_headers
                ) as response:

                    if response.status == 200:
                        data = await response.json()
                        print(f"✅ ดึง inbox สำเร็จ - พบ {len(data.get('inbox', {}).get('threads', []))} conversations")
                        return data
                    else:
                        print(f"❌ Failed to get inbox - Status: {response.status}")
                        error_text = await response.text()
                        print(f"Error response: {error_text[:500]}")
                        return None

        except Exception as e:
            print(f"❌ Error getting inbox: {e}")
            return None

    async def extract_conversation_thread(self, thread_id: str, thread_info: Dict) -> Dict:
        """ดึงข้อความในการสนทนาทั้งหมด"""
        try:
            conversation_data = {
                'thread_id': thread_id,
                'participants': [],
                'messages': [],
                'media': [],
                'metadata': {
                    'extracted_at': datetime.now().isoformat(),
                    'message_count': 0,
                    'date_range': {},
                }
            }

            # ดึงข้อมูลผู้เข้าร่วม
            for user in thread_info.get('users', []):
                participant = {
                    'user_id': user.get('pk'),
                    'username': user.get('username'),
                    'full_name': user.get('full_name'),
                    'profile_pic_url': user.get('profile_pic_url'),
                    'is_verified': user.get('is_verified', False),
                    'is_private': user.get('is_private', False)
                }
                conversation_data['participants'].append(participant)
                self.extraction_stats['participants_mapped'] += 1

            # ดึงข้อความทั้งหมด
            cursor = None
            page_count = 0
            max_pages = 50  # จำกัดการดึงข้อมูล

            while page_count < max_pages:
                try:
                    # สร้าง URL สำหรับดึงข้อความ
                    items_url = self.api_endpoints['thread_items'].format(thread_id=thread_id)
                    if cursor:
                        items_url += f"?cursor={cursor}"

                    async with aiohttp.ClientSession() as session:
                        async with session.get(items_url, headers=self.base_headers) as response:

                            if response.status == 200:
                                data = await response.json()
                                items = data.get('thread', {}).get('items', [])

                                if not items:
                                    break

                                # Process each message
                                for item in items:
                                    message = await self._process_message_item(item)
                                    if message:
                                        conversation_data['messages'].append(message)
                                        self.extraction_stats['messages_extracted'] += 1

                                # Check for next page
                                cursor = data.get('thread', {}).get('oldest_cursor')
                                if not cursor:
                                    break

                                page_count += 1
                                await asyncio.sleep(random.uniform(0.5, 1.5))  # Rate limiting

                            else:
                                print(f"❌ Failed to get thread items - Status: {response.status}")
                                break

                except Exception as e:
                    print(f"⚠️ Error in thread extraction page {page_count}: {e}")
                    break

            # Update metadata
            if conversation_data['messages']:
                conversation_data['metadata']['message_count'] = len(conversation_data['messages'])
                timestamps = [msg['timestamp'] for msg in conversation_data['messages'] if msg.get('timestamp')]
                if timestamps:
                    conversation_data['metadata']['date_range'] = {
                        'earliest': min(timestamps),
                        'latest': max(timestamps)
                    }

            print(f"✅ Extracted {len(conversation_data['messages'])} messages from thread {thread_id}")
            return conversation_data

        except Exception as e:
            print(f"❌ Error extracting conversation: {e}")
            return {}

    async def _process_message_item(self, item: Dict) -> Optional[Dict]:
        """ประมวลผลข้อความแต่ละรายการ"""
        try:
            message_data = {
                'item_id': item.get('item_id'),
                'item_type': item.get('item_type'),
                'user_id': item.get('user_id'),
                'timestamp': item.get('timestamp'),
                'message_text': '',
                'media_data': {},
                'reactions': [],
                'reply_to': None,
                'is_sent_by_viewer': item.get('is_sent_by_viewer', False)
            }

            # Extract text message
            if item.get('text'):
                message_data['message_text'] = item['text']

            # Extract media
            if item.get('media'):
                media_data = await self._extract_media_data(item['media'])
                message_data['media_data'] = media_data
                if media_data:
                    self.extraction_stats['media_extracted'] += 1

            # Extract reactions
            if item.get('reactions'):
                message_data['reactions'] = item['reactions']['emojis']

            # Extract reply information
            if item.get('replied_to_message'):
                message_data['reply_to'] = {
                    'item_id': item['replied_to_message'].get('item_id'),
                    'text': item['replied_to_message'].get('text', '')
                }

            return message_data

        except Exception as e:
            print(f"⚠️ Error processing message item: {e}")
            return None

    async def _extract_media_data(self, media: Dict) -> Dict:
        """ดึงข้อมูล media จากข้อความ"""
        try:
            media_data = {
                'media_type': media.get('media_type'),
                'image_versions': [],
                'video_versions': [],
                'audio_data': {}
            }

            # Image data
            if media.get('image_versions2', {}).get('candidates'):
                media_data['image_versions'] = media['image_versions2']['candidates']

            # Video data
            if media.get('video_versions'):
                media_data['video_versions'] = media['video_versions']

            # Audio data (voice messages)
            if media.get('audio'):
                media_data['audio_data'] = {
                    'audio_src': media['audio'].get('audio_src'),
                    'duration': media['audio'].get('duration'),
                    'waveform_data': media['audio'].get('waveform_data')
                }

            return media_data

        except Exception as e:
            print(f"⚠️ Error extracting media: {e}")
            return {}

    async def extract_all_conversations_for_target(self, target_username: str) -> Dict:
        """ดึงการสนทนาทั้งหมดของเป้าหมาย"""
        try:
            print(f"🎯 เริ่มดึงข้อมูล DM สำหรับ {target_username}")

            # โหลด session ใหม่
            if not self.load_fresh_session():
                print("❌ ไม่สามารถโหลด session ได้!")
                return {}

            # ฉีดคุกกี้ใหม่
            if not await self.inject_fresh_cookies(target_username):
                print("⚠️ Cookie injection ล้มเหลว แต่จะลองดำเนินการต่อ...")

            # ดึง inbox
            inbox_data = await self.get_dm_inbox()
            if not inbox_data:
                print("❌ ไม่สามารถดึง inbox ได้!")
                return {}

            # ประมวลผลการสนทนาทั้งหมด
            all_conversations = {
                'target': target_username,
                'extracted_at': datetime.now().isoformat(),
                'conversations': [],
                'summary': {
                    'total_conversations': 0,
                    'total_messages': 0,
                    'total_participants': 0,
                    'total_media': 0
                }
            }

            threads = inbox_data.get('inbox', {}).get('threads', [])
            print(f"💬 พบ {len(threads)} การสนทนา")

            # ดึงข้อมูลการสนทนาทีละอัน
            for thread in threads[:10]:  # จำกัดที่ 10 การสนทนาแรก
                thread_id = thread.get('thread_id')
                if thread_id:
                    print(f"📥 กำลังดึงการสนทนา {thread_id}")

                    conversation = await self.extract_conversation_thread(thread_id, thread)
                    if conversation:
                        all_conversations['conversations'].append(conversation)
                        self.extraction_stats['conversations_found'] += 1

                    # พักระหว่างการดึงข้อมูล
                    await asyncio.sleep(random.uniform(1, 3))

            # อัพเดต summary
            all_conversations['summary'] = {
                'total_conversations': len(all_conversations['conversations']),
                'total_messages': sum(len(c.get('messages', [])) for c in all_conversations['conversations']),
                'total_participants': sum(len(c.get('participants', [])) for c in all_conversations['conversations']),
                'total_media': self.extraction_stats['media_extracted']
            }

            print(f"✅ สำเร็จ! ดึงได้ {all_conversations['summary']['total_conversations']} การสนทนา")
            print(f"📊 สถิติการดึงข้อมูล: {self.extraction_stats}")

            return all_conversations

        except Exception as e:
            print(f"❌ Error in conversation extraction: {e}")
            return {}

    def save_conversations_to_file(self, conversations_data: Dict, target_username: str):
        """บันทึกข้อมูลการสนทนาลงไฟล์"""
        try:
            timestamp = int(time.time())
            filename = f"ultra_dm_conversations_{target_username}_{timestamp}.json"

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(conversations_data, f, ensure_ascii=False, indent=2)

            print(f"💾 บันทึกข้อมูลลง {filename} แล้ว")
            print(f"📊 ข้อมูลที่บันทึก:")
            print(f"   - การสนทนา: {conversations_data['summary']['total_conversations']}")
            print(f"   - ข้อความ: {conversations_data['summary']['total_messages']}")
            print(f"   - ผู้เข้าร่วม: {conversations_data['summary']['total_participants']}")
            print(f"   - สื่อ: {conversations_data['summary']['total_media']}")

            return filename

        except Exception as e:
            print(f"❌ Error saving conversations: {e}")
            return None

    def save_to_database(self, conversations_data: Dict, target_username: str):
        """บันทึกข้อมูลลงฐานข้อมูล"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # สร้างตารางถ้ายังไม่มี
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dm_conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target_username TEXT,
                    thread_id TEXT,
                    participant_data TEXT,
                    message_data TEXT,
                    extraction_timestamp TEXT,
                    message_count INTEGER,
                    media_count INTEGER
                )
            ''')

            # บันทึกข้อมูลการสนทนา
            for conversation in conversations_data.get('conversations', []):
                cursor.execute('''
                    INSERT INTO dm_conversations
                    (target_username, thread_id, participant_data, message_data,
                     extraction_timestamp, message_count, media_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    target_username,
                    conversation.get('thread_id'),
                    json.dumps(conversation.get('participants', []), ensure_ascii=False),
                    json.dumps(conversation.get('messages', []), ensure_ascii=False),
                    datetime.now().isoformat(),
                    len(conversation.get('messages', [])),
                    len([msg for msg in conversation.get('messages', []) if msg.get('media_data')])
                ))

            conn.commit()
            conn.close()

            print(f"✅ บันทึกข้อมูลลงฐานข้อมูล {self.db_path} แล้ว")

        except Exception as e:
            print(f"❌ Error saving to database: {e}")

async def main():
    """ฟังก์ชันหลักสำหรับทดสอบ"""
    extractor = UltraDMConversationExtractor()

    # เป้าหมายที่จะดึงข้อมูล
    targets = ["whatilove1728", "alx.trading"]

    for target in targets:
        print(f"\n🎯 เริ่มดึงข้อมูล DM สำหรับ {target}")
        print("="*50)

        # ดึงการสนทนาทั้งหมด
        conversations = await extractor.extract_all_conversations_for_target(target)

        if conversations:
            # บันทึกลงไฟล์
            filename = extractor.save_conversations_to_file(conversations, target)

            # บันทึกลงฐานข้อมูล
            extractor.save_to_database(conversations, target)

            print(f"✅ เสร็จสิ้นการดึงข้อมูลสำหรับ {target}")
        else:
            print(f"❌ ไม่สามารถดึงข้อมูลสำหรับ {target} ได้")

        # พักระหว่างเป้าหมาย
        await asyncio.sleep(5)

if __name__ == "__main__":
    print("💬🔓 Ultra DM Conversation Extractor 2025 🔓💬")
    print("ระบบดึงข้อความ DM ทั้งสองฝั่งแบบสมบูรณ์!")
    print("="*60)

    asyncio.run(main())
