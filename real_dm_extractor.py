# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Real DM Extractor - ใช้วิธีการแบบ real browser
"""
import requests
import json
import os
from datetime import datetime

def get_real_browser_headers(sessionid):
    """สร้าง headers แบบ real browser"""
    return {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Cookie': f'sessionid={sessionid}; ig_did=94BD1C3E-8B5D-4C91-9F61-25C4E6A0A4EC; ig_nrcb=1; csrftoken=abc123',
        'Pragma': 'no-cache',
        'Referer': 'https://www.instagram.com/direct/',
        'Sec-Ch-Ua': '"Google Chrome";v="120", "Chromium";v="120", "Not:A-Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Asbd-Id': '129477',
        'X-Csrftoken': 'abc123',
        'X-Ig-App-Id': '936619743392459',
        'X-Ig-Www-Claim': '0',
        'X-Instagram-Ajax': '1010624542',
        'X-Requested-With': 'XMLHttpRequest'
    }

def extract_dms_real():
    print("🔥 REAL DM EXTRACTOR")
    print("="*50)

    # โหลด session
    try:
        with open('tools/session_alx_trading.json', 'r') as f:
            session = json.load(f)
        sessionid = session.get('sessionid', '')
        print(f"✅ Session: {sessionid[:15]}...")
    except Exception:
        print("❌ No session file")
        return

    # สร้าง real browser headers
    headers = get_real_browser_headers(sessionid)

    # ทดสอบหลาย endpoints
    endpoints = [
        ('Web DM Page', 'https://www.instagram.com/direct/inbox/'),
        ('GraphQL DM', 'https://www.instagram.com/graphql/query/'),
        ('Mobile API', 'https://i.instagram.com/api/v1/direct_v2/inbox/'),
    ]

    for name, url in endpoints:
        print(f"\n🎯 Testing {name}...")

        try:
            if 'graphql' in url:
                # GraphQL query สำหรับ DM
                data = {
                    'query_hash': 'e9ba915e9d1f23398a05b60b6e1d7fb5',
                    'variables': json.dumps({})
                }
                response = requests.post(url, headers=headers, data=data, timeout=10)
            else:
                response = requests.get(url, headers=headers, timeout=10)

            print(f"📡 Status: {response.status_code}")

            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')

                if 'application/json' in content_type:
                    try:
                        data = response.json()
                        if 'inbox' in data:
                            threads = data['inbox'].get('threads', [])
                            print(f"🎉 SUCCESS! Found {len(threads)} DM threads")

                            # บันทึกผลลัพธ์
                            output_file = f'results/real_dm_extraction_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                            os.makedirs('results', exist_ok=True)

                            with open(output_file, 'w') as f:
                                json.dump(data, f, indent=2)

                            print(f"💾 Saved to: {output_file}")
                            return True
                        else:
                            print(f"📊 JSON response (no inbox): {str(data)[:100]}...")
                    except Exception:
                        print(f"📄 JSON parse error: {response.text[:100]}...")
                else:
                    # HTML response
                    if 'direct' in response.text and 'inbox' in response.text:
                        print("✅ Got DM page HTML (need to extract data)")
                        # บันทึก HTML
                        output_file = f'results/dm_page_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
                        os.makedirs('results', exist_ok=True)
                        with open(output_file, 'w') as f:
                            f.write(response.text)
                        print(f"💾 HTML saved to: {output_file}")
                    else:
                        print(f"📄 HTML response: {response.text[:100]}...")

            elif response.status_code == 401:
                print("❌ Unauthorized - session expired")
            elif response.status_code == 403:
                print("❌ Forbidden - may be blocked")
            else:
                print(f"❌ Error: {response.status_code}")

        except Exception as e:
            print(f"❌ Exception: {e}")

    return False

if __name__ == "__main__":
    extract_dms_real()
