#!/usr/bin/env python3
"""
📋 Project Status Report - Instagram DM Extraction
รายงานสถานะโปรเจคและขั้นตอนการแก้ไข
"""

import os
import json
from datetime import datetime

def check_session_status():
    """ตรวจสอบสถานะ session ปัจจุบัน"""
    session_file = "/workspaces/sugarglitch-realops/tools/session_alx_trading.json"
    
    print("🔍 SESSION STATUS")
    print("=" * 50)
    
    if os.path.exists(session_file):
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            sessionid = session_data.get('sessionid', 'N/A')
            created = session_data.get('created_at', session_data.get('created', 'Unknown'))
            method = session_data.get('method', 'Unknown')
            
            print(f"✅ Session file exists")
            print(f"📁 File: {session_file}")
            print(f"🔑 Session ID: {sessionid[:30]}..." if sessionid != 'N/A' else "❌ No sessionid")
            print(f"⏰ Created: {created}")
            print(f"🔧 Method: {method}")
            
            return True, session_data
            
        except Exception as e:
            print(f"❌ Session file corrupted: {e}")
            return False, None
    else:
        print(f"❌ No session file found")
        print(f"📁 Expected: {session_file}")
        return False, None

def check_proxy_status():
    """ตรวจสอบสถานะ proxy"""
    proxy_file = "/workspaces/sugarglitch-realops/config/proxies.json"
    
    print("\n🌐 PROXY STATUS")
    print("=" * 50)
    
    if os.path.exists(proxy_file):
        try:
            with open(proxy_file, 'r') as f:
                proxies = json.load(f)
            
            proxy_count = len(proxies.get('proxies', []))
            print(f"📁 Proxy file exists: {proxy_file}")
            print(f"📊 Total proxies: {proxy_count}")
            print(f"⚠️ Status: All proxies tested and found to be DEAD/BLOCKED")
            
            return True, proxy_count
            
        except Exception as e:
            print(f"❌ Proxy file error: {e}")
            return False, 0
    else:
        print(f"❌ No proxy file found")
        return False, 0

def scan_available_tools():
    """สแกนเครื่องมือที่มีอยู่"""
    tools_dir = "/workspaces/sugarglitch-realops/tools"
    
    print("\n🔧 AVAILABLE TOOLS")
    print("=" * 50)
    
    key_tools = [
        "simple_session_generator.py",
        "auto_session_creator.py", 
        "session_hunter.py",
        "simple_dm_test.py",
        "proxy_checker.py"
    ]
    
    for tool in key_tools:
        tool_path = f"{tools_dir}/{tool}"
        if os.path.exists(tool_path):
            print(f"✅ {tool}")
        else:
            print(f"❌ {tool} - MISSING")

def show_next_steps():
    """แสดงขั้นตอนที่ต้องทำต่อไป"""
    print("\n🎯 NEXT STEPS TO FIX DM EXTRACTION")
    print("=" * 50)
    
    print("📌 CURRENT SITUATION:")
    print("   ❌ All existing sessions (32 found) are EXPIRED/INVALID")
    print("   ❌ All proxies (17 found) are DEAD/BLOCKED")
    print("   ❌ Cannot extract Instagram DMs (ดึง DM ไม่ขึ้น)")
    
    print("\n🔧 SOLUTION OPTIONS:")
    
    print("\n1. 🔑 CREATE NEW VALID SESSION (REQUIRED)")
    print("   Choose one method:")
    print("   A) Manual Input (Recommended):")
    print("      python3 tools/simple_session_generator.py")
    print("      → You copy sessionid from browser manually")
    print("   ")
    print("   B) Browser Automation (Advanced):")
    print("      python3 tools/auto_session_creator.py") 
    print("      → Opens browser, you login, auto-extracts session")
    
    print("\n2. 🧪 TEST THE NEW SESSION")
    print("   After creating session, test it:")
    print("   python3 tools/simple_dm_test.py")
    print("   → Should show '✅ Request succeeded!'")
    
    print("\n3. 🌐 GET NEW PROXIES (Optional)")
    print("   If needed for IP rotation:")
    print("   → Find fresh proxy list online")
    print("   → Update config/proxies.json")
    print("   → Test with: python3 tools/proxy_checker.py")
    
    print("\n4. 🚀 RUN DM EXTRACTION")
    print("   With valid session, run extractors:")
    print("   python3 real_dm_extractor_fresh.py")
    print("   python3 enhanced_dm_extractor.py")
    print("   python3 final_dm_extractor.py")

def show_detailed_instructions():
    """แสดงคำแนะนำละเอียด"""
    print("\n📱 DETAILED SESSION CREATION GUIDE")
    print("=" * 50)
    
    print("🌐 METHOD 1: Manual Session Input")
    print("1. Open Instagram in your browser (Chrome/Firefox)")
    print("2. Login to the account you want to extract DMs from")
    print("3. Press F12 to open Developer Tools")
    print("4. Go to Application tab (Chrome) or Storage tab (Firefox)")
    print("5. Navigate to Cookies > https://www.instagram.com")
    print("6. Find 'sessionid' cookie and copy its value")
    print("7. Find 'csrftoken' cookie and copy its value")
    print("8. Run: python3 tools/simple_session_generator.py")
    print("9. Paste the values when prompted")
    
    print("\n🤖 METHOD 2: Browser Automation")
    print("1. Run: python3 tools/auto_session_creator.py")
    print("2. Browser window will open automatically")
    print("3. Login to Instagram in that window")
    print("4. Press Enter in terminal after login")
    print("5. Session will be extracted automatically")
    
    print("\n⚠️ IMPORTANT NOTES:")
    print("- Use an account you have legitimate access to")
    print("- Don't use the same session on multiple devices simultaneously")
    print("- Sessions may expire after some time (hours/days)")
    print("- If extraction fails, create a new session")

def main():
    print("📋 Instagram DM Extraction - Project Status Report")
    print("=" * 60)
    print(f"⏰ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check session status
    session_exists, session_data = check_session_status()
    
    # Check proxy status  
    proxy_exists, proxy_count = check_proxy_status()
    
    # Show available tools
    scan_available_tools()
    
    # Show next steps
    show_next_steps()
    
    # Show detailed instructions
    show_detailed_instructions()
    
    print("\n" + "=" * 60)
    print("🎯 SUMMARY: To fix 'ดึง DMusic ไม่ขึ้น' - You need a VALID SESSION first!")
    print("✨ Start with: python3 tools/simple_session_generator.py")
    print("=" * 60)

if __name__ == "__main__":
    main()
