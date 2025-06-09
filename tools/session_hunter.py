# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔍 Session Hunter - หา session ที่ใช้งานได้จากไฟล์ในโปรเจค
"""

import json
import os
import requests
import urllib.parse
from datetime import datetime
import glob
from pathlib import Path

class SessionHunter:
    def __init__(self):
        self.project_root = "/workspaces/sugarglitch-realops"
        self.working_sessions = []

    def extract_sessionid_from_text(self, text):
        """ดึง sessionid จากข้อความต่างๆ"""
        sessionids = []

        # Pattern 1: JSON format {"sessionid": "..."}
        import re
        patterns = [
            r'"sessionid":\s*"([^"]+)"',
            r"'sessionid':\s*'([^']+)'",
            r"sessionid=([^;\s&]+)",
            r"sessionid:\s*([^,\s}]+)",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text)
            sessionids.extend(matches)

        # URL decode if needed
        decoded_sessions = []
        for sid in sessionids:
            try:
                decoded = urllib.parse.unquote(sid)
                decoded_sessions.append(decoded)
            except Exception:
                decoded_sessions.append(sid)

        return list(set(decoded_sessions))  # Remove duplicates

    def find_all_session_files(self):
        """หาไฟล์ทั้งหมดที่อาจมี session"""
        session_files = []

        # Search patterns
        patterns = [
            "**/session*.json",
            "**/hijacked*.json",
            "**/spoofed*.json",
            "**/rotated*.json",
            "**/fresh*.json",
            "**/session*",
            "**/*session*",
            "**/tools/session*",
            "**/sessions/*",
            "**/hijacked_sessions/*"
        ]

        for pattern in patterns:
            files = glob.glob(f"{self.project_root}/{pattern}", recursive=True)
            session_files.extend(files)

        # Remove duplicates and sort
        session_files = list(set(session_files))
        session_files.sort()

        return session_files

    def extract_sessions_from_file(self, file_path):
        """ดึง session จากไฟล์"""
        sessions = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Try to parse as JSON first
            try:
                data = json.loads(content)
                sessions.extend(self.extract_sessions_from_json(data))
            except json.JSONDecodeError:
                # If not JSON, search for patterns in text
                sessionids = self.extract_sessionid_from_text(content)
                for sid in sessionids:
                    sessions.append({
                        'sessionid': sid,
                        'source': file_path,
                        'method': 'text_extraction'
                    })

        except Exception as e:
            print(f"⚠️ ไม่สามารถอ่าน {file_path}: {e}")

        return sessions

    def extract_sessions_from_json(self, data, source_path=""):
        """ดึง session จาก JSON data"""
        sessions = []

        def search_recursive(obj, path=""):
            if isinstance(obj, dict):
                # Direct sessionid
                if 'sessionid' in obj:
                    session_data = {
                        'sessionid': obj['sessionid'],
                        'source': source_path,
                        'method': 'json_direct',
                        'path': path
                    }

                    # Add additional fields if available
                    if 'csrftoken' in obj:
                        session_data['csrftoken'] = obj['csrftoken']
                    if 'user_agent' in obj:
                        session_data['user_agent'] = obj['user_agent']
                    if 'cookies' in obj and isinstance(obj['cookies'], dict):
                        session_data['all_cookies'] = obj['cookies']

                    sessions.append(session_data)

                # Cookies object
                if 'cookies' in obj and isinstance(obj['cookies'], dict):
                    cookies = obj['cookies']
                    if 'sessionid' in cookies:
                        sessions.append({
                            'sessionid': cookies['sessionid'],
                            'source': source_path,
                            'method': 'json_cookies',
                            'path': path + '.cookies',
                            'all_cookies': cookies
                        })

                # Cookie array (Playwright format)
                if 'cookies' in obj and isinstance(obj['cookies'], list):
                    for cookie in obj['cookies']:
                        if isinstance(cookie, dict) and cookie.get('name') == 'sessionid':
                            sessions.append({
                                'sessionid': cookie['value'],
                                'source': source_path,
                                'method': 'json_cookie_array',
                                'path': path + '.cookies[]'
                            })

                # Recurse into nested objects
                for key, value in obj.items():
                    search_recursive(value, f"{path}.{key}" if path else key)

            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    search_recursive(item, f"{path}[{i}]")

        search_recursive(data)
        return sessions

    def test_session(self, session_data):
        """ทดสอบ session"""
        sessionid = session_data['sessionid']
        csrftoken = session_data.get('csrftoken', 'missing')

        headers = {
            "User-Agent": session_data.get('user_agent', "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15"),
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrftoken,
            "Cookie": f"sessionid={sessionid}; csrftoken={csrftoken};"
        }

        test_urls = [
            {
                "name": "Current User",
                "url": "https://i.instagram.com/api/v1/accounts/current_user/",
                "key": "user"
            },
            {
                "name": "DM Inbox",
                "url": "https://i.instagram.com/api/v1/direct_v2/inbox/?limit=5",
                "key": "inbox"
            }
        ]

        results = {}
        total_score = 0

        for test in test_urls:
            try:
                response = requests.get(test['url'], headers=headers, timeout=10)

                if response.status_code == 200:
                    try:
                        data = response.json()
                        if test['key'] in data:
                            results[test['name']] = "✅ SUCCESS"
                            total_score += 1

                            # Get additional info
                            if test['key'] == 'user':
                                username = data['user'].get('username', 'N/A')
                                results[f"{test['name']}_info"] = f"User: {username}"
                            elif test['key'] == 'inbox':
                                threads = data['inbox'].get('threads', [])
                                results[f"{test['name']}_info"] = f"Threads: {len(threads)}"
                        else:
                            results[test['name']] = f"⚠️ No {test['key']} key"
                    except Exception:
                        results[test['name']] = "⚠️ Invalid JSON"
                elif response.status_code in [400, 401, 403]:
                    results[test['name']] = "❌ Unauthorized"
                elif response.status_code == 429:
                    results[test['name']] = "❌ Rate Limited"
                else:
                    results[test['name']] = f"❌ HTTP {response.status_code}"

            except Exception as e:
                results[test['name']] = f"❌ Error: {str(e)[:30]}"

        return total_score, results

    def hunt_sessions(self):
        """หา session ทั้งหมดในโปรเจค"""
        print("🔍 Session Hunter - กำลังค้นหา session ในโปรเจค...")
        print("=" * 60)

        # Find all potential session files
        session_files = self.find_all_session_files()
        print(f"📁 พบไฟล์ที่น่าสนใจ: {len(session_files)} ไฟล์")

        all_sessions = []

        # Extract sessions from each file
        for file_path in session_files:
            print(f"\n📄 กำลังตรวจสอบ: {os.path.relpath(file_path, self.project_root)}")
            sessions = self.extract_sessions_from_file(file_path)

            if sessions:
                print(f"   ✅ พบ {len(sessions)} session(s)")
                all_sessions.extend(sessions)
            else:
                print(f"   ⚠️ ไม่พบ session")

        print(f"\n📊 รวมพบ session ทั้งหมด: {len(all_sessions)} ตัว")

        if not all_sessions:
            print("❌ ไม่พบ session ใดๆ ในโปรเจค")
            return []

        # Remove duplicate sessionids
        unique_sessions = {}
        for session in all_sessions:
            try:
                sid = session['sessionid']
                if isinstance(sid, str) and len(sid) > 10 and sid not in unique_sessions:
                    unique_sessions[sid] = session
            except (KeyError, TypeError) as e:
                print(f"   ⚠️ ข้อมูล session ไม่ถูกต้อง: {e}")
                continue

        print(f"🔄 Session ที่ไม่ซ้ำกัน: {len(unique_sessions)} ตัว")

        # Test each unique session
        print(f"\n🧪 กำลังทดสอบ session...")
        print("=" * 60)

        working_sessions = []

        for i, (sessionid, session_data) in enumerate(unique_sessions.items(), 1):
            print(f"\n[{i}/{len(unique_sessions)}] ทดสอบ: {sessionid[:20]}...")
            print(f"   📁 Source: {os.path.basename(session_data['source'])}")
            print(f"   🔧 Method: {session_data['method']}")

            score, results = self.test_session(session_data)

            for test_name, result in results.items():
                if not test_name.endswith('_info'):
                    print(f"   {result} {test_name}")
                else:
                    print(f"      ℹ️ {result}")

            print(f"   📊 Score: {score}/2")

            if score > 0:
                session_data['test_score'] = score
                session_data['test_results'] = results
                working_sessions.append(session_data)

        # Sort by score (best first)
        working_sessions.sort(key=lambda x: x['test_score'], reverse=True)

        return working_sessions

    def save_best_session(self, working_sessions):
        """บันทึก session ที่ดีที่สุด"""
        if not working_sessions:
            print("\n❌ ไม่มี session ที่ใช้งานได้")
            return False

        best_session = working_sessions[0]

        # Create session file format
        session_file_data = {
            "sessionid": best_session['sessionid'],
            "csrftoken": best_session.get('csrftoken', 'extracted'),
            "user_agent": best_session.get('user_agent', "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15"),
            "cookies": best_session.get('all_cookies', {
                "sessionid": best_session['sessionid'],
                "csrftoken": best_session.get('csrftoken', 'extracted')
            }),
            "source_info": {
                "extracted_from": best_session['source'],
                "method": best_session['method'],
                "test_score": best_session['test_score'],
                "extracted_at": datetime.now().isoformat()
            }
        }

        # Save to main session file
        output_file = "/workspaces/sugarglitch-realops/tools/session_alx_trading.json"

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(session_file_data, f, indent=2, ensure_ascii=False)

            print(f"\n✅ บันทึก session ที่ดีที่สุดแล้ว: {output_file}")
            print(f"📊 คะแนนทดสอบ: {best_session['test_score']}/2")
            print(f"📁 ต้นฉบับ: {os.path.basename(best_session['source'])}")

            return True

        except Exception as e:
            print(f"\n❌ ไม่สามารถบันทึกไฟล์: {e}")
            return False

def main():
    hunter = SessionHunter()

    # Hunt for sessions
    working_sessions = hunter.hunt_sessions()

    if working_sessions:
        print(f"\n🎉 พบ session ที่ใช้งานได้: {len(working_sessions)} ตัว")

        print(f"\n📋 รายการ session ที่ใช้งานได้:")
        for i, session in enumerate(working_sessions, 1):
            print(f"{i}. {session['sessionid'][:30]}... (Score: {session['test_score']}/2)")
            print(f"   Source: {os.path.basename(session['source'])}")

        # Save best session
        if hunter.save_best_session(working_sessions):
            print(f"\n🎯 ขั้นตอนต่อไป:")
            print(f"1. รัน: python3 tools/simple_dm_test.py")
            print(f"2. ถ้าสำเร็จ จะแสดง '✅ Request succeeded!'")
            print(f"3. จากนั้นสามารถรัน DM extractor ได้")

    else:
        print(f"\n❌ ไม่พบ session ที่ใช้งานได้เลย")
        print(f"💡 ต้องสร้าง session ใหม่ด้วย:")
        print(f"   python3 tools/manual_session_input.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 ยกเลิกโดยผู้ใช้")
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {e}")
        import traceback
        traceback.print_exc()
