#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Telegram Message Bomber (Educational Purpose Only)
ระบบส่งข้อความแบบต่อเนื่องสำหรับการทดสอบ

⚠️ WARNING: ใช้เพื่อการศึกษาเท่านั้น!
"""

import asyncio
import logging
from telethon import TelegramClient
from telethon.errors import FloodWaitError, PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.types import InputPeerUser, InputPeerChat, InputPeerChannel
import time
import random
import json
from datetime import datetime

# ตั้งค่า logging เพื่อดู error
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_bomber.log'),
        logging.StreamHandler()
    ]
)

class TelegramBomber:
    def __init__(self, api_id, api_hash, phone):
        """
        สร้าง Telegram client สำหรับการส่งข้อความ
        
        Args:
            api_id (str): API ID จาก my.telegram.org
            api_hash (str): API Hash จาก my.telegram.org  
            phone (str): เบอร์โทรศัพท์ (+66xxxxxxxxx)
        """
        self.client = TelegramClient('bomber_session', api_id, api_hash)
        self.phone = phone
        self.stats = {
            'messages_sent': 0,
            'messages_failed': 0,
            'floods_encountered': 0,
            'start_time': None
        }
        
    async def connect_client(self):
        """เชื่อมต่อกับ Telegram API"""
        try:
            await self.client.start(phone=self.phone)
            me = await self.client.get_me()
            print(f"✅ เชื่อมต่อสำเร็จแล้วค่ะ! ผู้ใช้: {me.first_name}")
            logging.info(f"Connected as {me.username or me.first_name}")
            return True
        except Exception as e:
            print(f"❌ เชื่อมต่อไม่ได้: {e}")
            logging.error(f"Connection failed: {e}")
            return False
    
    async def send_flood_messages(self, target_username, message, count=50, delay=0.5, random_delay=True):
        """
        ส่งข้อความแบบต่อเนื่อง (ระวัง Flood Protection!)
        
        Args:
            target_username (str): username ของเป้าหมาย (@username หรือ username)
            message (str): ข้อความที่จะส่ง
            count (int): จำนวนข้อความ (default: 50)
            delay (float): ช่วงเวลาหน่วง (วินาที) (default: 0.5)
            random_delay (bool): ใช้เวลาหน่วงแบบสุ่ม (default: True)
        """
        try:
            # หาเป้าหมาย
            if not target_username.startswith('@'):
                target_username = f'@{target_username}'
                
            entity = await self.client.get_entity(target_username)
            print(f"🎯 พบเป้าหมาย: {entity.first_name or entity.title}")
            
            self.stats['start_time'] = datetime.now()
            success_count = 0
            
            # รายการข้อความที่หลากหลาย
            message_variants = [
                f"{message} 💕",
                f"{message} ✨", 
                f"{message} 🌸",
                f"{message} 💪",
                f"{message} 🚀",
                message
            ]
            
            for i in range(count):
                try:
                    # เลือกข้อความแบบสุ่ม
                    current_message = random.choice(message_variants) if len(message_variants) > 1 else message
                    final_message = f"{current_message} #{i+1}"
                    
                    # ส่งข้อความ
                    await self.client.send_message(entity, final_message)
                    success_count += 1
                    self.stats['messages_sent'] += 1
                    
                    print(f"📤 ส่งข้อความที่ {i+1}/{count} สำเร็จ")
                    
                    # หน่วงเวลาเพื่อหลีกเลี่ยง flood protection
                    if random_delay:
                        sleep_time = delay + random.uniform(0, delay)
                    else:
                        sleep_time = delay
                        
                    await asyncio.sleep(sleep_time)
                    
                except FloodWaitError as e:
                    self.stats['floods_encountered'] += 1
                    print(f"⏳ ต้องรอ {e.seconds} วินาที เพราะ flood protection")
                    logging.warning(f"FloodWait: {e.seconds} seconds")
                    await asyncio.sleep(e.seconds)
                    
                except PeerFloodError:
                    print("❌ โดน peer flood ban แล้วค่ะ (ส่งข้อความมากเกินไป)")
                    logging.error("PeerFloodError encountered")
                    break
                    
                except UserPrivacyRestrictedError:
                    print("❌ ผู้ใช้ตั้งค่าความเป็นส่วนตัวไม่ให้รับข้อความจากคนแปลกหน้า")
                    logging.error("User privacy restricted")
                    break
                    
                except Exception as e:
                    self.stats['messages_failed'] += 1
                    print(f"❌ Error: {e}")
                    logging.error(f"Message send error: {e}")
                    
            # แสดงสถิติ
            await self.show_stats(success_count, count)
            
        except Exception as e:
            print(f"❌ หาเป้าหมายไม่เจอ: {e}")
            logging.error(f"Target not found: {e}")

    async def send_scheduled_messages(self, target_username, messages_list, schedule_minutes=5):
        """
        ส่งข้อความตามกำหนดเวลา
        
        Args:
            target_username (str): username ของเป้าหมาย
            messages_list (list): รายการข้อความที่จะส่ง
            schedule_minutes (int): ช่วงเวลาระหว่างข้อความ (นาที)
        """
        try:
            if not target_username.startswith('@'):
                target_username = f'@{target_username}'
                
            entity = await self.client.get_entity(target_username)
            print(f"📅 เริ่มส่งข้อความตามกำหนดเวลาไป: {entity.first_name or entity.title}")
            
            for i, message in enumerate(messages_list):
                try:
                    await self.client.send_message(entity, message)
                    print(f"📤 ส่งข้อความที่ {i+1}/{len(messages_list)}: {message[:50]}...")
                    
                    if i < len(messages_list) - 1:  # ไม่รอในข้อความสุดท้าย
                        wait_seconds = schedule_minutes * 60
                        print(f"⏰ รอ {schedule_minutes} นาทีสำหรับข้อความถัดไป...")
                        await asyncio.sleep(wait_seconds)
                        
                except Exception as e:
                    print(f"❌ ส่งข้อความที่ {i+1} ไม่สำเร็จ: {e}")
                    
            print("✅ ส่งข้อความตามกำหนดเวลาเสร็จสิ้น!")
            
        except Exception as e:
            print(f"❌ Error ใน scheduled messages: {e}")

    async def show_stats(self, success_count, total_count):
        """แสดงสถิติการส่งข้อความ"""
        if self.stats['start_time']:
            duration = datetime.now() - self.stats['start_time']
            
        print("\n" + "="*50)
        print("📊 สถิติการส่งข้อความ")
        print("="*50)
        print(f"✅ ส่งสำเร็จ: {success_count}/{total_count} ข้อความ")
        print(f"📈 อัตราสำเร็จ: {(success_count/total_count)*100:.1f}%")
        print(f"❌ ส่งไม่สำเร็จ: {self.stats['messages_failed']} ข้อความ")
        print(f"⏳ โดน Flood: {self.stats['floods_encountered']} ครั้ง")
        if self.stats['start_time']:
            print(f"⏱️ เวลาที่ใช้: {duration}")
        print("="*50)

    async def save_session_info(self):
        """บันทึกข้อมูล session สำหรับใช้ในอนาคต"""
        try:
            me = await self.client.get_me()
            session_info = {
                'user_id': me.id,
                'username': me.username,
                'first_name': me.first_name,
                'phone': me.phone,
                'stats': self.stats,
                'saved_at': datetime.now().isoformat()
            }
            
            with open('bomber_session_info.json', 'w', encoding='utf-8') as f:
                json.dump(session_info, f, ensure_ascii=False, indent=2, default=str)
                
            print("💾 บันทึกข้อมูล session แล้ว")
            
        except Exception as e:
            print(f"❌ บันทึก session info ไม่ได้: {e}")

# วิธีใช้งาน
async def main():
    print("🚀 Telegram Message Bomber")
    print("⚠️ ใช้อย่างรับผิดชอบ!")
    print("-" * 40)
    
    # ใส่ข้อมูลของตัวเองที่นี่
    API_ID = 'your_api_id'  # จาก my.telegram.org
    API_HASH = 'your_api_hash'  # จาก my.telegram.org
    PHONE = '+66xxxxxxxxx'  # เบอร์โทรของคุณ
    
    # ตรวจสอบว่าใส่ข้อมูลแล้วหรือยัง
    if API_ID == 'your_api_id' or API_HASH == 'your_api_hash':
        print("❌ กรุณาใส่ API_ID และ API_HASH ที่ถูกต้อง!")
        print("📋 ไปรับที่: https://my.telegram.org")
        return
    
    bomber = TelegramBomber(API_ID, API_HASH, PHONE)
    
    if await bomber.connect_client():
        # ตัวอย่างการใช้งาน 1: ส่งข้อความแบบ flood
        target = "@target_username"  # เปลี่ยนเป็น username เป้าหมาย
        message = "สวัสดีค่ะ! 💕"
        
        print(f"🎯 เป้าหมาย: {target}")
        print(f"💬 ข้อความ: {message}")
        
        # เลือกโหมดการส่ง
        choice = input("\nเลือกโหมด:\n1. ส่งแบบ flood\n2. ส่งตามกำหนดเวลา\nใส่หมายเลข (1-2): ")
        
        if choice == "1":
            count = int(input("จำนวนข้อความ (default: 10): ") or "10")
            delay = float(input("หน่วงเวลา วินาที (default: 1.0): ") or "1.0")
            
            await bomber.send_flood_messages(target, message, count=count, delay=delay)
            
        elif choice == "2":
            messages = [
                "สวัสดีครับ! 👋",
                "วันนี้เป็นยังไงบ้าง? 😊",
                "มีอะไรน่าสนใจไหม? 🤔",
                "ขอให้มีความสุขนะครับ! 💕"
            ]
            
            minutes = int(input("ช่วงเวลาระหว่างข้อความ (นาที, default: 1): ") or "1")
            await bomber.send_scheduled_messages(target, messages, schedule_minutes=minutes)
        
        # บันทึกข้อมูล session
        await bomber.save_session_info()
    
    await bomber.client.disconnect()
    print("👋 ขอบคุณที่ใช้งาน Telegram Bomber!")

# รันโปรแกรม
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ หยุดการทำงานโดยผู้ใช้")
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        logging.error(f"Main error: {e}")
