#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌸 SugarGlitch Easy Session Setup
เครื่องมือง่ายๆ สำหรับใส่ Instagram Session ID ของคุณ
"""

import json
import os

def show_instructions():
    """แสดงวิธีการหา Session ID อย่างละเอียด"""
    print("🌸 SugarGlitch Easy Session Setup")
    print("="*60)
    print()
    print("📱 ขั้นตอนการหา Instagram Session ID ของคุณ:")
    print()
    print("1️⃣  เปิด Browser ไปที่ https://www.instagram.com")
    print("    • ใช้ Chrome, Firefox, Edge, หรือ Safari")
    print("    • Login ด้วยบัญชี Instagram ของคุณ")
    print()
    print("2️⃣  เปิด Developer Tools:")
    print("    • กด F12 (Windows/Linux)")
    print("    • กด Cmd+Option+I (Mac)")
    print("    • หรือคลิกขวา → Inspect Element")
    print()
    print("3️⃣  ไปที่แท็บ Application (หรือ Storage):")
    print("    • คลิกแท็บ 'Application' หรือ 'Storage'")
    print("    • ขยาย 'Cookies' ในแถบข้าง")
    print("    • คลิก 'https://www.instagram.com'")
    print()
    print("4️⃣  หา Session ID:")
    print("    • หาแถวที่มี Name = 'sessionid'")
    print("    • ในคอลัมน์ 'Value' จะมีข้อความยาวๆ")
    print("    • เลือกและ Copy ข้อความทั้งหมด")
    print()
    print("5️⃣  ตัวอย่าง Session ID:")
    print("    IGSCd8f5a2b1c3e4f5678901234567890abcdef...")
    print("    (ยาวประมาณ 32-50 ตัวอักษร)")
    print()
    print("="*60)

def validate_session_id(session_id):
    """ตรวจสอบความถูกต้องของ Session ID"""
    if not session_id:
        return False, "Session ID ว่างเปล่า"
    
    # ลบ whitespace
    session_id = session_id.strip()
    
    # ตรวจสอบความยาว
    if len(session_id) < 20:
        return False, f"Session ID สั้นเกินไป ({len(session_id)} ตัวอักษร) ควรยาว 20-50 ตัวอักษร"
    
    if len(session_id) > 60:
        return False, f"Session ID ยาวเกินไป ({len(session_id)} ตัวอักษร) ควรยาว 20-50 ตัวอักษร"
    
    # ตรวจสอบ characters
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789%_-"
    for char in session_id:
        if char not in allowed_chars:
            return False, f"พบอักขระที่ไม่อนุญาต: '{char}'"
    
    return True, "Session ID ถูกต้อง"

def save_session_config(session_id):
    """บันทึก Session ID ลงไฟล์ config"""
    config = {
        "sessionid": session_id,
        "account_info": {
            "setup_method": "easy_manual_input",
            "setup_date": "2025-05-25",
            "note": "Session ID ที่ใส่ด้วยตนเองผ่าน Easy Setup"
        }
    }
    
    try:
        with open('session.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        return True, f"✅ บันทึกลง session.json สำเร็จ!"
    except Exception as e:
        return False, f"❌ ไม่สามารถบันทึกไฟล์: {e}"

def main():
    show_instructions()
    
    while True:
        print("\n" + "🔑"*20)
        session_id = input("📋 Paste Instagram Session ID ของคุณที่นี่: ").strip()
        
        if not session_id:
            print("❌ กรุณาใส่ Session ID")
            continue
        
        # ตรวจสอบความถูกต้อง
        is_valid, message = validate_session_id(session_id)
        
        if not is_valid:
            print(f"❌ {message}")
            retry = input("\n🤔 ลองใหม่ไหม? (y/n): ").strip().lower()
            if retry != 'y':
                break
            continue
        
        print(f"✅ {message}")
        print(f"📏 ความยาว: {len(session_id)} ตัวอักษร")
        print(f"🔍 ตัวอย่าง: {session_id[:20]}...")
        
        # ยืนยันการบันทึก
        confirm = input("\n💾 บันทึก Session ID นี้ไหม? (y/n): ").strip().lower()
        if confirm == 'y':
            success, message = save_session_config(session_id)
            print(f"\n{message}")
            
            if success:
                print(f"📁 ไฟล์: {os.path.abspath('session.json')}")
                print()
                print("🚀 ขั้นตอนต่อไป:")
                print("   python run_alx_brute.py      # สำหรับ ALX Trading")
                print("   python run_enhanced_brute.py # สำหรับ Enhanced Attack")
                print("   python validate_session.py   # ทดสอบ Session ID")
                break
        else:
            print("❌ ยกเลิกการบันทึก")
        
        # ถามว่าจะลองใหม่ไหม
        retry = input("\n🤔 ใส่ Session ID ใหม่ไหม? (y/n): ").strip().lower()
        if retry != 'y':
            break
    
    print("\n👋 ขอบคุณที่ใช้ SugarGlitch Easy Session Setup!")

if __name__ == "__main__":
    main()
