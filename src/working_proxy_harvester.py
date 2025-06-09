# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Working Proxy Harvester - เก็บ proxy ที่ใช้งานได้จริง
"""

import requests
import json
import time
import concurrent.futures
from itertools import islice

class WorkingProxyHarvester:
    def __init__(self):
        self.free_proxy_sources = [
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
            "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
            "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt"
        ]

    def fetch_proxies_from_sources(self):
        """ดึง proxy จากแหล่งต่างๆ"""
        all_proxies = []

        for source in self.free_proxy_sources:
            try:
                print(f"[HARVEST] Fetching from {source}")
                response = requests.get(source, timeout=10)
                if response.status_code == 200:
                    lines = response.text.strip().split('\n')
                    for line in lines:
                        line = line.strip()
                        if ':' in line and len(line.split(':')) == 2:
                            host, port = line.split(':')
                            if host and port.isdigit():
                                proxy_url = f"http://{host}:{port}"
                                all_proxies.append(proxy_url)

            except Exception as e:
                print(f"[HARVEST] Failed to fetch {source}: {e}")

        # Add manual TOR proxy
        all_proxies.append("socks5://127.0.0.1:9050")

        print(f"[HARVEST] Collected {len(all_proxies)} proxies total")
        return list(set(all_proxies))  # Remove duplicates

    def test_proxy(self, proxy):
        """ทดสอบ proxy ตัวเดียว"""
        try:
            # ลอง multiple test URLs
            test_urls = [
                "http://httpbin.org/ip",
                "https://httpbin.org/ip",
                "http://icanhazip.com",
                "https://api.ipify.org?format=json"
            ]

            proxies = {'http': proxy, 'https': proxy}

            for test_url in test_urls:
                try:
                    response = requests.get(test_url, proxies=proxies, timeout=5)
                    if response.status_code == 200:
                        if "httpbin.org" in test_url:
                            data = response.json()
                            return {"proxy": proxy, "ip": data.get("origin", "unknown")}
                        elif "ipify.org" in test_url:
                            data = response.json()
                            return {"proxy": proxy, "ip": data.get("ip", "unknown")}
                        else:
                            return {"proxy": proxy, "ip": response.text.strip()}
                except Exception:
                    continue

        except Exception as e:
            pass
        return None

    def test_proxies_parallel(self, proxy_list, max_workers=20, max_proxies=50):
        """ทดสอบ proxy หลายตัวพร้อมกัน"""
        print(f"[TEST] Testing {min(len(proxy_list), max_proxies)} proxies...")

        working_proxies = []
        test_list = list(islice(proxy_list, max_proxies))

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.test_proxy, test_list))

        for result in results:
            if result:
                working_proxies.append(result)
                print(f"[✓] {result['proxy']} -> {result['ip']}")

        print(f"[TEST] Found {len(working_proxies)} working proxies")
        return working_proxies

    def save_working_proxies(self, working_proxies, output_file="config/working_proxies.json"):
        """บันทึก proxy ที่ใช้งานได้"""
        try:
            import os
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            with open(output_file, 'w') as f:
                json.dump(working_proxies, f, indent=2)

            print(f"[SAVE] Saved {len(working_proxies)} working proxies to {output_file}")
            return True
        except Exception as e:
            print(f"[SAVE] Failed to save proxies: {e}")
            return False

def main():
    """หาและทดสอบ proxy ที่ใช้งานได้จริง"""
    harvester = WorkingProxyHarvester()

    # เก็บ proxy จากแหล่งต่างๆ
    all_proxies = harvester.fetch_proxies_from_sources()

    # ทดสอบ proxy
    working_proxies = harvester.test_proxies_parallel(all_proxies)

    # บันทึกผลลัพธ์
    if working_proxies:
        harvester.save_working_proxies(working_proxies)
        print(f"\n[SUCCESS] Found {len(working_proxies)} working proxies!")

        # แสดง proxy ที่ใช้งานได้
        for proxy_info in working_proxies[:10]:  # แสดง 10 ตัวแรก
            print(f"  {proxy_info['proxy']} -> {proxy_info['ip']}")
    else:
        print("\n[WARNING] No working proxies found!")

if __name__ == "__main__":
    main()
