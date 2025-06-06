#!/usr/bin/env python3
"""
Instagram DM Extraction - Problem Solver
Addresses all current issues with DM extraction
"""

import json
import requests
import time
import sys
from pathlib import Path

def main():
    print("🚨 Instagram DM Extraction - Problem Analysis")
    print("=" * 60)
    
    # Current problems identified
    problems = [
        "❌ Instagram username 'alx.trading' not found",
        "❌ IP address blocked by Instagram", 
        "❌ All session files expired/invalid",
        "❌ No real DM data extracted"
    ]
    
    for problem in problems:
        print(problem)
    
    print("\n🔧 SOLUTION STEPS:")
    print("=" * 60)
    
    print("\n1️⃣ USERNAME CORRECTION:")
    print("   Instagram usernames cannot contain periods (.) in the middle")
    print("   'alx.trading' is INVALID - must be:")
    print("   • alxtrading")
    print("   • alx_trading") 
    print("   • alx-trading (but - is not allowed either)")
    print("   • alxtrading_")
    
    print("\n2️⃣ IP BLOCKING SOLUTION:")
    print("   Instagram has blocked the current IP address")
    print("   Solutions:")
    print("   • Use proxy rotation")
    print("   • Use VPN")
    print("   • Wait for IP unblock (24-48 hours)")
    print("   • Use different server/environment")
    
    print("\n3️⃣ SESSION ACQUISITION:")
    print("   All current sessions are expired")
    print("   Need fresh session via:")
    print("   • Manual browser login")
    print("   • Copy sessionid from browser dev tools")
    print("   • Use unblocked IP for login")
    
    print("\n4️⃣ IMMEDIATE NEXT STEPS:")
    print("   1. Verify correct username exists on Instagram")
    print("   2. Get fresh sessionid from browser (manual)")
    print("   3. Use proxy/VPN to avoid IP block")
    print("   4. Test extraction with valid session")
    
    print("\n" + "🔍 Checking actual Instagram account...")
    
    # Check the most likely usernames
    likely_usernames = ["alxtrading", "alx_trading", "alxtrading_"]
    
    for username in likely_usernames:
        try:
            url = f"https://www.instagram.com/{username}/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200 and "Sorry, this page isn't available" not in response.text:
                print(f"✅ FOUND: {username} exists on Instagram!")
                
                # Create corrected config
                corrected_config = {
                    "correct_username": username,
                    "original_invalid": "alx.trading",
                    "status": "found",
                    "url": url
                }
                
                with open("corrected_username.json", "w") as f:
                    json.dump(corrected_config, f, indent=2)
                
                print(f"📁 Saved correct username to: corrected_username.json")
                break
            else:
                print(f"❌ {username} - not found")
                
        except Exception as e:
            print(f"❌ {username} - error: {e}")
    
    print("\n" + "🎯 MANUAL STEPS REQUIRED:")
    print("=" * 60)
    print("1. Open Instagram in browser")
    print("2. Log into your account")  
    print("3. Navigate to the correct username found above")
    print("4. Open Developer Tools (F12)")
    print("5. Go to Application/Storage → Cookies")
    print("6. Find 'sessionid' cookie and copy its value")
    print("7. Save sessionid to a new file")
    print("8. Re-run extraction with correct username and fresh session")
    
    print(f"\n💡 The key issue: 'alx.trading' is not a valid Instagram username!")
    print(f"   Instagram usernames cannot contain periods in the middle.")

if __name__ == "__main__":
    main()
