# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Instagram OSINT Tool โหดๆ
 CTF
ใช้ได้กับ public profile เท่านั้น!
"""
import requests
import json
import re
import time
from urllib.parse import quote
import asyncio
import aiohttp
from datetime import datetime

class InstaOSINT:
    def __init__(self):
        # Session แบบประหยัดเมมโมรี่
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q = 0.9,image/webp,*/*;q = 0.8',
            'Accept-Language': 'en-US,en;q = 0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })

        self.found_data = {
            'profile_info': {},
            'posts': [],
            'followers_sample': [],
            'following_sample': [],
            'tagged_users': set(),
            'hashtags': set(),
            'locations': set()
        }

    def extract_json_from_page(self, html_content):
        """ดึง JSON data จาก Instagram page (เทคนิคโหดๆ!)"""
        try:
            # หา JSON data ที่ซ่อนอยู่ใน HTML
            json_pattern = r'window\._sharedData\s*=\s*({.+?});'
            match = re.search(json_pattern, html_content)
            if match:
                return json.loads(match.group(1))

            # วิธีที่ 2: หา JSON ใน script tags
            script_pattern = r'<script type="application/ld\+json">(.+?)</script>'
            matches = re.findall(script_pattern, html_content, re.DOTALL)
            for match in matches:
                try:
                    return json.loads(match)
                except Exception:
                    continue

        except Exception as e:
            print(f"❌ Error extracting JSON: {e}")
        return None

    def get_profile_info(self, username):
        """ดึงข้อมูล profile แบบโหดๆ"""
        print(f"🔍 Gathering info for @{username}")

        try:
            # Method 1: ใช้ Instagram web interface
            url = f"https://www.instagram.com/{username}/"
            response = self.session.get(url, timeout = 10)

            if response.status_code == 200:
                # ดึง JSON data จากหน้าเว็บ
                json_data = self.extract_json_from_page(response.text)

                if json_data:
                    try:
                        # ดึงข้อมูลจาก JSON (structure อาจเปลี่ยนได้)
                        user_data = json_data.get('entry_data', {}).get('ProfilePage', [{}])[0]
                        graphql = user_data.get('graphql', {})
                        user = graphql.get('user', {})

                        profile_info = {
                            'username': user.get('username', username),
                            'full_name': user.get('full_name', ''),
                            'biography': user.get('biography', ''),
                            'external_url': user.get('external_url', ''),
                            'followers_count': user.get('edge_followed_by', {}).get('count', 0),
                            'following_count': user.get('edge_follow', {}).get('count', 0),
                            'posts_count': user.get('edge_owner_to_timeline_media', {}).get('count', 0),
                            'is_private': user.get('is_private', False),
                            'is_verified': user.get('is_verified', False),
                            'profile_pic_url': user.get('profile_pic_url_hd', ''),
                            'business_category': user.get('business_category_name', ''),
                            'is_business_account': user.get('is_business_account', False)
                        }

                        self.found_data['profile_info'] = profile_info
                        self.print_profile_info(profile_info)

                        # ดึงข้อมูล posts ล่าสุด
                        posts = user.get('edge_owner_to_timeline_media', {}).get('edges', [])
                        self.extract_posts_info(posts)

                        return True

                    except Exception as e:
                        print(f"❌ Error parsing JSON data: {e}")

            # Method 2: Alternative method ถ้า method 1 ไม่ได้
            print("🔄 Trying alternative method...")
            return self.get_profile_alternative(username)

        except Exception as e:
            print(f"❌ Error getting profile: {e}")
            return False

    def get_profile_alternative(self, username):
        """วิธีทางเลือกในการดึงข้อมูล"""
        try:
            # ใช้ผ่าน mobile version (เบาและเร็วกว่า)
            mobile_url = f"https://m.instagram.com/{username}/"
            response = self.session.get(mobile_url, timeout = 10)

            if response.status_code == 200:
                # Parse HTML แบบง่ายๆ
                html = response.text

                # ดึงข้อมูลพื้นฐานจาก HTML tags
                profile_info = {
                    'username': username,
                    'full_name': self.extract_meta_content(html, 'og:title'),
                    'biography': self.extract_meta_content(html, 'og:description'),
                    'profile_pic_url': self.extract_meta_content(html, 'og:image'),
                    'is_private': 'This Account is Private' in html
                }

                self.found_data['profile_info'] = profile_info
                self.print_profile_info(profile_info)
                return True

        except Exception as e:
            print(f"❌ Alternative method failed: {e}")

        return False

    def extract_meta_content(self, html, property_name):
        """ดึงข้อมูลจาก meta tags"""
        pattern = f'<meta property="{property_name}" content="([^"]*)"'
        match = re.search(pattern, html)
        return match.group(1) if match else ""

    def extract_posts_info(self, posts_data):
        """วิเคราะห์ข้อมูล posts แบบละเอียด"""
        print("📸 Analyzing recent posts...")

        for post in posts_data[:10]:  # วิเคราะห์ 10 โพสต์ล่าสุด
            try:
                node = post.get('node', {})

                post_info = {
                    'id': node.get('id', ''),
                    'shortcode': node.get('shortcode', ''),
                    'timestamp': datetime.fromtimestamp(node.get('taken_at_timestamp', 0)),
                    'caption': '',
                    'likes_count': node.get('edge_liked_by', {}).get('count', 0),
                    'comments_count': node.get('edge_media_to_comment', {}).get('count', 0),
                    'is_video': node.get('is_video', False),
                    'hashtags': [],
                    'mentions': [],
                    'location': None
                }

                # ดึง caption และวิเคราะห์
                caption_edges = node.get('edge_media_to_caption', {}).get('edges', [])
                if caption_edges:
                    caption_text = caption_edges[0].get('node', {}).get('text', '')
                    post_info['caption'] = caption_text

                    # หา hashtags
                    hashtags = re.findall(r'#(\w+)', caption_text)
                    post_info['hashtags'] = hashtags
                    self.found_data['hashtags'].update(hashtags)

                    # หา mentions
                    mentions = re.findall(r'@(\w+)', caption_text)
                    post_info['mentions'] = mentions
                    self.found_data['tagged_users'].update(mentions)

                # ดึงข้อมูล location
                location = node.get('location')
                if location:
                    location_name = location.get('name', '')
                    post_info['location'] = location_name
                    self.found_data['locations'].add(location_name)

                self.found_data['posts'].append(post_info)

                print(f"   📸 Post {post_info['shortcode']}: {post_info['likes_count']} likes, {post_info['comments_count']} comments")

            except Exception as e:
                print(f"❌ Error analyzing post: {e}")

    def print_profile_info(self, profile_info):
        """แสดงข้อมูล profile แบบสวยๆ"""
        print("\n" + "="*60)
        print("👤 PROFILE INFORMATION")
        print("="*60)

        print(f"🔹 Username: @{profile_info.get('username', 'N/A')}")
        print(f"🔹 Full Name: {profile_info.get('full_name', 'N/A')}")
        print(f"🔹 Biography: {profile_info.get('biography', 'N/A')}")
        print(f"🔹 External URL: {profile_info.get('external_url', 'N/A')}")
        print(f"🔹 Followers: {profile_info.get('followers_count', 'N/A'):,}")
        print(f"🔹 Following: {profile_info.get('following_count', 'N/A'):,}")
        print(f"🔹 Posts: {profile_info.get('posts_count', 'N/A'):,}")
        print(f"🔹 Private: {'Yes' if profile_info.get('is_private') else 'No'}")
        print(f"🔹 Verified: {'Yes' if profile_info.get('is_verified') else 'No'}")
        print(f"🔹 Business: {'Yes' if profile_info.get('is_business_account') else 'No'}")

        if profile_info.get('business_category'):
            print(f"🔹 Business Category: {profile_info['business_category']}")

    async def check_username_variations(self, base_username):
        """เช็ค username variations แบบ async (เร็วสุดๆ!)"""
        print(f"🔍 Checking username variations for '{base_username}'...")

        # สร้าง variations
        variations = [
            base_username + str(i) for i in range(1, 100)  # username1, username2, ...
        ] + [
            base_username + suffix for suffix in ['_', '__', '___', '.', '_official', '_real', '_og']
        ] + [
            prefix + base_username for prefix in ['_', 'real_', 'official_', 'the_']
        ]

        async def check_single_username(session, username):
            try:
                url = f"https://www.instagram.com/{username}/"
                async with session.get(url, timeout = 5) as response:
                    if response.status == 200:
                        text = await response.text()
                        if 'Sorry, this page isn\'t available' not in text:
                            return username, True
            except Exception:
                pass
            return username, False

        # ใช้ async เพื่อเช็คหลาย username พร้อมกัน
        async with aiohttp.ClientSession(
            headers = self.session.headers,
            timeout = aiohttp.ClientTimeout(total = 10)
        ) as session:
            tasks = [check_single_username(session, username) for username in variations[:50]]  # เช็ค 50 อันแรก
            results = await asyncio.gather(*tasks, return_exceptions = True)

            found_usernames = []
            for result in results:
                if isinstance(result, tuple) and result[1]:
                    found_usernames.append(result[0])

            if found_usernames:
                print(f"✅ Found variations:")
                for username in found_usernames:
                    print(f"   📍 @{username}")
            else:
                print("❌ No variations found")

    def generate_comprehensive_report(self):
        """สร้างรายงานแบบครบถ้วน"""
        print("\n" + "="*80)
        print("📊 COMPREHENSIVE OSINT REPORT")
        print("="*80)

        profile = self.found_data['profile_info']

        print(f"\n📈 Statistics Summary:")
        print(f"   👥 Followers: {profile.get('followers_count', 0):,}")
        print(f"   👤 Following: {profile.get('following_count', 0):,}")
        print(f"   📸 Posts analyzed: {len(self.found_data['posts'])}")
        print(f"   🏷️  Unique hashtags: {len(self.found_data['hashtags'])}")
        print(f"   👥 Tagged users: {len(self.found_data['tagged_users'])}")
        print(f"   📍 Locations mentioned: {len(self.found_data['locations'])}")

        # แสดง hashtags ยอดนิยม
        if self.found_data['hashtags']:
            print(f"\n🏷️ Most Used Hashtags:")
            for hashtag in list(self.found_data['hashtags'])[:10]:
                print(f"   #{hashtag}")

        # แสดง users ที่ถูก mention
        if self.found_data['tagged_users']:
            print(f"\n👥 Tagged/Mentioned Users:")
            for user in list(self.found_data['tagged_users'])[:10]:
                print(f"   @{user}")

        # แสดง locations
        if self.found_data['locations']:
            print(f"\n📍 Mentioned Locations:")
            for location in list(self.found_data['locations'])[:10]:
                print(f"   📍 {location}")

        # วิเคราะห์ activity patterns
        if self.found_data['posts']:
            print(f"\n📊 Activity Analysis:")
            posts = self.found_data['posts']

            total_likes = sum(post['likes_count'] for post in posts)
            total_comments = sum(post['comments_count'] for post in posts)
            avg_likes = total_likes / len(posts) if posts else 0
            avg_comments = total_comments / len(posts) if posts else 0

            print(f"   💝 Average likes per post: {avg_likes:.1f}")
            print(f"   💬 Average comments per post: {avg_comments:.1f}")

            video_posts = sum(1 for post in posts if post['is_video'])
            print(f"   🎥 Video posts: {video_posts}/{len(posts)} ({video_posts/len(posts)*100:.1f}%)")

# 🚀 วิธีใช้งาน
async def main():
    print("🔍 Instagram OSINT Tool - Educational Purpose Only! 💖")
    print("=" * 60)

    username = input("👤 Enter Instagram username (without @): ").strip().replace('@', '')

    if not username:
        print("❌ Please provide a username!")
        return

    osint = InstaOSINT()

    print(f"\n🚀 Starting OSINT analysis for @{username}")
    print("🔄 This may take a few moments...\n")

    # ดึงข้อมูล profile หลัก
    success = osint.get_profile_info(username)

    if success:
        # เช็ค username variations
        print(f"\n🔍 Checking for username variations...")
        await osint.check_username_variations(username)

        # สร้างรายงานสรุป
        osint.generate_comprehensive_report()

        # เสนอการส่งออกรายงาน
        export = input(f"\n💾 Export report to file? (y/n): ").lower().strip()
        if export == 'y':
            filename = f"osint_report_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(osint.found_data, f, indent = 2, ensure_ascii = False, default = str)
            print(f"✅ Report saved to {filename}")

    else:
        print("❌ Failed to gather profile information")
        print("💡 Possible reasons:")
        print("   - Username doesn't exist")
        print("   - Account is private")
        print("   - Instagram is blocking requests")
        print("   - Network connectivity issues")

if __name__ == "__main__":
    asyncio.run(main())
