# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Super Enhanced DM Extractor - ดึง DM แบบโหดๆ (Hardcore Mode)
Multiple endpoints, proxy support, real-time extraction
"""
import requests
import json
import os
import random
import time
from datetime import datetime
from urllib.parse import urljoin
import re

class SuperEnhancedDMExtractor:
    def __init__(self):
        self.session_data = None
        self.headers = {}
        self.proxies = []
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'
        ]
        self.api_endpoints = [
            'https://www.instagram.com/api/v1/direct_v2/inbox/',
            'https://i.instagram.com/api/v1/direct_v2/inbox/',
            'https://www.instagram.com/direct/inbox/api/',
            'https://www.instagram.com/api/v1/direct/inbox/',
            'https://i.instagram.com/api/v1/direct/inbox/',
        ]

    def load_session(self):
        """Load Instagram session from file"""
        try:
            with open('tools/session_alx_trading.json', 'r') as f:
                self.session_data = json.load(f)

            sessionid = self.session_data.get('sessionid', '')
            csrf_token = self.session_data.get('csrftoken', '')

            print(f"✅ Session loaded: {sessionid[:20]}...")
            print(f"✅ CSRF token: {csrf_token[:20]}..." if csrf_token else "⚠️  No CSRF token")

            return True
        except Exception as e:
            print(f"❌ Cannot load session: {e}")
            return False

    def setup_headers(self, endpoint_type="api"):
        """Setup headers for different endpoint types"""
        sessionid = self.session_data.get('sessionid', '')
        csrf_token = self.session_data.get('csrftoken', '')

        base_headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q = 0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Cookie': f'sessionid={sessionid}',
            'Referer': 'https://www.instagram.com/direct/inbox/',
            'Origin': 'https://www.instagram.com'
        }

        if endpoint_type == "api":
            base_headers.update({
                'x-ig-app-id': '936619743392459',
                'x-asbd-id': '129477',
                'x-ig-www-claim': '0',
                'x-requested-with': 'XMLHttpRequest',
            })

            if csrf_token:
                base_headers['x-csrftoken'] = csrf_token

        elif endpoint_type == "graphql":
            base_headers.update({
                'x-ig-app-id': '936619743392459',
                'x-fb-lsd': 'randomstring123',
                'x-requested-with': 'XMLHttpRequest',
            })

        self.headers = base_headers
        return base_headers

    def load_proxies(self):
        """Load proxy configuration"""
        proxy_files = [
            'config/proxy_config.json',
            'config/real_proxy_config.json',
            'config/working_proxies.json'
        ]

        for proxy_file in proxy_files:
            try:
                if os.path.exists(proxy_file):
                    with open(proxy_file, 'r') as f:
                        data = json.load(f)
                        if 'proxies' in data:
                            self.proxies.extend(data['proxies'])
                        elif 'brightdata' in data:
                            bd = data['brightdata']
                            self.proxies.append({
                                'http': f"http://{bd['username']}:{bd['password']}@{bd['host']}:{bd['port']}",
                                'https': f"http://{bd['username']}:{bd['password']}@{bd['host']}:{bd['port']}"
                            })
            except Exception as e:
                print(f"⚠️  Failed to load proxies from {proxy_file}: {e}")

        print(f"📡 Loaded {len(self.proxies)} proxies")

    def make_request(self, url, method="GET", data = None, use_proxy = True):
        """Make HTTP request with retry logic"""
        max_retries = 3

        for attempt in range(max_retries):
            try:
                proxy = None
                if use_proxy and self.proxies:
                    proxy = random.choice(self.proxies)

                print(f"📡 Attempt {attempt + 1}: {method} {url}")
                if proxy:
                    print(f"🔄 Using proxy: {list(proxy.values())[0].split('@')[1] if '@' in list(proxy.values())[0] else 'Unknown'}")

                response = requests.request(
                    method = method,
                    url = url,
                    headers = self.headers,
                    data = data,
                    proxies = proxy,
                    timeout = 15,
                    allow_redirects = True
                )

                print(f"📡 Response: {response.status_code}")

                if response.status_code == 200:
                    return response
                elif response.status_code == 401:
                    print("❌ Session expired (401)")
                    return response
                elif response.status_code == 403:
                    print("❌ Forbidden (403) - IP may be blocked")
                elif response.status_code == 429:
                    print("❌ Rate limited (429)")
                    time.sleep(5)
                else:
                    print(f"⚠️  Status {response.status_code}: {response.text[:100]}...")

            except requests.exceptions.Timeout:
                print(f"⏰ Timeout on attempt {attempt + 1}")
            except requests.exceptions.RequestException as e:
                print(f"❌ Request error: {e}")

            time.sleep(2)  # Wait between retries

        return None

    def extract_csrf_from_html(self, html_content):
        """Extract CSRF token from HTML page"""
        patterns = [
            r'"csrf_token":"([^"]+)"',
            r'csrfToken":"([^"]+)"',
            r'csrf_token":\s*"([^"]+)"',
            r'csrftoken":\s*"([^"]+)"'
        ]

        for pattern in patterns:
            match = re.search(pattern, html_content)
            if match:
                token = match.group(1)
                print(f"✅ Extracted CSRF token: {token[:20]}...")
                return token

        return None

    def try_direct_inbox_page(self):
        """Try to access direct inbox page and extract data"""
        print("\n🔍 Trying direct inbox page...")

        self.setup_headers("web")
        response = self.make_request('https://www.instagram.com/direct/inbox/', use_proxy = False)

        if response and response.status_code == 200:
            html_content = response.text

            # Extract CSRF token if not available
            if not self.session_data.get('csrftoken'):
                csrf_token = self.extract_csrf_from_html(html_content)
                if csrf_token:
                    self.session_data['csrftoken'] = csrf_token

            # Look for JSON data in HTML
            json_patterns = [
                r'window\._sharedData\s*=\s*({.*?});',
                r'window\.\_initialData\s*=\s*({.*?});',
                r'data-inbox-data="([^"]+)"',
                r'"inbox":\s*({.*?})',
            ]

            for pattern in json_patterns:
                matches = re.findall(pattern, html_content, re.DOTALL)
                if matches:
                    try:
                        for match in matches:
                            if match.startswith('{'):
                                data = json.loads(match)
                                print(f"✅ Found JSON data structure")
                                self.process_inbox_data(data)
                                return True
                    except json.JSONDecodeError:
                        continue

        return False

    def try_api_endpoints(self):
        """Try different API endpoints for DM extraction"""
        print("\n🔍 Trying API endpoints...")

        for endpoint in self.api_endpoints:
            print(f"\n📡 Trying endpoint: {endpoint}")

            self.setup_headers("api")
            response = self.make_request(endpoint)

            if response and response.status_code == 200:
                try:
                    data = response.json()
                    print("✅ Got JSON response!")
                    self.process_inbox_data(data)
                    return True
                except json.JSONDecodeError:
                    print("❌ Response is not JSON")
                    # Try to extract from HTML
                    if "<!DOCTYPE html>" in response.text:
                        print("📄 Got HTML response, trying to extract data...")
                        csrf_token = self.extract_csrf_from_html(response.text)
                        if csrf_token and not self.session_data.get('csrftoken'):
                            self.session_data['csrftoken'] = csrf_token
                            print("🔄 Retrying with extracted CSRF token...")
                            self.setup_headers("api")
                            retry_response = self.make_request(endpoint)
                            if retry_response and retry_response.status_code == 200:
                                try:
                                    data = retry_response.json()
                                    print("✅ Success with CSRF token!")
                                    self.process_inbox_data(data)
                                    return True
                                except json.JSONDecodeError:
                                    continue

            time.sleep(1)  # Rate limiting

        return False

    def try_mobile_api(self):
        """Try mobile API endpoints"""
        print("\n🔍 Trying mobile API endpoints...")

        mobile_endpoints = [
            'https://i.instagram.com/api/v1/direct_v2/inbox/?visual_message_return_type = unseen&thread_message_limit = 10&persistentBadging = true&limit = 20',
            'https://i.instagram.com/api/v1/direct_v2/inbox/?persistentBadging = true&limit = 10',
            'https://www.instagram.com/api/v1/direct_v2/threads/',
        ]

        # Mobile headers
        mobile_headers = {
            'User-Agent': 'Instagram 219.0.0.12.117 Android',
            'Accept': '*/*',
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
            'X-IG-Capabilities': '3brTvw==',
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Bandwidth-Speed-KBPS': '2500.000',
            'X-IG-Bandwidth-TotalBytes-B': '0',
            'X-IG-Bandwidth-TotalTime-MS': '0',
            'X-FB-HTTP-Engine': 'Liger',
            'Cookie': f'sessionid={self.session_data.get("sessionid", "")}',
        }

        self.headers = mobile_headers

        for endpoint in mobile_endpoints:
            print(f"\n📱 Trying mobile endpoint: {endpoint}")
            response = self.make_request(endpoint, use_proxy = False)

            if response and response.status_code == 200:
                try:
                    data = response.json()
                    print("✅ Got mobile JSON response!")
                    self.process_inbox_data(data)
                    return True
                except json.JSONDecodeError:
                    print("❌ Mobile response is not JSON")

            time.sleep(1)

        return False

    def process_inbox_data(self, data):
        """Process inbox data and extract DMs"""
        print("\n📊 Processing inbox data...")

        # Different data structures to check
        inbox_paths = [
            ['inbox'],
            ['data', 'inbox'],
            ['data', 'user', 'inbox'],
            ['viewer', 'inbox'],
            ['props', 'pageProps', 'inbox'],
        ]

        inbox_data = None
        for path in inbox_paths:
            temp_data = data
            try:
                for key in path:
                    temp_data = temp_data[key]
                inbox_data = temp_data
                print(f"✅ Found inbox data at path: {' -> '.join(path)}")
                break
            except (KeyError, TypeError):
                continue

        if not inbox_data:
            print("⚠️  No inbox data found, checking threads directly...")
            # Check for threads at different levels
            threads_paths = [
                ['threads'],
                ['data', 'threads'],
                ['viewer', 'threads'],
            ]

            for path in threads_paths:
                temp_data = data
                try:
                    for key in path:
                        temp_data = temp_data[key]
                    threads = temp_data
                    print(f"✅ Found threads at path: {' -> '.join(path)}")
                    self.save_results(threads, len(threads))
                    return
                except (KeyError, TypeError):
                    continue

        if inbox_data:
            threads = inbox_data.get('threads', [])
            print(f"✅ Found {len(threads)} DM threads")

            if threads:
                self.display_threads(threads[:5])  # Show first 5
                self.save_results(threads, len(threads))
            else:
                print("⚠️  No threads found in inbox data")
                # Save raw data for analysis
                self.save_raw_data(data)
        else:
            print("❌ Could not extract inbox data")
            self.save_raw_data(data)

    def display_threads(self, threads):
        """Display thread information"""
        print("\n📋 DM Threads:")
        for i, thread in enumerate(threads):
            thread_title = thread.get('thread_title', 'No Title')
            thread_id = thread.get('thread_id', 'Unknown')
            last_activity = thread.get('last_activity_at', 0)
            users = thread.get('users', [])
            user_names = [user.get('username', 'Unknown') for user in users]

            print(f"  {i+1}. {thread_title}")
            print(f"     ID: {thread_id}")
            print(f"     Users: {', '.join(user_names[:3])}")
            print(f"     Last activity: {last_activity}")

            # Show recent messages if available
            items = thread.get('items', [])
            if items:
                print(f"     Messages: {len(items)}")
                recent_msg = items[0] if items else {}
                msg_text = recent_msg.get('text', 'No text')
                print(f"     Recent: {msg_text[:50]}...")
            print()

    def save_results(self, threads, total_count):
        """Save extraction results"""
        os.makedirs('results', exist_ok = True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        result = {
            'extraction_time': datetime.now().isoformat(),
            'extractor': 'super_enhanced_dm_extractor',
            'total_threads': total_count,
            'status': 'success',
            'session_used': self.session_data.get('sessionid', '')[:20] + '...',
            'threads': threads
        }

        output_file = f'results/super_enhanced_dm_extraction_{timestamp}.json'
        with open(output_file, 'w') as f:
            json.dump(result, f, indent = 2)

        print(f"💾 Results saved to: {output_file}")
        print(f"🎉 Super Enhanced DM extraction completed! Found {total_count} threads")

    def save_raw_data(self, data):
        """Save raw data for analysis"""
        os.makedirs('results/raw', exist_ok = True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        output_file = f'results/raw/raw_response_{timestamp}.json'
        with open(output_file, 'w') as f:
            json.dump(data, f, indent = 2)

        print(f"💾 Raw data saved to: {output_file}")

    def run(self):
        """Main extraction process"""
        print("🚀 SUPER ENHANCED DM EXTRACTOR - HARDCORE MODE")
        print("="*60)

        if not self.load_session():
            return False

        self.load_proxies()

        # Try multiple methods
        methods = [
            ("Mobile API", self.try_mobile_api),
            ("API Endpoints", self.try_api_endpoints),
            ("Direct Inbox Page", self.try_direct_inbox_page),
        ]

        for method_name, method_func in methods:
            print(f"\n🔥 Trying method: {method_name}")
            try:
                if method_func():
                    print(f"✅ Success with {method_name}!")
                    return True
            except Exception as e:
                print(f"❌ {method_name} failed: {e}")
                import traceback
                traceback.print_exc()

            print(f"⏳ Waiting before next method...")
            time.sleep(3)

        print("\n❌ All extraction methods failed")
        print("💡 Possible issues:")
        print("   - Session expired")
        print("   - IP blocked by Instagram")
        print("   - Account requires verification")
        print("   - Rate limit exceeded")

        return False

def main():
    extractor = SuperEnhancedDMExtractor()
    extractor.run()

if __name__ == "__main__":
    main()
