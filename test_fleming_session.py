# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔍 Session Tester - ทดสอบ session จากไฟล์ fleming654
"""
import json
import requests
import urllib.parse
from datetime import datetime

def test_fleming_session():
    print("🧪 TESTING FLEMING654 SESSION")
    print("=" * 40)

    # โหลด session
    try:
        with open('alx_trading_session_fleming654.json', 'r') as f:
            session_data = json.load(f)

        sessionid = session_data.get('sessionid', '')
        print(f"📋 Original Session: {sessionid}")

        # URL decode sessionid
        decoded_sessionid = urllib.parse.unquote(sessionid)
        print(f"🔓 Decoded Session: {decoded_sessionid}")

    except Exception as e:
        print(f"❌ Error loading session: {e}")
        return

    # ทดสอบ session
    session = requests.Session()

    # เพิ่ม cookies
    cookies = {
        'sessionid': decoded_sessionid,
        'csrftoken': 'test',
        'mid': f'Y{int(datetime.now().timestamp())}-0'
    }

    for name, value in cookies.items():
        session.cookies.set(name, value, domain='.instagram.com')

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.instagram.com/',
    }

    session.headers.update(headers)

    print("\n🌐 Testing Instagram homepage...")
    try:
        response = session.get('https://www.instagram.com/', timeout=15)
        print(f"📊 Status: {response.status_code}")

        if response.status_code == 200:
            content = response.text
            print(f"📄 Content length: {len(content)}")

            # เช็คการ login
            if 'login' in content.lower() and 'password' in content.lower():
                print("❌ Not logged in - session invalid")
            elif '"viewer"' in content:
                print("✅ Session seems valid - found viewer data")

                # ลองดึงข้อมูล DM
                print("\n💬 Testing DM access...")
                dm_response = session.get('https://www.instagram.com/direct/inbox/', timeout=15)
                print(f"📊 DM Status: {dm_response.status_code}")

                if dm_response.status_code == 200:
                    dm_content = dm_response.text
                    print(f"📄 DM Content length: {len(dm_content)}")

                    # บันทึก HTML
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    html_file = f'results/fleming_dm_test_{timestamp}.html'

                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(dm_content)

                    print(f"💾 DM HTML saved: {html_file}")

                    # วิเคราะห์เนื้อหา
                    if 'direct' in dm_content.lower():
                        print("🎯 Found 'direct' in DM page")
                    if 'inbox' in dm_content.lower():
                        print("🎯 Found 'inbox' in DM page")
                    if 'thread' in dm_content.lower():
                        print("🎯 Found 'thread' in DM page")
                    if 'alx.trading' in dm_content.lower():
                        print("🎯 Found 'alx.trading' in DM page")

                    return True
                else:
                    print(f"❌ DM access failed: {dm_response.status_code}")
            else:
                print("⚠️ Unknown login status")
        else:
            print(f"❌ Homepage access failed: {response.status_code}")

    except Exception as e:
        print(f"❌ Error testing session: {e}")

    return False

if __name__ == "__main__":
    test_fleming_session()
