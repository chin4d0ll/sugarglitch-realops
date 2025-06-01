#!/usr/bin/env python3
"""
💀📱 Instagram DM Extractor - Enhanced Version 💀📱
=================================================
เครื่องมือดึง DMs จาก Instagram ที่ปรับปรุงแล้ว
พร้อมการป้องกันและจัดการข้อผิดพลาดที่ดีกว่า

New Features:
- 🔐 Password masking and validation
- 🛡️ Better error handling 
- 💾 Session persistence
- 🎯 Smart retry mechanism
- 📊 Progress indicators
- 🌐 Proxy support
"""

import asyncio
import json
import time
import random
import getpass
import os
from datetime import datetime
from pathlib import Path
import re

try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes, ChallengeRequired
except ImportError:
    print("❌ Please install instagrapi: pip install instagrapi")
    exit(1)

class EnhancedInstagramDMExtractor:
    def __init__(self):
        self.client = Client()
        self.client.delay_range = [1, 3]
        
        # Session file for persistence
        self.session_file = Path.home() / ".instagram_dm_session.json"
        
        # Progress tracking
        self.current_conversation = 0
        self.total_conversations = 0
        
    def log(self, message, level='info'):
        """Enhanced logging with colors"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        icons = {
            'info': '💙',
            'success': '✅', 
            'error': '❌',
            'working': '⚡',
            'found': '🔍',
            'warning': '⚠️'
        }
        
        # ANSI color codes
        colors = {
            'info': '\033[36m',      # Cyan
            'success': '\033[32m',   # Green
            'error': '\033[31m',     # Red
            'working': '\033[33m',   # Yellow
            'found': '\033[35m',     # Magenta
            'warning': '\033[93m',   # Bright Yellow
            'reset': '\033[0m'       # Reset
        }
        
        icon = icons.get(level, '💙')
        color = colors.get(level, colors['info'])
        reset = colors['reset']
        
        print(f"{color}[{timestamp}] {icon} {message}{reset}")
    
    def validate_username(self, username):
        """Validate Instagram username format"""
        if not username:
            return False, "Username ห้ามว่าง"
        
        if len(username) < 3:
            return False, "Username สั้นเกินไป (ต้องมีอย่างน้อย 3 ตัวอักษร)"
        
        if not re.match(r'^[a-zA-Z0-9_.]+$', username):
            return False, "Username มีตัวอักษรที่ไม่รองรับ (ใช้ได้เฉพาะ a-z, A-Z, 0-9, _, .)"
        
        return True, "Username ถูกต้อง"
    
    def validate_password(self, password):
        """Validate password strength"""
        if not password:
            return False, "รหัสผ่านห้ามว่าง"
        
        if len(password) < 6:
            return False, "รหัสผ่านสั้นเกินไป (ต้องมีอย่างน้อย 6 ตัวอักษร)"
        
        # Check strength
        strength_score = 0
        checks = []
        
        if len(password) >= 8:
            strength_score += 1
            checks.append("✅ ความยาวเพียงพอ")
        else:
            checks.append("❌ สั้นเกินไป")
        
        if any(c.isupper() for c in password):
            strength_score += 1
            checks.append("✅ มีตัวพิมพ์ใหญ่")
        else:
            checks.append("⚠️ ไม่มีตัวพิมพ์ใหญ่")
        
        if any(c.islower() for c in password):
            strength_score += 1
            checks.append("✅ มีตัวพิมพ์เล็ก")
        else:
            checks.append("⚠️ ไม่มีตัวพิมพ์เล็ก")
        
        if any(c.isdigit() for c in password):
            strength_score += 1
            checks.append("✅ มีตัวเลข")
        else:
            checks.append("⚠️ ไม่มีตัวเลข")
        
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if any(c in special_chars for c in password):
            strength_score += 1
            checks.append("✅ มีอักขระพิเศษ")
        else:
            checks.append("⚠️ ไม่มีอักขระพิเศษ")
        
        # Determine strength level
        if strength_score <= 2:
            strength = "🔴 อ่อน"
        elif strength_score <= 3:
            strength = "🟡 ปานกลาง"
        elif strength_score <= 4:
            strength = "🟢 ดี"
        else:
            strength = "💚 แข็งแกร่ง"
        
        return True, f"รหัสผ่าน: {strength}"
    
    def get_credentials(self):
        """Get and validate user credentials"""
        print("🔐 ข้อมูลการเข้าสู่ระบบ Instagram")
        print("=" * 50)
        
        # Get username
        while True:
            username = input("📧 Instagram username: ").strip()
            is_valid, message = self.validate_username(username)
            
            if is_valid:
                self.log(message, 'success')
                break
            else:
                self.log(message, 'error')
                continue
        
        # Get password
        while True:
            password = getpass.getpass("🔐 Instagram password: ")
            is_valid, message = self.validate_password(password)
            
            if is_valid:
                self.log(message, 'info')
                
                # Ask for confirmation if password is weak
                if "🔴" in message:
                    confirm = input("⚠️ รหัสผ่านอ่อน ต้องการดำเนินการต่อ? (y/N): ").strip().lower()
                    if confirm not in ['y', 'yes', 'ใช่']:
                        continue
                break
            else:
                self.log(message, 'error')
                continue
        
        return username, password
    
    def save_session(self, username):
        """Save session for future use"""
        try:
            session_data = {
                'username': username,
                'last_login': datetime.now().isoformat(),
                'settings': self.client.get_settings()
            }
            
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            self.log("💾 บันทึก session แล้ว", 'success')
            
        except Exception as e:
            self.log(f"⚠️ ไม่สามารถบันทึก session: {e}", 'warning')
    
    def load_session(self, username):
        """Load saved session"""
        try:
            if not self.session_file.exists():
                return False
            
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            
            if session_data.get('username') == username:
                self.client.set_settings(session_data.get('settings', {}))
                self.log("💡 โหลด session ที่บันทึกไว้", 'info')
                return True
                
        except Exception as e:
            self.log(f"⚠️ ไม่สามารถโหลด session: {e}", 'warning')
        
        return False
    
    async def login_with_retry(self, username, password, max_attempts=3):
        """Login with enhanced retry mechanism"""
        
        # Try to load existing session first
        if self.load_session(username):
            try:
                # Test if session is still valid
                self.client.account_info()
                self.log("✅ ใช้ session ที่บันทึกไว้สำเร็จ!", 'success')
                return True
            except:
                self.log("⚠️ Session หมดอายุ กำลัง login ใหม่...", 'warning')
        
        for attempt in range(max_attempts):
            try:
                self.log(f"🔐 กำลัง login (ครั้งที่ {attempt + 1}/{max_attempts})...", 'working')
                
                self.client.login(username, password)
                self.log("✅ Login สำเร็จ!", 'success')
                
                # Save session for future use
                self.save_session(username)
                
                return True
                
            except ChallengeRequired as e:
                self.log("🚨 ต้องการการยืนยันตัวตน", 'error')
                self.log("💡 กรุณาเปิด Instagram app และยืนยันการเข้าสู่ระบบ", 'info')
                
                choice = input("📱 ยืนยันแล้ว กด Enter เพื่อดำเนินการต่อ หรือ 'q' เพื่อออก: ").strip().lower()
                if choice == 'q':
                    return False
                continue
                
            except PleaseWaitFewMinutes:
                wait_time = 300 + (attempt * 120)  # Increasing wait time
                self.log(f"⏰ ถูก rate limit รอ {wait_time//60} นาที...", 'warning')
                
                for remaining in range(wait_time, 0, -30):
                    print(f"\r⏱️ รออีก {remaining//60}:{remaining%60:02d} นาที...", end='', flush=True)
                    await asyncio.sleep(30)
                print()
                
            except Exception as e:
                self.log(f"❌ Login ล้มเหลว: {str(e)}", 'error')
                if attempt < max_attempts - 1:
                    wait_time = 10 + (attempt * 5)
                    self.log(f"🔄 รอ {wait_time} วินาทีแล้วลองใหม่...", 'working')
                    await asyncio.sleep(wait_time)
                    
        return False
    
    def show_progress(self, current, total, message=""):
        """Show progress bar"""
        if total == 0:
            return
        
        percent = (current / total) * 100
        bar_length = 30
        filled_length = int(bar_length * current // total)
        
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        print(f"\r⏳ [{bar}] {percent:.1f}% ({current}/{total}) {message}", end='', flush=True)
        
        if current == total:
            print()  # New line when complete
    
    async def extract_dms(self, username, password, target_user=None, max_conversations=20, max_messages_per_conversation=100):
        """
        Enhanced DM extraction with better progress tracking
        """
        
        self.log(f"💀 เริ่มดึง DMs สำหรับ {username}", 'working')
        
        # Login
        if not await self.login_with_retry(username, password):
            return None
            
        dm_data = {
            'extractor': 'Enhanced Instagram DM Extractor v2.0',
            'username': username,
            'extraction_time': datetime.now().isoformat(),
            'target_user': target_user,
            'conversations': [],
            'total_messages': 0,
            'total_conversations': 0
        }
        
        try:
            # Get DM threads
            self.log("📥 กำลังดึงรายการการสนทนา...", 'working')
            threads = self.client.direct_threads()
            
            available_threads = threads[:max_conversations]
            self.total_conversations = len(available_threads)
            
            self.log(f"🔍 พบ {len(threads)} การสนทนา (จะประมวลผล {len(available_threads)} การสนทนา)", 'found')
            
            # Process conversations
            for i, thread in enumerate(available_threads, 1):
                try:
                    self.current_conversation = i
                    
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
                    
                    participant_names = [p['username'] for p in conversation['participants']]
                    
                    # Check target user filter
                    if target_user and target_user not in participant_names:
                        self.show_progress(i, self.total_conversations, f"ข้าม: {', '.join(participant_names)}")
                        continue
                    
                    self.show_progress(i, self.total_conversations, f"ประมวลผล: {', '.join(participant_names)}")
                    
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
                        
                        # Handle media
                        if hasattr(msg, 'media_share') and msg.media_share:
                            message['media'] = {
                                'type': 'media_share',
                                'media_id': str(msg.media_share.pk)
                            }
                        elif hasattr(msg, 'clip') and msg.clip:
                            message['media'] = {
                                'type': 'video',
                                'video_url': getattr(msg.clip, 'video_url', None)
                            }
                        elif hasattr(msg, 'photo') and msg.photo:
                            message['media'] = {
                                'type': 'photo',
                                'photo_url': getattr(msg.photo, 'thumbnail_url', None)
                            }
                        elif hasattr(msg, 'voice_media') and msg.voice_media:
                            message['media'] = {
                                'type': 'voice',
                                'audio_url': getattr(msg.voice_media.audio, 'audio_url', None) if hasattr(msg.voice_media, 'audio') else None
                            }
                        
                        conversation['messages'].append(message)
                    
                    conversation['message_count'] = len(conversation['messages'])
                    dm_data['conversations'].append(conversation)
                    dm_data['total_messages'] += conversation['message_count']
                    
                    # Human-like delay
                    await asyncio.sleep(random.uniform(2, 4))
                    
                except Exception as e:
                    self.log(f"❌ ข้อผิดพลาดในการประมวลผลการสนทนา: {str(e)}", 'error')
                    continue
            
            dm_data['total_conversations'] = len(dm_data['conversations'])
            
            # Logout
            try:
                self.client.logout()
                self.log("🚪 ออกจากระบบแล้ว", 'success')
            except:
                pass
                
            self.log(f"🎉 การดึงข้อมูลเสร็จสิ้น! {dm_data['total_messages']} ข้อความจาก {dm_data['total_conversations']} การสนทนา", 'success')
            return dm_data
            
        except Exception as e:
            self.log(f"💔 การดึงข้อมูลล้มเหลว: {str(e)}", 'error')
            return None

async def main():
    """Main function with enhanced UI"""
    print("💀📱 Enhanced Instagram DM Extractor 💀📱")
    print("=" * 60)
    print("🚀 เครื่องมือดึง DMs ที่ปรับปรุงแล้ว")
    print("✨ ความสามารถใหม่: การตรวจสอบรหัสผ่าน, session persistence, progress tracking")
    print("=" * 60)
    
    # Initialize extractor
    extractor = EnhancedInstagramDMExtractor()
    
    # Get credentials
    username, password = extractor.get_credentials()
    
    # Get options
    print("\n⚙️ ตัวเลือกการดึงข้อมูล")
    print("-" * 30)
    
    target_user = input("🎯 ระบุผู้ใช้เป้าหมาย (ไม่ระบุ = ทั้งหมด): ").strip()
    target_user = target_user if target_user else None
    
    try:
        max_conversations = int(input("💬 จำนวนการสนทนาสูงสุด [20]: ") or "20")
        max_messages = int(input("📝 ข้อความต่อการสนทนา [100]: ") or "100")
    except ValueError:
        max_conversations = 20
        max_messages = 100
    
    # Confirmation
    print(f"\n🔍 สรุปการตั้งค่า:")
    print(f"👤 Username: {username}")
    print(f"🎯 Target: {target_user or 'ทั้งหมด'}")
    print(f"💬 Max conversations: {max_conversations}")
    print(f"📝 Messages per conversation: {max_messages}")
    
    confirm = input("\n✅ ยืนยันการดำเนินการ? (Y/n): ").strip().lower()
    if confirm in ['n', 'no', 'ไม่']:
        print("❌ ยกเลิกการดำเนินการ")
        return
    
    # Extract DMs
    result = await extractor.extract_dms(username, password, target_user, max_conversations, max_messages)
    
    if result:
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"enhanced_instagram_dms_{username}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 สรุปผลลัพธ์")
        print("=" * 40)
        print(f"💬 การสนทนาทั้งหมด: {result['total_conversations']}")
        print(f"📝 ข้อความทั้งหมด: {result['total_messages']}")
        print(f"💾 บันทึกไฟล์: {filename}")
        
        # Show conversation preview
        if result['conversations']:
            print(f"\n🔍 ตัวอย่างการสนทนา:")
            for i, conv in enumerate(result['conversations'][:5], 1):
                participants = [p['username'] for p in conv['participants']]
                print(f"  {i}. {', '.join(participants)} ({conv['message_count']} ข้อความ)")
            
            if len(result['conversations']) > 5:
                print(f"  ... และอีก {len(result['conversations']) - 5} การสนทนา")
        
        print(f"\n✅ การดึงข้อมูลเสร็จสิ้นสมบูรณ์!")
        
    else:
        print("❌ การดึงข้อมูลล้มเหลว!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚡ การดำเนินการถูกยกเลิกโดยผู้ใช้")
    except Exception as e:
        print(f"\n💔 ข้อผิดพลาดที่ไม่คาดคิด: {e}")
