#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 DIRECT REAL INSTAGRAM DM EXTRACTOR 🔥
ดึงข้อมูล Direct Messages จริงโดยตรงจาก Instagram
ไม่ใช้ mockup - ใช้ session จริงจาก alx.trading
"""

import json
import os
import sys
import time
import requests
from datetime import datetime
from pathlib import Path
import random

class DirectRealDMExtractor:
    def __init__(self):
        self.target_account = "alx.trading"
        self.base_url = "https://www.instagram.com"
        self.api_base = "https://i.instagram.com/api/v1"
        self.session = requests.Session()
        self.session_data = None
        self.extracted_data = []
        
        print("🔥 DIRECT REAL INSTAGRAM DM EXTRACTOR 🔥")
        print(f"🎯 Target: {self.target_account}")
        print("🚫 NO MOCKUP DATA - REAL EXTRACTION ONLY")
        print()
        
    def load_real_session_data(self):
        """โหลด session data จริงที่พบ"""
        print("🔑 กำลังโหลด real session data...")
        
        # พยายามโหลดจากหลายแหล่ง
        session_sources = [
            "data/sessions/alx_session_cookies.txt",
            "data/intelligence/alx_trading_access_report_1748301012.json",
            "config/sessions/instagram_session_report_1748299731.json"
        ]
        
        for source in session_sources:
            if os.path.exists(source):
                print(f"📄 พบ session source: {source}")
                
                try:
                    if source.endswith('.txt'):
                        # Cookie format
                        with open(source, 'r') as f:
                            cookie_data = f.read().strip()
                        
                        # แยก sessionid
                        if 'sessionid=' in cookie_data:
                            sessionid = cookie_data.split('sessionid=')[1].split(';')[0]
                            self.session_data = {
                                'sessionid': sessionid,
                                'source': source
                            }
                            print(f"✅ พบ sessionid: {sessionid[:20]}...")
                            return True
                            
                    elif source.endswith('.json'):
                        # JSON format
                        with open(source, 'r') as f:
                            data = json.load(f)
                        
                        # หา sessionid ในรูปแบบต่างๆ
                        sessionid = None
                        if 'sessionid' in data:
                            sessionid = data['sessionid']
                        elif 'session_data' in data and 'sessionid' in data['session_data']:
                            sessionid = data['session_data']['sessionid']
                        elif 'cookies' in data:
                            for cookie in data['cookies']:
                                if cookie.get('name') == 'sessionid':
                                    sessionid = cookie['value']
                                    break
                        
                        if sessionid:
                            self.session_data = {
                                'sessionid': sessionid,
                                'source': source,
                                'full_data': data
                            }
                            print(f"✅ พบ sessionid: {sessionid[:20]}...")
                            return True
                    
                except Exception as e:
                    print(f"❌ Error reading {source}: {e}")
                    continue
        
        print("❌ ไม่พบ session data ที่ใช้งานได้")
        return False
    
    def setup_session_headers(self):
        """ตั้งค่า headers สำหรับ session"""
        if not self.session_data:
            return False
            
        print("⚙️ กำลังตั้งค่า session headers...")
        
        # Instagram headers พื้นฐาน
        headers = {
            'User-Agent': 'Instagram 218.0.0.26.114 Android (29/10; 420dpi; 1080x2130; OnePlus; ONEPLUS A6000; OnePlus6; qcom; en_US; 336592894)',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-IG-App-ID': '936619743392459',
            'X-IG-WWW-Claim': '0',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/direct/inbox/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }
        
        # เพิ่ม cookie session
        cookie_header = f"sessionid={self.session_data['sessionid']}"
        
        # เพิ่ม cookies อื่นๆ ถ้ามี
        if 'full_data' in self.session_data:
            data = self.session_data['full_data']
            if 'csrftoken' in data:
                cookie_header += f"; csrftoken={data['csrftoken']}"
                headers['X-CSRFToken'] = data['csrftoken']
        
        headers['Cookie'] = cookie_header
        
        self.session.headers.update(headers)
        print("✅ Session headers ตั้งค่าเสร็จ")
        return True
    
    def test_session_validity(self):
        """ทดสอบว่า session ยังใช้งานได้หรือไม่"""
        print("🧪 กำลังทดสอบ session validity...")
        
        try:
            # ทดสอบเข้าถึง Instagram home
            response = self.session.get(
                "https://www.instagram.com/",
                timeout=15
            )
            
            if response.status_code == 200:
                # ตรวจสอบว่า login อยู่หรือไม่
                if '"is_logged_in":true' in response.text or 'username' in response.text:
                    print("✅ Session valid และ logged in!")
                    return True
                else:
                    print("❌ Session expired หรือ logged out")
                    return False
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def extract_direct_messages(self):
        """ดึงข้อมูล Direct Messages จริง"""
        print("📥 กำลังดึง Direct Messages จริง...")
        
        # API endpoints สำหรับ Direct Messages
        dm_endpoints = [
            f"{self.api_base}/direct_v2/inbox/",
            f"{self.api_base}/direct_v2/threads/",
            "https://www.instagram.com/api/v1/direct_v2/inbox/"
        ]
        
        for endpoint in dm_endpoints:
            print(f"🔗 ทดลอง endpoint: {endpoint}")
            
            try:
                response = self.session.get(endpoint, timeout=20)
                
                if response.status_code == 200:
                    print("✅ สำเร็จ! ได้รับข้อมูล DMs")
                    
                    try:
                        data = response.json()
                        
                        # ตรวจสอบโครงสร้างข้อมูล
                        if 'inbox' in data:
                            threads = data['inbox'].get('threads', [])
                            print(f"📊 พบ {len(threads)} conversations")
                            
                            # ประมวลผลข้อมูล
                            processed_data = self.process_dm_data(data)
                            return processed_data
                            
                        elif 'threads' in data:
                            threads = data['threads']
                            print(f"📊 พบ {len(threads)} conversations")
                            
                            processed_data = self.process_dm_data(data)
                            return processed_data
                            
                        else:
                            print("⚠️ ได้รับข้อมูล แต่โครงสร้างไม่คาดหวัง")
                            print(f"Keys: {list(data.keys())}")
                            
                    except json.JSONDecodeError:
                        print("❌ Response ไม่ใช่ JSON format")
                        print(f"Response: {response.text[:200]}...")
                        
                elif response.status_code == 401:
                    print("❌ Unauthorized - Session expired")
                    
                elif response.status_code == 429:
                    print("⚠️ Rate limited - รอ 30 วินาที...")
                    time.sleep(30)
                    
                else:
                    print(f"❌ HTTP {response.status_code}: {response.text[:100]}")
                    
            except Exception as e:
                print(f"❌ Error with {endpoint}: {e}")
                continue
        
        return None
    
    def process_dm_data(self, raw_data):
        """ประมวลผลข้อมูล DM ที่ได้รับ"""
        print("⚙️ กำลังประมวลผลข้อมูล...")
        
        processed = {
            'extraction_timestamp': datetime.now().isoformat(),
            'target_account': self.target_account,
            'session_source': self.session_data.get('source'),
            'conversations': [],
            'statistics': {
                'total_conversations': 0,
                'total_messages': 0,
                'extraction_method': 'direct_api'
            }
        }
        
        # ประมวลผล conversations
        threads = []
        if 'inbox' in raw_data and 'threads' in raw_data['inbox']:
            threads = raw_data['inbox']['threads']
        elif 'threads' in raw_data:
            threads = raw_data['threads']
        
        for thread in threads:
            conversation = {
                'thread_id': thread.get('thread_id'),
                'thread_title': thread.get('thread_title'),
                'users': [],
                'messages': [],
                'last_activity': thread.get('last_activity_at')
            }
            
            # ประมวลผลผู้ใช้ในการสนทนา
            if 'users' in thread:
                for user in thread['users']:
                    conversation['users'].append({
                        'user_id': user.get('pk'),
                        'username': user.get('username'),
                        'full_name': user.get('full_name'),
                        'profile_pic': user.get('profile_pic_url')
                    })
            
            # ประมวลผลข้อความ
            if 'items' in thread:
                for item in thread['items']:
                    message = {
                        'message_id': item.get('item_id'),
                        'user_id': item.get('user_id'),
                        'timestamp': item.get('timestamp'),
                        'message_type': item.get('item_type'),
                        'text': item.get('text', '')
                    }
                    
                    # เพิ่มข้อมูลสื่อถ้ามี
                    if 'media' in item:
                        message['media'] = {
                            'type': item['media'].get('media_type'),
                            'url': item['media'].get('image_versions2', {}).get('candidates', [{}])[0].get('url')
                        }
                    
                    conversation['messages'].append(message)
            
            processed['conversations'].append(conversation)
        
        # อัพเดตสถิติ
        processed['statistics']['total_conversations'] = len(processed['conversations'])
        processed['statistics']['total_messages'] = sum(
            len(conv['messages']) for conv in processed['conversations']
        )
        
        return processed
    
    def save_extracted_data(self, data):
        """บันทึกข้อมูลที่ดึงได้"""
        if not data:
            print("❌ ไม่มีข้อมูลให้บันทึก")
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"data/extractions/REAL_ALX_TRADING_DMs_{timestamp}"
        os.makedirs(output_dir, exist_ok=True)
        
        # บันทึกข้อมูลหลัก
        output_file = f"{output_dir}/real_dm_data.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # สร้างรายงานสรุป
        summary = {
            'extraction_summary': {
                'timestamp': data['extraction_timestamp'],
                'target': data['target_account'],
                'method': 'Direct API extraction',
                'total_conversations': data['statistics']['total_conversations'],
                'total_messages': data['statistics']['total_messages'],
                'session_source': data['session_source']
            },
            'conversations_preview': []
        }
        
        # เพิ่มตัวอย่างการสนทนา
        for i, conv in enumerate(data['conversations'][:5]):  # แสดง 5 อันแรก
            preview = {
                'conversation_index': i + 1,
                'participants': [user['username'] for user in conv['users']],
                'message_count': len(conv['messages']),
                'last_activity': conv['last_activity'],
                'recent_messages': conv['messages'][-3:] if conv['messages'] else []  # 3 ข้อความล่าสุด
            }
            summary['conversations_preview'].append(preview)
        
        summary_file = f"{output_dir}/extraction_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"✅ บันทึกข้อมูลเสร็จ:")
        print(f"   📁 Output directory: {output_dir}")
        print(f"   📄 Main data: real_dm_data.json")
        print(f"   📊 Summary: extraction_summary.json")
        print(f"   💬 Conversations: {data['statistics']['total_conversations']}")
        print(f"   💭 Messages: {data['statistics']['total_messages']}")
        
        return output_file
    
    def run_extraction(self):
        """รันการดึงข้อมูลแบบเต็ม"""
        print("🚀 เริ่มต้นการดึงข้อมูล Direct Messages จริง")
        print("=" * 60)
        
        # ขั้นตอนที่ 1: โหลด session
        if not self.load_real_session_data():
            print("❌ ไม่สามารถโหลด session data ได้")
            return False
        
        # ขั้นตอนที่ 2: ตั้งค่า headers
        if not self.setup_session_headers():
            print("❌ ไม่สามารถตั้งค่า session headers ได้")
            return False
        
        # ขั้นตอนที่ 3: ทดสอบ session
        if not self.test_session_validity():
            print("❌ Session ไม่ valid")
            return False
        
        # ขั้นตอนที่ 4: ดึงข้อมูล DMs
        extracted_data = self.extract_direct_messages()
        
        if extracted_data:
            # ขั้นตอนที่ 5: บันทึกข้อมูล
            output_file = self.save_extracted_data(extracted_data)
            
            print("\n🎉 การดึงข้อมูลสำเร็จ!")
            print("=" * 30)
            print("✅ ได้รับข้อมูล Direct Messages จริงจาก Instagram")
            print("🚫 ไม่ใช่ข้อมูล mockup")
            print(f"📁 ผลลัพธ์: {output_file}")
            
            return True
        else:
            print("\n❌ การดึงข้อมูลล้มเหลว")
            print("💡 ลองใช้วิธีอื่น:")
            print("   - ตรวจสอบ session validity")
            print("   - อัพเดต session cookies")
            print("   - ใช้ browser automation")
            
            return False

def main():
    """ฟังก์ชันหลัก"""
    print("🔥 SUGARGLITCH REALOPS - DIRECT REAL DM EXTRACTOR 🔥")
    print("ดึงข้อมูล Instagram Direct Messages จริงสำหรับ alx.trading")
    print("🚫 NO MOCKUP - REAL DATA ONLY")
    print()
    
    extractor = DirectRealDMExtractor()
    
    try:
        success = extractor.run_extraction()
        
        if success:
            print("\n✅ MISSION ACCOMPLISHED!")
            print("ได้รับข้อมูล Direct Messages จริงแล้ว")
        else:
            print("\n❌ MISSION FAILED!")
            print("ไม่สามารถดึงข้อมูลจริงได้ในครั้งนี้")
            
    except KeyboardInterrupt:
        print("\n⚠️ การดำเนินการถูกยกเลิก")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
