#!/usr/bin/env python3
"""
🔑 CSRF TOKEN TEST - ทดสอบการดึง CSRF token จริง
"""

import asyncio
import aiohttp
import re
from fake_useragent import UserAgent


async def test_csrf_extraction():
    print("🔑 Testing CSRF Token Extraction from Instagram...")
    print("="*60)

    ua = UserAgent()

    headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    async with aiohttp.ClientSession(headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as session:
        try:
            print("📡 Connecting to Instagram...")
            async with session.get('https://www.instagram.com/') as response:
                print(f"📊 HTTP Status: {response.status}")
                print(f"📏 Response Headers: {dict(response.headers)}")

                if response.status == 200:
                    text = await response.text()
                    print(f"📄 Page Length: {len(text)} characters")

                    # ทดสอบหลายรูปแบบการหา CSRF token
                    patterns = {
                        'Pattern 1': r'"csrf_token":"([^"]+)"',
                        'Pattern 2': r'csrf_token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                        'Pattern 3': r'csrftoken["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                        'Pattern 4': r'window\._sharedData\s*=\s*[^}]*"csrf_token":"([^"]+)"'
                    }

                    found_tokens = []

                    for pattern_name, pattern in patterns.items():
                        matches = re.findall(pattern, text, re.IGNORECASE)
                        if matches:
                            for token in matches:
                                if len(token) > 10:  # Token ต้องมีความยาวมากกว่า 10
                                    found_tokens.append((pattern_name, token))
                                    print(
                                        f"✅ {pattern_name}: {token[:8]}...{token[-4:]} (length: {len(token)})")

                    if found_tokens:
                        print(
                            f"\n🎉 Found {len(found_tokens)} potential CSRF tokens!")

                        # ทดสอบ token แรก
                        best_token = found_tokens[0][1]
                        print(
                            f"🔑 Best Token: {best_token[:12]}...{best_token[-6:]}")

                        # ตรวจสอบลักษณะของ token
                        print(f"📊 Token Analysis:")
                        print(f"   Length: {len(best_token)}")
                        print(
                            f"   Contains digits: {'Yes' if any(c.isdigit() for c in best_token) else 'No'}")
                        print(
                            f"   Contains letters: {'Yes' if any(c.isalpha() for c in best_token) else 'No'}")
                        print(
                            f"   Contains special chars: {'Yes' if any(not c.isalnum() for c in best_token) else 'No'}")

                        # ทดสอบใช้ token นี้ในการส่ง request
                        await test_token_usage(session, best_token)

                    else:
                        print("❌ No CSRF tokens found!")

                        # Debug: แสดงส่วนของหน้าเว็บ
                        print("\n📄 Page content sample:")
                        lines = text.split('\n')[:20]
                        for i, line in enumerate(lines):
                            print(f"{i+1:2d}: {line[:100]}")

                        # ค้นหาคำว่า csrf หรือ token
                        csrf_mentions = []
                        for i, line in enumerate(text.split('\n')):
                            if 'csrf' in line.lower() or 'token' in line.lower():
                                csrf_mentions.append(
                                    f"Line {i+1}: {line.strip()[:150]}")

                        if csrf_mentions:
                            print("\n🔍 Lines containing 'csrf' or 'token':")
                            for mention in csrf_mentions[:10]:
                                print(f"   {mention}")

                else:
                    print(
                        f"❌ Failed to access Instagram: HTTP {response.status}")

        except Exception as e:
            print(f"💥 Error: {e}")


async def test_token_usage(session, token):
    """ทดสอบใช้ CSRF token"""
    print(f"\n🧪 Testing CSRF token usage...")

    headers = {
        'X-CSRFToken': token,
        'X-Instagram-AJAX': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.instagram.com/'
    }

    # ทดสอบส่ง request ง่ายๆ (ไม่ใช่ login จริง)
    test_data = {'test': 'csrf_validation'}

    try:
        # ส่งไปหน้าที่ต้องการ CSRF (อาจจะได้ response ที่บอกว่า token ถูกต้องหรือไม่)
        async with session.post(
            'https://www.instagram.com/api/v1/web/accounts/login/ajax/',
            data=test_data,
            headers=headers
        ) as response:

            print(f"🧪 Test Status: {response.status}")
            response_text = await response.text()

            if response.status == 403:
                print("⚠️ CSRF token rejected (403 Forbidden)")
            elif response.status == 400:
                print(
                    "✅ CSRF token accepted (400 Bad Request - missing required fields)")
            elif response.status == 200:
                print("✅ CSRF token accepted (200 OK)")
            else:
                print(f"🤔 Unexpected response: {response.status}")

            print(f"📄 Response preview: {response_text[:200]}")

    except Exception as e:
        print(f"💥 Token test error: {e}")


async def main():
    await test_csrf_extraction()

if __name__ == "__main__":
    asyncio.run(main())
