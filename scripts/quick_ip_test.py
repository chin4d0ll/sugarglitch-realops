#!/usr/bin/env python3
"""
🔄 Quick IP Test
===============

Test current IP and Instagram access
"""

import requests
import subprocess


def get_current_ip():
    """ดู IP ปัจจุบัน"""
    try:
        print("🔍 Checking current IP...")
        response = requests.get('https://ifconfig.me', timeout=10)
        return response.text.strip()
    except Exception as e:
        print(f"❌ Error getting IP: {e}")
        try:
            response = requests.get('https://api.ipify.org', timeout=10)
            return response.text.strip()
        except Exception as e2:
            print(f"❌ Backup IP check failed: {e2}")
            return "Unknown"


def test_instagram_access():
    """ทดสอบการเข้า Instagram"""
    try:
        print("🧪 Testing Instagram access...")
        response = requests.get(
            'https://www.instagram.com/accounts/login/',
            timeout=15,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )

        if response.status_code == 200:
            return "✅ accessible"
        elif response.status_code == 429:
            return "🚨 rate_limited"
        else:
            return f"⚠️ http_{response.status_code}"
    except Exception as e:
        return f"❌ error: {str(e)[:50]}"


def main():
    print("🔄 Quick IP and Instagram Test")
    print("=" * 40)

    # Get current IP
    current_ip = get_current_ip()
    print(f"📍 Current IP: {current_ip}")

    # Test Instagram access
    status = test_instagram_access()
    print(f"📊 Instagram status: {status}")

    if "rate_limited" in status:
        print("\n🔄 Rate limited detected!")
        print("💡 Solutions:")
        print("   1. Use VPN")
        print("   2. Change network")
        print("   3. Wait 6-24 hours")
        print("   4. Use mobile data")
    elif "accessible" in status:
        print("\n🎉 Instagram accessible! Ready for attack!")
    else:
        print(f"\n⚠️ Unexpected status: {status}")


if __name__ == "__main__":
    main()
