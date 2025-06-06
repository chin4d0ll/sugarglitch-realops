#!/usr/bin/env python3
"""
Final DM Extractor - Uses fresh session to extract real DMs
"""

import json
import os
import sys
import requests
from datetime import datetime

class FinalDMExtractor:
    def __init__(self, target_username="alx.trading"):
        self.target_username = target_username
        self.session_file = f"tools/session_{target_username.replace('.', '_')}.json"
        self.output_dir = f"real_extraction/{target_username}"
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
    def load_session(self):
        """Load session from file"""
        try:
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            
            sessionid = session_data.get('sessionid', '')
            if not sessionid:
                print(f"❌ No sessionid found in {self.session_file}")
                return None
                
            print(f"✅ Loaded session from {self.session_file}")
            print(f"   Sessionid: {sessionid[:20]}...")
            return sessionid
            
        except FileNotFoundError:
            print(f"❌ Session file not found: {self.session_file}")
            print("   Run simple_session_guide.py first to set up your session.")
            return None
        except Exception as e:
            print(f"❌ Failed to load session: {e}")
            return None
    
    def get_headers(self, sessionid, csrftoken=""):
        """Get headers for Instagram API requests"""
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-CSRFToken': csrftoken,
            'X-IG-App-ID': '936619743392459',
            'X-IG-WWW-Claim': '0',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Cookie': f'sessionid={sessionid}; csrftoken={csrftoken}',
            'Referer': 'https://www.instagram.com/direct/inbox/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }
    
    def extract_dms(self, sessionid):
        """Extract DMs from target user"""
        print(f"\n🎯 Starting DM extraction for: {self.target_username}")
        print("="*60)
        
        headers = self.get_headers(sessionid)
        
        try:
            # Step 1: Get user ID
            print("Step 1: Looking up user ID...")
            user_url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={self.target_username}'
            
            user_response = requests.get(user_url, headers=headers, timeout=15)
            print(f"   Status: {user_response.status_code}")
            
            if user_response.status_code != 200:
                print(f"❌ Failed to get user info: {user_response.status_code}")
                print(f"   Response: {user_response.text[:200]}...")
                return False
            
            user_data = user_response.json()
            
            if 'data' not in user_data or 'user' not in user_data['data']:
                print("❌ Invalid user data received")
                print(f"   Response keys: {list(user_data.keys())}")
                return False
            
            target_user_id = user_data['data']['user']['id']
            print(f"✅ Found user ID: {target_user_id}")
            
            # Step 2: Get DM threads
            print("\nStep 2: Fetching DM threads...")
            threads_url = 'https://www.instagram.com/api/v1/direct_v2/inbox/?persistentBadging=true&folder=&limit=50'
            
            threads_response = requests.get(threads_url, headers=headers, timeout=15)
            print(f"   Status: {threads_response.status_code}")
            
            if threads_response.status_code != 200:
                print(f"❌ Failed to get threads: {threads_response.status_code}")
                if threads_response.status_code == 401:
                    print("   Session appears to be invalid or expired")
                elif threads_response.status_code == 403:
                    print("   Access forbidden - may need to verify account")
                print(f"   Response: {threads_response.text[:200]}...")
                return False
            
            threads_data = threads_response.json()
            threads = threads_data.get('inbox', {}).get('threads', [])
            print(f"✅ Found {len(threads)} total threads")
            
            # Step 3: Find target conversation
            print(f"\nStep 3: Looking for conversation with {self.target_username}...")
            target_thread = None
            
            for i, thread in enumerate(threads):
                thread_users = thread.get('users', [])
                print(f"   Thread {i+1}: {len(thread_users)} users")
                
                for user in thread_users:
                    user_id = str(user.get('pk', ''))
                    username = user.get('username', '')
                    print(f"     User: {username} (ID: {user_id})")
                    
                    if user_id == str(target_user_id) or username == self.target_username:
                        target_thread = thread
                        print(f"✅ Found target thread!")
                        break
                
                if target_thread:
                    break
            
            if not target_thread:
                print(f"❌ No conversation found with {self.target_username}")
                print("   This could mean:")
                print("   - You haven't messaged this user yet")
                print("   - The conversation is archived")
                print("   - The username is incorrect")
                return False
            
            thread_id = target_thread['thread_id']
            print(f"✅ Thread ID: {thread_id}")
            
            # Step 4: Extract messages
            print(f"\nStep 4: Extracting messages from thread...")
            messages_url = f'https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/?limit=100'
            
            messages_response = requests.get(messages_url, headers=headers, timeout=15)
            print(f"   Status: {messages_response.status_code}")
            
            if messages_response.status_code != 200:
                print(f"❌ Failed to get messages: {messages_response.status_code}")
                print(f"   Response: {messages_response.text[:200]}...")
                return False
            
            messages_data = messages_response.json()
            messages = messages_data.get('thread', {}).get('items', [])
            
            print(f"✅ Extracted {len(messages)} messages!")
            
            # Step 5: Save results
            print(f"\nStep 5: Saving results...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.output_dir, f"REAL_DMS_{timestamp}.json")
            
            # Process messages for better readability
            processed_messages = []
            for msg in messages:
                processed_msg = {
                    'message_id': msg.get('item_id', ''),
                    'timestamp': msg.get('timestamp', ''),
                    'user_id': msg.get('user_id', ''),
                    'message_type': msg.get('item_type', ''),
                    'text': msg.get('text', ''),
                    'is_sent_by_me': msg.get('user_id') != target_user_id,
                    'raw_data': msg
                }
                processed_messages.append(processed_msg)
            
            result = {
                'extraction_info': {
                    'target_username': self.target_username,
                    'target_user_id': target_user_id,
                    'thread_id': thread_id,
                    'extraction_time': datetime.now().isoformat(),
                    'message_count': len(messages),
                    'status': 'SUCCESS - REAL DATA EXTRACTED'
                },
                'messages': processed_messages,
                'raw_thread_data': target_thread
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Results saved to: {output_file}")
            
            # Step 6: Show summary
            print(f"\n🎉 EXTRACTION COMPLETE!")
            print("="*60)
            print(f"Target: {self.target_username}")
            print(f"Messages extracted: {len(messages)}")
            print(f"Thread ID: {thread_id}")
            print(f"Output file: {output_file}")
            print(f"Status: REAL DATA SUCCESSFULLY EXTRACTED")
            
            # Show first few messages as preview
            if processed_messages:
                print(f"\n📋 MESSAGE PREVIEW (first 3 messages):")
                for i, msg in enumerate(processed_messages[:3]):
                    sender = "You" if msg['is_sent_by_me'] else self.target_username
                    text = msg['text'] or f"[{msg['message_type']} message]"
                    print(f"   {i+1}. {sender}: {text[:100]}...")
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def run(self):
        """Main execution"""
        print("🚀 FINAL DM EXTRACTOR - REAL DATA EXTRACTION")
        print("="*60)
        print(f"Target: {self.target_username}")
        print(f"Session file: {self.session_file}")
        print(f"Output directory: {self.output_dir}")
        print()
        
        # Load session
        sessionid = self.load_session()
        if not sessionid:
            return False
        
        # Extract DMs
        success = self.extract_dms(sessionid)
        
        if success:
            print(f"\n✅ DM extraction completed successfully!")
            print(f"Check the output files in: {self.output_dir}")
        else:
            print(f"\n❌ DM extraction failed.")
            print(f"Make sure your session is valid and you have DMs with {self.target_username}")
        
        return success

if __name__ == "__main__":
    try:
        extractor = FinalDMExtractor()
        extractor.run()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
