# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Instagram API Response Analyzer - วิเคราะห์ข้อมูลที่ได้จาก bypass
"""

import json
import sqlite3
import requests
from datetime import datetime
import os

class InstagramDataAnalyzer:
    def __init__(self):
        self.db_name = f"instagram_analysis_{int(datetime.now().timestamp())}.sqlite"
        self.init_database()

    def init_database(self):
        """สร้าง database สำหรับเก็บข้อมูลวิเคราะห์"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profile_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                user_id TEXT,
                full_name TEXT,
                biography TEXT,
                follower_count INTEGER,
                following_count INTEGER,
                media_count INTEGER,
                is_private BOOLEAN,
                is_verified BOOLEAN,
                profile_pic_url TEXT,
                external_url TEXT,
                analysis_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                raw_data TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bypass_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_url TEXT,
                response_size INTEGER,
                success BOOLEAN,
                method TEXT,
                proxy_used TEXT,
                attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT
            )
        ''')

        conn.commit()
        conn.close()
        print(f"[DB] Database initialized: {self.db_name}")

    def test_live_extraction(self, target_username="alx.trading"):
        """ทดสอบการ extract ข้อมูลจริงจาก Instagram"""
        try:
            # Use advanced_rate_bypass_arsenal_2025.py to get real data
            print(f"[LIVE] Testing live extraction for {target_username}")

            # Create a simple session with sessionid
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Instagram 308.0.0.16.113 Android (30/11; 450dpi; 1080x2400; samsung; SM-G991B)',
                'Accept': 'application/json,text/plain,*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'X-IG-App-ID': '936619743392459',
                'X-Requested-With': 'XMLHttpRequest',
            })

            # Load session cookie
            try:
                with open('sessions/alx_trading_sessionid_1748519701.json', 'r') as f:
                    session_data = json.load(f)
                    if 'sessionid' in session_data:
                        session.cookies.set('sessionid', session_data['sessionid'])
                        print(f"[AUTH] Loaded sessionid")
            except Exception as e:
                print(f"[AUTH] No session cookie: {e}")

            # Try to get profile data
            url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={target_username}"

            response = session.get(url, timeout=10)
            print(f"[LIVE] Response status: {response.status_code}")
            print(f"[LIVE] Response size: {len(response.content)} bytes")

            if response.status_code == 200:
                try:
                    data = response.json()
                    self.analyze_profile_data(data, target_username)
                    self.save_bypass_attempt(url, len(response.content), True, "direct", "none")
                    return data
                except json.JSONDecodeError:
                    print(f"[ERROR] Invalid JSON response")
                    print(f"[PREVIEW] {response.text[:500]}...")
            else:
                print(f"[ERROR] Failed with status {response.status_code}")
                print(f"[PREVIEW] {response.text[:500]}...")
                self.save_bypass_attempt(url, len(response.content), False, "direct", "none")

        except Exception as e:
            print(f"[ERROR] Exception in live extraction: {e}")

        return None

    def analyze_profile_data(self, data, username):
        """วิเคราะห์ข้อมูล profile ที่ได้มา"""
        try:
            if 'data' in data and 'user' in data['data']:
                user_data = data['data']['user']

                profile_info = {
                    'username': username,
                    'user_id': user_data.get('id', ''),
                    'full_name': user_data.get('full_name', ''),
                    'biography': user_data.get('biography', ''),
                    'follower_count': user_data.get('edge_followed_by', {}).get('count', 0),
                    'following_count': user_data.get('edge_follow', {}).get('count', 0),
                    'media_count': user_data.get('edge_owner_to_timeline_media', {}).get('count', 0),
                    'is_private': user_data.get('is_private', False),
                    'is_verified': user_data.get('is_verified', False),
                    'profile_pic_url': user_data.get('profile_pic_url_hd', ''),
                    'external_url': user_data.get('external_url', ''),
                    'raw_data': json.dumps(data)
                }

                # Save to database
                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()

                cursor.execute('''
                    INSERT INTO profile_analysis (
                        username, user_id, full_name, biography, follower_count,
                        following_count, media_count, is_private, is_verified,
                        profile_pic_url, external_url, raw_data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    profile_info['username'], profile_info['user_id'], profile_info['full_name'],
                    profile_info['biography'], profile_info['follower_count'], profile_info['following_count'],
                    profile_info['media_count'], profile_info['is_private'], profile_info['is_verified'],
                    profile_info['profile_pic_url'], profile_info['external_url'], profile_info['raw_data']
                ))

                conn.commit()
                conn.close()

                print(f"[ANALYSIS] Profile data saved for {username}")
                print(f"  User ID: {profile_info['user_id']}")
                print(f"  Full Name: {profile_info['full_name']}")
                print(f"  Followers: {profile_info['follower_count']:,}")
                print(f"  Following: {profile_info['following_count']:,}")
                print(f"  Posts: {profile_info['media_count']:,}")
                print(f"  Private: {profile_info['is_private']}")
                print(f"  Verified: {profile_info['is_verified']}")

                return profile_info

        except Exception as e:
            print(f"[ERROR] Failed to analyze profile data: {e}")

        return None

    def save_bypass_attempt(self, url, response_size, success, method, proxy):
        """บันทึกการพยายาม bypass"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO bypass_attempts (target_url, response_size, success, method, proxy_used)
                VALUES (?, ?, ?, ?, ?)
            ''', (url, response_size, success, method, proxy))

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"[ERROR] Failed to save bypass attempt: {e}")

    def generate_report(self):
        """สร้างรายงานการวิเคราะห์"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            print(f"\n🔍 INSTAGRAM BYPASS ANALYSIS REPORT")
            print(f"="*50)

            # Profile analysis
            cursor.execute("SELECT COUNT(*) FROM profile_analysis")
            profile_count = cursor.fetchone()[0]
            print(f"📊 Profiles analyzed: {profile_count}")

            if profile_count > 0:
                cursor.execute('''
                    SELECT username, full_name, follower_count, following_count,
                           media_count, is_private, is_verified
                    FROM profile_analysis ORDER BY analysis_time DESC
                ''')

                profiles = cursor.fetchall()
                for profile in profiles:
                    username, full_name, followers, following, posts, private, verified = profile
                    print(f"\n👤 {username} ({full_name})")
                    print(f"   📈 {followers:,} followers, {following:,} following, {posts:,} posts")
                    print(f"   🔒 Private: {private}, ✅ Verified: {verified}")

            # Bypass attempts
            cursor.execute("SELECT COUNT(*), SUM(success) FROM bypass_attempts")
            total_attempts, successful = cursor.fetchone()
            success_rate = (successful / total_attempts * 100) if total_attempts > 0 else 0

            print(f"\n🎯 BYPASS STATISTICS")
            print(f"   Total attempts: {total_attempts}")
            print(f"   Successful: {successful}")
            print(f"   Success rate: {success_rate:.1f}%")

            conn.close()

        except Exception as e:
            print(f"[ERROR] Failed to generate report: {e}")

def main():
    analyzer = InstagramDataAnalyzer()

    # Test live extraction
    targets = ["alx.trading", "whatilove1728"]

    for target in targets:
        print(f"\n🎯 Testing {target}...")
        data = analyzer.test_live_extraction(target)

    # Generate report
    analyzer.generate_report()

    print(f"\n💾 Analysis saved to: {analyzer.db_name}")

if __name__ == "__main__":
    main()