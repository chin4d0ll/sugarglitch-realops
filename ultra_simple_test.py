#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ Ultra Simple Instagram Test
ทดสอบแบบง่ายที่สุด
"""

import requests
import json
from pathlib import Path

def simple_test():
    """⚡ ทดสอบแบบง่ายๆ"""
    
    print("🌸 Ultra Simple Instagram Test")
    print("=" * 40)
    
    # Working mobile headers (confirmed from quick test)
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive'
    }
    
    # Load session
    session_file = Path("sessions/session-alx.trading")
    if session_file.exists():
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            if 'cookies' in session_data:
                cookies = session_data['cookies']
                print("✅ Session loaded with cookies")
            else:
                cookies = {}
                print("⚠️ No cookies in session")
        except:
            cookies = {}
            print("❌ Session load failed")
    else:
        cookies = {}
        print("❌ Session file not found")
    
    # Test 1: Basic Instagram homepage
    print("\n🏠 Testing Instagram homepage...")
    try:
        response = requests.get(
            'https://www.instagram.com/', 
            headers=headers,
            cookies=cookies,
            timeout=30
        )
        
        print(f"📊 Homepage: HTTP {response.status_code} ({len(response.text):,} chars)")
        
        if response.status_code == 200:
            print("✅ Homepage accessible!")
            
            # Check if logged in
            if 'instagram.com' in response.text and 'login' not in response.url:
                print("🔑 Logged in status detected!")
            
            # Save homepage content
            with open('data/homepage_test.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("💾 Homepage saved to data/homepage_test.html")
            
        else:
            print(f"❌ Homepage failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Homepage error: {e}")
    
    # Test 2: Try direct messages page
    print("\n📬 Testing direct messages...")
    try:
        response = requests.get(
            'https://www.instagram.com/direct/inbox/', 
            headers=headers,
            cookies=cookies,
            timeout=30
        )
        
        print(f"📊 Direct: HTTP {response.status_code} ({len(response.text):,} chars)")
        
        if response.status_code == 200:
            print("✅ Direct messages accessible!")
            
            # Check for DM content
            dm_keywords = ['direct', 'message', 'inbox', 'thread']
            content_lower = response.text.lower()
            
            found_keywords = [kw for kw in dm_keywords if kw in content_lower]
            if found_keywords:
                print(f"🎯 DM keywords found: {found_keywords}")
            
            # Save DM content
            with open('data/dm_page_test.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("💾 DM page saved to data/dm_page_test.html")
            
        elif response.status_code == 500:
            print("❌ Server error 500 - Instagram server issue")
        elif response.status_code == 429:
            print("⚠️ Rate limited - too many requests")
        else:
            print(f"❌ Direct messages failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Direct messages error: {e}")
    
    # Test 3: Try API endpoint
    print("\n🔌 Testing API endpoint...")
    try:
        # Add CSRF token if available
        api_headers = headers.copy()
        if 'csrftoken' in cookies:
            api_headers['X-CSRFToken'] = cookies['csrftoken']
        
        response = requests.get(
            'https://www.instagram.com/api/v1/direct_v2/inbox/', 
            headers=api_headers,
            cookies=cookies,
            timeout=30
        )
        
        print(f"📊 API: HTTP {response.status_code} ({len(response.text):,} chars)")
        
        if response.status_code == 200:
            print("✅ API accessible!")
            
            try:
                api_data = response.json()
                print(f"🔌 JSON response with {len(api_data)} keys")
                
                # Check for inbox data
                if 'inbox' in api_data:
                    inbox = api_data['inbox']
                    if 'threads' in inbox:
                        thread_count = len(inbox['threads'])
                        print(f"📬 Found {thread_count} DM threads!")
                
                # Save API response
                with open('data/api_response_test.json', 'w', encoding='utf-8') as f:
                    json.dump(api_data, f, ensure_ascii=False, indent=2)
                print("💾 API response saved to data/api_response_test.json")
                
            except json.JSONDecodeError:
                print("⚠️ API response is not JSON")
                with open('data/api_response_test.txt', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print("💾 API response saved as text")
            
        else:
            print(f"❌ API failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ API error: {e}")
    
    print("\n🎯 Test Complete!")
    print("📁 Check data/ folder for saved responses")

if __name__ == "__main__":
    # Ensure data directory exists
    Path("data").mkdir(exist_ok=True)
    simple_test()
