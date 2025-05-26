from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
Quick proxy test script
ทดสอบการเชื่อมต่อ proxy
"""

import json
import requests
import time
from requests.auth import HTTPProxyAuth

def test_proxy_connection():
    """ทดสอบการเชื่อมต่อ proxy"""
    
    # โหลด config
    with open('proxy_config.json', 'r') as f:
        config = json.load(f)
    
    if not config.get('enabled'):
        print("❌ Proxy ไม่ได้เปิดใช้งาน")
        return False
    
    # ตั้งค่า proxy
    proxy_url = f"http://{config['proxy_user']}:{config['proxy_pass']}@{config['proxy_host']}:{config['proxy_port']}"
    
    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }
    
    print("🔍 กำลังทดสอบ proxy connection...")
    print(f"Host: {config['proxy_host']}:{config['proxy_port']}")
    
    try:
        # ทดสอบ IP
        response = requests.get(
            'https://httpbin.org/ip',
            proxies=proxies,
            timeout=config.get('connection_timeout', 30)
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Proxy ทำงานได้! IP: {data['origin']}")
            
            # ทดสอบ location
            geo_response = requests.get(
                'https://ipapi.co/json/',
                proxies=proxies,
                timeout=30
            )
            
            if geo_response.status_code == 200:
                geo_data = geo_response.json()
                print(f"📍 Location: {geo_data.get('city', 'Unknown')}, {geo_data.get('country_name', 'Unknown')}")
            
            return True
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

def test_proxy_rotation():
    """ทดสอบการหมุน proxy"""
    
    print("\n🔄 ทดสอบ proxy rotation...")
    
    with open('proxy_config.json', 'r') as f:
        config = json.load(f)
    
    if not config.get('rotation', {}).get('enabled'):
        print("❌ Proxy rotation ไม่ได้เปิดใช้งาน")
        return
    
    proxy_url = f"http://{config['proxy_user']}:{config['proxy_pass']}@{config['proxy_host']}:{config['proxy_port']}"
    proxies = {'http': proxy_url, 'https': proxy_url}
    
    ips = []
    for i in range(3):
        try:
            response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=30)
            if response.status_code == 200:
                ip = response.json()['origin']
                ips.append(ip)
                print(f"Request {i+1}: {ip}")
                time.sleep(2)
        except Exception as e:
            print(f"Request {i+1} failed: {e}")
    
    unique_ips = len(set(ips))
    print(f"\n📊 ได้ IP ที่แตกต่างกัน: {unique_ips}/{len(ips)}")

if __name__ == "__main__":
    print("🚀 เริ่มทดสอบ Proxy Configuration")
    print("=" * 50)
    
    if test_proxy_connection():
        test_proxy_rotation()
    
    print("\n✅ การทดสอบเสร็จสิ้น")
