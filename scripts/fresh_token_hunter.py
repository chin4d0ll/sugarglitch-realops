# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔑 FRESH SESSION TOKEN HUNTER
Get new valid Instagram session tokens
"""

import requests
import json
import time
from datetime import datetime

def get_fresh_tokens():
    """หา fresh session tokens จากหลายวิธี"""

    print("🔍 FRESH TOKEN HUNTER")
    print("=" * 50)

    # Method 1: Check existing session files
    session_files = [
        "session.json",
        "session_clean.json",
        "alx_trading_session_fleming654.json",
        "sessions/*/session.json"
    ]

    for session_file in session_files:
        try:
            with open(session_file, 'r') as f:
                data = json.load(f)
                if 'sessionid' in data:
                    token = data['sessionid']
                    print(f"📁 Found token in {session_file}: {token[:20]}...")
                    if test_token_validity(token):
                        return token
        except Exception:
            continue

    # Method 2: Browser extraction guide
    print("\n🌐 BROWSER EXTRACTION METHOD:")
    print("1. เปิด Instagram ใน browser")
    print("2. Login เข้าบัญชี")
    print("3. กด F12 -> Application -> Cookies")
    print("4. หา 'sessionid' copy value")
    print("5. วางใส่ใน fresh_token.txt")

    # Method 3: Mobile app session
    print("\n📱 MOBILE APP METHOD:")
    print("1. เปิด Instagram app บนมือถือ")
    print("2. ใช้ Packet Capture (Charles/Burp)")
    print("3. ดักจับ sessionid จาก request headers")

    return None

def test_token_validity(token):
    """ทดสอบว่า token ยังใช้ได้หรือไม่"""

    headers = {
        'User-Agent': 'Instagram 123.0.0.26.121 Android',
        'Cookie': f'sessionid={token}'
    }

    try:
        response = requests.get('https://www.instagram.com/', headers = headers, timeout = 10)
        if response.status_code == 200 and '"is_logged_in":true' in response.text:
            print(f"✅ Token valid!")
            return True
        else:
            print(f"❌ Token invalid (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Error testing token: {e}")
        return False

if __name__ == "__main__":
    token = get_fresh_tokens()
    if token:
        print(f"\n🎉 Valid token found: {token}")
        # Save to file
        with open("fresh_token.txt", "w") as f:
            f.write(token)
        print("💾 Saved to fresh_token.txt")
    else:
        print("\n⚠️ No valid tokens found. Manual extraction needed.")
