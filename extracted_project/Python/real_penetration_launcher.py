#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💀 REAL PENETRATION LAUNCHER 💀
SugarGlitch - Dream Edition
No Demo, No Fake - Only Real Attack
"""

import os
import sys
import json
from datetime import datetime

def show_banner():
    print("💀" * 25)
    print("💀 REAL PENETRATION ATTACK SYSTEM 💀")
    print("💀 SugarGlitch - Dream Edition     💀")
    print("💀 No Demo, No Fake - Only Real   💀")
    print("💀" * 25)
    print()
    print("⚠️  WARNING: REAL ATTACK SYSTEM")
    print("📋 Target: Instagram accounts")
    print("🎯 Mode: Live penetration testing")
    print()

def check_requirements():
    """ตรวจสอบไฟล์ที่จำเป็น"""
    required_files = [
        'ultimate_fixed_hacker.py',
        'dream_api_hacker.py', 
        'fixed_attack_menu.py',
        'high_probability_targets.txt',
        'personal_passlist.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   • {file}")
        return False
    
    print("✅ All required files found")
    return True

def show_attack_options():
    print("🚀 SELECT ATTACK METHOD:")
    print()
    print("1️⃣  💀 Ultimate Fixed Hacker")
    print("    • Direct Chrome automation")
    print("    • CSRF token bypass")
    print("    • Real session extraction")
    print()
    print("2️⃣  🔥 Dream API Hacker")
    print("    • Pure API attacks")
    print("    • No GUI, faster execution")
    print("    • Advanced endpoint hitting")
    print()
    print("3️⃣  ⚡ Full Attack Menu")
    print("    • All 3 methods combined")
    print("    • Session hijack + replay")
    print("    • Complete penetration suite")
    print()
    print("0️⃣  ❌ Exit")
    print()

def log_attack_start():
    """บันทึกการเริ่มต้นการโจมตี"""
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "type": "REAL_ATTACK_START",
        "target_system": "Instagram",
        "attack_mode": "Real Penetration",
        "warning": "This is not a demo - real attack in progress"
    }
    
    os.makedirs('attack_logs', exist_ok=True)
    with open('attack_logs/real_attack_log.json', 'w') as f:
        json.dump(log_data, f, indent=4)

def main():
    show_banner()
    
    if not check_requirements():
        print("\n❌ Cannot proceed without required files")
        sys.exit(1)
    
    # Final confirmation
    print("🔥 FINAL CONFIRMATION:")
    confirm = input("Type 'REAL ATTACK' to proceed with live penetration: ").strip()
    
    if confirm != "REAL ATTACK":
        print("❌ Attack cancelled")
        sys.exit(0)
    
    log_attack_start()
    print("\n✅ Attack logged - proceeding...")
    
    while True:
        show_attack_options()
        choice = input("💀 Select attack method (1-3, 0 to exit): ").strip()
        
        if choice == "1":
            print("\n🚀 Launching Ultimate Fixed Hacker...")
            os.system('python ultimate_fixed_hacker.py')
            break
            
        elif choice == "2":
            print("\n🚀 Launching Dream API Hacker...")
            os.system('python dream_api_hacker.py')
            break
            
        elif choice == "3":
            print("\n🚀 Launching Full Attack Menu...")
            os.system('python fixed_attack_menu.py')
            break
            
        elif choice == "0":
            print("❌ Attack cancelled by user")
            break
            
        else:
            print("❌ Invalid choice. Select 1-3 or 0")

if __name__ == "__main__":
    main()
