# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Session Validation Script
Tests if the Instagram session is valid and working
"""

import sys
import requests
import json
from pathlib import Path
from urllib.parse import unquote

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

def test_session_validity():
    """Test if the session is valid by making a test request"""
    print("🔐 Testing Instagram Session Validity...")
    print("=" * 50)

    # Load session from config
    config_path = Path(__file__).parent / 'config' / 'settings.json'

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)

        session_data = config.get('session_data', {})
        sessionid = session_data.get('sessionid', '')

        if not sessionid or sessionid == 'YOUR_SESSION_ID_HERE':
            print("❌ No valid sessionid found in config")
            return False

        # URL decode sessionid if needed
        sessionid = unquote(sessionid)

        print(f"📋 Testing sessionid: {sessionid[:20]}...")

        # Create session
        session = requests.Session()

        # Set headers
        session.headers.update({
            'User-Agent': config.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

        # Set cookies
        session.cookies.set('sessionid', sessionid, domain='.instagram.com')
        if session_data.get('csrftoken') and session_data['csrftoken'] != 'missing':
            session.cookies.set('csrftoken', session_data['csrftoken'], domain='.instagram.com')
        if session_data.get('mid'):
            session.cookies.set('mid', session_data['mid'], domain='.instagram.com')
        if session_data.get('ig_did'):
            session.cookies.set('ig_did', session_data['ig_did'], domain='.instagram.com')

        print("📡 Testing connection to Instagram...")

        # Test 1: Basic page access
        try:
            response = session.get('https://www.instagram.com/')
            print(f"   Basic access: Status {response.status_code}")

            if 'login' in response.url:
                print("   ❌ Redirected to login - session may be invalid")
            else:
                print("   ✅ No login redirect - good sign")
        except Exception as e:
            print(f"   ❌ Basic access failed: {e}")
            return False

        # Test 2: API endpoint
        try:
            api_response = session.get('https://www.instagram.com/api/v1/accounts/edit/web_form_data/')
            print(f"   API access: Status {api_response.status_code}")

            if api_response.status_code == 200:
                try:
                    data = api_response.json()
                    if 'form_data' in data:
                        user_id = data['form_data'].get('user_id')
                        username = data['form_data'].get('username')
                        print(f"   ✅ Authentication successful!")
                        print(f"   👤 User ID: {user_id}")
                        print(f"   👤 Username: {username}")
                        return True
                    else:
                        print("   ⚠️  API returned data but no form_data")
                except json.JSONDecodeError:
                    print("   ⚠️  API returned non-JSON response")
            else:
                print(f"   ❌ API access failed with status {api_response.status_code}")

        except Exception as e:
            print(f"   ❌ API test failed: {e}")

        # Test 3: DM inbox (if basic auth worked)
        try:
            dm_response = session.get('https://www.instagram.com/api/v1/direct_v2/inbox/?persistentBadging=true&folder=&limit=1')
            print(f"   DM access: Status {dm_response.status_code}")

            if dm_response.status_code == 200:
                dm_data = dm_response.json()
                if 'inbox' in dm_data:
                    threads = dm_data.get('inbox', {}).get('threads', [])
                    print(f"   ✅ DM access successful! Found {len(threads)} threads")
                    return True
                else:
                    print("   ⚠️  DM API returned data but no inbox")
            elif dm_response.status_code == 401:
                print("   ❌ Unauthorized access to DMs")
            else:
                print(f"   ❌ DM access failed with status {dm_response.status_code}")

        except Exception as e:
            print(f"   ❌ DM test failed: {e}")

        return False

    except Exception as e:
        print(f"❌ Session validation failed: {e}")
        return False

def main():
    """Main function"""
    success = test_session_validity()

    print("\n" + "=" * 50)
    if success:
        print("🎉 SESSION IS VALID AND READY!")
        print("✅ You can now run: python main.py")
        print("📊 Real DM extraction will work with this session")
    else:
        print("❌ SESSION VALIDATION FAILED")
        print("💡 Suggestions:")
        print("   1. Check if sessionid is fresh (logged in recently)")
        print("   2. Try logging into Instagram again and get new sessionid")
        print("   3. Check if your IP/VPN is blocked by Instagram")
        print("   4. Verify the sessionid format is correct")

    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
