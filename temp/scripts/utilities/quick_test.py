#!/usr/bin/env python3

print("🚀 Quick Proxy Test Started")

try:
    import requests
    print("✅ requests imported")
    
    # ทดสอบ direct connection
    print("📡 Testing direct connection...")
    response = requests.get('https://httpbin.org/ip', timeout=5)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Your IP: {data['origin']}")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except requests.exceptions.Timeout:
    print("❌ Connection timeout")
except requests.exceptions.ConnectionError:
    print("❌ Connection error")
except Exception as e:
    print(f"❌ Error: {e}")

print("✅ Basic test completed")

# ตอนนี้ลองทดสอบ proxy
print("\n🔄 Testing proxy...")

try:
    # ใช้ public proxy ทดสอบ
    test_proxy = "http://proxy.server:8080"  # placeholder
    print("Proxy test would go here...")
    
except Exception as e:
    print(f"Proxy test error: {e}")

print("✅ All tests completed")
