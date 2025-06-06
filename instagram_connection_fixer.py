#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌸 Instagram Connection Fixer
แก้ปัญหา redirect loop และ connection issues
"""

import requests
import json
import time
from pathlib import Path

def fix_instagram_connection():
    """🔧 แก้ปัญหาการเชื่อมต่อ Instagram"""
    
    print("🌸 Instagram Connection Fixer")
    print("🔧 แก้ปัญหา redirect และ connection")
    print("=" * 50)
    
    # สร้าง session เพื่อจัดการ cookies และ redirects
    session = requests.Session()
    
    # ตั้งค่า headers ที่ Instagram ชอบ
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    })
    
    # โหลด session cookies
    session_file = Path("sessions/session-alx.trading")
    if session_file.exists():
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            if 'cookies' in session_data:
                # เพิ่ม cookies ใน session
                for name, value in session_data['cookies'].items():
                    session.cookies.set(name, value, domain='.instagram.com')
                print("✅ Session cookies loaded")
            
        except Exception as e:
            print(f"⚠️ Session load warning: {e}")
    
    # ทดสอบ connection แบบค่อยเป็นค่อยไป
    
    # Test 1: Basic connectivity
    print("\n🌐 Test 1: Basic connectivity...")
    try:
        response = session.get(
            'https://httpbin.org/get',
            timeout=10,
            allow_redirects=True
        )
        print(f"✅ Basic HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Basic HTTP failed: {e}")
        return
    
    # Test 2: Instagram homepage (ระวัง redirects)
    print("\n🏠 Test 2: Instagram homepage...")
    try:
        response = session.get(
            'https://www.instagram.com/',
            timeout=30,
            allow_redirects=True,
            max_redirects=10  # จำกัด redirects
        )
        
        print(f"📊 Homepage: HTTP {response.status_code}")
        print(f"📍 Final URL: {response.url}")
        print(f"📄 Content: {len(response.text):,} chars")
        
        if response.status_code == 200:
            print("✅ Homepage accessible!")
            
            # ตรวจสอบ content
            content = response.text.lower()
            if 'instagram' in content:
                print("🎯 Instagram content confirmed")
            
            if 'login' in response.url:
                print("🔑 Redirected to login (session may be expired)")
            else:
                print("✨ Not redirected to login (good sign!)")
            
            # บันทึกผลลัพธ์
            Path("data").mkdir(exist_ok=True)
            with open('data/homepage_fixed.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("💾 Saved to data/homepage_fixed.html")
            
        else:
            print(f"❌ Homepage failed: {response.status_code}")
            return
            
    except requests.exceptions.TooManyRedirects:
        print("❌ Too many redirects - Instagram is redirecting infinitely")
        print("💡 This might be a bot detection mechanism")
        return
    except Exception as e:
        print(f"❌ Homepage error: {e}")
        return
    
    # Test 3: Direct messages (ถ้า homepage ผ่าน)
    print("\n📬 Test 3: Direct messages...")
    time.sleep(5)  # รอ 5 วินาที
    
    try:
        response = session.get(
            'https://www.instagram.com/direct/inbox/',
            timeout=30,
            allow_redirects=True,
            max_redirects=5
        )
        
        print(f"📊 Direct: HTTP {response.status_code}")
        print(f"📍 Final URL: {response.url}")
        print(f"📄 Content: {len(response.text):,} chars")
        
        if response.status_code == 200:
            print("✅ Direct messages accessible!")
            
            # ตรวจหา DM indicators
            content = response.text.lower()
            dm_indicators = ['direct', 'message', 'inbox', 'thread', 'conversation']
            found = [ind for ind in dm_indicators if ind in content]
            
            if found:
                print(f"🎯 DM indicators found: {found}")
            
            # บันทึก
            with open('data/direct_fixed.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("💾 Saved to data/direct_fixed.html")
            
        elif response.status_code == 500:
            print("❌ Server error 500 - Instagram internal issue")
        else:
            print(f"❌ Direct messages failed: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Direct messages error: {e}")
    
    # Test 4: API endpoint (ถ้าทำได้)
    print("\n🔌 Test 4: API endpoint...")
    time.sleep(5)  # รอ 5 วินาที
    
    try:
        # เพิ่ม headers สำหรับ API
        api_headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'X-Instagram-AJAX': '1',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # เพิ่ม CSRF token ถ้ามี
        if 'csrftoken' in session.cookies:
            api_headers['X-CSRFToken'] = session.cookies['csrftoken']
        
        response = session.get(
            'https://www.instagram.com/api/v1/direct_v2/inbox/',
            headers=api_headers,
            timeout=30,
            allow_redirects=False  # API ไม่ควร redirect
        )
        
        print(f"📊 API: HTTP {response.status_code}")
        print(f"📄 Content: {len(response.text):,} chars")
        
        if response.status_code == 200:
            print("✅ API accessible!")
            
            try:
                api_data = response.json()
                print(f"🔌 Valid JSON with {len(api_data)} top-level keys")
                
                if 'inbox' in api_data:
                    inbox = api_data['inbox']
                    if 'threads' in inbox:
                        threads = inbox['threads']
                        print(f"📬 Found {len(threads)} DM threads!")
                        
                        # Show first few threads
                        for i, thread in enumerate(threads[:3]):
                            if 'thread_title' in thread:
                                title = thread['thread_title']
                                print(f"  Thread {i+1}: {title}")
                
                # บันทึก API response
                with open('data/api_fixed.json', 'w', encoding='utf-8') as f:
                    json.dump(api_data, f, ensure_ascii=False, indent=2)
                print("💾 Saved to data/api_fixed.json")
                
            except json.JSONDecodeError:
                print("⚠️ API response is not JSON")
                with open('data/api_fixed.txt', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print("💾 Saved as text to data/api_fixed.txt")
        
        elif response.status_code == 403:
            print("❌ API Forbidden - need valid session or CSRF")
        elif response.status_code == 404:
            print("❌ API Not Found - endpoint may be wrong")
        else:
            print(f"❌ API failed: {response.status_code}")
    
    except Exception as e:
        print(f"❌ API error: {e}")
    
    # สรุปผล
    print("\n🎯 Connection Test Summary:")
    print("=" * 30)
    print("📁 Check data/ folder for saved responses")
    print("💡 If homepage works but DMs don't, session might need refresh")
    print("🔧 If APIs work, you can extract DM data programmatically")

if __name__ == "__main__":
    fix_instagram_connection()
