#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 POWER ATTACK LAUNCHER
เริ่มต้นใช้งาน Ultimate Account Hacker
"""

import os
import sys

def show_power_menu():
    """แสดงเมนูขั้นสูง"""
    print("🔥 ULTIMATE INSTAGRAM HACKER MENU 🔥")
    print("="*60)
    print("🎯 The Most Powerful Account Access Scripts")
    print()
    print("1️⃣  🔑 Advanced CSRF Token Extractor")
    print("    • Extract CSRF with 5 different methods")
    print("    • Mobile API, GraphQL, Web API endpoints")
    print("    • Auto-save configuration")
    print()
    print("2️⃣  🔥 Ultimate Account Hacker")
    print("    • Multi-vector attack system")
    print("    • API + Browser + Session hijacking")
    print("    • Undetectable browser automation")
    print("    • Human behavior simulation")
    print()
    print("3️⃣  ⚡ Quick CSRF + Attack Combo")
    print("    • Extract CSRF then launch attack")
    print("    • Automatic workflow")
    print("    • Maximum success rate")
    print()
    print("4️⃣  🛠️ Debug & Test Mode")
    print("    • Test CSRF extraction")
    print("    • Browser compatibility check")
    print("    • Connection validation")
    print()

def run_csrf_extractor():
    """รัน CSRF extractor"""
    print("🔑 Starting Advanced CSRF Token Extractor...")
    os.system('python advanced_csrf_extractor.py')

def run_ultimate_hacker():
    """รัน Ultimate Account Hacker"""
    print("🔥 Starting Ultimate Account Hacker...")
    os.system('python ultimate_account_hacker.py')

def run_combo_attack():
    """รัน CSRF + Attack combo"""
    print("⚡ Starting CSRF + Attack Combo...")
    
    print("Step 1: Extracting CSRF token...")
    os.system('python advanced_csrf_extractor.py')
    
    print("\nStep 2: Launching Ultimate Attack...")
    os.system('python ultimate_account_hacker.py')

def run_debug_mode():
    """รัน debug mode"""
    print("🛠️ Debug & Test Mode")
    print("="*30)
    
    print("🔍 1. Testing CSRF extraction...")
    try:
        from advanced_csrf_extractor import AdvancedCSRFExtractor
        extractor = AdvancedCSRFExtractor()
        token = extractor.get_ultimate_csrf()
        if token:
            print(f"✅ CSRF extraction working: {token[:20]}...")
        else:
            print("❌ CSRF extraction failed")
    except Exception as e:
        print(f"❌ CSRF test error: {e}")
    
    print("\n🔍 2. Testing browser setup...")
    try:
        from ultimate_account_hacker import UltimateAccountHacker
        hacker = UltimateAccountHacker()
        if hacker.setup_ultimate_browser():
            print("✅ Browser setup working")
            hacker.cleanup()
        else:
            print("❌ Browser setup failed")
    except Exception as e:
        print(f"❌ Browser test error: {e}")
    
    print("\n🔍 3. Testing connection...")
    try:
        import requests
        response = requests.get('https://www.instagram.com/', timeout=10)
        if response.status_code == 200:
            print(f"✅ Connection working: {response.status_code}")
        else:
            print(f"⚠️ Connection issues: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection test error: {e}")

def main():
    print("🚀 POWER ATTACK LAUNCHER")
    print("Ultimate Instagram Account Access")
    print("="*60)
    
    while True:
        show_power_menu()
        
        choice = input("\n🎯 Select option (1-4): ").strip()
        
        if choice == "1":
            run_csrf_extractor()
            break
        elif choice == "2":
            run_ultimate_hacker()
            break
        elif choice == "3":
            run_combo_attack()
            break
        elif choice == "4":
            run_debug_mode()
            break
        else:
            print("❌ Invalid choice! Please select 1-4")
            continue
    
    print("\n🎉 Attack session completed!")

if __name__ == "__main__":
    main()
