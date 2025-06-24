#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 Telegram Auto Message Forwarder
ระบบ forward ข้อความอัตโนมัติระหว่างแชท/กลุ่ม/ช่อง

✨ Features:
- Auto forward ข้อความจากแชทต้นทางไปปลายทาง
- กรองตาม keywords
- กรองตามประเภทข้อความ (text, photo, video, etc.)
- ตั้งเวลา delay
- บันทึก log การ forward
- รองรับหลายกฎพร้อมกัน
"""

import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaVideo, MessageMediaDocument
import re
import json
import logging
from datetime import datetime
import os

# ตั้งค่า logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_forwarder.log'),
        logging.StreamHandler()
    ]
)

class TelegramForwarder:
    def __init__(self, api_id, api_hash, phone):
        """
        สร้าง Telegram auto forwarder
        
        Args:
            api_id (str): API ID จาก my.telegram.org
            api_hash (str): API Hash จาก my.telegram.org
            phone (str): เบอร์โทรศัพท์
        """
        self.client = TelegramClient('forwarder_session', api_id, api_hash)
        self.phone = phone
        self.forwarding_rules = {}  # เก็บกฎการ forward
        self.stats = {
            'messages_forwarded': 0,
            'messages_filtered': 0,
            'errors': 0,
            'start_time': None
        }
        self.is_running = False
        
    async def connect(self):
        """เชื่อมต่อและเริ่มต้น forwarder"""
        try:
            await self.client.start(phone=self.phone)
            me = await self.client.get_me()
            print(f"🤖 Auto Forwarder เริ่มทำงานแล้วค่ะ! ผู้ใช้: {me.first_name}")
            logging.info(f"Connected as {me.username or me.first_name}")
            return True
        except Exception as e:
            print(f"❌ เชื่อมต่อไม่ได้: {e}")
            logging.error(f"Connection failed: {e}")
            return False
        
    def add_forwarding_rule(self, rule_name, source_chat, target_chats, **options):
        """
        เพิ่มกฎการ forward
        
        Args:
            rule_name (str): ชื่อกฎ
            source_chat (str): แชทต้นทาง (@username หรือ chat_id)
            target_chats (list): รายการแชทปลายทาง
            **options: ตัวเลือกเพิ่มเติม
                - keywords (list): คำสำคัญที่ต้องมีในข้อความ
                - exclude_keywords (list): คำที่ห้ามมี
                - media_types (list): ประเภทสื่อที่จะ forward ['photo', 'video', 'document']
                - delay (float): หน่วงเวลาก่อน forward (วินาที)
                - add_prefix (str): ข้อความที่จะเพิ่มหน้าข้อความ
                - add_suffix (str): ข้อความที่จะเพิ่มท้ายข้อความ
                - max_forwards_per_hour (int): จำกัดจำนวนการ forward ต่อชั่วโมง
        """
        self.forwarding_rules[rule_name] = {
            'source_chat': source_chat,
            'target_chats': target_chats if isinstance(target_chats, list) else [target_chats],
            'keywords': options.get('keywords', []),
            'exclude_keywords': options.get('exclude_keywords', []),
            'media_types': options.get('media_types', ['all']),
            'delay': options.get('delay', 0.5),
            'add_prefix': options.get('add_prefix', ''),
            'add_suffix': options.get('add_suffix', ''),
            'max_forwards_per_hour': options.get('max_forwards_per_hour', 100),
            'forwards_this_hour': 0,
            'last_hour_reset': datetime.now().hour,
            'enabled': True
        }
        
        print(f"✅ เพิ่มกฎ '{rule_name}' สำหรับ forward จาก {source_chat} แล้ว")
        logging.info(f"Added forwarding rule: {rule_name}")
    
    def remove_forwarding_rule(self, rule_name):
        """ลบกฎการ forward"""
        if rule_name in self.forwarding_rules:
            del self.forwarding_rules[rule_name]
            print(f"🗑️ ลบกฎ '{rule_name}' แล้ว")
            logging.info(f"Removed forwarding rule: {rule_name}")
        else:
            print(f"❌ ไม่พบกฎ '{rule_name}'")
    
    def toggle_rule(self, rule_name, enabled=None):
        """เปิด/ปิดการใช้งานกฎ"""
        if rule_name in self.forwarding_rules:
            if enabled is None:
                enabled = not self.forwarding_rules[rule_name]['enabled']
            
            self.forwarding_rules[rule_name]['enabled'] = enabled
            status = "เปิด" if enabled else "ปิด"
            print(f"🔄 {status}การใช้งานกฎ '{rule_name}' แล้ว")
            logging.info(f"Toggled rule {rule_name}: {enabled}")
        else:
            print(f"❌ ไม่พบกฎ '{rule_name}'")
    
    def list_rules(self):
        """แสดงรายการกฎทั้งหมด"""
        if not self.forwarding_rules:
            print("📝 ไม่มีกฎการ forward")
            return
        
        print("\n📋 รายการกฎการ Forward:")
        print("=" * 60)
        
        for rule_name, rule in self.forwarding_rules.items():
            status = "🟢" if rule['enabled'] else "🔴"
            print(f"{status} {rule_name}")
            print(f"   📥 จาก: {rule['source_chat']}")
            print(f"   📤 ไป: {', '.join(rule['target_chats'])}")
            
            if rule['keywords']:
                print(f"   🔑 Keywords: {', '.join(rule['keywords'])}")
            if rule['exclude_keywords']:
                print(f"   🚫 Exclude: {', '.join(rule['exclude_keywords'])}")
            if rule['media_types'] != ['all']:
                print(f"   📎 Media: {', '.join(rule['media_types'])}")
            
            print(f"   ⏱️ Delay: {rule['delay']}s")
            print(f"   📊 Forwards this hour: {rule['forwards_this_hour']}/{rule['max_forwards_per_hour']}")
            print("-" * 60)
    
    async def _should_forward_message(self, event, rule):
        """ตรวจสอบว่าควร forward ข้อความหรือไม่"""
        message = event.message
        message_text = message.text or ""
        
        # ตรวจสอบ keywords ที่ต้องมี
        if rule['keywords']:
            has_keyword = any(
                keyword.lower() in message_text.lower() 
                for keyword in rule['keywords']
            )
            if not has_keyword:
                return False, "ไม่มี keyword ที่กำหนด"
        
        # ตรวจสอบ keywords ที่ห้ามมี
        if rule['exclude_keywords']:
            has_excluded = any(
                keyword.lower() in message_text.lower() 
                for keyword in rule['exclude_keywords']
            )
            if has_excluded:
                return False, "มี keyword ที่ห้าม"
        
        # ตรวจสอบประเภทสื่อ
        if rule['media_types'] != ['all']:
            media_type = self._get_media_type(message)
            if media_type not in rule['media_types'] and 'all' not in rule['media_types']:
                return False, f"ประเภทสื่อไม่ตรง ({media_type})"
        
        # ตรวจสอบ rate limit
        current_hour = datetime.now().hour
        if rule['last_hour_reset'] != current_hour:
            rule['forwards_this_hour'] = 0
            rule['last_hour_reset'] = current_hour
        
        if rule['forwards_this_hour'] >= rule['max_forwards_per_hour']:
            return False, "เกิน rate limit"
        
        return True, "ผ่านเงื่อนไขทั้งหมด"
    
    def _get_media_type(self, message):
        """ตรวจสอบประเภทสื่อของข้อความ"""
        if not message.media:
            return 'text'
        elif isinstance(message.media, MessageMediaPhoto):
            return 'photo'
        elif isinstance(message.media, MessageMediaVideo):
            return 'video'
        elif isinstance(message.media, MessageMediaDocument):
            if message.media.document.mime_type.startswith('audio/'):
                return 'audio'
            elif message.media.document.mime_type.startswith('video/'):
                return 'video'
            else:
                return 'document'
        else:
            return 'other'
    
    async def _forward_message(self, event, target_chat, rule):
        """Forward ข้อความไปยัง target"""
        try:
            message = event.message
            
            # เตรียมข้อความที่จะ forward
            if rule['add_prefix'] or rule['add_suffix']:
                # ถ้ามี prefix/suffix ให้ส่งเป็นข้อความใหม่
                original_text = message.text or ""
                new_text = f"{rule['add_prefix']}{original_text}{rule['add_suffix']}"
                
                # ส่งข้อความใหม่
                await self.client.send_message(target_chat, new_text)
                
                # ถ้ามีสื่อ ส่งแยก
                if message.media:
                    await self.client.send_file(target_chat, message.media)
            else:
                # Forward ข้อความต้นฉบับ
                await self.client.forward_messages(target_chat, message)
            
            return True
            
        except Exception as e:
            logging.error(f"Forward failed to {target_chat}: {e}")
            return False
    
    async def start_forwarding(self):
        """เริ่มต้น auto forward"""
        if self.is_running:
            print("⚠️ Auto forwarder กำลังทำงานอยู่แล้ว")
            return
        
        self.is_running = True
        self.stats['start_time'] = datetime.now()
        
        @self.client.on(events.NewMessage)
        async def message_handler(event):
            if not self.is_running:
                return
                
            try:
                # ตรวจสอบแต่ละกฎ
                for rule_name, rule in self.forwarding_rules.items():
                    if not rule['enabled']:
                        continue
                    
                    # ตรวจสอบว่าข้อความมาจาก source chat ที่กำหนดหรือไม่
                    source_match = False
                    
                    # ตรวจสอบ chat ID
                    if str(event.chat_id) == str(rule['source_chat']):
                        source_match = True
                    # ตรวจสอบ username
                    elif (hasattr(event.chat, 'username') and 
                          event.chat.username and 
                          f"@{event.chat.username}" == rule['source_chat']):
                        source_match = True
                    elif (hasattr(event.chat, 'username') and 
                          event.chat.username == rule['source_chat'].replace('@', '')):
                        source_match = True
                    
                    if not source_match:
                        continue
                    
                    # ตรวจสอบเงื่อนไขการ forward
                    should_forward, reason = await self._should_forward_message(event, rule)
                    
                    if not should_forward:
                        self.stats['messages_filtered'] += 1
                        logging.debug(f"Message filtered for rule {rule_name}: {reason}")
                        continue
                    
                    # หน่วงเวลาถ้ากำหนด
                    if rule['delay'] > 0:
                        await asyncio.sleep(rule['delay'])
                    
                    # Forward ไปทุก target
                    forwarded_count = 0
                    for target in rule['target_chats']:
                        try:
                            success = await self._forward_message(event, target, rule)
                            if success:
                                forwarded_count += 1
                                print(f"📤 Forward ข้อความจาก {rule['source_chat']} ไป {target} (กฎ: {rule_name})")
                                
                            await asyncio.sleep(0.5)  # หน่วงเล็กน้อยระหว่าง target
                            
                        except Exception as e:
                            self.stats['errors'] += 1
                            print(f"❌ Forward ไปยัง {target} ไม่สำเร็จ: {e}")
                            logging.error(f"Forward error to {target}: {e}")
                    
                    if forwarded_count > 0:
                        rule['forwards_this_hour'] += forwarded_count
                        self.stats['messages_forwarded'] += forwarded_count
                        
                        # บันทึก log
                        await self._log_forward_activity(rule_name, event, forwarded_count)
                        
            except Exception as e:
                self.stats['errors'] += 1
                print(f"❌ Error ใน message handler: {e}")
                logging.error(f"Message handler error: {e}")
        
        print("👂 เริ่มฟังข้อความและ auto forward...")
        print("กด Ctrl+C เพื่อหยุด")
        
        try:
            await self.client.run_until_disconnected()
        except KeyboardInterrupt:
            print("\n⏹️ หยุดการทำงานโดยผู้ใช้")
        finally:
            self.is_running = False
            await self.show_stats()
    
    def stop_forwarding(self):
        """หยุด auto forward"""
        self.is_running = False
        print("⏹️ หยุด auto forwarder แล้ว")
    
    async def _log_forward_activity(self, rule_name, event, forwarded_count):
        """บันทึก log การ forward"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'rule_name': rule_name,
                'source_chat': event.chat_id,
                'message_id': event.message.id,
                'message_text': (event.message.text or "")[:100],  # เก็บแค่ 100 ตัวอักษรแรก
                'media_type': self._get_media_type(event.message),
                'forwarded_count': forwarded_count
            }
            
            # สร้างโฟลเดอร์ถ้าไม่มี
            os.makedirs('forwarding_logs', exist_ok=True)
            
            # บันทึกใน JSON log file
            log_file = f"forwarding_logs/forward_log_{datetime.now().strftime('%Y%m%d')}.json"
            
            # อ่านข้อมูลเก่า
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                logs = []
            
            # เพิ่มข้อมูลใหม่
            logs.append(log_entry)
            
            # บันทึกกลับ
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logging.error(f"Log writing error: {e}")
    
    async def show_stats(self):
        """แสดงสถิติการทำงาน"""
        if not self.stats['start_time']:
            print("❌ ยังไม่เริ่มการทำงาน")
            return
        
        duration = datetime.now() - self.stats['start_time']
        
        print("\n" + "="*50)
        print("📊 สถิติการ Forward")
        print("="*50)
        print(f"📤 ข้อความที่ forward: {self.stats['messages_forwarded']:,}")
        print(f"🔍 ข้อความที่กรอง: {self.stats['messages_filtered']:,}")
        print(f"❌ ข้อผิดพลาด: {self.stats['errors']:,}")
        print(f"⏱️ เวลาที่ทำงาน: {duration}")
        print(f"📈 อัตราการ forward: {self.stats['messages_forwarded']/max(duration.total_seconds()/3600, 0.01):.1f} ข้อความ/ชั่วโมง")
        print("="*50)
    
    def save_rules_to_file(self, filename='forwarding_rules.json'):
        """บันทึกกฎลงไฟล์"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.forwarding_rules, f, ensure_ascii=False, indent=2, default=str)
            print(f"💾 บันทึกกฎใน {filename} แล้ว")
        except Exception as e:
            print(f"❌ บันทึกกฎไม่ได้: {e}")
    
    def load_rules_from_file(self, filename='forwarding_rules.json'):
        """โหลดกฎจากไฟล์"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.forwarding_rules = json.load(f)
            print(f"📂 โหลดกฎจาก {filename} แล้ว ({len(self.forwarding_rules)} กฎ)")
        except FileNotFoundError:
            print(f"❌ ไม่พบไฟล์ {filename}")
        except Exception as e:
            print(f"❌ โหลดกฎไม่ได้: {e}")

# วิธีใช้งาน
async def main():
    print("🔄 Telegram Auto Message Forwarder")
    print("=" * 50)
    
    # ใส่ข้อมูลของตัวเองที่นี่
    API_ID = 'your_api_id'  # จาก my.telegram.org
    API_HASH = 'your_api_hash'  # จาก my.telegram.org
    PHONE = '+66xxxxxxxxx'  # เบอร์โทรของคุณ
    
    # ตรวจสอบว่าใส่ข้อมูลแล้วหรือยัง
    if API_ID == 'your_api_id' or API_HASH == 'your_api_hash':
        print("❌ กรุณาใส่ API_ID และ API_HASH ที่ถูกต้อง!")
        print("📋 ไปรับที่: https://my.telegram.org")
        return
    
    forwarder = TelegramForwarder(API_ID, API_HASH, PHONE)
    
    if await forwarder.connect():
        # ลองโหลดกฎจากไฟล์
        forwarder.load_rules_from_file()
        
        # ตัวอย่างการตั้งกฎ
        print("\n📋 ตั้งค่ากฎการ Forward:")
        
        # กฎที่ 1: Forward ข่าวสำคัญ
        forwarder.add_forwarding_rule(
            rule_name="ข่าวสำคัญ",
            source_chat='@news_channel',
            target_chats=['@my_channel', '@backup_channel'],
            keywords=['ข่าวด่วน', 'สำคัญ', 'แจ้งเตือน'],
            exclude_keywords=['โฆษณา', 'สปอนเซอร์'],
            delay=1.0,
            add_prefix="🔥 ข่าวสำคัญ: ",
            max_forwards_per_hour=50
        )
        
        # กฎที่ 2: Forward รูปภาพเท่านั้น
        forwarder.add_forwarding_rule(
            rule_name="รูปภาพ",
            source_chat='@photo_channel',
            target_chats=['@my_photo_backup'],
            media_types=['photo'],
            delay=2.0
        )
        
        # กฎที่ 3: Forward ทุกอย่างจากกลุ่มเฉพาะ
        forwarder.add_forwarding_rule(
            rule_name="กลุ่มหลัก",
            source_chat='@main_group',
            target_chats=['@backup_group'],
            delay=0.5,
            max_forwards_per_hour=200
        )
        
        # แสดงกฎทั้งหมด
        forwarder.list_rules()
        
        # บันทึกกฎ
        forwarder.save_rules_to_file()
        
        # เริ่ม auto forward
        print("\n🚀 เริ่ม Auto Forward...")
        await forwarder.start_forwarding()
    
    await forwarder.client.disconnect()
    print("\n✅ เสร็จสิ้นการทำงาน!")

# รันโปรแกรม
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ หยุดการทำงานโดยผู้ใช้")
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        logging.error(f"Main error: {e}")
