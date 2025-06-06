#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ Quick Fix สำหรับ GitHub Codespace
แก้ไขปัญหาใน 1 นาที!
"""

import asyncio
import aiohttp
import json
import os
import sys
from pathlib import Path

async def quick_test():
    """⚡ ทดสอบเร็วๆ ว่า Codespace ใช้งานได้มั้ย"""
    print("🌸 Quick Codespace Test for chin4d0ll")
    print("=" * 40)
    
    # Test 1: Environment
    print("🔍 Environment Check:")
    print(f"  Python: {sys.version.split()[0]} ✅")
    print(f"  Platform: {sys.platform} ✅")
    print(f"  Working Dir: {os.getcwd()} ✅")
    
    # Test 2: Network
    print("\n🌐 Network Test:")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://httpbin.org/get', timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    print("  Basic HTTP: ✅")
                else:
                    print(f"  Basic HTTP: ❌ (status {response.status})")
    except Exception as e:
        print(f"  Basic HTTP: ❌ ({e})")
    
    # Test 3: Instagram accessibility
    print("\n📱 Instagram Test:")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.instagram.com/', 
                                 headers=headers, 
                                 timeout=aiohttp.ClientTimeout(total=15)) as response:
                print(f"  Instagram: Status {response.status} ({len(await response.text()):,} chars)")
                
                if response.status == 200:
                    print("  🎉 Instagram accessible from Codespace!")
                elif response.status == 429:
                    print("  ⚠️ Rate limited, but connection works!")
                else:
                    print(f"  ⚠️ Unexpected status: {response.status}")
                    
    except Exception as e:
        print(f"  Instagram: ❌ ({e})")
    
    # Test 4: Session file
    print("\n🔑 Session Test:")
    session_file = Path("session-alx.trading")
    if session_file.exists():
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
                
            if 'cookies' in session_data and 'sessionid' in session_data['cookies']:
                sessionid = session_data['cookies']['sessionid']
                print(f"  Session file: ✅ (ID: {sessionid[:10]}...)")
            else:
                print("  Session file: ⚠️ (no sessionid found)")
                
        except Exception as e:
            print(f"  Session file: ❌ ({e})")
    else:
        print("  Session file: ❌ (not found)")
    
    print("\n🎯 Recommendation:")
    print("  If Instagram is accessible, you can run the extractor!")
    print("  If rate limited, use longer delays between requests.")

if __name__ == "__main__":
    asyncio.run(quick_test())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ Quick Fix สำหรับ Instagram HTTP 500
แก้เร็วๆ ใน 2 นาที!
"""

import asyncio
import aiohttp
import random
import time

async def quick_500_fix():
    """⚡ แก้ปัญหา HTTP 500 แบบเร็ว"""
    
    print("🌸 Quick Instagram HTTP 500 Fix")
    print("⚡ แก้ไวไว 2 นาทีเสร็จ!")
    print("=" * 40)
    
    # Strategy 1: Mobile User Agent
    mobile_headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    print("📱 Strategy 1: Mobile User Agent")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.instagram.com/', 
                                 headers=mobile_headers, 
                                 timeout=aiohttp.ClientTimeout(total=30)) as response:
                print(f"  📊 Mobile: HTTP {response.status}")
                if response.status == 200:
                    print("  ✅ Mobile works! ใช้ mobile user agent ต่อไป")
                    return True
    except Exception as e:
        print(f"  ❌ Mobile failed: {e}")
    
    # Strategy 2: Different endpoint
    print("\n🔄 Strategy 2: Different Endpoint")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.instagram.com/accounts/login/', 
                                 headers=mobile_headers,
                                 timeout=aiohttp.ClientTimeout(total=30)) as response:
                print(f"  📊 Login page: HTTP {response.status}")
                if response.status == 200:
                    print("  ✅ Login page works! Server พร้อมใช้งาน")
                    return True
    except Exception as e:
        print(f"  ❌ Login page failed: {e}")
    
    # Strategy 3: Wait and retry
    print("\n⏰ Strategy 3: Wait and Retry")
    for i in range(1, 4):
        try:
            print(f"  🔄 Attempt {i}/3...")
            await asyncio.sleep(10)  # รอ 10 วินาที
            
            async with aiohttp.ClientSession() as session:
                async with session.get('https://www.instagram.com/', 
                                     headers=mobile_headers,
                                     timeout=aiohttp.ClientTimeout(total=45)) as response:
                    print(f"    📊 Retry {i}: HTTP {response.status}")
                    if response.status == 200:
                        print(f"  ✅ Success on retry {i}!")
                        return True
        except Exception as e:
            print(f"    ❌ Retry {i} failed: {e}")
    
    print("\n😢 All strategies failed")
    print("💡 Recommendations:")
    print("  1. Instagram servers มีปัญหาจริง รอ 30 นาทีแล้วลองใหม่")
    print("  2. ใช้ VPN เปลี่ยน IP address")
    print("  3. ลอง mobile hotspot แทน WiFi")
    print("  4. ตรวจสอบ session file ใหม่")
    
    return False

async def test_session_validity():
    """🔑 ทดสอบ session file"""
    print("\n🔑 Testing Session File...")
    
    try:
        import json
        from pathlib import Path
        
        session_files = [
            "session-alx.trading",
            "sessions/session-alx.trading",
            "/workspaces/sugarglitch-realops/sessions/session-alx.trading"
        ]
        
        for session_file in session_files:
            if Path(session_file).exists():
                print(f"✅ Found session: {session_file}")
                
                with open(session_file, 'r') as f:
                    data = json.load(f)
                
                if 'cookies' in data and 'sessionid' in data['cookies']:
                    sessionid = data['cookies']['sessionid']
                    print(f"✅ Valid session (length: {len(sessionid)})")
                    print(f"   SessionID preview: {sessionid[:10]}...{sessionid[-10:]}")
                    return True
                else:
                    print("❌ Invalid session format")
        
        print("❌ No valid session found")
        return False
        
    except Exception as e:
        print(f"❌ Session test failed: {e}")
        return False

async def advanced_instagram_test():
    """🌟 ทดสอบ Instagram แบบ advanced"""
    print("\n🌟 Advanced Instagram Test...")
    
    # ใช้ headers ที่เลียนแบบ real browser
    advanced_headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    }
    
    # ทดสอบหลาย endpoint
    test_urls = [
        ("Homepage", "https://www.instagram.com/"),
        ("Login", "https://www.instagram.com/accounts/login/"),
        ("API Test", "https://www.instagram.com/api/v1/"),
        ("Explore", "https://www.instagram.com/explore/")
    ]
    
    success_count = 0
    
    for name, url in test_urls:
        try:
            print(f"🔍 Testing {name}...")
            
            # รอสักหน่อยระหว่าง request
            if name != "Homepage":
                await asyncio.sleep(random.uniform(5, 10))
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, 
                                     headers=advanced_headers,
                                     timeout=aiohttp.ClientTimeout(total=60)) as response:
                    
                    print(f"  📊 {name}: HTTP {response.status} ({len(await response.text()):,} chars)")
                    
                    if response.status == 200:
                        success_count += 1
                        print(f"  ✅ {name} accessible!")
                    elif response.status == 429:
                        print(f"  ⚠️ {name} rate limited")
                    elif response.status == 500:
                        print(f"  ❌ {name} server error")
                    else:
                        print(f"  ⚠️ {name} status {response.status}")
                        
        except Exception as e:
            print(f"  ❌ {name} failed: {e}")
    
    print(f"\n📊 Results: {success_count}/{len(test_urls)} endpoints working")
    
    if success_count > 0:
        print("🎉 Good news! Instagram is partially accessible")
        print("💡 Try using different endpoints or mobile user agents")
        return True
    else:
        print("😢 No endpoints accessible")
        print("💡 Instagram may be having server issues")
        return False

async def main():
    """🚀 Main quick fix function"""
    print("🌸 Instagram HTTP 500 Quick Fixer")
    print("💖 Made with love for chin4d0ll")
    print("=" * 50)
    
    try:
        # Test 1: Quick fix strategies
        print("⚡ Running quick fix strategies...")
        if await quick_500_fix():
            print("\n🎉 Quick fix successful!")
            return
        
        # Test 2: Session validation
        print("\n🔑 Checking session...")
        session_valid = await test_session_validity()
        
        # Test 3: Advanced testing
        print("\n🌟 Running advanced tests...")
        if await advanced_instagram_test():
            print("\n✨ Some endpoints work! Try different strategies")
        else:
            print("\n😢 All tests failed")
            
            if not session_valid:
                print("\n💡 Primary issue: Invalid session")
                print("🔧 Fix: Create new session file")
            else:
                print("\n💡 Primary issue: Instagram server problems")
                print("🔧 Fix: Wait 30+ minutes or try VPN")
        
        # Final recommendations
        print("\n🎯 Final Recommendations:")
        print("1. 📱 Try mobile user agent: 'iPhone Safari'")
        print("2. ⏰ Use longer delays: 60+ seconds")
        print("3. 🔄 Try different endpoints first")
        print("4. 🌐 Consider using VPN/proxy")
        print("5. 🔑 Refresh session if needed")
        
    except KeyboardInterrupt:
        print("\n🛑 Quick fix interrupted")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(main())