#!/usr/bin/env python3
"""
🔥💥 ULTIMATE Instagram CSRF Hunter with Proxy Rotation 💥🔥
เวอร์ชันสุดท้าย ที่แก้ปัญหา Rate Limit ด้วย IP rotation และ stealth techniques
"""

import asyncio
import aiohttp
import re
import time
import random
from datetime import datetime
import cloudscraper
import requests
import sys
from itertools import cycle


class UltimateInstagramHunter:
    def __init__(self):
        self.found_tokens = []
        self.found_endpoints = []
        self.proxy_list = self._get_proxy_list()
        self.proxy_cycle = cycle(self.proxy_list) if self.proxy_list else None

    def _get_proxy_list(self):
        """รายการ free proxies สำหรับ IP rotation"""
        # Free proxy list (ใน production ควรใช้ proxy service จริง)
        proxies = [
            "8.210.83.33:80",
            "47.74.152.29:8888",
            "103.149.162.194:80",
            "154.236.184.70:1981",
            "91.107.233.107:8080",
            "103.127.1.130:80",
            "154.236.191.44:1976",
            "41.65.236.53:1976"
        ]
        return proxies

    def get_random_headers(self):
        """สร้าง random headers เพื่อหลบ detection"""
        user_agents = [
            ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/91.0.4472.124 Safari/537.36'),
            ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/91.0.4472.124 Safari/537.36'),
            ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
             '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'),
            ('Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) '
             'AppleWebKit/605.1.15 (KHTML, like Gecko) '
             'Version/14.0 Mobile/15E148 Safari/604.1'),
            ('Mozilla/5.0 (Android 11; Mobile; rv:68.0) '
             'Gecko/68.0 Firefox/88.0')
        ]

        return {
            'User-Agent': random.choice(user_agents),
            'Accept': ('text/html,application/xhtml+xml,application/xml;'
                       'q=0.9,image/webp,*/*;q=0.8'),
            'Accept-Language': random.choice([
                'en-US,en;q=0.9',
                'en-GB,en;q=0.9',
                'en-CA,en;q=0.9'
            ]),
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': random.choice([
                'max-age=0',
                'no-cache',
                'must-revalidate'
            ]),
            'DNT': '1'
        }

    async def test_single_request(self, url, method="direct"):
        """ทดสอบ request เดี่ยวๆ"""
        try:
            headers = self.get_random_headers()

            if method == "proxy" and self.proxy_cycle:
                proxy = next(self.proxy_cycle)
                print(f"   🔄 ใช้ proxy: {proxy}")

                # ใช้ requests กับ proxy
                proxies = {
                    'http': f'http://{proxy}',
                    'https': f'http://{proxy}'
                }
                response = requests.get(url, headers=headers,
                                        proxies=proxies, timeout=30)

                if response.status_code == 200:
                    print(f"   ✅ Proxy success! Size: {len(response.text)}")
                    await self._extract_data(response.text, url, method)
                    return True
                else:
                    print(f"   ⚠️  Proxy status: {response.status_code}")
                    return False

            elif method == "cloudscraper":
                scraper = cloudscraper.create_scraper()
                response = scraper.get(url, headers=headers, timeout=30)

                if response.status_code == 200:
                    print(
                        f"   ✅ Cloudscraper success! Size: {len(response.text)}")
                    await self._extract_data(response.text, url, method)
                    return True
                else:
                    print(
                        f"   ⚠️  Cloudscraper status: {response.status_code}")
                    return False

            else:  # direct request
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers) as response:
                        if response.status == 200:
                            content = await response.text()
                            print(f"   ✅ Direct success! Size: {len(content)}")
                            await self._extract_data(content, url, method)
                            return True
                        else:
                            print(f"   ⚠️  Direct status: {response.status}")
                            return False

        except Exception as e:
            print(f"   ❌ Error in {method}: {e}")
            return False

    async def ultimate_hunt(self, url):
        """Ultimate hunting strategy"""
        print("🔥💥 ULTIMATE Instagram CSRF Hunt เริ่มแล้ว! 💥🔥")
        print(f"🎯 Target: {url}")
        print("="*60)

        # Strategy 1: ลองทุก method
        methods = ["direct", "cloudscraper", "proxy"]

        for method in methods:
            print(f"\n🚀 Method: {method.upper()}")
            success = await self.test_single_request(url, method)

            if success:
                print(f"🎉 {method} method สำเร็จ!")
            else:
                print(f"💥 {method} method ล้มเหลว")

            # Random delay ระหว่าง method
            delay = random.uniform(3, 8)
            print(f"⏳ รอ {delay:.1f} วินาที...")
            await asyncio.sleep(delay)

        # Strategy 2: ลอง alternative URLs
        print(f"\n🌐 ลอง Alternative URLs...")
        alt_urls = [
            url.replace('www.instagram.com', 'm.instagram.com'),
            'https://www.instagram.com/accounts/login/',
            'https://www.instagram.com/',
            'https://i.instagram.com/',
            url + '?__a=1'
        ]

        for alt_url in alt_urls:
            print(f"🔍 Testing: {alt_url}")
            success = await self.test_single_request(alt_url, "direct")

            if success:
                print(f"🎉 Alternative URL สำเร็จ!")
                break

            await asyncio.sleep(random.uniform(2, 4))

    async def _extract_data(self, content, url, method):
        """Extract CSRF tokens และ endpoints จาก content"""
        # Extract CSRF tokens
        csrf_patterns = [
            r'"csrf_token":"([^"]+)"',
            r'csrftoken["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'_token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'window\._sharedData.*?"csrf_token":"([^"]+)"'
        ]

        token_found = False
        for pattern in csrf_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                token = match.group(1)
                if len(token) > 10:
                    self.found_tokens.append({
                        'token': token,
                        'source': url,
                        'method': method
                    })
                    token_preview = token[:30] + \
                        "..." if len(token) > 30 else token
                    print(f"   🔑 CSRF Token: {token_preview}")
                    token_found = True

        # Extract endpoints
        endpoint_patterns = [
            r'["\'/](api/v1/[^"\'>\s]+)',
            r'["\'/](ajax/[^"\'>\s]+)',
            r'["\'/](graphql[^"\'>\s]*)',
            r'action["\']?\s*:\s*["\']([^"\']+)["\']'
        ]

        endpoint_found = False
        unique_endpoints = set()

        for pattern in endpoint_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                endpoint = match.group(1)
                if not endpoint.startswith('http'):
                    full_endpoint = f"https://www.instagram.com{endpoint}"
                else:
                    full_endpoint = endpoint

                if (full_endpoint not in unique_endpoints and
                        'instagram.com' in full_endpoint):
                    unique_endpoints.add(full_endpoint)
                    self.found_endpoints.append({
                        'url': full_endpoint,
                        'source': method
                    })
                    print(f"   🌐 Endpoint: {full_endpoint}")
                    endpoint_found = True

        return token_found or endpoint_found

    def generate_report(self):
        """สร้างรายงานผลลัพธ์"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report = f"""
🔥💥 ULTIMATE Instagram CSRF Hunt Report 💥🔥
⏰ เวลา: {timestamp}
🎯 Hunt completed by Ultimate Hunter Framework
{'='*60}

🔑 CSRF TOKENS FOUND: {len(self.found_tokens)}
{'='*60}
"""

        if self.found_tokens:
            for i, token_data in enumerate(self.found_tokens, 1):
                token_preview = (token_data['token'][:50] + "..."
                                 if len(token_data['token']) > 50
                                 else token_data['token'])
                report += f"""
Token #{i}:
   🔐 Value: {token_preview}
   📍 Method: {token_data['method']}
   🔗 Source: {token_data['source']}
"""
        else:
            report += "\n❌ No CSRF tokens found\n"

        report += f"""

🌐 API ENDPOINTS FOUND: {len(self.found_endpoints)}
{'='*60}
"""

        if self.found_endpoints:
            for i, endpoint in enumerate(self.found_endpoints, 1):
                report += f"""
Endpoint #{i}:
   🔗 URL: {endpoint['url']}
   📍 Found via: {endpoint['source']}
"""
        else:
            report += "\n❌ No endpoints found\n"

        report += f"""

🎯 ANALYSIS:
{'='*60}
"""

        if self.found_tokens:
            report += "✅ SUCCESS! CSRF tokens discovered\n"
            report += "🔥 These tokens can be used for Instagram API calls\n"
            report += "💡 Remember to handle token expiration\n"
        else:
            report += "⚠️  No tokens found - Instagram has strong protection\n"
            report += "💡 Consider using different IP ranges or proxy services\n"

        if self.found_endpoints:
            report += f"\n✅ {len(self.found_endpoints)} API endpoints discovered\n"
            report += "🔥 Use these for further reconnaissance\n"

        report += f"""

💡 RECOMMENDATIONS:
{'='*60}
1. 🔄 Use residential proxies for better success rate
2. 🕐 Implement proper timing between requests
3. 🎭 Rotate user agents and headers frequently
4. 📱 Try mobile-specific endpoints
5. 🔍 Monitor for new Instagram API changes

{'='*60}
💖 Ultimate Hunt completed!
⚠️  Use ethically and responsibly!
{'='*60}
"""

        return report


async def main():
    """Main execution function"""
    print("🔥💥 ULTIMATE Instagram CSRF Hunter 💥🔥")
    print("💕 With Proxy Rotation & Advanced Bypass")
    print("="*50)

    # Get target URL
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = input("🎯 ใส่ Instagram URL: ").strip()

    if not target_url:
        target_url = "https://www.instagram.com/alx.trading/"
        print(f"ใช้ target เริ่มต้น: {target_url}")

    # Create hunter และเริ่ม ultimate hunt
    hunter = UltimateInstagramHunter()
    await hunter.ultimate_hunt(target_url)

    # Generate และแสดงรายงาน
    report = hunter.generate_report()
    print(report)

    # Save report
    timestamp = int(time.time())
    report_file = f"ultimate_instagram_hunt_{timestamp}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"📄 Ultimate report saved: {report_file}")

    # Summary
    print(f"\n🎯 ULTIMATE SUMMARY:")
    print(f"🔑 CSRF Tokens: {len(hunter.found_tokens)}")
    print(f"🌐 API Endpoints: {len(hunter.found_endpoints)}")

    if hunter.found_tokens:
        print(f"🎉 SUCCESS! Found {len(hunter.found_tokens)} working tokens!")
        print(f"💡 Next: Use tokens for Instagram API automation")
    else:
        print(f"⚠️  Challenge: No tokens found, try different approach")


if __name__ == "__main__":
    asyncio.run(main())
