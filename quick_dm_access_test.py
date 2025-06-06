#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Quick Instagram DM Test
ทดสอบ DM extraction แบบเร็วๆ สำหรับ chin4d0ll
"""

import requests
import json
import time
from pathlib import Path
import re

def quick_dm_test():
    """⚡ ทดสอบ DM extraction แบบเร็วๆ"""
    
    print("🌸 Quick Instagram DM Test")
    print("💖 Testing real DM extraction")
    print("=" * 40)
    
    # Load session
    session_file = Path("sessions/session-alx.trading")
    if not session_file.exists():
        print("❌ Session file not found")
        return False
    
    try:
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        cookies = session_data.get('cookies', {})
        print(f"✅ Session loaded: {len(cookies)} cookies")
    except Exception as e:
        print(f"💥 Session load error: {e}")
        return False
    
    # Headers that work (from previous tests)
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0'
    }
    
    # Add cookies
    if cookies:
        cookie_string = '; '.join([f"{k}={v}" for k, v in cookies.items()])
        headers['Cookie'] = cookie_string
    
    # Test 1: Direct messages page
    print("\n📬 Testing direct messages page...")
    try:
        response = requests.get(
            'https://www.instagram.com/direct/inbox/',
            headers=headers,
            timeout=45,
            allow_redirects=True
        )
        
        print(f"📊 DM Page: HTTP {response.status_code} | {len(response.text):,} chars")
        print(f"🔗 Final URL: {response.url}")
        
        if response.status_code == 200:
            content = response.text
            
            # Check for login redirect
            if 'login' in response.url.lower():
                print("❌ Redirected to login - session expired")
                return False
            
            # Look for DM indicators
            dm_keywords = ['inbox', 'direct', 'message', 'thread', 'conversation']
            found_keywords = [kw for kw in dm_keywords if kw.lower() in content.lower()]
            
            if found_keywords:
                print(f"✅ DM keywords found: {found_keywords}")
            else:
                print("⚠️ No DM keywords found")
            
            # Look for JSON data
            json_patterns = [
                r'window\._sharedData\s*=\s*({.*?});',
                r'"inbox":\s*({.*?})',
                r'"threads":\s*(\[.*?\])',
                r'"direct_inbox":\s*({.*?})'
            ]
            
            found_json = False
            for pattern in json_patterns:
                matches = re.findall(pattern, content, re.DOTALL)
                if matches:
                    print(f"✅ Found JSON data: {len(matches)} matches")
                    found_json = True
                    
                    # Try to parse first match
                    try:
                        data = json.loads(matches[0])
                        print(f"📋 JSON parsed successfully: {list(data.keys())[:5]}...")
                    except:
                        print("⚠️ JSON parsing failed")
            
            if not found_json:
                print("⚠️ No JSON data found in response")
            
            # Save response for analysis
            data_dir = Path("data")
            data_dir.mkdir(exist_ok=True)
            
            timestamp = int(time.time())
            dm_file = data_dir / f"dm_page_test_{timestamp}.html"
            
            with open(dm_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"💾 DM page saved: {dm_file}")
            
            # Check content preview
            preview = content[:1000].replace('\n', ' ').replace('\r', '')
            print(f"📄 Content preview: {preview}...")
            
            return True
            
        else:
            print(f"❌ DM page failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"💥 DM test error: {e}")
        return False

def test_api_endpoints():
    """🔗 Test Instagram API endpoints"""
    print("\n🔗 Testing Instagram API endpoints...")
    
    # Load session
    session_file = Path("sessions/session-alx.trading")
    try:
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        cookies = session_data.get('cookies', {})
    except:
        cookies = {}
    
    # API headers
    api_headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Instagram-AJAX': '1',
        'X-IG-App-ID': '936619743392459',
        'Referer': 'https://www.instagram.com/direct/inbox/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    
    # Add cookies and CSRF
    if cookies:
        cookie_string = '; '.join([f"{k}={v}" for k, v in cookies.items()])
        api_headers['Cookie'] = cookie_string
        
        if 'csrftoken' in cookies:
            api_headers['X-CSRFToken'] = cookies['csrftoken']
    
    # Test API endpoints
    api_endpoints = [
        ('direct_inbox_api', 'https://www.instagram.com/api/v1/direct_v2/inbox/'),
        ('direct_threads', 'https://www.instagram.com/api/v1/direct_v2/threads/'),
        ('graphql_inbox', 'https://www.instagram.com/graphql/query/')
    ]
    
    for name, url in api_endpoints:
        try:
            print(f"  Testing {name}: {url}")
            
            response = requests.get(
                url,
                headers=api_headers,
                timeout=30,
                allow_redirects=False
            )
            
            print(f"    📊 {name}: HTTP {response.status_code} | {len(response.text):,} chars")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"    ✅ JSON response: {list(data.keys())[:5]}...")
                    
                    # Save API response
                    data_dir = Path("data")
                    data_dir.mkdir(exist_ok=True)
                    
                    timestamp = int(time.time())
                    api_file = data_dir / f"{name}_response_{timestamp}.json"
                    
                    with open(api_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    
                    print(f"    💾 API response saved: {api_file}")
                    
                except json.JSONDecodeError:
                    print(f"    ⚠️ Not JSON response")
            
        except Exception as e:
            print(f"    💥 {name} error: {e}")
        
        time.sleep(2)

def main():
    """🚀 Main test function"""
    print("🚀 Quick Instagram DM Test")
    print("💖 Testing if DM extraction actually works")
    print("🎯 Educational purposes only")
    print()
    
    try:
        # Test 1: DM page access
        dm_success = quick_dm_test()
        
        # Test 2: API endpoints
        test_api_endpoints()
        
        # Summary
        print(f"\n📊 TEST SUMMARY:")
        print(f"  DM Page Access: {'✅' if dm_success else '❌'}")
        print(f"  API Tests: Check individual results above")
        
        if dm_success:
            print("\n🎉 Good news! DM access is working!")
            print("✨ You can proceed with DM extraction")
        else:
            print("\n😢 DM access failed")
            print("💡 Session might need refresh or manual login")
            
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted")
    except Exception as e:
        print(f"💥 Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
