from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3

import json
import requests

print("🚀 Simple Proxy Test")

# โหลด config
with open('proxy_config_simple.json') as f:
    config = json.load(f)

print(f"Config type: {config['proxy_type']}")

# ทดสอบแบบไม่ใช้ proxy ก่อน
try:
    print("\n📡 Testing direct connection...")
    response = requests.get('https://httpbin.org/ip', timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Direct IP: {data['origin']}")
except Exception as e:
    print(f"❌ Direct connection failed: {e}")

# ทดสอบ free proxy
free_proxies = config.get('free_proxies', [])
print(f"\n🔄 Testing {len(free_proxies)} free proxies...")

for i, proxy in enumerate(free_proxies):
    try:
        if proxy.get('username'):
            proxy_url = f"http://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"
        else:
            proxy_url = f"http://{proxy['host']}:{proxy['port']}"
        
        proxies = {'http': proxy_url, 'https': proxy_url}
        
        print(f"Testing proxy {i+1}: {proxy['host']}:{proxy['port']}")
        response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Proxy {i+1} works: {data['origin']}")
        else:
            print(f"❌ Proxy {i+1} HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Proxy {i+1} failed: {e}")

print("\n✅ Test completed")
