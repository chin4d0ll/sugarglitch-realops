#!/usr/bin/env python3
"""
🔥 TESTING REAL PROXY CONNECTION 🔥
Testing Bright Data proxy credentials
"""

import urllib.request
import ssl

def test_proxy_connection():
    proxy = 'http://brd-customer-hl_63f0835e-zone-mobile:fl13j3qcjvqh@brd.superproxy.io:33335'
    url = 'https://geo.brdtest.com/welcome.txt?product=mobile&method=native'

    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({'https': proxy, 'http': proxy}),
        urllib.request.HTTPSHandler(context=ssl._create_unverified_context())
    )

    try:
        print("🔥 TESTING BRIGHT DATA PROXY...")
        response = opener.open(url).read().decode()
        print("✅ PROXY CONNECTION SUCCESS!")
        print(f"Response: {response}")
        return True
    except Exception as e:
        print(f"❌ Proxy Error: {e}")
        return False

if __name__ == "__main__":
    test_proxy_connection()
