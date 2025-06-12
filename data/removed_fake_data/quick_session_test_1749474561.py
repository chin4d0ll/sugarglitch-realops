#!/usr/bin/env python3
"""
Quick Session Test - Testing without external dependencies
"""

import urllib.request
import urllib.parse
import json
import os

def test_session_basic():
    """Test session using only built-in modules"""

    # Check for session files
    session_files = [
        "/workspaces/sugarglitch-realops/alx_trading_session_fleming654.json",
        "/workspaces/sugarglitch-realops/fresh_sessions/working_session_1749202526.json",
        "/workspaces/sugarglitch-realops/session.json"
    ]

    session_data = None
    session_file = None

    # Find session file
    for file_path in session_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    session_data = json.load(f)
                    session_file = file_path
                    print(f"✅ Found session file: {file_path}")
                    break
            except Exception as e:
                print(f"❌ Cannot read file {file_path}: {e}")
                continue

    if not session_data:
        print("❌ No valid session file found")
        return False

    # Extract session data
    sessionid = session_data.get("sessionid") or session_data.get("cookies", {}).get("sessionid")
    if not sessionid:
        print("❌ No sessionid found in file")
        return False

    user_agent = session_data.get("user_agent", "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)")

    # Test URL
    test_url = "https://i.instagram.com/api/v1/accounts/current_user/"

    print(f"🔍 Testing session: {sessionid[:20]}...")
    print(f"📱 User-Agent: {user_agent[:50]}...")

    try:
        # Create request
        req = urllib.request.Request(test_url)
        req.add_header("User-Agent", user_agent)
        req.add_header("Accept", "*/*")
        req.add_header("Accept-Language", "en-US,en;q=0.9")
        req.add_header("X-Requested-With", "XMLHttpRequest")
        req.add_header("Cookie", f"sessionid={sessionid};")

        # Make request
        print(f"🌐 Testing URL: {test_url[:50]}...")
        
        with urllib.request.urlopen(req, timeout=15) as response:
            status_code = response.getcode()
            print(f"📊 Status Code: {status_code}")
            
            if status_code == 200:
                response_data = response.read().decode('utf-8')
                print(f"✅ Connection successful!")
                print(f"📝 Response length: {len(response_data)} bytes")
                print(f"📝 Response snippet: {response_data[:200]}...")
                
                # Try to parse as JSON
                try:
                    data = json.loads(response_data)
                    if "user" in data:
                        print(f"✅ User data found: {data.get('user', {}).get('username', 'N/A')}")
                        return True
                    else:
                        print(f"📝 Response keys: {list(data.keys())}")
                        return True
                except json.JSONDecodeError:
                    print("📝 Response is not JSON")
                    if "html" not in response_data.lower():
                        return True
            else:
                print(f"⚠️ Status {status_code}")

    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.reason}")
        if e.code in [401, 403]:
            print("❌ Session expired or no permission")
        elif e.code == 429:
            print("❌ Rate limited")
    except urllib.error.URLError as e:
        print(f"❌ URL Error: {e.reason}")
    except Exception as e:
        print(f"❌ Error: {e}")

    return False

if __name__ == "__main__":
    print("🚀 Starting Instagram Session Test...")
    success = test_session_basic()

    if success:
        print("\n✅ Session is working! Can proceed to proxy testing")
    else:
        print("\n❌ Session is invalid or expired - need to get new session")
