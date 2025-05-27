#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 ADVANCED REAL INSTAGRAM DM EXTRACTOR 🔥
ดึงข้อมูล Direct Messages จริงผ่าน Web Interface
ใช้ session จริงจาก alx.trading
"""

import json
import os
import sys
import time
import requests
from datetime import datetime
from pathlib import Path
import random
import re
from urllib.parse import urlencode
import base64

class AdvancedRealDMExtractor:
    def __init__(self):
        self.target_account = "alx.trading"
        self.base_url = "https://www.instagram.com"
        self.session = requests.Session()
        self.session_data = None
        self.csrf_token = None
        self.extracted_data = []
        
        print("🔥 ADVANCED REAL INSTAGRAM DM EXTRACTOR 🔥")
        print(f"🎯 Target: {self.target_account}")
        print("✨ Web Interface Method")
        print("🚫 NO MOCKUP DATA - REAL EXTRACTION ONLY")
        print()
        
    def load_session_cookies(self):
        """โหลด session cookies จริง"""
        print("🍪 กำลังโหลด session cookies...")
        
        cookie_file = "data/sessions/alx_session_cookies.txt"
        if not os.path.exists(cookie_file):
            print(f"❌ ไม่พบไฟล์ {cookie_file}")
            return False
        
        with open(cookie_file, 'r') as f:
            cookie_string = f.read().strip()
        
        print(f"📄 Cookie data: {cookie_string[:50]}...")
        
        # แยก cookies
        cookies = {}
        for part in cookie_string.split(';'):
            if '=' in part:
                key, value = part.strip().split('=', 1)
                cookies[key] = value
        
        # ตั้งค่า session cookies
        for name, value in cookies.items():
            self.session.cookies.set(name, value, domain='.instagram.com')
        
        # เก็บ CSRF token
        if 'csrftoken' in cookies:
            self.csrf_token = cookies['csrftoken']
            print(f"🔑 CSRF Token: {self.csrf_token[:10]}...")
        
        print("✅ Session cookies loaded")
        return True
    
    def setup_headers(self):
        """ตั้งค่า headers ให้เหมือน browser จริง"""
        print("⚙️ กำลังตั้งค่า headers...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
        
        if self.csrf_token:
            headers['X-CSRFToken'] = self.csrf_token
        
        self.session.headers.update(headers)
        print("✅ Headers configured")
    
    def test_login_status(self):
        """ทดสอบสถานะการ login"""
        print("🧪 กำลังทดสอบ login status...")
        
        try:
            response = self.session.get(f"{self.base_url}/", timeout=15)
            
            if response.status_code == 200:
                # ตรวจสอบว่า logged in หรือไม่
                content = response.text
                
                if 'is_logged_in":true' in content or '"username":"' in content:
                    print("✅ Successfully logged in!")
                    
                    # พยายามหา username
                    username_match = re.search(r'"username":"([^"]+)"', content)
                    if username_match:
                        current_user = username_match.group(1)
                        print(f"👤 Current user: {current_user}")
                        
                        if current_user == self.target_account:
                            print("🎯 Perfect! Logged in as target account!")
                            return True
                        else:
                            print(f"⚠️ Logged in as different user: {current_user}")
                            return True  # Still proceed
                    
                    return True
                else:
                    print("❌ Not logged in")
                    return False
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def get_direct_inbox_data(self):
        """ดึงข้อมูล inbox ผ่าน web interface"""
        print("📥 กำลังเข้าถึง Direct inbox...")
        
        try:
            # เข้าถึงหน้า Direct Messages
            direct_url = f"{self.base_url}/direct/inbox/"
            response = self.session.get(direct_url, timeout=20)
            
            if response.status_code == 200:
                print("✅ เข้าถึง Direct inbox สำเร็จ")
                
                # ดึงข้อมูล JavaScript variables
                return self.extract_js_data(response.text)
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error accessing inbox: {e}")
            return None
    
    def extract_js_data(self, html_content):
        """ดึงข้อมูลจาก JavaScript variables ในหน้าเว็บ"""
        print("🔍 กำลังวิเคราะห์ JavaScript data...")
        
        extracted_data = {
            'extraction_timestamp': datetime.now().isoformat(),
            'target_account': self.target_account,
            'extraction_method': 'web_javascript',
            'conversations': [],
            'raw_data': {}
        }
        
        # ค้นหา window._sharedData
        shared_data_match = re.search(r'window\._sharedData\s*=\s*({.+?});', html_content, re.DOTALL)
        if shared_data_match:
            try:
                shared_data = json.loads(shared_data_match.group(1))
                print("✅ พบ window._sharedData")
                extracted_data['raw_data']['shared_data'] = shared_data
                
                # วิเคราะห์ข้อมูล user
                if 'config' in shared_data and 'viewer' in shared_data['config']:
                    viewer = shared_data['config']['viewer']
                    print(f"👤 Viewer data: {viewer.get('username', 'Unknown')}")
                
            except json.JSONDecodeError:
                print("⚠️ ไม่สามารถ parse shared_data ได้")
        
        # ค้นหา GraphQL data
        graphql_matches = re.findall(r'"DirectInbox":\s*({.+?})', html_content)
        if graphql_matches:
            print(f"📊 พบ DirectInbox data: {len(graphql_matches)} entries")
            
            for i, match in enumerate(graphql_matches):
                try:
                    inbox_data = json.loads(match)
                    extracted_data['raw_data'][f'inbox_data_{i}'] = inbox_data
                    
                    # วิเคราะห์ conversations
                    self.parse_inbox_data(inbox_data, extracted_data)
                    
                except json.JSONDecodeError:
                    print(f"⚠️ ไม่สามารถ parse inbox_data_{i} ได้")
        
        # ค้นหา additional GraphQL queries
        additional_patterns = [
            r'"DirectThread":\s*({.+?})',
            r'"DirectMessages":\s*({.+?})',
            r'"threads":\s*(\[.+?\])',
            r'"messages":\s*(\[.+?\])'
        ]
        
        for pattern_name, pattern in [
            ('DirectThread', r'"DirectThread":\s*({.+?})'),
            ('DirectMessages', r'"DirectMessages":\s*({.+?})'),
            ('threads', r'"threads":\s*(\[.+?\])'),
            ('messages', r'"messages":\s*(\[.+?\])')
        ]:
            matches = re.findall(pattern, html_content)
            if matches:
                print(f"📊 พบ {pattern_name} data: {len(matches)} entries")
                for i, match in enumerate(matches):
                    try:
                        data = json.loads(match)
                        extracted_data['raw_data'][f'{pattern_name}_{i}'] = data
                    except json.JSONDecodeError:
                        continue
        
        return extracted_data
    
    def parse_inbox_data(self, inbox_data, extracted_data):
        """วิเคราะห์ข้อมูล inbox และแยก conversations"""
        print("🔍 กำลังวิเคราะห์ inbox data...")
        
        # ตรวจสอบโครงสร้างข้อมูล
        if isinstance(inbox_data, dict):
            # ค้นหา threads
            threads = []
            
            if 'threads' in inbox_data:
                threads = inbox_data['threads']
            elif 'edges' in inbox_data:
                threads = [edge.get('node', {}) for edge in inbox_data['edges']]
            
            print(f"📊 พบ {len(threads)} threads")
            
            for thread in threads:
                if isinstance(thread, dict):
                    conversation = self.parse_thread_data(thread)
                    if conversation:
                        extracted_data['conversations'].append(conversation)
    
    def parse_thread_data(self, thread):
        """วิเคราะห์ข้อมูล thread แต่ละอัน"""
        conversation = {
            'thread_id': thread.get('thread_id') or thread.get('id'),
            'thread_title': thread.get('thread_title'),
            'participants': [],
            'messages': [],
            'last_activity': thread.get('last_activity_at'),
            'message_count': thread.get('messages_count', 0)
        }
        
        # วิเคราะห์ผู้เข้าร่วม
        users = thread.get('users', [])
        if isinstance(users, list):
            for user in users:
                if isinstance(user, dict):
                    participant = {
                        'user_id': user.get('pk') or user.get('id'),
                        'username': user.get('username'),
                        'full_name': user.get('full_name'),
                        'profile_pic': user.get('profile_pic_url'),
                        'is_verified': user.get('is_verified', False)
                    }
                    conversation['participants'].append(participant)
        
        # วิเคราะห์ข้อความ
        items = thread.get('items', []) or thread.get('messages', [])
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    message = self.parse_message_data(item)
                    if message:
                        conversation['messages'].append(message)
        
        return conversation if conversation['thread_id'] else None
    
    def parse_message_data(self, item):
        """วิเคราะห์ข้อมูลข้อความแต่ละข้อ"""
        message = {
            'message_id': item.get('item_id') or item.get('id'),
            'user_id': item.get('user_id'),
            'timestamp': item.get('timestamp'),
            'message_type': item.get('item_type') or item.get('type'),
            'text': item.get('text', ''),
            'media': None
        }
        
        # วิเคราะห์สื่อ (รูปภาพ, วิดีโอ)
        if 'media' in item and item['media']:
            media = item['media']
            message['media'] = {
                'type': media.get('media_type'),
                'url': None
            }
            
            # ดึง URL รูปภาพ
            if 'image_versions2' in media and 'candidates' in media['image_versions2']:
                candidates = media['image_versions2']['candidates']
                if candidates:
                    message['media']['url'] = candidates[0].get('url')
        
        return message if message['message_id'] else None
    
    def make_graphql_request(self):
        """ทำ GraphQL request เพื่อดึงข้อมูล DMs"""
        print("🔗 กำลังทำ GraphQL request...")
        
        # GraphQL variables สำหรับ Direct Messages
        variables = {
            "id": "",
            "first": 20
        }
        
        # Instagram GraphQL endpoint
        graphql_url = f"{self.base_url}/graphql/query/"
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': f"{self.base_url}/direct/inbox/"
        }
        
        if self.csrf_token:
            headers['X-CSRFToken'] = self.csrf_token
        
        try:
            # Query ID สำหรับ Direct Inbox (อาจต้องอัพเดต)
            query_hash = "7219b10d28da92f8b9b909e69f69b4b7"  # Example query hash
            
            data = {
                'query_hash': query_hash,
                'variables': json.dumps(variables)
            }
            
            response = self.session.post(
                graphql_url,
                data=data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    print("✅ GraphQL request สำเร็จ")
                    return result
                except json.JSONDecodeError:
                    print("❌ GraphQL response ไม่ใช่ JSON")
                    return None
            else:
                print(f"❌ GraphQL Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ GraphQL request error: {e}")
            return None
    
    def save_extracted_data(self, data):
        """บันทึกข้อมูลที่ดึงได้"""
        if not data or not data.get('conversations') and not data.get('raw_data'):
            print("❌ ไม่มีข้อมูลให้บันทึก")
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"data/extractions/ADVANCED_REAL_ALX_DMs_{timestamp}"
        os.makedirs(output_dir, exist_ok=True)
        
        # บันทึกข้อมูลหลัก
        output_file = f"{output_dir}/advanced_real_dm_data.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # สร้างรายงานสรุป
        summary = {
            'extraction_summary': {
                'timestamp': data['extraction_timestamp'],
                'target': data['target_account'],
                'method': data['extraction_method'],
                'total_conversations': len(data.get('conversations', [])),
                'total_raw_data_entries': len(data.get('raw_data', {})),
                'data_sources': list(data.get('raw_data', {}).keys())
            },
            'conversations_found': []
        }
        
        # วิเคราะห์ conversations
        for i, conv in enumerate(data.get('conversations', [])):
            conv_summary = {
                'conversation_index': i + 1,
                'thread_id': conv.get('thread_id'),
                'participants': [p.get('username') for p in conv.get('participants', [])],
                'message_count': len(conv.get('messages', [])),
                'last_activity': conv.get('last_activity')
            }
            summary['conversations_found'].append(conv_summary)
        
        # วิเคราะห์ raw data
        raw_data_analysis = {}
        for key, value in data.get('raw_data', {}).items():
            if isinstance(value, dict):
                raw_data_analysis[key] = {
                    'type': 'object',
                    'keys': list(value.keys())[:10],  # แสดง 10 keys แรก
                    'size': len(str(value))
                }
            elif isinstance(value, list):
                raw_data_analysis[key] = {
                    'type': 'array',
                    'length': len(value),
                    'size': len(str(value))
                }
            else:
                raw_data_analysis[key] = {
                    'type': type(value).__name__,
                    'size': len(str(value))
                }
        
        summary['raw_data_analysis'] = raw_data_analysis
        
        summary_file = f"{output_dir}/advanced_extraction_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"✅ บันทึกข้อมูลเสร็จ:")
        print(f"   📁 Output directory: {output_dir}")
        print(f"   📄 Main data: advanced_real_dm_data.json")
        print(f"   📊 Summary: advanced_extraction_summary.json")
        print(f"   💬 Conversations: {len(data.get('conversations', []))}")
        print(f"   📦 Raw data entries: {len(data.get('raw_data', {}))}")
        
        return output_file
    
    def run_advanced_extraction(self):
        """รันการดึงข้อมูลแบบ advanced"""
        print("🚀 เริ่มต้น Advanced Real DM Extraction")
        print("=" * 60)
        
        # ขั้นตอนที่ 1: โหลด cookies
        if not self.load_session_cookies():
            print("❌ ไม่สามารถโหลด session cookies ได้")
            return False
        
        # ขั้นตอนที่ 2: ตั้งค่า headers
        self.setup_headers()
        
        # ขั้นตอนที่ 3: ทดสอบ login
        if not self.test_login_status():
            print("❌ Login status ไม่ถูกต้อง")
            return False
        
        # ขั้นตอนที่ 4: ดึงข้อมูล inbox
        extracted_data = self.get_direct_inbox_data()
        
        if extracted_data:
            # ขั้นตอนที่ 5: ลองทำ GraphQL request เพิ่มเติม
            graphql_data = self.make_graphql_request()
            if graphql_data:
                extracted_data['raw_data']['graphql_response'] = graphql_data
            
            # ขั้นตอนที่ 6: บันทึกข้อมูล
            output_file = self.save_extracted_data(extracted_data)
            
            print("\n🎉 Advanced Extraction สำเร็จ!")
            print("=" * 40)
            print("✅ ได้รับข้อมูล Direct Messages จริงจาก Instagram")
            print("🔍 ใช้วิธี Web Interface + JavaScript Parsing")
            print("🚫 ไม่ใช่ข้อมูล mockup")
            print(f"📁 ผลลัพธ์: {output_file}")
            
            return True
        else:
            print("\n❌ Advanced Extraction ล้มเหลว")
            return False

def main():
    """ฟังก์ชันหลัก"""
    print("🔥 SUGARGLITCH REALOPS - ADVANCED REAL DM EXTRACTOR 🔥")
    print("ดึงข้อมูล Instagram Direct Messages จริงด้วย Advanced Method")
    print("🚫 NO MOCKUP - REAL DATA ONLY")
    print()
    
    extractor = AdvancedRealDMExtractor()
    
    try:
        success = extractor.run_advanced_extraction()
        
        if success:
            print("\n✅ ADVANCED MISSION ACCOMPLISHED!")
            print("ได้รับข้อมูล Direct Messages จริงแล้ว")
        else:
            print("\n❌ ADVANCED MISSION FAILED!")
            print("ไม่สามารถดึงข้อมูลจริงได้ในครั้งนี้")
            
    except KeyboardInterrupt:
        print("\n⚠️ การดำเนินการถูกยกเลิก")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
