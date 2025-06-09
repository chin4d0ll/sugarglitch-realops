# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔄 Quick Session Creator - Alternative Methods
เนื่องจาก GUI browser ไม่ทำงานใน codespace
"""

import json
import requests
import os
from datetime import datetime

def method_1_sample_session():
    """วิธีที่ 1: ใช้ sample session สำหรับทดสอบ"""
    print("🧪 METHOD 1: Sample Session for Testing")
    print("=" * 50)
    print("⚠️ This uses a sample sessionid that probably won't work")
    print("   But you can see how the system works")

    # Sample session (likely expired)
    sample_sessions = [
        {
            "sessionid": "12345678901:ABCDEFGHIJ:abcdef123456789",
            "csrftoken": "samplecsrftoken123456789",
            "note": "Sample session - likely expired"
        },
        {
            "sessionid": "98765432109:ZYXWVUTSRQ:zyxwvu987654321",
            "csrftoken": "anothersampletoken987654",
            "note": "Another sample - for demo only"
        }
    ]

    for i, session in enumerate(sample_sessions, 1):
        print(f"\n{i}. {session['note']}")
        print(f"   SessionID: {session['sessionid'][:30]}...")

    choice = input(f"\nChoose sample session (1-{len(sample_sessions)}) or Enter to skip: ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(sample_sessions):
        selected = sample_sessions[int(choice)-1]
        return selected['sessionid'], selected['csrftoken'], "sample_testing"

    return None, None, None

def method_2_curl_instructions():
    """วิธีที่ 2: แนะนำใช้ curl ดึง session"""
    print("\n🌐 METHOD 2: Extract Session with cURL")
    print("=" * 50)
    print("📋 Instructions:")
    print("1. Open Instagram in browser and login")
    print("2. Open Network tab in DevTools (F12)")
    print("3. Go to any Instagram page (refresh if needed)")
    print("4. Find any request to i.instagram.com")
    print("5. Right-click → Copy → Copy as cURL")
    print("6. Paste the cURL command here")
    print("\nExample format:")
    print("curl 'https://i.instagram.com/...' -H 'cookie: sessionid=...; csrftoken=...'")

    print("\n📝 Paste your cURL command (or Enter to skip):")
    curl_command = input().strip()

    if curl_command and 'sessionid=' in curl_command and 'curl' in curl_command.lower():
        # Extract sessionid and csrftoken from curl command
        sessionid = extract_from_curl(curl_command, 'sessionid=')
        csrftoken = extract_from_curl(curl_command, 'csrftoken=')

        if sessionid:
            print(f"✅ Extracted sessionid: {sessionid[:30]}...")
            print(f"✅ Extracted csrftoken: {csrftoken[:20]}..." if csrftoken else "⚠️ No csrftoken found")
            return sessionid, csrftoken or 'missing', "curl_extraction"

    return None, None, None

def method_3_direct_input():
    """วิธีที่ 3: ใส่ sessionid โดยตรง"""
    print("\n🔑 METHOD 3: Direct SessionID Input")
    print("=" * 50)
    print("📱 How to get sessionid:")
    print("1. Login to Instagram in browser")
    print("2. Press F12 → Application → Cookies → instagram.com")
    print("3. Copy the 'sessionid' value")

    sessionid = input("\n📋 Paste sessionid here (or Enter to skip): ").strip()

    if sessionid and len(sessionid) > 20:
        csrftoken = input("📋 Paste csrftoken (optional, Enter to skip): ").strip()
        return sessionid, csrftoken or 'missing', "direct_input"

    return None, None, None

def extract_from_curl(curl_command, key):
    """ดึงค่าจาก curl command"""
    try:
        # Find cookie header
        if f'{key}' in curl_command:
            start = curl_command.find(key) + len(key)
            end = curl_command.find(';', start)
            if end == -1:
                end = curl_command.find("'", start)
            if end == -1:
                end = curl_command.find('"', start)
            if end == -1:
                end = len(curl_command)

            value = curl_command[start:end].strip()
            return value if value else None
    except Exception:
        pass
    return None

def test_and_save_session(sessionid, csrftoken, method):
    """ทดสอบและบันทึก session"""
    print(f"\n🧪 Testing session from {method}...")

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrftoken,
        "Cookie": f"sessionid={sessionid}; csrftoken={csrftoken};"
    }

    # Quick test
    try:
        response = requests.get(
            "https://i.instagram.com/api/v1/accounts/current_user/",
            headers=headers,
            timeout=10
        )

        print(f"📊 Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if 'user' in data:
                user = data['user']
                username = user.get('username', 'Unknown')
                print(f"✅ SUCCESS! Username: {username}")

                # Save session
                session_data = {
                    "sessionid": sessionid,
                    "csrftoken": csrftoken,
                    "user_agent": headers["User-Agent"],
                    "cookies": {
                        "sessionid": sessionid,
                        "csrftoken": csrftoken
                    },
                    "user_info": {
                        "username": username,
                        "full_name": user.get('full_name', ''),
                        "user_id": str(user.get('pk', ''))
                    },
                    "created_at": datetime.now().isoformat(),
                    "method": method,
                    "status": "verified_working"
                }

                output_file = "/workspaces/sugarglitch-realops/tools/session_alx_trading.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(session_data, f, indent=2)

                print(f"💾 Session saved: {output_file}")
                return True
            else:
                print("❌ No user data in response")
        else:
            print(f"❌ Failed - Status {response.status_code}")

    except Exception as e:
        print(f"❌ Test failed: {e}")

    return False

def main():
    print("🚀 Quick Session Creator - Alternative Methods")
    print("=" * 60)
    print("💡 Since GUI browser doesn't work in codespace,")
    print("   here are alternative ways to create a session:")

    # Try different methods
    methods = [
        method_1_sample_session,
        method_2_curl_instructions,
        method_3_direct_input
    ]

    for method_func in methods:
        sessionid, csrftoken, method_name = method_func()

        if sessionid:
            if test_and_save_session(sessionid, csrftoken, method_name):
                print("\n🎉 Session created successfully!")
                print("\n🎯 Next steps:")
                print("1. Run: python3 tools/simple_dm_test.py")
                print("2. If successful: Run DM extractors")
                return
            else:
                print("⚠️ Session didn't work, trying next method...")
                continue

    print("\n❌ No working session created")
    print("\n💡 Alternative: Use the manual session generator:")
    print("   python3 tools/simple_session_generator.py")
    print("   (You'll need to input a real sessionid manually)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
