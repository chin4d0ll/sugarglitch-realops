#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 INSTAGRAM SESSION REUSER
ใช้งาน session ที่มีอยู่แล้วเพื่อดึงข้อมูลแชทจริง
"""

import json
import time
import os
from datetime import datetime
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired

class InstagramSessionReuser:
    def __init__(self):
        self.username = "alx.trading"
        self.session_file = "session.json"
        self.cl = Client()
        
        # ตั้งค่าให้ปลอดภัย
        self.cl.delay_range = [2, 8]
        
    def load_session(self):
        """โหลด session ที่มีอยู่"""
        print("🔐 Loading existing session...")
        
        try:
            if not os.path.exists(self.session_file):
                print(f"❌ Session file {self.session_file} not found")
                return False
            
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            
            print(f"📄 Session file loaded")
            
            # ตรวจสอบว่ามี sessionid หรือไม่
            if 'sessionid' in session_data:
                sessionid = session_data['sessionid']
                print(f"🔑 SessionID: {sessionid[:20]}...")
                
                # ใช้ sessionid login
                result = self.cl.login_by_sessionid(sessionid)
                
                if result:
                    print("✅ Session login successful!")
                    return True
                else:
                    print("❌ Session login failed")
                    return False
            else:
                print("❌ No sessionid found in session file")
                return False
                
        except Exception as e:
            print(f"❌ Session load error: {e}")
            return False
    
    def test_session(self):
        """ทดสอบ session ว่าใช้งานได้หรือไม่"""
        print("🧪 Testing session...")
        
        try:
            # ลองดึงข้อมูลบัญชี
            account_info = self.cl.account_info()
            
            print(f"✅ Session works!")
            print(f"👤 Username: {account_info.username}")
            print(f"🆔 User ID: {account_info.pk}")
            print(f"👥 Followers: {account_info.follower_count}")
            print(f"👤 Following: {account_info.following_count}")
            
            return True
            
        except LoginRequired:
            print("❌ Session expired - login required")
            return False
        except ChallengeRequired:
            print("⚠️ Challenge required")
            return False
        except Exception as e:
            print(f"❌ Session test failed: {e}")
            return False
    
    def get_direct_messages(self, limit=20):
        """ดึงข้อมูล direct messages"""
        print(f"📥 Getting direct messages (limit: {limit})...")
        
        try:
            # ดึง thread list
            threads = self.cl.direct_threads(limit)
            
            print(f"📊 Found {len(threads)} conversation threads")
            
            conversations = []
            
            for thread in threads:
                print(f"\n💬 Thread ID: {thread.id}")
                print(f"👥 Users: {len(thread.users)} participants")
                
                # ดึงข้อมูลผู้ใช้ในการสนทนา
                for user in thread.users:
                    print(f"   👤 {user.username} ({user.full_name})")
                
                # ดึงข้อความล่าสุด
                messages = self.cl.direct_messages(thread.id, limit=10)
                print(f"   📝 Messages: {len(messages)}")
                
                conversation_data = {
                    'thread_id': thread.id,
                    'users': [{'username': u.username, 'full_name': u.full_name, 'pk': u.pk} for u in thread.users],
                    'messages_count': len(messages),
                    'last_activity': str(thread.last_activity_at),
                    'messages': []
                }
                
                # เก็บข้อความ
                for msg in messages[:5]:  # เก็บแค่ 5 ข้อความล่าสุด
                    message_data = {
                        'id': msg.id,
                        'text': msg.text if msg.text else '',
                        'timestamp': str(msg.timestamp),
                        'user_id': msg.user_id
                    }
                    conversation_data['messages'].append(message_data)
                
                conversations.append(conversation_data)
            
            # บันทึกข้อมูล
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"real_direct_messages_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(conversations, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"✅ Direct messages saved: {filename}")
            
            return conversations
            
        except Exception as e:
            print(f"❌ Failed to get direct messages: {e}")
            return None
    
    def find_women_contacts(self, conversations):
        """หาผู้หญิงจากการสนทนา"""
        print("🔍 Finding women contacts...")
        
        female_keywords = [
            'girl', 'lady', 'woman', 'princess', 'queen', 'baby', 'cute', 'pretty',
            'beauty', 'angel', 'sweet', 'lovely', 'miss', 'mrs', 'ms', 'she', 'her'
        ]
        
        women_contacts = []
        
        for conv in conversations:
            for user in conv['users']:
                username = user['username'].lower()
                full_name = user['full_name'].lower() if user['full_name'] else ''
                
                # ตรวจสอบคำสำคัญ
                is_female = False
                for keyword in female_keywords:
                    if keyword in username or keyword in full_name:
                        is_female = True
                        break
                
                if is_female:
                    women_contacts.append({
                        'username': user['username'],
                        'full_name': user['full_name'],
                        'user_id': user['pk'],
                        'thread_id': conv['thread_id'],
                        'messages_count': conv['messages_count'],
                        'last_activity': conv['last_activity']
                    })
        
        if women_contacts:
            print(f"✅ Found {len(women_contacts)} women contacts:")
            for woman in women_contacts:
                print(f"   👩 {woman['username']} ({woman['full_name']})")
            
            # บันทึกผลลัพธ์
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"women_contacts_from_dm_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(women_contacts, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Women contacts saved: {filename}")
        else:
            print("❌ No women contacts found")
        
        return women_contacts
    
    def get_user_info(self, username):
        """ดึงข้อมูลของ user"""
        try:
            user_info = self.cl.user_info_by_username(username)
            return {
                'username': user_info.username,
                'full_name': user_info.full_name,
                'biography': user_info.biography,
                'follower_count': user_info.follower_count,
                'following_count': user_info.following_count,
                'media_count': user_info.media_count,
                'is_private': user_info.is_private
            }
        except Exception as e:
            print(f"❌ Failed to get user info for {username}: {e}")
            return None
    
    def run_full_extraction(self):
        """รัน extraction แบบเต็ม"""
        print("🚀 INSTAGRAM SESSION REUSER - FULL EXTRACTION")
        print("=" * 60)
        print(f"👤 Target: {self.username}")
        print()
        
        # Step 1: Load session
        if not self.load_session():
            print("❌ Cannot load session. Need fresh login.")
            return False
        
        # Step 2: Test session
        if not self.test_session():
            print("❌ Session not working. Need fresh login.")
            return False
        
        print("\n" + "=" * 60)
        
        # Step 3: Get direct messages
        conversations = self.get_direct_messages(30)
        
        if not conversations:
            print("❌ No conversations found")
            return False
        
        print("\n" + "=" * 60)
        
        # Step 4: Find women
        women = self.find_women_contacts(conversations)
        
        print("\n" + "=" * 60)
        print("🎉 EXTRACTION COMPLETE!")
        print(f"📊 Total conversations: {len(conversations)}")
        print(f"👩 Women contacts found: {len(women)}")
        
        return True

def main():
    reuser = InstagramSessionReuser()
    reuser.run_full_extraction()

if __name__ == "__main__":
    main()
