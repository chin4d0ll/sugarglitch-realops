# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Ultra Simple DM Extractor - ไม่ยุ่งยาก
"""

import requests
import json
import time
from datetime import datetime

def read_real_session():
    """อ่าน session จริงๆ ที่ใช้งานได้"""
    session_file = "/workspaces/sugarglitch-realops/sessions/session-alx.trading"
    try:
        with open(session_file, 'r') as f:
            content = f.read().strip()

        # Parse JSON session data
        if content.startswith('{'):
            session_json = json.loads(content)
            if 'cookies' in session_json:
                return session_json['cookies']
            return session_json

        # Parse old format
        elif 'sessionid=' in content:
            lines = content.split('\n')
            session_data = {}
            for line in lines:
                if '=' in line:
                    key, value = line.split('=', 1)
                    session_data[key.strip()] = value.strip()
            return session_data
        return None
    except Exception as e:
        print(f"Error reading session: {e}")
        return None

def cute_request(url, cookies):
    """ง่ายๆ แค่ส่ง request"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }

    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        return response
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None

def main():
    print("🚀 Ultra Simple Instagram DM Extractor")
    print("=" * 50)

    # Read session
    session_data = read_real_session()
    if not session_data:
        print("❌ Cannot read session file")
        return

    print("✅ Session loaded")

    # Prepare cookies
    cookies = {}
    if 'sessionid' in session_data:
        cookies['sessionid'] = session_data['sessionid']
    if 'csrftoken' in session_data:
        cookies['csrftoken'] = session_data['csrftoken']

    # Test Instagram endpoint
    print("🔍 Testing Instagram connection...")

    url = "https://www.instagram.com/api/v1/direct_v2/inbox/"
    response = cute_request(url, cookies)

    if response:
        print(f"📡 Response status: {response.status_code}")

        if response.status_code == 200:
            print("🎉 SUCCESS! Got data from Instagram")
            try:
                data = response.json()
                print(f"📊 Found {len(data.get('inbox', {}).get('threads', []))} DM threads")

                # Save result
                timestamp = int(time.time())
                output_file = f"/workspaces/sugarglitch-realops/ultra_simple_extraction_{timestamp}.json"

                result = {
                    "timestamp": datetime.now().isoformat(),
                    "status": "success",
                    "threads_count": len(data.get('inbox', {}).get('threads', [])),
                    "data": data
                }

                with open(output_file, 'w') as f:
                    json.dump(result, f, indent=2)

                print(f"💾 Saved to: {output_file}")

            except Exception as e:
                print(f"❌ Error parsing response: {e}")

        elif response.status_code == 429:
            print("⏳ Rate limited - need to wait")

        else:
            print(f"❌ Error {response.status_code}")
            print(f"Response: {response.text[:200]}...")

    else:
        print("❌ No response from Instagram")

    print("\n✨ Done!")

if __name__ == "__main__":
    main()
