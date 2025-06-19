#!/usr/bin/env python3
"""
🔥 Advanced Instagram CSRF Hunter with Rate Limit Bypass 🔥
เวอร์ชันขั้นสูงที่แก้ปัญหา Rate Limit และ Detection
"""

import asyncio
import aiohttp
import re
import time
import random
from datetime import datetime
import cloudscraper
from fake_useragent import UserAgent
import sys


class AdvancedInstagramHunter:
    def __init__(self):
        self.ua = UserAgent()
        self.found_tokens = []
        self.found_endpoints = []
        self.session_cookies = {}

    def get_stealth_headers(self):
        """สร้าง headers แบบ stealth เพื่อหลบ detection"""
        return {
            'User-Agent': random.choice([
                ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/120.0.0.0 Safari/537.36'),
                ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/120.0.0.0 Safari/537.36'),
                ('Mozilla/5.0 (X11; Linux x86_64) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/120.0.0.0 Safari/537.36')
            ]),
            'Accept': ('text/html,application/xhtml+xml,application/xml;'
                       'q=0.9,image/webp,*/*;q=0.8'),
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'DNT': '1'
        }

    async def bypass_rate_limit_hunt(self, url):
        """ล่า CSRF tokens โดย bypass rate limit"""
        print("🔥 เริ่มล่า CSRF tokens แบบ Advanced Bypass!")
        print(f"🎯 Target: {url}")
        print("="*60)

        # Method 1: ใช้ cloudscraper เพื่อ bypass Cloudflare
        print("🌩️  Method 1: Cloudscraper Bypass...")
        await self._hunt_with_cloudscraper(url)

        # Method 2: ใช้ different endpoints
        print("\n🚀 Method 2: Alternative Endpoints...")
        await self._hunt_alternative_endpoints(url)

        # Method 3: ใช้ mobile user agent
        print("\n📱 Method 3: Mobile User Agent...")
        await self._hunt_with_mobile_ua(url)

        # Method 4: ค้นหาจาก cached/archive versions
        print("\n💾 Method 4: Archive/Cache Hunt...")
        await self._hunt_from_archives(url)

    async def _hunt_with_cloudscraper(self, url):
        """ใช้ cloudscraper เพื่อ bypass Cloudflare"""
        try:
            scraper = cloudscraper.create_scraper(
                browser={
                    'browser': 'chrome',
                    'platform': 'windows',
                    'mobile': False
                }
            )

            print("   🌩️  กำลังใช้ Cloudscraper...")
            response = scraper.get(url, timeout=30)

            if response.status_code == 200:
                print(
                    f"   ✅ Cloudscraper สำเร็จ! Status: {response.status_code}")
                print(f"   📊 Content size: {len(response.text)} bytes")

                # ค้นหา CSRF tokens
                await self._extract_csrf_tokens(response.text, url, "cloudscraper")

                # ค้นหา endpoints
                await self._extract_endpoints(response.text, url, "cloudscraper")

            else:
                print(
                    f"   ❌ Cloudscraper failed: Status {response.status_code}")

        except Exception as e:
            print(f"   ❌ Cloudscraper error: {e}")

    async def _hunt_alternative_endpoints(self, url):
        """ค้นหาจาก alternative endpoints ของ Instagram"""
        alternative_urls = [
            # Mobile version
            url.replace('www.instagram.com', 'm.instagram.com'),
            url + '?__a=1',  # Instagram API parameter
            url + '?__a=1&__d=dis',  # Instagram API with disable parameter
            # With language parameter
            url.replace('/alx.trading/', '/alx.trading/?hl=en'),
            'https://www.instagram.com/accounts/login/',  # Login page
            'https://www.instagram.com/',  # Main page
        ]

        async with aiohttp.ClientSession() as session:
            for alt_url in alternative_urls:
                try:
                    headers = self.get_stealth_headers()

                    print(f"   🔍 Testing: {alt_url}")
                    async with session.get(alt_url, headers=headers, timeout=30) as response:
                        if response.status == 200:
                            content = await response.text()
                            print(f"   ✅ Success! Status: {response.status}")

                            # Extract tokens และ endpoints
                            await self._extract_csrf_tokens(content, alt_url, "alternative")
                            await self._extract_endpoints(content, alt_url, "alternative")

                        elif response.status == 429:
                            print(f"   ⏳ Rate limited: {alt_url}")
                        else:
                            print(
                                f"   ⚠️  Status {response.status}: {alt_url}")

                    # Delay between requests
                    await asyncio.sleep(random.uniform(2, 5))

                except Exception as e:
                    print(f"   ❌ Error with {alt_url}: {e}")
                    continue

    async def _hunt_with_mobile_ua(self, url):
        """ใช้ mobile user agent"""
        mobile_headers = {
            'User-Agent': ('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)'
                           ' AppleWebKit/605.1.15 (KHTML, like Gecko)'
                           ' Version/17.0 Mobile/15E148 Safari/604.1'),
            'Accept': ('text/html,application/xhtml+xml,application/xml;'
                       'q=0.9,*/*;q=0.8'),
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }

        try:
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                print("   📱 กำลังใช้ Mobile User Agent...")
                async with session.get(url, headers=mobile_headers) as response:
                    if response.status == 200:
                        content = await response.text()
                        print(
                            f"   ✅ Mobile UA สำเร็จ! Status: {response.status}")

                        await self._extract_csrf_tokens(content, url, "mobile_ua")
                        await self._extract_endpoints(content, url, "mobile_ua")
                    else:
                        print(
                            f"   ❌ Mobile UA failed: Status {response.status}")

        except Exception as e:
            print(f"   ❌ Mobile UA error: {e}")

    async def _hunt_from_archives(self, url):
        """ค้นหาจาก archived/cached versions"""
        archive_urls = [
            f"https://web.archive.org/web/2023/{url}",
            f"https://webcache.googleusercontent.com/search?q=cache:{url}",
        ]

        async with aiohttp.ClientSession() as session:
            for archive_url in archive_urls:
                try:
                    headers = self.get_stealth_headers()
                    print(f"   💾 Testing archive: {archive_url}")

                    async with session.get(archive_url, headers=headers, timeout=30) as response:
                        if response.status == 200:
                            content = await response.text()
                            print(f"   ✅ Archive success!")

                            await self._extract_csrf_tokens(content, archive_url, "archive")
                            await self._extract_endpoints(content, archive_url, "archive")
                        else:
                            print(f"   ⚠️  Archive status: {response.status}")

                    await asyncio.sleep(random.uniform(1, 3))

                except Exception as e:
                    print(f"   ❌ Archive error: {e}")
                    continue

    async def _extract_csrf_tokens(self, content, url, method):
        """ดึง CSRF tokens จาก content"""
        # Instagram-specific CSRF patterns (ขั้นสูง)
        csrf_patterns = [
            r'"csrf_token":"([^"]+)"',
            r'csrftoken["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'_token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'authenticity_token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'<input[^>]*name=["\']([^"\']*csrf[^"\']*)["\'][^>]*value=["\']([^"\']+)["\']',
            r'<meta[^>]*name=["\']([^"\']*csrf[^"\']*)["\'][^>]*content=["\']([^"\']+)["\']',
            r'window\._sharedData\s*=\s*[^;]*csrf_token["\']?:\s*["\']([^"\']+)["\']',
            r'__igCsrfToken["\']?\s*[:=]\s*["\']([^"\']+)["\']'
        ]

        tokens_found = 0
        for pattern in csrf_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                if len(match.groups()) == 1:
                    token_value = match.group(1)
                    token_name = "csrf_token"
                elif len(match.groups()) == 2:
                    token_name, token_value = match.groups()
                else:
                    continue

                # Filter out invalid tokens
                if len(token_value) > 10 and not any(char in token_value for char in ['<', '>', '{', '}']):
                    # Check if we already have this token
                    if not any(t['value'] == token_value for t in self.found_tokens):
                        self.found_tokens.append({
                            'name': token_name,
                            'value': token_value,
                            'source': url,
                            'method': method
                        })
                        tokens_found += 1
                        token_preview = token_value[:25] + \
                            "..." if len(token_value) > 25 else token_value
                        print(
                            f"   🔑 Found Token: {token_name} = {token_preview} ({method})")

        if tokens_found > 0:
            print(f"   🎯 Method {method}: เจอ {tokens_found} CSRF tokens!")

    async def _extract_endpoints(self, content, url, method):
        """ดึง API endpoints จาก content"""
        # Instagram API patterns (ขั้นสูง)
        endpoint_patterns = [
            r'["\'/](api/v1/[^"\'>\s]+)',
            r'["\'/](ajax/[^"\'>\s]+)',
            r'["\'/](graphql[^"\'>\s]*)',
            r'["\'/](query[^"\'>\s]*)',
            r'fetch\(["\']([^"\']+)["\']',
            r'url["\']?\s*:\s*["\']([^"\']+)["\']',
            r'endpoint["\']?\s*:\s*["\']([^"\']+)["\']',
            r'action["\']?\s*:\s*["\']([^"\']+)["\']'
        ]

        endpoints_found = 0
        unique_endpoints = set()

        for pattern in endpoint_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                endpoint = match.group(1)

                # Clean และ normalize endpoint
                if not endpoint.startswith(('http', '//')):
                    if endpoint.startswith('/'):
                        full_endpoint = f"https://www.instagram.com{endpoint}"
                    else:
                        full_endpoint = f"https://www.instagram.com/{endpoint}"
                else:
                    full_endpoint = endpoint

                # Filter Instagram endpoints only
                if (full_endpoint not in unique_endpoints and
                    'instagram.com' in full_endpoint and
                        not any(ext in full_endpoint for ext in ['.js', '.css', '.png', '.jpg', '.gif'])):

                    unique_endpoints.add(full_endpoint)
                    self.found_endpoints.append({
                        'url': full_endpoint,
                        'method': 'GET',
                        'source': method,
                        'found_in': url
                    })
                    endpoints_found += 1
                    print(f"   🌐 Found Endpoint: {full_endpoint} ({method})")

        if endpoints_found > 0:
            print(f"   🎯 Method {method}: เจอ {endpoints_found} endpoints!")

    def generate_advanced_report(self):
        """สร้างรายงานขั้นสูง"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report = f"""
🔥 Advanced Instagram CSRF & Endpoint Hunt Report 🔥
⏰ เวลา: {timestamp}
🎯 Target: Instagram Profile Analysis
💕 โดย: Advanced Instagram Hunter Framework
{'='*60}

🔑 CSRF TOKENS DISCOVERED: {len(self.found_tokens)} tokens
{'='*60}
"""

        if self.found_tokens:
            for i, token in enumerate(self.found_tokens, 1):
                token_preview = token['value'][:40] + \
                    "..." if len(token['value']) > 40 else token['value']
                report += f"""
Token #{i}:
   🏷️  Name: {token['name']}
   🔐 Value: {token_preview}
   📍 Method: {token['method']}
   🔗 Source: {token['source']}
"""
        else:
            report += "\n❌ No CSRF tokens found (might be heavily protected)\n"

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
   🔍 Discovered in: {endpoint['found_in']}
"""
        else:
            report += "\n❌ No API endpoints found\n"

        # Analysis และ recommendations
        report += f"""

🎯 ANALYSIS & RECOMMENDATIONS:
{'='*60}
"""

        if self.found_tokens:
            report += "✅ CSRF tokens discovered - can proceed with authenticated requests\n"
            report += "🔥 Try using these tokens for Instagram API interactions\n"
            report += "⚠️  Remember to handle token expiration and refresh\n"
        else:
            report += "⚠️  No CSRF tokens found - Instagram might be using:\n"
            report += "   - Advanced bot detection\n"
            report += "   - IP-based rate limiting\n"
            report += "   - Cloudflare protection\n"
            report += "   - Try different IP/proxy\n"

        if self.found_endpoints:
            report += f"\n✅ {len(self.found_endpoints)} API endpoints discovered\n"
            report += "🔥 These endpoints can be used for further reconnaissance\n"
            report += "⚠️  Test each endpoint for CSRF requirements\n"

        report += f"""

💡 NEXT STEPS:
{'='*60}
1. 🔑 Use found CSRF tokens in requests
2. 🌐 Test discovered endpoints
3. 🔄 Implement token refresh mechanism  
4. 🕵️  Monitor for new endpoints
5. 🛡️  Implement proper rate limiting

{'='*60}
💖 Hunt completed by Advanced Instagram Hunter
⚠️  Use responsibly and ethically only!
{'='*60}
"""

        return report


async def main():
    """Main function"""
    print("🔥 Advanced Instagram CSRF Hunter 🔥")
    print("💕 Rate Limit Bypass & Advanced Detection")
    print("="*50)

    # รับ URL จาก command line หรือ input
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = input("🎯 ใส่ Instagram URL: ").strip()

    if not target_url:
        target_url = "https://www.instagram.com/alx.trading/"
        print(f"ใช้ตัวอย่าง: {target_url}")

    # สร้าง advanced hunter และเริ่มล่า
    hunter = AdvancedInstagramHunter()
    await hunter.bypass_rate_limit_hunt(target_url)

    # สร้างรายงานขั้นสูง
    report = hunter.generate_advanced_report()
    print(report)

    # บันทึกรายงาน
    timestamp = int(time.time())
    report_file = f"advanced_instagram_hunt_{timestamp}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"📄 รายงานขั้นสูงบันทึกแล้ว: {report_file}")

    # แสดงสรุปสำคัญ
    print(f"\n🎯 SUMMARY:")
    print(f"🔑 CSRF Tokens: {len(hunter.found_tokens)}")
    print(f"🌐 API Endpoints: {len(hunter.found_endpoints)}")

    if hunter.found_tokens:
        print(f"✅ SUCCESS: Found working CSRF tokens!")
        print(f"💡 Next: Use these tokens for Instagram API requests")
    else:
        print(f"⚠️  No tokens found - try different approach/proxy")


if __name__ == "__main__":
    asyncio.run(main())
