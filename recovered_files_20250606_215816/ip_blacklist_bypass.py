# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔥💀 IP BLACKLIST BYPASS SOLUTION 💀🔥
=====================================
Advanced solution for Instagram IP blacklist bypass

This script provides multiple approaches to bypass Instagram's IP blacklist:
1. Proxy rotation using free proxies
2. Tor network integration
3. VPN-like IP rotation
4. Session regeneration with new IP
"""

import requests
import json
import time
import random
import subprocess
import os
from typing import List, Dict, Optional
import threading
from concurrent.futures import ThreadPoolExecutor

class IPBlacklistBypass:
    """🚀 Advanced IP Blacklist Bypass System"""

    def __init__(self):
        self.working_proxies = []
        self.current_ip = None
        self.instagram_accessible = False

    def get_current_ip(self) -> Optional[str]:
        """Get current external IP address"""
        try:
            response = requests.get("https://httpbin.org/ip", timeout=10)
            if response.status_code == 200:
                self.current_ip = response.json().get('origin', 'unknown')
                print(f"🌍 Current IP: {self.current_ip}")
                return self.current_ip
        except Exception as e:
            print(f"❌ Failed to get IP: {e}")
        return None

    def test_instagram_access(self, proxy: str = None) -> bool:
        """Test if Instagram is accessible with current IP/proxy"""
        try:
            session = requests.Session()

            if proxy:
                session.proxies = {
                    'http': proxy,
                    'https': proxy
                }
                print(f"🌐 Testing with proxy: {proxy}")

            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
            })

            # Test Instagram accessibility
            response = session.get("https://www.instagram.com/", timeout=15)

            if response.status_code == 200:
                if "blacklist" not in response.text.lower() and "blocked" not in response.text.lower():
                    print("✅ Instagram is accessible!")
                    self.instagram_accessible = True
                    return True
                else:
                    print("🚫 Instagram access blocked/blacklisted")
            else:
                print(f"❌ Instagram returned status: {response.status_code}")

        except Exception as e:
            print(f"❌ Instagram test failed: {e}")

        self.instagram_accessible = False
        return False

    def fetch_free_proxies(self) -> List[str]:
        """Fetch free proxies from multiple sources"""
        print("🔍 Fetching free proxies...")

        proxies = []
        sources = [
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt"
        ]

        for source in sources:
            try:
                print(f"   Fetching from: {source}")
                response = requests.get(source, timeout=15)
                if response.status_code == 200:
                    lines = response.text.strip().split('\n')
                    for line in lines[:20]:  # Limit for speed
                        line = line.strip()
                        if ':' in line and len(line.split(':')) == 2:
                            host, port = line.split(':')
                            if host and port.isdigit():
                                proxy_url = f"http://{host}:{port}"
                                proxies.append(proxy_url)

            except Exception as e:
                print(f"   ❌ Failed to fetch from {source}: {e}")

        print(f"📊 Collected {len(proxies)} proxies")
        return proxies

    def test_proxy_fast(self, proxy: str) -> Optional[str]:
        """Fast proxy test"""
        try:
            session = requests.Session()
            session.proxies = {'http': proxy, 'https': proxy}
            session.timeout = 5

            # Quick test
            response = session.get("http://httpbin.org/ip", timeout=5)
            if response.status_code == 200:
                ip_data = response.json()
                return ip_data.get('origin', 'unknown')
        except Exception:
            pass
        return None

    def find_working_proxies(self, proxy_list: List[str], max_workers: int = 10) -> List[Dict]:
        """Find working proxies using parallel testing"""
        print(f"🧪 Testing {len(proxy_list)} proxies with {max_workers} workers...")

        working_proxies = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all proxy tests
            future_to_proxy = {executor.submit(self.test_proxy_fast, proxy): proxy for proxy in proxy_list}

            for future in future_to_proxy:
                proxy = future_to_proxy[future]
                try:
                    result_ip = future.result(timeout=10)
                    if result_ip:
                        working_proxies.append({
                            'proxy': proxy,
                            'ip': result_ip
                        })
                        print(f"✅ Working: {proxy} -> {result_ip}")

                        # Stop after finding enough working proxies
                        if len(working_proxies) >= 5:
                            break

                except Exception as e:
                    pass

        self.working_proxies = working_proxies
        print(f"🎉 Found {len(working_proxies)} working proxies!")
        return working_proxies

    def test_proxy_instagram_access(self, proxy_info: Dict) -> bool:
        """Test if proxy can access Instagram"""
        proxy = proxy_info['proxy']
        print(f"🧪 Testing Instagram access via {proxy}...")

        return self.test_instagram_access(proxy)

    def find_instagram_bypass_proxy(self) -> Optional[Dict]:
        """Find a proxy that can bypass Instagram blacklist"""
        print("🎯 Finding Instagram bypass proxy...")

        # Get fresh proxies
        proxy_list = self.fetch_free_proxies()

        if not proxy_list:
            print("❌ No proxies available")
            return None

        # Find working proxies
        working_proxies = self.find_working_proxies(proxy_list[:50])  # Test first 50

        if not working_proxies:
            print("❌ No working proxies found")
            return None

        # Test Instagram access for each working proxy
        for proxy_info in working_proxies:
            if self.test_proxy_instagram_access(proxy_info):
                print(f"🎉 Found Instagram bypass proxy: {proxy_info['proxy']}")
                return proxy_info

        print("💔 No proxy can bypass Instagram blacklist")
        return None

    def setup_tor_proxy(self) -> bool:
        """Try to setup Tor proxy for IP rotation"""
        print("🧅 Setting up Tor proxy...")

        try:
            # Check if tor is installed
            result = subprocess.run(['which', 'tor'], capture_output=True, text=True)
            if result.returncode != 0:
                print("📦 Installing Tor...")
                subprocess.run(['sudo', 'apt', 'update'], check=True)
                subprocess.run(['sudo', 'apt', 'install', '-y', 'tor'], check=True)

            # Start tor service
            print("🚀 Starting Tor service...")
            subprocess.run(['sudo', 'service', 'tor', 'start'], check=True)

            # Test tor proxy
            time.sleep(5)  # Give tor time to start

            tor_proxy = "socks5://127.0.0.1:9050"

            # Test tor connection
            session = requests.Session()
            session.proxies = {'http': tor_proxy, 'https': tor_proxy}

            response = session.get("https://httpbin.org/ip", timeout=15)
            if response.status_code == 200:
                tor_ip = response.json().get('origin', 'unknown')
                print(f"🧅 Tor IP: {tor_ip}")

                # Test Instagram access via Tor
                if self.test_instagram_access(tor_proxy):
                    print("🎉 Tor can bypass Instagram blacklist!")
                    return True
                else:
                    print("❌ Tor cannot bypass Instagram blacklist")

        except subprocess.CalledProcessError as e:
            print(f"❌ Tor setup failed: {e}")
        except Exception as e:
            print(f"❌ Tor test failed: {e}")

        return False

    def try_ip_rotation_techniques(self) -> Dict:
        """Try various IP rotation techniques"""
        print("🔄 Trying IP rotation techniques...")

        results = {
            'original_ip': self.get_current_ip(),
            'instagram_accessible_direct': self.test_instagram_access(),
            'bypass_proxy': None,
            'tor_available': False,
            'recommendations': []
        }

        # If Instagram is accessible directly, no need for bypass
        if results['instagram_accessible_direct']:
            print("✅ Instagram is accessible directly - no bypass needed!")
            results['recommendations'].append("No bypass needed - direct access works")
            return results

        print("🚫 Instagram is blocked/blacklisted with current IP")

        # Try proxy bypass
        bypass_proxy = self.find_instagram_bypass_proxy()
        if bypass_proxy:
            results['bypass_proxy'] = bypass_proxy
            results['recommendations'].append(f"Use proxy: {bypass_proxy['proxy']}")

        # Try Tor
        if self.setup_tor_proxy():
            results['tor_available'] = True
            results['recommendations'].append("Use Tor proxy: socks5://127.0.0.1:9050")

        # Add general recommendations
        if not results['bypass_proxy'] and not results['tor_available']:
            results['recommendations'].extend([
                "Wait 24-48 hours for IP blacklist to clear",
                "Use VPN service to change IP address",
                "Contact Instagram support if account is legitimate",
                "Use mobile data instead of WiFi",
                "Try different network (different ISP)"
            ])

        return results

    def save_bypass_config(self, results: Dict):
        """Save bypass configuration for later use"""
        config_dir = "config"
        os.makedirs(config_dir, exist_ok=True)

        config_file = f"{config_dir}/bypass_config.json"

        bypass_config = {
            'timestamp': int(time.time()),
            'original_ip': results.get('original_ip'),
            'instagram_accessible_direct': results.get('instagram_accessible_direct', False),
            'bypass_proxy': results.get('bypass_proxy'),
            'tor_available': results.get('tor_available', False),
            'working_proxies': self.working_proxies[:10],  # Save top 10
            'recommendations': results.get('recommendations', [])
        }

        with open(config_file, 'w') as f:
            json.dump(bypass_config, f, indent=2)

        print(f"💾 Bypass config saved: {config_file}")
        return config_file

    def display_results(self, results: Dict):
        """Display bypass results"""
        print("\n" + "="*60)
        print("🎯 IP BLACKLIST BYPASS RESULTS")
        print("="*60)

        print(f"🌍 Original IP: {results.get('original_ip', 'unknown')}")
        print(f"📊 Instagram Direct Access: {'✅ Yes' if results.get('instagram_accessible_direct') else '❌ No'}")

        if results.get('bypass_proxy'):
            proxy_info = results['bypass_proxy']
            print(f"🌐 Bypass Proxy Found: ✅ {proxy_info['proxy']} -> {proxy_info['ip']}")
        else:
            print("🌐 Bypass Proxy Found: ❌ No")

        print(f"🧅 Tor Available: {'✅ Yes' if results.get('tor_available') else '❌ No'}")

        print("\n📋 RECOMMENDATIONS:")
        for i, rec in enumerate(results.get('recommendations', []), 1):
            print(f"   {i}. {rec}")

        print("="*60)

    def run_bypass_analysis(self):
        """Run complete bypass analysis"""
        print("🚀 Starting IP Blacklist Bypass Analysis...")
        print("="*50)

        # Get current status
        results = self.try_ip_rotation_techniques()

        # Display results
        self.display_results(results)

        # Save configuration
        config_file = self.save_bypass_config(results)

        print(f"\n💡 Next steps:")
        if results.get('bypass_proxy'):
            print("   1. Use the found bypass proxy in your extraction script")
            print("   2. Update extraction config with proxy settings")
        elif results.get('tor_available'):
            print("   1. Configure extraction script to use Tor proxy")
            print("   2. Use socks5://127.0.0.1:9050 as proxy")
        else:
            print("   1. Wait 24-48 hours for IP blacklist to clear")
            print("   2. Or use commercial VPN service")
            print("   3. Or try mobile data connection")

        return results
def main():
    """Main function"""
    print("🔥💀 IP BLACKLIST BYPASS SOLUTION 💀🔥")
    print("="*40)

    bypass = IPBlacklistBypass()
    results = bypass.run_bypass_analysis()

    return results
if __name__ == "__main__":
    main()