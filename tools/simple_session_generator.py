# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔑 Instagram Session Generator - Simple Manual Input
เครื่องมือง่ายๆ สำหรับรับ session จาก user และทดสอบ
"""

import json
import requests
from datetime import datetime
import os

def input_session_manually():
    """รับ session จาก user ด้วยมือ"""
    print("🔑 Instagram Session Input")
    print("=" * 50)
    print("📱 วิธีการ:")
    print("1. เปิด Instagram ในเบราว์เซอร์ (Chrome/Firefox)")
    print("2. ล็อกอินเข้าบัญชีที่ต้องการ")
    print("3. กด F12 เพื่อเปิด Developer Tools")
    print("4. ไปแท็บ Application (Chrome) หรือ Storage (Firefox)")
    print("5. ไปที่ Cookies > https://www.instagram.com")
    print("6. หา sessionid และ csrftoken")
    print("7. คัดลอกค่ามาใส่ที่นี่")
    print("=" * 50)

    # รับ sessionid
    while True:
        sessionid = input("\n📋 กรุณาใส่ sessionid: ").strip()
        if sessionid and len(sessionid) > 20:
            break
        print("❌ sessionid ต้องยาวกว่า 20 ตัวอักษร")

    # รับ csrftoken (ไม่บังคับ)
    csrftoken = input("📋 กรุณาใส่ csrftoken (หรือกด Enter เพื่อข้าม): ").strip()
    if not csrftoken:
        csrftoken = "missing"

    return sessionid, csrftoken

def test_session_api(sessionid, csrftoken):
    """ทดสอบ session กับ Instagram API"""
    print("\n🧪 กำลังทดสอบ session...")

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrftoken,
        "Cookie": f"sessionid={sessionid}; csrftoken={csrftoken};"
    }

    # Test URLs
    tests = [
        {
            "name": "📱 Current User",
            "url": "https://i.instagram.com/api/v1/accounts/current_user/",
            "required_key": "user"
        },
        {
            "name": "💬 DM Inbox",
            "url": "https://i.instagram.com/api/v1/direct_v2/inbox/?limit=5",
            "required_key": "inbox"
        }
    ]

    success_count = 0
    user_info = {}

    for test in tests:
        print(f"\n{test['name']} Testing...")

        try:
            response = requests.get(test['url'], headers=headers, timeout=15)
            status = response.status_code

            print(f"   📊 Status Code: {status}")

            if status == 200:
                try:
                    data = response.json()

                    if test['required_key'] in data:
                        print(f"   ✅ SUCCESS - Valid response!")
                        success_count += 1

                        # Extract user info
                        if test['required_key'] == 'user':
                            user = data['user']
                            user_info = {
                                'username': user.get('username', 'Unknown'),
                                'full_name': user.get('full_name', 'Unknown'),
                                'user_id': str(user.get('pk', 'Unknown')),
                                'is_private': user.get('is_private', False)
                            }
                            print(f"   👤 Username: {user_info['username']}")
                            print(f"   📝 Full Name: {user_info['full_name']}")
                            print(f"   🔒 Private: {user_info['is_private']}")

                        elif test['required_key'] == 'inbox':
                            inbox = data['inbox']
                            threads = inbox.get('threads', [])
                            print(f"   💬 Message Threads: {len(threads)}")
                            if threads:
                                print(f"   📩 Recent Messages Found!")
                    else:
                        print(f"   ⚠️ Response missing '{test['required_key']}' key")
                        print(f"   Available keys: {list(data.keys())}")

                except json.JSONDecodeError:
                    print(f"   ❌ Invalid JSON response")

            elif status in [400, 401, 403]:
                print(f"   ❌ UNAUTHORIZED - Session invalid or expired")

            elif status == 429:
                print(f"   ❌ RATE LIMITED - Too many requests")

            elif status == 404:
                print(f"   ❌ NOT FOUND - Endpoint may be incorrect")

            else:
                print(f"   ⚠️ Unexpected status: {status}")

        except requests.RequestException as e:
            print(f"   ❌ Request failed: {str(e)[:50]}...")
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:50]}...")

    print(f"\n📊 Overall Results: {success_count}/2 tests passed")

    if success_count >= 1:
        print("✅ Session is WORKING!")
    else:
        print("❌ Session is NOT WORKING")

    return success_count >= 1, user_info

def save_working_session(sessionid, csrftoken, user_info):
    """บันทึก session ที่ใช้งานได้"""
    session_data = {
        "sessionid": sessionid,
        "csrftoken": csrftoken,
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "cookies": {
            "sessionid": sessionid,
            "csrftoken": csrftoken
        },
        "user_info": user_info,
        "created_at": datetime.now().isoformat(),
        "method": "manual_input_simple",
        "status": "verified_working"
    }

    # Main session file
    output_file = "/workspaces/sugarglitch-realops/tools/session_alx_trading.json"

    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Save main file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)

        # Create backup
        timestamp = int(datetime.now().timestamp())
        backup_file = f"/workspaces/sugarglitch-realops/tools/session_backup_{timestamp}.json"

        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Session files saved:")
        print(f"   Main: {output_file}")
        print(f"   Backup: {backup_file}")

        return True

    except Exception as e:
        print(f"\n❌ Failed to save session: {e}")
        return False

def main():
    print("🚀 Instagram Session Generator")
    print("💡 This tool will help you create a working Instagram session")

    # Get session from user
    sessionid, csrftoken = input_session_manually()

    # Test the session
    is_working, user_info = test_session_api(sessionid, csrftoken)

    if is_working:
        print("\n🎉 Great! The session is working!")

        # Save the session
        if save_working_session(sessionid, csrftoken, user_info):
            print("\n✅ Session saved successfully!")
            print("\n🎯 Next Steps:")
            print("1. Run: python3 tools/simple_dm_test.py")
            print("2. If successful, you'll see '✅ Request succeeded!'")
            print("3. Then you can run any DM extractor script")
            print("\n🔧 Available extractors:")
            print("   - python3 real_dm_extractor_fresh.py")
            print("   - python3 enhanced_dm_extractor.py")
            print("   - python3 final_dm_extractor.py")
        else:
            print("\n❌ Failed to save session")
    else:
        print("\n❌ Session is not working!")
        print("\n💡 Troubleshooting:")
        print("1. Make sure you're logged into Instagram in your browser")
        print("2. Check that sessionid and csrftoken are copied correctly")
        print("3. Try refreshing Instagram page and getting new cookies")
        print("4. Make sure the Instagram account is not restricted")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
