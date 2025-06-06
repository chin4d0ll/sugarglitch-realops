#!/usr/bin/env python3
"""
Instagram DM Connection Tester
Tests Instagram DM API connection using session cookies.

Usage:
    python3 tools/test_dm_connection.py [session_file]

Requirements:
    - Session JSON file with sessionid and user_agent
    - Internet connection
    - Valid Instagram session

Author: SugarGlitch RealOps
Date: June 6, 2025
"""

import json
import sys
import requests
import os
from pathlib import Path

def load_session(session_file: str) -> dict:
    """
    Load session data from JSON file.
    
    Args:
        session_file: Path to session JSON file
        
    Returns:
        dict: Session data containing sessionid and user_agent
        
    Raises:
        FileNotFoundError: If session file doesn't exist
        ValueError: If session file is invalid
    """
    if not os.path.exists(session_file):
        raise FileNotFoundError(f"Session file not found: {session_file}")
    
    try:
        with open(session_file, 'r', encoding='utf-8') as f:
            session_data = json.load(f)
        
        # Validate required fields
        required_fields = ['sessionid', 'user_agent']
        missing_fields = [field for field in required_fields if field not in session_data]
        
        if missing_fields:
            raise ValueError(f"Missing required fields in session file: {missing_fields}")
        
        return session_data
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in session file: {e}")

def test_dm_connection(session_data: dict) -> bool:
    """
    Test Instagram DM API connection.
    
    Args:
        session_data: Dictionary containing sessionid and user_agent
        
    Returns:
        bool: True if connection successful, False otherwise
    """
    # Instagram DM API endpoint
    dm_api_url = "https://i.instagram.com/api/v1/direct_v2/inbox/"
    
    # Prepare headers
    headers = {
        'User-Agent': session_data['user_agent'],
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': session_data.get('csrftoken', ''),
        'X-Instagram-AJAX': '1',
        'X-IG-App-ID': '936619743392459',
        'X-IG-WWW-Claim': '0',
        'Origin': 'https://www.instagram.com',
        'Referer': 'https://www.instagram.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Connection': 'keep-alive',
    }
    
    # Prepare cookies
    cookies = {
        'sessionid': session_data['sessionid'],
    }
    
    # Add additional cookies if available
    if 'csrftoken' in session_data:
        cookies['csrftoken'] = session_data['csrftoken']
    if 'ds_user_id' in session_data:
        cookies['ds_user_id'] = session_data['ds_user_id']
    if 'rur' in session_data:
        cookies['rur'] = session_data['rur']
    
    try:
        print("🔍 Testing Instagram DM API connection...")
        print(f"📡 Endpoint: {dm_api_url}")
        print(f"🍪 Session ID: {session_data['sessionid'][:10]}...")
        print(f"🌐 User Agent: {session_data['user_agent'][:50]}...")
        print()
        
        # Send GET request to DM inbox API
        response = requests.get(
            dm_api_url,
            headers=headers,
            cookies=cookies,
            timeout=30
        )
        
        print(f"📊 HTTP Status: {response.status_code}")
        print(f"📏 Response Size: {len(response.content)} bytes")
        
        # Check if request was successful
        if response.status_code == 200:
            try:
                data = response.json()
                
                # Check if response has expected structure
                if 'inbox' in data and 'threads' in data['inbox']:
                    threads = data['inbox']['threads']
                    thread_count = len(threads)
                    
                    print(f"✅ Connected – {thread_count} threads found")
                    
                    # Additional info
                    if 'has_older' in data['inbox']:
                        print(f"📋 Has older messages: {data['inbox']['has_older']}")
                    if 'unseen_count' in data['inbox']:
                        print(f"�️ Unseen count: {data['inbox']['unseen_count']}")
                    if 'unseen_count_ts' in data['inbox']:
                        print(f"⏰ Last unseen timestamp: {data['inbox']['unseen_count_ts']}")
                    
                    # Show some thread details if available
                    if thread_count > 0:
                        print(f"\n📝 Sample thread info:")
                        for i, thread in enumerate(threads[:3]):  # Show first 3 threads
                            thread_id = thread.get('thread_id', 'N/A')
                            users = thread.get('users', [])
                            user_names = [user.get('username', 'Unknown') for user in users]
                            print(f"  Thread {i+1}: {thread_id} ({', '.join(user_names)})")
                    
                    return True
                else:
                    print("❌ Response structure invalid - missing inbox/threads")
                    print(f"🔍 Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                    return False
                    
            except json.JSONDecodeError:
                print("❌ Response is not valid JSON")
                print(f"� Response preview: {response.text[:200]}...")
                return False
                
        elif response.status_code == 401:
            print("❌ Session invalid - Authentication failed (401)")
            return False
        elif response.status_code == 403:
            print("❌ Access forbidden - Account may be restricted (403)")
            return False
        elif response.status_code == 429:
            print("❌ Rate limited - Too many requests (429)")
            return False
        else:
            print(f"❌ Request failed with status {response.status_code}")
            try:
                error_data = response.json()
                if 'message' in error_data:
                    print(f"📝 Error message: {error_data['message']}")
            except:
                print(f"🔍 Response preview: {response.text[:200]}...")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timeout - Instagram servers may be slow")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - Check internet connection")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main function to run the DM connection test."""
    print("🔐 Instagram DM Connection Tester")
    print("=" * 50)
    
    # Determine session file path
    if len(sys.argv) > 1:
        session_file = sys.argv[1]
    else:
        # Default to the session file in tools directory
        session_file = os.path.join(os.path.dirname(__file__), 'session_alx_trading.json')
    
    try:
        # Load session data
        print(f"📂 Loading session from: {session_file}")
        session_data = load_session(session_file)
        print("✅ Session data loaded successfully")
        print()
        
        # Test DM connection
        success = test_dm_connection(session_data)
        
        print()
        print("=" * 50)
        if success:
            print("🎉 DM Connection Test: PASSED")
            print("✅ Session is valid and can access DM inbox")
        else:
            print("� DM Connection Test: FAILED")
            print("❌ Session is invalid or cannot access DM inbox")
            
        return 0 if success else 1
        
    except FileNotFoundError as e:
        print(f"❌ File Error: {e}")
        print("💡 Tip: Create a session file using auto_extract_session.py")
        return 1
    except ValueError as e:
        print(f"❌ Data Error: {e}")
        print("💡 Tip: Check session file format and content")
        return 1
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
