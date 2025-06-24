#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 INTERACTIVE TELEGRAM REAL DATA EXTRACTOR
สำหรับดึงข้อมูลจริงจาก Telegram API
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeRequiredError


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


class InteractiveTelegramExtractor:
    def __init__(self):
        self.api_id = None
        self.api_hash = None
        self.phone = None
        self.client = None
        self.session_name = 'telegram_real_session'
        
    def print_header(self):
        """แสดงหัวข้อ"""
        print(f"{Colors.BOLD}🔥 TELEGRAM REAL DATA EXTRACTOR 🔥{Colors.END}")
        print("=" * 60)
        print("🎯 Extract real data from Telegram API")
        print("⚠️  Requires valid Telegram API credentials")
        print("=" * 60)
        print()
        
    def print_step(self, message):
        print(f"{Colors.BLUE}📋 {message}{Colors.END}")
        
    def print_success(self, message):
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")
        
    def print_error(self, message):
        print(f"{Colors.RED}❌ {message}{Colors.END}")
        
    def print_warning(self, message):
        print(f"{Colors.YELLOW}⚠️ {message}{Colors.END}")

    def get_credentials_interactive(self):
        """รับข้อมูล API แบบ interactive"""
        self.print_step("Getting Telegram API credentials...")
        
        print(f"\n{Colors.YELLOW}📱 How to get Telegram API credentials:{Colors.END}")
        print("1. Go to https://my.telegram.org")
        print("2. Login with your phone number")
        print("3. Go to 'API development tools'")
        print("4. Create an application (any name)")
        print("5. Copy API ID and API Hash")
        print("6. Keep these credentials safe!")
        print()
        
        try:
            # Get API ID
            while not self.api_id:
                api_id_str = input(f"{Colors.BLUE}Enter your API ID: {Colors.END}").strip()
                if api_id_str.isdigit() and len(api_id_str) >= 6:
                    self.api_id = int(api_id_str)
                    break
                else:
                    self.print_error("Invalid API ID. Must be a number with at least 6 digits.")
            
            # Get API Hash
            while not self.api_hash:
                api_hash = input(f"{Colors.BLUE}Enter your API Hash: {Colors.END}").strip()
                if len(api_hash) >= 32:
                    self.api_hash = api_hash
                    break
                else:
                    self.print_error("Invalid API Hash. Must be at least 32 characters.")
            
            # Get phone number
            while not self.phone:
                phone = input(f"{Colors.BLUE}Enter your phone number (with country code, e.g., +66812345678): {Colors.END}").strip()
                if phone.startswith('+') and len(phone) >= 10:
                    self.phone = phone
                    break
                else:
                    self.print_error("Invalid phone number. Must start with + and country code.")
            
            self.print_success("✅ Credentials configured successfully!")
            return True
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Setup cancelled by user{Colors.END}")
            return False
        except Exception as e:
            self.print_error(f"Error: {e}")
            return False

    async def authenticate(self):
        """ยืนยันตัวตนกับ Telegram"""
        try:
            self.print_step("Connecting to Telegram...")
            
            self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)
            await self.client.connect()
            
            if not await self.client.is_user_authorized():
                self.print_warning("Not logged in. Starting authentication...")
                
                # Send code
                await self.client.send_code_request(self.phone)
                self.print_success("📱 Verification code sent to your phone!")
                
                # Get code from user
                code = input(f"{Colors.BLUE}Enter the verification code: {Colors.END}").strip()
                
                try:
                    await self.client.sign_in(self.phone, code)
                    self.print_success("🎉 Login successful!")
                    
                except SessionPasswordNeededError:
                    self.print_warning("🔐 Two-factor authentication enabled")
                    password = input(f"{Colors.BLUE}Enter your 2FA password: {Colors.END}").strip()
                    await self.client.sign_in(password=password)
                    self.print_success("🎉 Login with 2FA successful!")
                    
            else:
                self.print_success("Already authenticated!")
                
            return True
            
        except Exception as e:
            self.print_error(f"Authentication failed: {e}")
            return False

    async def get_target_info(self, username):
        """ดึงข้อมูลเป้าหมาย"""
        try:
            self.print_step(f"Getting information for: @{username}")
            
            # Get user entity
            user = await self.client.get_entity(username)
            
            # Extract user data
            user_data = {
                'id': user.id,
                'username': user.username,
                'first_name': getattr(user, 'first_name', ''),
                'last_name': getattr(user, 'last_name', ''),
                'phone': getattr(user, 'phone', ''),
                'is_bot': getattr(user, 'bot', False),
                'is_verified': getattr(user, 'verified', False),
                'is_premium': getattr(user, 'premium', False),
                'status': str(getattr(user, 'status', '')),
                'access_hash': getattr(user, 'access_hash', '')
            }
            
            self.print_success(f"✅ Found user: {user_data['first_name']} {user_data['last_name']}")
            return user_data
            
        except Exception as e:
            self.print_error(f"Failed to get user info: {e}")
            return None

    async def get_chat_messages(self, username, limit=50):
        """ดึงข้อความจากการแชท"""
        try:
            self.print_step(f"Getting chat messages with @{username} (limit: {limit})")
            
            messages = []
            user = await self.client.get_entity(username)
            
            # Get messages
            async for message in self.client.iter_messages(user, limit=limit):
                if message.text:
                    msg_data = {
                        'id': message.id,
                        'date': message.date.isoformat(),
                        'text': message.text,
                        'from_id': message.from_id.user_id if message.from_id else None,
                        'outgoing': message.out,
                        'reply_to': message.reply_to_msg_id if message.reply_to else None,
                        'views': getattr(message, 'views', 0)
                    }
                    messages.append(msg_data)
            
            self.print_success(f"✅ Retrieved {len(messages)} messages")
            return messages
            
        except Exception as e:
            self.print_error(f"Failed to get messages: {e}")
            return []

    async def get_mutual_contacts(self, username):
        """ดึงรายชื่อผู้ติดต่อร่วมกัน"""
        try:
            self.print_step(f"Getting mutual contacts with @{username}")
            
            user = await self.client.get_entity(username)
            contacts = await self.client(GetMutualContactsRequest(user.id))
            
            mutual_list = []
            for contact_id in contacts.users:
                try:
                    contact_user = await self.client.get_entity(contact_id)
                    contact_data = {
                        'id': contact_user.id,
                        'username': getattr(contact_user, 'username', ''),
                        'first_name': getattr(contact_user, 'first_name', ''),
                        'last_name': getattr(contact_user, 'last_name', '')
                    }
                    mutual_list.append(contact_data)
                except:
                    continue
            
            self.print_success(f"✅ Found {len(mutual_list)} mutual contacts")
            return mutual_list
            
        except Exception as e:
            self.print_error(f"Failed to get mutual contacts: {e}")
            return []

    async def extract_comprehensive_data(self, target_username):
        """ดึงข้อมูลครอบคลุม"""
        self.print_step(f"Starting comprehensive extraction for: @{target_username}")
        
        result = {
            'target': target_username,
            'extraction_time': datetime.now().isoformat(),
            'method': 'Telethon Real API',
            'user_info': None,
            'messages': [],
            'mutual_contacts': [],
            'extraction_success': False
        }
        
        try:
            # Get user info
            user_info = await self.get_target_info(target_username)
            if user_info:
                result['user_info'] = user_info
                result['extraction_success'] = True
            
            # Get messages
            messages = await self.get_chat_messages(target_username, limit=100)
            result['messages'] = messages
            
            # Get mutual contacts
            mutual_contacts = await self.get_mutual_contacts(target_username)
            result['mutual_contacts'] = mutual_contacts
            
            # Save data
            self.save_data(result, target_username)
            
            return result
            
        except Exception as e:
            self.print_error(f"Extraction failed: {e}")
            result['error'] = str(e)
            return result
        
        finally:
            if self.client:
                await self.client.disconnect()

    def save_data(self, data, target):
        """บันทึกข้อมูล"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON
        json_file = f"telegram_real_data_{target}_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Generate report
        self.generate_report(data, target, timestamp)
        
        self.print_success(f"✅ Data saved to: {json_file}")

    def generate_report(self, data, target, timestamp):
        """สร้างรายงาน"""
        report = f"""
🔥💎 TELEGRAM REAL DATA EXTRACTION REPORT 💎🔥
=====================================================================

🎯 Target: @{target}
⏰ Extraction Time: {timestamp}
🔬 Method: Telethon Real API
✅ Success: {data['extraction_success']}

📊 EXTRACTION SUMMARY:
=====================================================
"""
        
        if data['user_info']:
            user = data['user_info']
            report += f"""
👤 USER INFORMATION:
=====================================================
Name: {user['first_name']} {user['last_name']}
Username: @{user['username']}
User ID: {user['id']}
Phone: {user.get('phone', 'Hidden')}
Verified: {user['is_verified']}
Premium: {user['is_premium']}
Bot: {user['is_bot']}
Status: {user['status']}

"""
        
        if data['messages']:
            report += f"""
💬 CHAT MESSAGES ({len(data['messages'])}):
=====================================================
"""
            for i, msg in enumerate(data['messages'][:10], 1):
                direction = "→ OUT" if msg['outgoing'] else "← IN"
                report += f"""
{i}. [{msg['date'][:19]}] {direction}
   📝 {msg['text'][:100]}{'...' if len(msg['text']) > 100 else ''}

"""
        
        if data['mutual_contacts']:
            report += f"""
👥 MUTUAL CONTACTS ({len(data['mutual_contacts'])}):
=====================================================
"""
            for i, contact in enumerate(data['mutual_contacts'][:10], 1):
                report += f"""
{i}. {contact['first_name']} {contact['last_name']}
   👤 @{contact.get('username', 'No username')}
   🆔 {contact['id']}

"""
        
        report += f"""
🚨 SECURITY & LEGAL:
=====================================================
⚠️  This data was extracted using legitimate Telegram API
⚠️  All data is real and obtained with proper authentication
⚠️  Use responsibly and comply with local laws
⚠️  Respect privacy and data protection regulations

📡 TECHNICAL DETAILS:
=====================================================
Library: Telethon {timestamp[:8]}
Authentication: Real phone number + 2FA
Data Quality: HIGH (Real API data)
Privacy Level: CRITICAL (Personal data access)

=====================================================================
🔥 Real extraction by Interactive Telegram Framework
=====================================================================
"""
        
        report_file = f"telegram_real_report_{target}_{timestamp}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.print_success(f"✅ Report saved to: {report_file}")


async def main():
    """Main function"""
    extractor = InteractiveTelegramExtractor()
    
    try:
        # Show header
        extractor.print_header()
        
        # Get credentials
        if not extractor.get_credentials_interactive():
            return
        
        # Authenticate
        if not await extractor.authenticate():
            return
        
        # Get target
        print()
        target = input(f"{Colors.BLUE}Enter target username (without @): {Colors.END}").strip()
        
        if not target:
            extractor.print_error("No target specified")
            return
        
        # Extract data
        print(f"\n🎯 Target: @{target}")
        print("🔄 Starting real data extraction...")
        print()
        
        result = await extractor.extract_comprehensive_data(target)
        
        if result['extraction_success']:
            print(f"\n{Colors.GREEN}🎉 Extraction completed successfully!{Colors.END}")
            
            if result['user_info']:
                user = result['user_info']
                print(f"👤 User: {user['first_name']} {user['last_name']}")
                print(f"🆔 ID: {user['id']}")
                print(f"✅ Verified: {user['is_verified']}")
                print(f"💎 Premium: {user['is_premium']}")
            
            print(f"💬 Messages: {len(result['messages'])}")
            print(f"👥 Mutual Contacts: {len(result['mutual_contacts'])}")
            
        else:
            print(f"\n{Colors.RED}❌ Extraction failed{Colors.END}")
            if 'error' in result:
                print(f"Error: {result['error']}")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Operation cancelled by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}💥 Unexpected error: {e}{Colors.END}")


if __name__ == "__main__":
    asyncio.run(main())
