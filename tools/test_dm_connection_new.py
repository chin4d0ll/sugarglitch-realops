# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Test DM Connection Script
Tests Instagram Direct Message API connection using session cookies
"""

import json
import requests
import os
from typing import Dict, Any, Optional
def load_session(session_path: str) -> Optional[Dict[str, str]]:
    """
    Load session data from JSON file

    Args:
        session_path: Path to session JSON file

    Returns:
        Dictionary with sessionid and user_agent, or None if failed
    """
    try:
        if not os.path.exists(session_path):
            print(f"❌ Session file not found: {session_path}")
            return None

        with open(session_path, 'r') as f:
            session_data = json.load(f)

        # Validate required fields
        if 'sessionid' not in session_data:
            print("❌ Missing 'sessionid' in session data")
            return None

        if 'user_agent' not in session_data:
            print("❌ Missing 'user_agent' in session data")
            return None

        print(f"✅ Session loaded from: {session_path}")
        print(f"📊 SessionID: {session_data['sessionid'][:10]}...")
        print(f"🌐 User Agent: {session_data['user_agent'][:50]}...")

        return session_data

    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in session file: {e}")
        return None
    except Exception as e:
        print(f"❌ Error loading session: {e}")
        return None
def test_dm_connection(session_data: Dict[str, str]) -> bool:
    """
    Test DM connection using Instagram API

    Args:
        session_data: Dictionary with sessionid and user_agent

    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        print("\n🔍 Testing DM connection...")

        # Prepare headers
        headers = {
            'User-Agent': session_data['user_agent'],
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': session_data['sessionid'][:32],  # Use part of sessionid as CSRF token
            'X-Instagram-AJAX': '1',
            'X-IG-App-ID': '936619743392459',
            'Referer': 'https://www.instagram.com/',
            'Origin': 'https://www.instagram.com'
        }

        # Prepare cookies
        cookies = {
            'sessionid': session_data['sessionid'],
            'csrftoken': session_data['sessionid'][:32],
        }

        # Send GET request to Instagram DM API
        url = 'https://i.instagram.com/api/v1/direct_v2/inbox/'

        print(f"📡 Sending request to: {url}")

        response = requests.get(
            url,
            headers=headers,
            cookies=cookies,
            timeout=30
        )

        print(f"📊 HTTP Status: {response.status_code}")

        if response.status_code == 200:
            try:
                data = response.json()

                # Check if response has threads
                if 'inbox' in data and 'threads' in data['inbox']:
                    threads = data['inbox']['threads']
                    thread_count = len(threads)

                    print(f"✅ Connected – {thread_count} threads found")

                    # Print additional info if available
                    if 'has_older' in data['inbox']:
                        print(f"📄 Has older messages: {data['inbox']['has_older']}")

                    if 'unseen_count' in data['inbox']:
                        print(f"📬 Unseen messages: {data['inbox']['unseen_count']}")

                    return True
                else:
                    print("❌ Invalid response format - no threads found in inbox")
                    return False

            except json.JSONDecodeError:
                print("❌ Invalid JSON response")
                print(f"Response content: {response.text[:200]}...")
                return False

        elif response.status_code == 401:
            print("❌ Session invalid - Unauthorized (401)")
            return False
        elif response.status_code == 403:
            print("❌ Access forbidden - Possible rate limiting or blocked (403)")
            return False
        elif response.status_code == 429:
            print("❌ Too many requests - Rate limited (429)")
            return False
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return False

    except requests.exceptions.Timeout:
        print("❌ Request timeout - Instagram servers may be slow")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - Check internet connection")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
def main():
    """Main function"""
    print("🚀 Instagram DM Connection Test")
    print("=" * 40)

    # Default session paths to try
    session_paths = [
        'tools/validated_session.json',
        'tools/session_alx_trading.json',
        'session.json'
    ]

    session_data = None

    # Try to load session from available files
    for path in session_paths:
        session_data = load_session(path)
        if session_data:
            break

    if not session_data:
        print("\n❌ No valid session found. Please run auto_extract_session.py first.")
        return False

    # Test DM connection
    success = test_dm_connection(session_data)

    if success:
        print("\n✅ DM connection test completed successfully!")
    else:
        print("\n❌ DM connection test failed")

    return success
if __name__ == "__main__":
    main()
