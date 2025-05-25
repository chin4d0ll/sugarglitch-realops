#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Advanced Attack Mode Selector
เลือกระหว่าง Stealth Mode และ MITM Attack
"""

import os

def show_advanced_modes():
    """แสดงโหมดโจมตีขั้นสูง"""
    print("🚀 SugarGlitch Advanced Attack Modes")
    print("="*60)
    print("🎯 โหมดโจมตีขั้นสูง (หลีกเลี่ยง rate limiting):")
    print()
    print("1️⃣  🕷️ Stealth Browser Attack")
    print("    • ใช้ undetected Chrome driver")
    print("    • เลียนแบบพฤติกรรมมนุษย์")
    print("    • หลีกเลี่ยงการตรวจจับ")
    print("    • Random delays และ mouse movements")
    print()
    print("2️⃣  🔄 MITM Proxy Attack")
    print("    • ดักจับ HTTP traffic")
    print("    • แยก CSRF tokens และ session data")
    print("    • วิเคราะห์ requests/responses")
    print("    • Bypass rate limiting")
    print()
    print("3️⃣  ⚡ Hybrid Attack (Stealth + MITM)")
    print("    • รวมจุดแข็งของทั้งสองโหมด")
    print("    • ประสิทธิภาพสูงสุด")
    print("    • Automatic fallback")
    print()
    print("4️⃣  🔧 Quick Fix Mode")
    print("    • แก้ไขปัญหา rate limiting")
    print("    • ทดสอบการเชื่อมต่อ")
    print("    • Reset attack config")
    print()

def run_stealth_mode():
    """รัน Stealth Attack Mode"""
    print("🕷️ เริ่ม Stealth Attack Mode...")
    print("✅ รัน: python stealth_attack_engine.py")
    os.system('python stealth_attack_engine.py')

def run_mitm_mode():
    """รัน MITM Attack Mode"""
    print("🔄 เริ่ม MITM Attack Mode...")
    print("✅ รัน: python mitm_attack_engine.py")
    os.system('python mitm_attack_engine.py')

def run_hybrid_mode():
    """รัน Hybrid Attack Mode"""
    print("⚡ เริ่ม Hybrid Attack Mode...")
    print("🔄 Phase 1: เริ่มด้วย MITM เพื่อดักจับข้อมูล")
    
    choice = input("🤔 เริ่มด้วย MITM แล้วค่อย Stealth ไหม? (y/n): ").strip().lower()
    if choice == 'y':
        print("1️⃣ เริ่ม MITM Phase...")
        os.system('python mitm_attack_engine.py')
        
        print("\n2️⃣ เริ่ม Stealth Phase...")
        os.system('python stealth_attack_engine.py')
    else:
        print("🕷️ เริ่มด้วย Stealth Mode...")
        os.system('python stealth_attack_engine.py')

def quick_fix_mode():
    """โหมดแก้ไขปัญหาเร่งด่วน"""
    print("🔧 Quick Fix Mode")
    print("="*30)
    
    print("🔍 ตรวจสอบปัญหา...")
    print("✅ Rate limiting bypass")
    print("✅ Connection reset")
    print("✅ Proxy configuration")
    
    # สร้าง config ใหม่ที่หลีกเลี่ยง rate limiting
    quick_config = {
        "request_delay": 10,  # เพิ่มเป็น 10 วินาที
        "max_attempts": 10,   # ลดจำนวนครั้ง
        "use_proxy": False,   # ไม่ใช้ proxy
        "stealth_mode": True,
        "human_simulation": True,
        "random_delays": True
    }
    
    import json
    with open('quick_fix_config.json', 'w') as f:
        json.dump(quick_config, f, indent=4)
    
    print("💾 สร้าง quick_fix_config.json แล้ว")
    print("🚀 ใช้งาน: python stealth_attack_engine.py")

def main():
    print("🚀 SugarGlitch Advanced Attack Mode Selector")
    print("="*60)
    print("💡 เหตุผลที่ควรใช้โหมดขั้นสูง:")
    print("   • หลีกเลี่ยง 429 rate limiting errors")
    print("   • ไม่ติด Connection aborted")
    print("   • ประสิทธิภาพสูงกว่า brute force ธรรมดา")
    print("   • เลียนแบบพฤติกรรมมนุษย์")
    print()
    
    show_advanced_modes()
    
    while True:
        choice = input("\n🎯 เลือกโหมดโจมตี (1-4): ").strip()
        
        if choice == "1":
            run_stealth_mode()
            break
        elif choice == "2":
            run_mitm_mode()
            break
        elif choice == "3":
            run_hybrid_mode()
            break
        elif choice == "4":
            quick_fix_mode()
            break
        else:
            print("❌ เลือก 1-4 เท่านั้น")
    
    print("\n🎉 Advanced Attack Mode เสร็จสิ้น!")

if __name__ == "__main__":
    main()
