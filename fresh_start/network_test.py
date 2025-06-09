# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Simple network connectivity test
"""

import requests
import json
from datetime import datetime

def test_network():
    """Test basic network connectivity"""
    print(f"🌐 Network Test - {datetime.now()}")
    print("=" * 50)

    try:
        # Test basic HTTP connection
        response = requests.get("https://httpbin.org/ip", timeout=10)
        print(f"✅ Internet connection: OK (Status: {response.status_code})")
        print(f"📱 Public IP: {response.json().get('origin', 'unknown')}")

        # Test Instagram basic page (should be less likely to rate limit)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        ig_response = requests.get("https://www.instagram.com/robots.txt",
                                 headers=headers, timeout=10)
        print(f"📸 Instagram connectivity: Status {ig_response.status_code}")

        if ig_response.status_code == 200:
            print("✅ Instagram is accessible")
        else:
            print(f"⚠️ Instagram returned: {ig_response.status_code}")

    except Exception as e:
        print(f"❌ Network error: {e}")

    print("\n🎯 Environment Status:")
    print("- Internet: Available" if response.status_code == 200 else "- Internet: Not Available")
    print("- Instagram: Accessible" if ig_response.status_code == 200 else "- Instagram: Limited")
    print(f"- Timestamp: {datetime.now()}")

if __name__ == "__main__":
    test_network()
