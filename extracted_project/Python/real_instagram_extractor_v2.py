#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ดึงข้อมูลแชทจริงๆ จาก Instagram โดยใช้ session ที่ล็อคอินได้แล้ว (เวอร์ชัน 2)
Extract real chat data from Instagram using authenticated session (Version 2)
"""

import requests
import json
import time
from datetime import datetime

def load_real_session():
    """โหลด session จริงที่ล็อคอินได้แล้ว"""
    try:
        with open('session.json', 'r') as f:
            session_data = json.load(f)
        print("✅ โหลด session จริงสำเร็จ!")
        print(f"📱 User ID: {session_data.get('ds_user_id')}")
        print(f"🔑 Session ID: {session_data.get('sessionid')[:20]}...")
        return session_data
    except Exception as e:
        print(f"❌ ไม่สามารถโหลด session: {e}")
        return None

def create_instagram_session(session_data):
    """สร้าง session สำหรับ Instagram API"""
    session = requests.Session()
    
    # ตั้งค่า headers ให้เหมือน app Instagram จริง
    session.headers.update({
        'User-Agent': 'Instagram 219.0.0.12.117 Android (29/10; 420dpi; 1080x2280; samsung; SM-G975F; beyond2; exynos9820; en_US; 336448914)',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-IG-App-ID': '936619743392459',
        'X-IG-Android-ID': 'android-1234567890abcdef',
        'X-IG-Capabilities': '3brTv10=',
        'X-IG-Connection-Type': 'WIFI',
        'X-IG-Bandwidth-Speed-KBPS': '2000.000',
        'X-IG-Bandwidth-TotalBytes-B': '0',
        'X-IG-Bandwidth-TotalTime-MS': '0',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    })
    
    # ตั้งค่า cookies
    session.cookies.set('sessionid', session_data['sessionid'], domain='.instagram.com')
    session.cookies.set('ds_user_id', session_data['ds_user_id'], domain='.instagram.com')
    session.cookies.set('ig_did', 'B1C2D3E4-F5A6-7890-CDEF-123456789ABC', domain='.instagram.com')
    session.cookies.set('ig_nrcb', '1', domain='.instagram.com')
    session.cookies.set('csrftoken', 'abcdef1234567890', domain='.instagram.com')
    
    return session

def get_inbox_threads(session):
    """ดึงรายการ threads จาก inbox"""
    
    # ลอง API endpoints หลายตัว
    api_endpoints = [
        "https://i.instagram.com/api/v1/direct_v2/inbox/",
        "https://i.instagram.com/api/v1/direct_v2/threads/",
        "https://www.instagram.com/api/v1/direct_v2/inbox/",
    ]
    
    for endpoint in api_endpoints:
        try:
            print(f"🔍 ลอง endpoint: {endpoint}")
            response = session.get(endpoint, timeout=30)
            
            print(f"📡 Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ ดึงข้อมูลสำเร็จ!")
                return data
            elif response.status_code == 401:
                print("❌ Session หมดอายุ")
            elif response.status_code == 429:
                print("⏰ Rate limited - รอ 60 วินาที...")
                time.sleep(60)
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            continue
    
    return None

def extract_conversations_from_inbox(inbox_data):
    """แยกข้อมูลการสนทนาจาก inbox response"""
    
    if not inbox_data:
        return []
    
    conversations = []
    
    # ลองหา threads ในโครงสร้างต่างๆ
    threads = None
    if 'inbox' in inbox_data and 'threads' in inbox_data['inbox']:
        threads = inbox_data['inbox']['threads']
    elif 'threads' in inbox_data:
        threads = inbox_data['threads']
    elif 'data' in inbox_data:
        threads = inbox_data['data']
    
    if not threads:
        print("❌ ไม่พบ threads ในข้อมูล")
        return []
    
    print(f"📋 พบ {len(threads)} threads")
    
    for thread in threads:
        try:
            thread_id = thread.get('thread_id', 'unknown')
            
            # ดึงข้อมูลผู้ใช้
            users = thread.get('users', [])
            participants = []
            
            for user in users:
                username = user.get('username', 'unknown')
                full_name = user.get('full_name', '')
                is_verified = user.get('is_verified', False)
                
                participants.append({
                    'username': username,
                    'full_name': full_name,
                    'is_verified': is_verified
                })
            
            # ดึงข้อความล่าสุด
            items = thread.get('items', [])
            message_count = len(items)
            last_message = ""
            
            if items:
                last_item = items[0]
                if 'text' in last_item:
                    last_message = last_item['text']
                elif 'item_type' in last_item:
                    last_message = f"[{last_item['item_type']}]"
            
            conversation = {
                'thread_id': thread_id,
                'participants': participants,
                'message_count': message_count,
                'last_message': last_message,
                'last_activity': thread.get('last_activity_at', ''),
                'thread_title': thread.get('thread_title', '')
            }
            
            conversations.append(conversation)
            
        except Exception as e:
            print(f"❌ Error processing thread: {e}")
            continue
    
    return conversations

def identify_female_contacts(conversations):
    """ระบุผู้หญิงจากการสนทนา"""
    
    female_keywords = [
        'girl', 'queen', 'princess', 'babe', 'baby', 'cutie', 'angel',
        'beauty', 'lovely', 'sweet', 'honey', 'darling', 'gorgeous',
        'miss', 'lady', 'woman', 'female'
    ]
    
    thai_female_names = [
        'นิด', 'นิม', 'น้อย', 'นิ้ง', 'มิ้นต์', 'มิลค์', 'ปลอย', 'ปิ่น',
        'เฟิร์น', 'ฟาง', 'บี', 'บีม', 'เบล', 'กิ๊ฟ', 'จิ๋ว', 'เจน',
        'ดรีม', 'คิว', 'เค', 'เคท', 'คิม', 'วิว', 'เมย์', 'ยิ้ม'
    ]
    
    english_female_names = [
        'alice', 'anna', 'amy', 'bella', 'emma', 'grace', 'jenny', 'julia',
        'kate', 'kim', 'lisa', 'lucy', 'maria', 'mary', 'nancy', 'rose',
        'sara', 'sophie', 'tina', 'nina', 'mia', 'zoe', 'eva', 'ivy'
    ]
    
    all_female_indicators = female_keywords + thai_female_names + english_female_names
    
    female_contacts = []
    
    for conv in conversations:
        for participant in conv['participants']:
            username = participant['username'].lower()
            full_name = participant.get('full_name', '').lower()
            
            # ตรวจสอบในชื่อผู้ใช้และชื่อจริง
            text_to_check = f"{username} {full_name}"
            
            is_female = any(indicator in text_to_check for indicator in all_female_indicators)
            
            if is_female:
                female_contacts.append({
                    'username': participant['username'],
                    'full_name': participant.get('full_name', ''),
                    'is_verified': participant.get('is_verified', False),
                    'thread_id': conv['thread_id'],
                    'message_count': conv['message_count'],
                    'last_message': conv['last_message'],
                    'indicators_found': [ind for ind in all_female_indicators if ind in text_to_check]
                })
    
    return female_contacts

def main():
    print("🔍 ดึงข้อมูลแชทจริงๆ จาก Instagram (เวอร์ชัน 2)")
    print("Extracting REAL chat data from Instagram (Version 2)")
    print("=" * 70)
    
    # โหลด session จริง
    session_data = load_real_session()
    if not session_data:
        print("❌ ไม่มี session ให้ใช้")
        return
    
    # สร้าง Instagram session
    print("\n🔧 สร้าง Instagram session...")
    session = create_instagram_session(session_data)
    
    # ดึงข้อมูล inbox
    print("\n📥 ดึงข้อมูล inbox...")
    inbox_data = get_inbox_threads(session)
    
    if not inbox_data:
        print("❌ ไม่สามารถดึงข้อมูล inbox ได้")
        return
    
    # แยกข้อมูลการสนทนา
    print("\n💬 แยกข้อมูลการสนทนา...")
    conversations = extract_conversations_from_inbox(inbox_data)
    
    if not conversations:
        print("❌ ไม่พบการสนทนา")
        return
    
    print(f"✅ พบการสนทนา: {len(conversations)} รายการ")
    
    # ระบุผู้หญิงในการสนทนา
    print("\n👩 ระบุผู้หญิงในการสนทนา...")
    female_contacts = identify_female_contacts(conversations)
    
    # บันทึกข้อมูล
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"REAL_INSTAGRAM_CHATS_{timestamp}.json"
    
    output_data = {
        'extraction_info': {
            'timestamp': datetime.now().isoformat(),
            'target_account': 'alx.trading',
            'data_type': 'REAL_INSTAGRAM_DATA',
            'total_conversations': len(conversations),
            'total_female_contacts': len(female_contacts)
        },
        'conversations': conversations,
        'female_contacts': female_contacts
    }
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    # แสดงผล
    print(f"\n📊 ผลการดึงข้อมูลจริง:")
    print("=" * 50)
    print(f"💬 การสนทนาทั้งหมด: {len(conversations)}")
    print(f"👩 ผู้หญิงที่พบ: {len(female_contacts)}")
    
    if conversations:
        print(f"\n📋 ตัวอย่างการสนทนา:")
        for i, conv in enumerate(conversations[:5], 1):
            usernames = [p['username'] for p in conv['participants']]
            print(f"   {i}. {', '.join(usernames)} ({conv['message_count']} ข้อความ)")
            if conv['last_message']:
                print(f"      ล่าสุด: {conv['last_message'][:50]}...")
    
    if female_contacts:
        print(f"\n👩 ผู้หญิงที่พบ:")
        for i, contact in enumerate(female_contacts, 1):
            print(f"   {i}. @{contact['username']}")
            if contact['full_name']:
                print(f"      ชื่อ: {contact['full_name']}")
            print(f"      ข้อความ: {contact['message_count']} รายการ")
            if contact['last_message']:
                print(f"      ล่าสุด: {contact['last_message'][:50]}...")
            print(f"      คำที่พบ: {', '.join(contact['indicators_found'][:3])}")
            print()
    
    print(f"💾 ข้อมูลจริงบันทึกไว้ใน: {output_filename}")
    
    if female_contacts:
        print(f"\n🔴 สรุป: พบผู้หญิง {len(female_contacts)} คนที่ alx.trading คุยด้วยจริงๆ!")
        
        # สร้างรายงานสรุป
        summary_filename = f"REAL_WOMEN_SUMMARY_{timestamp}.txt"
        with open(summary_filename, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("ALX.TRADING - ผู้หญิงจริงที่คุยด้วย\n")
            f.write("REAL Women Contacts from Instagram\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"📅 วันที่: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"💬 การสนทนาทั้งหมด: {len(conversations)}\n")
            f.write(f"👩 ผู้หญิงที่พบ: {len(female_contacts)}\n\n")
            
            for i, contact in enumerate(female_contacts, 1):
                f.write(f"{i}. @{contact['username']}\n")
                if contact['full_name']:
                    f.write(f"   ชื่อจริง: {contact['full_name']}\n")
                f.write(f"   ข้อความ: {contact['message_count']} รายการ\n")
                if contact['last_message']:
                    f.write(f"   ข้อความล่าสุด: {contact['last_message'][:100]}...\n")
                f.write("\n")
        
        print(f"📄 สรุปผู้หญิงบันทึกไว้ใน: {summary_filename}")
    else:
        print(f"\n🟡 สรุป: ไม่พบผู้หญิงในข้อมูลที่ดึงได้")

if __name__ == "__main__":
    main()
