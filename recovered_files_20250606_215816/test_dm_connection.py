# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔍 QUICK INSTAGRAM CONNECTION TEST
ทดสอบการเชื่อมต่อ Instagram และตรวจสอบ session
"""

import json
import requests
import os

def test_instagram_connection():
    """ทดสอบการเชื่อมต่อ Instagram"""
    print("🔍 TESTING INSTAGRAM CONNECTION")
    print("=" * 40)

    # โหลด session
    session_file = "/workspaces/sugarglitch-realops/sessions/session-alx.trading"

    try:
        with open(session_file, 'r') as f:
            session_data = json.load(f)
            cookies = session_data.get('cookies', {})
            print(f"✅ Session loaded: {list(cookies.keys())}")
    except Exception as e:
        print(f"❌ Cannot load session: {e}")
        return False

    # สร้าง session
    session = requests.Session()

    # เพิ่ม cookies
    for name, value in cookies.items():
        session.cookies.set(name, value, domain='.instagram.com')

    # Headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://www.instagram.com/',
    }

    session.headers.update(headers)

    # ทดสอบการเข้าถึง Instagram
    try:
        print("\n📡 Testing Instagram homepage...")
        response = session.get("https://www.instagram.com/", timeout=10)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            content = response.text

            # ตรวจสอบการ login
            if '"is_logged_in":true' in content:
                print("✅ Successfully logged in to Instagram!")
                return True
            elif '"is_logged_in":false' in content:
                print("❌ Session expired - not logged in")
                return False
            else:
                print("⚠️ Cannot determine login status")
                # ตรวจสอบ indicators อื่น
                if 'Instagram' in content and len(content) > 10000:
                    print("✅ Instagram accessible (possible login)")
                    return True
                else:
                    print("❌ Instagram not accessible")
                    return False
        else:
            print(f"❌ Cannot access Instagram: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_target_profile():
    """ทดสอบการเข้าถึงโปรไฟล์ target"""
    print("\n🎯 TESTING TARGET PROFILE ACCESS")
    print("=" * 40)

    # โหลด session
    session_file = "/workspaces/sugarglitch-realops/sessions/session-alx.trading"

    try:
        with open(session_file, 'r') as f:
            session_data = json.load(f)
            cookies = session_data.get('cookies', {})
    except Exception:
        print("❌ Cannot load session")
        return False

    session = requests.Session()
    for name, value in cookies.items():
        session.cookies.set(name, value, domain='.instagram.com')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    session.headers.update(headers)

    # ทดสอบโปรไฟล์ target
    target = "alx.trading"
    try:
        print(f"📋 Accessing profile: {target}")
        response = session.get(f"https://www.instagram.com/{target}/", timeout=10)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            content = response.text
            if "Sorry, this page isn't available" in content:
                print("❌ Profile not found")
            elif "This account is private" in content:
                print("🔒 Profile is private")
            else:
                print("✅ Profile accessible")
                return True
        elif response.status_code == 404:
            print("❌ Profile not found (404)")
        else:
            print(f"❌ Error accessing profile: {response.status_code}")

        return False

    except Exception as e:
        print(f"❌ Profile access error: {e}")
        return False

def check_existing_data():
    """ตรวจสอบข้อมูลที่มีอยู่ในระบบ"""
    print("\n📊 CHECKING EXISTING DATA")
    print("=" * 40)

    # ตรวจสอบข้อมูล DM ที่มี
    dm_file = "/workspaces/sugarglitch-realops/data/alx_trading/real_messages_extraction_1748948322.json"

    try:
        with open(dm_file, 'r') as f:
            data = json.load(f)

        messages = data.get('conversation_data', {}).get('messages', [])
        print(f"✅ Found existing DM data: {len(messages)} messages")

        # ตรวจสอบว่าเป็นข้อมูลจริงหรือ demo
        if len(messages) > 0:
            first_msg = messages[0]
            msg_text = first_msg.get('text', '')

            print(f"📄 Sample message: {msg_text[:50]}...")

            # ตรวจสอบ indicators ของ demo data
            demo_indicators = ['example.com', 'uuid', 'demo', 'test', 'sample']
            is_demo = any(indicator in str(data).lower() for indicator in demo_indicators)

            if is_demo:
                print("⚠️ Data appears to be DEMO/SIMULATION")
            else:
                print("✅ Data appears to be REAL")

            return True, len(messages), is_demo
        else:
            print("❌ No messages found in data")
            return False, 0, False

    except Exception as e:
        print(f"❌ Cannot read existing data: {e}")
        return False, 0, False

def main():
    """Main test function"""
    print("🎯 INSTAGRAM DM DATA STATUS CHECK")
    print("=" * 50)

    # Test 1: Instagram connection
    instagram_ok = test_instagram_connection()

    # Test 2: Target profile access
    profile_ok = test_target_profile()

    # Test 3: Check existing data
    data_exists, msg_count, is_demo = check_existing_data()

    # Summary
    print("\n📋 SUMMARY")
    print("=" * 20)
    print(f"Instagram Connection: {'✅' if instagram_ok else '❌'}")
    print(f"Target Profile Access: {'✅' if profile_ok else '❌'}")
    print(f"Existing DM Data: {'✅' if data_exists else '❌'}")

    if data_exists:
        print(f"Message Count: {msg_count}")
        print(f"Data Type: {'⚠️ DEMO/SIMULATION' if is_demo else '✅ APPEARS REAL'}")

    # Recommendation
    print("\n💡 RECOMMENDATION")
    print("=" * 20)

    if data_exists and not is_demo:
        print("✅ มีข้อมูล DM ที่ดูเหมือนจะเป็นข้อมูลจริง")
        print(f"   จำนวน messages: {msg_count}")
        print("   ควรตรวจสอบเนื้อหาเพิ่มเติม")
    elif data_exists and is_demo:
        print("⚠️ มีข้อมูล DM แต่เป็น DEMO/SIMULATION")
        print("   ต้องการ session ที่ valid เพื่อดึงข้อมูลจริง")
    elif instagram_ok and profile_ok:
        print("✅ สามารถเชื่อมต่อ Instagram ได้")
        print("   แต่ยังไม่มีข้อมูล DM จริง")
        print("   ควรลองรัน extractor tools")
    else:
        print("❌ ไม่สามารถเชื่อมต่อ Instagram ได้")
        print("   ต้องอัพเดท session หรือ login ใหม่")

if __name__ == "__main__":
    main()