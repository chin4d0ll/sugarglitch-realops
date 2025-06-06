#!/usr/bin/env python3
"""
🎯 REAL INSTAGRAM DM EXTRACTOR 2025
===================================
ดึงข้อมูล DM จริงจาก Instagram โดยใช้ session จริง
- ใช้ session cookies ที่มีอยู่
- เชื่อมต่อ Instagram API จริง
- ดึงข้อมูล conversations และ messages จริง
"""

import json
import os
import time
import requests
import sqlite3
from datetime import datetime
from pathlib import Path
from target_database_manager import TargetDatabaseManager

class RealInstagramDMExtractor:
    """🎯 Real Instagram DM Extractor using actual session cookies"""
    
    def __init__(self):
        self.target = "alx.trading"
        self.project_root = "/workspaces/sugarglitch-realops"
        
        # Load real session
        self.session = self.load_session_cookies()
        
        # Instagram API endpoints
        self.base_url = "https://www.instagram.com"
        self.api_url = "https://www.instagram.com/api/v1"
        
        # Headers for Instagram requests
        self.headers = {
            'User-Agent': 'Instagram 219.0.0.12.117 Android',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'X-Instagram-AJAX': '1',
            'X-CSRFToken': '',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/',
            'Connection': 'keep-alive',
        }
        
        # Database setup
        self.db_manager = TargetDatabaseManager(f"{self.project_root}/integrated_targets_2025.db")
        
        # Output directory
        self.output_dir = f"{self.project_root}/real_extraction/alx_trading"
        os.makedirs(self.output_dir, exist_ok=True)
        
        print(f"🎯 Real Instagram DM Extractor initialized")
        print(f"   Target: {self.target}")
        print(f"   Session loaded: {'✅' if self.session else '❌'}")
    
    def load_session_cookies(self):
        """Load real session cookies from project"""
        session_file = f"{self.project_root}/sessions/session-alx.trading"
        
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
                return session_data.get('cookies', {})
        except Exception as e:
            print(f"❌ Error loading session: {e}")
            return None
    
    def setup_session(self):
        """Setup requests session with cookies"""
        session = requests.Session()
        
        if self.session:
            # Add cookies to session
            for name, value in self.session.items():
                session.cookies.set(name, value, domain='.instagram.com')
        
        # Get CSRF token
        try:
            response = session.get(f"{self.base_url}/", headers=self.headers)
            if response.status_code == 200:
                # Extract CSRF token from response
                csrf_token = session.cookies.get('csrftoken', '')
                self.headers['X-CSRFToken'] = csrf_token
                print(f"✅ CSRF token obtained: {csrf_token[:20]}...")
            else:
                print(f"❌ Failed to get CSRF token: {response.status_code}")
        except Exception as e:
            print(f"❌ Error setting up session: {e}")
        
        return session
    
    def get_user_id(self, username):
        """Get Instagram user ID from username"""
        session = self.setup_session()
        
        try:
            # Try to get user info
            url = f"{self.base_url}/{username}/"
            response = session.get(url, headers=self.headers)
            
            if response.status_code == 200:
                # Extract user ID from page source
                content = response.text
                if '"id":"' in content:
                    start = content.find('"id":"') + 6
                    end = content.find('"', start)
                    user_id = content[start:end]
                    print(f"✅ User ID found: {user_id}")
                    return user_id
            
            print(f"❌ Failed to get user ID: {response.status_code}")
            return None
            
        except Exception as e:
            print(f"❌ Error getting user ID: {e}")
            return None
    
    def get_direct_messages(self):
        """Get direct messages from Instagram"""
        session = self.setup_session()
        
        try:
            # Get inbox
            url = f"{self.api_url}/direct_v2/inbox/"
            response = session.get(url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Inbox data retrieved")
                return data
            else:
                print(f"❌ Failed to get inbox: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting direct messages: {e}")
            return None
    
    def get_thread_messages(self, thread_id):
        """Get messages from specific thread"""
        session = self.setup_session()
        
        try:
            url = f"{self.api_url}/direct_v2/threads/{thread_id}/"
            response = session.get(url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Thread {thread_id} messages retrieved")
                return data
            else:
                print(f"❌ Failed to get thread {thread_id}: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting thread messages: {e}")
            return None
    
    def search_conversations(self, target_username):
        """Search for conversations with specific user"""
        print(f"🔍 Searching for conversations with {target_username}")
        
        # Get user ID first
        target_user_id = self.get_user_id(target_username)
        if not target_user_id:
            return None
        
        # Get all DMs
        inbox_data = self.get_direct_messages()
        if not inbox_data:
            return None
        
        # Search for conversations with target user
        target_conversations = []
        
        if 'inbox' in inbox_data and 'threads' in inbox_data['inbox']:
            for thread in inbox_data['inbox']['threads']:
                # Check if target user is in this thread
                if 'users' in thread:
                    for user in thread['users']:
                        if str(user.get('pk')) == str(target_user_id):
                            print(f"✅ Found conversation with {target_username}")
                            target_conversations.append(thread)
                            break
        
        return target_conversations
    
    def extract_messages_from_thread(self, thread):
        """Extract all messages from a thread"""
        messages = []
        
        if 'items' in thread:
            for item in thread['items']:
                message_data = {
                    'id': item.get('id'),
                    'user_id': item.get('user_id'),
                    'timestamp': item.get('timestamp'),
                    'text': item.get('text', ''),
                    'item_type': item.get('item_type'),
                }
                
                # Extract media if present
                if 'media' in item:
                    message_data['media'] = item['media']
                
                # Extract reactions
                if 'reactions' in item:
                    message_data['reactions'] = item['reactions']
                
                messages.append(message_data)
        
        return messages
    
    def perform_real_extraction(self):
        """Perform real DM extraction"""
        print(f"\n🚀 STARTING REAL DM EXTRACTION")
        print(f"================================================")
        
        extraction_results = {
            'target': self.target,
            'extraction_timestamp': datetime.now().isoformat(),
            'method': 'real_instagram_api',
            'results': {
                'conversations': [],
                'total_messages': 0,
                'extraction_errors': []
            }
        }
        
        try:
            # Search for conversations with target
            conversations = self.search_conversations(self.target)
            
            if conversations:
                print(f"✅ Found {len(conversations)} conversation(s)")
                
                for i, thread in enumerate(conversations):
                    print(f"📋 Processing conversation {i+1}...")
                    
                    # Get detailed thread messages
                    thread_id = thread.get('thread_id')
                    if thread_id:
                        detailed_thread = self.get_thread_messages(thread_id)
                        if detailed_thread:
                            thread = detailed_thread.get('thread', thread)
                    
                    # Extract messages
                    messages = self.extract_messages_from_thread(thread)
                    
                    conversation_data = {
                        'thread_id': thread.get('thread_id'),
                        'thread_title': thread.get('thread_title', ''),
                        'users': thread.get('users', []),
                        'messages': messages,
                        'message_count': len(messages),
                        'last_activity': thread.get('last_activity_at')
                    }
                    
                    extraction_results['results']['conversations'].append(conversation_data)
                    extraction_results['results']['total_messages'] += len(messages)
                    
                    print(f"   ✅ Extracted {len(messages)} messages")
            
            else:
                print(f"❌ No conversations found with {self.target}")
                extraction_results['results']['extraction_errors'].append(
                    f"No conversations found with {self.target}"
                )
        
        except Exception as e:
            error_msg = f"Extraction error: {str(e)}"
            print(f"❌ {error_msg}")
            extraction_results['results']['extraction_errors'].append(error_msg)
        
        # Save results
        timestamp = int(time.time())
        output_file = f"{self.output_dir}/real_dm_extraction_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(extraction_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ REAL EXTRACTION COMPLETED!")
        print(f"📂 Results saved: {output_file}")
        print(f"📊 Total conversations: {len(extraction_results['results']['conversations'])}")
        print(f"📨 Total messages: {extraction_results['results']['total_messages']}")
        
        # Update database
        self.update_database(extraction_results)
        
        return extraction_results
    
    def update_database(self, results):
        """Update database with extraction results"""
        try:
            # Log extraction operation
            operation_data = {
                'target': self.target,
                'operation_type': 'real_dm_extraction',
                'timestamp': datetime.now().isoformat(),
                'results': results['results'],
                'success': len(results['results']['extraction_errors']) == 0
            }
            
            operation_id = self.db_manager.log_operation(
                self.target,
                'real_dm_extraction',
                operation_data
            )
            
            print(f"✅ Database updated - Operation ID: {operation_id}")
            
        except Exception as e:
            print(f"❌ Database update error: {e}")

def main():
    """Main execution function"""
    print("🎯 REAL INSTAGRAM DM EXTRACTOR 2025")
    print("=====================================")
    
    extractor = RealInstagramDMExtractor()
    results = extractor.perform_real_extraction()
    
    print("\n🎯 EXTRACTION SUMMARY")
    print("------------------------------")
    print(f"Target: {extractor.target}")
    print(f"Method: Real Instagram API")
    print(f"Conversations: {len(results['results']['conversations'])}")
    print(f"Messages: {results['results']['total_messages']}")
    print(f"Errors: {len(results['results']['extraction_errors'])}")

if __name__ == "__main__":
    main()