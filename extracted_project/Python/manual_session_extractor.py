#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Manual Session ID Extractor - สำหรับแยก Session ID ด้วยตนเอง
เครื่องมือช่วยให้คุณแยก Session ID จาก browser cookies ด้วยตนเอง
"""

import json
import re
from datetime import datetime

def extract_session_from_text():
    """แยก Session ID จากข้อความที่ copy มาจาก browser"""
    print("🍪 Manual Session ID Extractor")
    print("="*50)
    print("📋 วิธีใช้:")
    print("1. เปิด Instagram ใน browser")
    print("2. กด F12 → Application → Cookies → instagram.com") 
    print("3. หา cookie ชื่อ 'sessionid'")
    print("4. คัดลอกค่าใน column 'Value'")
    print("5. paste ที่นี่")
    print()
    
    # รับ input จากผู้ใช้
    raw_input = input("🔗 Paste Session ID ของคุณที่นี่: ").strip()
    
    if not raw_input:
        print("❌ ไม่มีข้อมูล")
        return None
    
    # ทำความสะอาด input
    session_id = clean_session_id(raw_input)
    
    if not session_id:
        print("❌ ไม่พบ Session ID ที่ถูกต้อง")
        return None
    
    # Validate format
    if validate_session_format(session_id):
        print(f"✅ Session ID ถูกต้อง: {session_id[:20]}...")
        
        # สร้าง config
        config = create_session_config(session_id)
        
        # บันทึกไฟล์
        save_session_config(config)
        
        return session_id
    else:
        print("❌ รูปแบบ Session ID ไม่ถูกต้อง")
        return None

def clean_session_id(raw_text):
    """ทำความสะอาด Session ID จากข้อความ"""
    
    # ลบ whitespace
    text = raw_text.strip()
    
    # หา pattern ของ Session ID (ตัวอักษรและตัวเลข 32-50 ตัวอักษร)
    patterns = [
        r'sessionid["\s]*[:=]["\s]*([a-zA-Z0-9%_-]{25,50})',
        r'["\s]*([a-zA-Z0-9%_-]{32,50})["\s]*',
        r'Value["\s]*[:=]["\s]*([a-zA-Z0-9%_-]{25,50})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    
    # ถ้าไม่เจอ pattern ให้ใช้ทั้งหมด (กรณี copy เฉพาะ value)
    if re.match(r'^[a-zA-Z0-9%_-]{25,50}$', text):
        return text
    
    return None

def validate_session_format(session_id):
    """ตรวจสอบรูปแบบ Session ID"""
    if not session_id:
        return False
    
    # ตรวจสอบความยาว (25-50 ตัวอักษร)
    if len(session_id) < 25 or len(session_id) > 50:
        return False
    
    # ตรวจสอบ characters (ต้องเป็น alphanumeric, %, _, -)
    if not re.match(r'^[a-zA-Z0-9%_-]+$', session_id):
        return False
    
    return True

def create_session_config(session_id):
    """สร้าง config object"""
    return {
        "sessionid": session_id,
        "account_info": {
            "extraction_method": "manual",
            "extracted_at": datetime.now().isoformat(),
            "browser": "manual_input",
            "validated": False,
            "notes": "Session ID ที่แยกด้วยตนเอง"
        }
    }

def save_session_config(config):
    """บันทึก config ลงไฟล์"""
    try:
        with open('session.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        print(f"✅ บันทึกลง session.json แล้ว")
        print(f"📁 ไฟล์: {os.path.abspath('session.json')}")
        
    except Exception as e:
        print(f"❌ ไม่สามารถบันทึกไฟล์: {e}")

def interactive_extraction():
    """โหมดแยก Session ID แบบ interactive"""
    print("🌸 SugarGlitch Manual Session Extractor")
    print("="*60)
    print("💡 เครื่องมือนี้จะช่วยคุณแยก Session ID จาก browser cookies")
    print()
    
    while True:
        session_id = extract_session_from_text()
        
        if session_id:
            print("\n🎉 สำเร็จ! Session ID พร้อมใช้งาน")
            
            # ถามว่าต้องการทดสอบไหม
            test = input("\n🧪 ต้องการทดสอบ Session ID นี้เลยไหม? (y/n): ")
            if test.lower() == 'y':
                import os
                print("🔄 กำลังทดสอบ Session ID...")
                os.system('python validate_session.py')
            break
        else:
            retry = input("\n🤔 ลองใหม่ไหม? (y/n): ")
            if retry.lower() != 'y':
                break

if __name__ == "__main__":
    import os
    interactive_extraction()
