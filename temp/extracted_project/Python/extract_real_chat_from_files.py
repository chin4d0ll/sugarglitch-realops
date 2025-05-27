#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
แยกข้อมูลแชทจริงจากไฟล์ที่มีอยู่
Extract real chat data from existing files
"""

import json
import re
import os
from datetime import datetime

def search_for_chat_files():
    """หาไฟล์ที่มีข้อมูลแชทจริง"""
    
    print("🔍 ค้นหาไฟล์ที่มีข้อมูลแชทจริง...")
    
    # รายการไฟล์ที่อาจมีข้อมูลแชท
    potential_files = [
        'session.json',
        'breach_session.json',
        'output/al.txt',
        'attack_log.txt',
        'debug_log.txt'
    ]
    
    chat_data_files = []
    
    for filename in potential_files:
        if os.path.exists(filename):
            try:
                file_size = os.path.getsize(filename)
                print(f"   📁 {filename}: {file_size:,} bytes")
                
                # ตรวจสอบเนื้อหา
                if filename.endswith('.json'):
                    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                        data = json.load(f)
                        if 'chat' in str(data).lower() or 'message' in str(data).lower() or 'conversation' in str(data).lower():
                            chat_data_files.append((filename, 'json', data))
                            print(f"      ✅ พบข้อมูลแชทในไฟล์ JSON")
                
                elif filename.endswith('.txt'):
                    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if any(keyword in content.lower() for keyword in ['chat', 'message', 'conversation', 'direct', 'dm']):
                            chat_data_files.append((filename, 'text', content))
                            print(f"      ✅ พบข้อมูลแชทในไฟล์ text")
                            
            except Exception as e:
                print(f"      ❌ ไม่สามารถอ่านไฟล์ {filename}: {e}")
    
    return chat_data_files

def extract_conversations_from_json(data):
    """แยกการสนทนาจากข้อมูล JSON"""
    
    conversations = []
    messages = []
    
    def search_recursive(obj, path=""):
        """ค้นหาข้อมูลแชทแบบ recursive"""
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_path = f"{path}.{key}" if path else key
                
                # หาคีย์ที่เกี่ยวข้องกับแชท
                if any(keyword in key.lower() for keyword in ['chat', 'message', 'conversation', 'thread', 'direct', 'dm', 'inbox']):
                    if isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict):
                                conversations.append({
                                    'source_key': new_path,
                                    'data': item,
                                    'type': 'chat_data'
                                })
                    elif isinstance(value, dict):
                        conversations.append({
                            'source_key': new_path,
                            'data': value,
                            'type': 'chat_data'
                        })
                
                search_recursive(value, new_path)
                
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                search_recursive(item, f"{path}[{i}]")
    
    search_recursive(data)
    return conversations

def extract_conversations_from_text(content):
    """แยกการสนทนาจากข้อความ"""
    
    conversations = []
    
    # หา pattern ของการสนทนา
    patterns = [
        r'(?:chat|conversation|message|dm|direct).*?with.*?([a-zA-Z0-9_.]+)',
        r'([a-zA-Z0-9_.]+).*?(?:says?|said|messages?|texted?)',
        r'@([a-zA-Z0-9_.]+)',
        r'user[:\s]+([a-zA-Z0-9_.]+)',
        r'username[:\s]+([a-zA-Z0-9_.]+)',
        r'([a-zA-Z0-9_.]*(?:girl|queen|baby|princess|cutie|babe|honey)[a-zA-Z0-9_.]*)',
    ]
    
    found_users = set()
    
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                match = match[0]
            if len(match) > 2 and len(match) < 30:
                found_users.add(match.lower())
    
    # สร้างรายการการสนทนา
    for user in found_users:
        conversations.append({
            'username': user,
            'source': 'text_extraction',
            'type': 'potential_contact'
        })
    
    return conversations

def analyze_female_contacts_in_real_data(all_conversations):
    """วิเคราะห์ผู้หญิงในข้อมูลจริง"""
    
    female_indicators = [
        'girl', 'queen', 'princess', 'baby', 'babe', 'cutie', 'honey',
        'sweetheart', 'darling', 'angel', 'beauty', 'lovely', 'pretty',
        'นิด', 'นิม', 'น้อย', 'นิ้ง', 'มิ้นต์', 'มิลค์', 'เมย์', 'ปลอย',
        'เฟิร์น', 'บี', 'อิ๊ก', 'กิ๊ฟ', 'จิ๋ว', 'ดรีม', 'คิว', 'ลิง', 'วิว'
    ]
    
    female_contacts = []
    
    for conv in all_conversations:
        if 'username' in conv:
            username = conv['username']
            if any(indicator in username.lower() for indicator in female_indicators):
                female_contacts.append({
                    'username': username,
                    'confidence': 'high',
                    'indicators': [ind for ind in female_indicators if ind in username.lower()],
                    'source': conv.get('source', 'unknown')
                })
        
        elif 'data' in conv:
            data = conv['data']
            # ตรวจสอบข้อมูลในโครงสร้าง
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, str):
                        if any(indicator in value.lower() for indicator in female_indicators):
                            female_contacts.append({
                                'data_key': key,
                                'value': value,
                                'confidence': 'medium',
                                'indicators': [ind for ind in female_indicators if ind in value.lower()],
                                'source': conv.get('source_key', 'json_data')
                            })
    
    return female_contacts

def main():
    print("🔍 แยกข้อมูลแชทจริงจากไฟล์ที่มีอยู่")
    print("Extracting real chat data from existing files")
    print("=" * 60)
    
    # ค้นหาไฟล์ที่มีข้อมูลแชท
    chat_files = search_for_chat_files()
    
    if not chat_files:
        print("❌ ไม่พบไฟล์ที่มีข้อมูลแชท")
        return
    
    all_conversations = []
    
    # แยกข้อมูลจากแต่ละไฟล์
    for filename, file_type, data in chat_files:
        print(f"\n📂 วิเคราะห์ไฟล์: {filename}")
        print("-" * 40)
        
        if file_type == 'json':
            conversations = extract_conversations_from_json(data)
            print(f"   📊 พบข้อมูลแชท: {len(conversations)} รายการ")
            all_conversations.extend(conversations)
            
        elif file_type == 'text':
            conversations = extract_conversations_from_text(data)
            print(f"   📊 พบผู้ใช้: {len(conversations)} คน")
            all_conversations.extend(conversations)
    
    print(f"\n📊 สรุปข้อมูลทั้งหมด:")
    print(f"   • รายการทั้งหมด: {len(all_conversations)}")
    
    # วิเคราะห์ผู้หญิง
    print(f"\n👩 วิเคราะห์ผู้หญิงในข้อมูลจริง...")
    female_contacts = analyze_female_contacts_in_real_data(all_conversations)
    
    if female_contacts:
        print(f"✅ พบผู้หญิง {len(female_contacts)} คน:")
        
        for i, contact in enumerate(female_contacts[:10], 1):  # แสดงแค่ 10 คนแรก
            if 'username' in contact:
                print(f"   {i}. 👩 {contact['username']} (indicators: {', '.join(contact['indicators'])})")
            elif 'value' in contact:
                print(f"   {i}. 📝 {contact['data_key']}: {contact['value'][:50]}...")
    else:
        print("❌ ไม่พบผู้หญิงที่ชัดเจนในข้อมูลนี้")
    
    # บันทึกผลลัพธ์
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_filename = f"extracted_real_chat_data_{timestamp}.json"
    
    result_data = {
        'extraction_timestamp': datetime.now().isoformat(),
        'source_files': [f[0] for f in chat_files],
        'total_conversations': len(all_conversations),
        'female_contacts': female_contacts,
        'all_conversations': all_conversations[:50]  # เก็บแค่ 50 รายการแรก
    }
    
    with open(result_filename, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 บันทึกผลลัพธ์แล้ว: {result_filename}")
    
    # สรุปผล
    if female_contacts:
        print(f"\n🎯 สรุป:")
        print(f"✅ พบข้อมูลแชทจริงที่มีผู้หญิง {len(female_contacts)} คน!")
        print(f"📊 แหล่งข้อมูล: {len(chat_files)} ไฟล์")
        
        high_confidence = [c for c in female_contacts if c.get('confidence') == 'high']
        if high_confidence:
            print(f"🔴 ความเชื่อมั่นสูง: {len(high_confidence)} คน")
            for contact in high_confidence[:5]:
                if 'username' in contact:
                    print(f"   • {contact['username']}")
    else:
        print(f"\n🟡 สรุป:")
        print(f"ไม่พบผู้หญิงที่ชัดเจนในข้อมูลที่ดึงมาได้")
        print(f"แต่ข้อมูลจาก output/al.txt ที่เราวิเคราะห์ไว้แล้วแสดงให้เห็นการติดต่อกับผู้หญิงมากมาย")

if __name__ == "__main__":
    main()
