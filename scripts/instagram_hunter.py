#!/usr/bin/env python3
"""
🌸 Quick Instagram CSRF & Endpoint Hunter 🌸
เวอร์ชันเร็วสำหรับ Instagram โดยเฉพาะ
"""

import asyncio
import aiohttp
import re
import time
from datetime import datetime
from fake_useragent import UserAgent
import sys


class InstagramHunter:
    def __init__(self):
        self.ua = UserAgent()
        self.found_tokens = []
        self.found_endpoints = []

    async def hunt_instagram(self, url):
        """ล่า CSRF tokens และ endpoints จาก Instagram"""
        print(f"🌸 เริ่มล่า CSRF tokens และ endpoints จาก: {url}")
        print("="*60)

        async with aiohttp.ClientSession() as session:
            # เตรียม headers แบบ Instagram
            headers = {
                'User-Agent': self.ua.random,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }

            try:
                # 1. เข้าสู่หน้า profile
                print(f"📱 กำลังเข้าสู่ Instagram profile...")
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        content = await response.text()
                        print(f"✅ เข้าได้แล้ว! Status: {response.status}")
                        print(f"📊 Content size: {len(content)} bytes")

                        # ค้นหา CSRF tokens
                        await self._hunt_csrf_tokens(content, url)

                        # ค้นหา endpoints
                        await self._hunt_endpoints(content, url)

                        # ค้นหา login page
                        await self._hunt_login_page(session, headers)

                    else:
                        print(f"❌ ไม่สามารถเข้าได้: Status {response.status}")

            except Exception as e:
                print(f"❌ Error: {e}")

    async def _hunt_csrf_tokens(self, content, url):
        """ล่า CSRF tokens"""
        print(f"\n🔑 กำลังล่า CSRF tokens...")

        # Instagram-specific CSRF patterns
        csrf_patterns = [
            r'"csrf_token":"([^"]+)"',
            r'csrftoken["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'_token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'<input[^>]*name=["\']([^"\']*csrf[^"\']*)["\'][^>]*value=["\']([^"\']+)["\']',
            r'<meta[^>]*name=["\']([^"\']*csrf[^"\']*)["\'][^>]*content=["\']([^"\']+)["\']'
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

                if len(token_value) > 10:  # Filter out short values
                    self.found_tokens.append({
                        'name': token_name,
                        'value': token_value,
                        'source': url,
                        'method': 'main_page'
                    })
                    tokens_found += 1
                    token_preview = token_value[:20] + \
                        "..." if len(token_value) > 20 else token_value
                    print(f"   ✅ Token: {token_name} = {token_preview}")

        print(f"🎯 เจอ CSRF tokens: {tokens_found} ตัว")

    async def _hunt_endpoints(self, content, url):
        """ล่า API endpoints"""
        print(f"\n🌐 กำลังล่า API endpoints...")

        # Instagram API patterns
        endpoint_patterns = [
            r'["\'/](api/[^"\'>\s]+)',
            r'["\'/](ajax/[^"\'>\s]+)',
            r'["\'/](graphql[^"\'>\s]*)',
            r'fetch\(["\']([^"\']+)["\']',
            r'url["\']?\s*:\s*["\']([^"\']+)["\']',
            r'endpoint["\']?\s*:\s*["\']([^"\']+)["\']'
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

                if full_endpoint not in unique_endpoints and 'instagram.com' in full_endpoint:
                    unique_endpoints.add(full_endpoint)
                    self.found_endpoints.append({
                        'url': full_endpoint,
                        'method': 'GET',
                        'source': 'main_page'
                    })
                    endpoints_found += 1
                    print(f"   ✅ Endpoint: {full_endpoint}")

        print(f"🎯 เจอ endpoints: {endpoints_found} ตัว")

    async def _hunt_login_page(self, session, headers):
        """ล่า CSRF tokens จากหน้า login"""
        print(f"\n🔐 กำลังล่า CSRF tokens จากหน้า login...")

        login_url = "https://www.instagram.com/accounts/login/"
        try:
            async with session.get(login_url, headers=headers) as response:
                if response.status == 200:
                    login_content = await response.text()
                    print(f"✅ เข้าหน้า login ได้แล้ว!")

                    # ค้นหา CSRF tokens ในหน้า login
                    login_patterns = [
                        r'"csrf_token":"([^"]+)"',
                        r'<input[^>]*name=["\']csrfmiddlewaretoken["\'][^>]*value=["\']([^"\']+)["\']',
                        r'<input[^>]*name=["\']_token["\'][^>]*value=["\']([^"\']+)["\']'
                    ]

                    login_tokens = 0
                    for pattern in login_patterns:
                        matches = re.finditer(
                            pattern, login_content, re.IGNORECASE)
                        for match in matches:
                            token_value = match.group(1)
                            if len(token_value) > 10:
                                self.found_tokens.append({
                                    'name': 'login_csrf_token',
                                    'value': token_value,
                                    'source': login_url,
                                    'method': 'login_page'
                                })
                                login_tokens += 1
                                token_preview = token_value[:20] + "..." if len(
                                    token_value) > 20 else token_value
                                print(f"   ✅ Login Token: {token_preview}")

                    print(f"🎯 เจอ login CSRF tokens: {login_tokens} ตัว")

        except Exception as e:
            print(f"❌ ไม่สามารถเข้าหน้า login: {e}")

    def generate_quick_report(self):
        """สร้างรายงานสรุปแบบเร็ว"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        report = f"""
🌸 Instagram CSRF & Endpoint Hunt Report 🌸
⏰ เวลา: {timestamp}
{'='*50}

🔑 CSRF Tokens พบ: {len(self.found_tokens)} ตัว
"""

        for i, token in enumerate(self.found_tokens, 1):
            token_preview = token['value'][:30] + \
                "..." if len(token['value']) > 30 else token['value']
            report += f"   {i}. {token['name']}: {token_preview}\n"
            report += f"      Source: {token['source']} ({token['method']})\n\n"

        report += f"""
🌐 API Endpoints พบ: {len(self.found_endpoints)} ตัว
"""

        for i, endpoint in enumerate(self.found_endpoints, 1):
            report += f"   {i}. {endpoint['url']}\n"

        report += f"""
{'='*50}
💖 Hunt completed! โดย Instagram Hunter Framework
"""

        return report


async def main():
    """Main function"""
    print("🌸 Instagram CSRF & Endpoint Hunter 🌸")
    print("💕 โดยเฉพาะสำหรับน้อง chin4d0ll!")
    print("="*50)

    # รับ URL จาก command line หรือ input
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = input("🎯 ใส่ Instagram URL: ").strip()

    if not target_url:
        target_url = "https://www.instagram.com/alx.trading/"
        print(f"ใช้ตัวอย่าง: {target_url}")

    # สร้าง hunter และเริ่มล่า
    hunter = InstagramHunter()
    await hunter.hunt_instagram(target_url)

    # สร้างรายงาน
    report = hunter.generate_quick_report()
    print(report)

    # บันทึกรายงาน
    timestamp = int(time.time())
    report_file = f"instagram_hunt_{timestamp}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"📄 รายงานบันทึกแล้ว: {report_file}")


if __name__ == "__main__":
    asyncio.run(main())
