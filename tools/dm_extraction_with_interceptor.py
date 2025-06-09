# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
DM Extraction with Interceptor
Example script showing how to use the request interceptor for DM extraction
"""

import requests
import json
import sys
import os

# Add tools directory to path
sys.path.insert(0, 'tools')

from real_alx_interceptor import InterceptorContext

def extract_dms_with_interceptor():
    """Extract Instagram DMs using the request interceptor"""

    print("🚀 Starting DM extraction with request interceptor...")

    # Load session data
    try:
        with open('tools/session_alx_trading.json', 'r') as f:
            session_data = json.load(f)
            sessionid = session_data.get('sessionid', '')
            username = session_data.get('username', '')
    except Exception as e:
        print(f"❌ Failed to load session data: {e}")
        return

    if not sessionid:
        print("❌ No valid session found")
        return

    print(f"📱 Using session for user: {username}")

    # Use interceptor context
    with InterceptorContext() as interceptor:
        print("🔍 Request interceptor activated")

        # Instagram API headers
        headers = {
            'User-Agent': 'Instagram 219.0.0.12.117 Android (29/10; 420dpi; 1080x2220; samsung; SM-G973F; beyond1; exynos9820; en_US; 336448961)',
            'X-IG-App-ID': '936619743392459',
            'X-ASBD-ID': '198387',
            'X-IG-WWW-Claim': '0',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'cookie': f'sessionid={sessionid}; csrftoken=missing;'
        }

        # Create session
        session = requests.Session()
        session.headers.update(headers)

        # Test endpoints
        endpoints = [
            'https://i.instagram.com/api/v1/direct_v2/inbox/',
            'https://i.instagram.com/api/v1/direct_v2/inbox/?visual_message_reply_chain_enabled=true&thread_message_limit=10&persistentBadging=true&limit=20',
            'https://i.instagram.com/api/v1/accounts/edit/web_form_data/',
            'https://i.instagram.com/api/v1/users/web_profile_info/?username=' + username
        ]

        results = []

        for i, endpoint in enumerate(endpoints, 1):
            print(f"\n📡 Testing endpoint {i}/{len(endpoints)}: {endpoint[:50]}...")

            try:
                response = session.get(endpoint, timeout=15)

                result = {
                    'endpoint': endpoint,
                    'status_code': response.status_code,
                    'success': response.status_code == 200,
                    'response_size': len(response.content),
                    'error': None
                }

                if response.status_code == 200:
                    print(f"✅ Success: {response.status_code} - {len(response.content)} bytes")

                    # Try to parse JSON
                    try:
                        data = response.json()
                        if 'inbox' in data:
                            threads = data['inbox'].get('threads', [])
                            print(f"📬 Found {len(threads)} DM threads")
                            result['dm_threads'] = len(threads)
                        elif 'user' in data:
                            user_info = data['user']
                            print(f"👤 User info: {user_info.get('username', 'unknown')}")
                            result['user_info'] = user_info.get('username', 'unknown')
                    except Exception:
                        print("📄 Response is not JSON")

                elif response.status_code in [401, 403]:
                    print(f"🔐 Authentication issue: {response.status_code}")
                    result['error'] = 'Authentication failed'
                elif response.status_code == 429:
                    print(f"⏱️ Rate limited: {response.status_code}")
                    result['error'] = 'Rate limited'
                else:
                    print(f"❌ Failed: {response.status_code}")
                    result['error'] = f'HTTP {response.status_code}'

                results.append(result)

            except Exception as e:
                print(f"💥 Error: {e}")
                results.append({
                    'endpoint': endpoint,
                    'status_code': 0,
                    'success': False,
                    'error': str(e)
                })

        print("\n" + "="*60)
        print("📊 EXTRACTION RESULTS")
        print("="*60)

        successful = sum(1 for r in results if r['success'])
        print(f"✅ Successful requests: {successful}/{len(results)}")

        if successful > 0:
            print("🎉 DM extraction partially successful!")

            # Save results
            output_file = f"results/dm_extraction_with_interceptor_{int(time.time())}.json"
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            with open(output_file, 'w') as f:
                json.dump({
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'username': username,
                    'results': results,
                    'interceptor_stats': interceptor.get_stats()
                }, f, indent=2)

            print(f"💾 Results saved to: {output_file}")
        else:
            print("❌ All requests failed")

        # Print interceptor statistics
        print("\n" + "="*60)
        print("📈 INTERCEPTOR STATISTICS")
        print("="*60)
        interceptor.print_stats()

if __name__ == "__main__":
    import time
    extract_dms_with_interceptor()
