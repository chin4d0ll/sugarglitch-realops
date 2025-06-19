#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌸 Advanced Social Media Intelligence - ขั้นเทพสุดๆ
สำหรับน้อง chin4d0ll ที่อยากได้ข้อมูลส่วนตัวแบบลึกๆ!
เร็วปรี๊ดดด ใช้เมมโมรี่น้อยๆ 💖
"""

import asyncio
import aiohttp
import concurrent.futures
import json
import time
import random
import re
import threading
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Tuple, AsyncGenerator
import gc
import psutil
import hashlib
import base64
from urllib.parse import quote, unquote, urlparse
import itertools
import weakref

# เพิ่มสีสวยๆ และ emojis น่ารักๆ


class Colors:
    PINK = '\033[95m'
    PURPLE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    SPARKLE = '\033[5m'
    HEART = '💖'
    STAR = '✨'
    END = '\033[0m'


def print_cute(text, color=Colors.PINK):
    """ปริ้นแบบน่ารักๆ พร้อม timestamp และ emoji"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{timestamp}] 🌸 {text} {Colors.HEART}{Colors.END}")


def print_sparkle(text):
    print_cute(f"{Colors.SPARKLE}{text}{Colors.END}", Colors.PURPLE)


@dataclass
class SocialProfile:
    """เก็บข้อมูล social media profile แบบประหยัดเมมโมรี่"""
    platform: str
    username: str
    url: str
    exists: bool = False
    followers: Optional[int] = None
    following: Optional[int] = None
    posts_count: Optional[int] = None
    verified: bool = False
    bio: Optional[str] = None
    location: Optional[str] = None
    join_date: Optional[str] = None
    profile_pic_url: Optional[str] = None
    last_activity: Optional[str] = None
    engagement_rate: Optional[float] = None
    privacy_level: str = 'unknown'  # public, private, limited
    risk_indicators: List[str] = field(default_factory=list)
    extracted_emails: List[str] = field(default_factory=list)
    extracted_phones: List[str] = field(default_factory=list)
    # friends/followers ที่สำคัญ
    connections: List[str] = field(default_factory=list)

    def __post_init__(self):
        """ประหยัดเมมโมรี่โดยใช้ __slots__ และ weakref"""
        if self.bio and len(self.bio) > 500:
            self.bio = self.bio[:500] + "..."  # ตัดข้อความยาวๆ

        # ลบ duplicates ใน lists
        self.risk_indicators = list(set(self.risk_indicators))
        self.extracted_emails = list(set(self.extracted_emails))
        self.extracted_phones = list(set(self.extracted_phones))


class MemoryEfficientSocialIntel:
    """Social Intelligence Engine ที่เร็วและประหยัดเมมโมรี่สุดๆ"""

    def __init__(self, max_concurrent: int = 50, cache_size: int = 1000):
        print_cute(
            "💕 กำลังเตรียม Advanced Social Intelligence Engine...", Colors.PURPLE)

        self.max_concurrent = min(max_concurrent, 100)  # จำกัดไม่ให้เยอะเกินไป
        self.cache_size = cache_size

        # ใช้ WeakValueDictionary เพื่อประหยัดเมมโมรี่
        self.profile_cache = weakref.WeakValueDictionary()
        self.session_pool = []

        # Semaphore สำหรับควบคุมการเชื่อมต่อ
        self.semaphore = asyncio.Semaphore(self.max_concurrent)

        # สถิติการทำงาน
        self.stats = {
            'profiles_found': 0,
            'requests_made': 0,
            'cache_hits': 0,
            'memory_cleaned': 0,
            'errors_handled': 0
        }

        # User agents หลากหลายเพื่อหลบการตรวจจับ
        self.user_agents = self._load_user_agents()

        # Platform-specific configurations
        self.platform_configs = self._load_platform_configs()

        print_sparkle("Social Intelligence Engine พร้อมแล้วค่า! 🔍💖")

    def _load_user_agents(self) -> List[str]:
        """โหลด user agents หลากหลาย"""
        return [
            # Desktop browsers
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/120.0',

            # Mobile browsers
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',

            # Social media app user agents
            'Instagram 302.0.0.27.108 Android',
            'FacebookApp/420.0.0.37.69 [FBAN/FB4A;FBAV/420.0.0.37.69]',
            'TwitterAndroid/10.16.0'
        ]

    def _load_platform_configs(self) -> Dict:
        """โหลดการตั้งค่าสำหรับแต่ละ platform"""
        return {
            'instagram': {
                'base_urls': [
                    'https://www.instagram.com/',
                    'https://instagram.com/',
                    'https://i.instagram.com/'
                ],
                'profile_indicators': [
                    '"is_private":', '"biography":', '"followers_count":',
                    '"following_count":', '"media_count":'
                ],
                'data_extraction': {
                    'followers': r'"edge_followed_by":{"count":(\d+)}',
                    'following': r'"edge_follow":{"count":(\d+)}',
                    'posts': r'"edge_owner_to_timeline_media":{"count":(\d+)}',
                    'bio': r'"biography":"([^"]*)"',
                    'verified': r'"is_verified":(true|false)',
                    'private': r'"is_private":(true|false)',
                    'profile_pic': r'"profile_pic_url_hd":"([^"]*)"'
                },
                'rate_limit': 2.0,  # วินาที
                'max_retries': 3
            },

            'facebook': {
                'base_urls': [
                    'https://www.facebook.com/',
                    'https://facebook.com/',
                    'https://m.facebook.com/',
                    'https://mobile.facebook.com/'
                ],
                'profile_indicators': [
                    'timeline', 'profile', 'about', 'friends', 'photos'
                ],
                'data_extraction': {
                    'name': r'<title>([^<]+)</title>',
                    'friends': r'(\d+)\s+friends?',
                    'location': r'Lives in ([^<]+)',
                    'workplace': r'Works at ([^<]+)',
                    'education': r'Studied at ([^<]+)'
                },
                'rate_limit': 3.0,
                'max_retries': 2
            },

            'twitter': {
                'base_urls': [
                    'https://twitter.com/',
                    'https://x.com/',
                    'https://mobile.twitter.com/'
                ],
                'profile_indicators': [
                    'followers', 'following', 'tweets', 'joined'
                ],
                'data_extraction': {
                    'followers': r'(\d+(?:,\d+)*)\s+Followers',
                    'following': r'(\d+(?:,\d+)*)\s+Following',
                    'tweets': r'(\d+(?:,\d+)*)\s+Tweets',
                    'bio': r'"description":"([^"]*)"',
                    'location': r'"location":"([^"]*)"',
                    'verified': r'"verified":(true|false)',
                    'joined': r'Joined ([^<]+)'
                },
                'rate_limit': 1.5,
                'max_retries': 3
            },

            'linkedin': {
                'base_urls': [
                    'https://www.linkedin.com/in/',
                    'https://linkedin.com/in/',
                    'https://www.linkedin.com/pub/'
                ],
                'profile_indicators': [
                    'experience', 'education', 'connections', 'skills'
                ],
                'data_extraction': {
                    'name': r'<title>([^|]+)',
                    'headline': r'"headline":"([^"]*)"',
                    'location': r'"locationName":"([^"]*)"',
                    'connections': r'(\d+(?:,\d+)*)\s+connections?',
                    'company': r'"companyName":"([^"]*)"',
                    'school': r'"schoolName":"([^"]*)"'
                },
                'rate_limit': 4.0,
                'max_retries': 2
            },

            'tiktok': {
                'base_urls': [
                    'https://www.tiktok.com/@',
                    'https://tiktok.com/@',
                    'https://m.tiktok.com/@'
                ],
                'profile_indicators': [
                    'followers', 'following', 'likes', 'videos'
                ],
                'data_extraction': {
                    'followers': r'"followerCount":(\d+)',
                    'following': r'"followingCount":(\d+)',
                    'likes': r'"heartCount":(\d+)',
                    'videos': r'"videoCount":(\d+)',
                    'bio': r'"desc":"([^"]*)"',
                    'verified': r'"verified":(true|false)'
                },
                'rate_limit': 2.5,
                'max_retries': 3
            },

            'github': {
                'base_urls': [
                    'https://github.com/',
                    'https://api.github.com/users/'
                ],
                'profile_indicators': [
                    'repositories', 'followers', 'following', 'stars'
                ],
                'data_extraction': {
                    'repos': r'"public_repos":(\d+)',
                    'followers': r'"followers":(\d+)',
                    'following': r'"following":(\d+)',
                    'bio': r'"bio":"([^"]*)"',
                    'location': r'"location":"([^"]*)"',
                    'company': r'"company":"([^"]*)"',
                    'blog': r'"blog":"([^"]*)"',
                    'email': r'"email":"([^"]*)"'
                },
                'rate_limit': 1.0,
                'max_retries': 3
            },

            'youtube': {
                'base_urls': [
                    'https://www.youtube.com/c/',
                    'https://www.youtube.com/@',
                    'https://www.youtube.com/user/',
                    'https://www.youtube.com/channel/'
                ],
                'profile_indicators': [
                    'subscribers', 'videos', 'views', 'channel'
                ],
                'data_extraction': {
                    'subscribers': r'(\d+(?:,\d+)*)\s+subscribers?',
                    'videos': r'(\d+(?:,\d+)*)\s+videos?',
                    'views': r'(\d+(?:,\d+)*)\s+views?',
                    'description': r'"description":{"simpleText":"([^"]*)"}'
                },
                'rate_limit': 2.0,
                'max_retries': 3
            }
        }

    async def create_optimized_session(self) -> aiohttp.ClientSession:
        """สร้าง session ที่ optimize แล้วสำหรับความเร็ว"""
        connector = aiohttp.TCPConnector(
            limit=self.max_concurrent,
            limit_per_host=20,
            ttl_dns_cache=300,
            use_dns_cache=True,
            keepalive_timeout=30,
            enable_cleanup_closed=True
        )

        timeout = aiohttp.ClientTimeout(
            total=15,
            connect=5,
            sock_read=10
        )

        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }

        return aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=headers
        )

    async def parallel_profile_search(self, queries: List[Tuple[str, str]]) -> AsyncGenerator[SocialProfile, None]:
        """ค้นหา profiles แบบ parallel พร้อม yield results แบบ streaming"""
        print_cute(
            f"🚀 กำลังค้นหา {len(queries)} profiles แบบ parallel...", Colors.CYAN)

        # สร้าง session
        session = await self.create_optimized_session()

        try:
            # สร้าง tasks สำหรับทุก platform และ query
            tasks = []

            for query, query_type in queries:
                for platform_name, config in self.platform_configs.items():
                    # สร้าง URLs สำหรับแต่ละ platform
                    urls = self._generate_profile_urls(
                        platform_name, query, config)

                    for url in urls:
                        task = self._check_single_profile(
                            session, platform_name, query, url, config, query_type
                        )
                        tasks.append(task)

            print_cute(
                f"📊 สร้าง {len(tasks)} tasks สำหรับการค้นหา", Colors.YELLOW)

            # รัน tasks แบบ batch เพื่อประหยัดเมมโมรี่
            batch_size = 20
            for i in range(0, len(tasks), batch_size):
                batch = tasks[i:i + batch_size]
                print_cute(
                    f"🔄 รัน batch {i//batch_size + 1}/{(len(tasks)-1)//batch_size + 1}", Colors.PURPLE)

                # รัน batch และ yield results ทันที
                results = await asyncio.gather(*batch, return_exceptions=True)

                for result in results:
                    if isinstance(result, SocialProfile) and result.exists:
                        yield result
                        self.stats['profiles_found'] += 1
                        print_sparkle(
                            f"✨ เจอ profile: {result.platform} - {result.username}")
                    elif isinstance(result, Exception):
                        self.stats['errors_handled'] += 1
                        print_cute(f"❌ Error: {result}", Colors.RED)

                # ทำความสะอาดเมมโมรี่หลังแต่ละ batch
                gc.collect()
                self.stats['memory_cleaned'] += 1

                # หน่วงเวลาเล็กน้อยเพื่อไม่ให้ระบบล่ม
                await asyncio.sleep(0.1)

        finally:
            await session.close()

    def _generate_profile_urls(self, platform: str, query: str, config: Dict) -> List[str]:
        """สร้าง URLs สำหรับการค้นหา profile"""
        urls = []
        base_urls = config['base_urls']

        for base_url in base_urls:
            if platform == 'github' and 'api.github.com' in base_url:
                # GitHub API endpoint
                urls.append(f"{base_url}{query}")
            elif platform == 'youtube':
                # YouTube มีหลายรูปแบบ URL
                if '@' in base_url:
                    urls.append(f"{base_url}{query}")
                else:
                    urls.append(f"{base_url}{query}")
            elif platform == 'tiktok':
                # TikTok ต้องมี @ หน้า username
                if not query.startswith('@'):
                    urls.append(f"{base_url}{query}")
                else:
                    urls.append(f"{base_url}{query[1:]}")  # ลบ @ ออก
            else:
                # Platform ปกติ
                urls.append(f"{base_url}{query}")

        return urls

    async def _check_single_profile(self,
                                    session: aiohttp.ClientSession,
                                    platform: str,
                                    query: str,
                                    url: str,
                                    config: Dict,
                                    query_type: str) -> Optional[SocialProfile]:
        """ตรวจสอบ profile เดียวแบบ async"""

        # ใช้ semaphore เพื่อจำกัดการเชื่อมต่อ
        async with self.semaphore:
            # เช็ค cache ก่อน
            cache_key = f"{platform}:{query}"
            if cache_key in self.profile_cache:
                self.stats['cache_hits'] += 1
                return self.profile_cache[cache_key]

            try:
                # หน่วงเวลาตาม rate limit ของแต่ละ platform
                await asyncio.sleep(random.uniform(0.5, config.get('rate_limit', 2.0)))

                # ส่ง request
                async with session.get(url) as response:
                    self.stats['requests_made'] += 1

                    if response.status == 200:
                        content = await response.text()

                        # ตรวจสอบว่าเป็น profile จริงมั้ย
                        if self._is_valid_profile(platform, content, config):
                            # สร้าง SocialProfile object
                            profile = await self._extract_profile_data(
                                platform, query, url, content, config, query_type
                            )

                            # เก็บใน cache (จำกัดขนาด cache)
                            if len(self.profile_cache) < self.cache_size:
                                self.profile_cache[cache_key] = profile

                            return profile

                    elif response.status == 429:  # Rate limited
                        print_cute(
                            f"⏸️ Rate limited on {platform}, waiting...", Colors.YELLOW)
                        await asyncio.sleep(random.uniform(10, 20))
                        return None

            except Exception as e:
                print_cute(f"❌ Error checking {platform}: {e}", Colors.RED)
                return None

        return None

    def _is_valid_profile(self, platform: str, content: str, config: Dict) -> bool:
        """ตรวจสอบว่า content เป็น profile จริงมั้ย"""

        # ตรวจสอบ negative indicators ก่อน
        negative_indicators = [
            'page not found', '404', 'user not found', 'account suspended',
            'profile unavailable', 'does not exist', 'not available',
            'this account doesn\'t exist', 'user does not exist',
            'account has been terminated', 'profile has been removed',
            'sorry, this page isn\'t available', 'the link you followed may be broken'
        ]

        content_lower = content.lower()
        for neg in negative_indicators:
            if neg in content_lower:
                return False

        # ตรวจสอบ positive indicators
        profile_indicators = config.get('profile_indicators', [])
        found_indicators = 0

        for indicator in profile_indicators:
            if indicator.lower() in content_lower:
                found_indicators += 1

        # ต้องเจออย่างน้อย 1 indicator หรือมี content เยอะพอ
        return found_indicators > 0 or len(content) > 5000

    async def _extract_profile_data(self,
                                    platform: str,
                                    query: str,
                                    url: str,
                                    content: str,
                                    config: Dict,
                                    query_type: str) -> SocialProfile:
        """ดึงข้อมูลจาก profile content"""

        profile = SocialProfile(
            platform=platform,
            username=query,
            url=url,
            exists=True
        )

        # ดึงข้อมูลตาม regex patterns ที่กำหนด
        extraction_patterns = config.get('data_extraction', {})

        for field, pattern in extraction_patterns.items():
            try:
                match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
                if match:
                    value = match.group(1)

                    # แปลงข้อมูลตามประเภท
                    if field in ['followers', 'following', 'posts', 'repos', 'videos']:
                        # ลบ comma และแปลงเป็นตัวเลข
                        value = int(value.replace(',', ''))
                        setattr(profile, field, value)
                    elif field in ['verified', 'private']:
                        # แปลงเป็น boolean
                        setattr(profile, field == 'verified',
                                value.lower() == 'true')
                    else:
                        # ข้อความธรรมดา
                        setattr(profile, field, value)

            except Exception as e:
                print_cute(f"⚠️ Error extracting {field}: {e}", Colors.YELLOW)

        # ดึงข้อมูลเสริม
        await self._extract_additional_data(profile, content)

        # ประเมินความเสี่ยง
        self._assess_profile_risk(profile, content)

        # คำนวณ engagement rate ถ้าเป็นไปได้
        self._calculate_engagement_rate(profile)

        return profile

    async def _extract_additional_data(self, profile: SocialProfile, content: str):
        """ดึงข้อมูลเพิ่มเติมจาก content"""

        # ดึง email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, content)
        profile.extracted_emails.extend(emails[:5])  # เก็บแค่ 5 อันแรก

        # ดึง phone numbers
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            r'\+66[-.\s]?\d{1,2}[-.\s]?\d{3,4}[-.\s]?\d{4}'  # Thai numbers
        ]

        for pattern in phone_patterns:
            phones = re.findall(pattern, content)
            profile.extracted_phones.extend(phones[:3])  # เก็บแค่ 3 อันแรก

        # ดึง social links อื่นๆ
        social_patterns = {
            'instagram': r'instagram\.com/([a-zA-Z0-9._]+)',
            'twitter': r'twitter\.com/([a-zA-Z0-9_]+)',
            'facebook': r'facebook\.com/([a-zA-Z0-9.]+)',
            'linkedin': r'linkedin\.com/in/([a-zA-Z0-9-]+)',
            'youtube': r'youtube\.com/(?:c/|@|user/)([a-zA-Z0-9_-]+)'
        }

        for platform_name, pattern in social_patterns.items():
            if platform_name != profile.platform:  # ไม่ดึงจาก platform เดียวกัน
                matches = re.findall(pattern, content, re.IGNORECASE)
                profile.connections.extend(matches[:3])  # เก็บแค่ 3 อันแรก

    def _assess_profile_risk(self, profile: SocialProfile, content: str):
        """ประเมินความเสี่ยงของ profile"""

        risk_indicators = []

        # ตรวจสอบข้อมูลส่วนตัวที่เปิดเผย
        if profile.extracted_emails:
            risk_indicators.append("เปิดเผย email address")

        if profile.extracted_phones:
            risk_indicators.append("เปิดเผย phone number")

        # ตรวจสอบข้อมูลตำแหน่ง
        location_keywords = ['address', 'location',
                             'live in', 'from', 'city', 'country']
        if any(keyword in content.lower() for keyword in location_keywords):
            risk_indicators.append("เปิดเผยข้อมูลตำแหน่ง")

        # ตรวจสอบข้อมูลการทำงาน
        work_keywords = ['work at', 'company', 'job', 'employer', 'office']
        if any(keyword in content.lower() for keyword in work_keywords):
            risk_indicators.append("เปิดเผยข้อมูลการทำงาน")

        # ตรวจสอบข้อมูลครอบครัว
        family_keywords = ['family', 'wife',
                           'husband', 'children', 'kids', 'parents']
        if any(keyword in content.lower() for keyword in family_keywords):
            risk_indicators.append("เปิดเผยข้อมูลครอบครัว")

        # ตรวจสอบการตั้งค่าความเป็นส่วนตัว
        if hasattr(profile, 'private') and not profile.private:
            profile.privacy_level = 'public'
            risk_indicators.append("บัญชีเป็น public")
        elif hasattr(profile, 'private') and profile.private:
            profile.privacy_level = 'private'

        # ตรวจสอบจำนวน followers/friends
        if hasattr(profile, 'followers') and profile.followers and profile.followers > 10000:
            risk_indicators.append("มี followers เยอะ - อาจเป็น public figure")

        profile.risk_indicators = risk_indicators

    def _calculate_engagement_rate(self, profile: SocialProfile):
        """คำนวณ engagement rate"""

        # ต้องมีข้อมูล followers และ posts
        if hasattr(profile, 'followers') and hasattr(profile, 'posts'):
            if profile.followers and profile.posts and profile.followers > 0:
                # สูตรง่ายๆ: posts / followers
                engagement = (profile.posts / profile.followers) * 100
                profile.engagement_rate = round(min(engagement, 100.0), 2)

    async def search_username_variations(self, base_username: str) -> AsyncGenerator[SocialProfile, None]:
        """ค้นหา username variations แบบอัจฉริยะ"""
        print_cute(
            f"🧠 กำลังสร้าง username variations สำหรับ: {base_username}", Colors.PURPLE)

        # สร้าง variations ของ username
        variations = self._generate_username_variations(base_username)

        print_cute(
            f"📝 สร้าง variations ได้ {len(variations)} แบบ", Colors.CYAN)

        # สร้าง queries สำหรับการค้นหา
        queries = [(variation, 'username') for variation in variations]

        # ค้นหาแบบ parallel
        async for profile in self.parallel_profile_search(queries):
            yield profile

    def _generate_username_variations(self, base_username: str) -> List[str]:
        """สร้าง username variations แบบอัจฉริยะ"""

        variations = [base_username]  # เริ่มจาก username เดิม
        base = base_username.lower()

        # เลขต่อท้าย
        for num in [1, 2, 3, 12, 21, 123, 321, 2023, 2024, 2025]:
            variations.extend([
                f"{base}{num}",
                f"{base}_{num}",
                f"{base}.{num}",
                f"{num}{base}"
            ])

        # ตัวอักษรพิเศษ
        special_chars = ['_', '.', '-']
        for char in special_chars:
            if char not in base:
                variations.extend([
                    f"{base}{char}",
                    f"{char}{base}",
                    base.replace('_', char) if '_' in base else f"{base}{char}"
                ])

        # ขยายและตัดคำ
        if len(base) > 4:
            variations.extend([
                base[:4],  # 4 ตัวแรก
                base[:5],  # 5 ตัวแรก
                base[:-1],  # ตัดตัวสุดท้าย
                base[:-2]  # ตัด 2 ตัวสุดท้าย
            ])

        # เพิ่มคำทั่วไป
        common_additions = ['official', 'real', 'the', 'im', 'its', 'me']
        for addition in common_additions:
            variations.extend([
                f"{base}{addition}",
                f"{addition}{base}",
                f"{base}_{addition}",
                f"{addition}_{base}"
            ])

        # ลบ duplicates และเรียงตาม priority
        # เก็บ order และลบ duplicates
        unique_variations = list(dict.fromkeys(variations))

        # จำกัดจำนวนเพื่อประหยัดเวลา
        return unique_variations[:50]

    async def deep_profile_analysis(self, profiles: List[SocialProfile]) -> Dict:
        """วิเคราะห์ profiles แบบลึกๆ"""
        print_cute(
            f"🔬 กำลังวิเคราะห์ {len(profiles)} profiles แบบลึกๆ...", Colors.PURPLE)

        analysis = {
            'total_profiles': len(profiles),
            'platforms_found': [],
            'risk_assessment': {
                'total_risk_score': 0,
                'risk_level': 'low',
                'privacy_concerns': [],
                'exposed_data': []
            },
            'data_correlation': {
                'common_usernames': [],
                'linked_accounts': [],
                'consistency_score': 0
            },
            'behavioral_patterns': {
                'activity_level': 'unknown',
                'posting_frequency': 'unknown',
                'engagement_patterns': []
            },
            'recommendations': []
        }

        if not profiles:
            return analysis

        # รวบรวมข้อมูลพื้นฐาน
        platforms = [p.platform for p in profiles]
        analysis['platforms_found'] = list(set(platforms))

        # วิเคราะห์ความเสี่ยง
        total_risk = 0
        all_risks = []
        exposed_emails = []
        exposed_phones = []

        for profile in profiles:
            # รวมคะแนนความเสี่ยง
            risk_count = len(profile.risk_indicators)
            total_risk += risk_count * 10  # 10 คะแนนต่อ risk

            all_risks.extend(profile.risk_indicators)
            exposed_emails.extend(profile.extracted_emails)
            exposed_phones.extend(profile.extracted_phones)

        # ประเมินระดับความเสี่ยงรวม
        analysis['risk_assessment']['total_risk_score'] = min(total_risk, 100)

        if total_risk >= 80:
            analysis['risk_assessment']['risk_level'] = 'critical'
        elif total_risk >= 60:
            analysis['risk_assessment']['risk_level'] = 'high'
        elif total_risk >= 40:
            analysis['risk_assessment']['risk_level'] = 'medium'
        else:
            analysis['risk_assessment']['risk_level'] = 'low'

        # ข้อมูลที่เปิดเผย
        analysis['risk_assessment']['exposed_data'] = {
            'emails': list(set(exposed_emails)),
            'phones': list(set(exposed_phones)),
            'total_emails': len(set(exposed_emails)),
            'total_phones': len(set(exposed_phones))
        }

        analysis['risk_assessment']['privacy_concerns'] = list(set(all_risks))

        # วิเคราะห์ความสัมพันธ์ระหว่างบัญชี
        self._analyze_account_correlation(profiles, analysis)

        # วิเคราะห์ behavioral patterns
        self._analyze_behavioral_patterns(profiles, analysis)

        # สร้างคำแนะนำ
        analysis['recommendations'] = self._generate_security_recommendations(
            analysis)

        print_sparkle(
            f"✨ วิเคราะห์เสร็จแล้ว! Risk Level: {analysis['risk_assessment']['risk_level']}")

        return analysis

    def _analyze_account_correlation(self, profiles: List[SocialProfile], analysis: Dict):
        """วิเคราะห์ความสัมพันธ์ระหว่างบัญชี"""

        # หา common patterns ใน usernames
        usernames = [p.username.lower() for p in profiles]

        # หาส่วนที่เหมือนกันใน usernames
        if len(usernames) > 1:
            common_parts = []
            for i, username1 in enumerate(usernames):
                for j, username2 in enumerate(usernames[i+1:], i+1):
                    # หาส่วนที่เหมือนกัน
                    common = self._find_common_substring(username1, username2)
                    if len(common) >= 3:  # อย่างน้อย 3 ตัวอักษร
                        common_parts.append(common)

            analysis['data_correlation']['common_usernames'] = list(
                set(common_parts))

        # หาบัญชีที่เชื่อมโยงกัน (มี cross-references)
        linked_accounts = []
        for profile in profiles:
            for connection in profile.connections:
                # เช็คว่า connection นี้ตรงกับ username ใน profiles อื่นมั้ย
                for other_profile in profiles:
                    if other_profile.username.lower() == connection.lower():
                        linked_accounts.append({
                            'from': f"{profile.platform}/{profile.username}",
                            'to': f"{other_profile.platform}/{other_profile.username}"
                        })

        analysis['data_correlation']['linked_accounts'] = linked_accounts

        # คำนวณ consistency score
        consistency_factors = []

        # ตรวจสอบความสม่ำเสมอของข้อมูล bio/description
        bios = [p.bio for p in profiles if p.bio]
        if len(bios) > 1:
            # เช็คว่า bio คล้ายกันมั้ย
            bio_similarity = self._calculate_text_similarity(bios)
            consistency_factors.append(bio_similarity)

        # ตรวจสอบความสม่ำเสมอของ location
        locations = [p.location for p in profiles if p.location]
        if len(locations) > 1:
            location_consistency = len(set(locations)) == 1  # ถ้าเหมือนกันหมด
            consistency_factors.append(80 if location_consistency else 20)

        # คำนวณคะแนนรวม
        if consistency_factors:
            analysis['data_correlation']['consistency_score'] = sum(
                consistency_factors) / len(consistency_factors)

    def _find_common_substring(self, str1: str, str2: str) -> str:
        """หาส่วนที่เหมือนกันระหว่าง 2 strings"""
        longest = ""
        for i in range(len(str1)):
            for j in range(i + 1, len(str1) + 1):
                substring = str1[i:j]
                if substring in str2 and len(substring) > len(longest):
                    longest = substring
        return longest

    def _calculate_text_similarity(self, texts: List[str]) -> float:
        """คำนวณความคล้ายกันของข้อความ"""
        if len(texts) < 2:
            return 100.0

        # ใช้วิธีง่ายๆ: เปรียบเทียบคำที่ซ้ำกัน
        all_words = []
        for text in texts:
            words = re.findall(r'\w+', text.lower())
            all_words.append(set(words))

        # หาคำที่ซ้ำกันใน texts ทั้งหมด
        common_words = set.intersection(*all_words) if all_words else set()
        total_unique_words = set.union(*all_words) if all_words else set()

        if len(total_unique_words) == 0:
            return 0.0

        similarity = (len(common_words) / len(total_unique_words)) * 100
        return similarity

    def _analyze_behavioral_patterns(self, profiles: List[SocialProfile], analysis: Dict):
        """วิเคราะห์ behavioral patterns"""

        # วิเคราะห์ระดับความ active
        total_posts = sum(p.posts_count for p in profiles if p.posts_count)
        total_followers = sum(p.followers for p in profiles if p.followers)

        if total_posts > 1000:
            analysis['behavioral_patterns']['activity_level'] = 'very_high'
        elif total_posts > 500:
            analysis['behavioral_patterns']['activity_level'] = 'high'
        elif total_posts > 100:
            analysis['behavioral_patterns']['activity_level'] = 'medium'
        else:
            analysis['behavioral_patterns']['activity_level'] = 'low'

        # วิเคราะห์ engagement patterns
        engagement_rates = [
            p.engagement_rate for p in profiles if p.engagement_rate]
        if engagement_rates:
            avg_engagement = sum(engagement_rates) / len(engagement_rates)

            if avg_engagement > 5.0:
                analysis['behavioral_patterns']['engagement_patterns'].append(
                    'high_engagement')
            elif avg_engagement > 2.0:
                analysis['behavioral_patterns']['engagement_patterns'].append(
                    'moderate_engagement')
            else:
                analysis['behavioral_patterns']['engagement_patterns'].append(
                    'low_engagement')

    def _generate_security_recommendations(self, analysis: Dict) -> List[str]:
        """สร้างคำแนะนำด้านความปลอดภัย"""

        recommendations = []
        risk_level = analysis['risk_assessment']['risk_level']
        exposed_data = analysis['risk_assessment']['exposed_data']

        # คำแนะนำตาม risk level
        if risk_level in ['critical', 'high']:
            recommendations.extend([
                "🚨 ลดการเปิดเผยข้อมูลส่วนตัวใน social media ทันที",
                "🔒 เปลี่ยนการตั้งค่าบัญชีให้เป็น private",
                "🛡️ เปิด two-factor authentication ในทุกบัญชี",
                "📱 ตรวจสอบและลบข้อมูลส่วนตัวที่ไม่จำเป็น"
            ])

        # คำแนะนำสำหรับข้อมูลที่เปิดเผย
        if exposed_data['total_emails'] > 0:
            recommendations.append(
                f"📧 พบ email {exposed_data['total_emails']} ตัว - ควรลบหรือซ่อนข้อมูลนี้")

        if exposed_data['total_phones'] > 0:
            recommendations.append(
                f"📞 พบเบอร์โทร {exposed_data['total_phones']} หมายเลข - ควรลบออกจาก public profiles")

        # คำแนะนำทั่วไป
        recommendations.extend([
            "🔍 ตรวจสอบการตั้งค่าความเป็นส่วนตัวเป็นประจำ",
            "👥 จำกัดการเปิดเผยข้อมูลเครือข่ายเพื่อนและครอบครัว",
            "📷 ระวังการแชร์รูปภาพที่มี metadata",
            "🌐 ใช้ VPN เมื่อเข้า social media จากที่สาธารณะ"
        ])

        return recommendations

    def generate_comprehensive_report(self, analysis: Dict, profiles: List[SocialProfile]) -> str:
        """สร้างรายงานแบบละเอียดสุดๆ"""

        report_lines = [
            "🌸" * 60,
            f"📊 Advanced Social Media Intelligence Report",
            f"⏰ สร้างเมื่อ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"👤 ผู้ใช้: chin4d0ll",
            "🌸" * 60,
            ""
        ]

        # สรุปผลการค้นหา
        report_lines.extend([
            "🎯 สรุปผลการค้นหา:",
            f"   📱 Platforms ที่เจอ: {len(analysis['platforms_found'])} แห่ง",
            f"   📊 Profiles ทั้งหมด: {analysis['total_profiles']} profiles",
            f"   ⚠️ Risk Level: {analysis['risk_assessment']['risk_level'].upper()}",
            f"   🔢 Risk Score: {analysis['risk_assessment']['total_risk_score']}/100",
            ""
        ])

        # รายละเอียด platforms ที่เจอ
        if analysis['platforms_found']:
            report_lines.extend([
                "📱 Platforms ที่พบ profiles:",
                *[f"   • {platform.title()}" for platform in analysis['platforms_found']],
                ""
            ])

        # รายละเอียดแต่ละ profile
        report_lines.extend([
            "👤 รายละเอียด Profiles:",
            ""
        ])

        for profile in profiles:
            report_lines.extend([
                f"   🌟 {profile.platform.upper()} - {profile.username}",
                f"      🔗 URL: {profile.url}",
                f"      👥 Followers: {profile.followers or 'ไม่ทราบ'}",
                f"      📝 Posts: {profile.posts_count or 'ไม่ทราบ'}",
                f"      ✅ Verified: {'ใช่' if profile.verified else 'ไม่'}",
                f"      🔒 Privacy: {profile.privacy_level}",
                ""
            ])

            if profile.bio:
                report_lines.extend([
                    f"      📄 Bio: {profile.bio[:100]}{'...' if len(profile.bio) > 100 else ''}",
                    ""
                ])

            if profile.risk_indicators:
                report_lines.extend([
                    f"      ⚠️ Risk Indicators:",
                    *[f"         - {risk}" for risk in profile.risk_indicators],
                    ""
                ])

        # ข้อมูลที่เปิดเผย
        exposed_data = analysis['risk_assessment']['exposed_data']
        if exposed_data['total_emails'] > 0 or exposed_data['total_phones'] > 0:
            report_lines.extend([
                "🚨 ข้อมูลส่วนตัวที่เปิดเผย:",
                f"   📧 Email addresses: {exposed_data['total_emails']} ตัว",
                f"   📞 Phone numbers: {exposed_data['total_phones']} หมายเลข",
                ""
            ])

            if exposed_data['emails']:
                report_lines.extend([
                    "   📧 Emails ที่พบ:",
                    # แสดงแค่ 5 อันแรก
                    *[f"      - {email}" for email in exposed_data['emails'][:5]],
                    ""
                ])

            if exposed_data['phones']:
                report_lines.extend([
                    "   📞 Phone numbers ที่พบ:",
                    # แสดงแค่ 5 อันแรก
                    *[f"      - {phone}" for phone in exposed_data['phones'][:5]],
                    ""
                ])

        # การวิเคราะห์ความสัมพันธ์
        correlation = analysis['data_correlation']
        if correlation['common_usernames'] or correlation['linked_accounts']:
            report_lines.extend([
                "🔗 การวิเคราะห์ความสัมพันธ์:",
                f"   🎯 Consistency Score: {correlation['consistency_score']:.1f}/100",
                ""
            ])

            if correlation['common_usernames']:
                report_lines.extend([
                    "   🔤 Common Username Patterns:",
                    *[f"      - {pattern}" for pattern in correlation['common_usernames']],
                    ""
                ])

            if correlation['linked_accounts']:
                report_lines.extend([
                    "   🔗 Linked Accounts:",
                    *[f"      - {link['from']} → {link['to']}" for link in correlation['linked_accounts']],
                    ""
                ])

        # Behavioral patterns
        behavioral = analysis['behavioral_patterns']
        report_lines.extend([
            "🧠 Behavioral Patterns:",
            f"   📊 Activity Level: {behavioral['activity_level']}",
            f"   💬 Engagement Patterns: {', '.join(behavioral['engagement_patterns']) if behavioral['engagement_patterns'] else 'ไม่ทราบ'}",
            ""
        ])

        # คำแนะนำด้านความปลอดภัย
        recommendations = analysis['recommendations']
        if recommendations:
            report_lines.extend([
                "💡 คำแนะนำด้านความปลอดภัย:",
                *[f"   {rec}" for rec in recommendations],
                ""
            ])

        # สถิติการทำงาน
        report_lines.extend([
            "📈 สถิติการทำงาน:",
            f"   🔍 Profiles ที่พบ: {self.stats['profiles_found']}",
            f"   📡 Requests ที่ส่ง: {self.stats['requests_made']}",
            f"   💾 Cache hits: {self.stats['cache_hits']}",
            f"   🧹 Memory cleanups: {self.stats['memory_cleaned']}",
            f"   ❌ Errors handled: {self.stats['errors_handled']}",
            ""
        ])

        report_lines.extend([
            "🌸" * 60,
            "💖 รายงานสร้างโดย Advanced Social Intelligence Engine",
            "⚠️ ใช้ข้อมูลนี้อย่างรับผิดชอบและถูกกฎหมาย",
            "📚 เพื่อการศึกษาและป้องกันตัวเองเท่านั้น",
            "🌸" * 60
        ])

        return "\n".join(report_lines)

    def cleanup_resources(self):
        """ทำความสะอาดทรัพยากรทั้งหมด"""
        self.profile_cache.clear()
        self.session_pool.clear()
        gc.collect()
        print_sparkle("🧹 ทำความสะอาดทรัพยากรเสร็จแล้ว!")

# 🎯 Main Application สำหรับ Social Intelligence


async def social_intelligence_main():
    """ฟังก์ชันหลักสำหรับรัน Social Intelligence"""

    print_cute("""
    💕 ยินดีต้อนรับสู่ Advanced Social Intelligence Engine
    🌸 โดยเฉพาะสำหรับน้อง chin4d0ll!
    
    ✨ คุณสมบัติขั้นเทพ:
    🔍 ค้นหา social media profiles แบบครอบคลุม
    🧠 สร้าง username variations อัจฉริยะ
    📊 วิเคราะห์ข้อมูลส่วนตัวแบบลึกๆ
    ⚠️ ประเมินความเสี่ยงด้านความปลอดภัย
    🔗 วิเคราะห์ความสัมพันธ์ระหว่างบัญชี
    💡 คำแนะนำด้านความปลอดภัยแบบเฉพาะบุคคล
    
    🚨 คำเตือน: ใช้เพื่อการศึกษาและป้องกันตัวเองเท่านั้น!
    """, Colors.PURPLE)

    # สร้าง Social Intelligence Engine
    intel_engine = MemoryEfficientSocialIntel(
        max_concurrent=30, cache_size=500)

    try:
        # รับข้อมูลจากผู้ใช้
        print_cute("\n🎯 ใส่ข้อมูลที่ต้องการค้นหา:", Colors.CYAN)

        search_query = input(
            f"{Colors.PINK}👤 Username, Email, หรือ Name: {Colors.END}").strip()

        if not search_query:
            search_query = "chin4d0ll"  # ตัวอย่างสำหรับทดลอง
            print_cute(f"ใช้ตัวอย่าง: {search_query}", Colors.YELLOW)

        # ถามว่าต้องการค้นหา variations มั้ย
        search_variations = input(
            f"{Colors.PINK}🔄 ต้องการค้นหา username variations มั้ยคะ? (y/n): {Colors.END}").strip().lower()
        include_variations = search_variations in ['y', 'yes', 'ใช่', '1']

        print_cute(f"\n🚀 เริ่มการค้นหา Social Intelligence...", Colors.GREEN)

        profiles_found = []

        if include_variations:
            # ค้นหาแบบ variations
            print_cute("🧠 กำลังค้นหา username variations...", Colors.PURPLE)
            async for profile in intel_engine.search_username_variations(search_query):
                profiles_found.append(profile)
                print_sparkle(
                    f"✨ เจอ: {profile.platform} - {profile.username}")
        else:
            # ค้นหาแบบปกติ
            queries = [(search_query, 'username')]
            async for profile in intel_engine.parallel_profile_search(queries):
                profiles_found.append(profile)
                print_sparkle(
                    f"✨ เจอ: {profile.platform} - {profile.username}")

        print_cute(
            f"\n📊 เจอ profiles ทั้งหมด: {len(profiles_found)}", Colors.GREEN)

        if profiles_found:
            # วิเคราะห์ profiles
            print_cute("🔬 กำลังวิเคราะห์ profiles แบบลึกๆ...", Colors.PURPLE)
            analysis = await intel_engine.deep_profile_analysis(profiles_found)

            # สร้างรายงาน
            timestamp = int(time.time())
            report_filename = f"social_intelligence_report_{timestamp}.txt"
            report = intel_engine.generate_comprehensive_report(
                analysis, profiles_found)

            # บันทึกรายงาน
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write(report)

            print_cute(f"\n📋 สร้างรายงานแล้ว: {report_filename}", Colors.GREEN)
            print(report)

            # แสดงสรุปสำคัญ
            risk_level = analysis['risk_assessment']['risk_level']
            risk_score = analysis['risk_assessment']['total_risk_score']

            print_cute(f"\n🎯 สรุป Risk Assessment:", Colors.BOLD)

            if risk_level in ['critical', 'high']:
                print_cute(
                    f"   ⚠️ Risk Level: {risk_level.upper()} ({risk_score}/100)", Colors.RED)
                print_cute(
                    "   🚨 ควรดำเนินการปรับปรุงความปลอดภัยทันที!", Colors.RED)
            elif risk_level == 'medium':
                print_cute(
                    f"   ⚠️ Risk Level: {risk_level.upper()} ({risk_score}/100)", Colors.YELLOW)
                print_cute(
                    "   💡 ควรปรับปรุงการตั้งค่าความเป็นส่วนตัว", Colors.YELLOW)
            else:
                print_cute(
                    f"   ✅ Risk Level: {risk_level.upper()} ({risk_score}/100)", Colors.GREEN)
                print_cute("   👍 ระดับความปลอดภัยดี!", Colors.GREEN)

        else:
            print_cute(
                "😅 ไม่เจอ social media profiles สำหรับการค้นหานี้", Colors.YELLOW)
            print_cute(
                "💡 ลองเปลี่ยน username หรือใช้ variations ดูนะคะ", Colors.CYAN)

        # ทำความสะอาด
        intel_engine.cleanup_resources()

    except KeyboardInterrupt:
        print_cute("\n⏹️ หยุดการทำงานโดยผู้ใช้", Colors.YELLOW)
    except Exception as e:
        print_cute(f"\n❌ เกิดข้อผิดพลาด: {e}", Colors.RED)
    finally:
        print_cute(
            "\n💖 ขอบคุณที่ใช้ Social Intelligence Engine ค่า!", Colors.PINK)

if __name__ == "__main__":
    asyncio.run(social_intelligence_main())
