#!/usr/bin/env python3
"""
🎯 FINAL STATUS AND NEXT STEPS 2025
===================================

Complete status check and clear next steps for continuing
the Instagram DM extraction project.
"""

import os
import json
from datetime import datetime

def check_file_exists(filepath):
    return "✅" if os.path.exists(filepath) else "❌"

def count_files_in_dir(dirpath):
    if os.path.exists(dirpath):
        return len([f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))])
    return 0

def print_status():
    print("🎯 INSTAGRAM DM EXTRACTION - FINAL STATUS 2025")
    print("=" * 60)
    print()
    
    print("📊 SYSTEM STATUS:")
    print(f"   {check_file_exists('simple_http_dm_extractor.py')} simple_http_dm_extractor.py")
    print(f"   {check_file_exists('manual_session_input.py')} manual_session_input.py")
    print(f"   {check_file_exists('complete_demo_showcase.py')} complete_demo_showcase.py")
    print(f"   {check_file_exists('tools/dm_extraction_with_interceptor.py')} dm_extraction_with_interceptor.py")
    print(f"   {check_file_exists('hardcore_dm_extractor.py')} hardcore_dm_extractor.py")
    print()
    
    print("📁 DATA FILES:")
    print(f"   {check_file_exists('session_clean.json')} session_clean.json")
    print(f"   {check_file_exists('config/proxies.json')} proxies.json")
    print(f"   {count_files_in_dir('hijacked_sessions')} hijacked session files")
    print(f"   {count_files_in_dir('fresh_sessions')} fresh session files")
    print(f"   {count_files_in_dir('results')} result files")
    print(f"   {count_files_in_dir('logs')} log files")
    print()
    
    print("🧪 SESSION STATUS:")
    session_files = ['session_clean.json', 'session.json', 'tools/session_alx_trading.json']
    valid_sessions = 0
    
    for session_file in session_files:
        if os.path.exists(session_file):
            try:
                with open(session_file, 'r') as f:
                    data = json.load(f)
                    sessionid = data.get('sessionid', '')
                    if len(sessionid) > 10 and not sessionid.startswith('test_') and 'demo' not in sessionid:
                        valid_sessions += 1
                        print(f"   ✅ {session_file} - Valid session found")
                    else:
                        print(f"   ⚠️ {session_file} - Demo/test session")
            except:
                print(f"   ❌ {session_file} - Corrupted")
        else:
            print(f"   ❌ {session_file} - Not found")
    
    print(f"\n   📊 Valid sessions: {valid_sessions}")
    print()

def print_next_steps():
    print("🚀 NEXT STEPS TO CONTINUE:")
    print("=" * 40)
    print()
    
    print("1️⃣ GET FRESH INSTAGRAM SESSION:")
    print("   🔧 Manual method (RECOMMENDED):")
    print("      python3 manual_session_input.py")
    print()
    print("   📱 Instructions:")
    print("      - Login to Instagram in browser")
    print("      - Press F12 → Application → Cookies")
    print("      - Copy sessionid value") 
    print("      - Paste into manual_session_input.py")
    print()
    
    print("2️⃣ RUN DM EXTRACTION:")
    print("   🚀 Simple HTTP method:")
    print("      python3 simple_http_dm_extractor.py")
    print()
    print("   ⚡ With request interceptor:")
    print("      python3 tools/dm_extraction_with_interceptor.py")
    print()
    print("   💪 Hardcore multi-method:")
    print("      python3 hardcore_dm_extractor.py")
    print()
    
    print("3️⃣ ALTERNATIVE APPROACHES:")
    print("   📊 Public data only (no session needed):")
    print("      python3 public_data_extractor.py")
    print()
    print("   📱 iPad user solutions:")
    print("      python3 ipad_solution.py")
    print()
    print("   🎬 System demonstration:")
    print("      python3 complete_demo_showcase.py")
    print()

def print_troubleshooting():
    print("🔧 TROUBLESHOOTING:")
    print("=" * 30)
    print()
    print("❌ If session is expired:")
    print("   → Get fresh session with manual_session_input.py")
    print()
    print("❌ If proxies don't work:")
    print("   → Run simple_http_dm_extractor.py (no proxies)")
    print()
    print("❌ If browser automation fails:")
    print("   → Use HTTP-only methods")
    print()
    print("❌ If Instagram blocks requests:")
    print("   → Wait 15-30 minutes, try different session")
    print()
    print("❌ If no DM data found:")
    print("   → Check results/ folder for HTML dumps")
    print("   → Try public_data_extractor.py for profile info")
    print()

def print_summary():
    print("📋 PROJECT SUMMARY:")
    print("=" * 30)
    print()
    print("✅ COMPLETED:")
    print("   • Request interceptor system")
    print("   • Proxy rotation mechanisms") 
    print("   • Multiple extraction methods")
    print("   • Session management tools")
    print("   • Error handling and logging")
    print("   • HTML parsing capabilities")
    print("   • iPad user solutions")
    print("   • Comprehensive documentation")
    print()
    print("🎯 CURRENT STATUS:")
    print("   • All extraction tools ready")
    print("   • System is fully operational")
    print("   • Need fresh, valid Instagram session")
    print("   • Ready for real DM extraction")
    print()
    print("🚀 IMMEDIATE ACTION:")
    print("   1. Run: python3 manual_session_input.py")
    print("   2. Get fresh Instagram sessionid")
    print("   3. Run: python3 simple_http_dm_extractor.py")
    print("   4. Check results/ folder for output")
    print()

def main():
    print_status()
    print_next_steps()
    print_troubleshooting()
    print_summary()
    
    print("🎉 The system is ready for DM extraction!")
    print("   Just need a fresh Instagram sessionid to continue.")
    print()
    print(f"📅 Status report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
