# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🎯 IMPROVED DM EXTRACTOR WITH RATE LIMITING PROTECTION
=====================================================
✨ แก้ไขปัญหา HTTP 429 แบบ girly-cute ✨

Features:
- Smart request with exponential backoff
- Retry-After header detection
- Random delays to avoid pattern detection
- Rate limiting protection
- Advanced session management
"""

import requests
import json
import time
import random
from datetime import datetime
import os

class CuteRateLimitProtectedExtractor:
    """💕 Cute DM Extractor with rate limiting protection 💕"""

    def __init__(self):
        self.target = "alx.trading"
        self.base_delay = 5  # Base delay between requests (seconds)
        self.max_retry = 3   # Maximum retry attempts
        self.last_request_time = 0

        # Load valid sessions
        self.sessions = self.load_sessions()
        print(f"💖 Loaded {len(self.sessions)} sessions")

    def load_sessions(self):
        """💕 Load all valid sessions"""
        sessions = []
        session_files = [
            '/workspaces/sugarglitch-realops/sessions/session-alx.trading',
            '/workspaces/sugarglitch-realops/sessions_regenerated/quick_bypass_session.json'
        ]

        for file_path in session_files:
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        sessions.append({
                            'file': os.path.basename(file_path),
                            'path': file_path,
                            'cookies': data.get('cookies', {})
                        })
                        print(f"✅ Loaded: {os.path.basename(file_path)}")
            except Exception as e:
                print(f"❌ Failed to load {file_path}: {e}")

        return sessions

    def cute_request(self, url, headers, session_name="unknown"):
        """💖 Cute request with smart rate limiting protection 💖"""

        # Rate limiting protection - ensure minimum delay
        elapsed = time.time() - self.last_request_time
        if elapsed < self.base_delay:
            sleep_time = self.base_delay - elapsed
            print(f"   ⏰ Rate limiting protection: waiting {sleep_time:.1f}s ✨")
            time.sleep(sleep_time)

        retry_count = 0
        while retry_count < self.max_retry:
            try:
                # Add cute random jitter 💕
                jitter = random.uniform(1.0, 3.0)
                if retry_count > 0:
                    print(f"   🔄 Retry {retry_count}/{self.max_retry} with {jitter:.1f}s jitter 💝")
                    time.sleep(jitter)

                self.last_request_time = time.time()
                print(f"   📡 Requesting: {url[:50]}... (Session: {session_name}) 💖")

                # Make the request
                response = requests.get(url, headers=headers, timeout=30)

                # Handle HTTP 429 - Too Many Requests 🛡️
                if response.status_code == 429:
                    print(f"   💔 HTTP 429 - Too Many Requests! (Session: {session_name})")

                    # Check for Retry-After header (Instagram sometimes provides this)
                    retry_after = response.headers.get('Retry-After')
                    if retry_after:
                        wait_time = int(retry_after)
                        print(f"   💤 Server says wait {wait_time}s (Retry-After header) 😴")
                        time.sleep(wait_time)
                    else:
                        # Exponential backoff with cute randomization
                        wait_time = random.uniform(10, 25) * (retry_count + 1)
                        print(f"   💤 Exponential backoff: waiting {wait_time:.1f}s 😴✨")
                        time.sleep(wait_time)

                    retry_count += 1
                    continue

                # Success responses 🎉
                elif response.status_code in [200, 201]:
                    print(f"   ✅ Success! HTTP {response.status_code} - {len(response.content)} bytes 🎉")
                    return response

                # Other responses (404, etc.) 📝
                else:
                    print(f"   📝 HTTP {response.status_code} - {len(response.content)} bytes")
                    if retry_count < self.max_retry - 1:
                        wait_time = random.uniform(3, 8)
                        print(f"   ⏰ Retrying after {wait_time:.1f}s... 💫")
                        time.sleep(wait_time)
                        retry_count += 1
                        continue
                    return response

            except requests.RequestException as e:
                print(f"   💥 Request error: {e}")
                if retry_count < self.max_retry - 1:
                    wait_time = random.uniform(5, 12)
                    print(f"   ⏰ Network retry after {wait_time:.1f}s... 🌸")
                    time.sleep(wait_time)
                    retry_count += 1
                    continue
                raise

        # If we get here, all retries failed 😢
        print(f"   😢 All retry attempts failed for {url}")
        return response if 'response' in locals() else None

    def create_cute_headers(self, session_data):
        """💕 Create cute headers with session cookies"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }

        # Add session cookies 🍪
        if session_data['cookies']:
            cookie_str = '; '.join([f"{k}={v}" for k, v in session_data['cookies'].items()])
            headers['Cookie'] = cookie_str
            print(f"   🍪 Added cookies from {session_data['file']}")

        return headers

    def test_instagram_access(self):
        """💖 Test Instagram access with rate limiting protection"""
        print("\\n💕 TESTING INSTAGRAM ACCESS WITH RATE LIMITING PROTECTION 💕")
        print("=" * 65)

        test_urls = [
            ('Basic Instagram', 'https://www.instagram.com/'),
            ('Target Profile', f'https://www.instagram.com/{self.target}/'),
            ('Direct Messages', 'https://www.instagram.com/direct/inbox/'),
            ('GraphQL API', 'https://www.instagram.com/api/graphql/'),
        ]

        results = []

        for session_data in self.sessions[:2]:  # Test first 2 sessions
            print(f"\\n🎀 Testing session: {session_data['file']} 🎀")
            print("-" * 50)

            headers = self.create_cute_headers(session_data)

            for test_name, url in test_urls:
                print(f"\\n💝 {test_name}:")

                try:
                    response = self.cute_request(url, headers, session_data['file'])

                    if response:
                        result = {
                            'session': session_data['file'],
                            'test': test_name,
                            'url': url,
                            'status_code': response.status_code,
                            'response_size': len(response.content),
                            'success': response.status_code in [200, 201],
                            'timestamp': datetime.now().isoformat()
                        }

                        # Analyze response for interesting content
                        if response.status_code == 200:
                            content = response.text.lower()
                            result['analysis'] = {
                                'contains_login': 'login' in content,
                                'contains_messages': 'message' in content,
                                'contains_inbox': 'inbox' in content,
                                'contains_user_data': 'user' in content,
                                'is_json': response.headers.get('content-type', '').startswith('application/json')
                            }

                        results.append(result)
                        print(f"   📊 Result logged! ✨")

                    else:
                        print(f"   😢 No response received")

                except Exception as e:
                    print(f"   💥 Error: {e}")

                # Delay between tests for rate limiting protection
                print(f"   💤 Sleeping 3-7s between tests... 😴")
                time.sleep(random.uniform(3, 7))

        # Save results
        timestamp = int(time.time())
        output_file = f"/workspaces/sugarglitch-realops/cute_rate_limit_test_{timestamp}.json"

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'test_info': {
                    'target': self.target,
                    'timestamp': datetime.now().isoformat(),
                    'method': 'cute_rate_limiting_protection',
                    'sessions_tested': len(self.sessions),
                    'total_tests': len(results)
                },
                'results': results
            }, f, indent=2, ensure_ascii=False)

        print(f"\\n🎉 TESTING COMPLETED! 🎉")
        print(f"📁 Results saved: {output_file}")
        print(f"📊 Total tests: {len(results)}")
        print(f"✅ Successful requests: {sum(1 for r in results if r['success'])}")
        print(f"❌ Failed requests: {sum(1 for r in results if not r['success'])}")

        # Summary of HTTP status codes
        status_codes = {}
        for result in results:
            code = result['status_code']
            status_codes[code] = status_codes.get(code, 0) + 1

        print("\\n📈 Status Code Summary:")
        for code, count in sorted(status_codes.items()):
            emoji = "✅" if code in [200, 201] else "⚠️" if code == 429 else "📝"
            print(f"   {emoji} HTTP {code}: {count} requests")

        return results

def main():
    """💖 Main cute function 💖"""
    print("🌸✨ CUTE INSTAGRAM DM EXTRACTOR WITH RATE LIMITING PROTECTION ✨🌸")
    print("=" * 70)
    print("💕 Fixing HTTP 429 issues with girly-cute techniques! 💕")
    print()

    extractor = CuteRateLimitProtectedExtractor()
    results = extractor.test_instagram_access()

    print("\\n💖 All done! Hope this fixes the 429 issues! 💖")
    print("🌸 Remember: patience is key for rate limiting! 🌸")

if __name__ == "__main__":
    main()