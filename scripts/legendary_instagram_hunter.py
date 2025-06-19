#!/usr/bin/env python3
"""
🔥💎 LEGENDARY Instagram Intelligence Hunter 💎🔥
เทคนิคขั้นสูงสุด! ใช้ third-party APIs และ cached data sources
"""

import asyncio
import aiohttp
import re
import time
import random
import json
from datetime import datetime
import requests
import sys


class LegendaryInstagramHunter:
    def __init__(self):
        self.found_data = []
        self.intelligence_sources = []

    async def legendary_hunt(self, username_or_url):
        """Hunt ขั้นสูงสุดด้วย multiple intelligence sources"""
        print("🔥💎 LEGENDARY Instagram Intelligence Hunt! 💎🔥")
        print(f"🎯 Target: {username_or_url}")
        print("="*60)

        # Extract username from URL
        username = self._extract_username(username_or_url)
        print(f"👤 Username detected: {username}")

        # Method 1: Public Instagram API (no auth required)
        print("\n🚀 Method 1: Public Instagram API Hunt...")
        await self._hunt_public_api(username)

        # Method 2: Social Media Intelligence APIs
        print("\n🔍 Method 2: Social Intelligence APIs...")
        await self._hunt_social_apis(username)

        # Method 3: Cached/Archive data
        print("\n💾 Method 3: Cached Data Mining...")
        await self._hunt_cached_data(username)

        # Method 4: OSINT Sources
        print("\n🕵️  Method 4: Open Source Intelligence...")
        await self._hunt_osint_sources(username)

        # Method 5: Alternative endpoints
        print("\n🌐 Method 5: Alternative Endpoint Discovery...")
        await self._hunt_alternative_endpoints(username)

    def _extract_username(self, url_or_username):
        """Extract username จาก URL หรือ username"""
        if 'instagram.com' in url_or_username:
            # Extract from URL like https://www.instagram.com/alx.trading/
            match = re.search(r'instagram\.com/([^/]+)', url_or_username)
            return match.group(1) if match else url_or_username
        else:
            return url_or_username

    async def _hunt_public_api(self, username):
        """ล่าข้อมูลจาก public Instagram API endpoints"""
        public_endpoints = [
            f"https://www.instagram.com/{username}/?__a=1",
            f"https://www.instagram.com/{username}/?__a=1&__d=dis",
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
            f"https://www.instagram.com/web/search/topsearch/?query={username}",
        ]

        for endpoint in public_endpoints:
            try:
                print(f"   🔍 Testing: {endpoint}")

                headers = {
                    'User-Agent': ('Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 '
                                   'like Mac OS X) AppleWebKit/605.1.15 '
                                   '(KHTML, like Gecko) Version/14.1.2 '
                                   'Mobile/15E148 Safari/604.1'),
                    'Accept': 'application/json',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'X-Instagram-AJAX': '1',
                    'X-Requested-With': 'XMLHttpRequest'
                }

                async with aiohttp.ClientSession() as session:
                    async with session.get(endpoint, headers=headers) as response:
                        if response.status == 200:
                            content = await response.text()

                            # Try to parse as JSON
                            try:
                                data = json.loads(content)
                                print(
                                    f"   ✅ JSON data retrieved! Size: {len(content)}")

                                # Extract useful information
                                info = self._extract_instagram_info(
                                    data, endpoint)
                                if info:
                                    self.found_data.append(info)
                                    print(f"   🎯 Information extracted!")

                            except json.JSONDecodeError:
                                # Not JSON, but might contain useful data
                                print(f"   ⚠️  HTML content retrieved, parsing...")
                                await self._parse_html_content(content, endpoint)

                        elif response.status == 429:
                            print(f"   ⏳ Rate limited: {endpoint}")
                        else:
                            print(f"   ❌ Status {response.status}: {endpoint}")

                # Delay between requests
                await asyncio.sleep(random.uniform(2, 5))

            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue

    async def _hunt_social_apis(self, username):
        """ล่าข้อมูลจาก social media APIs"""
        # ใช้ alternative social APIs ที่ไม่ต้อง authentication
        social_endpoints = [
            f"https://api.social-searcher.com/v2/search?q={username}&type=instagram",
            f"https://www.googleapis.com/customsearch/v1?q=site:instagram.com+{username}",
            # GitHub for cross-platform
            f"https://api.github.com/search/users?q={username}",
        ]

        for endpoint in social_endpoints:
            try:
                print(f"   🔍 Social API: {endpoint}")

                headers = {
                    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                                   'Chrome/91.0.4472.124 Safari/537.36')
                }

                # Use requests for better proxy support
                response = requests.get(endpoint, headers=headers, timeout=30)

                if response.status_code == 200:
                    print(f"   ✅ Social API success!")

                    # Try to parse response
                    try:
                        data = response.json()
                        social_info = {
                            'source': 'social_api',
                            'endpoint': endpoint,
                            'data': data,
                            'timestamp': datetime.now().isoformat()
                        }
                        self.found_data.append(social_info)
                        print(f"   🎯 Social data extracted!")

                    except:
                        # Store as text if not JSON
                        social_info = {
                            'source': 'social_api_text',
                            'endpoint': endpoint,
                            # First 1000 chars
                            'content': response.text[:1000],
                            'timestamp': datetime.now().isoformat()
                        }
                        self.found_data.append(social_info)

                await asyncio.sleep(random.uniform(1, 3))

            except Exception as e:
                print(f"   ❌ Social API error: {e}")
                continue

    async def _hunt_cached_data(self, username):
        """ล่าข้อมูลจาก cached และ archive sources"""
        cache_sources = [
            f"https://web.archive.org/web/*/instagram.com/{username}",
            f"https://webcache.googleusercontent.com/search?q=cache:instagram.com/{username}",
            f"https://archive.today/https://instagram.com/{username}",
        ]

        for source in cache_sources:
            try:
                print(f"   💾 Cache source: {source}")

                headers = {
                    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                   'AppleWebKit/537.36')
                }

                async with aiohttp.ClientSession() as session:
                    async with session.get(source, headers=headers) as response:
                        if response.status == 200:
                            content = await response.text()
                            print(
                                f"   ✅ Cache data found! Size: {len(content)}")

                            # Extract any useful patterns
                            await self._parse_html_content(content, source)

                        else:
                            print(f"   ⚠️  Cache status: {response.status}")

                await asyncio.sleep(random.uniform(2, 4))

            except Exception as e:
                print(f"   ❌ Cache error: {e}")
                continue

    async def _hunt_osint_sources(self, username):
        """ล่าข้อมูลจาก OSINT sources"""
        print(f"   🕵️  Gathering OSINT data for: {username}")

        # Manual OSINT patterns (ค้นหาข้อมูลที่เกี่ยวข้อง)
        osint_patterns = {
            'email_patterns': [
                f"{username}@gmail.com",
                f"{username}@yahoo.com",
                f"{username}@outlook.com",
                f"contact@{username}.com"
            ],
            'social_patterns': [
                f"https://twitter.com/{username}",
                f"https://facebook.com/{username}",
                f"https://linkedin.com/in/{username}",
                f"https://tiktok.com/@{username}"
            ],
            'domain_patterns': [
                f"{username}.com",
                f"{username}.net",
                f"www.{username}.com"
            ]
        }

        osint_data = {
            'source': 'osint_analysis',
            'username': username,
            'patterns': osint_patterns,
            'timestamp': datetime.now().isoformat()
        }

        self.found_data.append(osint_data)
        print(f"   🎯 OSINT patterns generated!")

    async def _hunt_alternative_endpoints(self, username):
        """ค้นหา alternative Instagram endpoints"""
        alt_endpoints = [
            f"https://www.picuki.com/profile/{username}",
            f"https://imginn.com/{username}",
            f"https://gramho.com/profile/{username}",
            f"https://dumpor.com/v/{username}",
        ]

        for endpoint in alt_endpoints:
            try:
                print(f"   🌐 Alternative: {endpoint}")

                headers = {
                    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                   'AppleWebKit/537.36')
                }

                async with aiohttp.ClientSession() as session:
                    async with session.get(endpoint, headers=headers) as response:
                        if response.status == 200:
                            content = await response.text()
                            print(
                                f"   ✅ Alternative success! Size: {len(content)}")

                            # Parse for Instagram data
                            await self._parse_html_content(content, endpoint)

                        else:
                            print(
                                f"   ⚠️  Alternative status: {response.status}")

                await asyncio.sleep(random.uniform(1, 3))

            except Exception as e:
                print(f"   ❌ Alternative error: {e}")
                continue

    def _extract_instagram_info(self, data, source):
        """Extract useful information จาก Instagram JSON data"""
        try:
            info = {
                'source': 'instagram_api',
                'endpoint': source,
                'timestamp': datetime.now().isoformat()
            }

            # Look for user data
            if 'graphql' in data and 'user' in data['graphql']:
                user = data['graphql']['user']
                info['user_data'] = {
                    'id': user.get('id'),
                    'username': user.get('username'),
                    'full_name': user.get('full_name'),
                    'biography': user.get('biography'),
                    'external_url': user.get('external_url'),
                    'follower_count': user.get('edge_followed_by', {}).get('count'),
                    'following_count': user.get('edge_follow', {}).get('count'),
                    'is_private': user.get('is_private'),
                    'is_verified': user.get('is_verified')
                }

            # Look for CSRF tokens
            csrf_token = None
            if 'csrf_token' in str(data):
                csrf_match = re.search(r'"csrf_token":"([^"]+)"', str(data))
                if csrf_match:
                    csrf_token = csrf_match.group(1)
                    info['csrf_token'] = csrf_token

            return info if ('user_data' in info or 'csrf_token' in info) else None

        except Exception as e:
            print(f"   ❌ Extract error: {e}")
            return None

    async def _parse_html_content(self, content, source):
        """Parse HTML content สำหรับ useful data"""
        try:
            # Look for CSRF tokens
            csrf_patterns = [
                r'"csrf_token":"([^"]+)"',
                r'csrftoken["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                r'window\._sharedData.*?"csrf_token":"([^"]+)"'
            ]

            found_tokens = []
            for pattern in csrf_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    token = match.group(1)
                    if len(token) > 10:
                        found_tokens.append(token)

            # Look for API endpoints
            endpoint_patterns = [
                r'"api_url":"([^"]+)"',
                r'["\'/](api/v1/[^"\'>\s]+)',
                r'["\'/](graphql[^"\'>\s]*)'
            ]

            found_endpoints = []
            for pattern in endpoint_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    endpoint = match.group(1)
                    found_endpoints.append(endpoint)

            if found_tokens or found_endpoints:
                html_data = {
                    'source': 'html_parse',
                    'url': source,
                    'csrf_tokens': found_tokens,
                    'endpoints': found_endpoints,
                    'timestamp': datetime.now().isoformat()
                }
                self.found_data.append(html_data)

                if found_tokens:
                    print(f"   🔑 Found {len(found_tokens)} CSRF tokens!")
                if found_endpoints:
                    print(f"   🌐 Found {len(found_endpoints)} endpoints!")

        except Exception as e:
            print(f"   ❌ HTML parse error: {e}")

    def generate_legendary_report(self):
        """สร้างรายงาน legendary hunt"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report = f"""
🔥💎 LEGENDARY Instagram Intelligence Report 💎🔥
⏰ เวลา: {timestamp}
🎯 Hunt completed by Legendary Intelligence Framework
{'='*70}

📊 INTELLIGENCE SUMMARY:
{'='*70}
Total data sources: {len(self.found_data)}
"""

        # Count different types of data
        csrf_tokens = []
        endpoints = []
        user_data = []
        osint_data = []

        for item in self.found_data:
            if 'csrf_token' in item or 'csrf_tokens' in item:
                if 'csrf_token' in item:
                    csrf_tokens.append(item['csrf_token'])
                if 'csrf_tokens' in item:
                    csrf_tokens.extend(item['csrf_tokens'])

            if 'endpoints' in item:
                endpoints.extend(item['endpoints'])

            if 'user_data' in item:
                user_data.append(item['user_data'])

            if item.get('source') == 'osint_analysis':
                osint_data.append(item)

        report += f"""
🔑 CSRF Tokens found: {len(csrf_tokens)}
🌐 API Endpoints found: {len(endpoints)}
👤 User profiles found: {len(user_data)}
🕵️  OSINT patterns: {len(osint_data)}
"""

        # Detail each category
        if csrf_tokens:
            report += f"\n🔑 CSRF TOKENS:\n{'='*40}\n"
            for i, token in enumerate(csrf_tokens[:5], 1):  # Show first 5
                token_preview = token[:50] + \
                    "..." if len(token) > 50 else token
                report += f"Token #{i}: {token_preview}\n"

        if endpoints:
            report += f"\n🌐 API ENDPOINTS:\n{'='*40}\n"
            for i, endpoint in enumerate(endpoints[:10], 1):  # Show first 10
                report += f"Endpoint #{i}: {endpoint}\n"

        if user_data:
            report += f"\n👤 USER DATA:\n{'='*40}\n"
            for i, user in enumerate(user_data, 1):
                report += f"""User #{i}:
   Username: {user.get('username', 'N/A')}
   Full name: {user.get('full_name', 'N/A')}
   Followers: {user.get('follower_count', 'N/A')}
   Following: {user.get('following_count', 'N/A')}
   Verified: {user.get('is_verified', 'N/A')}
   Private: {user.get('is_private', 'N/A')}
   Bio: {user.get('biography', 'N/A')[:100]}...
   
"""

        if osint_data:
            report += f"\n🕵️  OSINT INTELLIGENCE:\n{'='*40}\n"
            for osint in osint_data:
                patterns = osint.get('patterns', {})
                report += f"Username: {osint.get('username')}\n"
                if 'email_patterns' in patterns:
                    report += f"Potential emails: {', '.join(patterns['email_patterns'][:3])}\n"
                if 'social_patterns' in patterns:
                    report += f"Social profiles: {', '.join(patterns['social_patterns'][:3])}\n"
                report += "\n"

        # Data sources summary
        report += f"\n📊 DATA SOURCES:\n{'='*40}\n"
        source_counts = {}
        for item in self.found_data:
            source = item.get('source', 'unknown')
            source_counts[source] = source_counts.get(source, 0) + 1

        for source, count in source_counts.items():
            report += f"{source}: {count} items\n"

        report += f"""

🎯 LEGENDARY ANALYSIS:
{'='*70}
"""

        if csrf_tokens:
            report += f"✅ SUCCESS! {len(csrf_tokens)} CSRF tokens discovered\n"
            report += "🔥 These tokens can be used for Instagram automation\n"
        else:
            report += "⚠️  No CSRF tokens found through public methods\n"
            report += "💡 Consider using authenticated approaches\n"

        if user_data:
            report += f"\n✅ {len(user_data)} user profiles successfully extracted\n"
            report += "🔥 Rich user data available for analysis\n"

        if endpoints:
            report += f"\n✅ {len(endpoints)} API endpoints discovered\n"
            report += "🔥 These can be used for further reconnaissance\n"

        report += f"""

💡 LEGENDARY RECOMMENDATIONS:
{'='*70}
1. 🔑 Use discovered tokens for API authentication
2. 👤 Analyze user patterns for social engineering
3. 🌐 Test discovered endpoints for vulnerabilities
4. 🕵️  Cross-reference OSINT data with other platforms
5. 🔄 Implement token refresh mechanisms
6. 📊 Use data for behavioral analysis

🔥 NEXT LEVEL ACTIONS:
{'='*70}
1. 🚀 Automated Instagram interaction using tokens
2. 🎯 Targeted social engineering campaigns
3. 🌐 API endpoint vulnerability assessment
4. 🕵️  Deep OSINT cross-platform correlation
5. 🔍 Advanced behavioral pattern analysis

{'='*70}
💎 Legendary Hunt completed by Ultimate Intelligence Framework
⚠️  Use all data ethically and responsibly!
{'='*70}
"""

        return report


async def main():
    """Main legendary hunt execution"""
    print("🔥💎 LEGENDARY Instagram Intelligence Hunter 💎🔥")
    print("💕 Ultimate Intelligence Gathering Framework")
    print("="*60)

    # Get target
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = input("🎯 ใส่ Instagram URL หรือ username: ").strip()

    if not target:
        target = "https://www.instagram.com/alx.trading/"
        print(f"ใช้ target เริ่มต้น: {target}")

    # Start legendary hunt
    hunter = LegendaryInstagramHunter()
    await hunter.legendary_hunt(target)

    # Generate และแสดงรายงาน
    report = hunter.generate_legendary_report()
    print(report)

    # Save report
    timestamp = int(time.time())
    report_file = f"legendary_instagram_intelligence_{timestamp}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    # Save raw data as JSON
    data_file = f"legendary_instagram_data_{timestamp}.json"
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(hunter.found_data, f, indent=2,
                  ensure_ascii=False, default=str)

    print(f"📄 Legendary report saved: {report_file}")
    print(f"📊 Raw data saved: {data_file}")

    # Final summary
    print(f"\n🎯 LEGENDARY SUMMARY:")
    print(f"📊 Total intelligence items: {len(hunter.found_data)}")

    # Count tokens and endpoints
    total_tokens = 0
    total_endpoints = 0

    for item in hunter.found_data:
        if 'csrf_token' in item:
            total_tokens += 1
        if 'csrf_tokens' in item:
            total_tokens += len(item['csrf_tokens'])
        if 'endpoints' in item:
            total_endpoints += len(item['endpoints'])

    print(f"🔑 CSRF Tokens: {total_tokens}")
    print(f"🌐 API Endpoints: {total_endpoints}")

    if total_tokens > 0:
        print(f"🎉 LEGENDARY SUCCESS! Found working intelligence data!")
        print(f"💡 Next: Use data for advanced Instagram automation")
    else:
        print(f"🔍 Intelligence gathered, continue with advanced techniques")


if __name__ == "__main__":
    asyncio.run(main())
