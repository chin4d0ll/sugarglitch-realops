#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 REAL TELEGRAM API DATA EXTRACTOR 🔥
สำหรับดึงข้อมูลจริงจาก Telegram API
ใช้ telethon library เพื่อเข้าถึงข้อมูลจริง
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import re


class RealTelegramExtractor:
    def __init__(self):
        # คุณต้องได้ API credentials จาก https://my.telegram.org/
        self.api_id = None  # ใส่ API ID ของคุณ
        self.api_hash = None  # ใส่ API Hash ของคุณ
        self.phone = None  # ใส่เบอร์โทรของคุณ
        self.client = None
        self.session_file = 'telegram_session'

    def setup_credentials(self):
        """ตั้งค่า API credentials"""
        print("🔧 ตั้งค่า Telegram API Credentials")
        print("=" * 50)
        print("📱 คุณต้องมี API credentials จาก https://my.telegram.org/")
        print("1. ไปที่ https://my.telegram.org/")
        print("2. เข้าสู่ระบบด้วยเบอร์โทร")
        print("3. ไป API development tools")
        print("4. สร้าง app ใหม่")
        print("5. คัดลอก API ID และ API Hash")
        print()

        # อ่านจากไฟล์ config หรือ input
        config_file = 'telegram_config.json'
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                self.api_id = config.get('api_id')
                self.api_hash = config.get('api_hash')
                self.phone = config.get('phone')
                print(f"✅ โหลด config จาก {config_file}")
        else:
            print("❌ ไม่พบไฟล์ config")
            print("📝 สร้างไฟล์ telegram_config.json ด้วยข้อมูล:")
            config_template = {
                "api_id": "YOUR_API_ID",
                "api_hash": "YOUR_API_HASH",
                "phone": "YOUR_PHONE_NUMBER"
            }
            with open(config_file, 'w') as f:
                json.dump(config_template, f, indent=2)
            print(f"📄 ไฟล์ {config_file} ถูกสร้างแล้ว")
            print("✏️ กรุณาแก้ไขไฟล์นี้ด้วยข้อมูลจริง")
            return False

        if not all([self.api_id, self.api_hash, self.phone]):
            print("❌ ข้อมูล API ไม่ครบถ้วน")
            return False

        return True

    async def connect_telegram(self):
        """เชื่อมต่อกับ Telegram"""
        try:
            self.client = TelegramClient(
                self.session_file, self.api_id, self.api_hash)
            await self.client.start(phone=self.phone)

            if not await self.client.is_user_authorized():
                print("❌ ไม่สามารถเข้าสู่ระบบได้")
                return False

            me = await self.client.get_me()
            print(f"✅ เชื่อมต่อสำเร็จ: {me.first_name} {me.last_name or ''}")
            return True

        except Exception as e:
            print(f"❌ ข้อผิดพลาดในการเชื่อมต่อ: {e}")
            return False

    async def get_user_info(self, username):
        """ดึงข้อมูลผู้ใช้"""
        try:
            user = await self.client.get_entity(username)
            return {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': user.phone,
                'is_verified': user.verified,
                'is_premium': getattr(user, 'premium', False),
                'status': str(user.status) if hasattr(user, 'status') else None
            }
        except Exception as e:
            print(f"❌ ไม่สามารถดึงข้อมูลผู้ใช้ {username}: {e}")
            return None

    async def get_chat_history(self, username, limit=100):
        """ดึงประวัติแชท"""
        try:
            entity = await self.client.get_entity(username)
            messages = await self.client.get_messages(entity, limit=limit)

            chat_data = []
            for msg in messages:
                if msg.message:
                    message_data = {
                        'id': msg.id,
                        'date': msg.date.isoformat(),
                        'from_id': msg.from_id.user_id if msg.from_id else None,
                        'to_id': msg.peer_id.user_id if hasattr(msg.peer_id, 'user_id') else None,
                        'message': msg.message,
                        'reply_to': msg.reply_to.reply_to_msg_id if msg.reply_to else None,
                        'forwarded_from': str(msg.fwd_from) if msg.fwd_from else None,
                        'media': str(msg.media) if msg.media else None,
                        'entities': [str(entity) for entity in msg.entities] if msg.entities else []
                    }
                    chat_data.append(message_data)

            return chat_data

        except Exception as e:
            print(f"❌ ไม่สามารถดึงประวัติแชท {username}: {e}")
            return []

    async def get_dialogs(self, limit=50):
        """ดึงรายการแชททั้งหมด"""
        try:
            dialogs = await self.client.get_dialogs(limit=limit)
            dialog_list = []

            for dialog in dialogs:
                dialog_data = {
                    'id': dialog.entity.id,
                    'title': dialog.title,
                    'username': getattr(dialog.entity, 'username', None),
                    'type': type(dialog.entity).__name__,
                    'unread_count': dialog.unread_count,
                    'last_message_date': dialog.date.isoformat() if dialog.date else None,
                    'is_pinned': dialog.pinned
                }
                dialog_list.append(dialog_data)

            return dialog_list

        except Exception as e:
            print(f"❌ ไม่สามารถดึงรายการแชท: {e}")
            return []

    async def search_messages(self, query, limit=50):
        """ค้นหาข้อความ"""
        try:
            results = []
            async for message in self.client.iter_messages(None, search=query, limit=limit):
                if message.message:
                    result = {
                        'id': message.id,
                        'date': message.date.isoformat(),
                        'chat_id': message.chat_id,
                        'from_id': message.from_id.user_id if message.from_id else None,
                        'message': message.message,
                        'chat_title': getattr(message.chat, 'title', 'Private Chat')
                    }
                    results.append(result)

            return results

        except Exception as e:
            print(f"❌ ไม่สามารถค้นหาข้อความ: {e}")
            return []

    def analyze_sensitive_data(self, messages):
        """วิเคราะห์ข้อมูลสำคัญในข้อความ"""
        sensitive_patterns = {
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'password': r'(?i)(password|pass|pwd)\s*[:=]\s*([^\s]+)',
            'phone': r'(\+?\d{1,4}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
            'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            'thai_id': r'\b\d{13}\b',
            'bank_account': r'\b\d{3}-?\d{1}-?\d{5}-?\d{1}\b',
            'crypto_address': r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b|0x[a-fA-F0-9]{40}',
            'seed_phrase': r'\b(?:\w+\s+){11,23}\w+\b'
        }

        findings = []
        for msg in messages:
            text = msg.get('message', '')
            for pattern_name, pattern in sensitive_patterns.items():
                matches = re.findall(pattern, text)
                if matches:
                    findings.append({
                        'message_id': msg.get('id'),
                        'date': msg.get('date'),
                        'pattern_type': pattern_name,
                        'matches': matches,
                        'context': text[:200] + '...' if len(text) > 200 else text
                    })

        return findings

    async def extract_target_data(self, target_username):
        """ดึงข้อมูลครบถ้วนของเป้าหมาย"""
        print(f"🎯 กำลังดึงข้อมูล: {target_username}")

        # ข้อมูลผู้ใช้
        user_info = await self.get_user_info(target_username)

        # ประวัติแชท
        chat_history = await self.get_chat_history(target_username, limit=500)

        # วิเคราะห์ข้อมูลสำคัญ
        sensitive_data = self.analyze_sensitive_data(chat_history)

        # ค้นหาข้อความที่มีคำสำคัญ
        keywords = ['password', 'pin', 'code',
                    'account', 'wallet', 'bank', 'money']
        keyword_results = {}
        for keyword in keywords:
            results = await self.search_messages(keyword, limit=20)
            if results:
                keyword_results[keyword] = results

        return {
            'target': target_username,
            'user_info': user_info,
            'chat_history': chat_history,
            'sensitive_data': sensitive_data,
            'keyword_searches': keyword_results,
            'extraction_time': datetime.now().isoformat(),
            'total_messages': len(chat_history),
            'sensitive_findings': len(sensitive_data)
        }

    def save_results(self, data, target):
        """บันทึกผลลัพธ์"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # บันทึกข้อมูลดิบ
        json_file = f"real_telegram_data_{target}_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # สร้างรายงาน
        report_file = f"real_telegram_report_{target}_{timestamp}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("🔥 REAL TELEGRAM DATA EXTRACTION REPORT 🔥\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"🎯 Target: {target}\n")
            f.write(f"⏰ Extraction Time: {data['extraction_time']}\n")
            f.write(f"📊 Total Messages: {data['total_messages']}\n")
            f.write(f"🚨 Sensitive Findings: {data['sensitive_findings']}\n\n")

            # ข้อมูลผู้ใช้
            if data['user_info']:
                f.write("👤 USER INFORMATION:\n")
                f.write("-" * 30 + "\n")
                for key, value in data['user_info'].items():
                    f.write(f"{key}: {value}\n")
                f.write("\n")

            # ข้อมูลสำคัญที่พบ
            if data['sensitive_data']:
                f.write("🚨 SENSITIVE DATA FOUND:\n")
                f.write("-" * 30 + "\n")
                for finding in data['sensitive_data']:
                    f.write(f"Type: {finding['pattern_type']}\n")
                    f.write(f"Date: {finding['date']}\n")
                    f.write(f"Matches: {finding['matches']}\n")
                    f.write(f"Context: {finding['context']}\n")
                    f.write("-" * 20 + "\n")
                f.write("\n")

            # ข้อความล่าสุด
            f.write("💬 RECENT MESSAGES:\n")
            f.write("-" * 30 + "\n")
            for msg in data['chat_history'][:10]:
                f.write(f"[{msg['date']}] ID:{msg['id']}\n")
                f.write(f"Message: {msg['message'][:100]}...\n")
                f.write("-" * 20 + "\n")

        print(f"✅ บันทึกข้อมูลเรียบร้อย:")
        print(f"   📄 JSON: {json_file}")
        print(f"   📋 Report: {report_file}")

    async def run_extraction(self, target_username):
        """รันการดึงข้อมูล"""
        print("🔥 REAL TELEGRAM DATA EXTRACTOR 🔥")
        print("=" * 50)

        # ตั้งค่า credentials
        if not self.setup_credentials():
            return

        # เชื่อมต่อ Telegram
        if not await self.connect_telegram():
            return

        try:
            # ดึงข้อมูล
            data = await self.extract_target_data(target_username)

            # บันทึกผลลัพธ์
            self.save_results(data, target_username)

            print("\n🎉 การดึงข้อมูลเสร็จสมบูรณ์!")

        except Exception as e:
            print(f"❌ ข้อผิดพลาด: {e}")

        finally:
            await self.client.disconnect()


async def main():
    """ฟังก์ชันหลัก"""
    extractor = RealTelegramExtractor()

    # เป้าหมายที่ต้องการดึงข้อมูล
    target = "Alx_TYW"  # เปลี่ยนเป็น username ที่ต้องการ

    await extractor.run_extraction(target)

if __name__ == "__main__":
    print("🚀 Starting Real Telegram Data Extraction...")
    asyncio.run(main())
