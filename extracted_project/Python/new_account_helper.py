#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🆕 New Instagram Account Creator Guide
คู่มือสร้างบัญชี Instagram ใหม่สำหรับการทดสอบ
"""

import json
import webbrowser
from datetime import datetime

def create_new_account_guide():
    """คู่มือสร้างบัญชีใหม่"""
    print("🆕 Instagram New Account Creator")
    print("="*50)
    print()
    print("📱 ขั้นตอนการสร้างบัญชี Instagram ใหม่:")
    print()
    print("1️⃣  เตรียมข้อมูล:")
    print("    • Email ใหม่ที่ยังไม่เคยใช้กับ Instagram")
    print("    • เบอร์โทรศัพท์ (ถ้ามี)")
    print("    • Username ที่ต้องการ")
    print("    • Password ที่แข็งแรง")
    print()
    print("2️⃣  สร้างบัญชี:")
    print("    • ไปที่ https://www.instagram.com/accounts/emailsignup/")
    print("    • กรอกข้อมูลที่เตรียมไว้")
    print("    • ยืนยัน email")
    print()
    print("3️⃣  ตั้งค่าบัญชี:")
    print("    • อัพโหลดรูปโปรไฟล์")
    print("    • เขียน Bio")
    print("    • ตั้งค่าเป็น Private (สำหรับความปลอดภัย)")
    print()
    print("4️⃣  หา Session ID:")
    print("    • Login แล้วกด F12")
    print("    • Application → Cookies → sessionid")
    print("    • Copy Value")
    print()
    
    open_signup = input("🌐 เปิดหน้าสมัครสมาชิก Instagram ไหม? (y/n): ").strip().lower()
    if open_signup == 'y':
        webbrowser.open('https://www.instagram.com/accounts/emailsignup/')
        print("✅ เปิดหน้าสมัครสมาชิกในเบราว์เซอร์แล้ว")
    
    return True

def create_temporary_session():
    """สร้าง temporary session สำหรับทดสอบ"""
    print("\n🔧 สร้าง Temporary Session")
    print("="*40)
    
    temp_session = {
        "sessionid": "temp_session_waiting_for_real_account",
        "account_info": {
            "status": "waiting_for_new_account",
            "created_at": datetime.now().isoformat(),
            "note": "Temporary session - รอการสร้างบัญชีใหม่",
            "next_steps": [
                "สร้างบัญชี Instagram ใหม่",
                "Login และหา Session ID",
                "อัพเดท session.json ด้วย Session ID จริง"
            ]
        }
    }
    
    with open('session.json', 'w', encoding='utf-8') as f:
        json.dump(temp_session, f, indent=4, ensure_ascii=False)
    
    print("✅ สร้าง temporary session ลง session.json แล้ว")
    print("📝 เมื่อได้ Session ID จริงแล้ว ให้รัน:")
    print("   python easy_session_setup.py")
    
    return temp_session

def show_email_suggestions():
    """แนะนำ email providers สำหรับสร้างบัญชี"""
    print("\n📧 แนะนำ Email Providers:")
    print("="*30)
    print("🔹 Gmail: gmail.com (แนะนำ)")
    print("🔹 Outlook: outlook.com")
    print("🔹 Yahoo: yahoo.com")
    print("🔹 ProtonMail: protonmail.com (ความเป็นส่วนตัวสูง)")
    print()
    print("💡 Tips:")
    print("   • ใช้ email ที่ยังไม่เคยลงทะเบียน Instagram")
    print("   • เก็บ email และ password ไว้ในที่ปลอดภัย")
    print("   • อย่าใช้ข้อมูลส่วนตัวจริงในชื่อผู้ใช้")

def show_username_suggestions():
    """แนะนำการตั้ง username"""
    print("\n👤 แนะนำการตั้ง Username:")
    print("="*35)
    print("✅ ควรใช้:")
    print("   • ตัวอักษร a-z, A-Z")
    print("   • ตัวเลข 0-9")
    print("   • จุด (.) และ underscore (_)")
    print("   • ความยาว 3-30 ตัวอักษร")
    print()
    print("❌ ไม่ควรใช้:")
    print("   • ข้อมูลส่วนตัวจริง")
    print("   • ชื่อจริงของคุณ")
    print("   • วันเกิดหรือเบอร์โทร")
    print()
    print("💡 ตัวอย่าง username ที่ดี:")
    print("   • test_user_2025")
    print("   • demo.account.ig")
    print("   • practice_insta_123")

def main():
    print("🆕 Instagram Account Setup Helper")
    print("="*45)
    print("💡 เครื่องมือช่วยสร้างบัญชี Instagram ใหม่สำหรับการทดสอบ")
    print()
    
    while True:
        print("🛠️ เลือกการดำเนินการ:")
        print("1. 📋 ดูคู่มือสร้างบัญชีใหม่")
        print("2. 📧 ดูแนะนำ Email Providers")
        print("3. 👤 ดูแนะนำการตั้ง Username")
        print("4. 🔧 สร้าง Temporary Session")
        print("5. 🌐 เปิดหน้าสมัครสมาชิก Instagram")
        print("6. ❌ ออก")
        
        choice = input("\n🤔 เลือก (1-6): ").strip()
        
        if choice == "1":
            create_new_account_guide()
        elif choice == "2":
            show_email_suggestions()
        elif choice == "3":
            show_username_suggestions()
        elif choice == "4":
            create_temporary_session()
        elif choice == "5":
            webbrowser.open('https://www.instagram.com/accounts/emailsignup/')
            print("✅ เปิดหน้าสมัครสมาชิกในเบราว์เซอร์แล้ว")
        elif choice == "6":
            break
        else:
            print("❌ กรุณาเลือก 1-6")
        
        print("\n" + "-"*50)
    
    print("\n🎉 ขอบคุณที่ใช้ Instagram Account Setup Helper!")
    print("📝 เมื่อสร้างบัญชีเสร็จแล้ว อย่าลืมรัน:")
    print("   python easy_session_setup.py")

if __name__ == "__main__":
    main()
