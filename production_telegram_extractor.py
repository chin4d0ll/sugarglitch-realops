#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 PRODUCTION TELEGRAM EXTRACTOR
เครื่องมือดึงข้อมูลจริงจาก Telegram API
พร้อมการจัดการ error และ security
"""

import asyncio
import json
import time
import os
import sys
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.tl.types import User, Channel, Chat
from telethon.errors import SessionPasswordNeededError, FloodWaitError


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


class ProductionTelegramExtractor:
    def __init__(self):
        self.api_id = None
        self.api_hash = None
        self.phone = None
        self.client = None
        self.session_name = 'production_telegram_session'

    def print_step(self, message):
        print(f"{Colors.BLUE}📋 {message}{Colors.END}")

    def print_success(self, message):
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")

    def print_error(self, message):
        print(f"{Colors.RED}❌ {message}{Colors.END}")

    def print_warning(self, message):
        print(f"{Colors.YELLOW}⚠️ {message}{Colors.END}")

    def get_credentials(self):
        """รับ credentials จริงจากผู้ใช้"""
        print(f"{Colors.BOLD}🔥 PRODUCTION TELEGRAM EXTRACTOR 🔥{Colors.END}")
        print("=" * 60)
        print()

        self.print_step("Getting Telegram API credentials")
        print("📱 How to get Telegram API credentials:")
        print("1. Go to https://my.telegram.org")
        print("2. Login with your phone number")
        print("3. Go to 'API development tools'")
        print("4. Create an application")
        print("5. Copy API ID and API Hash")
        print()

        try:
            # รับ API ID
            while True:
                api_id_input = input("🔑 Enter your API ID: ").strip()
                try:
                    self.api_id = int(api_id_input)
                    break
                except ValueError:
                    self.print_error("API ID must be a number!")

            # รับ API Hash
            while True:
                self.api_hash = input("🔑 Enter your API Hash: ").strip()
                if self.api_hash:
                    break
                self.print_error("API Hash cannot be empty!")

            # รับเบอร์โทร
            while True:
                self.phone = input(
                    "📱 Enter phone number (with country code, e.g., +66812345678): ").strip()
                if self.phone.startswith('+') and len(self.phone) > 5:
                    break
                self.print_error(
                    "Phone number must start with + and country code!")

            self.print_success("Credentials configured successfully!")
            return True

        except KeyboardInterrupt:
            self.print_warning("\nSetup cancelled by user")
            return False

    async def connect_telegram(self):
        """เชื่อมต่อกับ Telegram"""
        try:
            self.print_step("Connecting to Telegram...")

            self.client = TelegramClient(
                self.session_name, self.api_id, self.api_hash)
            await self.client.connect()

            if not await self.client.is_user_authorized():
                self.print_warning(
                    "Authorization required. Starting login process...")
                return await self.login_telegram()
            else:
                self.print_success("Already authorized!")
                return True

        except Exception as e:
            self.print_error(f"Connection failed: {e}")
            return False

    async def login_telegram(self):
        """เข้าสู่ระบบ Telegram"""
        try:
            self.print_step("Sending verification code...")

            await self.client.send_code_request(self.phone)
            self.print_success(f"Verification code sent to {self.phone}")

            # รับ verification code
            while True:
                code = input("🔢 Enter verification code: ").strip()
                if code:
                    break
                self.print_error("Code cannot be empty!")

            try:
                await self.client.sign_in(self.phone, code)
                self.print_success("Login successful!")
                return True

            except SessionPasswordNeededError:
                self.print_warning("2FA is enabled on your account")

                while True:
                    password = input("🔐 Enter your 2FA password: ").strip()
                    if password:
                        break
                    self.print_error("Password cannot be empty!")

                await self.client.sign_in(password=password)
                self.print_success("2FA login successful!")
                return True

        except FloodWaitError as e:
            self.print_error(f"Rate limited! Wait {e.seconds} seconds")
            return False
        except Exception as e:
            self.print_error(f"Login failed: {e}")
            return False

    async def get_user_info(self, username):
        """ดึงข้อมูลผู้ใช้"""
        try:
            self.print_step(f"Getting user info for: @{username}")

            # ลบ @ ถ้ามี
            if username.startswith('@'):
                username = username[1:]

            user = await self.client.get_entity(username)

            user_data = {
                'id': user.id,
                'username': user.username,
                'first_name': getattr(user, 'first_name', ''),
                'last_name': getattr(user, 'last_name', ''),
                'phone': getattr(user, 'phone', 'Hidden'),
                'is_bot': getattr(user, 'bot', False),
                'is_verified': getattr(user, 'verified', False),
                'is_premium': getattr(user, 'premium', False),
                'status': str(getattr(user, 'status', 'unknown')),
                'bio': '',
                'extraction_time': datetime.now().isoformat()
            }

            # ดึง bio/about
            try:
                full_user = await self.client.get_entity(user.id)
                if hasattr(full_user, 'about'):
                    user_data['bio'] = full_user.about
            except:
                pass

            self.print_success(
                f"User found: {user_data['first_name']} {user_data['last_name']} (@{user_data['username']})")
            return user_data

        except Exception as e:
            self.print_error(f"Failed to get user info: {e}")
            return None

    async def get_chat_messages(self, username, limit=50):
        """ดึงข้อความจากแชท"""
        try:
            self.print_step(
                f"Getting chat messages with @{username} (limit: {limit})")

            if username.startswith('@'):
                username = username[1:]

            user = await self.client.get_entity(username)
            messages = []

            async for message in self.client.iter_messages(user, limit=limit):
                if message.text:
                    msg_data = {
                        'id': message.id,
                        'date': message.date.isoformat(),
                        'text': message.text,
                        'from_id': message.from_id.user_id if message.from_id else None,
                        'is_outgoing': message.out,
                        'reply_to': message.reply_to_msg_id if message.reply_to else None,
                        'views': getattr(message, 'views', 0)
                    }
                    messages.append(msg_data)

            self.print_success(f"Retrieved {len(messages)} messages")
            return messages

        except Exception as e:
            self.print_error(f"Failed to get messages: {e}")
            return []

    async def get_user_dialogs(self):
        """ดึงรายการ dialogs/chats"""
        try:
            self.print_step("Getting user dialogs...")

            dialogs = await self.client.get_dialogs()
            dialog_data = []

            for dialog in dialogs:
                if hasattr(dialog.entity, 'username') and dialog.entity.username:
                    data = {
                        'id': dialog.entity.id,
                        'title': getattr(dialog.entity, 'title', ''),
                        'username': dialog.entity.username,
                        'type': type(dialog.entity).__name__,
                        'unread_count': dialog.unread_count,
                        'is_pinned': dialog.pinned
                    }

                    if isinstance(dialog.entity, Channel):
                        data['participants_count'] = getattr(
                            dialog.entity, 'participants_count', 0)
                        data['is_megagroup'] = getattr(
                            dialog.entity, 'megagroup', False)
                        data['is_broadcast'] = getattr(
                            dialog.entity, 'broadcast', False)

                    dialog_data.append(data)

            self.print_success(f"Found {len(dialog_data)} dialogs")
            return dialog_data

        except Exception as e:
            self.print_error(f"Failed to get dialogs: {e}")
            return []

    async def extract_complete_data(self, target_username):
        """ดึงข้อมูลครบถ้วน"""
        self.print_step(
            f"Starting complete data extraction for: @{target_username}")

        # เชื่อมต่อ
        if not await self.connect_telegram():
            self.print_error("Failed to connect to Telegram")
            return None

        result = {
            'target': target_username,
            'extraction_time': datetime.now().isoformat(),
            'method': 'Telethon Production API',
            'user_info': None,
            'chat_messages': [],
            'user_dialogs': [],
            'statistics': {}
        }

        try:
            # ดึงข้อมูลผู้ใช้
            user_info = await self.get_user_info(target_username)
            if user_info:
                result['user_info'] = user_info

                # ดึงข้อความแชท
                messages = await self.get_chat_messages(target_username, limit=100)
                result['chat_messages'] = messages

                # ดึง dialogs
                dialogs = await self.get_user_dialogs()
                result['user_dialogs'] = dialogs

                # สถิติ
                result['statistics'] = {
                    'total_messages': len(messages),
                    'total_dialogs': len(dialogs),
                    'user_found': True,
                    'data_points': len(messages) + len(dialogs) + 1
                }

            else:
                result['statistics'] = {
                    'user_found': False,
                    'total_messages': 0,
                    'total_dialogs': 0,
                    'data_points': 0
                }

        except Exception as e:
            self.print_error(f"Extraction error: {e}")
            result['error'] = str(e)

        finally:
            # ปิดการเชื่อมต่อ
            if self.client:
                await self.client.disconnect()
                self.print_step("Disconnected from Telegram")

        # บันทึกผลลัพธ์
        self.save_results(result, target_username)

        return result

    def save_results(self, data, target):
        """บันทึกผลลัพธ์"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # บันทึก JSON
        json_filename = f"production_telegram_data_{target}_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # สร้างรายงาน
        self.generate_report(data, target, timestamp)

        self.print_success(f"Data saved to: {json_filename}")

    def generate_report(self, data, target, timestamp):
        """สร้างรายงานแบบอ่านง่าย"""
        report = f"""
🔥💎 PRODUCTION TELEGRAM EXTRACTION REPORT 💎🔥
======================================================================

🎯 Target: @{target}
⏰ Extraction Time: {timestamp}
🔬 Method: Telethon Production API (Real Data)
📊 Status: {'SUCCESS' if data['statistics'].get('user_found') else 'FAILED'}

📈 EXTRACTION STATISTICS:
==================================================
User Found: {'✅ Yes' if data['statistics'].get('user_found') else '❌ No'}
Messages Retrieved: {data['statistics'].get('total_messages', 0)}
Dialogs Found: {data['statistics'].get('total_dialogs', 0)}
Total Data Points: {data['statistics'].get('data_points', 0)}

"""

        if data['user_info']:
            user = data['user_info']
            report += f"""
👤 USER PROFILE (REAL DATA):
==================================================
Name: {user['first_name']} {user['last_name']}
Username: @{user['username']}
User ID: {user['id']}
Phone: {user['phone']}
Bio: {user['bio'][:100]}{'...' if len(user['bio']) > 100 else ''}
Verified: {'✅' if user['is_verified'] else '❌'}
Premium: {'✅' if user['is_premium'] else '❌'}
Bot: {'✅' if user['is_bot'] else '❌'}
Status: {user['status']}

"""

        if data['chat_messages']:
            report += f"""
💬 CHAT MESSAGES (REAL DATA):
==================================================
Total Messages: {len(data['chat_messages'])}

Recent Messages:
"""
            for i, msg in enumerate(data['chat_messages'][:10], 1):
                direction = "→ Outgoing" if msg['is_outgoing'] else "← Incoming"
                report += f"""
{i}. [{msg['date'][:19]}] {direction}
   📝 {msg['text'][:100]}{'...' if len(msg['text']) > 100 else ''}
   Views: {msg.get('views', 0)}

"""

        if data['user_dialogs']:
            report += f"""
📱 USER DIALOGS (REAL DATA):
==================================================
Total Dialogs: {len(data['user_dialogs'])}

Active Chats:
"""
            for i, dialog in enumerate(data['user_dialogs'][:10], 1):
                report += f"""
{i}. {dialog['title']}
   Username: @{dialog['username']}
   Type: {dialog['type']}
   Unread: {dialog['unread_count']}
   Pinned: {'✅' if dialog['is_pinned'] else '❌'}

"""

        report += f"""
🚨 SECURITY & LEGAL NOTICE:
==================================================
⚠️  This data was extracted using legitimate Telegram API
⚠️  All data is real and private - handle with extreme care
⚠️  Ensure compliance with local privacy laws
⚠️  Use only for authorized security testing
⚠️  Delete sensitive data after analysis

================================================================================
🔥 Production extraction by Advanced Telegram Framework
📡 Powered by Telethon API - Real Data Extraction
🕐 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
================================================================================
"""

        report_filename = f"production_telegram_report_{target}_{timestamp}.txt"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)

        self.print_success(f"Report saved to: {report_filename}")


async def main():
    """Main execution function"""
    extractor = ProductionTelegramExtractor()

    # รับ credentials
    if not extractor.get_credentials():
        sys.exit(1)

    print()
    print("🎯 Available targets from project:")
    print("1. Alx_TYW (main target - alx.trading)")
    print("2. ALX_TYW (variant)")
    print("3. alx_tyw (lowercase variant)")
    print("4. alxtrading (no underscore)")
    print("5. Custom target")
    print()

    choice = input(
        "Select target (1-5) or press Enter for default (Alx_TYW): ").strip()

    if choice == "1" or choice == "":
        target = "Alx_TYW"
    elif choice == "2":
        target = "ALX_TYW"
    elif choice == "3":
        target = "alx_tyw"
    elif choice == "4":
        target = "alxtrading"
    elif choice == "5":
        target = input("🎯 Enter custom target username (without @): ").strip()
        if not target:
            extractor.print_error("Target username required!")
            sys.exit(1)
    else:
        extractor.print_error("Invalid choice! Using default target.")
        target = "Alx_TYW"

    print(f"\n🔄 Starting extraction for: @{target}")
    print("⚠️  This will connect to real Telegram API")
    print("⚠️  Make sure you have permission to extract this data")
    print()

    confirm = input("Continue? (y/N): ").strip().lower()
    if confirm != 'y':
        extractor.print_warning("Extraction cancelled")
        sys.exit(0)

    try:
        result = await extractor.extract_complete_data(target)

        if result and result['statistics'].get('user_found'):
            print(
                f"\n{Colors.GREEN}🎉 EXTRACTION COMPLETED SUCCESSFULLY!{Colors.END}")
            print(f"📊 Data Points: {result['statistics']['data_points']}")
            print(f"💬 Messages: {result['statistics']['total_messages']}")
            print(f"📱 Dialogs: {result['statistics']['total_dialogs']}")
        else:
            print(
                f"\n{Colors.YELLOW}⚠️ EXTRACTION COMPLETED WITH ISSUES{Colors.END}")
            print("Target may not exist or be accessible")

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️ Extraction interrupted by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}💥 Extraction failed: {e}{Colors.END}")


if __name__ == "__main__":
    asyncio.run(main())
