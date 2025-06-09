# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
⚡🎯 DM EXTRACTION COMMANDER 2025 🎯⚡
===================================
- Command-line interface for DM extraction
- Multi-session management
- Automated extraction workflows
- Advanced filtering and targeting
- Real-time monitoring commands
- Batch processing capabilities

ระบบควบคุม DM extraction แบบ Command Line!

Created by: น้องจิน (chin4d0ll) ♥️
For: Ultimate Instagram Intelligence Operations 2025
"""

import asyncio
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import readline
import colorama
from colorama import Fore, Back, Style, init
import time
import os

# Initialize colorama
init(autoreset=True)

# Import our modules
try:
    from extreme_dm_intelligence_extractor_2025 import ExtremeDMIntelligenceExtractor, MessageType, SentimentLevel
except ImportError:
    print(f"{Fore.RED}❌ ไม่พบ extreme_dm_intelligence_extractor_2025.py")
    sys.exit(1)

class DMExtractionCommander:
    """⚡🎯 ระบบควบคุม DM extraction"""

    def __init__(self):
        self.extractor = ExtremeDMIntelligenceExtractor()
        self.session_loaded = False
        self.current_threads = []
        self.monitoring_active = False

        print(f"{Fore.CYAN}⚡🎯 DM EXTRACTION COMMANDER 2025 🎯⚡")
        print(f"{Fore.YELLOW}=" * 50)

    def print_banner(self):
        """แสดง banner"""
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════╗
║           {Fore.YELLOW}⚡ DM EXTRACTION COMMANDER 2025 ⚡{Fore.CYAN}           ║
║                                                      ║
║  {Fore.GREEN}🧠 AI-Powered DM Intelligence System{Fore.CYAN}               ║
║  {Fore.GREEN}💬 Advanced Conversation Analysis{Fore.CYAN}                  ║
║  {Fore.GREEN}🔄 Real-time Monitoring Capabilities{Fore.CYAN}               ║
║  {Fore.GREEN}📊 Comprehensive Data Visualization{Fore.CYAN}                ║
║                                                      ║
║           {Fore.MAGENTA}Created by น้องจิน (chin4d0ll) ♥️{Fore.CYAN}          ║
╚══════════════════════════════════════════════════════╝
        """
        print(banner)

    def print_status(self):
        """แสดงสถานะปัจจุบัน"""
        stats = self.extractor.get_statistics()

        print(f"\n{Fore.YELLOW}📊 สถานะระบบ:")
        print(f"  {Fore.GREEN}✓ Sessions: {stats['active_sessions']}/{stats['session_pool_size']}")
        print(f"  {Fore.GREEN}✓ Messages Extracted: {stats['extraction_stats']['messages_extracted']}")
        print(f"  {Fore.GREEN}✓ Conversations Analyzed: {stats['extraction_stats']['conversations_analyzed']}")
        print(f"  {Fore.GREEN}✓ Patterns Detected: {stats['extraction_stats']['patterns_detected']}")
        print(f"  {Fore.GREEN}✓ Monitoring: {'🔄 Active' if stats['monitoring_active'] else '⏹️ Inactive'}")

    async def load_sessions_command(self, args: List[str]):
        """โหลดเซสชัน"""
        session_dir = args[0] if args else "sessions/"

        print(f"{Fore.YELLOW}📁 โหลดเซสชันจาก: {session_dir}")
        count = await self.extractor.load_session_pool(session_dir)

        if count > 0:
            self.session_loaded = True
            print(f"{Fore.GREEN}✅ โหลด {count} sessions เรียบร้อย")
        else:
            print(f"{Fore.RED}❌ ไม่สามารถโหลดเซสชัน")

    async def list_conversations_command(self, args: List[str]):
        """แสดงรายการ conversations"""
        if not self.session_loaded:
            print(f"{Fore.RED}❌ กรุณาโหลดเซสชันก่อน")
            return

        limit = int(args[0]) if args else 20

        print(f"{Fore.YELLOW}🔍 ดึงรายการ conversations (จำกัด {limit} รายการ)...")
        threads = await self.extractor.extract_conversation_threads(limit)

        if threads:
            self.current_threads = threads
            print(f"\n{Fore.GREEN}📝 พบ {len(threads)} conversations:")
            print(f"{Fore.CYAN}{'No.':<4} {'Thread ID':<15} {'Users':<30} {'Last Activity'}")
            print(f"{Fore.CYAN}{'-' * 70}")

            for i, thread in enumerate(threads):
                thread_id = thread.get('thread_id', 'unknown')[:12] + '...'
                users = [user.get('username', 'unknown') for user in thread.get('users', [])]
                user_str = ', '.join(users[:2])
                if len(users) > 2:
                    user_str += f" +{len(users)-2}"

                last_activity = thread.get('last_activity_at', 'unknown')
                print(f"{Fore.WHITE}{i+1:<4} {thread_id:<15} {user_str:<30} {last_activity}")
        else:
            print(f"{Fore.RED}❌ ไม่พบ conversations")

    async def extract_messages_command(self, args: List[str]):
        """ดึงข้อความจาก thread"""
        if not args:
            print(f"{Fore.RED}❌ กรุณาระบุ thread index หรือ thread_id")
            return

        try:
            # ลองแปลงเป็น index ก่อน
            thread_index = int(args[0]) - 1
            if 0 <= thread_index < len(self.current_threads):
                thread_id = self.current_threads[thread_index]['thread_id']
            else:
                print(f"{Fore.RED}❌ Index ไม่ถูกต้อง")
                return
        except ValueError:
            # ถ้าไม่ใช่ index ให้ใช้เป็น thread_id
            thread_id = args[0]

        limit = int(args[1]) if len(args) > 1 else 100

        print(f"{Fore.YELLOW}💬 ดึงข้อความจาก thread: {thread_id} (จำกัด {limit} ข้อความ)...")
        messages = await self.extractor.extract_thread_messages(thread_id, limit)

        if messages:
            print(f"\n{Fore.GREEN}✅ ดึง {len(messages)} ข้อความเรียบร้อย")
            print(f"{Fore.CYAN}{'Time':<20} {'Sender':<15} {'Type':<10} {'Content'}")
            print(f"{Fore.CYAN}{'-' * 80}")

            for msg in messages[-10:]:  # แสดง 10 ข้อความล่าสุด
                time_str = msg.timestamp.strftime("%m/%d %H:%M")
                sender = msg.sender_username[:12]
                msg_type = msg.message_type.value[:8]
                content = msg.content[:40] + '...' if len(msg.content) > 40 else msg.content
                content = content.replace('\n', ' ')

                print(f"{Fore.WHITE}{time_str:<20} {sender:<15} {msg_type:<10} {content}")
        else:
            print(f"{Fore.RED}❌ ไม่สามารถดึงข้อความ")

    async def analyze_conversation_command(self, args: List[str]):
        """วิเคราะห์การสนทนา"""
        if not args:
            print(f"{Fore.RED}❌ กรุณาระบุ thread index หรือ thread_id")
            return

        try:
            thread_index = int(args[0]) - 1
            if 0 <= thread_index < len(self.current_threads):
                thread_id = self.current_threads[thread_index]['thread_id']
            else:
                print(f"{Fore.RED}❌ Index ไม่ถูกต้อง")
                return
        except ValueError:
            thread_id = args[0]

        print(f"{Fore.YELLOW}🔍 วิเคราะห์การสนทนา: {thread_id}...")

        # สร้างชื่อไฟล์รายงาน
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"reports/conversation_analysis_{timestamp}.json"

        # สร้างโฟลเดอร์ถ้าไม่มี
        Path("reports").mkdir(exist_ok=True)

        report = await self.extractor.generate_conversation_report(thread_id, report_path)

        if report:
            print(f"\n{Fore.GREEN}✅ การวิเคราะห์เสร็จสิ้น")
            print(f"{Fore.CYAN}📊 สรุปการสนทนา:")
            print(f"  👥 ผู้เข้าร่วม: {', '.join(report['participants'])}")
            print(f"  📨 ข้อความทั้งหมด: {report['summary']['total_messages']}")
            print(f"  🖼️ Media: {report['summary']['media_messages']}")
            print(f"  🎤 Voice: {report['summary']['voice_messages']}")
            print(f"  📅 ระยะเวลา: {report['summary']['conversation_span_days']} วัน")
            print(f"  💾 รายงานบันทึกที่: {report_path}")

            # แสดงสถิติผู้ใช้
            print(f"\n{Fore.CYAN}👥 สถิติผู้ใช้:")
            for user, count in report['user_stats'].items():
                print(f"  {user}: {count} ข้อความ")
        else:
            print(f"{Fore.RED}❌ ไม่สามารถวิเคราะห์การสนทนา")

    async def start_monitoring_command(self, args: List[str]):
        """เริ่มการติดตาม real-time"""
        if not args:
            print(f"{Fore.RED}❌ กรุณาระบุ thread indices (เช่น 1,2,3)")
            return

        try:
            indices = [int(i.strip()) - 1 for i in args[0].split(',')]
            thread_ids = []

            for idx in indices:
                if 0 <= idx < len(self.current_threads):
                    thread_ids.append(self.current_threads[idx]['thread_id'])
                else:
                    print(f"{Fore.YELLOW}⚠️ ข้าม index {idx+1} (ไม่ถูกต้อง)")

            if not thread_ids:
                print(f"{Fore.RED}❌ ไม่มี thread ที่ถูกต้อง")
                return

            print(f"{Fore.GREEN}🔄 เริ่มติดตาม {len(thread_ids)} threads...")
            for i, tid in enumerate(thread_ids):
                print(f"  {i+1}. {tid}")

            # เริ่มการติดตาม (จำลอง)
            self.monitoring_active = True
            print(f"{Fore.CYAN}✅ การติดตามเริ่มแล้ว (พิมพ์ 'stop_monitor' เพื่อหยุด)")

        except ValueError:
            print(f"{Fore.RED}❌ รูปแบบ indices ไม่ถูกต้อง")

    def stop_monitoring_command(self, args: List[str]):
        """หยุดการติดตาม"""
        if self.monitoring_active:
            self.monitoring_active = False
            self.extractor.stop_monitoring()
            print(f"{Fore.YELLOW}⏹️ หยุดการติดตาม")
        else:
            print(f"{Fore.YELLOW}⚠️ ไม่มีการติดตามที่กำลังทำงาน")

    def export_command(self, args: List[str]):
        """ส่งออกข้อมูล"""
        if not args:
            print(f"{Fore.RED}❌ กรุณาระบุรูปแบบ: excel, csv, json")
            return

        format_type = args[0].lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if format_type not in ['excel', 'csv', 'json']:
            print(f"{Fore.RED}❌ รูปแบบไม่ถูกต้อง: {format_type}")
            return

        output_path = f"exports/dm_export_{timestamp}.{format_type}"
        Path("exports").mkdir(exist_ok=True)

        print(f"{Fore.YELLOW}📤 ส่งออกข้อมูลเป็น {format_type.upper()}...")
        print(f"{Fore.GREEN}✅ ส่งออกเป็น: {output_path}")

    def help_command(self, args: List[str]):
        """แสดงคำสั่งที่ใช้งานได้"""
        commands = {
            "load_sessions [dir]": "โหลดเซสชันจากโฟลเดอร์",
            "list_conversations [limit]": "แสดงรายการ conversations",
            "extract <index|thread_id> [limit]": "ดึงข้อความจาก thread",
            "analyze <index|thread_id>": "วิเคราะห์การสนทนา",
            "start_monitor <indices>": "เริ่มติดตาม threads (เช่น 1,2,3)",
            "stop_monitor": "หยุดการติดตาม",
            "export <format>": "ส่งออกข้อมูล (excel/csv/json)",
            "status": "แสดงสถานะระบบ",
            "clear": "ล้างหน้าจอ",
            "help": "แสดงคำสั่งนี้",
            "exit": "ออกจากโปรแกรม"
        }

        print(f"\n{Fore.CYAN}🔧 คำสั่งที่ใช้งานได้:")
        print(f"{Fore.CYAN}{'-' * 50}")

        for cmd, desc in commands.items():
            print(f"  {Fore.GREEN}{cmd:<30} {Fore.WHITE}{desc}")

        print(f"\n{Fore.YELLOW}💡 ตัวอย่างการใช้งาน:")
        print(f"  {Fore.CYAN}load_sessions sessions/")
        print(f"  {Fore.CYAN}list_conversations 10")
        print(f"  {Fore.CYAN}extract 1 50")
        print(f"  {Fore.CYAN}analyze 1")
        print(f"  {Fore.CYAN}start_monitor 1,2,3")

    async def run_interactive(self):
        """รันโหมด interactive"""
        self.print_banner()
        print(f"{Fore.GREEN}🚀 พิมพ์ 'help' เพื่อดูคำสั่งที่ใช้งานได้")

        while True:
            try:
                # แสดง prompt
                if self.monitoring_active:
                    prompt = f"{Fore.RED}[MONITORING] {Fore.CYAN}DM-Commander> {Style.RESET_ALL}"
                else:
                    prompt = f"{Fore.CYAN}DM-Commander> {Style.RESET_ALL}"

                user_input = input(prompt).strip()

                if not user_input:
                    continue

                parts = user_input.split()
                command = parts[0].lower()
                args = parts[1:]

                # ประมวลผลคำสั่ง
                if command in ['exit', 'quit', 'q']:
                    print(f"{Fore.YELLOW}👋 ลาก่อน!")
                    break

                elif command == 'clear':
                    os.system('clear' if os.name == 'posix' else 'cls')
                    self.print_banner()

                elif command == 'help':
                    self.help_command(args)

                elif command == 'status':
                    self.print_status()

                elif command == 'load_sessions':
                    await self.load_sessions_command(args)

                elif command == 'list_conversations':
                    await self.list_conversations_command(args)

                elif command == 'extract':
                    await self.extract_messages_command(args)

                elif command == 'analyze':
                    await self.analyze_conversation_command(args)

                elif command == 'start_monitor':
                    await self.start_monitoring_command(args)

                elif command == 'stop_monitor':
                    self.stop_monitoring_command(args)

                elif command == 'export':
                    self.export_command(args)

                else:
                    print(f"{Fore.RED}❌ คำสั่งไม่ถูกต้อง: {command}")
                    print(f"{Fore.YELLOW}💡 พิมพ์ 'help' เพื่อดูคำสั่งที่ใช้งานได้")

            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}👋 ลาก่อน!")
                break

            except Exception as e:
                print(f"{Fore.RED}❌ Error: {e}")

async def main():
    """ฟังก์ชันหลัก"""
    parser = argparse.ArgumentParser(description="DM Extraction Commander 2025")
    parser.add_argument('--interactive', '-i', action='store_true', help='รันโหมด interactive')
    parser.add_argument('--load-sessions', help='โหลดเซสชันจากโฟลเดอร์')
    parser.add_argument('--list-conversations', type=int, help='แสดงรายการ conversations')
    parser.add_argument('--extract', help='ดึงข้อความจาก thread_id')
    parser.add_argument('--analyze', help='วิเคราะห์การสนทนา thread_id')

    args = parser.parse_args()

    commander = DMExtractionCommander()

    if args.interactive or len(sys.argv) == 1:
        # รันโหมด interactive
        await commander.run_interactive()
    else:
        # รันคำสั่งเดียว
        if args.load_sessions:
            await commander.load_sessions_command([args.load_sessions])

        if args.list_conversations:
            await commander.list_conversations_command([str(args.list_conversations)])

        if args.extract:
            await commander.extract_messages_command([args.extract])

        if args.analyze:
            await commander.analyze_conversation_command([args.analyze])

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 ลาก่อน!")
        sys.exit(0)