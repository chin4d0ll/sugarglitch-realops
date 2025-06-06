#!/usr/bin/env python3
"""
Test real Instagram extraction with session-alx.trading
"""

import json
import requests
import time
import os
from datetime import datetime

def load_session():
    """Load the real session file"""
    try:
        with open('/workspaces/sugarglitch-realops/sessions/session-alx.trading', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading session: {e}")
        return None

def cute_request(url, session, method='GET', **kwargs):
    """Cute rate limiting request handler"""
    max_retries = 5
    base_delay = 1
    
    for attempt in range(max_retries):
        try:
            print(f"🌟 Making cute request to {url} (attempt {attempt + 1})")
            
            if method.upper() == 'GET':
                response = session.get(url, **kwargs)
            elif method.upper() == 'POST':
                response = session.post(url, **kwargs)
            else:
                response = session.request(method, url, **kwargs)
            
            print(f"📊 Response status: {response.status_code}")
            
            if response.status_code == 429:
                retry_after = response.headers.get('Retry-After', base_delay * (2 ** attempt))
                print(f"😴 Rate limited! Cute sleep for {retry_after} seconds...")
                time.sleep(float(retry_after))
                continue
            
            if response.status_code == 200:
                print("✅ Cute request successful!")
                return response
            else:
                print(f"⚠️ Unexpected status: {response.status_code}")
                return response
                
        except Exception as e:
            print(f"❌ Request error: {e}")
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"😴 Waiting {delay}s before retry...")
                time.sleep(delay)
    
    print("❌ All cute attempts failed!")
    return None

def test_real_extraction():
    """Test real extraction with session"""
    print("🚀 Starting REAL Instagram DM extraction test...")
    print("=" * 50)
    
    # Load session
    session_data = load_session()
    if not session_data:
        return
    
    print(f"✅ Loaded session data: {list(session_data.keys())}")
    
    # Create requests session
    session = requests.Session()
    
    # Set up session cookies
    if 'cookies' in session_data:
        cookies = session_data['cookies']
        for cookie_name, cookie_value in cookies.items():
            session.cookies.set(cookie_name, cookie_value, domain='.instagram.com')
            print(f"🍪 Set cookie: {cookie_name}")
    
    # Set headers
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    })
    
    # Test Instagram main page
    print("\n🔍 Testing Instagram main page...")
    response = cute_request('https://www.instagram.com/', session)
    if response and response.status_code == 200:
        print("✅ Instagram main page accessible!")
        if 'alx.trading' in response.text or 'alx' in response.text:
            print("🎯 Found potential account reference!")
    else:
        print("❌ Instagram main page failed")
        return
    
    # Test direct inbox
    print("\n📬 Testing direct inbox...")
    inbox_url = 'https://www.instagram.com/direct/inbox/'
    response = cute_request(inbox_url, session)
    if response and response.status_code == 200:
        print("✅ Direct inbox accessible!")
        print(f"📊 Response length: {len(response.text)} characters")
        
        # Save response for analysis
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        with open(f'/workspaces/sugarglitch-realops/data/real_inbox_test_{timestamp}.html', 'w') as f:
            f.write(response.text)
        print(f"💾 Saved inbox response to real_inbox_test_{timestamp}.html")
    else:
        print("❌ Direct inbox failed")
        return
    
    # Test API endpoint
    print("\n🔧 Testing API endpoint...")
    api_url = 'https://www.instagram.com/api/v1/direct_v2/inbox/'
    response = cute_request(api_url, session, headers={
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': session.cookies.get('csrftoken', ''),
        'X-IG-App-ID': '936619743392459',
    })
    
    if response and response.status_code == 200:
        print("✅ API endpoint accessible!")
        try:
            data = response.json()
            print(f"📊 API response keys: {list(data.keys())}")
            
            # Save API response
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            with open(f'/workspaces/sugarglitch-realops/data/real_api_test_{timestamp}.json', 'w') as f:
                json.dump(data, f, indent=2)
            print(f"💾 Saved API response to real_api_test_{timestamp}.json")
            
            # Check for actual DM data
            if 'inbox' in data and 'threads' in data['inbox']:
                threads = data['inbox']['threads']
                print(f"🎯 Found {len(threads)} DM threads!")
                
                for i, thread in enumerate(threads[:3]):  # Show first 3 threads
                    print(f"   Thread {i+1}: {thread.get('thread_title', 'No title')}")
                    if 'users' in thread:
                        usernames = [user.get('username', 'Unknown') for user in thread['users']]
                        print(f"      Users: {', '.join(usernames)}")
                    if 'items' in thread and thread['items']:
                        last_msg = thread['items'][0]
                        msg_type = last_msg.get('item_type', 'unknown')
                        print(f"      Last message type: {msg_type}")
                
                return True
            else:
                print("⚠️ No DM threads found in API response")
                
        except Exception as e:
            print(f"❌ Error parsing API response: {e}")
            print(f"📄 Raw response: {response.text[:500]}...")
    else:
        print("❌ API endpoint failed")
    
    return False

if __name__ == "__main__":
    test_real_extraction()
