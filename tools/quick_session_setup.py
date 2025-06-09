# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Quick Session Setup Tool
Streamlined tool for obtaining and testing Instagram session
"""

import os
import json
import sys
import requests
from datetime import datetime

def get_session_manually():
    """Get session data from user input"""
    print("\n" + "="*60)
    print("📝 MANUAL SESSION INPUT")
    print("="*60)
    print("To get your Instagram session:")
    print("1. Open Instagram in your browser and log in")
    print("2. Press F12 to open Developer Tools")
    print("3. Go to Application/Storage > Cookies > https://www.instagram.com")
    print("4. Find and copy the 'sessionid' value")
    print("5. Paste it below")
    print()

    sessionid = input("Enter your Instagram sessionid: ").strip()

    if not sessionid:
        print("❌ Sessionid is required!")
        return None

    # Optional additional cookies for better reliability
    print("\nOptional cookies (press Enter to skip):")
    csrftoken = input("csrftoken: ").strip()
    ds_user_id = input("ds_user_id: ").strip()

    session_data = {
        'sessionid': sessionid,
        'csrftoken': csrftoken,
        'ds_user_id': ds_user_id
    }

    return session_data

def test_session(session_data):
    """Test if session is valid"""
    print("\n🔍 Testing session validity...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    # Build cookie string
    cookies = []
    for key, value in session_data.items():
        if value:  # Only include non-empty values
            cookies.append(f"{key}={value}")

    if cookies:
        headers['Cookie'] = "; ".join(cookies)

    try:
        # Test Instagram main page
        response = requests.get('https://www.instagram.com/', headers=headers, timeout=10)

        if response.status_code == 200:
            if 'login' in response.url.lower() or '"is_logged_in":false' in response.text:
                print("❌ Session invalid - not logged in")
                return False
            else:
                print("✅ Session is valid!")
                return True
        else:
            print(f"❌ HTTP error: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Error testing session: {e}")
        return False

def save_session(session_data, target="alx.trading"):
    """Save session to file"""
    session_info = {
        'sessionid': session_data.get('sessionid', ''),
        'csrftoken': session_data.get('csrftoken', ''),
        'ds_user_id': session_data.get('ds_user_id', ''),
        'target': target,
        'created_at': datetime.now().isoformat(),
        'status': 'active'
    }

    os.makedirs('tools', exist_ok=True)
    session_file = 'tools/session_alx_trading.json'

    try:
        with open(session_file, 'w') as f:
            json.dump(session_info, f, indent=2)
        print(f"✅ Session saved to {session_file}")
        return True
    except Exception as e:
        print(f"❌ Failed to save session: {e}")
        return False

def main():
    print("🚀 QUICK SESSION SETUP FOR INSTAGRAM DM EXTRACTION")
    print("="*60)

    # Get session data
    session_data = get_session_manually()
    if not session_data:
        print("❌ No session data provided")
        return False

    # Test session
    if not test_session(session_data):
        print("❌ Session test failed")
        return False

    # Save session
    if not save_session(session_data):
        print("❌ Failed to save session")
        return False

    print("\n🎉 SUCCESS! Session is valid and saved!")
    print("\nNext steps:")
    print("1. Add working proxies to config/proxies.json")
    print("2. Run DM extraction with interceptor protection")
    print("3. Check logs/requests.log for monitoring")

    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
