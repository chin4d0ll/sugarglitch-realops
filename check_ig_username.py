# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Check Instagram Username Format
"""

import requests
import json

def check_ig_username_variants():
    """Check different variants of the username"""

    username_variants = [
        "alx.trading",
        "alxtrading",
        "alx_trading",
        "alx-trading",
        "alxtrading_",
        "_alxtrading",
        "alx.trading_",
        "alx_trading_official"
    ]

    print("🔍 Checking Instagram username variants...")
    print("=" * 50)

    for username in username_variants:
        try:
            # Check if username exists by trying to access the profile page
            url = f"https://www.instagram.com/{username}/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                if "Page Not Found" not in response.text and "Sorry, this page isn't available" not in response.text:
                    print(f"✅ {username} - EXISTS (Status: {response.status_code})")

                    # Try to extract some basic info
                    if '"username":"' in response.text:
                        print(f"   📍 Profile appears to be active")

                else:
                    print(f"❌ {username} - NOT FOUND (Page shows not available)")
            else:
                print(f"❌ {username} - HTTP {response.status_code}")

        except Exception as e:
            print(f"❌ {username} - ERROR: {str(e)}")

    print("\n" + "=" * 50)
    print("📝 Note: Instagram usernames:")
    print("   - Cannot contain periods (.) in the middle")
    print("   - Can contain underscores (_)")
    print("   - Can contain periods only at the end")
    print("   - Must be lowercase")
    print("   - Cannot start with a period")

if __name__ == "__main__":
    check_ig_username_variants()
