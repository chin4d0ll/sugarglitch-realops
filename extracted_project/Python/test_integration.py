#!/usr/bin/env python3
"""
🔥 ULTIMATE SYSTEM INTEGRATION TEST 🔥
Test the complete Instagram brute force system

This script tests:
- Virtual display setup
- Browser automation
- Proxy integration
- Session extraction
- Error handling
"""

import os
import sys
import json
import time
import logging
from datetime import datetime

# Add modules path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from ultimate_browser_manager import UltimateBrowserManager
from ultimate_proxy_manager import UltimateProxyManager

def test_virtual_display():
    """Test virtual display setup"""
    print("🖥️ Testing virtual display setup...")
    
    try:
        manager = UltimateBrowserManager(debug=True)
        success = manager.setup_virtual_display()
        
        if success:
            print("✅ Virtual display setup successful")
            return True
        else:
            print("❌ Virtual display setup failed")
            return False
            
    except Exception as e:
        print(f"❌ Virtual display test error: {e}")
        return False

def test_proxy_manager():
    """Test proxy manager functionality"""
    print("🌐 Testing proxy manager...")
    
    try:
        proxy_manager = UltimateProxyManager()
        
        # Test proxy retrieval
        proxy = proxy_manager.get_next_proxy()
        
        if proxy:
            print(f"✅ Proxy manager working - Got proxy: {proxy.get('endpoint', 'Unknown')}")
            return True
        else:
            print("❌ Proxy manager failed to provide proxy")
            return False
            
    except Exception as e:
        print(f"❌ Proxy manager test error: {e}")
        return False

def test_browser_creation():
    """Test browser creation with proxy"""
    print("🌍 Testing browser creation...")
    
    browser_manager = None
    
    try:
        # Get proxy
        proxy_manager = UltimateProxyManager()
        proxy_config = proxy_manager.get_next_proxy()
        
        # Create browser manager
        browser_manager = UltimateBrowserManager(proxy_config=proxy_config, debug=True)
        
        # Setup display
        if not browser_manager.setup_virtual_display():
            print("❌ Failed to setup virtual display")
            return False
        
        # Create browser
        browser = browser_manager.create_browser_session()
        
        if browser:
            print("✅ Browser creation successful")
            
            # Test navigation
            print("📱 Testing Instagram navigation...")
            if browser_manager.navigate_to_instagram():
                print("✅ Instagram navigation successful")
                
                # Test session extraction
                print("🔐 Testing session extraction...")
                session_data = browser_manager.extract_session_data()
                
                if session_data and session_data.get('success'):
                    print(f"✅ Session extraction successful - {len(session_data.get('cookies', {}))} cookies found")
                else:
                    print("⚠️ Session extraction returned empty/invalid data")
                
                return True
            else:
                print("❌ Instagram navigation failed")
                return False
        else:
            print("❌ Browser creation failed")
            return False
            
    except Exception as e:
        print(f"❌ Browser test error: {e}")
        return False
        
    finally:
        if browser_manager:
            browser_manager.cleanup()

def test_login_attempt():
    """Test actual login attempt (with dummy credentials)"""
    print("🔑 Testing login attempt...")
    
    browser_manager = None
    
    try:
        # Get proxy
        proxy_manager = UltimateProxyManager()
        proxy_config = proxy_manager.get_next_proxy()
        
        # Create browser manager
        browser_manager = UltimateBrowserManager(proxy_config=proxy_config, debug=True)
        
        # Setup display
        if not browser_manager.setup_virtual_display():
            print("❌ Failed to setup virtual display")
            return False
        
        # Create browser
        browser = browser_manager.create_browser_session()
        
        if not browser:
            print("❌ Failed to create browser")
            return False
        
        # Navigate to Instagram
        if not browser_manager.navigate_to_instagram():
            print("❌ Failed to navigate to Instagram")
            return False
        
        # Attempt login with dummy credentials
        print("🔐 Attempting login with test credentials...")
        dummy_username = "test_user_not_real"
        dummy_password = "test_password_123"
        
        login_result = browser_manager.perform_login(dummy_username, dummy_password)
        
        if login_result:
            print("⚠️ Login returned success (unexpected for dummy credentials)")
        else:
            print("✅ Login properly failed for dummy credentials")
        
        # Test session extraction regardless
        session_data = browser_manager.extract_session_data()
        
        if session_data:
            print(f"✅ Session extraction working - {len(session_data.get('cookies', {}))} cookies found")
        else:
            print("❌ Session extraction failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Login test error: {e}")
        return False
        
    finally:
        if browser_manager:
            browser_manager.cleanup()

def test_ultimate_engine():
    """Test the ultimate engine with safe mode"""
    print("🔥 Testing Ultimate Instagram Engine...")
    
    try:
        from ultimate_instagram_engine import UltimateInstagramEngine
        
        # Create test config
        test_config = {
            "max_threads": 1,
            "delay_between_attempts": (1, 2),
            "max_attempts_per_proxy": 5,
            "debug": True,
            "session_validation": {
                "check_profile_access": False,  # Disable for testing
                "check_feed_access": False,     # Disable for testing
                "verify_username": False        # Disable for testing
            }
        }
        
        # Save test config
        with open('test_config.json', 'w') as f:
            json.dump(test_config, f, indent=2)
        
        # Create test targets and passwords
        with open('test_targets.txt', 'w') as f:
            f.write('test_user_not_real\n')
        
        with open('test_passwords.txt', 'w') as f:
            f.write('test_password_123\n')
        
        # Create engine
        engine = UltimateInstagramEngine(config_file='test_config.json')
        
        print("✅ Ultimate Engine created successfully")
        
        # Test loading
        targets = engine.load_targets('test_targets.txt')
        passwords = engine.load_passwords('test_passwords.txt')
        
        if targets and passwords:
            print("✅ Target and password loading successful")
        else:
            print("❌ Failed to load targets or passwords")
            return False
        
        print("✅ Ultimate Engine integration test passed")
        return True
        
    except Exception as e:
        print(f"❌ Ultimate Engine test error: {e}")
        return False

def run_complete_test():
    """Run complete system test"""
    print("🔥" * 50)
    print("🔥 ULTIMATE INSTAGRAM SYSTEM INTEGRATION TEST 🔥")
    print("🔥" * 50)
    print()
    
    tests = [
        ("Virtual Display", test_virtual_display),
        ("Proxy Manager", test_proxy_manager),
        ("Browser Creation", test_browser_creation),
        ("Login Attempt", test_login_attempt),
        ("Ultimate Engine", test_ultimate_engine)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"🧪 RUNNING TEST: {test_name}")
        print('='*60)
        
        start_time = time.time()
        success = test_func()
        end_time = time.time()
        
        results.append({
            'name': test_name,
            'success': success,
            'duration': end_time - start_time
        })
        
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"\n🏁 {test_name}: {status} ({end_time - start_time:.1f}s)")
    
    # Summary
    print("\n" + "🔥" * 60)
    print("🔥 TEST SUMMARY")
    print("🔥" * 60)
    
    passed = sum(1 for r in results if r['success'])
    total = len(results)
    
    for result in results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"{status} {result['name']} ({result['duration']:.1f}s)")
    
    print(f"\n🎯 TOTAL: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! System is ready for attack!")
    else:
        print("⚠️ Some tests failed. Check configuration before attacking.")
    
    # Save test results
    test_results = {
        'timestamp': datetime.now().isoformat(),
        'total_tests': total,
        'passed_tests': passed,
        'failed_tests': total - passed,
        'success_rate': passed / total * 100,
        'results': results
    }
    
    os.makedirs('test_output', exist_ok=True)
    with open('test_output/integration_test_results.json', 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\n📊 Test results saved to test_output/integration_test_results.json")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_complete_test()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n❌ Critical test error: {e}")
        exit(1)
