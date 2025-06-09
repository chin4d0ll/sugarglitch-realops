# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔧 SESSION VALIDATOR AND FIXER
Validate and fix session issues for ALX.Trading
"""

import json
import urllib.parse
import requests
import time

def load_and_decode_session():
    """Load and properly decode session"""
    session_file = "/workspaces/sugarglitch-realops/sessions/session-alx.trading"

    try:
        with open(session_file, 'r') as f:
            session_data = json.load(f)

        print("📄 Raw session data:")
        print(json.dumps(session_data, indent=2))

        # Extract sessionid
        sessionid = session_data.get('cookies', {}).get('sessionid', '')
        print(f"\n🔑 Raw sessionid: {sessionid}")

        # URL decode it
        decoded_sessionid = urllib.parse.unquote(sessionid)
        print(f"🔓 Decoded sessionid: {decoded_sessionid}")

        return {
            'raw': sessionid,
            'decoded': decoded_sessionid,
            'cookies': {'sessionid': decoded_sessionid}
        }

    except Exception as e:
        print(f"❌ Session load error: {e}")
        return None

def test_session_validity(cookies):
    """Test if session is still valid"""
    print(f"\n🧪 Testing session validity...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    session = requests.Session()
    session.cookies.update(cookies)
    session.headers.update(headers)

    # Test different endpoints
    test_urls = [
        'https://www.instagram.com/',
        'https://www.instagram.com/accounts/edit/',
        'https://www.instagram.com/alx.trading/',
    ]

    results = {}

    for url in test_urls:
        try:
            print(f"🔍 Testing: {url}")
            response = session.get(url, timeout=15, allow_redirects=False)

            print(f"   Status: {response.status_code}")

            if response.status_code == 302:
                location = response.headers.get('location', '')
                print(f"   Redirect to: {location}")
                if 'login' in location:
                    results[url] = 'login_required'
                else:
                    results[url] = 'redirect'
            elif response.status_code == 200:
                # Check if we're actually logged in
                content = response.text
                if 'Log In' in content and 'Sign Up' in content:
                    results[url] = 'not_logged_in'
                    print(f"   ❌ Not logged in")
                elif 'instagram.com/accounts/login' in content:
                    results[url] = 'login_redirect'
                    print(f"   ❌ Login redirect in content")
                else:
                    results[url] = 'success'
                    print(f"   ✅ Access granted")
            else:
                results[url] = f'error_{response.status_code}'
                print(f"   ❌ Error {response.status_code}")

        except Exception as e:
            print(f"   ❌ Exception: {e}")
            results[url] = f'exception_{str(e)}'

    return results

def try_extract_with_simple_method(cookies):
    """Try simple extraction with working session"""
    print(f"\n📨 Attempting simple DM extraction...")

    session = requests.Session()
    session.cookies.update(cookies)

    # Add proper headers
    headers = {
        'User-Agent': 'Instagram 219.0.0.12.117 Android',
        'Accept': '*/*',
        'Accept-Language': 'en-US',
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Instagram-AJAX': '1',
        'X-CSRFToken': 'missing',
    }
    session.headers.update(headers)

    # First, try to get CSRF token
    try:
        response = session.get('https://www.instagram.com/', allow_redirects=False)
        if response.status_code == 200:
            import re
            csrf_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
            if csrf_match:
                csrf_token = csrf_match.group(1)
                session.headers['X-CSRFToken'] = csrf_token
                print(f"✅ CSRF token obtained: {csrf_token[:20]}...")
    except Exception:
        pass

    # Try mobile API endpoints
    mobile_endpoints = [
        'https://i.instagram.com/api/v1/direct_v2/inbox/?visual_message_return_type=unseen',
        'https://i.instagram.com/api/v1/direct_v2/threads/',
        'https://www.instagram.com/api/v1/direct_v2/inbox/',
    ]

    for endpoint in mobile_endpoints:
        try:
            print(f"🔍 Mobile API: {endpoint}")
            response = session.get(endpoint, timeout=20, allow_redirects=False)
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'inbox' in data or 'threads' in data:
                        print(f"   ✅ DM data found!")

                        # Save the data
                        output_file = f"/workspaces/sugarglitch-realops/data/dm_success_{int(time.time())}.json"
                        with open(output_file, 'w') as f:
                            json.dump(data, f, indent=2)
                        print(f"   📁 Saved: {output_file}")
                        return data
                except Exception:
                    print(f"   ⚠️ Non-JSON response")
            else:
                print(f"   ❌ Status {response.status_code}")

        except Exception as e:
            print(f"   ❌ Error: {e}")

    return None

def main():
    print("🔧 SESSION VALIDATOR AND FIXER")
    print("=" * 50)

    # Load and decode session
    session_info = load_and_decode_session()
    if not session_info:
        return

    # Test with decoded cookies
    cookies = session_info['cookies']
    validity_results = test_session_validity(cookies)

    print(f"\n📊 VALIDITY TEST RESULTS:")
    for url, result in validity_results.items():
        print(f"   {url}: {result}")

    # If any URL works, try extraction
    if any(result == 'success' for result in validity_results.values()):
        print(f"\n✅ Some endpoints accessible, trying extraction...")
        dm_data = try_extract_with_simple_method(cookies)

        if dm_data:
            print(f"\n🎉 SUCCESS! DM data extracted")
        else:
            print(f"\n❌ No DM data found")
    else:
        print(f"\n❌ Session appears invalid or expired")
        print(f"💡 May need fresh session or different approach")

if __name__ == "__main__":
    main()
