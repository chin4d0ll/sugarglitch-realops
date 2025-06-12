# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔧 MANUAL SESSION INPUT TOOL
===========================

Simple tool to manually input a valid Instagram sessionid
and test it immediately.
"""

import json
import requests
import os

def get_session_input():
    """Get session from user input"""
    print("🔧 MANUAL SESSION INPUT TOOL")
    print("=" * 40)
    print()
    print("📋 INSTRUCTIONS:")
    print("1. Open Instagram in your browser")
    print("2. Login to your account")
    print("3. Press F12 to open Developer Tools")
    print("4. Go to Application → Storage → Cookies → https://www.instagram.com")
    print("5. Find 'sessionid' and copy its value")
    print()

    sessionid = input("🔑 Paste your sessionid here: ").strip()

    if len(sessionid) < 10:
        print("❌ Session too short, please try again")
        return None

    return sessionid

def test_session(sessionid):
    """Test if session is valid"""
    print("🧪 Testing session validity...")

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q = 0.9,*/*;q = 0.8',
    })
    session.cookies.set('sessionid', sessionid)

    try:
        # Test with profile page
        response = session.get('https://www.instagram.com/accounts/edit/', timeout = 10)

        if response.status_code == 200:
            if 'Edit Profile' in response.text or 'edit_profile' in response.text:
                print("✅ Session is VALID!")
                return True
            else:
                print("⚠️ Session might be expired or limited")

        print(f"❌ Session test failed - Status: {response.status_code}")
        return False

    except Exception as e:
        print(f"❌ Session test error: {e}")
        return False

def save_session(sessionid, target="alx.trading"):
    """Save session to file"""
    session_data = {
        "sessionid": sessionid,
        "target": target,
        "created": "manual_input",
        "timestamp": "2025-06-06"
    }

    # Save to multiple locations
    files = [
        "session_clean.json",
        "tools/session_alx_trading.json",
        "fresh_sessions/manual_session.json"
    ]

    os.makedirs("fresh_sessions", exist_ok = True)

    for filename in files:
        try:
            with open(filename, 'w') as f:
                json.dump(session_data, f, indent = 2)
            print(f"✅ Saved to {filename}")
        except Exception as e:
            print(f"❌ Failed to save {filename}: {e}")

def main():
    sessionid = get_session_input()

    if sessionid:
        if test_session(sessionid):
            save_session(sessionid)
            print()
            print("🎉 SUCCESS! Session saved and ready to use")
            print()
            print("🚀 NEXT STEPS:")
            print("   python3 simple_http_dm_extractor.py")
            print("   python3 tools/dm_extraction_with_interceptor.py")
        else:
            print("❌ Session is not valid. Please try getting a fresh one.")
    else:
        print("❌ No session provided")

if __name__ == "__main__":
    main()
