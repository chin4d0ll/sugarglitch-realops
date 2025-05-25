#!/usr/bin/env python3
"""
🧪 Test Updated Bright Data Proxy
ทดสอบการเชื่อมต่อ proxy ที่อัปเดตแล้ว
"""

import requests
import json
from requests.auth import HTTPProxyAuth

def test_proxy_direct():
    """ทดสอบ proxy โดยตรง"""
    print("🌐 Testing Bright Data Scraping Browser Proxy...")
    print("=" * 50)
    
    # ข้อมูล proxy ใหม่
    proxy_host = "brd.superproxy.io"
    proxy_port = "9222"
    proxy_user = "brd-customer-hl_63f0835e-zone-scraping_browser"
    proxy_pass = "59m84ggoef95"
    
    # สร้าง proxy URL
    proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
    
    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }
    
    print(f"Proxy Host: {proxy_host}:{proxy_port}")
    print(f"Proxy User: {proxy_user}")
    print(f"Testing connection...")
    
    try:
        # ทดสอบการเชื่อมต่อ
        session = requests.Session()
        session.proxies = proxies
        
        # เพิ่ม headers
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
        })
        
        # ทดสอบกับ httpbin
        print("\n1. Testing with httpbin.org...")
        response = session.get('https://httpbin.org/ip', timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! IP: {data.get('origin')}")
            
            # ทดสอบ geo info
            print("\n2. Getting geo information...")
            geo_response = session.get('https://httpbin.org/headers', timeout=15)
            if geo_response.status_code == 200:
                print("✅ Headers test passed")
                
            # ทดสอบกับ Instagram endpoint (ปลอดภัย)
            print("\n3. Testing Instagram endpoint...")
            ig_response = session.get('https://www.instagram.com/', timeout=30)
            if ig_response.status_code == 200:
                print("✅ Instagram endpoint accessible!")
                print(f"   Response size: {len(ig_response.content)} bytes")
            else:
                print(f"⚠️ Instagram returned status: {ig_response.status_code}")
                
            return True
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_proxy_manager():
    """ทดสอบ ProxyManager class"""
    print("\n🔧 Testing ProxyManager class...")
    print("=" * 50)
    
    try:
        from modules.proxy_manager import ProxyManager
        
        proxy_manager = ProxyManager()
        print(f"✅ ProxyManager loaded")
        print(f"   Host: {proxy_manager.proxy_host}:{proxy_manager.proxy_port}")
        print(f"   User: {proxy_manager.proxy_user}")
        print(f"   Enabled: {proxy_manager.enabled}")
        
        # ทดสอบการเชื่อมต่อ
        print("\nTesting connection...")
        success = proxy_manager.test_connection()
        
        if success:
            print("✅ ProxyManager test successful!")
            return True
        else:
            print("❌ ProxyManager test failed!")
            return False
            
    except Exception as e:
        print(f"❌ ProxyManager error: {e}")
        return False

def test_brute_force_integration():
    """ทดสอบการรวมกับ brute force"""
    print("\n🔓 Testing Brute Force Integration...")
    print("=" * 50)
    
    try:
        from brute_force import InstagramBruteForce
        
        brute_force = InstagramBruteForce()
        print("✅ BruteForce class loaded")
        
        # ทดสอบการสร้าง session
        print("Testing session creation...")
        session = brute_force.create_session_with_proxy()
        
        if session.proxies:
            print("✅ Proxy session created successfully!")
            print(f"   Proxy: {list(session.proxies.values())[0][:50]}...")
            
            # ทดสอบ session
            try:
                response = session.get('https://httpbin.org/ip', timeout=15)
                if response.status_code == 200:
                    ip_data = response.json()
                    print(f"✅ Session test successful! IP: {ip_data.get('origin')}")
                    return True
                else:
                    print(f"❌ Session test failed: {response.status_code}")
                    return False
            except Exception as e:
                print(f"❌ Session test error: {e}")
                return False
        else:
            print("❌ No proxy configured in session")
            return False
            
    except Exception as e:
        print(f"❌ BruteForce integration error: {e}")
        return False

def main():
    """ฟังก์ชันหลัก"""
    print("🧪 Bright Data Proxy Test Suite")
    print("Updated May 24, 2025")
    print("=" * 60)
    
    results = []
    
    # Test 1: Direct proxy test
    results.append(test_proxy_direct())
    
    # Test 2: ProxyManager test
    results.append(test_proxy_manager())
    
    # Test 3: BruteForce integration test
    results.append(test_brute_force_integration())
    
    # สรุปผลการทดสอบ
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    test_names = [
        "Direct Proxy Connection",
        "ProxyManager Class",
        "BruteForce Integration"
    ]
    
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{i+1}. {name}: {status}")
    
    total_passed = sum(results)
    print(f"\nOverall: {total_passed}/{len(results)} tests passed")
    
    if total_passed == len(results):
        print("\n🎉 All tests passed! Your proxy is ready for brute force!")
        print("\n🚀 Next steps:")
        print("1. Run: python run_advanced_brute.py")
        print("2. Or test specific features: python test_proxy_brute.py")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
        print("💡 Common issues:")
        print("   - Check proxy credentials")
        print("   - Verify network connectivity")
        print("   - Ensure IP is whitelisted")

if __name__ == "__main__":
    main()
