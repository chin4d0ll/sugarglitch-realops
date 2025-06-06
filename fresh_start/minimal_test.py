#!/usr/bin/env python3
"""
🎯 MINIMAL RATE LIMITING TEST
==========================
ทดสอบแค่ basic functionality 💖
"""

import requests
import time
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def minimal_cute_request(url):
    """Minimal version of cute_request for testing"""
    print(f"🔥 Making request to: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"✅ Response: {response.status_code} - {len(response.content)} bytes")
        return response
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("🌸✨ MINIMAL RATE LIMITING TEST ✨🌸")
    print("=" * 50)
    
    # Test basic request
    response = minimal_cute_request('https://httpbin.org/status/200')
    
    if response:
        print("🎉 Basic HTTP request works!")
    else:
        print("💥 Basic HTTP request failed!")
    
    # Test Instagram (should work without auth)
    print("\n💫 Testing Instagram (no auth)...")
    response = minimal_cute_request('https://www.instagram.com/')
    
    if response:
        print("🎉 Instagram accessible!")
        if 'login' in response.text.lower():
            print("📝 Login page detected (normal for no-auth)")
        else:
            print("📝 Different page content")
    else:
        print("💥 Instagram not accessible!")
    
    print("\n🌸 Minimal test completed! 🌸")

if __name__ == "__main__":
    main()
