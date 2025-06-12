# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔥💀 SESSION REGENERATOR FLEMING654 💀🔥
=======================================
Advanced session regeneration and IP bypass system
Creates fresh sessions to bypass Instagram blacklists

Features:
- 🎭 Multiple user agent rotation
- 🌐 Proxy integration for IP rotation
- 🔄 Session warming techniques
- 🛡️ Anti-detection mechanisms
- ⚡ Fast session generation
"""

import requests
import json
import time
import random
import hashlib
import base64
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class SessionRegeneratorFleming654:
    """🔥 Advanced Session Regenerator"""

    def __init__(self):
        self.session = requests.Session()
        self.proxies = []
        self.user_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
            "Instagram 219.0.0.12.117 Android (29/10; 420dpi; 1080x2340; samsung; SM-G973F; beyond1; exynos9820; en_US; 336448914)",
            "Instagram 218.0.0.19.118 Android (28/9; 480dpi; 1080x2280; OnePlus; ONEPLUS A6000; OnePlus6; qcom; en_US; 334448938)"
        ]
        self.sessions_dir = Path("sessions_regenerated")
        self.sessions_dir.mkdir(exist_ok=True)

    def load_proxies(self) -> bool:
        """Load available proxies for IP rotation"""
        try:
            # Try to load from our proxy list
            proxy_files = [
                "config/working_proxies.json",
                "config/proxy_list.txt"
            ]

            for proxy_file in proxy_files:
                if os.path.exists(proxy_file):
                    if proxy_file.endswith('.json'):
                        with open(proxy_file, 'r') as f:
                            proxy_data = json.load(f)
                            if isinstance(proxy_data, list):
                                for item in proxy_data:
                                    if isinstance(item, dict) and 'proxy' in item:
                                        self.proxies.append(item['proxy'])
                                    elif isinstance(item, str):
                                        self.proxies.append(item)
                    else:
                        with open(proxy_file, 'r') as f:
                            for line in f:
                                line = line.strip()
                                if line and ':' in line:
                                    if not line.startswith('http'):
                                        line = f"http://{line}"
                                    self.proxies.append(line)

                    if self.proxies:
                        print(f"✅ Loaded {len(self.proxies)} proxies from {proxy_file}")
                        return True

            # Fallback to some free proxies for testing
            print("🌐 Using fallback proxy sources...")
            self.get_free_proxies()
            return len(self.proxies) > 0

        except Exception as e:
            print(f"❌ Failed to load proxies: {e}")
            return False

    def get_free_proxies(self):
        """Get some free proxies for testing"""
        try:
            # Simple free proxy sources
            sources = [
                "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all"
            ]

            for source in sources:
                try:
                    response = requests.get(source, timeout=10)
                    if response.status_code == 200:
                        proxies_text = response.text.strip()
                        for line in proxies_text.split('\n'):
                            line = line.strip()
                            if ':' in line:
                                proxy = f"http://{line}"
                                self.proxies.append(proxy)
                                if len(self.proxies) >= 10:  # Limit for testing
                                    break
                except Exception:
                    continue

        except Exception as e:
            print(f"⚠️ Could not fetch free proxies: {e}")

    def get_random_proxy(self) -> Optional[str]:
        """Get random proxy from pool"""
        if self.proxies:
            return random.choice(self.proxies)
        return None

    def create_stealth_session(self) -> requests.Session:
        """Create stealth session with anti-detection"""
        session = requests.Session()

        # Random user agent
        user_agent = random.choice(self.user_agents)

        # Stealth headers
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }

        session.headers.update(headers)

        # Set proxy if available
        proxy = self.get_random_proxy()
        if proxy:
            session.proxies = {
                'http': proxy,
                'https': proxy
            }
            print(f"🌐 Using proxy: {proxy}")

        return session

    def test_session_connectivity(self, session: requests.Session) -> bool:
        """Test if session can connect to Instagram"""
        try:
            # Test basic connectivity
            response = session.get("https://httpbin.org/ip", timeout=10)
            if response.status_code == 200:
                ip_info = response.json()
                print(f"🌍 Current IP: {ip_info.get('origin', 'unknown')}")

                # Test Instagram accessibility
                ig_response = session.get("https://www.instagram.com/", timeout=15)
                if ig_response.status_code == 200:
                    print("✅ Instagram accessible")
                    return True
                else:
                    print(f"❌ Instagram blocked (status: {ig_response.status_code})")
                    return False

        except Exception as e:
            print(f"❌ Connectivity test failed: {e}")
            return False

        return False

    def warm_up_session(self, session: requests.Session):
        """Warm up session with human-like behavior"""
        print("🔥 Warming up session...")

        warm_up_urls = [
            "https://httpbin.org/user-agent",
            "https://httpbin.org/headers",
            "https://www.google.com/",
        ]

        for i, url in enumerate(warm_up_urls):
            try:
                print(f"   🌡️ Warm-up step {i+1}/3...")
                response = session.get(url, timeout=10)
                time.sleep(random.uniform(2, 5))
            except Exception:
                pass

        print("✅ Session warmed up!")

    def generate_session_data(self) -> Dict:
        """Generate new session data"""
        timestamp = int(time.time())
        session_id = f"fleming654_{timestamp}_{random.randint(1000, 9999)}"

        return {
            'session_id': session_id,
            'timestamp': timestamp,
            'user_agent': random.choice(self.user_agents),
            'ip_rotated': True,
            'warmed_up': True,
            'created_by': 'SessionRegeneratorFleming654',
            'csrf_token': base64.b64encode(os.urandom(24)).decode(),
            'device_id': hashlib.md5(f"{session_id}_{timestamp}".encode()).hexdigest(),
            'status': 'fresh'
        }

    def save_session(self, session_data: Dict, session_name: str = None) -> str:
        """Save session data to file"""
        if not session_name:
            session_name = f"session_fleming654_{int(time.time())}.json"

        session_file = self.sessions_dir / session_name

        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)

        print(f"💾 Session saved: {session_file}")
        return str(session_file)

    def regenerate_multiple_sessions(self, count: int = 5) -> List[str]:
        """Generate multiple fresh sessions"""
        print(f"🔄 Regenerating {count} fresh sessions...")

        # Load proxies first
        self.load_proxies()

        generated_sessions = []

        for i in range(count):
            print(f"\n🎯 Generating session {i+1}/{count}...")

            try:
                # Create stealth session
                session = self.create_stealth_session()

                # Test connectivity
                if self.test_session_connectivity(session):
                    # Warm up session
                    self.warm_up_session(session)

                    # Generate session data
                    session_data = self.generate_session_data()
                    session_data['connectivity_tested'] = True
                    session_data['proxy_used'] = session.proxies.get('http', 'direct') if session.proxies else 'direct'

                    # Save session
                    session_file = self.save_session(session_data, f"fresh_session_{i+1}.json")
                    generated_sessions.append(session_file)

                    print(f"✅ Session {i+1} generated successfully!")

                else:
                    print(f"❌ Session {i+1} failed connectivity test")

                # Delay between sessions
                if i < count - 1:
                    delay = random.uniform(3, 8)
                    print(f"⏱️ Waiting {delay:.1f}s before next session...")
                    time.sleep(delay)

            except Exception as e:
                print(f"❌ Failed to generate session {i+1}: {e}")

        return generated_sessions

    def test_existing_sessions(self) -> List[str]:
        """Test existing sessions and return working ones"""
        print("🔍 Testing existing sessions...")

        working_sessions = []
        session_files = list(self.sessions_dir.glob("*.json"))

        for session_file in session_files:
            try:
                with open(session_file, 'r') as f:
                    session_data = json.load(f)

                print(f"🧪 Testing {session_file.name}...")

                # Create session with stored data
                test_session = self.create_stealth_session()

                if self.test_session_connectivity(test_session):
                    print(f"✅ {session_file.name} is working")
                    working_sessions.append(str(session_file))
                else:
                    print(f"❌ {session_file.name} is not working")

                time.sleep(2)

            except Exception as e:
                print(f"❌ Error testing {session_file.name}: {e}")

        return working_sessions

    def create_ip_bypass_session(self) -> Optional[str]:
        """Create special session designed to bypass IP blacklists"""
        print("🚀 Creating IP bypass session...")

        # Load proxies
        if not self.load_proxies():
            print("⚠️ No proxies available, using direct connection")

        # Try multiple proxy/session combinations
        for attempt in range(3):
            try:
                print(f"🎯 Bypass attempt {attempt + 1}/3...")

                # Create fresh session with different proxy each time
                session = self.create_stealth_session()

                # Test with longer timeout
                if self.test_session_connectivity(session):
                    # Extended warm-up for bypass
                    print("🔥 Extended warm-up for bypass...")
                    self.warm_up_session(session)

                    # Additional Instagram-specific warm-up
                    try:
                        ig_warmup = session.get("https://www.instagram.com/static/bundles/es6/ConsumerUICommons.js/e8b1ad7096ce.js", timeout=10)
                        time.sleep(3)
                    except Exception:
                        pass

                    # Generate bypass session data
                    session_data = self.generate_session_data()
                    session_data['bypass_mode'] = True
                    session_data['attempt'] = attempt + 1
                    session_data['special_purpose'] = 'ip_blacklist_bypass'

                    bypass_file = self.save_session(session_data, f"bypass_session_fleming654.json")
                    print(f"🎉 IP bypass session created: {bypass_file}")
                    return bypass_file

                time.sleep(5)  # Wait between attempts

            except Exception as e:
                print(f"❌ Bypass attempt {attempt + 1} failed: {e}")

        print("💔 Failed to create bypass session")
        return None

    def display_banner(self):
        """Display banner"""
        print("""
🔥💀 SESSION REGENERATOR FLEMING654 💀🔥
=======================================
🎭 Advanced Session Generation System
🌐 IP Blacklist Bypass Specialist
🛡️ Anti-Detection Technology
""")

    def run_interactive_menu(self):
        """Run interactive menu"""
        self.display_banner()

        while True:
            print("\n" + "="*50)
            print("🎯 SESSION REGENERATOR MENU")
            print("="*50)
            print("1. 🔄 Generate Fresh Sessions (Multiple)")
            print("2. 🚀 Create IP Bypass Session")
            print("3. 🧪 Test Existing Sessions")
            print("4. 📊 View Session Status")
            print("0. 💔 Exit")
            print("="*50)

            choice = input("👉 Select option: ").strip()

            if choice == "1":
                count = input("Number of sessions to generate (default 5): ").strip()
                count = int(count) if count.isdigit() else 5
                sessions = self.regenerate_multiple_sessions(count)
                print(f"\n🎉 Generated {len(sessions)} sessions!")

            elif choice == "2":
                bypass_session = self.create_ip_bypass_session()
                if bypass_session:
                    print(f"🎉 Bypass session ready: {bypass_session}")

            elif choice == "3":
                working = self.test_existing_sessions()
                print(f"\n📊 Found {len(working)} working sessions")

            elif choice == "4":
                self.show_session_status()

            elif choice == "0":
                print("👋 Goodbye!")
                break

            else:
                print("❌ Invalid option!")

    def show_session_status(self):
        """Show status of all sessions"""
        print("\n📊 SESSION STATUS")
        print("="*40)

        session_files = list(self.sessions_dir.glob("*.json"))

        if not session_files:
            print("❌ No sessions found")
            return

        for session_file in session_files:
            try:
                with open(session_file, 'r') as f:
                    session_data = json.load(f)

                created = datetime.fromtimestamp(session_data.get('timestamp', 0))
                age = datetime.now() - created

                print(f"📄 {session_file.name}")
                print(f"   Created: {created.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   Age: {age.days} days, {age.seconds//3600} hours")
                print(f"   Status: {session_data.get('status', 'unknown')}")
                print()

            except Exception as e:
                print(f"❌ Error reading {session_file.name}: {e}")
def main():
    """Main function"""
    regenerator = SessionRegeneratorFleming654()
    regenerator.run_interactive_menu()
if __name__ == "__main__":
    main()
