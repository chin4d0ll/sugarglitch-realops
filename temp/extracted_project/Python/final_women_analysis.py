#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
หาชื่อผู้หญิงจริงและข้อมูลการติดต่อที่ชัดเจน
Find real women names and clear contact information
"""

import json
import re
import os
from datetime import datetime

def extract_real_female_contacts(text):
    """หาข้อมูลการติดต่อผู้หญิงจริงๆ"""
    
    # Pattern สำหรับหาชื่อจริงของผู้หญิง (ไทยและอังกฤษ)
    thai_female_names = [
        'นิด', 'นิม', 'น้อย', 'นิ้ง', 'นาน', 'นิภา', 'นันท์', 'นภา',
        'มิ้นต์', 'มิลค์', 'เมย์', 'มายด์', 'มิ้ม', 'มิว', 'มด', 'มุก',
        'ปลอย', 'ปิ่น', 'ปาย', 'ปุ๊ก', 'ปิง', 'เปี่ยม', 'ปุ้ม', 'ปอ',
        'เฟิร์น', 'ฟาง', 'ฟิล์ม', 'ฟ้า', 'ฟลุ๊ค', 'เฟรม', 'ฟอร์ด',
        'บี', 'บีม', 'บุ๋ม', 'เบล', 'เบียร์', 'บู', 'บอล', 'เบนซ์',
        'อิ๊ก', 'อิส', 'อาย', 'อาร์น', 'เอิร์ธ', 'อุ้ม', 'อุ๊ม', 'อุ๋ม',
        'กิ๊ฟ', 'กิ๊ก', 'กอล์ฟ', 'เกรซ', 'เกม', 'กบ', 'เก๋', 'แก้ว',
        'จิ๋ว', 'จ๋า', 'จูน', 'เจน', 'เจ๋ง', 'จิ๊บ', 'จ๊ะ', 'เจี๊ยบ',
        'ดรีม', 'เดียร์', 'ดี', 'ดาว', 'เด็ก', 'ดู', 'เดอะ', 'ด้วง',
        'คิว', 'เค', 'คอย', 'เคท', 'คิม', 'เคียร์', 'เครื่อง', 'เค้ก',
        'ลิง', 'ลูก', 'ลิซ', 'แล็บ', 'ลาย', 'เลิฟ', 'ลีน', 'ลิต',
        'วิว', 'วาน', 'เวฟ', 'วิน', 'วี', 'เวียร์', 'วู้ด', 'เวล',
        'ยู', 'ยิ้ม', 'ยาย', 'ยุ้ย', 'เยล', 'ยิง', 'เยียร์', 'ยอร์ค',
        'ซู', 'เซฟ', 'ซิ่ง', 'เซิร์ฟ', 'ซิ้ม', 'ซีเค', 'ซาร่า', 'เซต',
        'หวาน', 'ห้อง', 'หนิง', 'เหน่ง', 'หน่อย', 'เฮ้า', 'หยาด'
    ]
    
    english_female_names = [
        'amy', 'anna', 'alice', 'amanda', 'angela', 'ava', 'bella', 'betty',
        'carol', 'christina', 'claire', 'crystal', 'diana', 'donna', 'emily',
        'emma', 'eva', 'grace', 'hannah', 'helen', 'jenny', 'jessica', 'julia',
        'kate', 'kelly', 'kim', 'linda', 'lisa', 'lucy', 'maria', 'mary',
        'michelle', 'nancy', 'nicole', 'olivia', 'patricia', 'rachel', 'rebecca',
        'rose', 'ruby', 'sally', 'sandra', 'sarah', 'sophia', 'stephanie',
        'susan', 'tiffany', 'victoria', 'wendy', 'zoe', 'may', 'jane', 'joy'
    ]
    
    all_female_names = thai_female_names + english_female_names
    found_names = {}
    
    # หาชื่อจริงในข้อความ
    for name in all_female_names:
        # หาชื่อที่เป็นคำแยกต่างหาก
        pattern = r'\b' + re.escape(name) + r'\b'
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            found_names[name] = len(matches)
    
    return found_names

def extract_social_media_accounts(text):
    """หาบัญชี social media ของผู้หญิง"""
    
    social_patterns = {
        'instagram': [
            r'ig[:\s]+([a-zA-Z0-9_.]+)',
            r'instagram[:\s]+([a-zA-Z0-9_.]+)',
            r'@([a-zA-Z0-9_.]*(?:girl|queen|babe|cutie|princess)[a-zA-Z0-9_.]*)',
            r'instagram\.com/([a-zA-Z0-9_.]+)'
        ],
        'facebook': [
            r'facebook[:\s]+([a-zA-Z0-9_.]+)',
            r'fb[:\s]+([a-zA-Z0-9_.]+)',
            r'facebook\.com/([a-zA-Z0-9_.]+)',
            r'm\.facebook\.com/([a-zA-Z0-9_.]+)'
        ],
        'line': [
            r'line[:\s]+([a-zA-Z0-9_.]+)',
            r'line\s+id[:\s]+([a-zA-Z0-9_.]+)',
            r'line[:\s]*id[:\s]*([a-zA-Z0-9_.]+)'
        ],
        'tiktok': [
            r'tiktok[:\s]+([a-zA-Z0-9_.]+)',
            r'tik\s*tok[:\s]+([a-zA-Z0-9_.]+)'
        ]
    }
    
    found_accounts = {}
    
    for platform, patterns in social_patterns.items():
        accounts = set()
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match) > 2 and len(match) < 30:  # ความยาวที่สมเหตุสมผล
                    accounts.add(match.lower())
        
        if accounts:
            found_accounts[platform] = list(accounts)
    
    return found_accounts

def extract_phone_numbers(text):
    """หาเบอร์โทรศัพท์ที่ชัดเจน"""
    
    phone_patterns = [
        r'(0[0-9]{8,9})',           # เบอร์ไทย 08X-XXX-XXXX
        r'(\+66[0-9]{8,9})',        # เบอร์ไทยแบบ international
        r'(\+44[0-9]{10,11})',      # เบอร์อังกฤษ
        r'(\d{3}-\d{3}-\d{4})',     # XXX-XXX-XXXX
        r'(\d{3}\s\d{3}\s\d{4})',   # XXX XXX XXXX
    ]
    
    found_phones = set()
    
    for pattern in phone_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            # กรองเบอร์ที่ดูเหมือนจริง
            if not match.startswith('1234') and not match == '0000000000':
                found_phones.add(match)
    
    return list(found_phones)

def find_conversation_context(text, names_or_accounts):
    """หาบริบทการสนทนาที่เกี่ยวข้องกับชื่อหรือ account"""
    
    contexts = {}
    
    for item in names_or_accounts:
        # หาข้อความรอบๆ ชื่อหรือ account นี้
        pattern = rf'.{{0,150}}{re.escape(item)}.{{0,150}}'
        matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
        
        if matches:
            # ทำความสะอาดข้อความ
            clean_matches = []
            for match in matches[:3]:  # เอาแค่ 3 ตัวอย่างแรก
                clean = re.sub(r'\s+', ' ', match.strip())
                if len(clean) > 10:
                    clean_matches.append(clean)
            
            if clean_matches:
                contexts[item] = clean_matches
    
    return contexts

def main():
    print("🔍 หาผู้หญิงจริงที่ alx.trading คุยด้วย (ข้อมูลเฉพาะเจาะจง)")
    print("Finding real women that alx.trading is chatting with (specific data)")
    print("=" * 80)
    
    # โหลดข้อมูล
    try:
        with open('output/al.txt', 'r', encoding='utf-8', errors='ignore') as f:
            al_data = f.read()
    except:
        print("❌ ไม่พบไฟล์ output/al.txt")
        return
    
    print(f"📁 ขนาดข้อมูล: {len(al_data):,} ตัวอักษร")
    
    # หาชื่อผู้หญิงจริง
    print("\n👤 กำลังหาชื่อผู้หญิงจริง...")
    real_female_names = extract_real_female_contacts(al_data)
    
    # หาบัญชี social media
    print("📱 กำลังหาบัญชี social media...")
    social_accounts = extract_social_media_accounts(al_data)
    
    # หาเบอร์โทรศัพท์
    print("📞 กำลังหาเบอร์โทรศัพท์...")
    phone_numbers = extract_phone_numbers(al_data)
    
    # หาบริบทการสนทนา
    print("💬 กำลังหาบริบทการสนทนา...")
    all_contacts = list(real_female_names.keys())
    for platform, accounts in social_accounts.items():
        all_contacts.extend(accounts)
    
    conversation_contexts = find_conversation_context(al_data, all_contacts[:10])  # เอาแค่ 10 รายการแรก
    
    # สร้างรายงาน
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"real_women_contacts_{timestamp}.txt"
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("ALX.TRADING - รายงานผู้หญิงจริงที่คุยด้วย\n")
        f.write("Real Women Contacts Report\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"📅 วันที่: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"🎯 Target: alx.trading\n")
        f.write(f"📁 ขนาดข้อมูล: {len(al_data):,} ตัวอักษร\n\n")
        
        # ชื่อผู้หญิงจริง
        f.write("👤 ชื่อผู้หญิงจริงที่พบ:\n")
        f.write("-" * 60 + "\n")
        if real_female_names:
            for name, count in sorted(real_female_names.items(), key=lambda x: x[1], reverse=True):
                f.write(f"• {name}: ปรากฏ {count} ครั้ง\n")
        else:
            f.write("ไม่พบชื่อผู้หญิงจริงที่ชัดเจน\n")
        
        # บัญชี Social Media
        f.write(f"\n📱 บัญชี Social Media:\n")
        f.write("-" * 60 + "\n")
        if social_accounts:
            for platform, accounts in social_accounts.items():
                f.write(f"\n🔸 {platform.upper()}:\n")
                for account in accounts[:5]:  # แสดงแค่ 5 รายการแรก
                    f.write(f"   • {account}\n")
        else:
            f.write("ไม่พบบัญชี social media ที่ชัดเจน\n")
        
        # เบอร์โทรศัพท์
        f.write(f"\n📞 เบอร์โทรศัพท์:\n")
        f.write("-" * 60 + "\n")
        if phone_numbers:
            for phone in phone_numbers:
                f.write(f"• {phone}\n")
        else:
            f.write("ไม่พบเบอร์โทรศัพท์ที่ชัดเจน\n")
        
        # บริบทการสนทนา
        f.write(f"\n💬 ตัวอย่างการสนทนา:\n")
        f.write("-" * 60 + "\n")
        if conversation_contexts:
            for contact, contexts in list(conversation_contexts.items())[:5]:
                f.write(f"\n🗣️ เกี่ยวกับ '{contact}':\n")
                for i, context in enumerate(contexts, 1):
                    f.write(f"   {i}. {context[:100]}...\n")
        else:
            f.write("ไม่พบบริบทการสนทนาที่เฉพาะเจาะจง\n")
        
        # สรุปผล
        f.write(f"\n🎯 สรุปผลการวิเคราะห์:\n")
        f.write("-" * 60 + "\n")
        f.write(f"👤 จำนวนชื่อผู้หญิงจริง: {len(real_female_names)}\n")
        f.write(f"📱 จำนวนบัญชี social media: {sum(len(accounts) for accounts in social_accounts.values())}\n")
        f.write(f"📞 จำนวนเบอร์โทรศัพท์: {len(phone_numbers)}\n")
        f.write(f"💬 จำนวนบริบทการสนทนา: {len(conversation_contexts)}\n")
        
        total_contacts = len(real_female_names) + sum(len(accounts) for accounts in social_accounts.values()) + len(phone_numbers)
        
        if total_contacts > 5:
            f.write(f"\n🔴 ผลสรุป: พบข้อมูลการติดต่อผู้หญิงจำนวนมาก ({total_contacts} รายการ)\n")
            f.write("      → alx.trading มีการติดต่อกับผู้หญิงหลายคนอย่างแน่นอน!\n")
        elif total_contacts > 0:
            f.write(f"\n🟡 ผลสรุป: พบข้อมูลการติดต่อบ้าง ({total_contacts} รายการ)\n")
        else:
            f.write(f"\n🟢 ผลสรุป: ไม่พบข้อมูลการติดต่อที่ชัดเจน\n")
    
    # แสดงผลบนหน้าจอ
    print("\n📊 ผลการวิเคราะห์:")
    print("-" * 60)
    
    if real_female_names:
        print(f"👤 ชื่อผู้หญิงจริงที่พบ ({len(real_female_names)} ชื่อ):")
        for name, count in sorted(real_female_names.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   • {name}: {count} ครั้ง")
    
    if social_accounts:
        print(f"\n📱 บัญชี Social Media:")
        for platform, accounts in social_accounts.items():
            print(f"   🔸 {platform}: {len(accounts)} บัญชี")
            for account in accounts[:3]:
                print(f"      • {account}")
    
    if phone_numbers:
        print(f"\n📞 เบอร์โทรศัพท์ ({len(phone_numbers)} เบอร์):")
        for phone in phone_numbers[:3]:
            print(f"   • {phone}")
    
    if conversation_contexts:
        print(f"\n💬 ตัวอย่างการสนทนา:")
        for contact, contexts in list(conversation_contexts.items())[:2]:
            print(f"   🗣️ {contact}: {contexts[0][:50]}...")
    
    total_contacts = len(real_female_names) + sum(len(accounts) for accounts in social_accounts.values()) + len(phone_numbers)
    
    print(f"\n💾 รายงานเต็มบันทึกไว้ใน: {report_filename}")
    
    if total_contacts > 5:
        print(f"\n🔴 สรุป: พบข้อมูลการติดต่อผู้หญิงจำนวนมาก ({total_contacts} รายการ)")
        print("      → alx.trading มีการติดต่อกับผู้หญิงหลายคนอย่างแน่นอน!")
    elif total_contacts > 0:
        print(f"\n🟡 สรุป: พบข้อมูลการติดต่อบ้าง ({total_contacts} รายการ)")
    else:
        print(f"\n🟢 สรุป: ไม่พบข้อมูลการติดต่อที่ชัดเจน")

if __name__ == "__main__":
    main()
