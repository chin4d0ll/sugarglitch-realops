#!/usr/bin/env python3
"""
ALX Trading DM Extractor
Extracts all Direct Messages from alx.trading using Instagram Private API
"""

import json
import requests
import os
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin


class ALXTradingDMExtractor:
    """Instagram DM Extractor for ALX Trading"""
    
    def __init__(self, session_path: str = "tools/session_alx_trading.json"):
        """
        Initialize the extractor
        
        Args:
            session_path: Path to session JSON file
        """
        self.session_path = session_path
        self.session_data = None
        self.headers = {}
        self.cookies = {}
        self.base_url = "https://i.instagram.com/api/v1"
        self.extracted_data = {
            "extraction_info": {
                "timestamp": datetime.now().isoformat(),
                "target": "alx.trading",
                "total_threads": 0,
                "total_messages": 0
            },
            "threads": []
        }
        
    def setup_directories(self):
        """สร้างโฟลเดอร์ที่จำเป็น"""
        os.makedirs(self.output_dir, exist_ok=True)
        
    def load_session(self):
        """โหลด session จากไฟล์"""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    session_data = json.load(f)
                    self.session = session_data.get('cookies', {}).get('sessionid', '')
                    print(f"✅ Loaded session for {self.target_account}")
                    print(f"   Session: {self.session[:20]}...{self.session[-10:]}")
            else:
                print(f"❌ Session file not found: {self.session_file}")
                return False
        except Exception as e:
            print(f"❌ Error loading session: {e}")
            return False
        return True
    
    def setup_database(self):
        """สร้าง database สำหรับเก็บ DM"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dm_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id TEXT,
                message_id TEXT UNIQUE,
                sender TEXT,
                recipient TEXT,
                content TEXT,
                timestamp INTEGER,
                message_type TEXT,
                media_url TEXT,
                extracted_time TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dm_threads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id TEXT UNIQUE,
                participant_1 TEXT,
                participant_2 TEXT,
                thread_name TEXT,
                last_activity INTEGER,
                message_count INTEGER,
                extracted_time TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database setup completed")
    
    def test_session_validity(self):
        """ทดสอบว่า session ยังใช้งานได้หรือไม่"""
        print("\\n🧪 Testing session validity...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Cookie': f'sessionid={self.session}',
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        test_urls = [
            'https://www.instagram.com/',
            'https://www.instagram.com/direct/inbox/',
            'https://i.instagram.com/api/v1/direct_v2/inbox/'
        ]
        
        valid_session = False
        for url in test_urls:
            try:
                print(f"   Testing: {url}")
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    if 'login' not in response.url.lower():
                        print(f"   ✅ Valid - Status: {response.status_code}")
                        valid_session = True
                    else:
                        print(f"   ❌ Redirected to login")
                else:
                    print(f"   ⚠️ Status: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
                
            time.sleep(1)
            
        return valid_session
    
    def extract_dm_threads(self):
        """ดึงรายการ thread ทั้งหมด"""
        print("\\n📋 Extracting DM threads...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Cookie': f'sessionid={self.session}',
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': 'missing',
            'X-Instagram-AJAX': '1'
        }
        
        # ลองหลาย endpoint
        endpoints = [
            'https://i.instagram.com/api/v1/direct_v2/inbox/',
            'https://www.instagram.com/direct/inbox/',
            'https://i.instagram.com/api/v1/direct_v2/threads/'
        ]
        
        threads_data = []
        for endpoint in endpoints:
            try:
                print(f"   Trying endpoint: {endpoint}")
                response = requests.get(endpoint, headers=headers, timeout=15)
                
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if 'inbox' in data:
                            threads = data['inbox'].get('threads', [])
                            print(f"   ✅ Found {len(threads)} threads")
                            threads_data.extend(threads)
                        elif 'threads' in data:
                            threads = data['threads']
                            print(f"   ✅ Found {len(threads)} threads")
                            threads_data.extend(threads)
                    except json.JSONDecodeError:
                        print(f"   ⚠️ Response not JSON, length: {len(response.text)}")
                        # บันทึก HTML response สำหรับ debug
                        with open(f"{self.output_dir}/response_debug_{int(time.time())}.html", 'w') as f:
                            f.write(response.text)
                else:
                    print(f"   ❌ Failed: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
                
            time.sleep(2)
            
        return threads_data
    
    def extract_thread_messages(self, thread_id):
        """ดึงข้อความจาก thread เฉพาะ"""
        print(f"\\n💬 Extracting messages from thread: {thread_id}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Cookie': f'sessionid={self.session}',
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        url = f'https://i.instagram.com/api/v1/direct_v2/threads/{thread_id}/'
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                thread = data.get('thread', {})
                items = thread.get('items', [])
                print(f"   ✅ Found {len(items)} messages")
                return items
            else:
                print(f"   ❌ Failed: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return []
    
    def save_extracted_data(self, threads_data, messages_data):
        """บันทึกข้อมูลที่ดึงได้"""
        timestamp = int(time.time())
        
        # บันทึกเป็น JSON
        extraction_data = {
            "extraction_time": datetime.now().isoformat(),
            "target_account": self.target_account,
            "session_used": self.session[:20] + "..." + self.session[-10:],
            "threads_found": len(threads_data),
            "total_messages": sum(len(messages) for messages in messages_data.values()),
            "threads": threads_data,
            "messages": messages_data
        }
        
        json_file = f"{self.output_dir}/alx_trading_dms_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(extraction_data, f, indent=2, ensure_ascii=False)
            
        print(f"\\n✅ Data saved to: {json_file}")
        
        # บันทึกลง database
        self.save_to_database(threads_data, messages_data)
        
        return json_file
    
    def save_to_database(self, threads_data, messages_data):
        """บันทึกข้อมูลลง SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # บันทึก threads
        for thread in threads_data:
            thread_id = thread.get('thread_id', '')
            users = thread.get('users', [])
            participants = [user.get('username', '') for user in users]
            
            cursor.execute('''
                INSERT OR REPLACE INTO dm_threads 
                (thread_id, participant_1, participant_2, thread_name, last_activity, message_count, extracted_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                thread_id,
                participants[0] if len(participants) > 0 else '',
                participants[1] if len(participants) > 1 else '',
                thread.get('thread_title', ''),
                thread.get('last_activity_at', 0),
                len(messages_data.get(thread_id, [])),
                datetime.now().isoformat()
            ))
        
        # บันทึก messages
        for thread_id, messages in messages_data.items():
            for message in messages:
                cursor.execute('''
                    INSERT OR REPLACE INTO dm_messages 
                    (thread_id, message_id, sender, recipient, content, timestamp, message_type, media_url, extracted_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    thread_id,
                    message.get('item_id', ''),
                    message.get('user_id', ''),
                    '',  # recipient
                    message.get('text', ''),
                    message.get('timestamp', 0),
                    message.get('item_type', ''),
                    '',  # media_url
                    datetime.now().isoformat()
                ))
        
        conn.commit()
        conn.close()
        print(f"✅ Data saved to database: {self.db_path}")
    
    def run_extraction(self):
        """รันการดึงข้อมูล DM แบบเต็ม"""
        print(f"🎯 STARTING DM EXTRACTION FOR @{self.target_account}")
        print("=" * 60)
        
        # ตั้งค่า database
        self.setup_database()
        
        # ทดสอบ session
        if not self.test_session_validity():
            print("❌ Session invalid - cannot proceed")
            return False
            
        # ดึง threads
        threads_data = self.extract_dm_threads()
        if not threads_data:
            print("⚠️ No threads found or extraction failed")
            return False
            
        # ดึงข้อความจาก threads
        messages_data = {}
        for thread in threads_data[:5]:  # จำกัดแค่ 5 threads แรกเพื่อทดสอบ
            thread_id = thread.get('thread_id', '')
            if thread_id:
                messages = self.extract_thread_messages(thread_id)
                messages_data[thread_id] = messages
                time.sleep(2)  # Rate limiting
                
        # บันทึกข้อมูล
        output_file = self.save_extracted_data(threads_data, messages_data)
        
        print("\\n🎯 EXTRACTION SUMMARY:")
        print(f"   📱 Target: @{self.target_account}")
        print(f"   📋 Threads found: {len(threads_data)}")
        print(f"   💬 Total messages: {sum(len(messages) for messages in messages_data.values())}")
        print(f"   📁 Output file: {output_file}")
        print(f"   🗄️ Database: {self.db_path}")
        
        return True

def main():
    print("🎯 ALX TRADING DM EXTRACTOR 2025")
    print("=" * 50)
    print("Extracting DMs from @alx.trading account")
    print()
    
    extractor = AlxTradingDMExtractor()
    success = extractor.run_extraction()
    
    if success:
        print("\\n✅ DM extraction completed successfully!")
    else:
        print("\\n❌ DM extraction failed!")
        
    print("\\n📋 Check the output files for extracted data")

if __name__ == "__main__":
    main()
