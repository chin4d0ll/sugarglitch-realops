# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔥💀 ULTIMATE FAST EXTRACTOR - DEBUG VERSION 💀🔥
===============================================
สคริปต์เร็วและโหดที่สุด สำหรับ debug!
"""

import requests
import json
import time
from datetime import datetime

class FastExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15',
            'Accept': '*/*'
        })

    def display_banner(self):
        print("""
🔥💀 ULTIMATE FAST EXTRACTOR 💀🔥
==============================
⚡ READY FOR MAXIMUM SPEED ⚡
""")

    def test_connection(self):
        """Test basic connection"""
        try:
            response = self.session.get('https://httpbin.org/ip', timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Connection OK - IP: {data['origin']}")
                return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    def quick_instagram_test(self, username):
        """Quick Instagram test"""
        try:
            url = f'https://www.instagram.com/{username}/'
            response = self.session.get(url, timeout=15)
            print(f"📊 Instagram response: {response.status_code}")

            if response.status_code == 200:
                print(f"✅ Successfully accessed @{username}")
                # Look for basic data
                if '"username":"' in response.text:
                    print("✅ Found username data in response")
                if '"biography":"' in response.text:
                    print("✅ Found biography data")
                return True
            else:
                print(f"⚠️ Response code: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def run_debug(self):
        """Run debug session"""
        self.display_banner()

        print("🔄 Testing basic connection...")
        if not self.test_connection():
            print("❌ Basic connection failed!")
            return

        print("\n🎯 Testing Instagram access...")
        targets = ['alx.trading', 'whatilove1728', 'instagram']

        for target in targets:
            print(f"\n🔍 Testing: @{target}")
            self.quick_instagram_test(target)
            time.sleep(2)  # Rate limiting

        print("\n🏁 Debug complete!")

if __name__ == "__main__":
    extractor = FastExtractor()
    extractor.run_debug()
