#!/usr/bin/env python3
"""
🎯 AUTO DM EXTRACTOR - Using Project Session
Extract real Instagram DMs using existing session files
"""

import json
import requests
import time
from datetime import datetime
import os
import sys

def print_flush(text):
    """Print with immediate flush"""
    print(text, flush=True)
    sys.stdout.flush()

class AutoDMExtractor:
    def __init__(self):
        self.target = "alx.trading"
        self.session_file = "/workspaces/sugarglitch-realops/tools/session_alx_trading.json"
        self.output_dir = "/workspaces/sugarglitch-realops/data/auto_extraction"
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        print_flush("🎯 AUTO DM EXTRACTOR - Using Project Session")
        print_flush("=" * 60)
        print_flush(f"Target: {self.target}")
        print_flush(f"Session file: {self.session_file}")
        
    def load_session(self):
        """Load session from project file"""
        try:
            with open(self.session_file, 'r') as f:
                cookies_data = json.load(f)
            
            # Extract sessionid from cookie format
            sessionid = None
            if isinstance(cookies_data, list):
                for cookie in cookies_data:
                    if cookie.get('name') == 'sessionid':
                        sessionid = cookie.get('value')
                        break
            elif isinstance(cookies_data, dict):
                sessionid = cookies_data.get('sessionid')
            
            if sessionid:
                print(f"✅ Loaded sessionid: {sessionid[:20]}...")
                return sessionid
            else:
                print("❌ No sessionid found in file")
                return None
                
        except Exception as e:
            print(f"❌ Error loading session: {e}")
            return None
    
    def test_session(self, sessionid):
        """Test if session is valid"""
        print("\n🧪 Testing session validity...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        cookies = {
            'sessionid': sessionid
        }
        
        session = requests.Session()
        session.cookies.update(cookies)
        session.headers.update(headers)
        
        try:
            response = session.get('https://www.instagram.com/', timeout=10)
            print(f"Instagram main page: {response.status_code}")
            
            if response.status_code == 200:
                if 'login' in response.url.lower():
                    print("❌ Session expired - redirected to login")
                    return False
                elif '"viewer"' in response.text or '"user"' in response.text:
                    print("✅ Session appears valid")
                    return True
                else:
                    print("⚠️ Uncertain session status, trying anyway...")
                    return True
            else:
                print(f"❌ Bad status code: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Session test failed: {e}")
            return False
    
    def get_user_info(self, sessionid):
        """Get current user info"""
        print("\n👤 Getting user info...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'X-Requested-With': 'XMLHttpRequest',
        }
        
        cookies = {
            'sessionid': sessionid
        }
        
        session = requests.Session()
        session.cookies.update(cookies)
        session.headers.update(headers)
        
        try:
            response = session.get('https://www.instagram.com/api/v1/accounts/edit/web_form_data/', timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'form_data' in data and 'username' in data['form_data']:
                    username = data['form_data']['username']
                    print(f"✅ Logged in as: {username}")
                    return username
            
            print("⚠️ Could not determine username")
            return "unknown_user"
            
        except Exception as e:
            print(f"⚠️ Could not get user info: {e}")
            return "unknown_user"
    
    def search_for_target_user(self, sessionid):
        """Search for target user"""
        print(f"\n🔍 Searching for {self.target}...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'X-Requested-With': 'XMLHttpRequest',
        }
        
        cookies = {
            'sessionid': sessionid
        }
        
        session = requests.Session()
        session.cookies.update(cookies)
        session.headers.update(headers)
        
        try:
            # Search for user
            search_url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={self.target}'
            response = session.get(search_url, timeout=10)
            
            print(f"Search response: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'user' in data['data']:
                    user_info = data['data']['user']
                    user_id = user_info.get('id')
                    username = user_info.get('username')
                    print(f"✅ Found user: {username} (ID: {user_id})")
                    return user_id
                else:
                    print(f"❌ User {self.target} not found in response")
                    return None
            else:
                print(f"❌ Search failed: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"❌ Error searching for user: {e}")
            return None
    
    def extract_direct_messages(self, sessionid, target_user_id=None):
        """Extract direct messages"""
        print(f"\n📥 Extracting direct messages...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'X-Requested-With': 'XMLHttpRequest',
        }
        
        cookies = {
            'sessionid': sessionid
        }
        
        session = requests.Session()
        session.cookies.update(cookies)
        session.headers.update(headers)
        
        try:
            # Get inbox
            inbox_url = 'https://www.instagram.com/api/v1/direct_v2/inbox/'
            print(f"Requesting inbox: {inbox_url}")
            response = session.get(inbox_url, timeout=15)
            
            print(f"Inbox API response: {response.status_code}")
            
            if response.status_code == 200:
                inbox_data = response.json()
                threads = inbox_data.get('inbox', {}).get('threads', [])
                print(f"✅ Found {len(threads)} conversation threads")
                
                # Look for our target by username
                target_thread = None
                found_conversations = []
                
                for thread in threads:
                    users = thread.get('users', [])
                    thread_usernames = []
                    
                    for user in users:
                        username = user.get('username', '')
                        thread_usernames.append(username)
                        
                        if username == self.target:
                            target_thread = thread
                            print(f"🎯 Found target thread with {self.target}!")
                            break
                    
                    found_conversations.append(', '.join(thread_usernames))
                
                if target_thread:
                    return self.extract_thread_messages(session, target_thread)
                else:
                    print(f"❌ No conversation found with {self.target}")
                    
                    # Show available conversations
                    print(f"\n📋 Found conversations with:")
                    for i, conv in enumerate(found_conversations[:10]):  # Show first 10
                        print(f"  {i+1}. {conv}")
                    
                    return {
                        'target': self.target,
                        'extraction_timestamp': datetime.now().isoformat(),
                        'total_messages': 0,
                        'messages': [],
                        'error': f'No conversation found with {self.target}',
                        'available_conversations': found_conversations[:10]
                    }
                    
            elif response.status_code == 401:
                print("❌ Unauthorized - session expired or invalid")
                return None
            elif response.status_code == 403:
                print("❌ Forbidden - may be rate limited")
                return None
            else:
                print(f"❌ Failed to get inbox: {response.status_code}")
                print(f"Response: {response.text[:300]}")
                return None
                
        except Exception as e:
            print(f"❌ Error extracting DMs: {e}")
            return None
    
    def extract_thread_messages(self, session, thread):
        """Extract messages from thread"""
        thread_id = thread.get('thread_id')
        print(f"💬 Extracting messages from thread {thread_id}...")
        
        try:
            # Get thread messages
            messages_url = f'https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/'
            response = session.get(messages_url, timeout=15)
            
            print(f"Thread messages response: {response.status_code}")
            
            if response.status_code == 200:
                thread_data = response.json()
                messages = thread_data.get('thread', {}).get('items', [])
                
                print(f"✅ Found {len(messages)} messages")
                
                # Process messages
                extracted_messages = []
                for msg in messages:
                    timestamp = msg.get('timestamp')
                    created_at = None
                    if timestamp:
                        try:
                            # Instagram timestamps are in microseconds
                            created_at = datetime.fromtimestamp(timestamp / 1000000).isoformat()
                        except:
                            created_at = str(timestamp)
                    
                    message_data = {
                        'id': msg.get('item_id'),
                        'timestamp': timestamp,
                        'created_at': created_at,
                        'user_id': msg.get('user_id'),
                        'text': msg.get('text', ''),
                        'item_type': msg.get('item_type'),
                    }
                    
                    # Add media if present
                    if 'media' in msg:
                        media = msg['media']
                        message_data['media'] = {
                            'type': media.get('media_type'),
                            'url': media.get('image_versions2', {}).get('candidates', [{}])[0].get('url', ''),
                        }
                    
                    # Add reaction info
                    if 'reactions' in msg:
                        message_data['reactions'] = msg['reactions']
                    
                    extracted_messages.append(message_data)
                
                return {
                    'thread_id': thread_id,
                    'target': self.target,
                    'messages': extracted_messages,
                    'total_messages': len(extracted_messages),
                    'extraction_timestamp': datetime.now().isoformat(),
                    'method': 'auto_extractor_project_session'
                }
            else:
                print(f"❌ Failed to get thread messages: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error extracting thread messages: {e}")
            return None
    
    def save_results(self, data):
        """Save extraction results"""
        if not data:
            print("❌ No data to save")
            return
        
        timestamp = int(time.time())
        output_file = f"{self.output_dir}/auto_dm_extraction_{timestamp}.json"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Results saved to: {output_file}")
            print(f"📊 Total messages extracted: {data.get('total_messages', 0)}")
            
            # Show sample messages
            messages = data.get('messages', [])
            if messages:
                print(f"\n📝 Sample messages (showing first 3):")
                for i, msg in enumerate(messages[:3]):
                    text = msg.get('text', '')[:50]
                    timestamp = msg.get('created_at', 'No timestamp')
                    print(f"  {i+1}. [{timestamp}] {text}...")
            elif 'error' in data:
                print(f"\n❌ Error: {data['error']}")
                if 'available_conversations' in data:
                    print("Available conversations found instead:")
                    for conv in data['available_conversations'][:5]:
                        print(f"  - {conv}")
            
        except Exception as e:
            print(f"❌ Error saving results: {e}")
    
    def run(self):
        """Main extraction process"""
        print("\n🚀 Starting automatic DM extraction...")
        
        # Load session from project
        sessionid = self.load_session()
        if not sessionid:
            print("❌ Could not load session from project")
            return
        
        # Test session
        if not self.test_session(sessionid):
            print("❌ Session is not valid")
            return
        
        # Get current user info
        current_user = self.get_user_info(sessionid)
        
        # Search for target user (optional)
        target_user_id = self.search_for_target_user(sessionid)
        
        # Extract DMs
        results = self.extract_direct_messages(sessionid, target_user_id)
        
        # Save results
        self.save_results(results)
        
        if results and results.get('total_messages', 0) > 0:
            print("\n🎉 SUCCESS! Real DM data extracted from project session!")
        else:
            print("\n⚠️ No messages found or extraction had issues")
            print("This could mean:")
            print("- No conversation exists with this user")
            print("- Session doesn't have access to this conversation")
            print("- The target user is in a different conversation format")

if __name__ == "__main__":
    extractor = AutoDMExtractor()
    extractor.run()
