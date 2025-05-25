#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Easy Attack Selector - เลือกโหมดโจมตีง่ายๆ
สำหรับผู้ใช้งาน SugarGlitch
"""

import os
import sys

def main_menu():
    """แสดงเมนูหลัก"""
    print("\n" + "="*60)
    print("🍭 SugarGlitch - Easy Attack Selector")
    print("="*60)
    print("🎯 เลือกโหมดโจมตีที่ต้องการ:")
    print()
    print("1️⃣  🕷️ Stealth Mode (แนะนำ)")
    print("    • ใช้งานง่าย มีประสิทธิภาพ")
    print("    • หลีกเลี่ยงการตรวจจับ")
    print("    • เลียนแบบพฤติกรรมมนุษย์")
    print()
    print("2️⃣  🔄 MITM Proxy Mode")
    print("    • ดักจับ traffic")
    print("    • วิเคราะห์ requests")
    print("    • ซับซ้อนกว่า แต่มีประสิทธิภาพสูง")
    print()
    print("3️⃣  ⚡ Quick Simple Attack")
    print("    • โหมดง่ายสุด ไม่ซับซ้อน")
    print("    • ใช้ Selenium ธรรมดา")
    print("    • เหมาะสำหรับมือใหม่")
    print()
    print("4️⃣  🔧 ตรวจสอบ Session ID")
    print("    • หา Session ID ของคุณ")
    print("    • สำหรับเข้าถึงบัญชีตัวเอง")
    print()
    print("0️⃣  ❌ ออกจากโปรแกรม")
    print("="*60)

def run_stealth_attack():
    """รัน Stealth Attack"""
    print("\n🕷️ เริ่ม Stealth Attack Mode...")
    try:
        os.system('python working_stealth_hacker.py')
    except:
        print("❌ ไม่พบไฟล์ working_stealth_hacker.py")
        print("💡 ให้สร้างไฟล์ใหม่...")

def run_mitm_attack():
    """รัน MITM Attack"""
    print("\n🔄 เริ่ม MITM Attack Mode...")
    try:
        os.system('python mitm_attack_engine.py')
    except:
        print("❌ ไม่พบไฟล์ mitm_attack_engine.py")

def run_simple_attack():
    """รัน Simple Attack"""
    print("\n⚡ เริ่ม Simple Attack Mode...")
    try:
        os.system('python simple_attack.py')
    except:
        print("❌ ไม่พบไฟล์ simple_attack.py")
        print("💡 ให้สร้างไฟล์ใหม่...")

def check_session():
    """ตรวจสอบ Session ID"""
    print("\n🔧 ตรวจสอบ Session ID...")
    try:
        os.system('python get_my_session.py')
    except:
        print("❌ ไม่พบไฟล์ get_my_session.py")

def main():
    """ฟังก์ชันหลัก"""
    while True:
        main_menu()
        
        try:
            choice = input("\n👉 เลือกตัวเลข (1-4, 0=ออก): ").strip()
            
            if choice == "1":
                run_stealth_attack()
            elif choice == "2":
                run_mitm_attack()
            elif choice == "3":
                run_simple_attack()
            elif choice == "4":
                check_session()
            elif choice == "0":
                print("\n👋 ลาก่อน! ขอบคุณที่ใช้ SugarGlitch")
                break
            else:
                print("\n❌ เลือกตัวเลข 1-4 หรือ 0 เท่านั้น")
                
        except KeyboardInterrupt:
            print("\n\n👋 ปิดโปรแกรม...")
            break
        except Exception as e:
            print(f"\n❌ เกิดข้อผิดพลาด: {str(e)}")

if __name__ == "__main__":
    main()
