#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
หาชื่อผู้หญิงเฉพาะเจาะจงที่ alx.trading คุยด้วย
Find Specific Women that alx.trading is chatting with
"""

import json
import re
import os
from datetime import datetime

def load_al_txt():
    """โหลดข้อมูลจาก output/al.txt"""
    try:
        with open('output/al.txt', 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except:
        return ""

def extract_female_names(text):
    """หาชื่อผู้หญิงที่เฉพาะเจาะจง"""
    
    # รายการชื่อผู้หญิงทั่วไป
    common_female_names = [
        'alice', 'anna', 'amy', 'amanda', 'angela', 'ava',
        'bella', 'betty', 'beth', 'brenda', 'brook',
        'cathy', 'carol', 'christina', 'claire', 'crystal',
        'diana', 'donna', 'debbie', 'emily', 'emma', 'eva',
        'fiona', 'grace', 'hannah', 'helen', 'iris', 'jenny',
        'jessica', 'julia', 'kate', 'kelly', 'kim', 'linda',
        'lisa', 'lucy', 'maria', 'mary', 'michelle', 'nancy',
        'nicole', 'olivia', 'pamela', 'patricia', 'rachel',
        'rebecca', 'rose', 'ruby', 'sally', 'sandra', 'sarah',
        'sophia', 'stephanie', 'susan', 'tiffany', 'victoria',
        'wendy', 'zoe', 'may', 'jane', 'joy', 'hope', 'faith',
        'noi', 'nim', 'nam', 'noon', 'ning', 'nid', 'nat',
        'ploy', 'pim', 'pam', 'pie', 'pin', 'mint', 'milk',
        'fang', 'beam', 'boom', 'gift', 'ice', 'dream',
        'bell', 'bee', 'beau', 'earn', 'earth', 'view',
        'petch', 'porn', 'putt', 'kate', 'koi', 'kim'
    ]
    
    found_names = {}
    text_lower = text.lower()
    
    # หาชื่อผู้หญิงทั่วไป
    for name in common_female_names:
        pattern = r'\b' + re.escape(name) + r'\b'
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        if matches:
            found_names[name] = len(matches)
    
    # หาชื่อที่มี pattern เฉพาะ
    special_patterns = {
        'มากบอย': r'มากบอย',
        'เป็นแฟน': r'เป็นแฟน',
        'รักเธอ': r'รักเธอ',
        'ที่รัก': r'ที่รัก',
        'darling': r'darling',
        'sweetheart': r'sweetheart',
        'babe': r'babe',
        'honey': r'honey',
        'my girl': r'my\s+girl',
        'girlfriend': r'girlfriend',
    }
    
    for pattern_name, pattern in special_patterns.items():
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        if matches:
            found_names[pattern_name] = len(matches)
    
    return found_names

def analyze_conversation_context(text):
    """วิเคราะห์บริบทของการสนทนา"""
    
    # หา pattern การสนทนาแบบส่วนตัว
    intimate_patterns = [
        r'อยากเจอ',
        r'คิดถึง',
        r'miss\s+you',
        r'love\s+you',
        r'want\s+to\s+see',
        r'thinking\s+of\s+you',
        r'งดงาม',
        r'สวย',
        r'cute',
        r'beautiful',
        r'sexy',
        r'pretty'
    ]
    
    found_intimate = {}
    for pattern in intimate_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            found_intimate[pattern] = len(matches)
    
    return found_intimate

def find_usernames_and_accounts(text):
    """หา username และ account ที่อาจเป็นผู้หญิง"""
    
    # Pattern สำหรับ username
    username_patterns = [
        r'@([a-zA-Z0-9_]+(?:girl|queen|princess|cutie|baby|babe|honey))',
        r'@([a-zA-Z0-9_]*(?:alice|anna|amy|bella|emma|grace|lucy|maria|sarah|kate|kim|jenny|lisa|rose)[a-zA-Z0-9_]*)',
        r'([a-zA-Z0-9_]*(?:girl|queen|princess|cutie|baby|babe|honey)[a-zA-Z0-9_]*)',
        r'([a-zA-Z0-9_]*(?:alice|anna|amy|bella|emma|grace|lucy|maria|sarah|kate|kim|jenny|lisa|rose)[a-zA-Z0-9_]*)'
    ]
    
    found_usernames = set()
    for pattern in username_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if len(match) > 2:  # ต้องมีความยาวมากกว่า 2 ตัวอักษร
                found_usernames.add(match.lower())
    
    return list(found_usernames)

def main():
    print("🔍 กำลังค้นหาผู้หญิงที่ alx.trading คุยด้วย...")
    print("Searching for specific women that alx.trading is chatting with...")
    print("=" * 70)
    
    # โหลดข้อมูล
    al_data = load_al_txt()
    if not al_data:
        print("❌ ไม่พบไฟล์ output/al.txt")
        return
    
    print(f"📁 ขนาดข้อมูล: {len(al_data):,} ตัวอักษร")
    
    # หาชื่อผู้หญิง
    print("\n👩 กำลังหาชื่อผู้หญิง...")
    female_names = extract_female_names(al_data)
    
    # วิเคราะห์บริบทสนทนา
    print("💕 กำลังวิเคราะห์บริบทส่วนตัว...")
    intimate_context = analyze_conversation_context(al_data)
    
    # หา username
    print("📱 กำลังหา username และ account...")
    usernames = find_usernames_and_accounts(al_data)
    
    # สร้างรายงาน
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"specific_women_analysis_{timestamp}.txt"
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("ALX.TRADING - รายงานผู้หญิงที่คุยด้วย (เฉพาะเจาะจง)\n")
        f.write("Specific Women Chat Analysis Report\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"📅 วันที่: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"🎯 Target: alx.trading\n")
        f.write(f"📁 ขนาดข้อมูล: {len(al_data):,} ตัวอักษร\n\n")
        
        # ชื่อผู้หญิงที่พบ
        f.write("👩 ชื่อผู้หญิงที่พบ:\n")
        f.write("-" * 50 + "\n")
        if female_names:
            for name, count in sorted(female_names.items(), key=lambda x: x[1], reverse=True):
                f.write(f"• {name}: {count} ครั้ง\n")
        else:
            f.write("ไม่พบชื่อผู้หญิงที่ชัดเจน\n")
        
        f.write("\n💕 บริบทส่วนตัว/ความสัมพันธ์:\n")
        f.write("-" * 50 + "\n")
        if intimate_context:
            for pattern, count in sorted(intimate_context.items(), key=lambda x: x[1], reverse=True):
                f.write(f"• {pattern}: {count} ครั้ง\n")
        else:
            f.write("ไม่พบบริบทส่วนตัวที่ชัดเจน\n")
        
        f.write("\n📱 Username/Account ที่อาจเป็นผู้หญิง:\n")
        f.write("-" * 50 + "\n")
        if usernames:
            for username in sorted(usernames):
                f.write(f"• {username}\n")
        else:
            f.write("ไม่พบ username ที่ชัดเจน\n")
        
        f.write("\n🎯 สรุป:\n")
        f.write("-" * 50 + "\n")
        f.write(f"📊 จำนวนชื่อผู้หญิงที่พบ: {len(female_names)}\n")
        f.write(f"💕 จำนวนบริบทส่วนตัว: {len(intimate_context)}\n")
        f.write(f"📱 จำนวน username: {len(usernames)}\n")
        
        if female_names or intimate_context or usernames:
            f.write("\n🔴 ผลสรุป: พบสัญญาณการติดต่อกับผู้หญิงในระดับสูง!\n")
        else:
            f.write("\n🟡 ผลสรุป: ไม่พบสัญญาณที่ชัดเจน\n")
    
    # แสดงผลหน้าจอ
    print("\n📊 ผลการวิเคราะห์:")
    print("-" * 50)
    
    if female_names:
        print("👩 ชื่อผู้หญิงที่พบ:")
        for name, count in sorted(female_names.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  • {name}: {count} ครั้ง")
    
    if intimate_context:
        print("\n💕 บริบทส่วนตัว:")
        for pattern, count in sorted(intimate_context.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  • {pattern}: {count} ครั้ง")
    
    if usernames:
        print("\n📱 Username ที่น่าสนใจ:")
        for username in sorted(usernames)[:10]:
            print(f"  • {username}")
    
    print(f"\n💾 รายงานเต็มบันทึกไว้ใน: {report_filename}")
    
    # สถิติรวม
    total_evidence = len(female_names) + len(intimate_context) + len(usernames)
    if total_evidence > 0:
        print(f"\n🔴 สรุป: พบหลักฐาน {total_evidence} รายการ - มีสัญญาณการติดต่อกับผู้หญิงแน่นอน!")
    else:
        print("\n🟡 สรุป: ไม่พบสัญญาณที่ชัดเจน")

if __name__ == "__main__":
    main()
