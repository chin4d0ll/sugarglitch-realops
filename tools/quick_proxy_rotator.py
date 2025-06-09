# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Quick Proxy Rotator - รันเร็ว ไม่ค้าง
"""
import requests
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def test_proxy_fast(proxy):
    """ทดสอบ proxy เร็วๆ"""
    try:
        proxies = {'http': proxy, 'https': proxy}
        response = requests.get('https://httpbin.org/ip',
                              proxies=proxies, timeout=3)
        if response.status_code == 200:
            return proxy
    except Exception:
        pass
    return None

def get_free_proxies():
    """ดึง free proxies เร็วๆ"""
    proxies = [
        "http://8.210.83.33:80",
        "http://47.74.152.29:8888",
        "http://43.134.68.153:3128",
        "http://47.88.3.19:8080",
        "http://8.134.140.146:8080",
        "http://43.157.8.79:8888",
        "http://47.113.90.161:83",
        "http://183.240.46.42:8080",
        "http://36.92.85.66:8080",
        "http://103.78.255.61:8080"
    ]
    return proxies

def update_proxies_fast():
    """อัปเดต proxies เร็วๆ"""
    print("🔄 Testing proxies quickly...")

    free_proxies = get_free_proxies()
    working_proxies = []

    # ทดสอบพร้อมกัน 5 ตัว
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(test_proxy_fast, proxy): proxy
                  for proxy in free_proxies}

        for future in as_completed(futures, timeout=5):
            result = future.result()
            if result:
                working_proxies.append(result)
                print(f"✅ Working: {result}")

            # เก็บแค่ 5 ตัวแรกที่ใช้ได้
            if len(working_proxies) >= 5:
                break

    if working_proxies:
        try:
            os.makedirs('config', exist_ok=True)
            with open('config/proxies.json', 'w') as f:
                json.dump(working_proxies, f, indent=2)
            print(f"✅ Updated {len(working_proxies)} working proxies!")
        except Exception as e:
            print(f"❌ Failed to save: {e}")
    else:
        print("❌ No working proxies found")

def main():
    print("⚡ QUICK PROXY ROTATOR - NO HANG!")
    print("="*40)
    update_proxies_fast()

if __name__ == "__main__":
    main()
