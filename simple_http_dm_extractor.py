# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🚀 SIMPLE HTTP-ONLY DM EXTRACTOR 2025
====================================

Direct Instagram API access without browser automation.
Uses pure HTTP requests for maximum speed and reliability.
"""

import requests
import json
import time
import random
from datetime import datetime
import os

class SimpleHttpDmExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.results = []

    def set_instagram_headers(self, sessionid):
        """Set proper Instagram headers"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-IG-App-ID': '936619743392459',
            'X-ASBD-ID': '198387',
            'X-IG-WWW-Claim': '0',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        })
        self.session.cookies.set('sessionid', sessionid)

    def extract_dms(self, target_username):
        """Extract DMs using multiple Instagram endpoints"""
        print(f"🚀 Starting DM extraction for {target_username}")

        # Try multiple endpoints
        endpoints = [
            f"https://i.instagram.com/api/v1/direct_v2/inbox/?visual_message_return_type=unseen&thread_message_limit=10&persistentBadging=true&limit=20",
            f"https://www.instagram.com/api/v1/direct_v2/inbox/",
            f"https://i.instagram.com/api/v1/direct_v2/threads/",
            f"https://www.instagram.com/direct/inbox/"
        ]

        for i, endpoint in enumerate(endpoints, 1):
            try:
                print(f"📡 Testing endpoint {i}/4: {endpoint[:50]}...")
                response = self.session.get(endpoint, timeout=10)
                print(f"   Status: {response.status_code}")

                if response.status_code == 200:
                    try:
                        data = response.json()
                        if 'inbox' in data or 'threads' in data:
                            self.results.append({
                                'endpoint': endpoint,
                                'status': 'success',
                                'data': data,
                                'timestamp': datetime.now().isoformat()
                            })
                            print(f"✅ Success! Found DM data at endpoint {i}")
                            return data
                    except Exception:
                        # Try HTML parsing
                        if 'window._sharedData' in response.text:
                            print(f"✅ Found HTML data at endpoint {i}")
                            self.extract_from_html(response.text, endpoint)

                else:
                    print(f"❌ Failed with status {response.status_code}")

            except Exception as e:
                print(f"❌ Error with endpoint {i}: {str(e)[:50]}...")

        return None

    def extract_from_html(self, html_content, endpoint):
        """Extract data from HTML response"""
        try:
            # Look for Instagram data in HTML
            markers = ['window._sharedData', 'window.__additionalDataLoaded', '"direct_v2"']

            for marker in markers:
                if marker in html_content:
                    print(f"📄 Found {marker} in HTML")
                    # Save HTML for analysis
                    filename = f"results/html_dump_{int(time.time())}.html"
                    os.makedirs('results', exist_ok=True)
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    print(f"💾 Saved HTML to {filename}")

                    self.results.append({
                        'endpoint': endpoint,
                        'status': 'html_found',
                        'marker': marker,
                        'file': filename,
                        'timestamp': datetime.now().isoformat()
                    })
                    return True

        except Exception as e:
            print(f"❌ HTML parsing error: {e}")

        return False

    def test_session_validity(self):
        """Test if session is valid"""
        try:
            response = self.session.get('https://www.instagram.com/accounts/edit/', timeout=10)
            if response.status_code == 200 and 'Edit Profile' in response.text:
                print("✅ Session is valid!")
                return True
            else:
                print(f"❌ Session invalid - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Session test failed: {e}")
            return False

    def save_results(self):
        """Save extraction results"""
        os.makedirs('results', exist_ok=True)
        filename = f"results/dm_extraction_{int(time.time())}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'extraction_time': datetime.now().isoformat(),
                'total_attempts': len(self.results),
                'successful_extractions': len([r for r in self.results if r['status'] == 'success']),
                'results': self.results
            }, f, indent=2, ensure_ascii=False)

        print(f"💾 Results saved to {filename}")
        return filename

def main():
    print("🚀 SIMPLE HTTP-ONLY DM EXTRACTOR 2025")
    print("=" * 50)

    extractor = SimpleHttpDmExtractor()

    # Try to find a valid session
    session_files = [
        'tools/session_alx_trading.json',
        'session.json',
        'demo_session.json',
        'fresh_sessions/working_session_1749202525.json'
    ]

    sessionid = None
    for session_file in session_files:
        if os.path.exists(session_file):
            try:
                with open(session_file, 'r') as f:
                    data = json.load(f)
                    if 'sessionid' in data and len(data['sessionid']) > 10:
                        sessionid = data['sessionid']
                        print(f"✅ Using session from {session_file}")
                        break
            except Exception as e:
                print(f"❌ Failed to load {session_file}: {e}")
                continue

    if not sessionid:
        print("❌ No valid session found!")
        print("\n💡 To get a session:")
        print("1. Login to Instagram in browser")
        print("2. Press F12 → Application → Cookies")
        print("3. Copy sessionid value")
        print("4. Create session.json: {'sessionid': 'your_session_here'}")
        return

    # Set headers and test session
    extractor.set_instagram_headers(sessionid)

    if not extractor.test_session_validity():
        print("❌ Session is not valid, trying anyway...")

    # Extract DMs
    results = extractor.extract_dms('alx.trading')

    # Save results
    filename = extractor.save_results()

    print("\n📊 EXTRACTION SUMMARY:")
    print(f"   Total attempts: {len(extractor.results)}")
    print(f"   Successful: {len([r for r in extractor.results if r['status'] == 'success'])}")
    print(f"   HTML found: {len([r for r in extractor.results if r['status'] == 'html_found'])}")
    print(f"   Results file: {filename}")

    if results:
        print("🎉 DM data extracted successfully!")
    else:
        print("⚠️ No direct DM data found, check HTML dumps for manual analysis")

if __name__ == "__main__":
    main()
