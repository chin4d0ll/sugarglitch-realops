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