#!/usr/bin/env python3
"""
🎯 ALX TRADING DM EXTRACTOR - DIRECT SESSION APPROACH
====================================================
ใช้ session file ที่มีอยู่เพื่อดึง DM จาก @alx.trading โดยตรง
"""

import json
import os
import requests
import time
from datetime import datetime
import sqlite3

class DirectDMExtractor:
    def __init__(self):
        self.target = "alx.trading"
        self.session_file = "/workspaces/sugarglitch-realops/sessions/session-alx.trading"
        self.output_dir = "/workspaces/sugarglitch-realops/data/alx_trading_dms"
        self.db_path = "/workspaces/sugarglitch-realops/data/alx_trading_dms_direct.db"
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Load session
        self.session_data = self.load_session()
        self.setup_database()
    
    def load_session(self):
        """โหลด session จากไฟล์"""
        try:
            with open(self.session_file, 'r') as f:
                data = json.load(f)
                print(f"✅ Session loaded for {self.target}")
                return data
        except Exception as e:
            print(f"❌ Error loading session: {e}")
            return None
    
    def setup_database(self):
        """สร้าง database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS dm_threads (
            thread_id TEXT PRIMARY KEY,
            target_username TEXT,
            participants TEXT,
            last_activity TEXT,
            message_count INTEGER,
            extraction_timestamp TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS dm_messages (
            message_id TEXT PRIMARY KEY,
            thread_id TEXT,
            sender_username TEXT,
            message_text TEXT,
            timestamp TEXT,
            message_type TEXT,
            extraction_timestamp TEXT,
            FOREIGN KEY (thread_id) REFERENCES dm_threads (thread_id)
        )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Database initialized: {self.db_path}")
    
    def get_headers(self):
        """สร้าง headers สำหรับ request"""
        return {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.instagram.com',
            'Pragma': 'no-cache',
            'Referer': 'https://www.instagram.com/direct/inbox/',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Linux"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-Asbd-Id': '198387',
            'X-Csrftoken': self.session_data.get('cookies', {}).get('csrftoken', ''),
            'X-Ig-App-Id': '936619743392459',
            'X-Ig-Www-Claim': '0',
            'X-Instagram-Ajax': '1',
            'X-Requested-With': 'XMLHttpRequest'
        }
    
    def get_cookies(self):
        """สร้าง cookies จาก session"""
        if not self.session_data:
            return {}
        
        cookies = self.session_data.get('cookies', {})
        return cookies
    
    def test_session_validity(self):
        """ทดสอบว่า session ยังใช้ได้อยู่ไหม"""
        print("🔍 Testing session validity...")
        
        session = requests.Session()
        session.cookies.update(self.get_cookies())
        session.headers.update(self.get_headers())
        
        try:
            # Test main page
            response = session.get('https://www.instagram.com/')
            print(f"   Main page: {response.status_code}")
            
            # Test direct inbox
            response = session.get('https://www.instagram.com/direct/inbox/')
            print(f"   Direct inbox: {response.status_code}")
            
            if response.status_code == 200:
                if 'login' not in response.url.lower():
                    print("✅ Session is valid!")
                    return True
                else:
                    print("❌ Session expired - redirected to login")
                    return False
            else:
                print(f"❌ Session invalid - status: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error testing session: {e}")
            return False
    
    def search_user(self, username):
        """ค้นหา user เพื่อหา user_id"""
        print(f"🔍 Searching for user: {username}")
        
        session = requests.Session()
        session.cookies.update(self.get_cookies())
        session.headers.update(self.get_headers())
        
        try:
            url = f"https://www.instagram.com/web/search/topsearch/?query={username}"
            response = session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                users = data.get('users', [])
                
                for user in users:
                    user_data = user.get('user', {})
                    if user_data.get('username') == username:
                        user_id = user_data.get('pk')
                        print(f"✅ Found user {username} with ID: {user_id}")
                        return user_id
                
                print(f"❌ User {username} not found in search results")
                return None
            else:
                print(f"❌ Search failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error searching user: {e}")
            return None
    
    def get_dm_threads(self):
        """ดึงรายการ DM threads"""
        print("📥 Getting DM threads...")
        
        session = requests.Session()
        session.cookies.update(self.get_cookies())
        session.headers.update(self.get_headers())
        
        try:
            url = "https://www.instagram.com/api/v1/direct_v2/inbox/"
            response = session.get(url)
            
            print(f"   Inbox API status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    threads = data.get('inbox', {}).get('threads', [])
                    print(f"✅ Found {len(threads)} DM threads")
                    return threads
                except json.JSONDecodeError:
                    print("❌ Response is not JSON")
                    # Save HTML for debugging
                    with open(f"{self.output_dir}/inbox_debug_{int(time.time())}.html", 'w') as f:
                        f.write(response.text)
                    return []
            else:
                print(f"❌ Failed to get inbox: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error getting DM threads: {e}")
            return []
    
    def find_target_thread(self, threads, target_username):
        """หา thread ที่มีการสนทนากับ target"""
        print(f"🎯 Looking for conversation with {target_username}...")
        
        for thread in threads:
            users = thread.get('users', [])
            for user in users:
                if user.get('username') == target_username:
                    thread_id = thread.get('thread_id')
                    print(f"✅ Found conversation thread: {thread_id}")
                    return thread
        
        print(f"❌ No conversation found with {target_username}")
        return None
    
    def get_thread_messages(self, thread_id):
        """ดึงข้อความจาก thread"""
        print(f"💬 Getting messages from thread: {thread_id}")
        
        session = requests.Session()
        session.cookies.update(self.get_cookies())
        session.headers.update(self.get_headers())
        
        try:
            url = f"https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/"
            response = session.get(url)
            
            print(f"   Thread API status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    messages = data.get('thread', {}).get('items', [])
                    print(f"✅ Found {len(messages)} messages")
                    return messages
                except json.JSONDecodeError:
                    print("❌ Response is not JSON")
                    return []
            else:
                print(f"❌ Failed to get messages: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error getting messages: {e}")
            return []
    
    def save_to_database(self, thread_data, messages):
        """บันทึกข้อมูลลงฐานข้อมูล"""
        print("💾 Saving to database...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Save thread
        thread_id = thread_data.get('thread_id')
        participants = json.dumps([user.get('username') for user in thread_data.get('users', [])])
        
        cursor.execute('''
            INSERT OR REPLACE INTO dm_threads 
            (thread_id, target_username, participants, last_activity, message_count, extraction_timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            thread_id,
            self.target,
            participants,
            thread_data.get('last_activity_at'),
            len(messages),
            datetime.now().isoformat()
        ))
        
        # Save messages
        for msg in messages:
            cursor.execute('''
                INSERT OR REPLACE INTO dm_messages
                (message_id, thread_id, sender_username, message_text, timestamp, message_type, extraction_timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                msg.get('item_id'),
                thread_id,
                msg.get('user_id'),  # This would need user ID to username mapping
                msg.get('text', ''),
                msg.get('timestamp'),
                msg.get('item_type'),
                datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
        print(f"✅ Saved {len(messages)} messages to database")
    
    def save_to_json(self, thread_data, messages):
        """บันทึกข้อมูลเป็น JSON"""
        print("💾 Saving to JSON...")
        
        output_data = {
            'extraction_info': {
                'target': self.target,
                'extraction_timestamp': datetime.now().isoformat(),
                'method': 'direct_session_extraction'
            },
            'thread_data': thread_data,
            'messages': messages,
            'summary': {
                'total_messages': len(messages),
                'thread_id': thread_data.get('thread_id'),
                'participants': [user.get('username') for user in thread_data.get('users', [])]
            }
        }
        
        output_file = f"{self.output_dir}/dm_extraction_{int(time.time())}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Data saved to: {output_file}")
        return output_file
    
    def extract_dms(self):
        """หลักการดึง DM"""
        print(f"🎯 STARTING DM EXTRACTION FOR {self.target}")
        print("=" * 50)
        
        # Test session
        if not self.test_session_validity():
            print("❌ Cannot proceed - invalid session")
            return False
        
        # Get all DM threads
        threads = self.get_dm_threads()
        if not threads:
            print("❌ No DM threads found")
            return False
        
        # Find target thread
        target_thread = self.find_target_thread(threads, self.target)
        if not target_thread:
            print(f"❌ No conversation found with {self.target}")
            return False
        
        # Get messages from target thread
        thread_id = target_thread.get('thread_id')
        messages = self.get_thread_messages(thread_id)
        
        if messages:
            # Save data
            self.save_to_database(target_thread, messages)
            json_file = self.save_to_json(target_thread, messages)
            
            print(f"\n✅ EXTRACTION COMPLETED!")
            print(f"   Target: {self.target}")
            print(f"   Messages found: {len(messages)}")
            print(f"   JSON output: {json_file}")
            print(f"   Database: {self.db_path}")
            return True
        else:
            print(f"❌ No messages found in conversation with {self.target}")
            return False

def main():
    """Main function"""
    print("🎯 ALX TRADING DM EXTRACTOR - DIRECT SESSION APPROACH")
    print("=" * 60)
    
    extractor = DirectDMExtractor()
    success = extractor.extract_dms()
    
    if success:
        print("\n🎉 DM extraction completed successfully!")
    else:
        print("\n❌ DM extraction failed")

if __name__ == "__main__":
    main()