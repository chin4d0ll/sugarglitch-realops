# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🌐 ADVANCED IP BLOCK BYPASS & RECOVERY SYSTEM 2025
==================================================
Comprehensive solution for Instagram IP blocking issues
Includes automated proxy rotation, VPN integration, and recovery strategies
"""

import time
import json
import random
import requests
import subprocess
import os
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class ProxyConfig:
    """Configuration for proxy settings"""
    proxy_type: str  # 'http', 'https', 'socks5'
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    country: Optional[str] = None

class AdvancedIPBypass:
    def __init__(self):
        self.working_proxies = []
        self.failed_proxies = []
        self.vpn_services = []
        self.last_block_time = None
        self.block_count = 0

        self.load_proxy_sources()
        self.load_vpn_configs()

    def load_proxy_sources(self):
        """Load proxy configurations from various sources"""
        # Free proxy APIs and sources
        self.proxy_sources = [
            {
                'name': 'ProxyList API',
                'url': 'https://api.proxyscrape.com/v2/',
                'params': {
                    'request': 'get',
                    'protocol': 'http',
                    'timeout': 10000,
                    'country': 'all',
                    'ssl': 'all',
                    'anonymity': 'all'
                }
            },
            {
                'name': 'Free Proxy List',
                'url': 'https://www.proxy-list.download/api/v1/get',
                'params': {
                    'type': 'http',
                    'anon': 'elite'
                }
            }
        ]

        # Load saved proxies
        try:
            with open('/workspaces/sugarglitch-realops/config/working_proxies.json', 'r') as f:
                saved_proxies = json.load(f)
                self.working_proxies.extend(saved_proxies.get('proxies', []))
        except Exception:
            pass

    def load_vpn_configs(self):
        """Load VPN service configurations"""
        self.vpn_services = [
            {
                'name': 'ExpressVPN',
                'command': 'expressvpn connect',
                'disconnect': 'expressvpn disconnect',
                'status': 'expressvpn status',
                'available': self.check_command_exists('expressvpn')
            },
            {
                'name': 'NordVPN',
                'command': 'nordvpn connect',
                'disconnect': 'nordvpn disconnect',
                'status': 'nordvpn status',
                'available': self.check_command_exists('nordvpn')
            },
            {
                'name': 'ProtonVPN',
                'command': 'protonvpn connect --fastest',
                'disconnect': 'protonvpn disconnect',
                'status': 'protonvpn status',
                'available': self.check_command_exists('protonvpn')
            },
            {
                'name': 'OpenVPN',
                'command': 'sudo openvpn --config',
                'disconnect': 'sudo killall openvpn',
                'status': 'pgrep openvpn',
                'available': self.check_command_exists('openvpn')
            }
        ]

    def check_command_exists(self, command):
        """Check if a command exists on the system"""
        try:
            subprocess.run(['which', command], capture_output=True, check=True)
            return True
        except Exception:
            return False

    def detect_current_ip(self):
        """Detect current public IP address"""
        ip_services = [
            'https://api.ipify.org',
            'https://ipinfo.io/ip',
            'https://icanhazip.com',
            'https://api.my-ip.io/ip'
        ]

        for service in ip_services:
            try:
                response = requests.get(service, timeout=10)
                if response.status_code == 200:
                    ip = response.text.strip()
                    return ip
            except Exception:
                continue

        return "Unknown"

    def test_instagram_access(self, proxy=None):
        """Test if Instagram is accessible"""
        try:
            proxies = proxy if proxy else None
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get('https://www.instagram.com/',
                                  headers=headers,
                                  proxies=proxies,
                                  timeout=15)

            if response.status_code == 200:
                # Check for block indicators
                block_indicators = [
                    "blocked your IP",
                    "rate limited",
                    "temporarily unavailable",
                    "suspicious activity"
                ]

                content = response.text.lower()
                for indicator in block_indicators:
                    if indicator in content:
                        return False, f"Block detected: {indicator}"

                return True, "Access successful"
            else:
                return False, f"HTTP {response.status_code}"

        except Exception as e:
            return False, f"Connection error: {e}"

    def fetch_fresh_proxies(self):
        """Fetch fresh proxies from online sources"""
        print("🔍 Fetching fresh proxies...")
        new_proxies = []

        for source in self.proxy_sources:
            try:
                print(f"  📡 Checking {source['name']}...")
                response = requests.get(source['url'], params=source.get('params'), timeout=15)

                if response.status_code == 200:
                    # Parse proxy list
                    proxies_text = response.text
                    proxy_lines = [line.strip() for line in proxies_text.split('\n') if line.strip()]

                    for line in proxy_lines[:20]:  # Limit to first 20
                        if ':' in line:
                            parts = line.split(':')
                            if len(parts) >= 2:
                                proxy_config = {
                                    'http': f'http://{parts[0]}:{parts[1]}',
                                    'https': f'http://{parts[0]}:{parts[1]}'
                                }
                                new_proxies.append(proxy_config)

                print(f"    ✅ Found {len(new_proxies)} proxies from {source['name']}")

            except Exception as e:
                print(f"    ❌ Failed to get proxies from {source['name']}: {e}")

        return new_proxies

    def test_proxies(self, proxies, max_test=10):
        """Test a list of proxies for Instagram access"""
        print(f"🧪 Testing {min(len(proxies), max_test)} proxies...")
        working = []

        for i, proxy in enumerate(proxies[:max_test]):
            print(f"  🔍 Testing proxy {i+1}/{min(len(proxies), max_test)}...", end='')

            success, message = self.test_instagram_access(proxy)

            if success:
                working.append(proxy)
                print(f" ✅ Working")
            else:
                print(f" ❌ Failed ({message})")

            time.sleep(1)  # Don't spam tests

        return working

    def rotate_ip_via_proxy(self):
        """Attempt to change IP via proxy rotation"""
        print("🔄 Attempting IP rotation via proxy...")

        # Try existing working proxies first
        if self.working_proxies:
            print(f"  📋 Testing {len(self.working_proxies)} known working proxies...")
            for proxy in self.working_proxies:
                success, message = self.test_instagram_access(proxy)
                if success:
                    print(f"  ✅ Found working proxy: {proxy}")
                    return proxy, "Existing proxy works"

        # Fetch and test new proxies
        fresh_proxies = self.fetch_fresh_proxies()
        if fresh_proxies:
            working_proxies = self.test_proxies(fresh_proxies)
            if working_proxies:
                best_proxy = working_proxies[0]

                # Save working proxies
                self.working_proxies.extend(working_proxies)
                self.save_working_proxies()

                print(f"  ✅ Found new working proxy: {best_proxy}")
                return best_proxy, "New proxy found"

        return None, "No working proxies found"

    def rotate_ip_via_vpn(self):
        """Attempt to change IP via VPN"""
        print("🌐 Attempting IP rotation via VPN...")

        available_vpns = [vpn for vpn in self.vpn_services if vpn['available']]

        if not available_vpns:
            print("  ❌ No VPN services available")
            return False, "No VPN services installed"

        for vpn in available_vpns:
            print(f"  🔧 Trying {vpn['name']}...")

            try:
                # Disconnect any existing connection
                subprocess.run(vpn['disconnect'], shell=True, capture_output=True)
                time.sleep(3)

                # Connect to VPN
                result = subprocess.run(vpn['command'], shell=True, capture_output=True)

                if result.returncode == 0:
                    time.sleep(10)  # Wait for connection to establish

                    # Test Instagram access
                    success, message = self.test_instagram_access()
                    if success:
                        new_ip = self.detect_current_ip()
                        print(f"  ✅ VPN connected successfully. New IP: {new_ip}")
                        return True, f"Connected via {vpn['name']}"

            except Exception as e:
                print(f"  ❌ Failed to connect via {vpn['name']}: {e}")

        return False, "All VPN attempts failed"

    def save_working_proxies(self):
        """Save working proxies to file"""
        try:
            os.makedirs('/workspaces/sugarglitch-realops/config', exist_ok=True)
            with open('/workspaces/sugarglitch-realops/config/working_proxies.json', 'w') as f:
                json.dump({'proxies': self.working_proxies[-50:]}, f)  # Keep last 50
        except Exception as e:
            print(f"⚠️ Failed to save working proxies: {e}")

    def wait_for_block_expiry(self):
        """Intelligent waiting for block expiry"""
        print("⏰ Waiting for IP block to expire...")

        # Calculate wait times based on block history
        if self.block_count == 0:
            wait_time = 3600  # 1 hour for first block
        elif self.block_count == 1:
            wait_time = 7200  # 2 hours for second block
        else:
            wait_time = 14400  # 4+ hours for repeated blocks

        # Add randomization to avoid pattern detection
        wait_time += random.randint(-600, 600)  # ±10 minutes

        print(f"  ⏱️ Calculated wait time: {wait_time//3600}h {(wait_time%3600)//60}m")

        # Check every 30 minutes if block is lifted
        check_interval = 1800  # 30 minutes
        elapsed = 0

        while elapsed < wait_time:
            remaining = wait_time - elapsed
            hours = remaining // 3600
            minutes = (remaining % 3600) // 60

            print(f"  ⏰ Waiting... {hours}h {minutes}m remaining")

            time.sleep(min(check_interval, remaining))
            elapsed += check_interval

            # Test if block is lifted
            success, message = self.test_instagram_access()
            if success:
                print("  ✅ Block appears to be lifted!")
                return True

        return False

    def change_network_interface(self):
        """Attempt to change network interface"""
        print("📡 Attempting network interface changes...")

        suggestions = [
            "🔌 Restart your router/modem (unplug for 30 seconds)",
            "📱 Switch to mobile data/hotspot if available",
            "🌐 Connect to a different WiFi network",
            "🔄 Request new IP from ISP (restart modem)",
            "🏢 Try from a different location/network"
        ]

        print("  💡 Manual network change suggestions:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"    {i}. {suggestion}")

        print("\n  ⚙️ Automatic network restart (Linux):")

        try:
            # Try to restart network manager (requires sudo)
            result = subprocess.run(['sudo', 'systemctl', 'restart', 'NetworkManager'],
                                  capture_output=True)
            if result.returncode == 0:
                print("    ✅ Network manager restarted")
                time.sleep(10)

                # Test new IP
                new_ip = self.detect_current_ip()
                print(f"    📍 New IP: {new_ip}")

                success, message = self.test_instagram_access()
                if success:
                    return True, "Network restart successful"

        except Exception as e:
            print(f"    ❌ Network restart failed: {e}")

        return False, "Manual intervention required"

    def comprehensive_bypass_attempt(self):
        """Run comprehensive IP block bypass attempts"""
        print("🚀 COMPREHENSIVE IP BLOCK BYPASS")
        print("=" * 50)

        current_ip = self.detect_current_ip()
        print(f"📍 Current IP: {current_ip}")

        # Test current access
        success, message = self.test_instagram_access()
        if success:
            print("✅ Instagram is currently accessible!")
            return True, "No block detected"

        print(f"🚨 Block confirmed: {message}")
        self.block_count += 1
        self.last_block_time = datetime.now()

        # Strategy 1: Proxy rotation
        print("\n🔄 STRATEGY 1: Proxy Rotation")
        print("-" * 30)
        proxy, proxy_message = self.rotate_ip_via_proxy()
        if proxy:
            return True, f"Bypass successful via proxy: {proxy_message}"

        # Strategy 2: VPN rotation
        print("\n🌐 STRATEGY 2: VPN Rotation")
        print("-" * 30)
        vpn_success, vpn_message = self.rotate_ip_via_vpn()
        if vpn_success:
            return True, f"Bypass successful via VPN: {vpn_message}"

        # Strategy 3: Network interface change
        print("\n📡 STRATEGY 3: Network Interface Change")
        print("-" * 30)
        network_success, network_message = self.change_network_interface()
        if network_success:
            return True, f"Bypass successful via network change: {network_message}"

        # Strategy 4: Wait for expiry
        print("\n⏰ STRATEGY 4: Wait for Block Expiry")
        print("-" * 30)
        wait_success = self.wait_for_block_expiry()
        if wait_success:
            return True, "Block lifted after waiting"

        return False, "All bypass strategies failed"

    def generate_recovery_script(self):
        """Generate a custom recovery script based on current situation"""
        script_content = f'''#!/usr/bin/env python3
"""
AUTO-GENERATED IP BLOCK RECOVERY SCRIPT
Generated at: {datetime.now().isoformat()}
Current IP: {self.detect_current_ip()}
Block Count: {self.block_count}
"""

import time
import requests
import random

def test_access():
    try:
        response = requests.get('https://www.instagram.com/', timeout=10)
        return response.status_code == 200 and "blocked" not in response.text.lower()
    except Exception:
        return False

def main():
    print("🚀 Starting recovery process...")

    # Test every 30 minutes for 4 hours
    max_attempts = 8
    attempt = 0

    while attempt < max_attempts:
        attempt += 1
        print(f"📍 Attempt {{attempt}}/{{max_attempts}}")

        if test_access():
            print("✅ Instagram access restored!")
            print("🎯 You can now run your extractors")
            break

        wait_time = random.randint(1800, 2100)  # 30-35 minutes
        print(f"⏰ Waiting {{wait_time//60}} minutes before next test...")
        time.sleep(wait_time)

    else:
        print("❌ Recovery unsuccessful after {{max_attempts}} attempts")
        print("💡 Try changing your network or using a VPN")

if __name__ == "__main__":
    main()
'''

        script_path = '/workspaces/sugarglitch-realops/auto_recovery.py'
        with open(script_path, 'w') as f:
            f.write(script_content)

        # Make executable
        os.chmod(script_path, 0o755)

        print(f"📄 Recovery script generated: {script_path}")
        print("🚀 Run with: python3 auto_recovery.py")

def main():
    """Main function"""
    print("🌐 ADVANCED IP BLOCK BYPASS & RECOVERY SYSTEM")
    print("=" * 60)

    bypass = AdvancedIPBypass()

    while True:
        print("\n🎯 BYPASS OPTIONS:")
        print("1. 🔍 Test Current Instagram Access")
        print("2. 🔄 Comprehensive Bypass Attempt")
        print("3. 📡 Manual Proxy Test")
        print("4. 🌐 Manual VPN Connection")
        print("5. 📄 Generate Recovery Script")
        print("6. 📊 System Status")
        print("q. 🚪 Quit")

        choice = input("\n🎮 Select option: ").strip().lower()

        if choice == 'q':
            break
        elif choice == '1':
            current_ip = bypass.detect_current_ip()
            print(f"📍 Current IP: {current_ip}")

            success, message = bypass.test_instagram_access()
            if success:
                print("✅ Instagram is accessible!")
            else:
                print(f"🚨 Instagram blocked: {message}")

        elif choice == '2':
            success, message = bypass.comprehensive_bypass_attempt()
            print(f"\n🎯 Result: {message}")

        elif choice == '3':
            proxy, message = bypass.rotate_ip_via_proxy()
            if proxy:
                print(f"✅ Proxy found: {proxy}")
            else:
                print(f"❌ No proxy: {message}")

        elif choice == '4':
            success, message = bypass.rotate_ip_via_vpn()
            if success:
                print(f"✅ VPN connected: {message}")
            else:
                print(f"❌ VPN failed: {message}")

        elif choice == '5':
            bypass.generate_recovery_script()

        elif choice == '6':
            print(f"📊 Block count: {bypass.block_count}")
            print(f"📍 Current IP: {bypass.detect_current_ip()}")
            print(f"🔧 Working proxies: {len(bypass.working_proxies)}")
            available_vpns = [vpn['name'] for vpn in bypass.vpn_services if vpn['available']]
            print(f"🌐 Available VPNs: {', '.join(available_vpns) if available_vpns else 'None'}")

        input("\n📱 Press Enter to continue...")

if __name__ == "__main__":
    main()
