# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Session Status Checker
"""
import requests
import json

def check_session_status():
    print("🔍 CHECKING SESSION STATUS")
    print("="*40)

    # โหลด session
    try:
        with open('tools/session_alx_trading.json', 'r') as f:
            session = json.load(f)
        sessionid = session.get('sessionid', '')
        print(f"Session ID: {sessionid}")
    except Exception:
        print("❌ Cannot load session file")
        return

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Cookie': f'sessionid={sessionid}'
    }

    # Test 1: Instagram homepage
    print("\n🧪 Test 1: Instagram Homepage")
    try:
        response = requests.get('https://www.instagram.com/', headers = headers, timeout = 10)
        print(f"Status: {response.status_code}")

        if 'login' in response.url.lower():
            print("❌ REDIRECTED TO LOGIN - Session expired!")
        elif '"is_logged_in":true' in response.text:
            print("✅ LOGGED IN - Session is valid!")
        elif '"is_logged_in":false' in response.text:
            print("❌ NOT LOGGED IN - Session expired!")
        else:
            print("⚠️  Unknown status - checking response...")
            if 'window._sharedData' in response.text[:1000]:
                print("✅ Got Instagram page")
            else:
                print("❌ Not Instagram page")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 2: Profile check
    print("\n🧪 Test 2: Profile Access")
    try:
        response = requests.get('https://www.instagram.com/accounts/edit/', headers = headers, timeout = 10)
        print(f"Status: {response.status_code}")

        if response.status_code == 200 and 'login' not in response.url:
            print("✅ Can access profile settings")
        else:
            print("❌ Cannot access profile - session invalid")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 3: Simple API call
    print("\n🧪 Test 3: Simple API")
    headers['x-ig-app-id'] = '936619743392459'
    try:
        response = requests.get('https://www.instagram.com/api/v1/users/web_profile_info/?username = instagram',
                               headers = headers, timeout = 10)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            print("✅ API access working")
        elif response.status_code == 401:
            print("❌ Unauthorized - session expired")
        elif response.status_code == 403:
            print("❌ Forbidden - session blocked")
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_session_status()
