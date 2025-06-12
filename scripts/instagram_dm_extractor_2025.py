# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Instagram DM Extractor 2025 - เริ่มต้นใหม่หมด
สำหรับ alx.trading ด้วย sessionid สด ๆ
"""
import os
import json
import requests
import time
from datetime import datetime
from urllib.parse import unquote

class InstagramDMExtractor:
    def __init__(self):
        print("🎯 INSTAGRAM DM EXTRACTOR 2025")
        print("=" * 50)
        print("Target: alx.trading")
        print("Mode: REAL DATA EXTRACTION")
        print()

        self.target = "alx.trading"
        self.output_dir = "EXTRACTED_DMS"
        os.makedirs(self.output_dir, exist_ok = True)

        # สร้าง session requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q = 0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'X-IG-App-ID': '936619743392459',
            'X-ASBD-ID': '129477',
            'X-IG-WWW-Claim': '0',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        })

    def load_session(self):
        """โหลด sessionid จากไฟล์"""
        print("🔑 Loading session...")

        # เช็คไฟล์ session ที่มี
        session_files = [
            "alx_trading_session_fleming654.json",
            "real_session.json",
            "session.json"
        ]

        for file in session_files:
            if os.path.exists(file):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)

                    sessionid = data.get('sessionid', '')
                    if sessionid and len(sessionid) > 10:
                        # URL decode sessionid ถ้าจำเป็น
                        sessionid = unquote(sessionid)

                        print(f"✅ Found sessionid in {file}")
                        print(f"📋 Session: {sessionid[:20]}...")

                        # เพิ่ม cookie ให้ session
                        self.session.cookies.set('sessionid', sessionid, domain='.instagram.com')

                        return sessionid
                except Exception as e:
                    print(f"❌ Error reading {file}: {e}")

        print("❌ No valid session found!")
        return None

    def test_session(self):
        """ทดสอบ session ว่าใช้งานได้ไหม"""
        print("\n🔍 Testing session...")

        try:
            # ทดสอบเข้า Instagram หน้าหลัก
            response = self.session.get('https://www.instagram.com/', timeout = 15)

            if response.status_code == 200:
                if '"is_logged_in":true' in response.text:
                    print("✅ Session is VALID!")
                    return True
                else:
                    print("❌ Session expired or invalid")
                    return False
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False

    def get_user_id(self):
        """ดึง user_id ของ target"""
        print(f"\n🔍 Getting user ID for {self.target}...")

        try:
            # ไปที่หน้า profile ของ target
            url = f"https://www.instagram.com/{self.target}/"
            response = self.session.get(url, timeout = 15)

            if response.status_code == 200:
                # หา user ID จาก HTML
                import re
                pattern = r'"id":"(\d+)".*?"username":"' + self.target + '"'
                match = re.search(pattern, response.text)

                if match:
                    user_id = match.group(1)
                    print(f"✅ Found user ID: {user_id}")
                    return user_id
                else:
                    print("❌ Could not find user ID in page")
                    return None
            else:
                print(f"❌ Could not access profile: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Error getting user ID: {e}")
            return None

    def extract_dms(self, user_id = None):
        """ดึง DMs จริง ๆ"""
        print(f"\n🚀 Extracting DMs from {self.target}...")

        try:
            # ลองหลายวิธี
            methods = [
                self._extract_via_direct_api,
                self._extract_via_inbox,
                self._extract_via_thread_search
            ]

            for i, method in enumerate(methods, 1):
                print(f"\n📡 Method {i}: {method.__name__}")
                result = method(user_id)

                if result:
                    print(f"✅ Success with method {i}!")
                    return result
                else:
                    print(f"❌ Method {i} failed, trying next...")

            print("❌ All extraction methods failed")
            return None

        except Exception as e:
            print(f"❌ Extraction error: {e}")
            return None

    def _extract_via_direct_api(self, user_id):
        """วิธีที่ 1: ใช้ Direct Messages API"""
        try:
            url = "https://www.instagram.com/api/v1/direct_v2/inbox/"
            params = {
                'persistentBadging': 'true',
                'folder': '',
                'limit': '20'
            }

            response = self.session.get(url, params = params, timeout = 15)
            print(f"Response: HTTP {response.status_code}")

            if response.status_code == 200:
                data = response.json()

                if 'inbox' in data and 'threads' in data['inbox']:
                    threads = data['inbox']['threads']
                    print(f"📱 Found {len(threads)} conversation threads")

                    # หาการสนทนากับ target
                    for thread in threads:
                        users = thread.get('users', [])
                        usernames = [u.get('username', '') for u in users]

                        if self.target in usernames:
                            print(f"🎯 Found conversation with {self.target}!")

                            # ดึงข้อความจาก thread นี้
                            thread_id = thread.get('thread_id')
                            messages = self._get_thread_messages(thread_id)

                            return {
                                'method': 'direct_api',
                                'thread_id': thread_id,
                                'participants': usernames,
                                'messages': messages,
                                'total_messages': len(messages)
                            }

                    print(f"❌ No conversation found with {self.target}")
                    return None
                else:
                    print("❌ Invalid inbox response")
                    return None
            else:
                print(f"❌ API Error: {response.status_code}")
                print(response.text[:200])
                return None

        except Exception as e:
            print(f"❌ Direct API error: {e}")
            return None

    def _extract_via_inbox(self, user_id):
        """วิธีที่ 2: ผ่าน Web Inbox"""
        try:
            url = "https://www.instagram.com/direct/inbox/"
            response = self.session.get(url, timeout = 15)

            if response.status_code == 200:
                # หาข้อมูลใน HTML
                if self.target in response.text:
                    print(f"✅ Found {self.target} in inbox HTML")

                    # พยายามดึงข้อมูลจาก HTML
                    import re

                    # หา thread data
                    pattern = r'"thread_id":"([^"]+)"[^}]+users.*?"username":"' + self.target + '"'
                    match = re.search(pattern, response.text)

                    if match:
                        thread_id = match.group(1)
                        print(f"✅ Found thread ID: {thread_id}")

                        messages = self._get_thread_messages(thread_id)

                        return {
                            'method': 'web_inbox',
                            'thread_id': thread_id,
                            'messages': messages,
                            'total_messages': len(messages)
                        }

                print(f"❌ {self.target} not found in inbox")
                return None
            else:
                print(f"❌ Inbox access failed: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Inbox method error: {e}")
            return None

    def _extract_via_thread_search(self, user_id):
        """วิธีที่ 3: ค้นหา thread โดยตรง"""
        try:
            if not user_id:
                print("❌ Need user_id for thread search")
                return None

            # ลองสร้าง thread ID จาก user ID
            url = f"https://www.instagram.com/api/v1/direct_v2/threads/brodcast/"

            # หรือลองใช้ search API
            search_url = "https://www.instagram.com/api/v1/direct_v2/ranked_recipients/"
            params = {
                'mode': 'raven',
                'show_threads': 'true',
                'query': self.target
            }

            response = self.session.get(search_url, params = params, timeout = 15)

            if response.status_code == 200:
                data = response.json()
                print(f"✅ Search response received")

                # หา thread ที่มี target
                if 'ranked_recipients' in data:
                    for recipient in data['ranked_recipients']:
                        if recipient.get('user', {}).get('username') == self.target:
                            print(f"✅ Found {self.target} in search results")

                            return {
                                'method': 'thread_search',
                                'user_info': recipient,
                                'total_messages': 0  # ต้องดึงต่อ
                            }

                print(f"❌ {self.target} not found in search")
                return None
            else:
                print(f"❌ Search failed: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Thread search error: {e}")
            return None

    def _get_thread_messages(self, thread_id):
        """ดึงข้อความจาก thread ID"""
        try:
            url = f"https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/"
            params = {
                'limit': '50'
            }

            response = self.session.get(url, params = params, timeout = 15)

            if response.status_code == 200:
                data = response.json()

                if 'thread' in data and 'items' in data['thread']:
                    items = data['thread']['items']
                    print(f"💬 Found {len(items)} messages in thread")

                    messages = []
                    for item in items:
                        msg = {
                            'item_id': item.get('item_id'),
                            'timestamp': item.get('timestamp'),
                            'user_id': item.get('user_id'),
                            'item_type': item.get('item_type'),
                            'text': item.get('text', ''),
                            'created_at': datetime.fromtimestamp(item.get('timestamp', 0) / 1000000).isoformat() if item.get('timestamp') else None
                        }

                        # เพิ่มข้อมูลสื่อถ้ามี
                        if 'media' in item:
                            msg['media'] = item['media']

                        messages.append(msg)

                    return messages
                else:
                    print("❌ No messages in thread response")
                    return []
            else:
                print(f"❌ Thread access failed: {response.status_code}")
                return []

        except Exception as e:
            print(f"❌ Error getting thread messages: {e}")
            return []

    def save_results(self, data):
        """บันทึกผลลัพธ์"""
        if not data:
            print("❌ No data to save")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # บันทึกเป็น JSON
        json_file = f"{self.output_dir}/alx_trading_dms_{timestamp}.json"

        result = {
            'target': self.target,
            'extracted_at': datetime.now().isoformat(),
            'extraction_data': data,
            'summary': {
                'method_used': data.get('method'),
                'total_messages': data.get('total_messages', 0),
                'thread_id': data.get('thread_id'),
                'participants': data.get('participants', [])
            }
        }

        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent = 2, ensure_ascii = False)

            print(f"\n💾 Results saved to: {json_file}")
            print(f"📊 Total messages: {data.get('total_messages', 0)}")

            # สร้าง HTML report ด้วย
            self._create_html_report(result, timestamp)

        except Exception as e:
            print(f"❌ Error saving results: {e}")

    def _create_html_report(self, data, timestamp):
        """สร้าง HTML report"""
        try:
            html_file = f"{self.output_dir}/alx_trading_report_{timestamp}.html"

            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Instagram DM Report - {self.target}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #e1306c; color: white; padding: 20px; border-radius: 10px; }}
        .summary {{ background: #f8f9fa; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        .message {{ border: 1px solid #ddd; margin: 10px 0; padding: 10px; border-radius: 5px; }}
        .timestamp {{ color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📱 Instagram DM Report</h1>
        <h2>Target: {self.target}</h2>
        <p>Extracted: {data['extracted_at']}</p>
    </div>

    <div class="summary">
        <h3>📊 Summary</h3>
        <p><strong>Method:</strong> {data['summary']['method_used']}</p>
        <p><strong>Total Messages:</strong> {data['summary']['total_messages']}</p>
        <p><strong>Thread ID:</strong> {data['summary']['thread_id']}</p>
        <p><strong>Participants:</strong> {', '.join(data['summary']['participants']) if data['summary']['participants'] else 'N/A'}</p>
    </div>

    <div class="messages">
        <h3>💬 Messages</h3>
"""

            # เพิ่มข้อความ
            messages = data['extraction_data'].get('messages', [])
            for msg in messages[:20]:  # แสดง 20 ข้อความแรก
                text = msg.get('text', 'No text')
                timestamp = msg.get('created_at', 'Unknown time')

                html_content += f"""
        <div class="message">
            <div class="timestamp">{timestamp}</div>
            <div class="text">{text}</div>
        </div>
"""

            html_content += """
    </div>
</body>
</html>
"""

            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"📄 HTML report saved: {html_file}")

        except Exception as e:
            print(f"❌ Error creating HTML report: {e}")

    def run(self):
        """เริ่มต้นการทำงาน"""
        print("🚀 Starting extraction process...\n")

        # 1. โหลด session
        sessionid = self.load_session()
        if not sessionid:
            print("❌ Cannot proceed without valid session")
            return

        # 2. ทดสอบ session
        if not self.test_session():
            print("❌ Session is not working")
            return

        # 3. ดึง user ID ของ target
        user_id = self.get_user_id()

        # 4. ดึง DMs
        result = self.extract_dms(user_id)

        # 5. บันทึกผลลัพธ์
        if result:
            self.save_results(result)
            print("\n🎉 Extraction completed successfully!")
        else:
            print("\n❌ Extraction failed")

if __name__ == "__main__":
    extractor = InstagramDMExtractor()
    extractor.run()
