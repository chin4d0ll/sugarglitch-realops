#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 Telegram Group Member Scraper
ระบบดึงข้อมูลสมาชิกกลุ่ม Telegram อย่างละเอียด

✨ Features:
- ดึงข้อมูลสมาชิกจากกลุ่ม/ช่อง
- บันทึกเป็น CSV, JSON, Excel
- วิเคราะห์ข้อมูลเบื้องต้น
- กรองข้อมูลตามเงื่อนไข
"""

import asyncio
from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest, GetFullChannelRequest
from telethon.tl.types import ChannelParticipantsSearch, ChannelParticipantsAdmins, ChannelParticipantsBanned
from telethon.errors import FloodWaitError, ChannelPrivateError
import csv
import json
import pandas as pd
from datetime import datetime
import logging
import os

# ตั้งค่า logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_scraper.log'),
        logging.StreamHandler()
    ]
)

class TelegramScraper:
    def __init__(self, api_id, api_hash, phone):
        """
        สร้าง Telegram scraper
        
        Args:
            api_id (str): API ID จาก my.telegram.org
            api_hash (str): API Hash จาก my.telegram.org
            phone (str): เบอร์โทรศัพท์
        """
        self.client = TelegramClient('scraper_session', api_id, api_hash)
        self.phone = phone
        self.scraped_data = []
        
    async def connect(self):
        """เชื่อมต่อกับ Telegram API"""
        try:
            await self.client.start(phone=self.phone)
            me = await self.client.get_me()
            print(f"🔗 เชื่อมต่อสำเร็จ! ผู้ใช้: {me.first_name}")
            logging.info(f"Connected as {me.username or me.first_name}")
            return True
        except Exception as e:
            print(f"❌ เชื่อมต่อไม่ได้: {e}")
            logging.error(f"Connection failed: {e}")
            return False
        
    async def get_group_info(self, group_username):
        """ดึงข้อมูลกลุ่มเบื้องต้น"""
        try:
            if not group_username.startswith('@'):
                group_username = f'@{group_username}'
                
            group = await self.client.get_entity(group_username)
            full_group = await self.client(GetFullChannelRequest(group))
            
            info = {
                'id': group.id,
                'title': group.title,
                'username': group.username,
                'members_count': full_group.full_chat.participants_count,
                'description': full_group.full_chat.about,
                'created_date': group.date.isoformat() if group.date else None,
                'is_megagroup': getattr(group, 'megagroup', False),
                'is_broadcast': getattr(group, 'broadcast', False)
            }
            
            print(f"📊 ข้อมูลกลุ่ม: {info['title']}")
            print(f"👥 สมาชิก: {info['members_count']:,} คน")
            print(f"📝 คำอธิบาย: {(info['description'] or 'ไม่มี')[:100]}...")
            
            return info
            
        except Exception as e:
            print(f"❌ ดึงข้อมูลกลุ่มไม่ได้: {e}")
            return None
        
    async def scrape_group_members(self, group_username, limit=1000, include_admins=True, include_banned=False):
        """
        ดึงข้อมูลสมาชิกกลุ่ม
        
        Args:
            group_username (str): ชื่อกลุ่ม (@groupname)
            limit (int): จำนวนสมาชิกที่จะดึง
            include_admins (bool): รวมข้อมูล admin
            include_banned (bool): รวมข้อมูล banned users
        """
        try:
            if not group_username.startswith('@'):
                group_username = f'@{group_username}'
                
            # เข้าร่วมกลุ่ม (ถ้ายังไม่ได้เข้า)
            group = await self.client.get_entity(group_username)
            
            print(f"📊 กำลังดึงข้อมูลจากกลุ่ม: {group.title}")
            
            all_participants = []
            offset = 0
            batch_size = 200
            
            # ดึงสมาชิกทั่วไป
            while len(all_participants) < limit:
                try:
                    # ดึงสมาชิกทีละ batch
                    participants = await self.client(GetParticipantsRequest(
                        group,
                        ChannelParticipantsSearch(''),
                        offset,
                        batch_size,
                        hash=0
                    ))
                    
                    if not participants.users:
                        break
                        
                    all_participants.extend(participants.users)
                    offset += len(participants.users)
                    
                    print(f"📥 ดึงข้อมูลแล้ว {len(all_participants)} คน...")
                    
                    # หน่วงเวลาเล็กน้อย
                    await asyncio.sleep(1)
                    
                except FloodWaitError as e:
                    print(f"⏳ ต้องรอ {e.seconds} วินาที")
                    await asyncio.sleep(e.seconds)
                    
                except Exception as e:
                    print(f"⚠️ Error ในการดึงข้อมูล: {e}")
                    break
            
            # ดึงข้อมูล admin (ถ้าต้องการ)
            admins = []
            if include_admins:
                try:
                    admin_participants = await self.client(GetParticipantsRequest(
                        group,
                        ChannelParticipantsAdmins(),
                        0,
                        100,
                        hash=0
                    ))
                    admins = admin_participants.users
                    print(f"👑 พบ admin {len(admins)} คน")
                except Exception as e:
                    print(f"⚠️ ดึงข้อมูล admin ไม่ได้: {e}")
            
            # ดึงข้อมูล banned users (ถ้าต้องการ)
            banned = []
            if include_banned:
                try:
                    banned_participants = await self.client(GetParticipantsRequest(
                        group,
                        ChannelParticipantsBanned(),
                        0,
                        100,
                        hash=0
                    ))
                    banned = banned_participants.users
                    print(f"🚫 พบ banned users {len(banned)} คน")
                except Exception as e:
                    print(f"⚠️ ดึงข้อมูล banned users ไม่ได้: {e}")
            
            # จัดรูปแบบข้อมูล
            members_data = []
            admin_ids = {admin.id for admin in admins}
            banned_ids = {user.id for user in banned}
            
            for user in all_participants[:limit]:
                # ดึงข้อมูลสถานะออนไลน์
                status = self._parse_user_status(user.status)
                
                member_info = {
                    'id': user.id,
                    'username': user.username or 'None',
                    'first_name': user.first_name or 'None',
                    'last_name': user.last_name or 'None',
                    'phone': user.phone or 'None',
                    'is_bot': user.bot or False,
                    'is_admin': user.id in admin_ids,
                    'is_banned': user.id in banned_ids,
                    'status': status['status'],
                    'last_seen': status['last_seen'],
                    'is_premium': getattr(user, 'premium', False),
                    'is_verified': getattr(user, 'verified', False),
                    'is_restricted': getattr(user, 'restricted', False),
                    'is_scam': getattr(user, 'scam', False),
                    'is_fake': getattr(user, 'fake', False),
                    'scraped_at': datetime.now().isoformat()
                }
                members_data.append(member_info)
            
            self.scraped_data = members_data
            print(f"✅ ดึงข้อมูลสำเร็จ {len(members_data)} คน!")
            
            # แสดงสถิติ
            await self._show_member_stats(members_data)
            
            return members_data
            
        except ChannelPrivateError:
            print("❌ กลุ่มเป็น private หรือคุณไม่ได้เป็นสมาชิก")
            return []
        except Exception as e:
            print(f"❌ Error: {e}")
            logging.error(f"Scraping error: {e}")
            return []
    
    def _parse_user_status(self, status):
        """แปลงสถานะผู้ใช้เป็นข้อมูลที่อ่านได้"""
        if not status:
            return {'status': 'Unknown', 'last_seen': None}
            
        status_name = status.__class__.__name__
        
        if status_name == 'UserStatusOnline':
            return {'status': 'Online', 'last_seen': 'Currently online'}
        elif status_name == 'UserStatusOffline':
            last_seen = status.was_online.isoformat() if status.was_online else None
            return {'status': 'Offline', 'last_seen': last_seen}
        elif status_name == 'UserStatusRecently':
            return {'status': 'Recently', 'last_seen': 'Recently active'}
        elif status_name == 'UserStatusLastWeek':
            return {'status': 'Last week', 'last_seen': 'Active last week'}
        elif status_name == 'UserStatusLastMonth':
            return {'status': 'Last month', 'last_seen': 'Active last month'}
        else:
            return {'status': status_name, 'last_seen': None}
    
    async def _show_member_stats(self, members_data):
        """แสดงสถิติสมาชิก"""
        if not members_data:
            return
            
        total = len(members_data)
        bots = sum(1 for m in members_data if m['is_bot'])
        admins = sum(1 for m in members_data if m['is_admin'])
        premium = sum(1 for m in members_data if m['is_premium'])
        verified = sum(1 for m in members_data if m['is_verified'])
        has_username = sum(1 for m in members_data if m['username'] != 'None')
        
        print("\n" + "="*50)
        print("📊 สถิติสมาชิก")
        print("="*50)
        print(f"👥 สมาชิกทั้งหมด: {total:,} คน")
        print(f"🤖 Bot: {bots:,} คน ({(bots/total)*100:.1f}%)")
        print(f"👑 Admin: {admins:,} คน ({(admins/total)*100:.1f}%)")
        print(f"⭐ Premium: {premium:,} คน ({(premium/total)*100:.1f}%)")
        print(f"✅ Verified: {verified:,} คน ({(verified/total)*100:.1f}%)")
        print(f"🏷️ มี Username: {has_username:,} คน ({(has_username/total)*100:.1f}%)")
        print("="*50)
    
    async def save_to_csv(self, data=None, filename=None):
        """บันทึกข้อมูลเป็นไฟล์ CSV"""
        if data is None:
            data = self.scraped_data
            
        if not data:
            print("❌ ไม่มีข้อมูลให้บันทึก")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'telegram_members_{timestamp}.csv'
            
        # สร้างโฟลเดอร์ถ้าไม่มี
        os.makedirs('scraped_data', exist_ok=True)
        filepath = os.path.join('scraped_data', filename)
            
        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            if data:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                writer.writeheader()
                writer.writerows(data)
                
        print(f"💾 บันทึกข้อมูลใน {filepath} แล้วค่ะ!")
        return filepath
    
    async def save_to_json(self, data=None, filename=None):
        """บันทึกข้อมูลเป็นไฟล์ JSON"""
        if data is None:
            data = self.scraped_data
            
        if not data:
            print("❌ ไม่มีข้อมูลให้บันทึก")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'telegram_members_{timestamp}.json'
        
        # สร้างโฟลเดอร์ถ้าไม่มี
        os.makedirs('scraped_data', exist_ok=True)
        filepath = os.path.join('scraped_data', filename)
            
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            
        print(f"💾 บันทึกข้อมูลใน {filepath} แล้วค่ะ!")
        return filepath
    
    async def save_to_excel(self, data=None, filename=None):
        """บันทึกข้อมูลเป็นไฟล์ Excel"""
        if data is None:
            data = self.scraped_data
            
        if not data:
            print("❌ ไม่มีข้อมูลให้บันทึก")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'telegram_members_{timestamp}.xlsx'
        
        try:
            # สร้างโฟลเดอร์ถ้าไม่มี
            os.makedirs('scraped_data', exist_ok=True)
            filepath = os.path.join('scraped_data', filename)
            
            df = pd.DataFrame(data)
            
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Members', index=False)
                
                # เพิ่มชีทสถิติ
                stats_data = self._generate_stats_data(data)
                stats_df = pd.DataFrame(stats_data)
                stats_df.to_excel(writer, sheet_name='Statistics', index=False)
                
            print(f"💾 บันทึกข้อมูลใน {filepath} แล้วค่ะ!")
            return filepath
            
        except ImportError:
            print("❌ ติดตั้ง pandas และ openpyxl ก่อน: pip install pandas openpyxl")
            return None
        except Exception as e:
            print(f"❌ บันทึก Excel ไม่ได้: {e}")
            return None
    
    def _generate_stats_data(self, data):
        """สร้างข้อมูลสถิติสำหรับ Excel"""
        if not data:
            return []
            
        total = len(data)
        stats = [
            {'Metric': 'Total Members', 'Count': total, 'Percentage': 100.0},
            {'Metric': 'Bots', 'Count': sum(1 for m in data if m['is_bot']), 'Percentage': 0},
            {'Metric': 'Admins', 'Count': sum(1 for m in data if m['is_admin']), 'Percentage': 0},
            {'Metric': 'Premium Users', 'Count': sum(1 for m in data if m['is_premium']), 'Percentage': 0},
            {'Metric': 'Verified Users', 'Count': sum(1 for m in data if m['is_verified']), 'Percentage': 0},
            {'Metric': 'Has Username', 'Count': sum(1 for m in data if m['username'] != 'None'), 'Percentage': 0},
        ]
        
        # คำนวณเปอร์เซ็นต์
        for stat in stats[1:]:
            stat['Percentage'] = (stat['Count'] / total) * 100 if total > 0 else 0
            
        return stats
    
    def filter_members(self, criteria):
        """กรองสมาชิกตามเงื่อนไข"""
        if not self.scraped_data:
            print("❌ ไม่มีข้อมูลให้กรอง")
            return []
            
        filtered = []
        for member in self.scraped_data:
            match = True
            
            for key, value in criteria.items():
                if key not in member:
                    continue
                    
                if isinstance(value, bool):
                    if member[key] != value:
                        match = False
                        break
                elif isinstance(value, str):
                    if value.lower() not in str(member[key]).lower():
                        match = False
                        break
            
            if match:
                filtered.append(member)
        
        print(f"🔍 กรองเจอ {len(filtered)} คนจากทั้งหมด {len(self.scraped_data)} คน")
        return filtered

# วิธีใช้งาน
async def main():
    print("📊 Telegram Group Member Scraper")
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
    
    scraper = TelegramScraper(API_ID, API_HASH, PHONE)
    
    if await scraper.connect():
        # ดึงข้อมูลจากกลุ่ม
        group_username = input("ใส่ username กลุ่ม (เช่น @group_name): ").strip()
        if not group_username:
            print("❌ กรุณาใส่ username กลุ่ม")
            return
        
        # ดูข้อมูลกลุ่มก่อน
        group_info = await scraper.get_group_info(group_username)
        if not group_info:
            return
        
        # ถามจำนวนสมาชิกที่จะดึง
        limit_input = input(f"จำนวนสมาชิกที่จะดึง (max: {group_info['members_count']}, default: 500): ")
        limit = int(limit_input) if limit_input.isdigit() else 500
        limit = min(limit, group_info['members_count'])
        
        print(f"\n🚀 เริ่มดึงข้อมูล {limit} คนจากกลุ่ม {group_info['title']}...")
        
        # ดึงข้อมูลสมาชิก
        members = await scraper.scrape_group_members(
            group_username, 
            limit=limit,
            include_admins=True,
            include_banned=False
        )
        
        if members:
            # บันทึกข้อมูลในทุกรูปแบบ
            print("\n💾 กำลังบันทึกข้อมูล...")
            await scraper.save_to_csv(members)
            await scraper.save_to_json(members)
            await scraper.save_to_excel(members)
            
            # ตัวอย่างการกรองข้อมูล
            print("\n🔍 ตัวอย่างการกรองข้อมูล:")
            
            # กรองเฉพาะ admin
            admins = scraper.filter_members({'is_admin': True})
            if admins:
                await scraper.save_to_json(admins, 'admins_only.json')
            
            # กรองเฉพาะ premium users
            premium_users = scraper.filter_members({'is_premium': True})
            if premium_users:
                await scraper.save_to_json(premium_users, 'premium_users.json')
            
            # กรองเฉพาะที่มี username
            users_with_username = scraper.filter_members({'username': lambda x: x != 'None'})
            print(f"👤 ผู้ใช้ที่มี username: {len(users_with_username)} คน")
    
    await scraper.client.disconnect()
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
