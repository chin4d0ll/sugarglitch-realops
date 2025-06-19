#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌸 Personal OSINT Master - สำหรับ chin4d0ll
ค้นหาข้อมูลส่วนตัวแบบลึกๆ เร็วปรี๊ดดด!
⚠️ ใช้เพื่อการศึกษาและป้องกันตัวเองเท่านั้น!
"""

import asyncio
import aiohttp
import concurrent.futures
import json
import time
import random
import re
import hashlib
import base64
import gc
import threading
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Set, Tuple
import requests
from urllib.parse import quote, urlparse
import phonenumbers
from phonenumbers import geocoder, carrier
import email_validator
import itertools
import os
import sys

# ใส่สีสวยๆ เหมือนเดิม


class Colors:
    PINK = '\033[95m'
    PURPLE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    SPARKLE = '\033[5m'
    END = '\033[0m'


def print_cute(text, color=Colors.PINK):
    """ปริ้นแบบน่ารักๆ พร้อม timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{timestamp}] {text}{Colors.END}")


def print_success(text):
    print_cute(f"✅ {text}", Colors.GREEN)


def print_warning(text):
    print_cute(f"⚠️ {text}", Colors.YELLOW)


def print_error(text):
    print_cute(f"❌ {text}", Colors.RED)


def print_info(text):
    print_cute(f"ℹ️ {text}", Colors.CYAN)


@dataclass
class PersonalInfo:
    """เก็บข้อมูลส่วนตัวที่เจอ"""
    email: Optional[str] = None
    phone: Optional[str] = None
    name: Optional[str] = None
    username: Optional[str] = None
    location: Optional[str] = None
    birth_date: Optional[str] = None
    social_accounts: List[str] = None
    leaked_passwords: List[str] = None
    associated_domains: List[str] = None
    photos: List[str] = None

    def __post_init__(self):
        if self.social_accounts is None:
            self.social_accounts = []
        if self.leaked_passwords is None:
            self.leaked_passwords = []
        if self.associated_domains is None:
            self.associated_domains = []
        if self.photos is None:
            self.photos = []


class PersonalOSINTEngine:
    """เครื่องมือค้นหาข้อมูลส่วนตัวแบบโหดๆ"""

    def __init__(self, max_workers: int = 30):
        print_cute("💕 กำลังเตรียม Personal OSINT Engine สุดลึก...",
                   Colors.PURPLE)

        self.max_workers = max_workers
        self.session_pool = []
        self.results_cache = {}
        self.found_data = PersonalInfo()
        self.stats = {
            'total_searches': 0,
            'successful_hits': 0,
            'data_sources_checked': 0,
            'personal_data_found': 0
        }

        # User agents สำหรับหลบการตรวจจับ
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
        ]

        # ฐานข้อมูล breach ที่มีชื่อเสียง (สำหรับการศึกษา)
        self.breach_databases = [
            'haveibeenpwned.com',
            'leakcheck.io',
            'dehashed.com',
            'breachdirectory.org'
        ]

        print_success("Personal OSINT Engine พร้อมแล้วค่า! 🔍💖")

    def create_session(self) -> requests.Session:
        """สร้าง session ที่หมุน user agent และ headers"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
        return session

    def validate_email(self, email: str) -> Dict:
        """ตรวจสอบความถูกต้องของ email และดึงข้อมูล"""
        print_info(f"กำลังตรวจสอบ email: {email}")

        try:
            # ตรวจสอบ format
            validation = email_validator.validate_email(email)
            email_info = {
                'email': validation.email,
                'local_part': validation.local,
                'domain': validation.domain,
                'is_valid': True,
                'mx_exists': True,  # email_validator จะเช็ค MX record ให้
                'suggestions': []
            }

            # วิเคราะห์ domain
            domain = validation.domain.lower()

            # ตรวจสอบว่าเป็น disposable email มั้ย
            disposable_domains = [
                '10minutemail.com', 'guerrillamail.com', 'mailinator.com',
                'tempmail.org', 'throwaway.email', 'temp-mail.org'
            ]

            email_info['is_disposable'] = domain in disposable_domains

            # ตรวจสอบประเภท email provider
            provider_info = self._analyze_email_provider(domain)
            email_info.update(provider_info)

            print_success(
                f"Email ถูกต้อง! Provider: {provider_info.get('provider_type', 'Unknown')}")
            return email_info

        except Exception as e:
            print_error(f"Email ไม่ถูกต้อง: {e}")
            return {
                'email': email,
                'is_valid': False,
                'error': str(e)
            }

    def _analyze_email_provider(self, domain: str) -> Dict:
        """วิเคราะห์ email provider และข้อมูลที่เกี่ยวข้อง"""

        # Email providers ใหญ่ๆ
        providers = {
            'gmail.com': {
                'provider_type': 'Google',
                'country': 'US',
                'security_level': 'high',
                'features': ['2FA', 'OAuth', 'Recovery']
            },
            'yahoo.com': {
                'provider_type': 'Yahoo',
                'country': 'US',
                'security_level': 'medium',
                'features': ['2FA', 'Recovery']
            },
            'hotmail.com': {
                'provider_type': 'Microsoft',
                'country': 'US',
                'security_level': 'high',
                'features': ['2FA', 'OAuth', 'Recovery']
            },
            'outlook.com': {
                'provider_type': 'Microsoft',
                'country': 'US',
                'security_level': 'high',
                'features': ['2FA', 'OAuth', 'Recovery']
            },
            'protonmail.com': {
                'provider_type': 'ProtonMail',
                'country': 'CH',
                'security_level': 'very_high',
                'features': ['E2E_Encryption', '2FA', 'Anonymous']
            }
        }

        return providers.get(domain, {
            'provider_type': 'Custom/Corporate',
            'country': 'Unknown',
            'security_level': 'unknown',
            'features': []
        })

    def validate_phone(self, phone: str, country_code: str = None) -> Dict:
        """ตรวจสอบเบอร์โทรและดึงข้อมูลที่เกี่ยวข้อง"""
        print_info(f"กำลังตรวจสอบเบอร์โทร: {phone}")

        try:
            # Parse phone number
            if country_code:
                parsed = phonenumbers.parse(phone, country_code)
            else:
                # ลองหลายประเทศ
                for cc in ['TH', 'US', 'GB', 'AU', 'CA']:
                    try:
                        parsed = phonenumbers.parse(phone, cc)
                        if phonenumbers.is_valid_number(parsed):
                            break
                    except:
                        continue
                else:
                    # ถ้าไม่มีประเทศไหนได้ ลอง parse โดยไม่มี country code
                    parsed = phonenumbers.parse(phone, None)

            if not phonenumbers.is_valid_number(parsed):
                return {'phone': phone, 'is_valid': False, 'error': 'Invalid phone number'}

            # ดึงข้อมูลจากเบอร์โทร
            phone_info = {
                'phone': phone,
                'formatted_international': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                'formatted_national': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
                'formatted_e164': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
                'country_code': parsed.country_code,
                'national_number': parsed.national_number,
                'is_valid': True
            }

            # ดึงข้อมูลประเทศ
            try:
                country = geocoder.description_for_number(parsed, 'en')
                phone_info['country'] = country
            except:
                phone_info['country'] = 'Unknown'

            # ดึงข้อมูล carrier
            try:
                carrier_name = carrier.name_for_number(parsed, 'en')
                phone_info['carrier'] = carrier_name
            except:
                phone_info['carrier'] = 'Unknown'

            # ตรวจสอบประเภทเบอร์
            number_type = phonenumbers.number_type(parsed)
            type_names = {
                phonenumbers.PhoneNumberType.MOBILE: 'Mobile',
                phonenumbers.PhoneNumberType.FIXED_LINE: 'Fixed Line',
                phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: 'Fixed Line or Mobile',
                phonenumbers.PhoneNumberType.TOLL_FREE: 'Toll Free',
                phonenumbers.PhoneNumberType.PREMIUM_RATE: 'Premium Rate',
                phonenumbers.PhoneNumberType.VOIP: 'VoIP'
            }
            phone_info['number_type'] = type_names.get(number_type, 'Unknown')

            print_success(
                f"เบอร์โทรถูกต้อง! ประเทศ: {phone_info['country']}, Carrier: {phone_info['carrier']}")
            return phone_info

        except Exception as e:
            print_error(f"ไม่สามารถตรวจสอบเบอร์โทรได้: {e}")
            return {
                'phone': phone,
                'is_valid': False,
                'error': str(e)
            }

    async def search_social_media_deep(self, query: str, search_type: str = 'username') -> Dict:
        """ค้นหา social media แบบลึกๆ"""
        print_info(
            f"กำลังค้นหา social media สำหรับ: {query} (ประเภท: {search_type})")

        # Social media platforms พร้อม URL patterns
        platforms = {
            'facebook': {
                'url_patterns': [
                    f'https://facebook.com/{query}',
                    f'https://fb.com/{query}',
                    f'https://m.facebook.com/{query}'
                ],
                'search_methods': ['username', 'email', 'phone'],
                'data_richness': 'very_high'
            },
            'instagram': {
                'url_patterns': [
                    f'https://instagram.com/{query}',
                    f'https://www.instagram.com/{query}'
                ],
                'search_methods': ['username', 'email'],
                'data_richness': 'high'
            },
            'twitter': {
                'url_patterns': [
                    f'https://twitter.com/{query}',
                    f'https://x.com/{query}'
                ],
                'search_methods': ['username', 'email'],
                'data_richness': 'high'
            },
            'linkedin': {
                'url_patterns': [
                    f'https://linkedin.com/in/{query}',
                    f'https://www.linkedin.com/in/{query}'
                ],
                'search_methods': ['username', 'email', 'name'],
                'data_richness': 'very_high'
            },
            'tiktok': {
                'url_patterns': [
                    f'https://tiktok.com/@{query}',
                    f'https://www.tiktok.com/@{query}'
                ],
                'search_methods': ['username'],
                'data_richness': 'medium'
            },
            'youtube': {
                'url_patterns': [
                    f'https://youtube.com/c/{query}',
                    f'https://youtube.com/@{query}',
                    f'https://youtube.com/user/{query}'
                ],
                'search_methods': ['username', 'email'],
                'data_richness': 'high'
            },
            'github': {
                'url_patterns': [
                    f'https://github.com/{query}'
                ],
                'search_methods': ['username', 'email'],
                'data_richness': 'very_high'
            },
            'reddit': {
                'url_patterns': [
                    f'https://reddit.com/user/{query}',
                    f'https://www.reddit.com/u/{query}'
                ],
                'search_methods': ['username'],
                'data_richness': 'medium'
            },
            'telegram': {
                'url_patterns': [
                    f'https://t.me/{query}'
                ],
                'search_methods': ['username'],
                'data_richness': 'medium'
            },
            'discord': {
                'url_patterns': [
                    f'https://discord.com/users/{query}'  # ต้องมี User ID
                ],
                'search_methods': ['username'],
                'data_richness': 'low'
            },
            'snapchat': {
                'url_patterns': [
                    f'https://snapchat.com/add/{query}'
                ],
                'search_methods': ['username'],
                'data_richness': 'low'
            },
            'pinterest': {
                'url_patterns': [
                    f'https://pinterest.com/{query}',
                    f'https://www.pinterest.com/{query}'
                ],
                'search_methods': ['username', 'email'],
                'data_richness': 'medium'
            }
        }

        found_accounts = {}

        async def check_platform_existence(platform_name, platform_info):
            """ตรวจสอบว่ามี account ใน platform นี้มั้ย"""
            results = []

            for url in platform_info['url_patterns']:
                try:
                    async with aiohttp.ClientSession(
                        timeout=aiohttp.ClientTimeout(total=10),
                        headers={'User-Agent': random.choice(self.user_agents)}
                    ) as session:
                        async with session.get(url) as response:
                            account_info = {
                                'platform': platform_name,
                                'url': url,
                                'status_code': response.status,
                                'exists': False,
                                'profile_data': {}
                            }

                            if response.status == 200:
                                content = await response.text()

                                # ตรวจสอบว่าเป็น profile จริงมั้ย (ไม่ใช่ error page)
                                if self._validate_profile_content(platform_name, content):
                                    account_info['exists'] = True
                                    account_info['profile_data'] = self._extract_profile_data(
                                        platform_name, content)
                                    print_success(
                                        f"เจอ {platform_name}: {url}")
                                    self.stats['successful_hits'] += 1

                            results.append(account_info)

                except Exception as e:
                    print_error(f"Error checking {platform_name}: {e}")

                # หน่วงเวลาเพื่อไม่ให้โดน rate limit
                await asyncio.sleep(random.uniform(0.5, 2.0))

            return results

        # รัน parallel สำหรับทุก platform
        tasks = []
        for platform_name, platform_info in platforms.items():
            if search_type in platform_info['search_methods']:
                task = check_platform_existence(platform_name, platform_info)
                tasks.append(task)
                self.stats['data_sources_checked'] += 1

        print_info(f"กำลังตรวจสอบ {len(tasks)} platforms พร้อมกัน...")

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # รวบรวมผลลัพธ์
        for result in results:
            if isinstance(result, list):
                for account in result:
                    if account['exists']:
                        platform = account['platform']
                        if platform not in found_accounts:
                            found_accounts[platform] = []
                        found_accounts[platform].append(account)

        total_found = sum(len(accounts)
                          for accounts in found_accounts.values())
        print_success(f"เจอ social media accounts ทั้งหมด {total_found} แห่ง!")

        return {
            'query': query,
            'search_type': search_type,
            'accounts_found': found_accounts,
            'total_platforms': len(found_accounts),
            'total_accounts': total_found,
            'timestamp': datetime.now().isoformat()
        }

    def _validate_profile_content(self, platform: str, content: str) -> bool:
        """ตรวจสอบว่า content เป็น profile page จริงมั้ย"""

        # Keywords ที่บอกว่าเป็น profile จริง
        positive_indicators = {
            'facebook': ['timeline', 'profile', 'posts', 'friends', 'photos'],
            'instagram': ['posts', 'followers', 'following', 'biography'],
            'twitter': ['tweets', 'followers', 'following', 'joined'],
            'linkedin': ['experience', 'education', 'connections', 'skills'],
            'github': ['repositories', 'commits', 'followers', 'starred'],
            'youtube': ['subscribers', 'videos', 'playlists', 'channel'],
            'tiktok': ['followers', 'following', 'likes', 'videos'],
            'reddit': ['karma', 'posts', 'comments', 'awards']
        }

        # Keywords ที่บอกว่าไม่เจอ profile
        negative_indicators = [
            'page not found', '404', 'user not found', 'account suspended',
            'profile unavailable', 'does not exist', 'not available',
            'this account doesn\'t exist', 'user does not exist'
        ]

        content_lower = content.lower()

        # ตรวจสอบ negative indicators ก่อน
        for neg in negative_indicators:
            if neg in content_lower:
                return False

        # ตรวจสอบ positive indicators
        if platform in positive_indicators:
            for pos in positive_indicators[platform]:
                if pos in content_lower:
                    return True

        # ถ้าไม่เจอ specific indicators แต่มี content เยอะ = น่าจะเป็น profile
        return len(content) > 5000

    def _extract_profile_data(self, platform: str, content: str) -> Dict:
        """ดึงข้อมูลจาก profile page"""
        profile_data = {
            'platform': platform,
            'data_extracted': [],
            'metadata': {}
        }

        try:
            # ใช้ regex ดึงข้อมูลพื้นฐาน

            # ดึง title
            title_match = re.search(
                r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
            if title_match:
                profile_data['title'] = title_match.group(1).strip()

            # ดึง meta description
            desc_match = re.search(
                r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
            if desc_match:
                profile_data['description'] = desc_match.group(1).strip()

            # ดึงข้อมูลเฉพาะ platform
            if platform == 'facebook':
                profile_data.update(self._extract_facebook_data(content))
            elif platform == 'instagram':
                profile_data.update(self._extract_instagram_data(content))
            elif platform == 'linkedin':
                profile_data.update(self._extract_linkedin_data(content))
            elif platform == 'github':
                profile_data.update(self._extract_github_data(content))

        except Exception as e:
            profile_data['extraction_error'] = str(e)

        return profile_data

    def _extract_facebook_data(self, content: str) -> Dict:
        """ดึงข้อมูลจาก Facebook profile"""
        data = {}

        # ดึงจำนวน friends (ถ้าเป็น public)
        friends_match = re.search(r'(\d+)\s+friends?', content, re.IGNORECASE)
        if friends_match:
            data['friends_count'] = friends_match.group(1)

        # ดึงข้อมูล location ถ้ามี
        location_patterns = [
            r'Lives in ([^<]+)',
            r'From ([^<]+)',
            r'location["\'][^>]*>([^<]+)'
        ]

        for pattern in location_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                data['location'] = match.group(1).strip()
                break

        return data

    def _extract_instagram_data(self, content: str) -> Dict:
        """ดึงข้อมูลจาก Instagram profile"""
        data = {}

        # ดึงจำนวน followers, following, posts
        patterns = {
            'followers': r'(\d+)\s+followers?',
            'following': r'(\d+)\s+following',
            'posts': r'(\d+)\s+posts?'
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                data[key] = match.group(1)

        # ดึง biography
        bio_match = re.search(r'"biography":"([^"]+)"', content)
        if bio_match:
            data['biography'] = bio_match.group(1)

        return data

    def _extract_linkedin_data(self, content: str) -> Dict:
        """ดึงข้อมูลจาก LinkedIn profile"""
        data = {}

        # ดึงข้อมูลงาน
        job_patterns = [
            r'<h2[^>]*>([^<]+)</h2>.*?<h3[^>]*>([^<]+)</h3>',  # Name and title
            r'"headline":"([^"]+)"',  # JSON data
        ]

        for pattern in job_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                if len(match.groups()) >= 2:
                    data['name'] = match.group(1).strip()
                    data['title'] = match.group(2).strip()
                else:
                    data['headline'] = match.group(1).strip()
                break

        # ดึงจำนวน connections
        conn_match = re.search(r'(\d+)\s+connections?', content, re.IGNORECASE)
        if conn_match:
            data['connections'] = conn_match.group(1)

        return data

    def _extract_github_data(self, content: str) -> Dict:
        """ดึงข้อมูลจาก GitHub profile"""
        data = {}

        # ดึงจำนวน repos, followers, following
        patterns = {
            'repositories': r'(\d+)\s+repositories?',
            'followers': r'(\d+)\s+followers?',
            'following': r'(\d+)\s+following'
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                data[key] = match.group(1)

        # ดึง bio
        bio_match = re.search(r'"bio":"([^"]+)"', content)
        if bio_match:
            data['bio'] = bio_match.group(1)

        # ดึง location
        location_match = re.search(r'"location":"([^"]+)"', content)
        if location_match:
            data['location'] = location_match.group(1)

        return data

    async def search_data_breaches(self, query: str, query_type: str = 'email') -> Dict:
        """ค้นหาในฐานข้อมูล data breaches"""
        print_info(f"กำลังค้นหา data breaches สำหรับ: {query}")
        print_warning(
            "⚠️ การค้นหา data breaches เพื่อการศึกษาและป้องกันเท่านั้น!")

        breach_results = {
            'query': query,
            'query_type': query_type,
            'breaches_found': [],
            'total_breaches': 0,
            'risk_level': 'low',
            'recommendations': []
        }

        # Have I Been Pwned API (ตัวอย่าง - ต้องมี API key จริง)
        await self._check_haveibeenpwned(query, breach_results)

        # DeHashed API (ตัวอย่าง - ต้องมี subscription)
        await self._check_dehashed(query, breach_results)

        # วิเคราะห์ risk level
        if breach_results['total_breaches'] > 5:
            breach_results['risk_level'] = 'very_high'
            breach_results['recommendations'].extend([
                'เปลี่ยนรหัสผ่านทุกบัญชีทันที',
                'เปิด 2FA ในทุกบัญชีที่สำคัญ',
                'ตรวจสอบ credit report',
                'ใช้ password manager'
            ])
        elif breach_results['total_breaches'] > 2:
            breach_results['risk_level'] = 'high'
            breach_results['recommendations'].extend([
                'เปลี่ยนรหัสผ่านบัญชีสำคัญ',
                'เปิด 2FA',
                'ใช้รหัสผ่านที่แข็งแกร่ง'
            ])
        elif breach_results['total_breaches'] > 0:
            breach_results['risk_level'] = 'medium'
            breach_results['recommendations'].append(
                'เปลี่ยนรหัสผ่านบัญชีที่เกี่ยวข้อง')

        return breach_results

    async def _check_haveibeenpwned(self, email: str, results: Dict):
        """ตรวจสอบกับ Have I Been Pwned API"""
        try:
            # NOTE: ต้องมี API key จริงสำหรับการใช้งานจริง
            # นี่เป็นตัวอย่างโครงสร้าง

            api_url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            headers = {
                'hibp-api-key': 'YOUR_API_KEY_HERE',  # ต้องสมัคร API key
                'User-Agent': random.choice(self.user_agents)
            }

            # สำหรับตัวอย่าง เราจะใช้ mock data
            mock_breaches = [
                {
                    'Name': 'Adobe',
                    'Title': 'Adobe',
                    'Domain': 'adobe.com',
                    'BreachDate': '2013-10-04',
                    'AddedDate': '2013-12-04T00:00:00Z',
                    'PwnCount': 152445165,
                    'Description': 'In October 2013, 153 million Adobe accounts were breached...',
                    'DataClasses': ['Email addresses', 'Password hints', 'Passwords', 'Usernames']
                }
            ]

            # เพิ่ม mock data ถ้าเป็น email ที่กำหนด
            if '@' in email:  # ถ้าเป็น email format
                results['breaches_found'].extend(mock_breaches)
                results['total_breaches'] += len(mock_breaches)
                print_warning(
                    f"⚠️ พบข้อมูลใน {len(mock_breaches)} data breaches!")

        except Exception as e:
            print_error(f"Error checking Have I Been Pwned: {e}")

    async def _check_dehashed(self, query: str, results: Dict):
        """ตรวจสอบกับ DeHashed API"""
        try:
            # NOTE: DeHashed ต้องมี subscription
            # นี่เป็นตัวอย่างโครงสร้าง

            mock_data = [
                {
                    'id': '123456789',
                    'email': query if '@' in query else f"{query}@example.com",
                    'username': query,
                    'password': 'hash_value_here',
                    'hashed_password': 'bcrypt_hash',
                    'name': 'John Doe',
                    'database_name': 'Collection #1'
                }
            ]

            # เพิ่ม mock data
            results['breaches_found'].extend(mock_data)
            results['total_breaches'] += len(mock_data)

        except Exception as e:
            print_error(f"Error checking DeHashed: {e}")

    def search_people_search_engines(self, name: str, location: str = None) -> Dict:
        """ค้นหาจาก People Search Engines"""
        print_info(f"กำลังค้นหาข้อมูลบุคคลสำหรับ: {name}")

        # People search engines (สำหรับการศึกษา)
        search_engines = [
            'pipl.com',
            'spokeo.com',
            'whitepages.com',
            'truthfinder.com',
            'beenverified.com',
            'instantcheckmate.com'
        ]

        results = {
            'name': name,
            'location': location,
            'sources_checked': search_engines,
            'found_profiles': [],
            'possible_matches': []
        }

        # สำหรับตัวอย่าง เราจะใช้ mock data
        mock_profiles = [
            {
                'source': 'whitepages.com',
                'name': name,
                'age': '25-30',
                'location': location or 'Bangkok, Thailand',
                'phone': '+66-8X-XXX-XXXX',
                'relatives': ['Jane Doe', 'John Smith'],
                'addresses': [
                    {
                        'address': '123 Main St, Bangkok',
                        'years': '2020-2023'
                    }
                ]
            }
        ]

        results['found_profiles'] = mock_profiles
        results['total_matches'] = len(mock_profiles)

        print_success(f"เจอข้อมูลที่ตรงกันจาก {len(mock_profiles)} แหล่ง")

        return results

    def reverse_image_search(self, image_url: str) -> Dict:
        """ค้นหาภาพย้อนกลับเพื่อหาข้อมูลเพิ่มเติม"""
        print_info(f"กำลังทำ reverse image search สำหรับ: {image_url}")

        # Reverse image search engines
        search_urls = {
            'google': f'https://www.google.com/searchbyimage?image_url={quote(image_url)}',
            'tineye': f'https://tineye.com/search?url={quote(image_url)}',
            'yandex': f'https://yandex.com/images/search?rpt=imageview&url={quote(image_url)}',
            'bing': f'https://www.bing.com/images/searchbyimage?FORM=IRSBIQ&cbir=sbi&imgurl={quote(image_url)}'
        }

        results = {
            'image_url': image_url,
            'search_engines': search_urls,
            'matches_found': [],
            'metadata': {}
        }

        # ตัวอย่าง metadata ที่อาจได้จากภาพ
        mock_metadata = {
            'image_size': '1920x1080',
            'file_format': 'JPEG',
            'creation_date': '2023-12-15',
            'camera_model': 'iPhone 14 Pro',
            'gps_coordinates': None,  # อาจมี GPS ถ้าไม่ได้ลบ EXIF
            'similar_images': [
                'https://example.com/similar1.jpg',
                'https://example.com/similar2.jpg'
            ]
        }

        results['metadata'] = mock_metadata

        return results

    async def comprehensive_personal_search(self,
                                            email: str = None,
                                            phone: str = None,
                                            name: str = None,
                                            username: str = None) -> Dict:
        """การค้นหาข้อมูลส่วนตัวแบบครอบคลุม"""

        print_cute(f"\n🎯 เริ่มการค้นหาข้อมูลส่วนตัวแบบครอบคลุม", Colors.BOLD)
        print_cute("=" * 60, Colors.PINK)

        start_time = time.time()
        comprehensive_results = {
            'search_parameters': {
                'email': email,
                'phone': phone,
                'name': name,
                'username': username
            },
            'timestamp': datetime.now().isoformat(),
            'results': {},
            'risk_assessment': {},
            'recommendations': []
        }

        # รายการ tasks ที่จะรัน
        tasks_to_run = []

        # Email validation และ search
        if email:
            print_info(f"📧 เพิ่ม email search: {email}")
            tasks_to_run.append(
                ('email_validation', self.validate_email(email)))
            tasks_to_run.append(
                ('email_breaches', self.search_data_breaches(email, 'email')))
            tasks_to_run.append(
                ('email_social', self.search_social_media_deep(email, 'email')))

        # Phone validation และ search
        if phone:
            print_info(f"📱 เพิ่ม phone search: {phone}")
            tasks_to_run.append(
                ('phone_validation', self.validate_phone(phone)))
            tasks_to_run.append(
                ('phone_social', self.search_social_media_deep(phone, 'phone')))

        # Username search
        if username:
            print_info(f"👤 เพิ่ม username search: {username}")
            tasks_to_run.append(
                ('username_social', self.search_social_media_deep(username, 'username')))

        # Name search
        if name:
            print_info(f"🏷️ เพิ่ม name search: {name}")
            tasks_to_run.append(
                ('name_people_search', self.search_people_search_engines(name)))

        print_info(f"🚀 กำลังรัน {len(tasks_to_run)} tasks พร้อมกัน...")

        # รัน async tasks
        async_tasks = [(name, task)
                       for name, task in tasks_to_run if asyncio.iscoroutine(task)]
        sync_tasks = [(name, task) for name,
                      task in tasks_to_run if not asyncio.iscoroutine(task)]

        # รัน async tasks
        for task_name, task in async_tasks:
            try:
                result = await task
                comprehensive_results['results'][task_name] = result
                print_success(f"✅ {task_name} เสร็จแล้ว!")
                self.stats['total_searches'] += 1
            except Exception as e:
                comprehensive_results['results'][task_name] = {'error': str(e)}
                print_error(f"❌ {task_name} ผิดพลาด: {e}")

        # รัน sync tasks
        for task_name, task_func in sync_tasks:
            try:
                if callable(task_func):
                    result = task_func()
                else:
                    result = task_func
                comprehensive_results['results'][task_name] = result
                print_success(f"✅ {task_name} เสร็จแล้ว!")
                self.stats['total_searches'] += 1
            except Exception as e:
                comprehensive_results['results'][task_name] = {'error': str(e)}
                print_error(f"❌ {task_name} ผิดพลาด: {e}")

        # วิเคราะห์ความเสี่ยงรวม
        comprehensive_results['risk_assessment'] = self._assess_overall_risk(
            comprehensive_results['results'])

        # สร้างคำแนะนำ
        comprehensive_results['recommendations'] = self._generate_recommendations(
            comprehensive_results['results'])

        # คำนวณเวลาที่ใช้
        end_time = time.time()
        comprehensive_results['scan_duration'] = round(
            end_time - start_time, 2)
        comprehensive_results['statistics'] = self.stats.copy()

        print_cute(
            f"\n🎉 การค้นหาเสร็จสิ้น! ใช้เวลา {comprehensive_results['scan_duration']} วินาที", Colors.GREEN)
        print_cute("=" * 60, Colors.PINK)

        return comprehensive_results

    def _assess_overall_risk(self, results: Dict) -> Dict:
        """ประเมินความเสี่ยงรวมจากผลการค้นหา"""
        risk_score = 0
        risk_factors = []

        # ตรวจสอบ data breaches
        if 'email_breaches' in results:
            breach_data = results['email_breaches']
            if isinstance(breach_data, dict) and breach_data.get('total_breaches', 0) > 0:
                breach_count = breach_data['total_breaches']
                risk_score += min(breach_count * 15, 60)  # สูงสุด 60 คะแนน
                risk_factors.append(f"พบข้อมูลใน {breach_count} data breaches")

        # ตรวจสอบ social media exposure
        social_accounts = 0
        for key in results:
            if 'social' in key and isinstance(results[key], dict):
                social_accounts += results[key].get('total_accounts', 0)

        if social_accounts > 10:
            risk_score += 25
            risk_factors.append(
                f"มี social media accounts เยอะ ({social_accounts} บัญชี)")
        elif social_accounts > 5:
            risk_score += 15
            risk_factors.append(
                f"มี social media accounts ปานกลาง ({social_accounts} บัญชี)")

        # ตรวจสอบข้อมูลส่วนตัวที่เปิดเผย
        if 'name_people_search' in results:
            people_data = results['name_people_search']
            if isinstance(people_data, dict) and people_data.get('total_matches', 0) > 0:
                risk_score += 20
                risk_factors.append(
                    "ข้อมูลส่วนตัวปรากฏใน people search engines")

        # กำหนด risk level
        if risk_score >= 80:
            risk_level = 'CRITICAL'
        elif risk_score >= 60:
            risk_level = 'HIGH'
        elif risk_score >= 40:
            risk_level = 'MEDIUM'
        elif risk_score >= 20:
            risk_level = 'LOW'
        else:
            risk_level = 'MINIMAL'

        return {
            'risk_score': min(risk_score, 100),
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'privacy_exposure': 'HIGH' if social_accounts > 8 else 'MEDIUM' if social_accounts > 3 else 'LOW'
        }

    def _generate_recommendations(self, results: Dict) -> List[str]:
        """สร้างคำแนะนำตามผลการค้นหา"""
        recommendations = []

        # คำแนะนำพื้นฐาน
        recommendations.extend([
            "🔐 ใช้รหัสผ่านที่แข็งแกร่งและไม่ซ้ำกันในแต่ละบัญชี",
            "🛡️ เปิด Two-Factor Authentication (2FA) ในบัญชีสำคัญ",
            "🔍 ตรวจสอบการตั้งค่าความเป็นส่วนตัวใน social media",
            "📱 ระวังข้อมูลที่แชร์ใน social media"
        ])

        # คำแนะนำเฉพาะตามผลการค้นหา
        if any('breaches' in key for key in results):
            recommendations.append(
                "⚠️ เปลี่ยนรหัสผ่านทันทีสำหรับบัญชีที่อยู่ใน data breach")

        if any('social' in key for key in results):
            recommendations.extend([
                "👁️ ตรวจสอบว่าข้อมูลอะไรบ้างที่เป็น public ใน social media",
                "🔒 ปรับการตั้งค่าให้เป็น private มากขึ้น"
            ])

        if any('people_search' in key for key in results):
            recommendations.extend([
                "📞 ติดต่อ people search engines เพื่อขอลบข้อมูล",
                "🏠 หลีกเลี่ยงการแชร์ที่อยู่และข้อมูลส่วนตัว"
            ])

        return recommendations

    def generate_detailed_report(self, results: Dict, output_file: str = None) -> str:
        """สร้างรายงานแบบละเอียด"""
        report_lines = [
            "🌸" * 50,
            f"📊 Personal OSINT Report - ข้อมูลส่วนตัว",
            f"⏰ วันที่สแกน: {results.get('timestamp', 'Unknown')}",
            f"⚡ ระยะเวลา: {results.get('scan_duration', 0)} วินาที",
            "🌸" * 50,
            ""
        ]

        # แสดงพารามิเตอร์การค้นหา
        search_params = results.get('search_parameters', {})
        report_lines.extend([
            "🎯 พารามิเตอร์การค้นหา:",
            f"   📧 Email: {search_params.get('email', 'ไม่ระบุ')}",
            f"   📱 Phone: {search_params.get('phone', 'ไม่ระบุ')}",
            f"   👤 Name: {search_params.get('name', 'ไม่ระบุ')}",
            f"   🏷️ Username: {search_params.get('username', 'ไม่ระบุ')}",
            ""
        ])

        # แสดงผลการประเมินความเสี่ยง
        risk_assessment = results.get('risk_assessment', {})
        report_lines.extend([
            "⚠️ การประเมินความเสี่ยง:",
            f"   🎯 Risk Score: {risk_assessment.get('risk_score', 0)}/100",
            f"   📊 Risk Level: {risk_assessment.get('risk_level', 'Unknown')}",
            f"   🔒 Privacy Exposure: {risk_assessment.get('privacy_exposure', 'Unknown')}",
            ""
        ])

        # แสดงปัจจัยเสี่ยง
        risk_factors = risk_assessment.get('risk_factors', [])
        if risk_factors:
            report_lines.extend([
                "🚨 ปัจจัยเสี่ยงที่พบ:",
                *[f"   • {factor}" for factor in risk_factors],
                ""
            ])

        # แสดงผลการค้นหาแต่ละประเภท
        search_results = results.get('results', {})

        # Email results
        if 'email_validation' in search_results:
            email_data = search_results['email_validation']
            if email_data.get('is_valid'):
                report_lines.extend([
                    "📧 ผลการตรวจสอบ Email:",
                    f"   ✅ Email: {email_data.get('email')}",
                    f"   🏢 Provider: {email_data.get('provider_type', 'Unknown')}",
                    f"   🌍 Country: {email_data.get('country', 'Unknown')}",
                    f"   🛡️ Security Level: {email_data.get('security_level', 'Unknown')}",
                    ""
                ])

        # Data breaches
        if 'email_breaches' in search_results:
            breach_data = search_results['email_breaches']
            breach_count = breach_data.get('total_breaches', 0)
            report_lines.extend([
                "🔥 Data Breaches ที่พบ:",
                f"   📊 จำนวน breaches: {breach_count}",
                f"   ⚠️ Risk Level: {breach_data.get('risk_level', 'Unknown')}",
                ""
            ])

        # Social media accounts
        social_total = 0
        for key in search_results:
            if 'social' in key:
                social_data = search_results[key]
                if isinstance(social_data, dict):
                    social_total += social_data.get('total_accounts', 0)

        if social_total > 0:
            report_lines.extend([
                "📱 Social Media Accounts:",
                f"   📊 ทั้งหมด: {social_total} บัญชี",
                ""
            ])

        # Phone validation
        if 'phone_validation' in search_results:
            phone_data = search_results['phone_validation']
            if phone_data.get('is_valid'):
                report_lines.extend([
                    "📱 ผลการตรวจสอบเบอร์โทร:",
                    f"   ✅ เบอร์: {phone_data.get('formatted_international')}",
                    f"   🌍 ประเทศ: {phone_data.get('country', 'Unknown')}",
                    f"   📡 Carrier: {phone_data.get('carrier', 'Unknown')}",
                    f"   📞 ประเภท: {phone_data.get('number_type', 'Unknown')}",
                    ""
                ])

        # คำแนะนำ
        recommendations = results.get('recommendations', [])
        if recommendations:
            report_lines.extend([
                "💡 คำแนะนำด้านความปลอดภัย:",
                *[f"   {rec}" for rec in recommendations],
                ""
            ])

        # สถิติการทำงาน
        stats = results.get('statistics', {})
        report_lines.extend([
            "📈 สถิติการทำงาน:",
            f"   🔍 การค้นหาทั้งหมด: {stats.get('total_searches', 0)}",
            f"   ✅ ผลลัพธ์ที่พบ: {stats.get('successful_hits', 0)}",
            f"   🗄️ แหล่งข้อมูลที่ตรวจสอบ: {stats.get('data_sources_checked', 0)}",
            f"   📋 ข้อมูลส่วนตัวที่พบ: {stats.get('personal_data_found', 0)}",
            ""
        ])

        report_lines.extend([
            "🌸" * 50,
            "💖 รายงานสร้างโดย Personal OSINT Engine",
            "⚠️ ใช้ข้อมูลนี้อย่างรับผิดชอบและถูกกฎหมาย",
            "🌸" * 50
        ])

        report_content = "\n".join(report_lines)

        # บันทึกไฟล์ถ้าต้องการ
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print_success(f"💾 บันทึกรายงานแล้วที่: {output_file}")

        return report_content

    def cleanup_memory(self):
        """ทำความสะอาดเมมโมรี่"""
        self.results_cache.clear()
        self.session_pool.clear()
        gc.collect()
        print_success("🧹 ทำความสะอาดเมมโมรี่แล้ว!")

# 🎯 Main Application


async def main():
    """ฟังก์ชันหลักสำหรับรันโปรแกรม"""
    print_cute("""
    💕 ยินดีต้อนรับสู่ Personal OSINT Master
    🌸 สำหรับน้อง chin4d0ll โดยเฉพาะ!
    
    ✨ คุณสมบัติการค้นหาข้อมูลส่วนตัว:
    📧 Email validation และ breach checking
    📱 Phone number validation และ carrier lookup
    👤 Username และ social media searching
    🏷️ Name searching ใน people databases
    🔍 Reverse image searching
    ⚠️ Risk assessment และ recommendations
    
    🚨 คำเตือน: ใช้เพื่อการศึกษาและป้องกันตัวเองเท่านั้น!
    """, Colors.PURPLE)

    # สร้าง Personal OSINT Engine
    osint_engine = PersonalOSINTEngine(max_workers=30)

    try:
        # รับข้อมูลจากผู้ใช้
        print_cute(
            "\n🎯 กรอกข้อมูลที่ต้องการค้นหา (กรอกอย่างน้อย 1 ข้อมูล):", Colors.CYAN)

        email = input(
            f"{Colors.PINK}📧 Email address (Enter เพื่อข้าม): {Colors.END}").strip()
        phone = input(
            f"{Colors.PINK}📱 Phone number (Enter เพื่อข้าม): {Colors.END}").strip()
        name = input(
            f"{Colors.PINK}👤 Full name (Enter เพื่อข้าม): {Colors.END}").strip()
        username = input(
            f"{Colors.PINK}🏷️ Username (Enter เพื่อข้าม): {Colors.END}").strip()

        # ตรวจสอบว่ามีข้อมูลอย่างน้อย 1 อย่าง
        if not any([email, phone, name, username]):
            print_warning("ไม่มีข้อมูลให้ค้นหา! จะใช้ตัวอย่างแทน...")
            email = "test@example.com"  # ตัวอย่างสำหรับทดลอง

        # เริ่มการค้นหา
        print_cute(f"\n🚀 เริ่มการค้นหาข้อมูลส่วนตัว...", Colors.GREEN)

        results = await osint_engine.comprehensive_personal_search(
            email=email or None,
            phone=phone or None,
            name=name or None,
            username=username or None
        )

        # สร้างรายงาน
        timestamp = int(time.time())
        report_filename = f"personal_osint_report_{timestamp}.txt"
        report = osint_engine.generate_detailed_report(
            results, report_filename)

        print_cute("\n📋 สรุปรายงาน:", Colors.BOLD)
        print(report)

        # แสดงข้อมูลสำคัญ
        risk_assessment = results.get('risk_assessment', {})
        print_cute(f"\n🎯 สรุปความเสี่ยง:", Colors.YELLOW)
        print_cute(f"   Risk Score: {risk_assessment.get('risk_score', 0)}/100",
                   Colors.RED if risk_assessment.get('risk_score', 0) > 60 else Colors.GREEN)
        print_cute(f"   Risk Level: {risk_assessment.get('risk_level', 'Unknown')}", Colors.RED if risk_assessment.get(
            'risk_level') in ['HIGH', 'CRITICAL'] else Colors.GREEN)

        # ทำความสะอาด
        osint_engine.cleanup_memory()

    except KeyboardInterrupt:
        print_cute("\n⏹️ หยุดการทำงานโดยผู้ใช้", Colors.YELLOW)
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาด: {e}")
    finally:
        print_cute("\n💖 ขอบคุณที่ใช้ Personal OSINT Engine ค่า!", Colors.PINK)

if __name__ == "__main__":
    # เช็ค dependencies
    required_modules = ['aiohttp', 'requests',
                        'phonenumbers', 'email-validator']
    missing_modules = []

    for module in required_modules:
        try:
            if module == 'email-validator':
                __import__('email_validator')
            else:
                __import__(module.replace('-', '_'))
        except ImportError:
            missing_modules.append(module)

    if missing_modules:
        print_error(f"ขาด modules: {', '.join(missing_modules)}")
        print_cute(
            f"ติดตั้งด้วย: pip install {' '.join(missing_modules)}", Colors.YELLOW)
        sys.exit
