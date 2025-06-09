# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Quick Proxy Updater
Easily add working proxies to the system
"""

import json
import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class ProxyUpdater:
    def __init__(self):
        self.proxy_file = "config/proxies.json"
        self.working_proxies = []

        # Ensure config directory exists
        os.makedirs("config", exist_ok=True)

    def test_proxy(self, proxy):
        """Test if a proxy is working"""
        try:
            proxies = {'http': proxy, 'https': proxy}
            response = requests.get(
                'http://httpbin.org/ip',
                proxies=proxies,
                timeout=10
            )
            if response.status_code == 200:
                return proxy
        except Exception:
            pass
        return None

    def get_free_proxies(self):
        """Get list of free proxies to test"""
        print("🔍 Getting free proxy list...")

        # Basic free proxy list
        free_proxies = [
            "http://173.245.49.63:80",
            "http://172.67.254.149:80",
            "http://188.114.97.8:80",
            "http://185.238.228.26:80",
            "http://141.101.122.54:80",
            "http://172.67.131.199:80",
            "http://104.21.48.84:80",
            "http://162.159.242.1:80",
            "http://162.159.243.1:80",
            "http://104.16.132.229:80",
            "http://104.16.133.229:80",
            "http://108.162.192.148:80",
            "http://108.162.193.148:80",
            "http://141.101.120.54:80",
            "http://141.101.121.54:80",
            "http://172.67.182.72:80",
            "http://172.67.183.72:80",
            "http://188.114.96.8:80",
            "http://188.114.98.8:80",
            "http://203.32.121.97:80"
        ]

        return free_proxies

    def test_proxies_bulk(self, proxy_list):
        """Test multiple proxies concurrently"""
        print(f"🧪 Testing {len(proxy_list)} proxies...")

        working = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_proxy = {executor.submit(self.test_proxy, proxy): proxy for proxy in proxy_list}

            for future in as_completed(future_to_proxy):
                result = future.result()
                if result:
                    working.append(result)
                    print(f"✅ Working: {result}")
                else:
                    proxy = future_to_proxy[future]
                    print(f"❌ Failed: {proxy}")

        return working

    def add_custom_proxies(self):
        """Allow user to add custom proxies"""
        print("\n📝 ADD CUSTOM PROXIES")
        print("="*30)
        print("Enter proxies one by one (format: http://ip:port)")
        print("Press Enter with empty line to finish")

        custom_proxies = []
        while True:
            proxy = input("Proxy: ").strip()
            if not proxy:
                break

            if proxy.startswith('http://') or proxy.startswith('https://'):
                custom_proxies.append(proxy)
                print(f"Added: {proxy}")
            else:
                print("❌ Invalid format. Use: http://ip:port")

        return custom_proxies

    def save_proxies(self, proxies):
        """Save working proxies to file"""
        try:
            with open(self.proxy_file, 'w') as f:
                json.dump(proxies, f, indent=2)
            print(f"💾 Saved {len(proxies)} proxies to {self.proxy_file}")
            return True
        except Exception as e:
            print(f"❌ Failed to save proxies: {e}")
            return False

    def load_current_proxies(self):
        """Load current proxy list"""
        try:
            if os.path.exists(self.proxy_file):
                with open(self.proxy_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return []

    def run(self):
        """Main execution"""
        print("🔧 PROXY UPDATER")
        print("="*40)

        current_proxies = self.load_current_proxies()
        print(f"Current proxies: {len(current_proxies)}")

        print("\nChoose option:")
        print("1. Test free proxy list")
        print("2. Add custom proxies")
        print("3. Test current proxies")
        print("4. Clear all proxies")

        choice = input("\nChoice (1-4): ").strip()

        if choice == '1':
            free_proxies = self.get_free_proxies()
            working = self.test_proxies_bulk(free_proxies)
            if working:
                self.save_proxies(working)
                print(f"\n🎉 Found {len(working)} working proxies!")
            else:
                print("\n❌ No working proxies found")

        elif choice == '2':
            custom = self.add_custom_proxies()
            if custom:
                print(f"\nTesting {len(custom)} custom proxies...")
                working = self.test_proxies_bulk(custom)
                if working:
                    # Add to existing proxies
                    all_proxies = current_proxies + working
                    self.save_proxies(all_proxies)
                    print(f"\n🎉 Added {len(working)} working proxies!")

        elif choice == '3':
            if current_proxies:
                working = self.test_proxies_bulk(current_proxies)
                self.save_proxies(working)
                print(f"\n📊 {len(working)}/{len(current_proxies)} proxies are working")
            else:
                print("❌ No proxies to test")

        elif choice == '4':
            self.save_proxies([])
            print("🗑️ All proxies cleared")

if __name__ == "__main__":
    updater = ProxyUpdater()
    updater.run()
