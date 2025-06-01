#!/usr/bin/env python3
"""
💀📱 Standalone Instagram DM Extractor 💀📱
==========================================
เครื่องมือดึง DMs จาก Instagram แบบเร็วและปลอดภัย

Features:
- ดึง DMs จาก conversations ทั้งหมด
- รองรับ text, photos, videos, voice messages
- มี retry mechanism สำหรับ rate limiting
- บันทึกผลลัพธ์เป็น JSON
- Human-like delays เพื่อหลีกเลี่ยงการตรวจจับ
"""

import asyncio
import json
import time
import random
from datetime import datetime
from pathlib import Path

try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes, ChallengeRequired
except ImportError:
    print("❌ Please install instagrapi: pip install instagrapi")
    exit(1)

class InstagramDMExtractor:
    def __init__(self):
        self.client = Client()
        self.client.delay_range = [1, 3]  # Human-like delays
        
    def log(self, message, level='info'):
        """Pretty logging"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        icons = {
            'info': '💙',
            'success': '✅', 
            'error': '❌',
            'working': '⚡',
            'found': '🔍'
        }
        icon = icons.get(level, '💙')
        print(f"[{timestamp}] {icon} {message}")
    
    async def login(self, username, password, max_attempts=3):
        """Login with retry mechanism"""
        for attempt in range(max_attempts):
            try:
                self.log(f"🔐 Login attempt {attempt + 1}/{max_attempts}...")
                self.client.login(username, password)
                self.log("✅ Login successful!", 'success')
                return True
                
            except ChallengeRequired as e:
                self.log("🚨 Challenge required - please verify manually", 'error')
                print("Challenge URL:", e.challenge_url if hasattr(e, 'challenge_url') else 'N/A')
                return False
                
            except PleaseWaitFewMinutes:
                wait_time = 300 + (attempt * 60)  # Increasing wait time
                self.log(f"⏰ Rate limited - waiting {wait_time//60} minutes...", 'working')
                await asyncio.sleep(wait_time)
                
            except Exception as e:
                self.log(f"❌ Login failed: {str(e)}", 'error')
                if attempt < max_attempts - 1:
                    await asyncio.sleep(10 + (attempt * 5))
                    
        return False
    
    async def extract_dms(self, username, password, target_user=None, max_conversations=20, max_messages_per_conversation=100):
        """
        Extract Instagram DMs
        
        Args:
            username: Your Instagram username
            password: Your Instagram password  
            target_user: Specific user to extract DMs from (optional)
            max_conversations: Maximum number of conversations to process
            max_messages_per_conversation: Maximum messages per conversation
        """
        
        self.log(f"💀 Starting DM extraction for {username}", 'working')
        
        # Login
        if not await self.login(username, password):
            return None
            
        dm_data = {
            'extractor': 'Instagram DM Extractor v2.0',
            'username': username,
            'extraction_time': datetime.now().isoformat(),
            'target_user': target_user,
            'conversations': [],
            'total_messages': 0,
            'total_conversations': 0
        }
        
        try:
            # Get DM threads
            self.log("📥 Fetching DM threads...", 'working')
            threads = self.client.direct_threads()
            self.log(f"Found {len(threads)} conversations", 'found')
            
            # Process conversations
            processed = 0
            for thread in threads[:max_conversations]:
                try:
                    # Thread info
                    conversation = {
                        'thread_id': thread.id,
                        'participants': [],
                        'messages': [],
                        'last_activity': thread.last_activity_at.isoformat() if thread.last_activity_at else None,
                        'message_count': 0
                    }
                    
                    # Get participants
                    for user in thread.users:
                        participant = {
                            'username': user.username,
                            'full_name': user.full_name,
                            'user_id': str(user.pk),
                            'is_verified': user.is_verified,
                            'profile_pic_url': user.profile_pic_url
                        }
                        conversation['participants'].append(participant)
                    
                    # Check if target user filter applies
                    if target_user:
                        usernames = [p['username'] for p in conversation['participants']]
                        if target_user not in usernames:
                            continue
                    
                    self.log(f"💬 Processing conversation with: {', '.join([p['username'] for p in conversation['participants']])}", 'working')
                    
                    # Get messages
                    messages = self.client.direct_messages(thread.id, amount=max_messages_per_conversation)
                    
                    for msg in messages:
                        message = {
                            'message_id': msg.id,
                            'sender_id': str(msg.user_id),
                            'timestamp': msg.timestamp.isoformat(),
                            'text': msg.text or '',
                            'message_type': msg.item_type,
                            'media': None
                        }
                        
                        # Handle different message types
                        if hasattr(msg, 'media_share') and msg.media_share:
                            message['media'] = {
                                'type': 'media_share',
                                'media_id': str(msg.media_share.pk),
                                'media_type': msg.media_share.media_type
                            }
                        elif hasattr(msg, 'clip') and msg.clip:
                            message['media'] = {
                                'type': 'video',
                                'video_url': msg.clip.video_url if hasattr(msg.clip, 'video_url') else None
                            }
                        elif hasattr(msg, 'photo') and msg.photo:
                            message['media'] = {
                                'type': 'photo', 
                                'photo_url': msg.photo.thumbnail_url if hasattr(msg.photo, 'thumbnail_url') else None
                            }
                        elif hasattr(msg, 'voice_media') and msg.voice_media:
                            message['media'] = {
                                'type': 'voice',
                                'audio_url': msg.voice_media.audio.audio_url if hasattr(msg.voice_media, 'audio') else None
                            }
                        
                        conversation['messages'].append(message)
                    
                    conversation['message_count'] = len(conversation['messages'])
                    dm_data['conversations'].append(conversation)
                    dm_data['total_messages'] += conversation['message_count']
                    processed += 1
                    
                    self.log(f"✅ Extracted {conversation['message_count']} messages", 'success')
                    
                    # Human-like delay
                    await asyncio.sleep(random.uniform(2, 5))
                    
                except Exception as e:
                    self.log(f"❌ Error processing conversation: {str(e)}", 'error')
                    continue
            
            dm_data['total_conversations'] = len(dm_data['conversations'])
            
            # Logout
            try:
                self.client.logout()
                self.log("🚪 Logged out successfully", 'success')
            except:
                pass
                
            self.log(f"🎉 Extraction complete! {dm_data['total_messages']} messages from {dm_data['total_conversations']} conversations", 'success')
            return dm_data
            
        except Exception as e:
            self.log(f"💔 Extraction failed: {str(e)}", 'error')
            return None

async def main():
    """Main function"""
    print("💀📱 Instagram DM Extractor 💀📱")
    print("=" * 50)
    
    # Get user input
    username = input("📧 Instagram username: ").strip()
    if not username:
        print("❌ Username required!")
        return
        
    password = input("🔐 Instagram password: ").strip()  
    if not password:
        print("❌ Password required!")
        return
        
    target_user = input("🎯 Target specific user (optional): ").strip()
    target_user = target_user if target_user else None
    
    # Initialize extractor
    extractor = InstagramDMExtractor()
    
    # Extract DMs
    result = await extractor.extract_dms(username, password, target_user)
    
    if result:
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"instagram_dms_{username}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 RESULTS SUMMARY")
        print("=" * 30)
        print(f"💬 Total conversations: {result['total_conversations']}")
        print(f"📝 Total messages: {result['total_messages']}")
        print(f"💾 Saved to: {filename}")
        
        # Show conversation preview
        if result['conversations']:
            print(f"\n🔍 CONVERSATION PREVIEW:")
            for i, conv in enumerate(result['conversations'][:3], 1):
                participants = [p['username'] for p in conv['participants']]
                print(f"  {i}. {', '.join(participants)} ({conv['message_count']} messages)")
                
    else:
        print("❌ Extraction failed!")

if __name__ == "__main__":
    asyncio.run(main())
