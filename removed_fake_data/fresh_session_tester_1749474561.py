# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Fresh Session Tester - ทดสอบ fresh hijacked sessions
"""

import json
import requests
import os
from datetime import datetime

def load_fresh_session(session_file):
    """โหลด fresh hijacked session"""
    try:
        with open(session_file, 'r') as f:
            session_data = json.load(f)

        # แปลง cookies เป็น dict
        cookies = {}
        for cookie in session_data.get('cookies', []):
            cookies[cookie['name']] = cookie['value']

        return cookies, session_data.get('session_info', {})

    except Exception as e:
        print(f"❌ ไม่สามารถโหลด session {session_file}: {e}")
        return None, None

def test_session(cookies, session_info):
    """ทดสอบ session ใหม่"""
    target = session_info.get('target_account', 'unknown')
    created = session_info.get('created_date', 'unknown')

    print(f"🎯 ทดสอบ session สำหรับ: {target}")
    print(f"📅 สร้างเมื่อ: {created}")
    print(f"🍪 มีคุกกี้: {len(cookies)} ตัว")

    # Headers สำหรับ Instagram
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": cookies.get('csrftoken', ''),
        "Referer": "https://www.instagram.com/direct/inbox/"
    }

    # สร้าง cookie string
    cookie_string = "; ".join([f"{name}={value}" for name, value in cookies.items()])
    headers["Cookie"] = cookie_string

    # URLs ทดสอบ
    test_urls = [
        {
            "name": "Current User Info",
            "url": "https://i.instagram.com/api/v1/accounts/current_user/",
            "success_key": "user"
        },
        {
            "name": "DM Inbox",
            "url": "https://i.instagram.com/api/v1/direct_v2/inbox/?visual_message_reply_chain_enabled=true&thread_message_limit=10&persistentBadging=true&limit=20",
            "success_key": "inbox"
        },
        {
            "name": "User Search",
            "url": f"https://i.instagram.com/api/v1/users/web_profile_info/?username={target}",
            "success_key": "data"
        }
    ]

    results = {}

    for test in test_urls:
        print(f"\n🌐 ทดสอบ: {test['name']}")

        try:
            response = requests.get(test['url'], headers=headers, timeout=15)
            print(f"📊 Status: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    if test['success_key'] in data:
                        print(f"✅ สำเร็จ! พบข้อมูล: {test['success_key']}")

                        # แสดงรายละเอียดเพิ่มเติม
                        if test['success_key'] == 'user':
                            username = data['user'].get('username', 'N/A')
                            full_name = data['user'].get('full_name', 'N/A')
                            print(f"   👤 Username: {username}")
                            print(f"   📝 Full Name: {full_name}")

                        elif test['success_key'] == 'inbox':
                            threads = data['inbox'].get('threads', [])
                            print(f"   💬 พบ {len(threads)} threads")
                            if threads:
                                print(f"   🎯 Thread แรก: {threads[0].get('thread_title', 'Untitled')}")

                        elif test['success_key'] == 'data':
                            user_data = data['data'].get('user', {})
                            username = user_data.get('username', 'N/A')
                            followers = user_data.get('edge_followed_by', {}).get('count', 0)
                            print(f"   👤 Target: {username}")
                            print(f"   👥 Followers: {followers:,}")

                        results[test['name']] = True
                    else:
                        print(f"⚠️ ไม่พบ key '{test['success_key']}' ใน response")
                        print(f"   Keys ที่มี: {list(data.keys())}")
                        results[test['name']] = False

                except json.JSONDecodeError:
                    print(f"⚠️ Response ไม่ใช่ JSON: {response.text[:100]}...")
                    results[test['name']] = False

            elif response.status_code == 400:
                try:
                    error_data = response.json()
                    error_code = error_data.get('error_code', 'N/A')
                    message = error_data.get('message', 'N/A')
                    print(f"❌ Error {error_code}: {message}")
                except Exception:
                    print(f"❌ Bad Request: {response.text[:100]}...")
                results[test['name']] = False

            elif response.status_code in [401, 403]:
                print("❌ ไม่มีสิทธิ์ - Session อาจหมดอายุ")
                results[test['name']] = False

            elif response.status_code == 429:
                print("❌ Rate limited - ถูกบล็อกชั่วคราว")
                results[test['name']] = False

            else:
                print(f"⚠️ Status {response.status_code}: {response.text[:50]}...")
                results[test['name']] = False

        except Exception as e:
            print(f"❌ เชื่อมต่อไม่ได้: {e}")
            results[test['name']] = False

    return results

def find_best_session():
    """หา session ที่ดีที่สุด"""
    hijacked_dir = "/workspaces/sugarglitch-realops/hijacked_sessions"

    # หาไฟล์ fresh_hijacked_session ทั้งหมด
    fresh_sessions = []

    for filename in os.listdir(hijacked_dir):
        if filename.startswith("fresh_hijacked_session_") and filename.endswith(".json"):
            fresh_sessions.append(os.path.join(hijacked_dir, filename))

    fresh_sessions.sort(reverse=True)  # เรียงจากใหม่สุด

    print(f"🔍 พบ {len(fresh_sessions)} fresh sessions")

    best_session = None
    best_score = 0

    for session_file in fresh_sessions[:5]:  # ทดสอบ 5 ไฟล์แรก
        print(f"\n{'='*60}")
        print(f"📁 ทดสอบ: {os.path.basename(session_file)}")

        cookies, session_info = load_fresh_session(session_file)
        if not cookies:
            continue

        results = test_session(cookies, session_info)
        score = sum(results.values())

        print(f"\n📊 คะแนน: {score}/3")

        if score > best_score:
            best_score = score
            best_session = session_file

        if score == 3:
            print("🎉 พบ session ที่สมบูรณ์แล้ว!")
            break

    return best_session, best_score

if __name__ == "__main__":
    print("🚀 เริ่มค้นหา Fresh Session ที่ใช้งานได้...")

    best_session, score = find_best_session()

    if best_session and score > 0:
        print(f"\n🏆 Session ที่ดีที่สุด: {os.path.basename(best_session)}")
        print(f"📊 คะแนน: {score}/3")

        # คัดลอกไปยัง session file หลัก
        target_file = "/workspaces/sugarglitch-realops/tools/session_alx_trading.json"

        # โหลดและแปลงรูปแบบ
        cookies, session_info = load_fresh_session(best_session)
        if cookies:
            # สร้างรูปแบบเดิม
            converted_session = {
                "sessionid": cookies.get("sessionid", ""),
                "csrftoken": cookies.get("csrftoken", ""),
                "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15",
                "cookies": cookies,
                "source": os.path.basename(best_session),
                "updated": datetime.now().isoformat()
            }

            with open(target_file, 'w', encoding='utf-8') as f:
                json.dump(converted_session, f, indent=2)

            print(f"✅ อัปเดต session ไฟล์หลักแล้ว: {target_file}")
            print("🎯 พร้อมใช้งาน! ลองรัน simple_dm_test.py อีกครั้ง")

    else:
        print("\n❌ ไม่พบ session ที่ใช้งานได้")
        print("💡 ต้องสร้าง session ใหม่ด้วย Playwright หรือวิธีอื่น")
