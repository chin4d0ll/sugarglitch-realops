#!/usr/bin/env python3
"""
วิธีง่ายๆ สำหรับผู้ใช้ iPad 
Simple iPad Instagram Solution
"""

def show_ipad_methods():
    print("📱 วิธีหา SessionID บน iPad (เลือกวิธีที่ทำได้)")
    print("=" * 55)
    print()
    
    print("🔥 วิธีที่ 1: Safari (ง่ายที่สุด)")
    print("1. เปิด Safari → ไป instagram.com") 
    print("2. Login เข้าบัญชี Instagram")
    print("3. ในช่อง address bar พิมพ์:")
    print("   javascript:alert(document.cookie)")
    print("4. กด Enter")
    print("5. จะมี popup ขึ้นมาแสดง cookies")
    print("6. หาคำว่า sessionid= แล้วคัดลอกตัวเลขตัวอักษรที่อยู่หลัง =")
    print()
    
    print("💡 วิธีที่ 2: Chrome บน iPad")
    print("1. Download Chrome app")
    print("2. ไป instagram.com และ login")
    print("3. กด ... menu → More tools")
    print("4. เลือก Console")
    print("5. พิมพ์: document.cookie")
    print("6. หา sessionid ในผลลัพธ์")
    print()
    
    print("⚡ วิธีที่ 3: ใช้ Shortcuts (iOS)")
    print("1. เปิด Shortcuts app")
    print("2. สร้าง shortcut ใหม่")
    print("3. เพิ่ม 'Get Contents of Web Page'")
    print("4. ใส่ URL: https://instagram.com")
    print("5. รันหลังจาก login Instagram")
    print()

def show_alternatives():
    print("🎯 ทางเลือกอื่นๆ (ถ้าหา SessionID ไม่ได้)")
    print("=" * 45)
    print()
    
    print("📞 ขอความช่วยเหลือ:")
    print("- ขอให้เพื่อนที่มีคอมช่วยหา sessionid")
    print("- ส่งมาทาง chat แล้วเราจะรันให้")
    print()
    
    print("🌐 ใช้ข้อมูลสาธารณะ:")
    print("- สกัดข้อมูลที่เปิดเผยสาธารณะได้")
    print("- ไม่ได้ข้อมูล DM แต่ได้ข้อมูลบัญชี")
    print()
    
    print("💻 ยืมคอมพิวเตอร์:")
    print("- ไปร้านเน็ต หรือยืมเครื่องเพื่อน")
    print("- เปิด Chrome/Firefox → F12 → หา sessionid")
    print()

def show_what_we_can_do():
    print("✅ สิ่งที่เราทำได้ตอนนี้")
    print("=" * 30)
    print()
    
    print("🔍 ข้อมูลสาธารณะ alx.trading:")
    print("- ชื่อบัญชี และชื่อเต็ม")
    print("- จำนวนผู้ติดตาม")
    print("- จำนวนโพสต์")
    print("- ประวัติส่วนตัว")
    print("- สถานะบัญชี (ส่วนตัว/สาธารณะ)")
    print()
    
    print("❌ สิ่งที่ต้องการ SessionID:")
    print("- ข้อความ DM")
    print("- รูปภาพใน DM")
    print("- ข้อมูลส่วนตัว")
    print("- รายชื่อผู้ติดตาม")
    print()

def main():
    print("📱 Instagram DM Extractor - iPad Solution")
    print("=" * 50)
    print("วิธีแก้ปัญหาสำหรับผู้ใช้ iPad")
    print()
    
    show_ipad_methods()
    show_alternatives()
    show_what_we_can_do()
    
    print("🚀 NEXT STEPS:")
    print("=" * 15)
    print("1. ลองวิธีหา SessionID ข้างบน")
    print("2. ถ้าได้แล้วส่งมา เราจะรันให้")
    print("3. ถ้าไม่ได้ เราสกัดข้อมูลสาธารณะให้")
    print()
    print("💪 ระบบพร้อมรันทันทีเมื่อมี SessionID!")

if __name__ == "__main__":
    main()
