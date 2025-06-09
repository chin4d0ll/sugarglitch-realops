#!/usr/bin/env python3
"""
Simple Network Test with Built-in Modules Only
"""

import urllib.request
import urllib.error
import socket
import time

def simple_network_test():
    print("🌐 Simple Network Connectivity Test")
    print("=" * 40)
    
    # Test 1: DNS Resolution
    print("\n1️⃣ Testing DNS resolution...")
    try:
        ip = socket.gethostbyname('www.instagram.com')
        print(f"✅ instagram.com → {ip}")
    except Exception as e:
        print(f"❌ DNS failed: {e}")
        return
    
    # Test 2: Basic HTTP connection
    print("\n2️⃣ Testing basic HTTP connection...")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15'
        }
        req = urllib.request.Request('https://www.instagram.com/', headers=headers)
        response = urllib.request.urlopen(req, timeout=15)
        status = response.getcode()
        print(f"📱 Instagram Status: {status}")
        
        if status == 200:
            print("✅ Instagram is reachable")
        else:
            print(f"🟡 Instagram returned status {status}")
            
    except urllib.error.HTTPError as e:
        print(f"🟡 HTTP Error: {e.code} - {e.reason}")
        if e.code in [301, 302]:
            print("ℹ️  This is a redirect - normal for Instagram")
    except urllib.error.URLError as e:
        print(f"❌ URL Error: {e.reason}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
    
    # Test 3: Try Instagram API endpoint
    print("\n3️⃣ Testing Instagram API endpoint...")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15'
        }
        req = urllib.request.Request('https://i.instagram.com/api/v1/', headers=headers)
        response = urllib.request.urlopen(req, timeout=10)
        status = response.getcode()
        print(f"🔌 API Status: {status}")
    except urllib.error.HTTPError as e:
        print(f"🟡 API HTTP Error: {e.code} - {e.reason}")
    except Exception as e:
        print(f"❌ API Error: {e}")

if __name__ == "__main__":
    simple_network_test()
