# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Simple Auto Session Extractor - Just One Test
เครื่องมือง่ายๆ ดึง session อัตโนมัติ แค่ทดสอบเดียว
"""

import json
import requests
import time
from datetime import datetime

def get_fresh_session_auto():
    """ดึง session ใหม่อัตโนมัติ"""

    print("🚀 AUTO SESSION EXTRACTOR - SIMPLE VERSION")
    print("="*50)

    # ใช้ Bright Data proxy credentials
    proxy_auth = "brd-customer-hl_63f0835e-zone-scraping_agent:o5wnk3ws1r04"
    proxy_host = "brd.superproxy.io:22225"

    proxies = {
        'http': f'http://{proxy_auth}@{proxy_host}',
        'https': f'http://{proxy_auth}@{proxy_host}'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        print("📡 Testing connection with Bright Data...")

        # ทดสอบการเชื่อมต่อก่อน
        test_response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=10)
        if test_response.status_code == 200:
            ip_info = test_response.json()
            print(f"✅ Connected! IP: {ip_info.get('origin', 'unknown')}")
        else:
            print(f"❌ Connection failed: {test_response.status_code}")
            return None

        # พยายามดึง Instagram page ผ่าน proxy
        print("📱 Accessing Instagram...")
        ig_response = requests.get('https://www.instagram.com/', proxies=proxies, headers=headers, timeout=15)

        if ig_response.status_code == 200:
            print("✅ Instagram accessible")

            # พยายามหา sessionid ใน response headers หรือ cookies
            if ig_response.cookies:
                session_cookies = {}
                for cookie in ig_response.cookies:
                    session_cookies[cookie.name] = cookie.value
                    print(f"🍪 Found cookie: {cookie.name}")

                if session_cookies:
                    # สร้าง session data
                    session_data = {
                        'sessionid': session_cookies.get('sessionid', ''),
                        'csrftoken': session_cookies.get('csrftoken', ''),
                        'mid': session_cookies.get('mid', ''),
                        'target': 'alx.trading',
                        'created_at': datetime.now().isoformat(),
                        'status': 'auto-extracted',
                        'method': 'bright-data-proxy'
                    }

                    # บันทึกลงไฟล์
                    with open('tools/session_alx_trading.json', 'w') as f:
                        json.dump(session_data, f, indent=2)

                    print("✅ Session saved!")
                    return session_data

            print("ℹ️ No cookies found in response")

        else:
            print(f"❌ Instagram access failed: {ig_response.status_code}")

    except Exception as e:
        print(f"❌ Error: {e}")

    return None

def main():
    """Main function - แค่ทดสอบเดียว"""
    session = get_fresh_session_auto()

    if session:
        print("\n🎉 SUCCESS!")
        print(f"Session ID: {session.get('sessionid', 'N/A')[:20]}...")
    else:
        print("\n❌ FAILED - No session extracted")
        print("💡 Try manual method instead")

if __name__ == "__main__":
    main()
