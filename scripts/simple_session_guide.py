# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Simple Session Guide for Instagram DM Extraction
Step-by-step guide to get your Instagram sessionid
"""

import json
import os
from datetime import datetime

def get_session_guide():
    """Guide user through getting sessionid"""
    print("🔐 HOW TO GET YOUR INSTAGRAM SESSIONID")
    print("="*50)
    print()
    print("STEP 1: Open Instagram in your browser")
    print("- Go to https://www.instagram.com")
    print("- Log in to your account")
    print()
    print("STEP 2: Open Developer Tools")
    print("- Press F12 (or right-click → Inspect)")
    print("- Go to 'Application' tab (Chrome) or 'Storage' tab (Firefox)")
    print()
    print("STEP 3: Find Cookies")
    print("- In the left sidebar, expand 'Cookies'")
    print("- Click on 'https://www.instagram.com'")
    print()
    print("STEP 4: Copy sessionid")
    print("- Find the cookie named 'sessionid'")
    print("- Copy its Value (long string of letters and numbers)")
    print()
    print("STEP 5: Paste it below")
    print("- The sessionid should be about 40+ characters long")
    print("- It typically starts with letters/numbers")
    print()

def save_session_simple(sessionid, target="alx.trading"):
    """Save sessionid in simple format"""
    session_data = {
        'sessionid': sessionid,
        'target': target,
        'created_at': datetime.now().isoformat(),
        'status': 'active'
    }

    # Ensure tools directory exists
    os.makedirs("tools", exist_ok = True)

    session_file = f"tools/session_{target.replace('.', '_')}.json"

    try:
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent = 2)
        print(f"✅ Session saved to: {session_file}")
        return session_file
    except Exception as e:
        print(f"❌ Failed to save session: {e}")
        return None

def test_session_quick(sessionid):
    """Quick test of sessionid"""
    import requests

    headers = {
        'Cookie': f'sessionid={sessionid}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get('https://www.instagram.com/', headers = headers, timeout = 10)
        if 'login' in response.url.lower():
            return False, "Session expired - redirected to login"
        else:
            return True, "Session appears valid"
    except Exception as e:
        return False, f"Test failed: {e}"

def main():
    print("🎯 INSTAGRAM DM EXTRACTION - SESSION SETUP")
    print("="*60)
    print()

    get_session_guide()

    while True:
        sessionid = input("Enter your sessionid: ").strip()

        if not sessionid:
            print("❌ Please enter a sessionid")
            continue

        if len(sessionid) < 20:
            print("❌ Sessionid seems too short. Please check and try again.")
            continue

        print(f"\n🔍 Testing sessionid (first 20 chars): {sessionid[:20]}...")

        is_valid, message = test_session_quick(sessionid)
        print(f"Result: {message}")

        if is_valid:
            print("✅ Session test passed!")
            session_file = save_session_simple(sessionid)
            if session_file:
                print(f"\n🎉 SUCCESS!")
                print(f"Your session is saved and ready to use.")
                print(f"File: {session_file}")
                print(f"\nNext step: Run the DM extractor with this session.")
                break
        else:
            print("❌ Session test failed.")
            retry = input("Try again? (y/n): ").lower()
            if not retry.startswith('y'):
                break

    print("\nDone!")

if __name__ == "__main__":
    main()
