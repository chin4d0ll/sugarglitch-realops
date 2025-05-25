#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
วิเคราะห์การสนทนาเฉพาะบุคคลกับผู้หญิง
Analyze specific conversations with women
"""

import json
import re
import os
from datetime import datetime

def extract_conversation_snippets(text, target_usernames):
    """หาส่วนของการสนทนาที่เกี่ยวข้องกับ username ที่น่าสนใจ"""
    
    conversations = {}
    
    for username in target_usernames:
        # หาส่วนที่มี username นี้
        pattern = rf'.{{0,100}}{re.escape(username)}.{{0,100}}'
        matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
        
        if matches:
            conversations[username] = {
                'count': len(matches),
                'snippets': matches[:5]  # เก็บแค่ 5 ตัวอย่างแรก
            }
    
    return conversations

def find_real_names_in_conversations(text):
    """หาชื่อจริงของผู้หญิงในการสนทนา"""
    
    # Pattern สำหรับหาชื่อจริง
    name_patterns = [
        r'ชื่อ\s*([ก-๙a-zA-Z]+)',
        r'เรียก\s*([ก-๙a-zA-Z]+)',
        r'name\s+is\s+([a-zA-Z]+)',
        r'call\s+me\s+([a-zA-Z]+)',
        r'my\s+name\s+([a-zA-Z]+)',
        r'i\'m\s+([a-zA-Z]+)',
        r'สวัสดี\s*([ก-๙a-zA-Z]+)',
        r'hello\s+([a-zA-Z]+)',
    ]
    
    found_names = set()
    
    for pattern in name_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if len(match) > 1 and len(match) < 20:  # ชื่อที่มีความยาวสมเหตุสมผล
                found_names.add(match.lower())
    
    return list(found_names)

def analyze_relationship_context(text):
    """วิเคราะห์บริบทความสัมพันธ์"""
    
    relationship_indicators = {
        'romantic': [
            r'รัก', r'love', r'ที่รัก', r'darling', r'honey', r'sweetheart',
            r'kiss', r'จูบ', r'hug', r'กอด', r'miss\s+you', r'คิดถึง'
        ],
        'intimate': [
            r'เซ็กซ์', r'sex', r'make\s+love', r'sleep\s+together',
            r'นอนด้วยกัน', r'ที่นอน', r'bedroom', r'bed'
        ],
        'emotional': [
            r'เศร้า', r'sad', r'เหงา', r'lonely', r'ผิดหวัง', r'disappointed',
            r'happy', r'ดีใจ', r'excited', r'ตื่นเต้น'
        ],
        'meetup': [
            r'เจอกัน', r'meet', r'พบกัน', r'ไปด้วยกัน', r'go\s+together',
            r'date', r'เดท', r'dinner', r'ข้าวเย็น', r'lunch', r'ข้าวเที่ยง'
        ]
    }
    
    found_contexts = {}
    
    for category, patterns in relationship_indicators.items():
        matches = []
        for pattern in patterns:
            found = re.findall(pattern, text, re.IGNORECASE)
            matches.extend(found)
        
        if matches:
            found_contexts[category] = len(matches)
    
    return found_contexts

def find_phone_numbers_and_contacts(text):
    """หาเบอร์โทรและข้อมูลติดต่อ"""
    
    contact_patterns = [
        r'(\d{3}-\d{3}-\d{4})',  # XXX-XXX-XXXX
        r'(\d{10})',             # 10 digits
        r'(0\d{8,9})',          # Thai phone numbers
        r'(\+66\d{8,9})',       # Thai international format
        r'line\s*id\s*:\s*([a-zA-Z0-9_.-]+)',
        r'line\s*:\s*([a-zA-Z0-9_.-]+)',
        r'facebook\s*:\s*([a-zA-Z0-9_.-]+)',
        r'ig\s*:\s*([a-zA-Z0-9_.-]+)',
        r'instagram\s*:\s*([a-zA-Z0-9_.-]+)',
    ]
    
    found_contacts = []
    
    for pattern in contact_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        found_contacts.extend(matches)
    
    return list(set(found_contacts))  # remove duplicates

def main():
    print("🔍 วิเคราะห์การสนทนาเฉพาะบุคคลกับผู้หญิง...")
    print("Analyzing specific conversations with women...")
    print("=" * 70)
    
    # โหลดข้อมูล
    try:
        with open('output/al.txt', 'r', encoding='utf-8', errors='ignore') as f:
            al_data = f.read()
    except:
        print("❌ ไม่พบไฟล์ output/al.txt")
        return
    
    print(f"📁 ขนาดข้อมูล: {len(al_data):,} ตัวอักษร")
    
    # Username ที่น่าสนใจจากการวิเคราะห์ก่อนหน้า
    target_usernames = [
        'babygirl', 'bangkokgirl', 'prettygirl', 'goodgirl', 'homegirl',
        'insecurequeen', 'princess', 'cutie', 'girlbestfriends'
    ]
    
    # หาการสนทนาเฉพาะ
    print("💬 กำลังหาส่วนการสนทนา...")
    conversations = extract_conversation_snippets(al_data, target_usernames)
    
    # หาชื่อจริง
    print("👤 กำลังหาชื่อจริง...")
    real_names = find_real_names_in_conversations(al_data)
    
    # วิเคราะห์บริบทความสัมพันธ์
    print("💕 กำลังวิเคราะห์บริบทความสัมพันธ์...")
    relationship_contexts = analyze_relationship_context(al_data)
    
    # หาข้อมูลติดต่อ
    print("📞 กำลังหาข้อมูลติดต่อ...")
    contacts = find_phone_numbers_and_contacts(al_data)
    
    # สร้างรายงาน
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"detailed_women_conversations_{timestamp}.txt"
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("ALX.TRADING - รายงานการสนทนากับผู้หญิงแบบละเอียด\n")
        f.write("Detailed Women Conversations Analysis\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"📅 วันที่: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"🎯 Target: alx.trading\n\n")
        
        # การสนทนาเฉพาะ
        f.write("💬 การสนทนาที่พบ:\n")
        f.write("-" * 50 + "\n")
        if conversations:
            for username, data in conversations.items():
                f.write(f"\n👤 {username}:\n")
                f.write(f"   📊 จำนวนการกล่าวถึง: {data['count']} ครั้ง\n")
                f.write(f"   💬 ตัวอย่างการสนทนา:\n")
                for i, snippet in enumerate(data['snippets'][:3], 1):
                    clean_snippet = snippet.replace('\n', ' ').strip()[:100]
                    f.write(f"      {i}. {clean_snippet}...\n")
        else:
            f.write("ไม่พบการสนทนาที่เฉพาะเจาะจง\n")
        
        # ชื่อจริงที่พบ
        f.write(f"\n👤 ชื่อจริงที่อาจพบ:\n")
        f.write("-" * 50 + "\n")
        if real_names:
            for name in sorted(real_names):
                f.write(f"• {name}\n")
        else:
            f.write("ไม่พบชื่อจริงที่ชัดเจน\n")
        
        # บริบทความสัมพันธ์
        f.write(f"\n💕 บริบทความสัมพันธ์:\n")
        f.write("-" * 50 + "\n")
        if relationship_contexts:
            for context_type, count in relationship_contexts.items():
                f.write(f"• {context_type}: {count} ครั้ง\n")
        else:
            f.write("ไม่พบบริบทความสัมพันธ์ที่ชัดเจน\n")
        
        # ข้อมูลติดต่อ
        f.write(f"\n📞 ข้อมูลติดต่อที่พบ:\n")
        f.write("-" * 50 + "\n")
        if contacts:
            for contact in contacts[:10]:  # แสดงแค่ 10 รายการแรก
                f.write(f"• {contact}\n")
        else:
            f.write("ไม่พบข้อมูลติดต่อที่ชัดเจน\n")
        
        f.write(f"\n🎯 สรุปผล:\n")
        f.write("-" * 50 + "\n")
        f.write(f"💬 จำนวนการสนทนา: {len(conversations)}\n")
        f.write(f"👤 จำนวนชื่อจริง: {len(real_names)}\n")
        f.write(f"💕 ประเภทความสัมพันธ์: {len(relationship_contexts)}\n")
        f.write(f"📞 ข้อมูลติดต่อ: {len(contacts)}\n")
    
    # แสดงผลหน้าจอ
    print("\n📊 ผลการวิเคราะห์:")
    print("-" * 50)
    
    if conversations:
        print("💬 การสนทนาที่พบ:")
        for username, data in list(conversations.items())[:5]:
            print(f"  👤 {username}: {data['count']} ครั้ง")
    
    if real_names:
        print(f"\n👤 ชื่อจริงที่อาจพบ ({len(real_names)} ชื่อ):")
        for name in sorted(real_names)[:10]:
            print(f"  • {name}")
    
    if relationship_contexts:
        print(f"\n💕 บริบทความสัมพันธ์:")
        for context_type, count in relationship_contexts.items():
            print(f"  • {context_type}: {count} ครั้ง")
    
    if contacts:
        print(f"\n📞 ข้อมูลติดต่อ ({len(contacts)} รายการ):")
        for contact in contacts[:5]:
            print(f"  • {contact}")
    
    print(f"\n💾 รายงานเต็มบันทึกไว้ใน: {report_filename}")
    
    # สถิติรวม
    total_evidence = len(conversations) + len(real_names) + len(relationship_contexts) + len(contacts)
    if total_evidence > 10:
        print(f"\n🔴 สรุป: พบหลักฐานมากมาย ({total_evidence} รายการ) - alx.trading มีการติดต่อกับผู้หญิงอย่างชัดเจน!")
    elif total_evidence > 0:
        print(f"\n🟡 สรุป: พบหลักฐานบ้าง ({total_evidence} รายการ)")
    else:
        print(f"\n🟢 สรุป: ไม่พบหลักฐานที่ชัดเจน")

if __name__ == "__main__":
    main()
