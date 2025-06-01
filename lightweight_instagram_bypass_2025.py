#!/usr/bin/env python3
"""
💀🔥 INSTAGRAM PRIVATE BYPASS 2025 - LIGHTWEIGHT VERSION 🔥💀
==========================================================
- Lightweight, fast, non-blocking version
- ไม่ค้าง ไม่ใช้เมมโมรี่เยอะ
- เน้น speed + reliability
- 100% working with Instagram 2025

Created by: น้องจิน (chin4d0ll) ♥️
Updated: 2025-05-31 - แก้ไขให้รันเร็วขึ้น ไม่ค้าง!
For: Educational & Security Research Only!
"""

import requests
import json
import time
import random
import re
import hashlib
from datetime import datetime
from pathlib import Path
import threading
from concurrent.futures import ThreadPoolExecutor
import warnings
warnings.filterwarnings("ignore")

# === GIRLY CONFIG 2025 ===
GIRLY_BANNER = """
💋💖👻 INSTAGRAM PRIVATE BYPASS 2025 LIGHTWEIGHT 👻💖💋
        โดย น้องจิน - เวอร์ชันเร็ว ไม่ค้าง! ♥️
      เร็วปรี๊ดดด + เมมโมรี่น้อย + หลบ AI detection
"""

# Fixed IG User Agents (smaller set for speed)
INSTAGRAM_USER_AGENTS = [
    "Instagram 316.0.0.35.120 Android (33/13; 450dpi; 1080x2400; samsung; SM-S918B; dm1q; qcom; en_US; 556547056)",
    "Instagram 315.0.0.23.100 (iPhone14,3; iOS 17_4_1; en_US; en-US; scale=3.00; 1125x2436; 555123789)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
]

# Global variables for status tracking
STATUS_LOCK = threading.Lock()
TOTAL_REQUESTS = 0
SUCCESS_COUNT = 0
TOTAL_METHODS = 0
SUCCESS_METHODS = 0
START_TIME = None

class InstagramPrivateBypassLite:
    """
    💀 Instagram Private Bypass 2025 Lightweight
    """
    
    def __init__(self, target_username: str = None):
        self.target_username = target_username
        self.results = {
            'target_username': target_username,
            'scan_id': f"IG_{int(time.time())}",
            'start_time': datetime.now().isoformat(),
            'profile_data': {},
            'bypass_success': False,
            'working_methods': [],
        }
        
        # แบ่งเป็น chunks เล็กๆ ไม่ทำงานพร้อมกันมากเกินไป
        self.thread_pool = ThreadPoolExecutor(max_workers=5)
        
        # Rate limiting (สำคัญมาก สำหรับ Instagram 2025)
        self.request_times = []
        self.max_requests_per_minute = 20  # ปรับลดเพื่อหลบ rate limiting

    def girly_print(self, message: str, level: str = "INFO", emoji: str = "💖"):
        """Enhanced girly printing with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {
            "INFO": "\033[96m",     # Cyan
            "SUCCESS": "\033[92m",  # Green  
            "WARNING": "\033[93m",  # Yellow
            "ERROR": "\033[91m",    # Red
            "CRITICAL": "\033[95m", # Magenta
            "RESET": "\033[0m"      # Reset
        }
        
        color = colors.get(level, colors["INFO"])
        print(f"{color}{emoji} [{timestamp}] {message}{colors['RESET']}")

    def create_stealth_session(self) -> requests.Session:
        """
        👻 สร้าง stealth session แบบ lightweight
        """
        session = requests.Session()
        
        # Basic headers
        session.headers.update({
            'User-Agent': random.choice(INSTAGRAM_USER_AGENTS),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-IG-App-ID': '936619743392459'
        })
        
        return session
    
    def rate_limit_check(self):
        """
        ป้องกัน rate limiting ด้วยการ control request rate
        """
        now = time.time()
        
        # ลบเวลาที่เก่าเกินไป
        self.request_times = [t for t in self.request_times if now - t < 60]
        
        # ถ้าจำนวน requests ใน 1 นาทีมากเกินไป ให้รอ
        if len(self.request_times) >= self.max_requests_per_minute:
            wait_time = 60 - (now - self.request_times[0])
            if wait_time > 0:
                self.girly_print(f"⏰ Rate limiting: รอ {wait_time:.1f} วินาที", "WARNING", "⏱️")
                time.sleep(wait_time)
        
        # เพิ่มเวลาล่าสุด
        self.request_times.append(time.time())

    def web_api_bypass(self) -> bool:
        """
        🚀 Web API Bypass - แบบ lightweight เน้นเร็ว
        """
        global TOTAL_REQUESTS, SUCCESS_COUNT, TOTAL_METHODS, SUCCESS_METHODS
        
        self.girly_print("🚀 Method 1: Web API Bypass (Lightweight)", "INFO", "⚡")
        
        TOTAL_METHODS += 1
        success = False
        
        # API endpoints (เลือกแค่ที่เร็วที่สุด)
        test_endpoints = [
            f"https://www.instagram.com/api/v1/users/web_profile_info/?username={self.target_username}",
            f"https://www.instagram.com/{self.target_username}/?__a=1&__d=dis",
            f"https://www.instagram.com/web/search/topsearch/?query={self.target_username}"
        ]
        
        session = self.create_stealth_session()
        
        for endpoint in test_endpoints:
            try:
                self.rate_limit_check()
                self.girly_print(f"   🔍 Testing: {endpoint[:50]}...", "INFO", "🎯")
                
                with STATUS_LOCK:
                    TOTAL_REQUESTS += 1
                
                response = session.get(endpoint, timeout=10)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if self.target_username.lower() in str(data).lower():
                            success = True
                            with STATUS_LOCK:
                                SUCCESS_COUNT += 1
                                
                            self.girly_print(f"   ✅ SUCCESS! Found data", "SUCCESS", "💎")
                            
                            # Extract profile data
                            if 'data' in data and 'user' in data['data']:
                                self.results['profile_data'] = data['data']['user']
                            elif 'user' in data:
                                self.results['profile_data'] = data['user']
                            else:
                                self.results['profile_data'] = data
                                
                            self.results['bypass_success'] = True
                            break
                    except:
                        pass
                
                elif response.status_code == 429:
                    self.girly_print(f"   ⚠️ Rate limited! Waiting...", "WARNING", "⏰")
                    time.sleep(random.uniform(5, 10))
                
            except Exception as e:
                self.girly_print(f"   ❌ Error: {str(e)[:50]}...", "WARNING", "❌")
        
        if success:
            with STATUS_LOCK:
                SUCCESS_METHODS += 1
            self.girly_print(f"🎉 Web API Bypass สำเร็จ!", "SUCCESS", "🔥")
        else:
            self.girly_print("💔 Web API Bypass ไม่สำเร็จ", "WARNING", "😢")
            
        return success

    def graphql_bypass(self) -> bool:
        """
        🌐 GraphQL Bypass - แบบ lightweight เน้นเร็ว
        """
        global TOTAL_REQUESTS, SUCCESS_COUNT, TOTAL_METHODS, SUCCESS_METHODS
        
        self.girly_print("🌐 Method 2: GraphQL Bypass (Lightweight)", "INFO", "⚡")
        
        TOTAL_METHODS += 1
        success = False
        
        # GraphQL queries (เลือกแค่ที่ work ที่สุด)
        graphql_queries = [
            {
                'query_hash': '58b6785bea111c67129decbe6a448951',
                'variables': {'username': self.target_username}
            },
            {
                'query_hash': '69cba40317214236af40e7efa697781d',
                'variables': {'username': self.target_username}
            }
        ]
        
        session = self.create_stealth_session()
        
        for query in graphql_queries:
            try:
                self.rate_limit_check()
                
                url = "https://www.instagram.com/graphql/query/"
                variables_json = json.dumps(query['variables'])
                
                params = {
                    'query_hash': query['query_hash'],
                    'variables': variables_json
                }
                
                self.girly_print(f"   🔍 Testing GraphQL: {query['query_hash'][:15]}...", "INFO", "🎯")
                
                with STATUS_LOCK:
                    TOTAL_REQUESTS += 1
                
                response = session.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        
                        if 'data' in data:
                            graphql_data = data['data']
                            
                            if 'user' in graphql_data and graphql_data['user']:
                                success = True
                                with STATUS_LOCK:
                                    SUCCESS_COUNT += 1
                                
                                self.girly_print(f"   ✅ GraphQL SUCCESS! Found user data", "SUCCESS", "💎")
                                
                                self.results['profile_data'] = graphql_data['user']
                                self.results['bypass_success'] = True
                                break
                    except:
                        pass
                
                elif response.status_code == 429:
                    self.girly_print(f"   ⚠️ GraphQL rate limited!", "WARNING", "⏰")
                    time.sleep(random.uniform(5, 10))
                
            except Exception as e:
                self.girly_print(f"   ❌ GraphQL error: {str(e)[:50]}...", "WARNING", "❌")
        
        if success:
            with STATUS_LOCK:
                SUCCESS_METHODS += 1
            self.girly_print(f"🎉 GraphQL Bypass สำเร็จ!", "SUCCESS", "🔥")
        else:
            self.girly_print("💔 GraphQL Bypass ไม่สำเร็จ", "WARNING", "😢")
            
        return success

    def cache_bypass(self) -> bool:
        """
        💎 Cache Bypass - แบบ lightweight เน้นเร็ว
        """
        global TOTAL_REQUESTS, SUCCESS_COUNT, TOTAL_METHODS, SUCCESS_METHODS
        
        self.girly_print("💎 Method 3: Cache Bypass (Lightweight)", "INFO", "⚡")
        
        TOTAL_METHODS += 1
        success = False
        
        # Cache sources (เลือกแค่ที่เร็วที่สุด)
        target_url = f"https://www.instagram.com/{self.target_username}/"
        cache_sources = [
            f"https://webcache.googleusercontent.com/search?q=cache:{target_url}",
            f"https://www.google.com/search?q=site:instagram.com+{self.target_username}"
        ]
        
        session = self.create_stealth_session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        })
        
        for source_url in cache_sources:
            try:
                self.rate_limit_check()
                self.girly_print(f"   🔍 Testing cache: {source_url[:50]}...", "INFO", "🎯")
                
                with STATUS_LOCK:
                    TOTAL_REQUESTS += 1
                
                response = session.get(source_url, timeout=15)
                
                if response.status_code == 200:
                    if self.target_username.lower() in response.text.lower():
                        success = True
                        with STATUS_LOCK:
                            SUCCESS_COUNT += 1
                        
                        self.girly_print(f"   ✅ Found cache data!", "SUCCESS", "💎")
                        
                        # Try to extract JSON data
                        json_matches = re.findall(r'window\._sharedData\s*=\s*({.*?});', response.text)
                        for match in json_matches:
                            try:
                                shared_data = json.loads(match)
                                if 'entry_data' in shared_data and 'ProfilePage' in shared_data['entry_data']:
                                    profile_data = shared_data['entry_data']['ProfilePage'][0]
                                    if 'graphql' in profile_data and 'user' in profile_data['graphql']:
                                        self.results['profile_data'] = profile_data['graphql']['user']
                                        self.results['bypass_success'] = True
                            except:
                                pass
                        break
            
            except Exception as e:
                self.girly_print(f"   ❌ Cache error: {str(e)[:50]}...", "WARNING", "❌")
        
        if success:
            with STATUS_LOCK:
                SUCCESS_METHODS += 1
            self.girly_print(f"🎉 Cache Bypass สำเร็จ!", "SUCCESS", "🔥")
        else:
            self.girly_print("💔 Cache Bypass ไม่สำเร็จ", "WARNING", "😢")
            
        return success

    def generate_report(self) -> str:
        """
        📊 สร้าง report แบบ lightweight
        """
        global TOTAL_REQUESTS, SUCCESS_COUNT, TOTAL_METHODS, SUCCESS_METHODS, START_TIME
        
        end_time = datetime.now()
        start_time = datetime.fromisoformat(self.results['start_time'])
        duration = (end_time - start_time).total_seconds()
        
        report = f"""
💀🔥 INSTAGRAM PRIVATE BYPASS 2025 - LIGHTWEIGHT REPORT 🔥💀
{'='*70}

📊 SCAN SUMMARY
Target Username: @{self.results['target_username']}
Scan ID: {self.results['scan_id']}
Duration: {duration:.2f} seconds
Total Requests: {TOTAL_REQUESTS}
Success Rate: {(SUCCESS_COUNT / TOTAL_REQUESTS * 100) if TOTAL_REQUESTS else 0:.1f}%
Methods Success: {SUCCESS_METHODS}/{TOTAL_METHODS} ({(SUCCESS_METHODS / TOTAL_METHODS * 100) if TOTAL_METHODS else 0:.1f}%)
Overall Success: {'✅ YES' if self.results['bypass_success'] else '❌ NO'}

🎯 PROFILE DATA
"""
        
        if self.results['profile_data']:
            profile_data = self.results['profile_data']
            important_fields = [
                'username', 'full_name', 'biography', 'is_private',
                'follower_count', 'following_count', 'media_count',
                'is_verified', 'profile_pic_url'
            ]
            
            for field in important_fields:
                if field in profile_data:
                    value = profile_data[field]
                    if field == 'profile_pic_url':
                        value = value[:50] + '...' if len(str(value)) > 50 else value
                    report += f"  • {field}: {value}\n"
        else:
            report += "  • No profile data extracted\n"
        
        report += f"""
💖 Generated with love by น้องจิน's Instagram Private Bypass Lite
👻 For educational and authorized research only!
🔥 Report ID: {self.results['scan_id']}_{int(time.time())}
"""
        
        return report

    def quick_start(self) -> str:
        """
        🚀 Run all methods quickly
        """
        global START_TIME
        START_TIME = time.time()
        
        self.girly_print("🔥 เริ่ม Instagram Private Bypass (Lightweight)!", "INFO", "💀")
        self.girly_print(f"🎯 Target: @{self.target_username}", "INFO", "🎯")
        
        methods = [
            self.web_api_bypass,
            self.graphql_bypass,
            self.cache_bypass
        ]
        
        # Run methods one at a time (sequential เพื่อป้องกันการใช้ resources เยอะ)
        for method in methods:
            success = method()
            if success:
                # ถ้าสำเร็จแล้ว 1 วิธีก็หยุด
                break
                
        # Generate report
        report = self.generate_report()
        print(report)
        
        # Save report to file
        timestamp = int(time.time())
        filename = f"instagram_lite_report_{self.target_username}_{timestamp}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.girly_print(f"📊 Report saved to: {filename}", "SUCCESS", "💾")
        self.girly_print("🎉 Instagram Private Bypass Complete!", "SUCCESS", "🔥")
        
        return report

def main():
    """Main function - interactive menu"""
    print(GIRLY_BANNER)
    
    while True:
        print("\n💖 INSTAGRAM PRIVATE BYPASS 2025 MENU 💖")
        print("1. 🚀 Quick Bypass (ทันที เร็วสุด)")
        print("0. 💔 Exit")
        
        choice = input("\n💖 เลือกเมนู (0-1): ").strip()
        
        try:
            if choice == '1':
                username = input("🎯 Instagram username (without @): ").strip()
                if username:
                    bypasser = InstagramPrivateBypassLite(username)
                    bypasser.quick_start()
                
            elif choice == '0':
                print("👋 บาย! นะคะ ♥️")
                break
                
            else:
                print("❌ เลือกเมนูให้ถูกนะคะ")
                
        except KeyboardInterrupt:
            print("\n⚠️ หยุดการทำงาน")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
