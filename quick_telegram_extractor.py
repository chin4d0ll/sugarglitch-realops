#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 QUICK TELEGRAM EXTRACTOR - For Project Targets
ใช้ข้อมูล target ที่มีอยู่ในโปรเจกต์แล้ว
"""

import asyncio
import json
import sys
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import Channel
from telethon.errors import SessionPasswordNeededError, FloodWaitError


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


class QuickTelegramExtractor:
    def __init__(self):
        # Project targets from existing data
        self.project_targets = {
            'alx.trading': {
                'telegram_username': 'Alx_TYW',
                'variants': ['ALX_TYW', 'alx_tyw', 'alxtrading', 'alex_trading', 'alx_crypto'],
                'description': 'Primary target - cryptocurrency trader'
            }
        }

        self.api_id = None
        self.api_hash = None
        self.phone = None
        self.client = None
        self.session_name = 'quick_telegram_session'

    def print_step(self, message):
        print(f"{Colors.BLUE}📋 {message}{Colors.END}")

    def print_success(self, message):
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")

    def print_error(self, message):
        print(f"{Colors.RED}❌ {message}{Colors.END}")

    def print_warning(self, message):
        print(f"{Colors.YELLOW}⚠️ {message}{Colors.END}")

    def show_project_targets(self):
        """แสดง targets ที่มีในโปรเจกต์"""
        print(f"{Colors.BOLD}🎯 PROJECT TARGETS FROM EXISTING DATA:{Colors.END}")
        print("=" * 60)

        for profile, data in self.project_targets.items():
            print(f"\n📱 Profile: {profile}")
            print(f"🔗 Telegram: @{data['telegram_username']}")
            print(f"📝 Description: {data['description']}")
            print(
                f"🔄 Variants: {', '.join(['@' + v for v in data['variants']])}")

        print()

    def get_quick_credentials(self):
        """รับ credentials แบบเร็ว"""
        print(f"{Colors.BOLD}🚀 QUICK TELEGRAM EXTRACTOR 🚀{Colors.END}")
        print("=" * 50)
        print("⚡ For quick setup with project targets")
        print()

        try:
            self.api_id = int(input("🔑 API ID: "))
            self.api_hash = input("🔑 API Hash: ").strip()
            self.phone = input("📱 Phone (+66xxx): ").strip()

            if not all([self.api_id, self.api_hash, self.phone]):
                self.print_error("All credentials required!")
                return False

            return True

        except (ValueError, KeyboardInterrupt):
            self.print_error("Setup failed!")
            return False

    def select_target(self):
        """เลือก target จากโปรเจกต์"""
        self.show_project_targets()

        print("🎯 Quick target selection:")
        print("1. Alx_TYW (main)")
        print("2. ALX_TYW")
        print("3. alx_tyw")
        print("4. alxtrading")
        print("5. alex_trading")
        print("6. alx_crypto")
        print("7. All variants")
        print()

        choice = input("Select (1-7) or Enter for main target: ").strip()

        if choice == "1" or choice == "":
            return ["Alx_TYW"]
        elif choice == "2":
            return ["ALX_TYW"]
        elif choice == "3":
            return ["alx_tyw"]
        elif choice == "4":
            return ["alxtrading"]
        elif choice == "5":
            return ["alex_trading"]
        elif choice == "6":
            return ["alx_crypto"]
        elif choice == "7":
            return list(self.project_targets['alx.trading']['variants'])
        else:
            return ["Alx_TYW"]

    async def quick_connect(self):
        """เชื่อมต่อแบบเร็ว"""
        try:
            self.print_step("Quick connecting...")

            self.client = TelegramClient(
                self.session_name, self.api_id, self.api_hash)
            await self.client.connect()

            if not await self.client.is_user_authorized():
                await self.client.send_code_request(self.phone)
                code = input("🔢 Verification code: ").strip()

                try:
                    await self.client.sign_in(self.phone, code)
                except SessionPasswordNeededError:
                    password = input("🔐 2FA password: ").strip()
                    await self.client.sign_in(password=password)

            self.print_success("Connected!")
            return True

        except Exception as e:
            self.print_error(f"Connection failed: {e}")
            return False

    async def quick_extract(self, username):
        """ดึงข้อมูลแบบเร็ว"""
        try:
            if username.startswith('@'):
                username = username[1:]

            self.print_step(f"Extracting @{username}")

            # Get user info
            user = await self.client.get_entity(username)

            # Quick data structure
            data = {
                'username': username,
                'id': user.id,
                'name': f"{getattr(user, 'first_name', '')} {getattr(user, 'last_name', '')}".strip(),
                'phone': getattr(user, 'phone', 'Hidden'),
                'verified': getattr(user, 'verified', False),
                'premium': getattr(user, 'premium', False),
                'status': str(getattr(user, 'status', 'unknown')),
                'extraction_time': datetime.now().isoformat()
            }

            # Get recent messages (quick sample)
            messages = []
            try:
                async for message in self.client.iter_messages(user, limit=10):
                    if message.text:
                        messages.append({
                            'date': message.date.isoformat(),
                            'text': message.text[:100],
                            'outgoing': message.out
                        })
            except:
                pass

            data['recent_messages'] = messages
            data['message_count'] = len(messages)

            self.print_success(
                f"✅ @{username}: {data['name']} - {len(messages)} messages")
            return data

        except Exception as e:
            self.print_error(f"❌ @{username}: {e}")
            return {'username': username, 'error': str(e), 'extraction_time': datetime.now().isoformat()}

    async def extract_multiple_targets(self, targets):
        """ดึงข้อมูลหลาย targets"""
        if not await self.quick_connect():
            return None

        results = {
            'extraction_time': datetime.now().isoformat(),
            'total_targets': len(targets),
            'successful_extractions': 0,
            'failed_extractions': 0,
            'targets': {}
        }

        for target in targets:
            data = await self.quick_extract(target)
            results['targets'][target] = data

            if 'error' in data:
                results['failed_extractions'] += 1
            else:
                results['successful_extractions'] += 1

            # Small delay between targets
            await asyncio.sleep(1)

        await self.client.disconnect()

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"quick_telegram_extraction_{timestamp}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        # Generate quick report
        self.generate_quick_report(results, timestamp)

        return results

    def generate_quick_report(self, results, timestamp):
        """สร้างรายงานแบบเร็ว"""
        report = f"""
🚀💎 QUICK TELEGRAM EXTRACTION REPORT 💎🚀
========================================================

⏰ Extraction Time: {timestamp}
🎯 Total Targets: {results['total_targets']}
✅ Successful: {results['successful_extractions']}
❌ Failed: {results['failed_extractions']}

📊 EXTRACTION RESULTS:
========================================================

"""

        for username, data in results['targets'].items():
            if 'error' in data:
                report += f"❌ @{username}: {data['error']}\n\n"
            else:
                report += f"""
✅ @{username}
   👤 Name: {data.get('name', 'Unknown')}
   📱 Phone: {data.get('phone', 'Hidden')}
   🔖 Verified: {'Yes' if data.get('verified') else 'No'}
   💎 Premium: {'Yes' if data.get('premium') else 'No'}
   📊 Status: {data.get('status', 'Unknown')}
   💬 Messages: {data.get('message_count', 0)}

"""

                if data.get('recent_messages'):
                    report += "   📝 Recent Messages:\n"
                    for i, msg in enumerate(data['recent_messages'][:3], 1):
                        direction = "→" if msg['outgoing'] else "←"
                        report += f"   {i}. {direction} {msg['text'][:50]}...\n"
                    report += "\n"

        report += f"""
🔥 SUMMARY:
========================================================
• Quick extraction completed in real-time
• Using Telethon API for authentic data
• All data from project target: alx.trading
• Telegram variants successfully mapped

⚠️  SECURITY NOTE:
========================================================
This data was extracted using legitimate API access.
Handle all personal information with care and in 
compliance with privacy laws and regulations.

========================================================
🚀 Quick extraction by Project Telegram Framework
📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
========================================================
"""

        report_filename = f"quick_telegram_report_{timestamp}.txt"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)

        self.print_success(f"Report saved: {report_filename}")


async def main():
    """Main function"""
    extractor = QuickTelegramExtractor()

    if not extractor.get_quick_credentials():
        sys.exit(1)

    targets = extractor.select_target()

    print(f"\n🎯 Selected targets: {', '.join(['@' + t for t in targets])}")
    print("🚀 Starting quick extraction...")

    confirm = input("\nProceed? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        sys.exit(0)

    try:
        results = await extractor.extract_multiple_targets(targets)

        if results:
            print(f"\n{Colors.GREEN}🎉 QUICK EXTRACTION COMPLETED!{Colors.END}")
            print(
                f"✅ Success: {results['successful_extractions']}/{results['total_targets']}")

            if results['successful_extractions'] > 0:
                print("\n📊 Summary:")
                for username, data in results['targets'].items():
                    if 'error' not in data:
                        print(
                            f"  @{username}: {data['name']} ({data['message_count']} messages)")

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Extraction interrupted{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Extraction failed: {e}{Colors.END}")


if __name__ == "__main__":
    asyncio.run(main())
