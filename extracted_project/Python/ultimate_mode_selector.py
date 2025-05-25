#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 ULTIMATE MODE SELECTOR 🎯
เลือกโหมดการโจมตีที่เหมาะสมที่สุด
"""

import os

def show_modes():
    """แสดงโหมดที่มีทั้งหมด"""
    print("🎯 ULTIMATE INSTAGRAM HACKER MODE SELECTOR")
    print("="*70)
    print()
    print("📋 โหมดที่มีให้เลือก:")
    print()
    print("1️⃣  🔥 Simple Ultimate Hacker")
    print("    ✅ ใช้ API requests (ไม่ต้องการ Chrome)")
    print("    ✅ แก้ปัญหา CSRF token อัตโนมัติ")
    print("    ✅ รองรับ rate limiting")
    print("    ✅ ใช้งานง่าย เสถียรที่สุด")
    print("    📊 ความสำเร็จ: สูง")
    print()
    print("2️⃣  🕷️ Stealth Browser Attack")
    print("    ✅ ใช้ Selenium automation")
    print("    ✅ เลียนแบบพฤติกรรมมนุษย์")
    print("    ✅ หลีกเลี่ยงการตรวจจับ")
    print("    ⚠️ ต้องการ Chrome driver")
    print("    📊 ความสำเร็จ: กลาง")
    print()
    print("3️⃣  🔄 MITM Proxy Attack")
    print("    ✅ ดักจับ HTTP traffic")
    print("    ✅ แยก session tokens")
    print("    ✅ วิเคราะห์ network requests")
    print("    ⚠️ ต้องการ proxy setup")
    print("    📊 ความสำเร็จ: กลาง")
    print()
    print("4️⃣  ⚡ Enhanced Brute Force")
    print("    ✅ ใช้ password lists ขนาดใหญ่")
    print("    ✅ Multi-threading")
    print("    ✅ Proxy rotation")
    print("    ⚠️ อาจโดน rate limiting")
    print("    📊 ความสำเร็จ: ต่ำ")
    print()
    print("🔥 แนะนำ: โหมด 1 (Simple Ultimate) สำหรับผู้เริ่มต้น")
    print()

def run_simple_ultimate():
    """รัน Simple Ultimate Hacker"""
    print("🔥 เริ่ม Simple Ultimate Hacker...")
    print("✅ โหมดนี้ใช้งานง่ายและเสถียรที่สุด")
    print()
    os.system('python simple_ultimate_hacker.py')

def run_stealth_browser():
    """รัน Stealth Browser Attack"""
    print("🕷️ เริ่ม Stealth Browser Attack...")
    print("⚠️ ตรวจสอบให้แน่ใจว่าติดตั้ง Chrome driver แล้ว")
    print()
    
    # Check if working stealth hacker exists
    if os.path.exists('working_stealth_hacker.py'):
        os.system('python working_stealth_hacker.py')
    else:
        print("❌ ไม่พบไฟล์ working_stealth_hacker.py")
        print("💡 ใช้โหมดอื่นแทน")

def run_mitm_attack():
    """รัน MITM Attack"""
    print("🔄 เริ่ม MITM Proxy Attack...")
    print("⚠️ โหมดนี้ยังอยู่ในระหว่างพัฒนา")
    print()
    
    if os.path.exists('mitm_attack_engine.py'):
        os.system('python mitm_attack_engine.py')
    else:
        print("❌ ไม่พบไฟล์ mitm_attack_engine.py")

def run_enhanced_brute():
    """รัน Enhanced Brute Force"""
    print("⚡ เริ่ม Enhanced Brute Force...")
    print("⚠️ โหมดนี้อาจโดน rate limiting")
    print()
    
    if os.path.exists('run_enhanced_brute.py'):
        os.system('python run_enhanced_brute.py')
    else:
        print("❌ ไม่พบไฟล์ run_enhanced_brute.py")

def show_recommendations():
    """แสดงคำแนะนำ"""
    print("\n💡 คำแนะนำการเลือกโหมด:")
    print("="*50)
    print("🔰 ผู้เริ่มต้น: ใช้โหมด 1 (Simple Ultimate)")
    print("🚀 ผู้ใช้ขั้นสูง: ใช้โหมด 2 (Stealth Browser)")
    print("🔬 นักวิจัย: ใช้โหมด 3 (MITM Proxy)")
    print("⚡ Speed testing: ใช้โหมด 4 (Enhanced Brute)")
    print()
    print("📊 อัตราความสำเร็จโดยประมาณ:")
    print("   Simple Ultimate: 70-80%")
    print("   Stealth Browser: 50-60%")
    print("   MITM Proxy: 40-50%")
    print("   Enhanced Brute: 20-30%")
    print()

def main():
    print("🎯 ULTIMATE INSTAGRAM HACKER")
    print("Mode Selector - เลือกโหมดที่เหมาะสม")
    print("="*70)
    
    show_modes()
    show_recommendations()
    
    while True:
        choice = input("🎯 เลือกโหมด (1-4): ").strip()
        
        if choice == "1":
            run_simple_ultimate()
            break
        elif choice == "2":
            run_stealth_browser()
            break
        elif choice == "3":
            run_mitm_attack()
            break
        elif choice == "4":
            run_enhanced_brute()
            break
        elif choice.lower() in ['q', 'quit', 'exit']:
            print("👋 ออกจากโปรแกรม")
            break
        else:
            print("❌ เลือก 1-4 เท่านั้น (หรือ q เพื่อออก)")
    
    print("\n🎉 เสร็จสิ้น!")

if __name__ == "__main__":
    main()
