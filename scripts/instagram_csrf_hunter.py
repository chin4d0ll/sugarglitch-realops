#!/usr/bin/env python3
"""
🌸 Instagram-Specific CSRF & Token Hunter 🌸
💕 เฉพาะสำหรับ Instagram patterns และ endpoints
🔥 ออกแบบมาเพื่อ bypass Instagram security โดยเฉพาะ!
"""

import asyncio
import aiohttp
import re
import json
import time
import random
from datetime import datetime
from urllib.parse import urljoin
import cloudscraper

# สีสวยๆ


class Colors:
    PINK = '\033[95m'
    PURPLE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_cute(text, color=Colors.PINK):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{timestamp}] 🌸 {text} 💕{Colors.END}")


def print_success(text):
    print_cute(f"✅ {text}", Colors.GREEN)


def print_warning(text):
    print_cute(f"⚠️ {text}", Colors.YELLOW)


def print_error(text):
    print_cute(f"❌ {text}", Colors.RED)


def print_info(text):
    print_cute(f"ℹ️ {text}", Colors.CYAN)


class InstagramCSRFHunter:
    """เฉพาะสำหรับ Instagram CSRF และ token hunting"""

    def __init__(self):
        self.found_tokens = []
        self.found_endpoints = []
        self.session_data = {}

        # Instagram-specific patterns
        self.instagram_patterns = {
            'csrf_tokens': [
                r'"csrf_token":"([^"]+)"',
                r'csrftoken["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                r'window\._sharedData.*?"csrf_token":"([^"]+)"',
                r'__igCsrfToken["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                r'X-CSRFToken["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                r'ig_csrf_token["\']?\s*[:=]\s*["\']([^"\']+)["\']'
            ],
            'session_tokens': [
                r'"sessionid":"([^"]+)"',
                r'sessionid["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                r'ig_session["\']?\s*[:=]\s*["\']([^"\']+)["\']'
            ],
            'api_endpoints': [
                r'["\'/](api/v1/[^"\'>\s]+)',
                r'["\'/](graphql[^"\'>\s]*)',
                r'["\'/](ajax/[^"\'>\s]+)',
                r'["\'/](web/[^"\'>\s]+)',
                r'endpoint["\']?\s*:\s*["\']([^"\']+)["\']'
            ],
            'instagram_specific': [
                r'ig_[a-zA-Z_]+["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                r'__ig[a-zA-Z_]+["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                r'Instagram[a-zA-Z_]+["\']?\s*[:=]\s*["\']([^"\']+)["\']'
            ]
        }

        # Instagram API endpoints ที่รู้จัก
        self.known_instagram_endpoints = [
            '/api/v1/web/accounts/login/ajax/',
            '/api/v1/web/likes/unlike/',
            '/api/v1/web/likes/like/',
            '/api/v1/web/comments/add/',
            '/api/v1/web/friendships/follow/',
            '/api/v1/web/friendships/unfollow/',
            '/graphql/query/',
            '/ajax/bz',
            '/web/direct_v2/threads/',
            '/api/v1/users/web_profile_info/',
            '/web/search/topsearch/',
            '/accounts/login/ajax/',
            '/accounts/logout/ajax/'
        ]

    def get_instagram_headers(self):
        """สร้าง headers เฉพาะสำหรับ Instagram"""
        return {
            'User-Agent': random.choice([
                ('Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 '
                 'like Mac OS X) AppleWebKit/605.1.15 '
                 '(KHTML, like Gecko) Version/14.1.2 '
                 'Mobile/15E148 Safari/604.1'),
                ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/91.0.4472.124 Safari/537.36'),
                ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/91.0.4472.124 Safari/537.36')
            ]),
            'Accept': ('text/html,application/xhtml+xml,application/xml;'
                       'q=0.9,image/webp,image/apng,*/*;q=0.8'),
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest'
        }

    async def hunt_instagram_tokens(self, instagram_url):
        """ล่า tokens เฉพาะสำหรับ Instagram"""
        print_info(f"🎯 เริ่มล่า Instagram tokens: {instagram_url}")

        # Method 1: Direct approach
        await self._hunt_direct_approach(instagram_url)

        # Method 2: Mobile approach
        await self._hunt_mobile_approach(instagram_url)

        # Method 3: Cloudscraper approach
        await self._hunt_cloudscraper_approach(instagram_url)

        # Method 4: Alternative endpoints
        await self._hunt_alternative_endpoints(instagram_url)

        # Method 5: Public API approach
        await self._hunt_public_api_approach(instagram_url)

        return self.found_tokens, self.found_endpoints

    async def _hunt_direct_approach(self, url):
        """วิธีการตรง ๆ"""
        print_info("🎯 Method 1: Direct Approach")

        try:
            async with aiohttp.ClientSession() as session:
                headers = self.get_instagram_headers()

                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        content = await response.text()
                        self._extract_instagram_data(content, url, "direct")
                        print_success("✅ Direct approach ได้ข้อมูล!")
                    else:
                        print_warning(
                            f"⚠️ Direct approach: Status {response.status}")
        except Exception as e:
            print_error(f"❌ Direct approach error: {e}")

    async def _hunt_mobile_approach(self, url):
        """วิธีการ mobile"""
        print_info("📱 Method 2: Mobile Approach")

        try:
            mobile_headers = {
                'User-Agent': ('Instagram 219.0.0.12.117 Android '
                               '(29/10; 420dpi; 1080x2340; samsung; '
                               'SM-G975F; beyond2; exynos9820; en_US; 334361595)'),
                'Accept': '*/*',
                'Accept-Language': 'en-US',
                'Accept-Encoding': 'gzip, deflate',
                'X-IG-App-ID': '936619743392459',
                'X-IG-Capabilities': '3brTvx0=',
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Bandwidth-Speed-KBPS': '2000.000',
                'X-IG-Bandwidth-TotalBytes-B': '0',
                'X-IG-Bandwidth-TotalTime-MS': '0'
            }

            async with aiohttp.ClientSession() as session:
                # Try mobile version
                mobile_url = url.replace(
                    'www.instagram.com', 'm.instagram.com')
                async with session.get(mobile_url, headers=mobile_headers) as response:
                    if response.status == 200:
                        content = await response.text()
                        self._extract_instagram_data(
                            content, mobile_url, "mobile")
                        print_success("✅ Mobile approach ได้ข้อมูล!")
                    else:
                        print_warning(
                            f"⚠️ Mobile approach: Status {response.status}")
        except Exception as e:
            print_error(f"❌ Mobile approach error: {e}")

    async def _hunt_cloudscraper_approach(self, url):
        """วิธีการ cloudscraper"""
        print_info("☁️ Method 3: Cloudscraper Approach")

        try:
            scraper = cloudscraper.create_scraper(
                browser={
                    'browser': 'chrome',
                    'platform': 'darwin',
                    'mobile': False
                }
            )

            headers = self.get_instagram_headers()
            response = scraper.get(url, headers=headers, timeout=30)

            if response.status_code == 200:
                self._extract_instagram_data(
                    response.text, url, "cloudscraper")
                print_success("✅ Cloudscraper approach ได้ข้อมูล!")
            else:
                print_warning(
                    f"⚠️ Cloudscraper: Status {response.status_code}")
        except Exception as e:
            print_error(f"❌ Cloudscraper error: {e}")

    async def _hunt_alternative_endpoints(self, url):
        """ลอง alternative endpoints"""
        print_info("🔄 Method 4: Alternative Endpoints")

        # สร้าง alternative URLs
        alternatives = [
            url + '?__a=1',
            url + '?__a=1&__d=dis',
            url.replace('/alx.trading/', '/alx.trading/?hl=en'),
            'https://www.instagram.com/accounts/login/',
            'https://www.instagram.com/',
            'https://i.instagram.com/api/v1/users/web_profile_info/?username=alx.trading'
        ]

        async with aiohttp.ClientSession() as session:
            for alt_url in alternatives:
                try:
                    headers = self.get_instagram_headers()
                    async with session.get(alt_url, headers=headers) as response:
                        if response.status == 200:
                            content = await response.text()

                            # ลองแปลงเป็น JSON ถ้าเป็นไปได้
                            try:
                                json_data = json.loads(content)
                                self._extract_from_json(json_data, alt_url)
                                print_success(f"✅ JSON data from: {alt_url}")
                            except:
                                self._extract_instagram_data(
                                    content, alt_url, "alternative")

                        await asyncio.sleep(random.uniform(1, 3))

                except Exception as e:
                    continue

    async def _hunt_public_api_approach(self, url):
        """ลอง public API endpoints"""
        print_info("🌐 Method 5: Public API Approach")

        # Extract username
        username_match = re.search(r'instagram\.com/([^/]+)', url)
        if not username_match:
            return

        username = username_match.group(1)

        # Test known endpoints
        base_url = "https://www.instagram.com"
        test_endpoints = [
            f"/web/search/topsearch/?query={username}",
            f"/{username}/?__a=1",
            "/accounts/login/",
            "/api/v1/web/get_ruling_for_content/",
        ]

        async with aiohttp.ClientSession() as session:
            for endpoint in test_endpoints:
                try:
                    full_url = base_url + endpoint
                    headers = self.get_instagram_headers()

                    async with session.get(full_url, headers=headers) as response:
                        if response.status == 200:
                            content = await response.text()

                            # บันทึกเป็น endpoint ที่พบ
                            self.found_endpoints.append({
                                'url': full_url,
                                'method': 'GET',
                                'status': response.status,
                                'source': 'public_api'
                            })

                            # Extract tokens
                            self._extract_instagram_data(
                                content, full_url, "public_api")

                        await asyncio.sleep(random.uniform(0.5, 1.5))

                except Exception as e:
                    continue

    def _extract_instagram_data(self, content, source_url, method):
        """Extract Instagram-specific data"""

        # Extract CSRF tokens
        for pattern in self.instagram_patterns['csrf_tokens']:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                token = match.group(1)
                if len(token) > 10:
                    token_data = {
                        'type': 'csrf_token',
                        'value': token,
                        'source': source_url,
                        'method': method,
                        'pattern': pattern[:50] + "..."
                    }
                    self.found_tokens.append(token_data)
                    print_success(f"🔑 CSRF Token: {token[:25]}... ({method})")

        # Extract session tokens
        for pattern in self.instagram_patterns['session_tokens']:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                token = match.group(1)
                if len(token) > 10:
                    token_data = {
                        'type': 'session_token',
                        'value': token,
                        'source': source_url,
                        'method': method,
                        'pattern': pattern[:50] + "..."
                    }
                    self.found_tokens.append(token_data)
                    print_success(
                        f"🍪 Session Token: {token[:25]}... ({method})")

        # Extract API endpoints
        for pattern in self.instagram_patterns['api_endpoints']:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                endpoint = match.group(1)
                full_endpoint = urljoin('https://www.instagram.com', endpoint)

                endpoint_data = {
                    'url': full_endpoint,
                    'method': 'GET',
                    'source': method,
                    'found_in': source_url
                }
                self.found_endpoints.append(endpoint_data)
                print_success(f"🌐 Endpoint: {full_endpoint} ({method})")

        # Extract Instagram-specific tokens
        for pattern in self.instagram_patterns['instagram_specific']:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                token = match.group(1)
                if len(token) > 5:
                    token_data = {
                        'type': 'instagram_specific',
                        'value': token,
                        'source': source_url,
                        'method': method,
                        'pattern': pattern[:50] + "..."
                    }
                    self.found_tokens.append(token_data)
                    print_success(f"📱 IG Token: {token[:25]}... ({method})")

    def _extract_from_json(self, json_data, source_url):
        """Extract data จาก JSON response"""
        try:
            json_str = json.dumps(json_data)
            self._extract_instagram_data(json_str, source_url, "json")

            # Look for specific keys
            if isinstance(json_data, dict):
                for key, value in json_data.items():
                    if 'csrf' in key.lower() or 'token' in key.lower():
                        if isinstance(value, str) and len(value) > 10:
                            token_data = {
                                'type': 'json_token',
                                'key': key,
                                'value': value,
                                'source': source_url,
                                'method': 'json'
                            }
                            self.found_tokens.append(token_data)
                            print_success(
                                f"🔐 JSON Token ({key}): {value[:25]}...")
        except Exception as e:
            print_warning(f"JSON extraction error: {e}")

    def generate_instagram_report(self):
        """สร้างรายงานเฉพาะ Instagram"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report = f"""
🌸💕 Instagram-Specific CSRF & Token Hunt Report 💕🌸
⏰ เวลา: {timestamp}
🎯 Target: Instagram Profile Analysis
💕 โดย: Instagram CSRF Hunter Framework
{'='*60}

🔑 TOKENS DISCOVERED: {len(self.found_tokens)} tokens
{'='*60}
"""

        if self.found_tokens:
            # จัดกลุ่มตามประเภท
            token_types = {}
            for token in self.found_tokens:
                token_type = token['type']
                if token_type not in token_types:
                    token_types[token_type] = []
                token_types[token_type].append(token)

            for token_type, tokens in token_types.items():
                report += f"\n📌 {token_type.upper()} ({len(tokens)} tokens):\n"

                for i, token in enumerate(tokens, 1):
                    token_preview = (token['value'][:40] + "..."
                                     if len(token['value']) > 40
                                     else token['value'])
                    report += f"""
Token #{i}:
   🔐 Value: {token_preview}
   📍 Method: {token['method']}
   🔗 Source: {token['source']}
"""
                    if 'key' in token:
                        report += f"   🏷️  Key: {token['key']}\n"
                    if 'pattern' in token:
                        report += f"   🔍 Pattern: {token['pattern']}\n"
        else:
            report += "\n❌ No tokens found\n"

        report += f"""

🌐 API ENDPOINTS DISCOVERED: {len(self.found_endpoints)} endpoints
{'='*60}
"""

        if self.found_endpoints:
            for i, endpoint in enumerate(self.found_endpoints, 1):
                report += f"""
Endpoint #{i}:
   🔗 URL: {endpoint['url']}
   📝 Method: {endpoint['method']}
   📍 Found via: {endpoint['source']}
"""
                if 'status' in endpoint:
                    report += f"   📊 Status: {endpoint['status']}\n"
        else:
            report += "\n❌ No endpoints found\n"

        # Instagram-specific analysis
        report += f"""

📱 INSTAGRAM-SPECIFIC ANALYSIS:
{'='*60}
"""

        csrf_count = len(
            [t for t in self.found_tokens if t['type'] == 'csrf_token'])
        session_count = len(
            [t for t in self.found_tokens if t['type'] == 'session_token'])
        ig_count = len(
            [t for t in self.found_tokens if t['type'] == 'instagram_specific'])

        report += f"🔑 CSRF Tokens: {csrf_count}\n"
        report += f"🍪 Session Tokens: {session_count}\n"
        report += f"📱 Instagram-specific Tokens: {ig_count}\n"
        report += f"🌐 API Endpoints: {len(self.found_endpoints)}\n"

        if csrf_count > 0:
            report += "\n✅ SUCCESS: CSRF tokens พบแล้ว!\n"
            report += "🔥 สามารถใช้สำหรับ Instagram automation\n"
        else:
            report += "\n⚠️ No CSRF tokens found - Instagram security is strong\n"

        report += f"""

💡 INSTAGRAM RECOMMENDATIONS:
{'='*60}
1. 🔑 ใช้ CSRF tokens ที่พบสำหรับ API calls
2. 🍪 เก็บ session tokens สำหรับ authentication
3. 📱 ใช้ mobile endpoints สำหรับ better success rate
4. ⏰ ใช้ proper delays เพื่อหลีกเลี่ยง rate limiting
5. 🔄 Rotate user agents และ headers
6. 🌐 ทดสอบ discovered endpoints เพิ่มเติม

{'='*60}
💖 Instagram Hunt completed!
⚠️ ใช้อย่างรับผิดชอบและถูกกฎหมายเท่านั้น!
{'='*60}
"""

        return report


async def main():
    """Main function สำหรับ Instagram hunter"""
    print_cute("🌸💕 Instagram-Specific CSRF & Token Hunter 💕🌸", Colors.PURPLE)
    print_cute("📱 เฉพาะสำหรับ Instagram patterns และ bypasses!", Colors.CYAN)

    import sys

    # Get target URL
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = input("🎯 ใส่ Instagram URL: ").strip()

    if not target_url:
        target_url = "https://www.instagram.com/alx.trading/"
        print_warning(f"ใช้ตัวอย่าง: {target_url}")

    # Create hunter
    hunter = InstagramCSRFHunter()

    # Start hunting
    print_info("🚀 เริ่มการล่า Instagram tokens และ endpoints...")
    tokens, endpoints = await hunter.hunt_instagram_tokens(target_url)

    # Generate report
    report = hunter.generate_instagram_report()

    # Save report
    timestamp = int(time.time())
    report_file = f"instagram_csrf_hunt_{timestamp}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    # Display results
    print(report)
    print_success(f"📄 รายงานบันทึกแล้ว: {report_file}")

    # Summary
    print_cute("\n🎯 SUMMARY:", Colors.BOLD)
    print(f"🔑 Total tokens: {len(tokens)}")
    print(f"🌐 Total endpoints: {len(endpoints)}")

    if tokens:
        print_success("🎉 SUCCESS! พบ tokens สำหรับ Instagram!")
    else:
        print_warning("⚠️ ไม่พบ tokens - ลองวิธีอื่นต่อ")

if __name__ == "__main__":
    asyncio.run(main())
