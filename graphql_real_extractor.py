#!/usr/bin/env python3
"""
🔥 SUGARGLITCH REALOPS - GRAPHQL REAL EXTRACTOR 🔥
ดึงข้อมูล Instagram DMs จริงด้วย GraphQL Endpoints
🚫 NO SIMULATION - REAL GRAPHQL EXTRACTION
"""

import requests
import json
import time
import random
from datetime import datetime
import os
from urllib.parse import quote_plus
import hashlib

class GraphQLRealExtractor:
    def __init__(self):
        self.sessions = []
        self.base_url = "https://www.instagram.com"
        self.graphql_url = f"{self.base_url}/graphql/query/"
        
        # Instagram GraphQL Query Hashes (real ones used by Instagram web)
        self.query_hashes = {
            'direct_inbox': 'f2405dedf9400e64cb609ca5fd0a2ee9',  # DirectInboxQuery
            'thread_messages': '1ae6a197b4b9d4d69a11db9d10b8b13e',  # DirectThreadMessagesQuery
            'user_info': '47975e2b28aa6507ab6e4dc4e4e5f962',  # UserInfoQuery
            'search_users': '9b43d2c05f05df3470c8a93b7a1dea95',  # SearchUsersQuery
        }
        
        print("🔥 SUGARGLITCH REALOPS - GRAPHQL REAL EXTRACTOR 🔥")
        print("ดึงข้อมูล Instagram DMs จริงด้วย GraphQL Endpoints")
        print("🚫 NO SIMULATION - REAL GRAPHQL EXTRACTION")
        
    def load_sessions(self):
        """โหลด verified sessions จากไฟล์ต่างๆ"""
        session_files = [
            "data/sessions/alx_session_cookies.txt",
            "config/sessions/alx_trading_sessionid_alt.json", 
            "alx_trading_active_session_20250527_050413.json",
            "alx_trading_active_session_20250527_050337.json"
        ]
        
        print(f"\n🔑 กำลังโหลด verified sessions...")
        
        for file_path in session_files:
            if os.path.exists(file_path):
                print(f"📄 Loading: {file_path}")
                try:
                    with open(file_path, 'r') as f:
                        if file_path.endswith('.json'):
                            data = json.load(f)
                            if isinstance(data, dict):
                                self.sessions.append(data)
                            elif isinstance(data, list):
                                self.sessions.extend(data)
                        else:
                            # Text format
                            content = f.read().strip()
                            if 'sessionid=' in content:
                                sessionid = content.split('sessionid=')[1].split(';')[0]
                                session_data = {'sessionid': sessionid}
                                if 'csrftoken=' in content:
                                    csrftoken = content.split('csrftoken=')[1].split(';')[0]
                                    session_data['csrftoken'] = csrftoken
                                self.sessions.append(session_data)
                except Exception as e:
                    print(f"❌ Error loading {file_path}: {e}")
        
        print(f"✅ Loaded {len(self.sessions)} verified sessions")
        return len(self.sessions) > 0
    
    def get_headers(self, session_data):
        """สร้าง headers สำหรับ GraphQL requests"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': session_data.get('csrftoken', ''),
            'X-Instagram-AJAX': '1',
            'X-IG-App-ID': '936619743392459',
            'X-ASBD-ID': '129477',
            'X-IG-WWW-Claim': '0',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/direct/inbox/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
        
        # Build cookie string
        cookies = []
        for key, value in session_data.items():
            if key in ['sessionid', 'csrftoken', 'ds_user_id', 'ig_did', 'ig_nrcb']:
                cookies.append(f"{key}={value}")
        
        if cookies:
            headers['Cookie'] = '; '.join(cookies)
        
        return headers
    
    def make_graphql_request(self, query_hash, variables, session_data):
        """ทำ GraphQL request"""
        headers = self.get_headers(session_data)
        
        data = {
            'query_hash': query_hash,
            'variables': json.dumps(variables)
        }
        
        try:
            response = requests.post(
                self.graphql_url,
                headers=headers,
                data=data,
                timeout=15,
                allow_redirects=False
            )
            
            print(f"📊 GraphQL Response: {response.status_code}")
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ GraphQL Error: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return None
    
    def test_session_with_graphql(self, session_data):
        """ทดสอบ session ด้วย GraphQL UserInfoQuery"""
        print(f"🧪 Testing session with GraphQL...")
        
        # Try to get current user info
        variables = {}
        result = self.make_graphql_request(
            self.query_hashes['user_info'], 
            variables, 
            session_data
        )
        
        if result and 'data' in result:
            print("✅ GraphQL Session Valid!")
            return True
        else:
            print("❌ GraphQL Session Invalid")
            return False
    
    def extract_direct_inbox(self, session_data):
        """ดึงข้อมูล Direct Inbox ด้วย GraphQL"""
        print(f"📥 กำลังดึงข้อมูล DMs ผ่าน GraphQL DirectInboxQuery...")
        
        variables = {
            "fetch_reason": "initial_snapshot",
            "folder": "",
            "thread_message_limit": 20,
            "first": 20
        }
        
        result = self.make_graphql_request(
            self.query_hashes['direct_inbox'],
            variables,
            session_data
        )
        
        if result and 'data' in result:
            print("✅ GraphQL Direct Inbox successful!")
            inbox_data = result['data']
            
            # Save raw response
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"data/extractions/graphql_inbox_{timestamp}.json"
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Raw GraphQL response saved: {output_file}")
            return inbox_data
        else:
            print("❌ GraphQL Direct Inbox failed")
            return None
    
    def extract_thread_messages(self, thread_id, session_data):
        """ดึงข้อความในสレดเฉพาะ"""
        print(f"📨 กำลังดึงข้อความจาก thread: {thread_id}")
        
        variables = {
            "thread_id": thread_id,
            "first": 50
        }
        
        result = self.make_graphql_request(
            self.query_hashes['thread_messages'],
            variables,
            session_data
        )
        
        if result and 'data' in result:
            print(f"✅ Thread messages extracted: {thread_id}")
            return result['data']
        else:
            print(f"❌ Failed to extract thread: {thread_id}")
            return None
    
    def run_extraction(self):
        """เริ่มต้น REAL GraphQL extraction"""
        print(f"\n🚀 เริ่มต้น GRAPHQL REAL EXTRACTION")
        print("=" * 60)
        
        if not self.load_sessions():
            print("❌ No sessions loaded!")
            return False
        
        success_count = 0
        
        for i, session_data in enumerate(self.sessions, 1):
            print(f"\n🔄 Testing session {i}/{len(self.sessions)}")
            print(f"📄 Session data keys: {list(session_data.keys())}")
            
            # Test session validity
            if self.test_session_with_graphql(session_data):
                print("✅ Session validated! Extracting data...")
                
                # Extract direct inbox
                inbox_data = self.extract_direct_inbox(session_data)
                
                if inbox_data:
                    success_count += 1
                    print("✅ REAL DATA EXTRACTED!")
                    
                    # If we find threads, extract messages from them
                    if 'viewer' in inbox_data and 'message_threads' in inbox_data['viewer']:
                        threads = inbox_data['viewer']['message_threads'].get('edges', [])
                        print(f"📨 Found {len(threads)} conversation threads")
                        
                        for thread in threads[:5]:  # Limit to first 5 threads
                            thread_node = thread.get('node', {})
                            thread_id = thread_node.get('thread_key', '')
                            
                            if thread_id:
                                thread_messages = self.extract_thread_messages(thread_id, session_data)
                                if thread_messages:
                                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                    thread_file = f"data/extractions/thread_{thread_id}_{timestamp}.json"
                                    
                                    with open(thread_file, 'w', encoding='utf-8') as f:
                                        json.dump(thread_messages, f, indent=2, ensure_ascii=False)
                                    
                                    print(f"💾 Thread saved: {thread_file}")
                    
                    # Random delay to avoid rate limiting
                    time.sleep(random.uniform(2, 5))
                else:
                    print("❌ No data extracted from this session")
            else:
                print("❌ Session validation failed")
            
            # Delay between sessions
            time.sleep(random.uniform(1, 3))
        
        if success_count > 0:
            print(f"\n✅ GRAPHQL EXTRACTION SUCCESS!")
            print(f"📊 Successfully extracted from {success_count} sessions")
            return True
        else:
            print(f"\n❌ GRAPHQL EXTRACTION FAILED!")
            print("ไม่สามารถดึงข้อมูลจริงผ่าน GraphQL ได้")
            return False

def main():
    print("\n🔥 GRAPHQL REAL INSTAGRAM DM EXTRACTOR 🔥")
    print("🎯 Target: alx.trading")
    print("📊 GraphQL + Advanced Query Hashes")
    print("🚫 NO SIMULATION - REAL GRAPHQL CALLS")
    print("🔒 Advanced Bypass Techniques")
    
    extractor = GraphQLRealExtractor()
    success = extractor.run_extraction()
    
    if success:
        print("\n🎉 MISSION ACCOMPLISHED!")
        print("✅ Real Instagram DMs extracted successfully")
        print("📁 Check data/extractions/ for output files")
    else:
        print("\n💥 MISSION FAILED!")
        print("❌ Unable to extract real data")

if __name__ == "__main__":
    main()
