#!/usr/bin/env python3
"""
Quick network connectivity test for Instagram
"""

import requests
import time
from datetime import datetime

def test_connectivity():
    print("🌐 NETWORK CONNECTIVITY TEST")
    print("=" * 40)
    
    try:
        print("📡 Testing basic internet connectivity...")
        response = requests.get('https://httpbin.org/get', timeout=10)
        print(f"✅ Basic internet: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Basic internet failed: {e}")
        return False
    
    try:
        print("📱 Testing Instagram access...")
        response = requests.get('https://www.instagram.com/', timeout=15)
        print(f"📊 Instagram: HTTP {response.status_code} | {len(response.content)} bytes")
        
        if response.status_code == 200:
            print("✅ Instagram is accessible!")
            return True
        else:
            print(f"⚠️ Instagram returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Instagram access failed: {e}")
        return False

if __name__ == "__main__":
    test_connectivity()
