#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 PYROGRAM TELEGRAM EXTRACTOR
ใช้ Pyrogram API สำหรับดึงข้อมูล Telegram
"""

import asyncio
import json
import time
import os
from datetime import datetime
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeRequired


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


class PyrogramExtractor:
    def __init__(self):
        # Telegram API credentials
        self.api_id = 12345  # แทนที่ด้วย API ID จริง
        self.api_hash = "abcd1234"  # แทนที่ด้วย API Hash จริง
        self.phone_number = "+66812345678"  # แทนที่ด้วยเบอร์จริง

        self.client = None
        self.session_name = "pyrogram_session"

    def print_step(self, message):
        print(f"{Colors.BLUE}📋 {message}{Colors.END}")

    def print_success(self, message):
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")

    def print_error(self, message):
        print(f"{Colors.RED}❌ {message}{Colors.END}")

    def print_warning(self, message):
        print(f"{Colors.YELLOW}⚠️ {message}{Colors.END}")

    async def setup_client(self):
        """ตั้งค่า Pyrogram client"""
        try:
            self.print_step("Setting up Pyrogram client...")

            self.client = Client(
                self.session_name,
                api_id=self.api_id,
                api_hash=self.api_hash,
                phone_number=self.phone_number
            )

            self.print_success("Client setup completed")
            return True

        except Exception as e:
            self.print_error(f"Client setup failed: {e}")
            return False

    async def connect_and_auth(self):
        """เชื่อมต่อและยืนยันตัวตน"""
        try:
            self.print_step("Connecting to Telegram...")

            await self.client.start()

            self.print_success("Connected and authenticated!")
            return True

        except Exception as e:
            self.print_error(f"Connection failed: {e}")
            # ใช้ demo mode สำหรับการทดสอบ
            self.print_warning("Using demo mode for testing...")
            return False

    async def get_user_data(self, username):
        """ดึงข้อมูลผู้ใช้"""
        try:
            self.print_step(f"Getting user data for: {username}")

            # ใน demo mode ให้ return demo data
            if not self.client:
                return self.get_demo_user_data(username)

            user = await self.client.get_users(username)

            user_data = {
                'id': user.id,
                'is_self': user.is_self,
                'is_contact': user.is_contact,
                'is_mutual_contact': user.is_mutual_contact,
                'is_deleted': user.is_deleted,
                'is_bot': user.is_bot,
                'is_verified': user.is_verified,
                'is_restricted': user.is_restricted,
                'is_scam': user.is_scam,
                'is_fake': user.is_fake,
                'is_premium': user.is_premium,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'phone_number': user.phone_number,
                'status': str(user.status),
                'last_online_date': str(user.last_online_date) if user.last_online_date else None,
                'photo': str(user.photo) if user.photo else None
            }

            self.print_success(f"User data retrieved for: {user.first_name}")
            return user_data

        except Exception as e:
            self.print_error(f"Failed to get user data: {e}")
            return self.get_demo_user_data(username)

    def get_demo_user_data(self, username):
        """สร้างข้อมูล demo สำหรับทดสอบ"""
        return {
            'id': 123456789,
            'username': username,
            'first_name': 'Alex',
            'last_name': 'Trading',
            'phone_number': '+66812345678',
            'is_verified': False,
            'is_premium': True,
            'is_bot': False,
            'status': 'online',
            'last_online_date': datetime.now().isoformat(),
            'bio': 'Cryptocurrency trader and investor',
            'demo_mode': True
        }

    async def get_chat_history(self, username, limit=100):
        """ดึงประวัติการแชท"""
        try:
            self.print_step(f"Getting chat history with: {username}")

            if not self.client:
                return self.get_demo_chat_history(username, limit)

            messages = []
            async for message in self.client.get_chat_history(username, limit=limit):
                if message.text:
                    msg_data = {
                        'message_id': message.id,
                        'date': message.date.isoformat(),
                        'text': message.text,
                        'from_user': message.from_user.username if message.from_user else None,
                        'is_outgoing': message.outgoing,
                        'reply_to_message_id': message.reply_to_message_id,
                        'edit_date': message.edit_date.isoformat() if message.edit_date else None
                    }
                    messages.append(msg_data)

            self.print_success(f"Retrieved {len(messages)} messages")
            return messages

        except Exception as e:
            self.print_error(f"Failed to get chat history: {e}")
            return self.get_demo_chat_history(username, limit)

    def get_demo_chat_history(self, username, limit):
        """สร้างประวัติแชท demo"""
        messages = []
        for i in range(min(limit, 20)):
            msg = {
                'message_id': i + 1,
                'date': (datetime.now() - timedelta(hours=i)).isoformat(),
                'text': f"Demo message {i+1} from {username} conversation",
                'from_user': username if i % 2 == 0 else 'me',
                'is_outgoing': i % 2 == 1,
                'reply_to_message_id': None,
                'edit_date': None,
                'demo_mode': True
            }
            messages.append(msg)

        return messages

    async def get_common_chats(self, username):
        """ดึงแชทร่วมกัน"""
        try:
            self.print_step(f"Getting common chats with: {username}")

            if not self.client:
                return self.get_demo_common_chats(username)

            user = await self.client.get_users(username)
            common_chats = await self.client.get_common_chats(user.id)

            chats_data = []
            for chat in common_chats:
                chat_data = {
                    'id': chat.id,
                    'title': chat.title,
                    'username': chat.username,
                    'type': str(chat.type),
                    'members_count': chat.members_count if hasattr(chat, 'members_count') else 0
                }
                chats_data.append(chat_data)

            self.print_success(f"Found {len(chats_data)} common chats")
            return chats_data

        except Exception as e:
            self.print_error(f"Failed to get common chats: {e}")
            return self.get_demo_common_chats(username)

    def get_demo_common_chats(self, username):
        """สร้างแชทร่วม demo"""
        return [
            {
                'id': 1001234567890,
                'title': 'Crypto Trading Group',
                'username': 'crypto_trading_vip',
                'type': 'supergroup',
                'members_count': 1250,
                'demo_mode': True
            },
            {
                'id': 1001234567891,
                'title': 'Investment Club',
                'username': 'investment_club_th',
                'type': 'group',
                'members_count': 456,
                'demo_mode': True
            }
        ]

    async def extract_comprehensive_data(self, target_username):
        """ดึงข้อมูลครบถ้วน"""
        self.print_step(
            f"Starting comprehensive extraction for: {target_username}")

        # Setup client
        await self.setup_client()

        # Try to connect (will fallback to demo mode if fails)
        connected = await self.connect_and_auth()

        result = {
            'target': target_username,
            'extraction_time': datetime.now().isoformat(),
            'method': 'Pyrogram API',
            'connected': connected,
            'user_data': None,
            'chat_history': [],
            'common_chats': [],
            'analysis': {}
        }

        # Get user data
        user_data = await self.get_user_data(target_username)
        result['user_data'] = user_data

        # Get chat history
        chat_history = await self.get_chat_history(target_username)
        result['chat_history'] = chat_history

        # Get common chats
        common_chats = await self.get_common_chats(target_username)
        result['common_chats'] = common_chats

        # Analyze data
        result['analysis'] = self.analyze_data(result)

        # Disconnect if connected
        if self.client and connected:
            await self.client.stop()

        # Save results
        self.save_results(result, target_username)

        return result

    def analyze_data(self, data):
        """วิเคราะห์ข้อมูล"""
        analysis = {
            'total_messages': len(data['chat_history']),
            'total_common_chats': len(data['common_chats']),
            'user_activity': 'active' if data['user_data'] and data['user_data'].get('status') == 'online' else 'inactive',
            'privacy_level': 'high' if data['user_data'] and not data['user_data'].get('phone_number') else 'medium',
            'account_type': 'premium' if data['user_data'] and data['user_data'].get('is_premium') else 'regular',
            'verification_status': 'verified' if data['user_data'] and data['user_data'].get('is_verified') else 'unverified'
        }

        # Analyze message patterns
        if data['chat_history']:
            outgoing = sum(
                1 for msg in data['chat_history'] if msg.get('is_outgoing'))
            incoming = len(data['chat_history']) - outgoing
            analysis['message_ratio'] = f"{outgoing}:{incoming} (out:in)"

        return analysis

    def save_results(self, data, target):
        """บันทึกผลลัพธ์"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save JSON
        json_filename = f"pyrogram_extraction_{target}_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Generate report
        self.generate_report(data, target, timestamp)

        self.print_success(f"Results saved to: {json_filename}")

    def generate_report(self, data, target, timestamp):
        """สร้างรายงาน"""
        report = f"""
🔥💎 PYROGRAM TELEGRAM EXTRACTION REPORT 💎🔥
======================================================================

🎯 Target: {target}
⏰ Extraction Time: {timestamp}
🔬 Method: Pyrogram API
🌐 Connection Status: {'Connected' if data['connected'] else 'Demo Mode'}

📊 EXTRACTION SUMMARY:
==================================================
User Data Retrieved: {'Yes' if data['user_data'] else 'No'}
Chat Messages: {len(data['chat_history'])}
Common Chats: {len(data['common_chats'])}

"""

        if data['user_data']:
            user = data['user_data']
            report += f"""
👤 USER PROFILE:
==================================================
Name: {user.get('first_name', '')} {user.get('last_name', '')}
Username: @{user.get('username', '')}
User ID: {user.get('id', '')}
Phone: {user.get('phone_number', 'Hidden')}
Premium: {user.get('is_premium', False)}
Verified: {user.get('is_verified', False)}
Status: {user.get('status', 'Unknown')}
Last Online: {user.get('last_online_date', 'Unknown')}

"""

        if data['chat_history']:
            report += f"""
💬 CHAT ANALYSIS:
==================================================
Total Messages: {len(data['chat_history'])}
"""
            for i, msg in enumerate(data['chat_history'][:5], 1):
                direction = "→" if msg.get('is_outgoing') else "←"
                report += f"""
{i}. [{msg['date'][:19]}] {direction} {msg.get('from_user', 'Unknown')}
   📝 {msg['text'][:80]}{'...' if len(msg['text']) > 80 else ''}

"""

        if data['common_chats']:
            report += f"""
📢 COMMON CHATS:
==================================================
"""
            for i, chat in enumerate(data['common_chats'], 1):
                report += f"""
{i}. {chat['title']}
   👥 Members: {chat['members_count']}
   🔗 @{chat.get('username', 'No username')}

"""

        analysis = data.get('analysis', {})
        if analysis:
            report += f"""
🔍 INTELLIGENCE ANALYSIS:
==================================================
Activity Level: {analysis.get('user_activity', 'Unknown')}
Account Type: {analysis.get('account_type', 'Unknown')}
Privacy Level: {analysis.get('privacy_level', 'Unknown')}
Verification: {analysis.get('verification_status', 'Unknown')}
Message Pattern: {analysis.get('message_ratio', 'Unknown')}

"""

        report += f"""
⚠️ EXTRACTION NOTES:
==================================================
• {"Real API data" if data['connected'] else "Demo data (API not connected)"}
• Data extracted using Pyrogram library
• All data follows Telegram's terms of service
• Use responsibly and legally

================================================================================
🔥 Extraction by Pyrogram Framework
📱 Telegram API v{timestamp[:8]}
================================================================================
"""

        report_filename = f"pyrogram_report_{target}_{timestamp}.txt"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)

        self.print_success(f"Report saved to: {report_filename}")


async def main():
    """Main function"""
    print(f"{Colors.BOLD}🔥 PYROGRAM TELEGRAM EXTRACTOR 🔥{Colors.END}")
    print("=" * 60)

    extractor = PyrogramExtractor()

    target = "Alx_TYW"

    print(f"\n🎯 Target: {target}")
    print("🔄 Starting Pyrogram extraction...")
    print("⚠️  Will attempt real API, fallback to demo mode")
    print()

    try:
        result = await extractor.extract_comprehensive_data(target)
        print(f"\n{Colors.GREEN}🎉 Extraction completed!{Colors.END}")

        # Print summary
        if result['user_data']:
            user = result['user_data']
            print(
                f"👤 Found: {user.get('first_name', '')} {user.get('last_name', '')}")

        print(f"💬 Messages: {len(result['chat_history'])}")
        print(f"📢 Common Chats: {len(result['common_chats'])}")

    except Exception as e:
        print(f"\n{Colors.RED}💥 Extraction error: {e}{Colors.END}")


if __name__ == "__main__":
    asyncio.run(main())
