#!/usr/bin/env python3
"""
Cookie Tester - Test if extracted cookies work
"""

import json
import requests
import os

def test_fresh_cookies():
    """Test if fresh cookies work with Instagram"""
    
    # Try to load cookies
    cookie_files = [
        "/workspaces/sugarglitch-realops/fresh_cookies.json",
        "/workspaces/sugarglitch-realops/fresh_cookies_full.json",
        "/workspaces/sugarglitch-realops/cookies/alx.trading_cookies_latest.json"
    ]
    
    cookies = None
    cookie_file_used = None
    
    for cookie_file in cookie_files:
        if os.path.exists(cookie_file):
            try:
                with open(cookie_file, 'r') as f:
                    cookies = json.load(f)
                cookie_file_used = cookie_file
                break
            except:
                continue
    
    if not cookies:
        print("❌ No cookie files found!")
        print("Available files should be:")
        for cf in cookie_files:
            print(f"  - {cf}")
        return False
    
    print(f"🍪 Testing cookies from: {cookie_file_used}")
    
    # Test with Instagram API
    session = requests.Session()
    
    # Add headers
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })
    
    # Add cookies
    for name, value in cookies.items():
        if isinstance(value, str) and not value.startswith("PASTE_YOUR_"):
            session.cookies.set(name, value, domain='.instagram.com')
    
    # Test URLs
    test_urls = [
        "https://www.instagram.com/alx.trading/",
        "https://www.instagram.com/api/v1/users/web_profile_info/?username=alx.trading",
        "https://www.instagram.com/"
    ]
    
    results = {}
    
    for url in test_urls:
        try:
            print(f"🔗 Testing: {url}")
            response = session.get(url, timeout=10)
            
            status = response.status_code
            is_logged_in = '"viewer":' in response.text or '"user":' in response.text
            is_blocked = "challenge" in response.text.lower() or "suspicious" in response.text.lower()
            
            results[url] = {
                'status_code': status,
                'is_logged_in': is_logged_in,
                'is_blocked': is_blocked,
                'content_length': len(response.text)
            }
            
            if status == 200 and is_logged_in and not is_blocked:
                print(f"  ✅ SUCCESS: {status} - Logged in")
            elif status == 200 and not is_blocked:
                print(f"  ⚠️ PARTIAL: {status} - Not logged in but accessible")
            elif is_blocked:
                print(f"  🚫 BLOCKED: {status} - Challenge required")
            else:
                print(f"  ❌ FAILED: {status}")
            
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            results[url] = {'error': str(e)}
    
    # Summary
    print("\n" + "="*50)
    print("🧪 COOKIE TEST RESULTS")
    print("="*50)
    
    success_count = sum(1 for r in results.values() if 
                       isinstance(r, dict) and 
                       r.get('status_code') == 200 and 
                       r.get('is_logged_in'))
    
    if success_count > 0:
        print(f"✅ COOKIES WORK! ({success_count}/{len(test_urls)} tests passed)")
        print("🚀 You can now run the main extraction script!")
        return True
    else:
        print("❌ COOKIES DON'T WORK")
        print("💡 Try extracting fresh cookies from browser")
        return False

if __name__ == "__main__":
    test_fresh_cookies()
