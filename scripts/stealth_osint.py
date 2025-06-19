#!/usr/bin/env python3
"""
🕵️ STEALTH OSINT WITH PROXY ROTATION 🕵️
========================================

ระบบ OSINT แบบหลบๆ หลีกๆ ไม่โดน rate limit!
- Proxy Rotation
- User-Agent Rotation
- Delay Management
- Multiple Search Methods
- Tor Support (if available)

⚠️ FOR AUTHORIZED PENETRATION TESTING ONLY ⚠️
"""

import requests
import json
import re
import time
import random
from datetime import datetime
import cloudscraper
from urllib.parse import quote
import itertools


class StealthOSINT:
    """Stealth OSINT ที่หลีกเลี่ยง detection"""

    def __init__(self, target_username="alx.trading"):
        self.target = target_username
        self.real_data = {}
        self.found_passwords = []

        # Proxy lists (free proxies - ในการใช้งานจริงควรใช้ premium)
        self.proxies_list = [
            None,  # Direct connection
            # {'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'},  # Tor
        ]

        # User-Agent rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'
        ]

        self.session_count = 0

    def get_random_headers(self):
        """สร้าง headers แบบสุ่ม"""
        user_agent = random.choice(self.user_agents)

        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': random.choice(['en-US,en;q=0.9', 'en-GB,en;q=0.9', 'en-US,en;q=0.5']),
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }

        return headers

    def make_stealth_request(self, url, max_retries=3):
        """ทำ request แบบ stealth"""
        self.session_count += 1

        for attempt in range(max_retries):
            try:
                # สุ่ม delay 2-8 วินาที
                delay = random.uniform(2, 8)
                print(f"⏳ รอ {delay:.1f} วินาที...")
                time.sleep(delay)

                # สุ่ม proxy
                proxy = random.choice(self.proxies_list) if len(
                    self.proxies_list) > 1 else None

                # สร้าง session ใหม่
                scraper = cloudscraper.create_scraper(
                    browser={
                        'browser': random.choice(['chrome', 'firefox']),
                        'platform': random.choice(['windows', 'darwin', 'linux']),
                        'mobile': False
                    }
                )

                headers = self.get_random_headers()

                print(
                    f"🔄 Attempt {attempt + 1}/{max_retries} - Session {self.session_count}")
                print(f"🌐 URL: {url}")
                print(f"🎭 User-Agent: {headers['User-Agent'][:50]}...")

                response = scraper.get(
                    url,
                    headers=headers,
                    proxies=proxy,
                    timeout=15,
                    allow_redirects=True
                )

                print(f"📊 Status: {response.status_code}")

                if response.status_code == 200:
                    print("✅ Request สำเร็จ!")
                    return response
                elif response.status_code == 429:
                    print("⚠️ Rate limited - เพิ่ม delay...")
                    time.sleep(random.uniform(10, 20))
                elif response.status_code == 403:
                    print("⚠️ Forbidden - ลองเปลี่ยน User-Agent...")
                    time.sleep(random.uniform(5, 10))
                else:
                    print(f"⚠️ Status {response.status_code}")

            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(random.uniform(3, 7))

        print("❌ ทุก attempts ล้มเหลว")
        return None

    def search_instagram_manual(self):
        """ค้นหา Instagram แบบ manual methods"""
        print("📸 ค้นหา Instagram ด้วยวิธี Manual...")

        # วิธีที่ 1: ลองหา Instagram profile
        url = f"https://www.instagram.com/{self.target}/"
        response = self.make_stealth_request(url)

        if response and response.status_code == 200:
            print("✅ พบ Instagram Profile!")
            return self.extract_instagram_data(response.text)

        # วิธีที่ 2: ลองค้นหาผ่าง Google
        print("🔍 ลองค้นหาผ่าง Google...")
        google_query = f"site:instagram.com {self.target}"
        google_url = f"https://www.google.com/search?q={quote(google_query)}"

        response = self.make_stealth_request(google_url)
        if response:
            # หาลิงค์ Instagram จากผลการค้นหา
            instagram_links = re.findall(
                r'https://www\.instagram\.com/[^"\\]+', response.text)
            if instagram_links:
                print(f"🔗 พบ Instagram links: {instagram_links[:3]}")

        return None

    def extract_instagram_data(self, html_content):
        """ดึงข้อมูลจาก Instagram HTML"""
        data = {}

        # ดึงข้อมูลจาก meta tags
        patterns = {
            'title': r'<title>([^<]+)</title>',
            'description': r'<meta property="og:description" content="([^"]*)"',
            'image': r'<meta property="og:image" content="([^"]*)"'
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, html_content)
            if match:
                data[key] = match.group(1)
                print(f"📝 {key}: {data[key][:100]}...")

        # หาข้อมูลจาก JSON
        json_patterns = [
            r'window\._sharedData = ({.*?});',
            r'"biography":"([^"]*)"',
            r'"full_name":"([^"]*)"',
            r'"external_url":"([^"]*)"'
        ]

        for pattern in json_patterns:
            matches = re.findall(pattern, html_content)
            if matches:
                print(f"🔍 พบข้อมูล: {matches[0][:100]}...")

        return data

    def search_alternative_platforms(self):
        """ค้นหาใน platforms อื่นๆ ที่เข้าถึงง่ายกว่า"""
        print("🌐 ค้นหาใน Alternative Platforms...")

        platforms = [
            {
                'name': 'GitHub',
                'url': f'https://github.com/{self.target}',
                'patterns': [r'"name":"([^"]*)"', r'"bio":"([^"]*)"']
            },
            {
                'name': 'Twitter Search',
                'url': f'https://twitter.com/search?q={self.target}',
                'patterns': [r'"name":"([^"]*)"']
            },
            {
                'name': 'Reddit',
                'url': f'https://www.reddit.com/user/{self.target}',
                'patterns': [r'"title":"([^"]*)"']
            }
        ]

        found_data = {}

        for platform in platforms:
            print(f"\n🔍 ตรวจสอบ {platform['name']}...")

            response = self.make_stealth_request(platform['url'])

            if response and response.status_code == 200:
                print(f"✅ เข้าถึง {platform['name']} สำเร็จ!")

                # หาข้อมูลตาม patterns
                platform_data = {}
                for pattern in platform['patterns']:
                    matches = re.findall(pattern, response.text)
                    if matches:
                        platform_data[pattern] = matches[:5]  # เอาแค่ 5 ผลแรก

                if platform_data:
                    found_data[platform['name']] = platform_data
                    print(
                        f"📊 พบข้อมูลใน {platform['name']}: {len(platform_data)} patterns")
            else:
                print(f"❌ ไม่สามารถเข้าถึง {platform['name']}")

        return found_data

    def generate_passwords_from_found_data(self, found_data):
        """สร้างรหัสผ่านจากข้อมูลที่พบ"""
        print("🔑 สร้างรหัสผ่านจากข้อมูลที่พบ...")

        passwords = set()

        # ดึงข้อมูลจากทุก platform
        for platform, data in found_data.items():
            print(f"📱 วิเคราะห์ข้อมูลจาก {platform}...")

            for pattern, matches in data.items():
                for match in matches:
                    if isinstance(match, str) and len(match) > 2:
                        # ทำความสะอาดข้อมูล
                        clean_text = re.sub(r'[^a-zA-Z0-9]', '', match.lower())

                        if len(clean_text) >= 3:
                            passwords.update([
                                clean_text,
                                f"{clean_text}123",
                                f"alex{clean_text}",
                                f"{clean_text}alex",
                                f"{clean_text}2024",
                                f"{clean_text}2025"
                            ])

        # เพิ่มรหัสผ่านพื้นฐาน
        base_passwords = [
            "alex.trading", "alextrading", "alx.trading", "alxtrading",
            "alex_trading", "alx_trading", "trading123", "forex123",
            "crypto123", "money123", "rich123", "success123",
            "alex2024", "alex2025", "trading2024", "trading2025"
        ]
        passwords.update(base_passwords)

        return list(passwords)

    def comprehensive_stealth_search(self):
        """ค้นหาแบบ comprehensive stealth"""
        print("🕵️ เริ่ม Comprehensive Stealth Search...")
        print("=" * 60)

        all_found_data = {}

        # ลอง Instagram
        instagram_data = self.search_instagram_manual()
        if instagram_data:
            all_found_data['Instagram'] = instagram_data

        # ค้นหา platforms อื่น
        alt_data = self.search_alternative_platforms()
        all_found_data.update(alt_data)

        # สร้างรหัสผ่าน
        passwords = self.generate_passwords_from_found_data(all_found_data)

        return passwords, all_found_data

    def save_stealth_report(self, passwords, found_data):
        """บันทึกรายงาน Stealth OSINT"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        report = {
            "target": self.target,
            "generated_at": datetime.now().isoformat(),
            "method": "Stealth OSINT with Proxy Rotation",
            "sessions_used": self.session_count,
            "platforms_checked": list(found_data.keys()),
            "intelligence_summary": {
                "platforms_found": len(found_data),
                "total_passwords": len(passwords),
                "confidence_level": "High" if found_data else "Medium"
            },
            "found_data": found_data,
            "top_passwords": passwords[:50]
        }

        # บันทึก report
        report_file = f"/workspaces/sugarglitch-realops/stealth_osint_report_{timestamp}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        # บันทึก passwords
        password_file = f"/workspaces/sugarglitch-realops/stealth_passwords.txt"
        with open(password_file, 'w', encoding='utf-8') as f:
            f.write(f"# STEALTH OSINT PASSWORDS\n")
            f.write(f"# Target: {self.target}\n")
            f.write(f"# Method: Stealth with Proxy Rotation\n")
            f.write(f"# Sessions: {self.session_count}\n")
            f.write(f"# Generated: {datetime.now().isoformat()}\n")
            f.write("# ==========================================\n\n")

            for pwd in passwords:
                f.write(pwd + '\n')

        return report_file, password_file


def main():
    """Main Stealth OSINT function"""

    print("🕵️" * 15 + " STEALTH OSINT " + "🕵️" * 15)
    print("🎯 Target: alx.trading")
    print("🔒 Mode: STEALTH - PROXY ROTATION")
    print("=" * 70)

    stealth = StealthOSINT("alx.trading")

    print("\n🔍 Phase 1: Stealth Intelligence Gathering")
    passwords, found_data = stealth.comprehensive_stealth_search()

    print(f"\n📊 STEALTH OSINT RESULTS:")
    print("=" * 50)
    print(f"🔄 Sessions Used: {stealth.session_count}")
    print(f"🌐 Platforms Found: {len(found_data)}")
    print(f"🔑 Total Passwords: {len(passwords)}")

    if found_data:
        print(f"\n📱 PLATFORMS WITH DATA:")
        print("=" * 50)
        for platform, data in found_data.items():
            print(f"   ✅ {platform}: {len(data)} data points")

    print(f"\n🔥 TOP 30 STEALTH PASSWORDS:")
    print("=" * 50)
    for i, pwd in enumerate(passwords[:30], 1):
        print(f"   {i:2d}. {pwd}")

    # บันทึกรายงาน
    report_file, password_file = stealth.save_stealth_report(
        passwords, found_data)

    print(f"\n💾 Stealth Report Saved:")
    print(f"   📄 Report: {report_file}")
    print(f"   🔑 Passwords: {password_file}")

    print(f"\n🎯 NEXT ACTIONS:")
    print("=" * 50)
    print("1. 🔥 Test stealth-generated passwords")
    print("2. 🕵️ Manual verification of found data")
    print("3. 🔄 Repeat with different proxy/timing")
    print("4. 📊 Cross-reference with other OSINT")

    print(f"\n🕵️ STEALTH OSINT COMPLETE!")
    return passwords, found_data


if __name__ == "__main__":
    main()
