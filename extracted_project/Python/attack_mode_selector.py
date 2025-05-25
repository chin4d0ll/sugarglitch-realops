#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌸 SugarGlitch Attack Mode Selector
เลือกโหมดโจมตีสำหรับการ hack Instagram accounts
"""

import json
import os
from datetime import datetime

def show_attack_modes():
    """แสดงโหมดโจมตีที่มี"""
    print("🌸 SugarGlitch Attack Mode Selector")
    print("="*60)
    print("🎯 โหมดโจมตีที่พร้อมใช้งาน:")
    print()
    print("1️⃣  🔥 ALX Trading Attack")
    print("    • เป้าหมาย: alx.trading")
    print("    • Wordlist: alx_trading_passwords.txt (2,568 passwords)")
    print("    • Features: Proxy rotation, Rate limiting")
    print()
    print("2️⃣  ⚡ WhatILove1728 Attack")
    print("    • เป้าหมาย: whatilove1728")
    print("    • Wordlist: whatilove1728.txt (26 passwords)")
    print("    • Features: Targeted attack, Fast mode")
    print()
    print("3️⃣  🚀 Enhanced Brute Force")
    print("    • เป้าหมาย: Custom target")
    print("    • Wordlist: Multiple wordlists")
    print("    • Features: Advanced evasion, Browser API")
    print()
    print("4️⃣  🎯 Advanced Attack Engine")
    print("    • เป้าหมาย: Multiple targets")
    print("    • Wordlist: Combined wordlists")
    print("    • Features: Full proxy integration, Multi-threading")
    print()
    print("5️⃣  🛠️ Custom Target Attack")
    print("    • เป้าหมาย: ใส่เป้าหมายเอง")
    print("    • Wordlist: เลือกเอง")
    print("    • Features: Customizable attack")
    print()

def setup_custom_target():
    """ตั้งค่าเป้าหมายที่กำหนดเอง"""
    print("\n🎯 Setup Custom Target Attack")
    print("="*40)
    
    target = input("📱 ใส่ Instagram username เป้าหมาย: ").strip()
    if not target:
        print("❌ ต้องใส่ username")
        return None
    
    print("\n📚 Wordlist ที่มี:")
    print("1. whatilove1728.txt (26 passwords)")
    print("2. alx_trading_passwords.txt (2,568 passwords)")
    print("3. common_passwords.txt (632 passwords)")
    print("4. ใส่ไฟล์ wordlist เอง")
    
    choice = input("\n🤔 เลือก wordlist (1-4): ").strip()
    
    wordlist_map = {
        "1": "whatilove1728.txt",
        "2": "alx_trading_passwords.txt", 
        "3": "common_passwords.txt"
    }
    
    if choice in wordlist_map:
        wordlist = wordlist_map[choice]
    elif choice == "4":
        wordlist = input("📁 ใส่ชื่อไฟล์ wordlist: ").strip()
        if not os.path.exists(wordlist):
            print(f"❌ ไม่พบไฟล์ {wordlist}")
            return None
    else:
        print("❌ เลือกไม่ถูกต้อง")
        return None
    
    return {
        "target": target,
        "wordlist": wordlist,
        "attack_type": "custom"
    }

def create_attack_config(attack_info):
    """สร้าง config สำหรับการโจมตี"""
    config = {
        "attack_session": {
            "target": attack_info["target"],
            "wordlist": attack_info["wordlist"],
            "attack_type": attack_info["attack_type"],
            "created_at": datetime.now().isoformat(),
            "status": "ready"
        },
        "attack_settings": {
            "request_delay": 3,
            "max_attempts": 50,
            "use_proxy": True,
            "proxy_rotation": True,
            "user_agent_rotation": True,
            "ethical_mode": True
        }
    }
    
    with open('current_attack_config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    
    return config

def run_attack_mode(mode):
    """รันโหมดโจมตีที่เลือก"""
    print(f"\n🚀 กำลังเตรียมโหมดโจมตี...")
    
    if mode == "1":
        print("🔥 ALX Trading Attack Mode")
        attack_info = {
            "target": "alx.trading",
            "wordlist": "alx_trading_passwords.txt",
            "attack_type": "alx_trading"
        }
        config = create_attack_config(attack_info)
        print("✅ Config พร้อม - รัน: python run_alx_brute.py")
        
    elif mode == "2":
        print("⚡ WhatILove1728 Attack Mode")
        attack_info = {
            "target": "whatilove1728",
            "wordlist": "whatilove1728.txt",
            "attack_type": "whatilove1728"
        }
        config = create_attack_config(attack_info)
        print("✅ Config พร้อม - รัน: python run_enhanced_brute.py")
        
    elif mode == "3":
        print("🚀 Enhanced Brute Force Mode")
        print("✅ รัน: python run_enhanced_brute.py")
        
    elif mode == "4":
        print("🎯 Advanced Attack Engine Mode")
        print("✅ รัน: python run_advanced_brute.py")
        
    elif mode == "5":
        attack_info = setup_custom_target()
        if attack_info:
            config = create_attack_config(attack_info)
            print(f"✅ Custom attack config พร้อม")
            print(f"🎯 Target: {attack_info['target']}")
            print(f"📚 Wordlist: {attack_info['wordlist']}")
            print("✅ รัน: python run_enhanced_brute.py")

def show_ethical_notice():
    """แสดงข้อความเตือนด้านจริยธรรม"""
    print("\n" + "⚠️"*20)
    print("🛡️  ETHICAL HACKING NOTICE")
    print("⚠️"*20)
    print("🔴 เครื่องมือนี้สำหรับการทดสอบความปลอดภัยเท่านั้น")
    print("🔴 ใช้กับบัญชีที่คุณเป็นเจ้าของหรือได้รับอนุญาตเท่านั้น")
    print("🔴 การใช้เพื่อโจมตีบัญชีผู้อื่นผิดกฎหมาย")
    print("🔴 ผู้พัฒนาไม่รับผิดชอบการใช้งานที่ผิดกฎหมาย")
    print("⚠️"*20)
    
    consent = input("\n🤔 ยืนยันว่าจะใช้เพื่อการทดสอบที่ถูกกฎหมายเท่านั้น (yes/no): ").strip().lower()
    return consent in ['yes', 'y']

def main():
    print("🌸 SugarGlitch - Instagram Security Testing Tool")
    print("="*60)
    
    # แสดงข้อความเตือนจริยธรรม
    if not show_ethical_notice():
        print("❌ ยกเลิกการใช้งาน")
        return
    
    show_attack_modes()
    
    while True:
        mode = input("\n🎯 เลือกโหมดโจมตี (1-5): ").strip()
        
        if mode in ["1", "2", "3", "4", "5"]:
            run_attack_mode(mode)
            break
        else:
            print("❌ เลือกโหมด 1-5 เท่านั้น")
    
    print("\n🎉 SugarGlitch Attack Mode พร้อมใช้งาน!")
    print("📋 อ่านคู่มือเพิ่มเติม: ETHICAL_TESTING_GUIDE.md")

if __name__ == "__main__":
    main()
