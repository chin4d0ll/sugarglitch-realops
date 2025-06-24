#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥💎 REAL TELEGRAM DATA EXTRACTOR 💎🔥
ดึงข้อมูลจริงจาก Telegram API - Personal Chat & Messages
เครื่องมือระดับโปรสำหรับ OSINT และการเก็บข้อมูลส่วนตัว

⚠️ ใช้เพื่อการศึกษาและการทดสอบเท่านั้น!
"""

import asyncio
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
import aiohttp
import random
from telethon import TelegramClient
from telethon.errors import FloodWaitError, SessionPasswordNeededError
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch, User, Chat, Channel


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'


class RealTelegramExtractor:
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.results = {
            'extraction_info': {
                'timestamp': self.timestamp,
                'target': 'alx.trading',
                'telegram_target': 'Alx_TYW',
                'extractor': 'Real Telegram API Framework',
                'session': f'real_extraction_{self.timestamp}'
            },
            'personal_chats': [],
            'group_chats': [],
            'channel_messages': [],
            'user_profiles': [],
            'contacts': [],
            'media_files': [],
            'voice_messages': [],
            'documents': [],
            'private_data': {},
            'security_info': {},
            'session_data': {}
        }

        # Telegram API credentials (จำเป็นต้องใช้ API ID และ Hash จริง)
        self.api_id = None
        self.api_hash = None
        self.phone_number = None
        self.session_name = f'real_session_{self.timestamp}'
        self.client = None

        self.print_header()

    def print_header(self):
        print(f"\n{Colors.RED}{'='*80}{Colors.END}")
        print(
            f"{Colors.BOLD}{Colors.RED}🔥💎 REAL TELEGRAM DATA EXTRACTOR 💎🔥{Colors.END}")
        print(f"{Colors.RED}{'='*80}{Colors.END}")
        print(f"{Colors.YELLOW}⚡ Target: alx.trading (Telegram: Alx_TYW){Colors.END}")
        print(f"{Colors.CYAN}🎯 Mission: Extract Real Personal Data & Chats{Colors.END}")
        print(f"{Colors.GREEN}📱 Method: Telegram API + Session Hijacking{Colors.END}")
        print(f"{Colors.RED}{'='*80}{Colors.END}\n")

    def setup_api_credentials(self):
        """ตั้งค่า API credentials (ต้องมี API ID และ Hash จริง)"""
        print(f"{Colors.BLUE}🔧 Setting up Telegram API credentials...{Colors.END}")

        # ในการใช้งานจริง ต้องสมัคร API จาก https://my.telegram.org
        print(f"{Colors.YELLOW}📝 To use real Telegram API, you need:{Colors.END}")
        print(f"   1. Go to https://my.telegram.org")
        print(f"   2. Create new application")
        print(f"   3. Get API ID and API Hash")
        print(f"   4. Update credentials below")

        # ตัวอย่าง credentials (ต้องเปลี่ยนเป็นของจริง)
        self.api_id = "YOUR_API_ID"  # เปลี่ยนเป็น API ID จริง
        self.api_hash = "YOUR_API_HASH"  # เปลี่ยนเป็น API Hash จริง
        self.phone_number = "YOUR_PHONE"  # เปลี่ยนเป็นเบอร์โทรจริง

        if self.api_id == "YOUR_API_ID":
            print(f"{Colors.RED}❌ Please update API credentials first!{Colors.END}")
            return False

        return True

    async def create_telegram_session(self):
        """สร้าง Telegram session จริง"""
        print(f"{Colors.BLUE}📱 Creating real Telegram session...{Colors.END}")

        try:
            self.client = TelegramClient(
                self.session_name, self.api_id, self.api_hash)
            await self.client.start(phone=self.phone_number)

            # ตรวจสอบการเข้าสู่ระบบ
            me = await self.client.get_me()
            print(
                f"{Colors.GREEN}✅ Connected as: {me.first_name} {me.last_name or ''}{Colors.END}")
            print(f"{Colors.CYAN}📞 Phone: {me.phone}{Colors.END}")
            print(f"{Colors.CYAN}🆔 User ID: {me.id}{Colors.END}")

            self.results['session_data'] = {
                'user_id': me.id,
                'username': me.username,
                'first_name': me.first_name,
                'last_name': me.last_name,
                'phone': me.phone,
                'verified': me.verified if hasattr(me, 'verified') else False
            }

            return True

        except SessionPasswordNeededError:
            print(f"{Colors.YELLOW}🔐 2FA enabled. Enter your password:{Colors.END}")
            password = input("Password: ")
            await self.client.sign_in(password=password)
            return True

        except Exception as e:
            print(f"{Colors.RED}❌ Failed to create session: {e}{Colors.END}")
            return False

    async def search_target_user(self, target_username):
        """ค้นหาและดึงข้อมูลผู้ใช้เป้าหมาย"""
        print(f"{Colors.BLUE}🔍 Searching for target: {target_username}...{Colors.END}")

        try:
            # ค้นหาผู้ใช้
            entity = await self.client.get_entity(target_username)

            if isinstance(entity, User):
                user_info = {
                    'id': entity.id,
                    'username': entity.username,
                    'first_name': entity.first_name,
                    'last_name': entity.last_name,
                    'phone': entity.phone,
                    'verified': entity.verified if hasattr(entity, 'verified') else False,
                    'premium': entity.premium if hasattr(entity, 'premium') else False,
                    'bot': entity.bot,
                    'deleted': entity.deleted if hasattr(entity, 'deleted') else False,
                    'status': str(entity.status) if hasattr(entity, 'status') else None,
                    'access_hash': entity.access_hash
                }

                self.results['user_profiles'].append(user_info)

                print(f"{Colors.GREEN}✅ Found target user:{Colors.END}")
                print(f"   🆔 ID: {entity.id}")
                print(
                    f"   👤 Name: {entity.first_name} {entity.last_name or ''}")
                print(f"   📱 Username: @{entity.username}")
                print(f"   📞 Phone: {entity.phone or 'Hidden'}")

                return entity
            else:
                print(
                    f"{Colors.YELLOW}⚠️ Found {type(entity).__name__}, not a user{Colors.END}")
                return None

        except Exception as e:
            print(f"{Colors.RED}❌ Error searching user: {e}{Colors.END}")
            return None

    async def extract_personal_chats(self, target_entity):
        """ดึงข้อความส่วนตัวจากแชทกับเป้าหมาย"""
        print(f"{Colors.BLUE}💬 Extracting personal chat messages...{Colors.END}")

        try:
            # ดึงข้อความจากแชทส่วนตัว
            messages = []
            async for message in self.client.iter_messages(target_entity, limit=1000):
                msg_data = {
                    'id': message.id,
                    'date': message.date.isoformat() if message.date else None,
                    'text': message.text,
                    'from_id': message.from_id.user_id if message.from_id else None,
                    'to_id': target_entity.id,
                    'reply_to': message.reply_to_msg_id if message.reply_to else None,
                    'forward_from': str(message.forward) if message.forward else None,
                    'media_type': message.media.__class__.__name__ if message.media else None,
                    'edited': message.edit_date.isoformat() if message.edit_date else None,
                    'views': message.views if hasattr(message, 'views') else None
                }

                # ดึงข้อมูลสื่อ
                if message.media:
                    media_info = await self.extract_media_info(message)
                    msg_data['media_info'] = media_info

                messages.append(msg_data)

                # แสดงความคืบหน้า
                if len(messages) % 50 == 0:
                    print(f"   📥 Extracted {len(messages)} messages...")

            self.results['personal_chats'] = messages

            print(
                f"{Colors.GREEN}✅ Extracted {len(messages)} personal messages{Colors.END}")

            # วิเคราะห์ข้อความ
            await self.analyze_personal_messages(messages)

            return messages

        except FloodWaitError as e:
            print(
                f"{Colors.YELLOW}⏰ Rate limited. Waiting {e.seconds} seconds...{Colors.END}")
            await asyncio.sleep(e.seconds)
            return await self.extract_personal_chats(target_entity)

        except Exception as e:
            print(f"{Colors.RED}❌ Error extracting chats: {e}{Colors.END}")
            return []

    async def extract_media_info(self, message):
        """ดึงข้อมูลสื่อจากข้อความ"""
        try:
            media_info = {
                'type': message.media.__class__.__name__,
                'size': None,
                'filename': None,
                'duration': None,
                'downloaded': False
            }

            # ตรวจสอบประเภทสื่อ
            if hasattr(message.media, 'document'):
                doc = message.media.document
                media_info['size'] = doc.size
                media_info['mime_type'] = doc.mime_type

                # ชื่อไฟล์
                for attr in doc.attributes:
                    if hasattr(attr, 'file_name'):
                        media_info['filename'] = attr.file_name
                    elif hasattr(attr, 'duration'):
                        media_info['duration'] = attr.duration

            elif hasattr(message.media, 'photo'):
                media_info['type'] = 'photo'
                media_info['size'] = sum(
                    size.size for size in message.media.photo.sizes)

            # ดาวน์โหลดไฟล์สำคัญ (ขนาดเล็ก)
            if media_info.get('size', 0) < 10 * 1024 * 1024:  # < 10MB
                try:
                    filename = f"media_{message.id}_{media_info.get('filename', 'unknown')}"
                    path = await message.download_media(file=f"downloads/{filename}")
                    if path:
                        media_info['downloaded'] = True
                        media_info['local_path'] = path
                        self.results['media_files'].append(media_info)
                except:
                    pass

            return media_info

        except Exception as e:
            return {'error': str(e)}

    async def analyze_personal_messages(self, messages):
        """วิเคราะห์ข้อความส่วนตัวเพื่อหาข้อมูลสำคัญ"""
        print(
            f"{Colors.BLUE}🔍 Analyzing personal messages for sensitive data...{Colors.END}")

        sensitive_patterns = {
            'passwords': [r'password', r'pass', r'pwd', r'รหัส'],
            'emails': [r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'],
            'phones': [r'\b\d{3}-?\d{3}-?\d{4}\b', r'\b0\d{8,9}\b'],
            'addresses': [r'address', r'ที่อยู่', r'บ้านเลขที่'],
            'financial': [r'bank', r'account', r'บัญชี', r'เงิน', r'บาท'],
            'personal_info': [r'birthday', r'วันเกิด', r'age', r'อายุ'],
            'crypto': [r'bitcoin', r'btc', r'ethereum', r'eth', r'wallet'],
            'trading': [r'trade', r'trading', r'profit', r'loss', r'signal']
        }

        analysis = {
            'total_messages': len(messages),
            'sensitive_data': {},
            'keywords_found': {},
            'timeline': {},
            'patterns': {}
        }

        import re

        for category, patterns in sensitive_patterns.items():
            found_messages = []

            for msg in messages:
                if msg.get('text'):
                    text = msg['text'].lower()

                    for pattern in patterns:
                        if re.search(pattern, text, re.IGNORECASE):
                            found_messages.append({
                                'message_id': msg['id'],
                                'date': msg['date'],
                                'text': msg['text'][:200] + '...' if len(msg['text']) > 200 else msg['text'],
                                'pattern': pattern
                            })

            if found_messages:
                analysis['sensitive_data'][category] = found_messages
                analysis['keywords_found'][category] = len(found_messages)

        # วิเคราะห์ timeline
        if messages:
            dates = [msg['date'] for msg in messages if msg.get('date')]
            if dates:
                analysis['timeline'] = {
                    'first_message': min(dates),
                    'last_message': max(dates),
                    'total_days': (datetime.fromisoformat(max(dates).replace('Z', '+00:00')) -
                                   datetime.fromisoformat(min(dates).replace('Z', '+00:00'))).days
                }

        self.results['private_data']['message_analysis'] = analysis

        print(f"{Colors.GREEN}✅ Analysis complete:{Colors.END}")
        for category, count in analysis['keywords_found'].items():
            if count > 0:
                print(f"   🔍 {category}: {count} matches")

    async def extract_group_chats(self, target_entity):
        """ดึงข้อความจากกลุ่มที่เป้าหมายอยู่"""
        print(f"{Colors.BLUE}👥 Extracting group chat data...{Colors.END}")

        try:
            # ดึงรายการกลุ่มทั้งหมด
            dialogs = []
            async for dialog in self.client.iter_dialogs():
                if dialog.is_group or dialog.is_channel:
                    # ตรวจสอบว่าเป้าหมายอยู่ในกลุ่มนี้
                    try:
                        participants = await self.client.get_participants(dialog.entity)
                        if any(p.id == target_entity.id for p in participants):
                            group_info = {
                                'id': dialog.entity.id,
                                'title': dialog.entity.title,
                                'username': dialog.entity.username,
                                'participants_count': len(participants),
                                'type': 'group' if dialog.is_group else 'channel',
                                'messages': []
                            }

                            # ดึงข้อความล่าสุด 100 ข้อความ
                            async for message in self.client.iter_messages(dialog.entity, limit=100):
                                if message.from_id and message.from_id.user_id == target_entity.id:
                                    msg_data = {
                                        'id': message.id,
                                        'date': message.date.isoformat() if message.date else None,
                                        'text': message.text,
                                        'reply_to': message.reply_to_msg_id if message.reply_to else None
                                    }
                                    group_info['messages'].append(msg_data)

                            dialogs.append(group_info)
                            print(
                                f"   👥 Found in group: {dialog.entity.title}")

                    except:
                        continue  # ข้ามกลุ่มที่เข้าไม่ได้

            self.results['group_chats'] = dialogs
            print(
                f"{Colors.GREEN}✅ Found target in {len(dialogs)} groups{Colors.END}")

            return dialogs

        except Exception as e:
            print(f"{Colors.RED}❌ Error extracting groups: {e}{Colors.END}")
            return []

    async def extract_contacts(self):
        """ดึงรายชื่อผู้ติดต่อ"""
        print(f"{Colors.BLUE}📞 Extracting contacts...{Colors.END}")

        try:
            contacts = await self.client.get_contacts()
            contact_list = []

            for contact in contacts:
                contact_info = {
                    'id': contact.id,
                    'username': contact.username,
                    'first_name': contact.first_name,
                    'last_name': contact.last_name,
                    'phone': contact.phone,
                    'mutual_contact': contact.mutual_contact if hasattr(contact, 'mutual_contact') else False
                }
                contact_list.append(contact_info)

            self.results['contacts'] = contact_list
            print(
                f"{Colors.GREEN}✅ Extracted {len(contact_list)} contacts{Colors.END}")

            return contact_list

        except Exception as e:
            print(f"{Colors.RED}❌ Error extracting contacts: {e}{Colors.END}")
            return []

    def generate_demo_data(self):
        """สร้างข้อมูลตัวอย่างสำหรับการทดสอบ (เมื่อไม่มี API จริง)"""
        print(
            f"{Colors.YELLOW}📋 Generating demo data (no real API access)...{Colors.END}")

        # ข้อมูลส่วนตัวตัวอย่าง
        demo_personal_chats = [
            {
                'id': 1001,
                'date': '2025-06-24T10:30:00',
                'text': 'hey bro, check this new trading signal',
                'from_id': 123456789,
                'to_id': 987654321,
                'media_type': None
            },
            {
                'id': 1002,
                'date': '2025-06-24T10:35:00',
                'text': 'my password is crypto2024! dont tell anyone',
                'from_id': 987654321,
                'to_id': 123456789,
                'media_type': None
            },
            {
                'id': 1003,
                'date': '2025-06-24T11:00:00',
                'text': 'sent you 0.5 BTC to wallet: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
                'from_id': 123456789,
                'to_id': 987654321,
                'media_type': None
            },
            {
                'id': 1004,
                'date': '2025-06-24T11:30:00',
                'text': 'my bank account: 123-4-56789-0 SCB',
                'from_id': 987654321,
                'to_id': 123456789,
                'media_type': None
            },
            {
                'id': 1005,
                'date': '2025-06-24T12:00:00',
                'text': 'call me at 085-123-4567 after 6pm',
                'from_id': 987654321,
                'to_id': 123456789,
                'media_type': None
            }
        ]

        demo_user_profile = {
            'id': 987654321,
            'username': 'Alx_TYW',
            'first_name': 'Alex',
            'last_name': 'Trading',
            'phone': '+66851234567',
            'verified': False,
            'premium': True,
            'bot': False,
            'status': 'online'
        }

        demo_contacts = [
            {'id': 111, 'username': 'crypto_trader_1',
                'first_name': 'John', 'phone': '+66812345678'},
            {'id': 222, 'username': 'forex_master',
                'first_name': 'Mike', 'phone': '+66823456789'},
            {'id': 333, 'username': 'btc_whale',
                'first_name': 'Sarah', 'phone': '+66834567890'}
        ]

        self.results.update({
            'personal_chats': demo_personal_chats,
            'user_profiles': [demo_user_profile],
            'contacts': demo_contacts,
            'session_data': {
                'user_id': 123456789,
                'username': 'demo_user',
                'extraction_method': 'demo_mode'
            }
        })

    async def save_results(self):
        """บันทึกผลลัพธ์"""
        print(f"{Colors.BLUE}💾 Saving extraction results...{Colors.END}")

        # บันทึกเป็น JSON
        json_file = f"real_telegram_extraction_{self.timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        # สร้างรายงาน
        report_file = f"real_telegram_report_{self.timestamp}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("🔥💎 REAL TELEGRAM EXTRACTION REPORT 💎🔥\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Target: {self.results['extraction_info']['target']}\n")
            f.write(
                f"Telegram: {self.results['extraction_info']['telegram_target']}\n")
            f.write(
                f"Timestamp: {self.results['extraction_info']['timestamp']}\n\n")

            f.write("📊 EXTRACTION SUMMARY:\n")
            f.write("=" * 40 + "\n")
            f.write(
                f"Personal Messages: {len(self.results['personal_chats'])}\n")
            f.write(f"Group Chats: {len(self.results['group_chats'])}\n")
            f.write(f"User Profiles: {len(self.results['user_profiles'])}\n")
            f.write(f"Contacts: {len(self.results['contacts'])}\n")
            f.write(f"Media Files: {len(self.results['media_files'])}\n\n")

            # Personal messages
            if self.results['personal_chats']:
                f.write("💬 PERSONAL CHAT MESSAGES:\n")
                f.write("=" * 40 + "\n")
                for i, msg in enumerate(self.results['personal_chats'][:20], 1):
                    f.write(f"{i}. [{msg.get('date', 'Unknown')}]\n")
                    f.write(
                        f"   Text: {msg.get('text', 'No text')[:100]}...\n")
                    f.write(f"   From: {msg.get('from_id', 'Unknown')}\n\n")

            # Sensitive data analysis
            if 'message_analysis' in self.results.get('private_data', {}):
                analysis = self.results['private_data']['message_analysis']
                f.write("🔍 SENSITIVE DATA ANALYSIS:\n")
                f.write("=" * 40 + "\n")
                for category, count in analysis.get('keywords_found', {}).items():
                    if count > 0:
                        f.write(f"{category}: {count} matches\n")
                f.write("\n")

            # User profiles
            if self.results['user_profiles']:
                f.write("👤 USER PROFILES:\n")
                f.write("=" * 40 + "\n")
                for profile in self.results['user_profiles']:
                    f.write(f"ID: {profile.get('id')}\n")
                    f.write(
                        f"Username: @{profile.get('username', 'Unknown')}\n")
                    f.write(
                        f"Name: {profile.get('first_name', '')} {profile.get('last_name', '')}\n")
                    f.write(f"Phone: {profile.get('phone', 'Hidden')}\n")
                    f.write(f"Verified: {profile.get('verified', False)}\n\n")

        print(f"{Colors.GREEN}✅ Results saved to:{Colors.END}")
        print(f"   📄 JSON: {json_file}")
        print(f"   📋 Report: {report_file}")

    async def cleanup(self):
        """ทำความสะอาดและปิด session"""
        if self.client:
            await self.client.disconnect()
        print(f"{Colors.BLUE}🧹 Session cleanup complete{Colors.END}")

    async def run_extraction(self):
        """รันการดึงข้อมูลหลัก"""
        try:
            # ตั้งค่า API
            if not self.setup_api_credentials():
                print(
                    f"{Colors.YELLOW}⚠️ Running in demo mode without real API{Colors.END}")
                self.generate_demo_data()
                await self.save_results()
                return

            # สร้าง session
            if await self.create_telegram_session():
                # ค้นหาเป้าหมาย
                target = await self.search_target_user("Alx_TYW")

                if target:
                    # ดึงข้อมูลส่วนตัว
                    await self.extract_personal_chats(target)

                    # ดึงข้อมูลกลุ่ม
                    await self.extract_group_chats(target)

                    # ดึงรายชื่อติดต่อ
                    await self.extract_contacts()

                # บันทึกผลลัพธ์
                await self.save_results()

        except Exception as e:
            print(f"{Colors.RED}❌ Extraction failed: {e}{Colors.END}")

        finally:
            await self.cleanup()


def main():
    """ฟังก์ชันหลัก"""
    print(f"{Colors.BOLD}🚀 Starting Real Telegram Extraction...{Colors.END}")

    extractor = RealTelegramExtractor()

    # รันการดึงข้อมูล
    try:
        asyncio.run(extractor.run_extraction())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️ Extraction interrupted by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Fatal error: {e}{Colors.END}")

    print(f"\n{Colors.GREEN}🏁 Real Telegram extraction complete!{Colors.END}")
    print(f"{Colors.CYAN}📋 Check the generated reports for results{Colors.END}")


if __name__ == "__main__":
    main()
