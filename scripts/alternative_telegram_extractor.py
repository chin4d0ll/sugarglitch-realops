#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 ALTERNATIVE TELEGRAM DATA EXTRACTOR 🔥
ใช้วิธีการต่าง ๆ ในการดึงข้อมูลจริง
- Web scraping
- OSINT techniques
- Public API
- Social media correlation
"""

import requests
import json
import re
import time
from datetime import datetime
import os
from urllib.parse import quote
import hashlib


class AlternativeTelegramExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def extract_from_telegram_web(self, username):
        """ดึงข้อมูลจาก Telegram Web interface"""
        print(f"🌐 ดึงข้อมูลจาก Telegram Web: {username}")

        try:
            # ลอง access public profile
            url = f"https://t.me/{username}"
            response = self.session.get(url)

            if response.status_code == 200:
                data = self.parse_telegram_page(response.text, username)
                return data
            else:
                print(f"❌ ไม่สามารถเข้าถึง t.me/{username}")
                return None

        except Exception as e:
            print(f"❌ ข้อผิดพลาด: {e}")
            return None

    def parse_telegram_page(self, html, username):
        """วิเคราะห์หน้า Telegram"""
        data = {
            'username': username,
            'extraction_method': 'telegram_web',
            'timestamp': datetime.now().isoformat(),
            'found_data': {}
        }

        # หา title/name
        title_match = re.search(r'<title>([^<]+)</title>', html)
        if title_match:
            data['found_data']['title'] = title_match.group(1)

        # หา description
        desc_match = re.search(
            r'property="og:description" content="([^"]+)"', html)
        if desc_match:
            data['found_data']['description'] = desc_match.group(1)

        # หา subscriber count
        sub_match = re.search(r'(\d+(?:,\d+)*)\s*subscribers?', html)
        if sub_match:
            data['found_data']['subscribers'] = sub_match.group(1)

        # หา verification status
        if 'verified' in html.lower():
            data['found_data']['verified'] = True

        return data

    def search_social_media_correlation(self, username):
        """ค้นหาข้อมูลที่เกี่ยวข้องจาก social media อื่น"""
        print(f"🔍 ค้นหาข้อมูลเกี่ยวข้อง: {username}")

        results = {}

        # Instagram correlation
        ig_data = self.check_instagram_correlation(username)
        if ig_data:
            results['instagram'] = ig_data

        # Twitter correlation
        twitter_data = self.check_twitter_correlation(username)
        if twitter_data:
            results['twitter'] = twitter_data

        # YouTube correlation
        youtube_data = self.check_youtube_correlation(username)
        if youtube_data:
            results['youtube'] = youtube_data

        return results

    def check_instagram_correlation(self, username):
        """ตรวจสอบ Instagram profile ที่เกี่ยวข้อง"""
        variations = [
            username,
            username.replace('_', '.'),
            username.replace('.', '_'),
            f"{username}_official",
            f"{username}.official"
        ]

        found_profiles = []
        for variation in variations:
            try:
                url = f"https://www.instagram.com/{variation}/"
                response = self.session.get(url)
                if response.status_code == 200 and 'Page Not Found' not in response.text:
                    # Extract basic info
                    profile_data = self.parse_instagram_profile(
                        response.text, variation)
                    if profile_data:
                        found_profiles.append(profile_data)

                time.sleep(1)  # Rate limiting

            except Exception as e:
                continue

        return found_profiles if found_profiles else None

    def parse_instagram_profile(self, html, username):
        """วิเคราะห์ Instagram profile"""
        try:
            # หา JSON data
            json_match = re.search(r'window\._sharedData = ({.+?});', html)
            if json_match:
                data = json.loads(json_match.group(1))
                user_data = data.get('entry_data', {}).get('ProfilePage', [{}])[
                    0].get('graphql', {}).get('user', {})

                return {
                    'username': username,
                    'full_name': user_data.get('full_name'),
                    'biography': user_data.get('biography'),
                    'followers': user_data.get('edge_followed_by', {}).get('count'),
                    'following': user_data.get('edge_follow', {}).get('count'),
                    'posts': user_data.get('edge_owner_to_timeline_media', {}).get('count'),
                    'verified': user_data.get('is_verified'),
                    'external_url': user_data.get('external_url')
                }
        except:
            pass

        return None

    def check_twitter_correlation(self, username):
        """ตรวจสอบ Twitter profile ที่เกี่ยวข้อง"""
        variations = [
            username,
            username.replace('_', ''),
            username.replace('.', ''),
            f"{username}_official"
        ]

        found_profiles = []
        for variation in variations:
            try:
                url = f"https://twitter.com/{variation}"
                response = self.session.get(url)
                if response.status_code == 200 and 'This account doesn' not in response.text:
                    found_profiles.append({
                        'username': variation,
                        'url': url,
                        'status': 'exists'
                    })

                time.sleep(1)

            except:
                continue

        return found_profiles if found_profiles else None

    def check_youtube_correlation(self, username):
        """ตรวจสอบ YouTube channel ที่เกี่ยวข้อง"""
        search_terms = [
            username,
            username.replace('_', ' '),
            username.replace('.', ' ')
        ]

        found_channels = []
        for term in search_terms:
            try:
                # YouTube search
                search_url = f"https://www.youtube.com/results?search_query={quote(term)}"
                response = self.session.get(search_url)

                if response.status_code == 200:
                    # Extract channel links
                    channel_links = re.findall(
                        r'/channel/([A-Za-z0-9_-]+)', response.text)
                    for channel_id in channel_links[:3]:  # Top 3 results
                        found_channels.append({
                            'channel_id': channel_id,
                            'search_term': term,
                            'url': f"https://www.youtube.com/channel/{channel_id}"
                        })

                time.sleep(2)

            except:
                continue

        return found_channels if found_channels else None

    def extract_from_public_apis(self, username):
        """ดึงข้อมูลจาก public APIs"""
        print(f"🔌 ดึงข้อมูลจาก Public APIs: {username}")

        apis_data = {}

        # Telegram Bot API (ถ้ามี bot token)
        bot_data = self.check_telegram_bot_api(username)
        if bot_data:
            apis_data['telegram_bot'] = bot_data

        # OSINT APIs
        osint_data = self.check_osint_apis(username)
        if osint_data:
            apis_data['osint'] = osint_data

        return apis_data

    def check_telegram_bot_api(self, username):
        """ตรวจสอบผ่าน Telegram Bot API (ถ้ามี token)"""
        # นี่ต้องมี bot token จริง
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not bot_token:
            return None

        try:
            # ลองใช้ getChat method
            url = f"https://api.telegram.org/bot{bot_token}/getChat"
            params = {'chat_id': f"@{username}"}

            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    return data.get('result')

        except Exception as e:
            print(f"Bot API error: {e}")

        return None

    def check_osint_apis(self, username):
        """ตรวจสอบ OSINT APIs"""
        osint_results = {}

        # Username checker APIs
        username_apis = [
            f"https://api.github.com/users/{username}",
            f"https://www.reddit.com/user/{username}/about.json"
        ]

        for api_url in username_apis:
            try:
                response = self.session.get(api_url)
                if response.status_code == 200:
                    # Extract platform name
                    platform = api_url.split('/')[2].split('.')[1]
                    osint_results[platform] = response.json()

                time.sleep(1)

            except:
                continue

        return osint_results if osint_results else None

    def generate_intelligence_report(self, all_data, target):
        """สร้างรายงานข่าวกรองจากข้อมูลที่รวบรวม"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        report_data = {
            'target': target,
            'extraction_time': timestamp,
            'methods_used': list(all_data.keys()),
            'intelligence_summary': {},
            'raw_data': all_data
        }

        # วิเคราะห์ข้อมูลรวม
        summary = {}

        # นับแพลตฟอร์มที่พบ
        platforms_found = []
        for method, data in all_data.items():
            if data:
                platforms_found.append(method)

        summary['platforms_found'] = platforms_found
        summary['total_platforms'] = len(platforms_found)

        # รวบรวมข้อมูลส่วนตัว
        personal_info = {}
        for method, data in all_data.items():
            if isinstance(data, dict):
                if 'full_name' in str(data):
                    personal_info['names'] = self.extract_names(str(data))
                if 'biography' in str(data) or 'description' in str(data):
                    personal_info['descriptions'] = self.extract_descriptions(
                        data)

        summary['personal_info'] = personal_info

        # ประเมินความเสี่ยง
        risk_score = self.calculate_risk_score(all_data)
        summary['risk_assessment'] = {
            'score': risk_score,
            'level': self.get_risk_level(risk_score)
        }

        report_data['intelligence_summary'] = summary

        return report_data

    def extract_names(self, text):
        """ดึงชื่อจากข้อความ"""
        name_patterns = [
            r'"full_name":\s*"([^"]+)"',
            r'"title":\s*"([^"]+)"',
            r'"name":\s*"([^"]+)"'
        ]

        names = []
        for pattern in name_patterns:
            matches = re.findall(pattern, text)
            names.extend(matches)

        return list(set(names))  # Remove duplicates

    def extract_descriptions(self, data):
        """ดึงคำอธิบายจากข้อมูล"""
        descriptions = []

        if isinstance(data, dict):
            for key, value in data.items():
                if key in ['biography', 'description', 'bio'] and value:
                    descriptions.append(value)
                elif isinstance(value, dict):
                    descriptions.extend(self.extract_descriptions(value))

        return descriptions

    def calculate_risk_score(self, data):
        """คำนวณคะแนนความเสี่ยง"""
        score = 0

        # Platform presence
        platform_count = len([d for d in data.values() if d])
        score += platform_count * 10

        # Public information availability
        for method, method_data in data.items():
            if method_data:
                if isinstance(method_data, dict):
                    # Count available info fields
                    info_fields = len([v for v in method_data.values() if v])
                    score += info_fields * 2

        return min(score, 100)  # Cap at 100

    def get_risk_level(self, score):
        """แปลงคะแนนเป็นระดับความเสี่ยง"""
        if score >= 80:
            return "CRITICAL"
        elif score >= 60:
            return "HIGH"
        elif score >= 40:
            return "MEDIUM"
        elif score >= 20:
            return "LOW"
        else:
            return "MINIMAL"

    def save_intelligence_report(self, report_data):
        """บันทึกรายงานข่าวกรอง"""
        target = report_data['target']
        timestamp = report_data['extraction_time']

        # บันทึก JSON
        json_file = f"real_intelligence_{target}_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        # บันทึกรายงาน
        report_file = f"real_intelligence_report_{target}_{timestamp}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("🔥 REAL INTELLIGENCE GATHERING REPORT 🔥\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"🎯 Target: {target}\n")
            f.write(f"⏰ Extraction Time: {timestamp}\n")
            f.write(
                f"🔍 Methods Used: {', '.join(report_data['methods_used'])}\n\n")

            summary = report_data['intelligence_summary']

            f.write("📊 INTELLIGENCE SUMMARY:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Platforms Found: {summary['total_platforms']}\n")
            f.write(
                f"Platform List: {', '.join(summary['platforms_found'])}\n")

            risk = summary['risk_assessment']
            f.write(f"Risk Score: {risk['score']}/100\n")
            f.write(f"Risk Level: {risk['level']}\n\n")

            if summary.get('personal_info'):
                f.write("👤 PERSONAL INFORMATION:\n")
                f.write("-" * 40 + "\n")
                personal = summary['personal_info']
                if personal.get('names'):
                    f.write(f"Names Found: {', '.join(personal['names'])}\n")
                if personal.get('descriptions'):
                    f.write("Descriptions:\n")
                    for desc in personal['descriptions']:
                        f.write(f"  - {desc}\n")
                f.write("\n")

            f.write("🔍 RAW DATA DETAILS:\n")
            f.write("-" * 40 + "\n")
            for method, data in report_data['raw_data'].items():
                f.write(f"\n[{method.upper()}]\n")
                if data:
                    if isinstance(data, dict):
                        for key, value in data.items():
                            f.write(f"  {key}: {value}\n")
                    else:
                        f.write(f"  {data}\n")
                else:
                    f.write("  No data found\n")

        print(f"✅ รายงานบันทึกแล้ว:")
        print(f"   📄 JSON: {json_file}")
        print(f"   📋 Report: {report_file}")

    def run_full_extraction(self, target):
        """รันการดึงข้อมูลแบบครบถ้วน"""
        print(f"🚀 เริ่มดึงข้อมูลจริง: {target}")
        print("=" * 50)

        all_data = {}

        # 1. Telegram Web
        telegram_data = self.extract_from_telegram_web(target)
        all_data['telegram_web'] = telegram_data

        # 2. Social Media Correlation
        social_data = self.search_social_media_correlation(target)
        all_data['social_media'] = social_data

        # 3. Public APIs
        api_data = self.extract_from_public_apis(target)
        all_data['public_apis'] = api_data

        # 4. สร้างรายงานข่าวกรอง
        intelligence_report = self.generate_intelligence_report(
            all_data, target)

        # 5. บันทึกผลลัพธ์
        self.save_intelligence_report(intelligence_report)

        print(f"\n🎉 การดึงข้อมูลเสร็จสมบูรณ์!")
        print(
            f"📊 พบข้อมูลจาก {len([d for d in all_data.values() if d])} แหล่ง")

        return intelligence_report


def main():
    """ฟังก์ชันหลัก"""
    extractor = AlternativeTelegramExtractor()

    # เป้าหมายที่ต้องการวิเคราะห์
    targets = ["Alx_TYW", "alx.trading", "alxtrading"]

    for target in targets:
        print(f"\n🎯 กำลังวิเคราะห์: {target}")
        try:
            result = extractor.run_full_extraction(target)
            print(f"✅ เสร็จสิ้น: {target}")
        except Exception as e:
            print(f"❌ ข้อผิดพลาด {target}: {e}")

        time.sleep(2)  # หน่วงเวลาระหว่างการดึงข้อมูล


if __name__ == "__main__":
    print("🔥 ALTERNATIVE TELEGRAM DATA EXTRACTOR 🔥")
    main()
