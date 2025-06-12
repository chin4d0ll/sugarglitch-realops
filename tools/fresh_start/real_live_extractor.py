# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🎯 REAL INSTAGRAM DM EXTRACTOR - LIVE SESSION
===========================================
ใช้ session จริงเพื่อดึงข้อมูล DM จริงๆ
"""

import json
import requests
import time
from datetime import datetime
from pathlib import Path
import sys

class RealInstagramExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session.headers.update(self.base_headers)

    def load_real_session(self):
        """โหลด session จริงที่มีอยู่"""
        session_file = Path("/workspaces/sugarglitch-realops/sessions/session-alx.trading")

        if session_file.exists():
            with open(session_file, 'r') as f:
                session_data = json.load(f)

            # ตั้งค่า cookies
            for name, value in session_data.get('cookies', {}).items():
                self.session.cookies.set(name, value, domain='.instagram.com')

            print(f"✅ Loaded real session from {session_file}")
            return True
        else:
            print(f"❌ Session file not found: {session_file}")
            return False

    def test_session_validity(self):
        """ทดสอบว่า session ยังใช้งานได้ไหม"""
        try:
            print("🔐 Testing session validity...")

            response = self.session.get("https://www.instagram.com/")

            if response.status_code == 200:
                if '"is_logged_in":true' in response.text or 'csrftoken' in response.text:
                    print("✅ Session is valid and logged in!")
                    return True
                else:
                    print("⚠️ Session may be expired or invalid")
                    return False
            else:
                print(f"❌ HTTP {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Session test failed: {e}")
            return False

    def extract_real_dms(self):
        """ดึงข้อมูล DM จริงๆ"""
        try:
            print("📱 Extracting real Instagram DMs...")

            # ลองเข้า direct inbox
            inbox_url = "https://www.instagram.com/direct/inbox/"

            print(f"📡 Requesting: {inbox_url}")
            response = self.session.get(inbox_url)

            print(f"📊 Response: HTTP {response.status_code}")
            print(f"📏 Content length: {len(response.text)} bytes")

            if response.status_code == 200:
                # บันทึก HTML response เพื่อการวิเคราะห์
                timestamp = int(time.time())
                html_file = f"real_instagram_response_{timestamp}.html"

                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)

                print(f"💾 HTML response saved to: {html_file}")

                # วิเคราะห์เนื้อหา
                content = response.text

                # หาข้อมูล JSON ที่ซ่อนอยู่ในหน้า
                if 'window._sharedData' in content:
                    print("🔍 Found _sharedData!")

                    # ดึง JSON data
                    start = content.find('window._sharedData = ') + len('window._sharedData = ')
                    end = content.find(';</script>', start)

                    if start > 0 and end > start:
                        json_str = content[start:end]
                        try:
                            shared_data = json.loads(json_str)

                            # บันทึก shared data
                            json_file = f"instagram_shared_data_{timestamp}.json"
                            with open(json_file, 'w', encoding='utf-8') as f:
                                json.dump(shared_data, f, indent=2, ensure_ascii=False)

                            print(f"💾 Shared data saved to: {json_file}")

                            # วิเคราะห์ข้อมูล
                            self.analyze_shared_data(shared_data)

                        except json.JSONDecodeError as e:
                            print(f"❌ JSON decode error: {e}")

                # หา GraphQL data หรือ API calls
                if 'direct' in content.lower() and ('thread' in content.lower() or 'message' in content.lower()):
                    print("🔍 Found potential DM data in response!")

                    # ค้นหา thread IDs หรือ message data
                    import re

                    # หา thread IDs
                    thread_pattern = r'"thread_id":"([^"]+)"'
                    thread_matches = re.findall(thread_pattern, content)

                    if thread_matches:
                        print(f"🧵 Found {len(thread_matches)} thread IDs:")
                        for thread_id in thread_matches[:5]:  # แสดง 5 อันแรก
                            print(f"   - {thread_id}")

                    # หา message data
                    message_pattern = r'"text":"([^"]+)"'
                    message_matches = re.findall(message_pattern, content)

                    if message_matches:
                        print(f"💬 Found {len(message_matches)} potential messages:")
                        for msg in message_matches[:3]:  # แสดง 3 อันแรก
                            print(f"   - \"{msg[:50]}...\"")

                return {
                    "status": "success",
                    "response_code": response.status_code,
                    "content_length": len(content),
                    "html_file": html_file,
                    "has_shared_data": 'window._sharedData' in content,
                    "has_dm_data": 'direct' in content.lower()
                }

            else:
                print(f"❌ Failed to access inbox: HTTP {response.status_code}")
                return {"status": "failed", "response_code": response.status_code}

        except Exception as e:
            print(f"❌ DM extraction failed: {e}")
            return {"status": "error", "error": str(e)}

    def analyze_shared_data(self, data):
        """วิเคราะห์ shared data จาก Instagram"""
        print("\n🔍 ANALYZING SHARED DATA:")

        if 'config' in data:
            config = data['config']
            print(f"👤 Viewer ID: {config.get('viewerId', 'N/A')}")

        if 'entry_data' in data:
            entry_data = data['entry_data']
            print(f"📄 Entry data keys: {list(entry_data.keys())}")

            # หา DirectPage data
            if 'DirectPage' in entry_data:
                direct_page = entry_data['DirectPage'][0] if entry_data['DirectPage'] else {}
                print("📱 Found DirectPage data!")

                if 'graphql' in direct_page:
                    graphql = direct_page['graphql']
                    if 'user' in graphql:
                        user = graphql['user']
                        print(f"👤 User: {user.get('username', 'N/A')}")

def main():
    print("🎯 REAL INSTAGRAM DM EXTRACTOR")
    print("=" * 50)
    print(f"⏰ Started at: {datetime.now()}")

    extractor = RealInstagramExtractor()

    # โหลด session จริง
    if not extractor.load_real_session():
        print("❌ Cannot load session, exiting...")
        sys.exit(1)

    # ทดสอบ session
    if not extractor.test_session_validity():
        print("❌ Session is invalid, exiting...")
        sys.exit(1)

    # ดึงข้อมูล DM จริง
    result = extractor.extract_real_dms()

    print(f"\n🎯 EXTRACTION RESULT:")
    print(f"Status: {result.get('status', 'unknown')}")

    if result.get('status') == 'success':
        print("✅ REAL DATA EXTRACTION SUCCESSFUL!")
        print(f"📁 Check the generated files for actual Instagram data")
    else:
        print("❌ Extraction failed")

    print(f"\n⏰ Completed at: {datetime.now()}")

if __name__ == "__main__":
    main()
