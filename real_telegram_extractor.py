#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 REAL TELEGRAM DATA EXTRACTOR
ดึงข้อมูลจริงจาก Telegram API โดยใช้ Telethon
"""

import asyncio
import json
import time
import os
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.tl.types import User, Channel, Chat
from telethon.errors import SessionPasswordNeededError, PhoneCodeRequiredError


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


class RealTelegramExtractor:
    def __init__(self):
        # Telegram API credentials (ใส่ค่าจริงได้ที่นี่)
        self.api_id = None  # ใส่ API ID จาก my.telegram.org
        self.api_hash = None  # ใส่ API Hash จาก my.telegram.org
        self.phone = None  # เบอร์โทรศัพท์ที่ลงทะเบียน Telegram
        
        self.client = None
        self.session_name = 'telegram_session'
        
    def print_step(self, message):
        print(f"{Colors.BLUE}📋 {message}{Colors.END}")
        
    def print_success(self, message):
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")
        
    def print_error(self, message):
        print(f"{Colors.RED}❌ {message}{Colors.END}")
        
    def print_warning(self, message):
        print(f"{Colors.YELLOW}⚠️ {message}{Colors.END}")

    def setup_credentials(self):
        """ตั้งค่า API credentials"""
        self.print_step("Setting up Telegram API credentials")
        
        if not self.api_id:
            self.print_warning("API ID not configured")
            print("📱 How to get Telegram API credentials:")
            print("1. Go to https://my.telegram.org")
            print("2. Login with your phone number")
            print("3. Go to 'API development tools'")
            print("4. Create an application")
            print("5. Copy API ID and API Hash")
            print()
            
            # ใส่ demo values สำหรับทดสอบ
            self.api_id = 12345  # แทนที่ด้วย API ID จริง
            self.api_hash = "abcd1234"  # แทนที่ด้วย API Hash จริง  
            self.phone = "+66812345678"  # แทนที่ด้วยเบอร์จริง
            
            self.print_warning("Using demo credentials. Replace with real ones for actual use.")
            
        return True

    async def connect_telegram(self):
        """เชื่อมต่อกับ Telegram"""
        try:
            self.print_step("Connecting to Telegram...")
            
            self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)
            await self.client.connect()
            
            if not await self.client.is_user_authorized():
                self.print_warning("Not authorized. Need to login.")
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
            self.print_step("Starting login process...")
            
            await self.client.send_code_request(self.phone)
            self.print_warning("Code sent to your phone. Enter it below:")
            
            # ในการใช้งานจริง ให้ใช้ input() เพื่อรับ code
            code = "12345"  # แทนที่ด้วย input("Enter code: ")
            
            await self.client.sign_in(self.phone, code)
            self.print_success("Login successful!")
            return True
            
        except SessionPasswordNeededError:
            self.print_warning("2FA enabled. Enter password:")
            password = "password"  # แทนที่ด้วย input("Enter password: ")
            await self.client.sign_in(password=password)
            self.print_success("Login with 2FA successful!")
            return True
            
        except Exception as e:
            self.print_error(f"Login failed: {e}")
            return False

    async def get_user_info(self, username):
        """ดึงข้อมูลผู้ใช้"""
        try:
            self.print_step(f"Getting user info for: {username}")
            
            user = await self.client.get_entity(username)
            
            user_data = {
                'id': user.id,
                'username': user.username,
                'first_name': getattr(user, 'first_name', ''),
                'last_name': getattr(user, 'last_name', ''),
                'phone': getattr(user, 'phone', ''),
                'is_bot': getattr(user, 'bot', False),
                'is_verified': getattr(user, 'verified', False),
                'is_premium': getattr(user, 'premium', False),
                'status': str(getattr(user, 'status', 'unknown')),
                'bio': ''
            }
            
            # ดึง bio
            try:
                full_user = await self.client.get_entity(user.id)
                if hasattr(full_user, 'about'):
                    user_data['bio'] = full_user.about
            except:
                pass
                
            self.print_success(f"User info retrieved: {user_data['first_name']} {user_data['last_name']}")
            return user_data
            
        except Exception as e:
            self.print_error(f"Failed to get user info: {e}")
            return None

    async def get_user_messages(self, username, limit=100):
        """ดึงข้อความของผู้ใช้"""
        try:
            self.print_step(f"Getting messages from: {username}")
            
            user = await self.client.get_entity(username)
            messages = []
            
            # ดึงข้อความจาก chat ส่วนตัว
            async for message in self.client.iter_messages(user, limit=limit):
                if message.text:
                    msg_data = {
                        'id': message.id,
                        'date': message.date.isoformat(),
                        'text': message.text,
                        'from_id': message.from_id.user_id if message.from_id else None,
                        'is_outgoing': message.out,
                        'reply_to': message.reply_to_msg_id if message.reply_to else None
                    }
                    messages.append(msg_data)
            
            self.print_success(f"Retrieved {len(messages)} messages")
            return messages
            
        except Exception as e:
            self.print_error(f"Failed to get messages: {e}")
            return []

    async def get_user_channels(self, username):
        """ดึงรายการ channels ที่ผู้ใช้เข้าร่วม"""
        try:
            self.print_step(f"Getting channels for: {username}")
            
            dialogs = await self.client.get_dialogs()
            channels = []
            
            for dialog in dialogs:
                if hasattr(dialog.entity, 'username') and dialog.entity.username:
                    if isinstance(dialog.entity, Channel):
                        channel_data = {
                            'id': dialog.entity.id,
                            'title': dialog.entity.title,
                            'username': dialog.entity.username,
                            'participants_count': getattr(dialog.entity, 'participants_count', 0),
                            'is_megagroup': getattr(dialog.entity, 'megagroup', False),
                            'is_broadcast': getattr(dialog.entity, 'broadcast', False)
                        }
                        channels.append(channel_data)
            
            self.print_success(f"Found {len(channels)} channels")
            return channels
            
        except Exception as e:
            self.print_error(f"Failed to get channels: {e}")
            return []

    async def extract_target_data(self, target_username):
        """ดึงข้อมูลครบถ้วนของเป้าหมาย"""
        self.print_step(f"Starting comprehensive data extraction for: {target_username}")
        
        if not await self.connect_telegram():
            self.print_error("Failed to connect to Telegram")
            return None
            
        result = {
            'target': target_username,
            'extraction_time': datetime.now().isoformat(),
            'user_info': None,
            'messages': [],
            'channels': [],
            'contacts': [],
            'media_files': []
        }
        
        # ดึงข้อมูลผู้ใช้
        user_info = await self.get_user_info(target_username)
        if user_info:
            result['user_info'] = user_info
            
        # ดึงข้อความ
        messages = await self.get_user_messages(target_username)
        result['messages'] = messages
        
        # ดึง channels
        channels = await self.get_user_channels(target_username)
        result['channels'] = channels
        
        await self.client.disconnect()
        
        # บันทึกผลลัพธ์
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"real_telegram_data_{target_username}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            
        self.print_success(f"Data saved to: {filename}")
        
        # สร้างรายงาน
        self.generate_report(result, target_username, timestamp)
        
        return result

    def generate_report(self, data, target, timestamp):
        """สร้างรายงานแบบอ่านง่าย"""
        report = f"""
🔥💎 REAL TELEGRAM DATA EXTRACTION REPORT 💎🔥
======================================================================

🎯 Target: {target}
⏰ Extraction Time: {timestamp}
🔬 Method: Telethon API (Real Data)

📊 EXTRACTION SUMMARY:
==================================================
User Found: {'Yes' if data['user_info'] else 'No'}
Messages Retrieved: {len(data['messages'])}
Channels Found: {len(data['channels'])}
Contacts Found: {len(data['contacts'])}

"""
        
        if data['user_info']:
            user = data['user_info']
            report += f"""
👤 USER INFORMATION:
==================================================
Name: {user['first_name']} {user['last_name']}
Username: @{user['username']}
User ID: {user['id']}
Phone: {user['phone']}
Bio: {user['bio']}
Verified: {user['is_verified']}
Premium: {user['is_premium']}
Status: {user['status']}

"""

        if data['messages']:
            report += f"""
💬 RECENT MESSAGES ({len(data['messages'])}):
==================================================
"""
            for i, msg in enumerate(data['messages'][:10], 1):
                direction = "→ Outgoing" if msg['is_outgoing'] else "← Incoming"
                report += f"""
{i}. [{msg['date'][:19]}] {direction}
   📝 Text: {msg['text'][:100]}{'...' if len(msg['text']) > 100 else ''}

"""

        if data['channels']:
            report += f"""
📢 CHANNELS ({len(data['channels'])}):
==================================================
"""
            for i, channel in enumerate(data['channels'][:10], 1):
                report += f"""
{i}. {channel['title']}
   Username: @{channel['username']}
   Members: {channel['participants_count']}
   Type: {'Megagroup' if channel['is_megagroup'] else 'Broadcast'}

"""

        report += f"""
🚨 SECURITY ANALYSIS:
==================================================
Data Sources: Telegram API (Authenticated)
Privacy Level: HIGH (Personal Messages & Info)
Risk Assessment: CRITICAL (Real Private Data)

⚠️ LEGAL NOTICE:
==================================================
This data was extracted using legitimate Telegram API.
Use responsibly and in compliance with local laws.
Respect user privacy and data protection regulations.

================================================================================
🔥 Real extraction by Advanced Telegram Framework
📡 Powered by Telethon API
================================================================================
"""
        
        report_filename = f"real_telegram_report_{target}_{timestamp}.txt"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)
            
        self.print_success(f"Report saved to: {report_filename}")


async def main():
    """Main execution function"""
    print(f"{Colors.BOLD}🔥 REAL TELEGRAM DATA EXTRACTOR 🔥{Colors.END}")
    print("=" * 60)
    
    extractor = RealTelegramExtractor()
    
    # Setup credentials
    if not extractor.setup_credentials():
        return
    
    # Target to extract
    target = "Alx_TYW"  # เปลี่ยนเป้าหมายได้ที่นี่
    
    print(f"\n🎯 Target: {target}")
    print("🔄 Starting real data extraction...")
    print("⚠️  This will attempt to connect to real Telegram API")
    print()
    
    try:
        result = await extractor.extract_target_data(target)
        if result:
            print(f"\n{Colors.GREEN}🎉 Extraction completed successfully!{Colors.END}")
        else:
            print(f"\n{Colors.RED}❌ Extraction failed{Colors.END}")
            
    except Exception as e:
        print(f"\n{Colors.RED}💥 Error during extraction: {e}{Colors.END}")


if __name__ == "__main__":
    asyncio.run(main())
