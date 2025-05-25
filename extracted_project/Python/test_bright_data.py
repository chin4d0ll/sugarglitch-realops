#!/usr/bin/env python3
"""
🌟 Bright Data Proxy Testing Script
ทดสอบการเชื่อมต่อ Bright Data proxy พร้อม features พิเศษ
"""

import json
import time
from modules.proxy_manager import ProxyManager

def test_bright_data_proxy():
    """ทดสอบ Bright Data proxy ทุก features"""
    
    print("🌟 BRIGHT DATA PROXY TESTING")
    print("=" * 60)
    
    # สร้าง ProxyManager instance
    proxy_manager = ProxyManager()
    
    print("📋 Current Configuration:")
    print(f"   • Enabled: {proxy_manager.enabled}")
    print(f"   • Host: {proxy_manager.proxy_host}")
    print(f"   • Port: {proxy_manager.proxy_port}")
    print(f"   • User: {proxy_manager.proxy_user}")
    print(f"   • Pass: {'*' * len(proxy_manager.proxy_pass) if proxy_manager.proxy_pass else 'Not set'}")
    print()
    
    if not proxy_manager.enabled:
        print("❌ Proxy is disabled. Please enable it in proxy_config.json")
        return
    
    # Test 1: Basic connection
    print("🔍 Test 1: Basic Connection")
    print("-" * 40)
    if proxy_manager.test_connection():
        print("✅ Basic connection successful!\n")
    else:
        print("❌ Basic connection failed!\n")
        return
    
    # Test 2: Bright Data specific features
    print("🌟 Test 2: Bright Data Features")
    print("-" * 40)
    if hasattr(proxy_manager, 'test_bright_data_features'):
        proxy_manager.test_bright_data_features()
    else:
        print("   ⚠️ Bright Data features not available in current ProxyManager")
    
    # Test 3: Instagram compatibility
    print("\n📱 Test 3: Instagram API Compatibility")
    print("-" * 40)
    test_instagram_compatibility(proxy_manager)
    
    # Test 4: Performance test
    print("\n⚡ Test 4: Performance Test")
    print("-" * 40)
    test_performance(proxy_manager)
    
    print("\n" + "=" * 60)
    print("✨ Bright Data testing completed!")

def test_instagram_compatibility(proxy_manager):
    """ทดสอบความเข้ากันได้กับ Instagram"""
    try:
        # ใช้ session ปกติหรือ Bright Data session
        if hasattr(proxy_manager, 'get_bright_data_session'):
            session = proxy_manager.get_bright_data_session(country="US")
        else:
            session = proxy_manager.get_session()
        
        # ทดสอบเข้า Instagram homepage
        print("   🔍 Testing Instagram homepage access...")
        
        # Instagram-like headers
        headers = {
            'User-Agent': 'Instagram 219.0.0.12.117 Android',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'X-IG-App-ID': '936619743392459',
        }
        session.headers.update(headers)
        
        # Test Instagram homepage
        response = session.get('https://www.instagram.com/', timeout=20)
        
        if response.status_code == 200:
            print("   ✅ Instagram homepage accessible")
            if 'instagram' in response.text.lower():
                print("   ✅ Instagram content loaded correctly")
            else:
                print("   ⚠️ Instagram content may be blocked")
        else:
            print(f"   ❌ Instagram access failed (Status: {response.status_code})")
            
    except Exception as e:
        print(f"   ❌ Instagram compatibility test failed: {e}")

def test_performance(proxy_manager):
    """ทดสอบประสิทธิภาพของ proxy"""
    print("   🚀 Testing proxy performance...")
    
    times = []
    success_count = 0
    
    for i in range(5):
        try:
            start_time = time.time()
            if hasattr(proxy_manager, 'rotate_session'):
                session = proxy_manager.rotate_session()
            else:
                session = proxy_manager.get_session()
            response = session.get("https://httpbin.org/ip", timeout=15)
            end_time = time.time()
            
            if response.status_code == 200:
                success_count += 1
                response_time = end_time - start_time
                times.append(response_time)
                ip = response.json().get('origin', 'Unknown')
                print(f"   Request {i+1}: {response_time:.2f}s - IP: {ip} ✅")
            else:
                print(f"   Request {i+1}: Failed ❌")
                
        except Exception as e:
            print(f"   Request {i+1}: Error - {str(e)[:50]}... ❌")
    
    if times:
        avg_time = sum(times) / len(times)
        print(f"\n   📊 Performance Results:")
        print(f"      • Success rate: {success_count}/5 ({success_count*20}%)")
        print(f"      • Average response time: {avg_time:.2f}s")
        print(f"      • Fastest: {min(times):.2f}s")
        print(f"      • Slowest: {max(times):.2f}s")
    else:
        print("   ❌ No successful requests for performance analysis")

def show_bright_data_tips():
    """แสดงเทคนิคการใช้ Bright Data"""
    print("\n💡 BRIGHT DATA OPTIMIZATION TIPS:")
    print("=" * 60)
    
    tips = [
        "🌍 ใช้ geo-targeting เพื่อหลีกเลี่ยง rate limiting",
        "🔄 Rotate sessions บ่อยๆ เพื่อป้องกันการ block",
        "⏱️ เพิ่ม delay ระหว่าง requests (แนะนำ 3-5 วินาที)",
        "📱 ใช้ mobile User-Agent สำหรับ Instagram",
        "🍪 จัดการ cookies อย่างระมัดระวัง",
        "📊 Monitor success rate และปรับ strategy",
        "🚫 หลีกเลี่ยงการส่ง request มากเกินไป",
        "🔍 ใช้ sticky sessions สำหรับ login flows"
    ]
    
    for tip in tips:
        print(f"   {tip}")
    
    print(f"\n📖 Configuration Example:")
    print(f'   {{"country": "US", "city": "newyork", "session": "sticky"}}')

def create_optimized_config():
    """สร้าง config ที่เหมาะสมสำหรับ Instagram brute force"""
    
    optimized_config = {
        "enabled": True,
        "host": "brd.superproxy.io",
        "port": 22225,
        "username": "brd-customer-YOUR_CUSTOMER_ID-zone-YOUR_ZONE",
        "password": "YOUR_PASSWORD",
        "rotation": {
            "enable_country_rotation": True,
            "countries": ["US", "GB", "CA", "AU", "DE"],
            "session_duration": 600,
            "max_requests_per_session": 50
        },
        "instagram_optimized": {
            "user_agents": [
                "Instagram 219.0.0.12.117 Android",
                "Instagram 218.0.0.26.114 Android",
                "Instagram 217.0.0.15.114 Android"
            ],
            "request_delay": 5,
            "retry_count": 3,
            "timeout": 30
        }
    }
    
    print("\n📝 Optimized Configuration Template:")
    print("=" * 60)
    print(json.dumps(optimized_config, indent=2))
    
    # Save template
    with open('proxy_config_optimized_template.json', 'w') as f:
        json.dump(optimized_config, f, indent=2)
    
    print(f"\n💾 Template saved to: proxy_config_optimized_template.json")

if __name__ == "__main__":
    print("🌟 Bright Data Proxy Testing Tool")
    print("เครื่องมือทดสอบ proxy สำหรับ Instagram brute force")
    print()
    
    test_bright_data_proxy()
    show_bright_data_tips()
    create_optimized_config()
    
    print("\n✨ Ready for Instagram brute force with Bright Data!")
    print("พร้อมใช้งาน brute force Instagram ด้วย Bright Data proxy!")
