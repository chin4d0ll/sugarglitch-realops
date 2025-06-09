# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🎯 QUICK RATE LIMITING TEST
========================
แค่ทดสอบ cute_request function เฉยๆ 💖
"""

import sys
import os
sys.path.append('/workspaces/sugarglitch-realops/fresh_start/src')

from instagram_extractor import InstagramDMExtractor
import json
import logging

# Setup cute logging 💕
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def quick_test():
    print("🌸✨ QUICK RATE LIMITING TEST ✨🌸")
    print("=" * 50)

    # Load config
    config_path = '/workspaces/sugarglitch-realops/fresh_start/config/settings.json'
    with open(config_path) as f:
        config = json.load(f)

    print(f"💖 Target: {config['target_username']}")
    print(f"🍪 Session ID: {config['session_data']['sessionid'][:20]}...")

    # Create extractor
    extractor = InstagramDMExtractor(config)

    # Test cute_request with simple Instagram homepage
    print("\n💫 Testing cute_request with Instagram homepage...")

    try:
        response = extractor.cute_request('https://www.instagram.com/')

        if response:
            print(f"✅ SUCCESS! Status: {response.status_code}")
            print(f"📊 Response size: {len(response.content)} bytes")

            # Check if logged in
            if 'login' in response.url:
                print("❌ Redirected to login - session might be invalid")
            else:
                print("✅ No login redirect - session looks good!")

        else:
            print("❌ No response received")

    except Exception as e:
        print(f"💥 Error: {e}")

    print("\n🌸 Test completed! 🌸")

if __name__ == "__main__":
    quick_test()
