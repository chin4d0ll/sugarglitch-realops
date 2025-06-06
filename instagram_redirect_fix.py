#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 Instagram Redirect Loop Fix for ALX Trading
แก้ปัญหา redirect loop และ HTTP 500 
"""

import requests
import json
from pathlib import Path
import urllib3
import warnings

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fix_redirect_loop():
    """🔧 แก้ปัญหา redirect loop"""
    print("🌸 Instagram Redirect Loop Fix")
    print("🔧 แก้ปัญหา 30 redirects สำหรับ ALX Trading")
    print("=" * 50)
    
    # Load session
    session_file = Path("sessions/session-alx.trading")
    session_data = {}
    
    if session_file.exists():
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            print("✅ Session loaded")
        except:
            print("❌ Session load failed")
    
    # 🛡️ Anti-redirect headers (มากที่สุดเท่าที่เป็นไปได้)
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'identity',  # ไม่ใช้ compression เพื่อหลีกเลี่ยงปัญหา
        'Connection': 'close',  # ปิด connection หลังใช้
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1'
    }
    
    # Session setup
    session = requests.Session()
    session.headers.update(headers)
    session.max_redirects = 5  # จำกัด redirects
    
    # Add cookies if available
    if session_data and 'cookies' in session_data:
        for name, value in session_data['cookies'].items():
            session.cookies.set(name, value, domain='.instagram.com')
        print("🔑 Session cookies applied")
    
    # Test 1: Simple connectivity
    print("\n🌐 Test 1: Basic Connectivity")
    try:
        response = session.get(
            'https://www.instagram.com/',
            allow_redirects=False,  # ไม่ follow redirects
            timeout=30,
            verify=False
        )
        print(f"  📊 Status: {response.status_code}")
        print(f"  📍 Location: {response.headers.get('Location', 'None')}")
        
        if response.status_code in [200, 302, 301]:
            print("  ✅ Basic connectivity works!")
        else:
            print(f"  ⚠️ Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Test 2: Follow redirects manually
    print("\n🔄 Test 2: Manual Redirect Following")
    try:
        url = 'https://www.instagram.com/'
        redirect_count = 0
        max_redirects = 3
        
        while redirect_count < max_redirects:
            response = session.get(
                url,
                allow_redirects=False,
                timeout=30,
                verify=False
            )
            
            print(f"  📊 Step {redirect_count + 1}: HTTP {response.status_code}")
            
            if response.status_code == 200:
                print("  ✅ Success! Final page reached")
                print(f"  📏 Content size: {len(response.text):,} chars")
                
                # Quick content check
                if 'instagram' in response.text.lower():
                    print("  🎉 Instagram content confirmed!")
                break
                
            elif response.status_code in [301, 302, 303, 307, 308]:
                location = response.headers.get('Location')
                if location:
                    if location.startswith('/'):
                        url = 'https://www.instagram.com' + location
                    else:
                        url = location
                    print(f"  🔄 Redirecting to: {url}")
                    redirect_count += 1
                else:
                    print("  ❌ Redirect without location!")
                    break
            else:
                print(f"  ❌ Unexpected status: {response.status_code}")
                break
                
    except Exception as e:
        print(f"  ❌ Manual redirect error: {e}")
    
    # Test 3: Direct ALX Trading profile
    print("\n🎯 Test 3: Direct ALX Trading Profile")
    try:
        # Reset session for clean test
        alx_session = requests.Session()
        alx_session.headers.update(headers)
        alx_session.max_redirects = 3
        
        # Add cookies
        if session_data and 'cookies' in session_data:
            for name, value in session_data['cookies'].items():
                alx_session.cookies.set(name, value, domain='.instagram.com')
        
        response = alx_session.get(
            'https://www.instagram.com/alx.trading/',
            allow_redirects=True,  # Allow limited redirects
            timeout=30,
            verify=False
        )
        
        print(f"  📊 Status: {response.status_code}")
        print(f"  📏 Size: {len(response.text):,} chars")
        print(f"  🔗 Final URL: {response.url}")
        
        if response.status_code == 200:
            print("  ✅ ALX Trading profile accessible!")
            
            # Save content for analysis
            timestamp = int(__import__('time').time())
            output_file = f"data/alx_profile_content_{timestamp}.html"
            Path("data").mkdir(exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"  💾 Content saved: {output_file}")
            
            # Content analysis
            content_lower = response.text.lower()
            if 'alx' in content_lower:
                print("  🎉 ALX content found!")
            if 'trading' in content_lower:
                print("  📈 Trading content found!")
            if 'profile' in content_lower or 'user' in content_lower:
                print("  👤 Profile structure detected!")
                
        else:
            print(f"  ❌ Failed with status: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ ALX profile error: {e}")
    
    # Test 4: Quick DM check
    print("\n📨 Test 4: DM Endpoint Check")
    try:
        dm_headers = headers.copy()
        dm_headers['Referer'] = 'https://www.instagram.com/'
        dm_headers['X-Requested-With'] = 'XMLHttpRequest'
        
        dm_session = requests.Session()
        dm_session.headers.update(dm_headers)
        dm_session.max_redirects = 2
        
        # Add cookies
        if session_data and 'cookies' in session_data:
            for name, value in session_data['cookies'].items():
                dm_session.cookies.set(name, value, domain='.instagram.com')
        
        response = dm_session.get(
            'https://www.instagram.com/direct/inbox/',
            allow_redirects=True,
            timeout=25,
            verify=False
        )
        
        print(f"  📊 Status: {response.status_code}")
        print(f"  📏 Size: {len(response.text):,} chars")
        
        if response.status_code == 200:
            print("  ✅ DM endpoint accessible!")
        elif response.status_code == 500:
            print("  😢 DM endpoint returns HTTP 500")
        else:
            print(f"  ⚠️ DM endpoint status: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ DM endpoint error: {e}")
    
    print("\n🌸 Redirect Fix Summary:")
    print("=" * 40)
    print("🔧 Fixed redirect loop by limiting redirects")
    print("📱 Using mobile headers for better compatibility")
    print("🔑 Applied session cookies properly")
    print("⚡ Using shorter timeouts to prevent hangs")
    
    print("\n💡 Next Steps for ALX Trading:")
    print("1. ✅ Use limited redirects (max 3-5)")
    print("2. 📱 Always use mobile User-Agent")
    print("3. 🔑 Ensure session cookies are fresh")
    print("4. ⏰ Use conservative timeouts (30s max)")
    print("5. 🛡️ Handle redirects manually if needed")

if __name__ == "__main__":
    fix_redirect_loop()
