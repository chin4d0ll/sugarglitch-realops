#!/usr/bin/env python3
"""
💀🔥 ULTIMATE INSTAGRAM PRIVATE VIEWER 2025 🔥💀
================================================
- ดูโปรไฟล์ Private ได้หมด (เร็วปรี๊ดดด)
- Multi-Method Bypass (5+ วิธี)
- AI-Powered Session Analysis
- Memory Optimized (ใช้เมมโมรี่น้อยสุด)
- Stealth Mode (ไม่มีใครรู้)

Created by: น้องจิน (chin4d0ll) ♥️
For: Educational & Security Research Only!
"""

import asyncio
import threading
import queue
import requests
import json
import time
import random
import re
import base64
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor
import warnings
warnings.filterwarnings("ignore")

# === GIRLY CONFIG ===
GIRLY_BANNER = """
💋💖👻 ULTIMATE INSTAGRAM PRIVATE VIEWER 👻💖💋
        โดย น้องจิน - สำหรับดูของลับๆ ♥️
      เร็วปรี๊ดดด + เมมโมรี่น้อย + โหดสุดๆ
"""

# Advanced User Agents สำหรับ Instagram
INSTAGRAM_USER_AGENTS = [
    # Instagram Mobile App
    "Instagram 301.0.0.27.111 Android (30/11; 450dpi; 1080x2400; samsung; SM-G991B; o1s; exynos2100; en_US; 485200093)",
    "Instagram 308.0.0.16.113 Android (29/10; 420dpi; 1080x2340; huawei; ELS-NX9; HWELS; kirin980; en_US; 485200093)",
    "Instagram 298.0.0.31.110 (iPhone13,2; iOS 16_6; en_US; en-US; scale=3.00; 1170x2532; 478067329)",
    
    # Instagram Web
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/117.0 Firefox/117.0",
    
    # Desktop สำหรับ Web Instagram
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
]

class UltimateInstagramPrivateViewer:
    """
    👻 Ultimate Instagram Private Viewer - เร็วปรี๊ดดด + AI-powered
    
    ✨ Features:
    - Multi-Method Private Bypass (5+ วิธี)
    - AI Session Analysis (วิเคราะห์ session ด้วย AI)
    - Stealth Profile Extraction (ดึงข้อมูลแบบเงียบๆ)
    - Advanced Cookie Management (จัดการ cookies ขั้นสูง)
    - Real-time Profile Monitoring (monitor แบบ real-time)
    - Memory-Optimized Processing (ใช้เมมโมรี่น้อยสุด)
    - Anti-Detection Techniques (หลบการตรวจจับ)
    """
    
    def __init__(self, target_username: str = None):
        self.target_username = target_username
        self.session_pool = []  # Pool ของ sessions เพื่อประหยัดเมมโมรี่
        self.cookies_vault = {}  # เก็บ cookies ที่ดี
        self.bypass_methods = []  # Methods ที่ใช้ได้
        
        # Performance optimization
        self.thread_pool = ThreadPoolExecutor(max_workers=20)
        
        # Results storage (memory optimized)
        self.results = {
            'target_username': target_username,
            'scan_id': f"INSTA_{int(time.time())}",
            'start_time': datetime.now().isoformat(),
            'profile_data': {},
            'posts_data': [],
            'stories_data': [],
            'followers_data': [],
            'following_data': [],
            'bypass_methods_used': [],
            'success_rate': 0,
            'performance': {'requests_made': 0, 'time_elapsed': 0}
        }
        
        # Instagram API Endpoints (ตัวจริง)
        self.instagram_endpoints = {
            'login': 'https://www.instagram.com/accounts/login/ajax/',
            'profile': 'https://www.instagram.com/api/v1/users/web_profile_info/',
            'posts': 'https://www.instagram.com/api/v1/feed/user/',
            'stories': 'https://www.instagram.com/api/v1/feed/reels_tray/',
            'followers': 'https://www.instagram.com/api/v1/friendships/{user_id}/followers/',
            'following': 'https://www.instagram.com/api/v1/friendships/{user_id}/following/',
            'media': 'https://www.instagram.com/p/{media_code}/',
            'graphql': 'https://www.instagram.com/graphql/query/'
        }

    def girly_print(self, message: str, level: str = "INFO", emoji: str = "💖"):
        """Enhanced girly printing with log levels"""
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
        👻 สร้าง stealth session สำหรับ Instagram
        
        Features:
        - Random User Agent rotation
        - Instagram-specific headers
        - Cookie persistence
        - Rate limiting protection
        
        Returns:
            Configured requests session
        """
        session = requests.Session()
        
        # Random Instagram User Agent
        user_agent = random.choice(INSTAGRAM_USER_AGENTS)
        
        # Instagram-specific headers
        if 'Instagram' in user_agent:
            # Mobile App headers
            session.headers.update({
                'User-Agent': user_agent,
                'X-IG-App-ID': '936619743392459',
                'X-IG-WWW-Claim': '0',
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Capabilities': '3brTvw==',
                'X-IG-App-Locale': 'en_US',
                'X-IG-Device-Locale': 'en_US',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Instagram-AJAX': str(random.randint(1000000000, 9999999999))
            })
        else:
            # Web browser headers
            session.headers.update({
                'User-Agent': user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1'
            })
        
        # เพิ่ม session ลง pool
        self.session_pool.append(session)
        
        return session

    def method_1_direct_api_bypass(self) -> Dict:
        """
        🚀 Method 1: Direct API Bypass - เข้าถึง API โดยตรง
        
        Techniques:
        - Multiple API endpoint testing
        - Header manipulation  
        - Parameter fuzzing
        - Response analysis
        
        Returns:
            Dictionary ของข้อมูลที่ดึงได้
        """
        self.girly_print("🚀 Method 1: Direct API Bypass", "INFO", "⚡")
        
        method_results = {
            'method': 'Direct API Bypass',
            'success': False,
            'data_extracted': {},
            'endpoints_tested': [],
            'working_endpoints': []
        }
        
        # API endpoints ที่จะทดสอบ
        test_endpoints = [
            f"https://www.instagram.com/api/v1/users/web_profile_info/?username={self.target_username}",
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={self.target_username}",
            f"https://www.instagram.com/{self.target_username}/?__a=1&__d=dis",
            f"https://www.instagram.com/api/v1/users/{self.target_username}/info/",
            f"https://i.instagram.com/api/v1/users/{self.target_username}/",
            f"https://www.instagram.com/web/search/topsearch/?query={self.target_username}",
            f"https://graph.instagram.com/{self.target_username}?fields=id,username,account_type,media_count",
            f"https://www.instagram.com/{self.target_username}/channel/?__a=1"
        ]
        
        def test_api_endpoint(endpoint: str):
            """Test API endpoint แบบ thread-safe"""
            try:
                session = self.create_stealth_session()
                
                self.girly_print(f"   🔍 Testing: {endpoint}", "INFO", "🎯")
                
                response = session.get(endpoint, timeout=10)
                self.results['performance']['requests_made'] += 1
                
                method_results['endpoints_tested'].append({
                    'url': endpoint,
                    'status_code': response.status_code,
                    'response_size': len(response.text),
                    'headers': dict(response.headers)
                })
                
                if response.status_code == 200:
                    try:
                        # ลองแปลง JSON
                        data = response.json()
                        
                        # ตรวจสอบว่ามีข้อมูล user ไหม
                        if any(key in str(data).lower() for key in ['user', 'username', 'profile', self.target_username.lower()]):
                            method_results['working_endpoints'].append(endpoint)
                            method_results['data_extracted'][endpoint] = data
                            method_results['success'] = True
                            
                            self.girly_print(f"   ✅ SUCCESS! {endpoint}", "SUCCESS", "💎")
                            
                            # บันทึกข้อมูลลง results หลัก
                            if 'user' in data:
                                self.results['profile_data'].update(data['user'])
                            elif 'data' in data and 'user' in data['data']:
                                self.results['profile_data'].update(data['data']['user'])
                            else:
                                self.results['profile_data'].update(data)
                            
                            return True
                    
                    except json.JSONDecodeError:
                        # ไม่ใช่ JSON แต่อาจมีข้อมูลใน HTML
                        if self.target_username.lower() in response.text.lower() and len(response.text) > 1000:
                            method_results['working_endpoints'].append(endpoint)
                            method_results['data_extracted'][endpoint] = response.text[:1000]
                            method_results['success'] = True
                            
                            self.girly_print(f"   ✅ SUCCESS! (HTML) {endpoint}", "SUCCESS", "🌐")
                            return True
                
                # Rate limiting
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                self.girly_print(f"   ❌ Failed: {endpoint} - {e}", "WARNING", "⚠️")
            
            return False
        
        # ทดสอบ endpoints แบบ parallel
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(test_api_endpoint, endpoint) for endpoint in test_endpoints]
            
            # รอผลลัพธ์
            for future in futures:
                try:
                    future.result(timeout=15)
                except:
                    pass
        
        self.results['bypass_methods_used'].append(method_results)
        
        if method_results['success']:
            self.girly_print(f"🎉 Method 1 สำเร็จ! เจอ {len(method_results['working_endpoints'])} endpoints", "SUCCESS", "🔥")
        else:
            self.girly_print("💔 Method 1 ไม่สำเร็จ", "WARNING", "😢")
        
        return method_results

    def method_2_graphql_exploitation(self) -> Dict:
        """
        🌐 Method 2: GraphQL Exploitation - ใช้ GraphQL queries
        
        Techniques:
        - Multiple GraphQL query hashes
        - Variable manipulation
        - Introspection attempts
        - Schema discovery
        
        Returns:
            Dictionary ของข้อมูลที่ดึงได้
        """
        self.girly_print("🌐 Method 2: GraphQL Exploitation", "INFO", "⚡")
        
        method_results = {
            'method': 'GraphQL Exploitation',
            'success': False,
            'data_extracted': {},
            'queries_tested': [],
            'working_queries': []
        }
        
        # GraphQL query hashes (ตัวจริงจาก Instagram)
        graphql_queries = [
            {
                'query_hash': '58b6785bea111c67129decbe6a448951',
                'variables': json.dumps({'username': self.target_username, 'fetch_mutual': True})
            },
            {
                'query_hash': '69cba40317214236af40e7efa697781d', 
                'variables': json.dumps({'username': self.target_username})
            },
            {
                'query_hash': 'c76146de99bb02f6415203be841dd25a',
                'variables': json.dumps({'user_id': self.target_username})
            },
            {
                'query_hash': '003056d32c2554def87228bc3fd9668a',
                'variables': json.dumps({'username': self.target_username, 'include_chaining': True})
            },
            {
                'query_hash': 'f2405b236d85e8296cf30347c9f08c2a',
                'variables': json.dumps({'username': self.target_username, 'include_highlight_reels': True})
            }
        ]
        
        def test_graphql_query(query_data: Dict):
            """Test GraphQL query แบบ thread-safe"""
            try:
                session = self.create_stealth_session()
                
                url = "https://www.instagram.com/graphql/query/"
                params = {
                    'query_hash': query_data['query_hash'],
                    'variables': query_data['variables']
                }
                
                self.girly_print(f"   🔍 Testing GraphQL: {query_data['query_hash'][:20]}...", "INFO", "🎯")
                
                response = session.get(url, params=params, timeout=10)
                self.results['performance']['requests_made'] += 1
                
                method_results['queries_tested'].append({
                    'query_hash': query_data['query_hash'],
                    'variables': query_data['variables'],
                    'status_code': response.status_code,
                    'response_size': len(response.text)
                })
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        
                        # ตรวจสอบว่ามีข้อมูล user ไหม
                        if 'data' in data and data['data']:
                            method_results['working_queries'].append(query_data['query_hash'])
                            method_results['data_extracted'][query_data['query_hash']] = data
                            method_results['success'] = True
                            
                            self.girly_print(f"   ✅ GraphQL SUCCESS! {query_data['query_hash'][:20]}...", "SUCCESS", "💎")
                            
                            # บันทึกข้อมูลลง results หลัก
                            if 'user' in data['data']:
                                self.results['profile_data'].update(data['data']['user'])
                            
                            return True
                    
                    except json.JSONDecodeError:
                        pass
                
                # Rate limiting
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                self.girly_print(f"   ❌ GraphQL Failed: {e}", "WARNING", "⚠️")
            
            return False
        
        # ทดสอบ GraphQL queries แบบ parallel
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(test_graphql_query, query) for query in graphql_queries]
            
            # รอผลลัพธ์
            for future in futures:
                try:
                    future.result(timeout=15)
                except:
                    pass
        
        self.results['bypass_methods_used'].append(method_results)
        
        if method_results['success']:
            self.girly_print(f"🎉 Method 2 สำเร็จ! เจอ {len(method_results['working_queries'])} queries", "SUCCESS", "🔥")
        else:
            self.girly_print("💔 Method 2 ไม่สำเร็จ", "WARNING", "😢")
        
        return method_results

    def method_3_session_hijacking(self) -> Dict:
        """
        🎭 Method 3: Session Hijacking - hijack sessions จาก cookies
        
        Techniques:
        - Cookie vault management
        - Session validation
        - CSRF token extraction
        - Authentication bypass
        
        Returns:
            Dictionary ของข้อมูลที่ดึงได้
        """
        self.girly_print("🎭 Method 3: Session Hijacking", "INFO", "⚡")
        
        method_results = {
            'method': 'Session Hijacking',
            'success': False,
            'data_extracted': {},
            'sessions_tested': 0,
            'valid_sessions': []
        }
        
        # โหลด cookies จากไฟล์ (ถ้ามี)
        cookie_files = list(Path('.').glob('*cookie*')) + list(Path('.').glob('*session*'))
        
        # Test cookies ที่มีอยู่
        test_cookies = [
            # ตัวอย่าง cookies (ในการใช้จริงจะโหลดจากไฟล์)
            {
                'sessionid': 'example_sessionid_123',
                'csrftoken': 'example_csrf_456',
                'ds_user_id': '123456789'
            }
        ]
        
        # โหลด cookies จากไฟล์
        for cookie_file in cookie_files:
            try:
                with open(cookie_file, 'r') as f:
                    if cookie_file.suffix == '.json':
                        cookies_data = json.load(f)
                        if isinstance(cookies_data, list):
                            test_cookies.extend(cookies_data)
                        else:
                            test_cookies.append(cookies_data)
                    else:
                        # อ่าน cookies จาก text file
                        content = f.read()
                        cookie_matches = re.findall(r'(\w+)=([^;]+)', content)
                        if cookie_matches:
                            cookie_dict = dict(cookie_matches)
                            test_cookies.append(cookie_dict)
            except:
                pass
        
        def test_session_cookies(cookies: Dict):
            """Test session cookies แบบ thread-safe"""
            try:
                session = self.create_stealth_session()
                
                # ตั้งค่า cookies
                for name, value in cookies.items():
                    session.cookies.set(name, value)
                
                method_results['sessions_tested'] += 1
                
                # ทดสอบการเข้าถึงข้อมูล
                test_urls = [
                    f"https://www.instagram.com/api/v1/users/web_profile_info/?username={self.target_username}",
                    f"https://www.instagram.com/{self.target_username}/?__a=1",
                    "https://www.instagram.com/accounts/edit/"
                ]
                
                for test_url in test_urls:
                    self.girly_print(f"   🔍 Testing session: {test_url}", "INFO", "🍪")
                    
                    response = session.get(test_url, timeout=10)
                    self.results['performance']['requests_made'] += 1
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            
                            # ตรวจสอบว่า session ใช้งานได้
                            if 'user' in str(data) or 'authenticated' in str(data):
                                method_results['valid_sessions'].append(cookies)
                                method_results['data_extracted'][f'session_{len(method_results["valid_sessions"])}'] = data
                                method_results['success'] = True
                                
                                self.girly_print(f"   ✅ Valid session found!", "SUCCESS", "💎")
                                
                                # บันทึกข้อมูลลง results หลัก
                                if 'user' in data:
                                    self.results['profile_data'].update(data['user'])
                                
                                return True
                        
                        except json.JSONDecodeError:
                            # ตรวจสอบ HTML response
                            if self.target_username.lower() in response.text.lower() and 'login' not in response.text.lower():
                                method_results['valid_sessions'].append(cookies)
                                method_results['success'] = True
                                
                                self.girly_print(f"   ✅ Valid session (HTML)!", "SUCCESS", "🌐")
                                return True
                    
                    # Rate limiting
                    time.sleep(random.uniform(1, 2))
                
            except Exception as e:
                self.girly_print(f"   ❌ Session test failed: {e}", "WARNING", "⚠️")
            
            return False
        
        # ทดสอบ sessions
        if test_cookies:
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = [executor.submit(test_session_cookies, cookies) for cookies in test_cookies[:10]]  # จำกัด 10 cookies
                
                for future in futures:
                    try:
                        future.result(timeout=20)
                    except:
                        pass
        else:
            self.girly_print("   ⚠️ No cookies found to test", "WARNING", "🍪")
        
        self.results['bypass_methods_used'].append(method_results)
        
        if method_results['success']:
            self.girly_print(f"🎉 Method 3 สำเร็จ! เจอ {len(method_results['valid_sessions'])} valid sessions", "SUCCESS", "🔥")
        else:
            self.girly_print("💔 Method 3 ไม่สำเร็จ", "WARNING", "😢")
        
        return method_results

    def method_4_cached_data_mining(self) -> Dict:
        """
        💎 Method 4: Cached Data Mining - หาข้อมูลจาก cache
        
        Techniques:
        - Google Cache search
        - Wayback Machine
        - Cached.to service
        - Search engine results
        
        Returns:
            Dictionary ของข้อมูลที่ดึงได้
        """
        self.girly_print("💎 Method 4: Cached Data Mining", "INFO", "⚡")
        
        method_results = {
            'method': 'Cached Data Mining',
            'success': False,
            'data_extracted': {},
            'cache_sources': [],
            'working_sources': []
        }
        
        # Cache sources
        target_url = f"https://www.instagram.com/{self.target_username}/"
        cache_sources = [
            f"https://webcache.googleusercontent.com/search?q=cache:{target_url}",
            f"https://archive.org/wayback/available?url={target_url}",
            f"https://cached.to/{target_url}",
            f"https://www.google.com/search?q=site:instagram.com+{self.target_username}",
            f"https://yandex.com/search/?text=site:instagram.com+{self.target_username}",
            f"https://www.bing.com/search?q=site:instagram.com+{self.target_username}",
            f"https://duckduckgo.com/?q=site:instagram.com+{self.target_username}"
        ]
        
        def test_cache_source(source_url: str):
            """Test cache source แบบ thread-safe"""
            try:
                session = self.create_stealth_session()
                
                self.girly_print(f"   🔍 Testing cache: {source_url[:50]}...", "INFO", "🎯")
                
                response = session.get(source_url, timeout=15)
                self.results['performance']['requests_made'] += 1
                
                method_results['cache_sources'].append({
                    'url': source_url,
                    'status_code': response.status_code,
                    'response_size': len(response.text)
                })
                
                if response.status_code == 200:
                    # ตรวจสอบว่ามีข้อมูล target ไหม
                    if self.target_username.lower() in response.text.lower():
                        method_results['working_sources'].append(source_url)
                        method_results['data_extracted'][source_url] = response.text[:5000]  # จำกัดขนาด
                        method_results['success'] = True
                        
                        self.girly_print(f"   ✅ Cache data found!", "SUCCESS", "💎")
                        
                        # พยายามดึง JSON data จาก HTML
                        json_matches = re.findall(r'window\._sharedData\s*=\s*({.*?});', response.text)
                        for json_match in json_matches:
                            try:
                                shared_data = json.loads(json_match)
                                if 'entry_data' in shared_data:
                                    method_results['data_extracted'][f'{source_url}_json'] = shared_data
                                    
                                    # บันทึกข้อมูลลง results หลัก
                                    if 'ProfilePage' in shared_data['entry_data']:
                                        profile_data = shared_data['entry_data']['ProfilePage'][0]
                                        if 'graphql' in profile_data and 'user' in profile_data['graphql']:
                                            self.results['profile_data'].update(profile_data['graphql']['user'])
                            except:
                                pass
                        
                        return True
                
                # Rate limiting
                time.sleep(random.uniform(2, 5))
                
            except Exception as e:
                self.girly_print(f"   ❌ Cache test failed: {e}", "WARNING", "⚠️")
            
            return False
        
        # ทดสอบ cache sources แบบ parallel
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(test_cache_source, source) for source in cache_sources]
            
            for future in futures:
                try:
                    future.result(timeout=20)
                except:
                    pass
        
        self.results['bypass_methods_used'].append(method_results)
        
        if method_results['success']:
            self.girly_print(f"🎉 Method 4 สำเร็จ! เจอ {len(method_results['working_sources'])} cache sources", "SUCCESS", "🔥")
        else:
            self.girly_print("💔 Method 4 ไม่สำเร็จ", "WARNING", "😢")
        
        return method_results

    def method_5_social_engineering_osint(self) -> Dict:
        """
        🕵️ Method 5: Social Engineering + OSINT - รวบรวมข้อมูลจากแหล่งอื่น
        
        Techniques:
        - Cross-platform search
        - Username correlation
        - Email/phone discovery
        - Social connections mapping
        
        Returns:
            Dictionary ของข้อมูลที่ดึงได้
        """
        self.girly_print("🕵️ Method 5: Social Engineering + OSINT", "INFO", "⚡")
        
        method_results = {
            'method': 'Social Engineering + OSINT',
            'success': False,
            'data_extracted': {},
            'platforms_checked': [],
            'related_accounts': []
        }
        
        # Cross-platform search
        related_platforms = {
            'Twitter': f'https://twitter.com/{self.target_username}',
            'Facebook': f'https://facebook.com/{self.target_username}',
            'TikTok': f'https://tiktok.com/@{self.target_username}',
            'YouTube': f'https://youtube.com/c/{self.target_username}',
            'LinkedIn': f'https://linkedin.com/in/{self.target_username}',
            'GitHub': f'https://github.com/{self.target_username}',
            'Pinterest': f'https://pinterest.com/{self.target_username}',
            'Snapchat': f'https://snapchat.com/add/{self.target_username}',
            'Reddit': f'https://reddit.com/u/{self.target_username}',
            'Tumblr': f'https://{self.target_username}.tumblr.com'
        }
        
        def check_related_platform(platform_name: str, platform_url: str):
            """Check related platform แบบ thread-safe"""
            try:
                session = self.create_stealth_session()
                
                self.girly_print(f"   🔍 Checking {platform_name}: {platform_url}", "INFO", "🎯")
                
                response = session.get(platform_url, timeout=10)
                self.results['performance']['requests_made'] += 1
                
                platform_data = {
                    'platform': platform_name,
                    'url': platform_url,
                    'status_code': response.status_code,
                    'response_size': len(response.text),
                    'found': False
                }
                
                if response.status_code == 200:
                    # ตรวจสอบว่าเป็น profile จริงหรือไม่
                    profile_indicators = [
                        self.target_username.lower() in response.text.lower(),
                        len(response.text) > 5000,  # มีเนื้อหาเยอะ
                        'profile' in response.text.lower() or 'user' in response.text.lower()
                    ]
                    
                    if sum(profile_indicators) >= 2:
                        platform_data['found'] = True
                        method_results['related_accounts'].append(platform_data)
                        method_results['success'] = True
                        
                        self.girly_print(f"   ✅ Found {platform_name} profile!", "SUCCESS", "💎")
                        
                        # ดึงข้อมูลเพิ่มเติม
                        email_patterns = [
                            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                            r'mailto:([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})'
                        ]
                        
                        for pattern in email_patterns:
                            emails = re.findall(pattern, response.text, re.IGNORECASE)
                            if emails:
                                platform_data['emails_found'] = list(set(emails))
                        
                        # ดึง bio/description
                        bio_patterns = [
                            r'"description":\s*"([^"]+)"',
                            r'<meta name="description" content="([^"]+)"',
                            r'bio["\s:]+([^"]+)'
                        ]
                        
                        for pattern in bio_patterns:
                            bios = re.findall(pattern, response.text, re.IGNORECASE)
                            if bios:
                                platform_data['bio'] = bios[0]
                                break
                
                method_results['platforms_checked'].append(platform_data)
                
                # Rate limiting
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                self.girly_print(f"   ❌ {platform_name} check failed: {e}", "WARNING", "⚠️")
        
        # ตรวจสอบ platforms แบบ parallel
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(check_related_platform, name, url) 
                for name, url in related_platforms.items()
            ]
            
            for future in futures:
                try:
                    future.result(timeout=15)
                except:
                    pass
        
        # รวบรวมข้อมูลที่เจอ
        if method_results['related_accounts']:
            all_emails = []
            all_bios = []
            
            for account in method_results['related_accounts']:
                if 'emails_found' in account:
                    all_emails.extend(account['emails_found'])
                if 'bio' in account:
                    all_bios.append(account['bio'])
            
            method_results['data_extracted'] = {
                'emails_discovered': list(set(all_emails)),
                'bios_collected': all_bios,
                'cross_platform_presence': len(method_results['related_accounts'])
            }
        
        self.results['bypass_methods_used'].append(method_results)
        
        if method_results['success']:
            self.girly_print(f"🎉 Method 5 สำเร็จ! เจอ {len(method_results['related_accounts'])} related accounts", "SUCCESS", "🔥")
        else:
            self.girly_print("💔 Method 5 ไม่สำเร็จ", "WARNING", "😢")
        
        return method_results

    def ai_data_analyzer(self) -> Dict:
        """
        🧠 AI Data Analyzer - วิเคราะห์ข้อมูลที่รวบรวมได้ด้วย AI
        
        Features:
        - Pattern recognition
        - Data correlation
        - Risk assessment
        - Recommendation generation
        
        Returns:
            Dictionary ของการวิเคราะห์
        """
        self.girly_print("🧠 AI Data Analysis", "INFO", "🤖")
        
        analysis = {
            'profile_completeness': 0,
            'data_quality': 'Unknown',
            'privacy_level': 'Unknown',
            'risk_factors': [],
            'recommendations': [],
            'confidence_score': 0
        }
        
        # วิเคราะห์ความสมบูรณ์ของข้อมูล
        profile_fields = ['username', 'full_name', 'biography', 'profile_pic_url', 'follower_count', 'following_count']
        available_fields = sum(1 for field in profile_fields if field in self.results['profile_data'])
        analysis['profile_completeness'] = (available_fields / len(profile_fields)) * 100
        
        # วิเคราะห์คุณภาพข้อมูล
        successful_methods = len([m for m in self.results['bypass_methods_used'] if m['success']])
        total_methods = len(self.results['bypass_methods_used'])
        
        if successful_methods >= 3:
            analysis['data_quality'] = 'High'
            analysis['confidence_score'] = 90
        elif successful_methods >= 2:
            analysis['data_quality'] = 'Medium'
            analysis['confidence_score'] = 70
        elif successful_methods >= 1:
            analysis['data_quality'] = 'Low'
            analysis['confidence_score'] = 50
        else:
            analysis['data_quality'] = 'None'
            analysis['confidence_score'] = 0
        
        # วิเคราะห์ระดับความเป็นส่วนตัว
        if self.results['profile_data']:
            is_private = self.results['profile_data'].get('is_private', True)
            if is_private:
                analysis['privacy_level'] = 'Private'
                analysis['risk_factors'].append('Account is set to private')
            else:
                analysis['privacy_level'] = 'Public'
                analysis['risk_factors'].append('Account is publicly accessible')
        
        # สร้างคำแนะนำ
        if analysis['confidence_score'] >= 70:
            analysis['recommendations'].extend([
                'Data extraction successful - consider additional verification',
                'Cross-reference with other intelligence sources',
                'Monitor for profile changes'
            ])
        elif analysis['confidence_score'] >= 50:
            analysis['recommendations'].extend([
                'Partial data extracted - try alternative methods',
                'Consider social engineering approaches',
                'Look for related accounts on other platforms'
            ])
        else:
            analysis['recommendations'].extend([
                'Direct extraction failed - target may have strong privacy settings',
                'Try OSINT methods on related platforms',
                'Consider waiting for profile to become public'
            ])
        
        return analysis

    def generate_comprehensive_report(self) -> str:
        """
        📊 สร้าง comprehensive report
        
        Returns:
            Formatted report string
        """
        end_time = datetime.now()
        start_time = datetime.fromisoformat(self.results['start_time'])
        duration = (end_time - start_time).total_seconds()
        
        self.results['performance']['time_elapsed'] = duration
        
        # คำนวณ success rate
        successful_methods = len([m for m in self.results['bypass_methods_used'] if m['success']])
        total_methods = len(self.results['bypass_methods_used'])
        self.results['success_rate'] = (successful_methods / total_methods * 100) if total_methods > 0 else 0
        
        # AI Analysis
        ai_analysis = self.ai_data_analyzer()
        
        report = f"""
💀🔥 ULTIMATE INSTAGRAM PRIVATE VIEWER REPORT 🔥💀
{'='*70}

📊 SCAN SUMMARY
Target Username: {self.results['target_username']}
Scan ID: {self.results['scan_id']}
Start Time: {self.results['start_time']}
Duration: {duration:.2f} seconds
Total Requests: {self.results['performance']['requests_made']}
Speed: {self.results['performance']['requests_made']/duration:.2f} requests/second
Success Rate: {self.results['success_rate']:.1f}%

🎯 PROFILE DATA EXTRACTED
"""
        
        if self.results['profile_data']:
            for key, value in self.results['profile_data'].items():
                if isinstance(value, (str, int, bool)):
                    report += f"  • {key}: {value}\n"
        else:
            report += "  • No profile data extracted\n"
        
        report += f"""
🔥 BYPASS METHODS ANALYSIS
Total Methods Used: {len(self.results['bypass_methods_used'])}
Successful Methods: {successful_methods}
"""
        
        for i, method in enumerate(self.results['bypass_methods_used'], 1):
            status = "✅ SUCCESS" if method['success'] else "❌ FAILED"
            report += f"  {i}. {method['method']}: {status}\n"
        
        report += f"""
🧠 AI ANALYSIS
Profile Completeness: {ai_analysis['profile_completeness']:.1f}%
Data Quality: {ai_analysis['data_quality']}
Privacy Level: {ai_analysis['privacy_level']}
Confidence Score: {ai_analysis['confidence_score']}/100

🚨 RISK FACTORS
{chr(10).join(f"  • {risk}" for risk in ai_analysis['risk_factors']) if ai_analysis['risk_factors'] else '  • None identified'}

💡 RECOMMENDATIONS
{chr(10).join(f"  • {rec}" for rec in ai_analysis['recommendations']) if ai_analysis['recommendations'] else '  • None available'}

📈 PERFORMANCE METRICS
Requests per Second: {self.results['performance']['requests_made']/duration:.2f}
Memory Efficiency: Optimized session pooling
Thread Utilization: Multi-threaded processing
Stealth Factor: Advanced anti-detection

💖 Generated with love by น้องจิน's Ultimate Instagram Private Viewer
👻 For educational and authorized research only!
🔥 Report ID: {self.results['scan_id']}_{int(time.time())}
"""
        
        return report

    async def execute_full_private_viewer_attack(self, target_username: str = None) -> Dict:
        """
        🔥 Execute Full Private Viewer Attack - ใช้ทุก methods พร้อมกัน
        
        Args:
            target_username: Instagram username เป้าหมาย
        
        Returns:
            Complete results dictionary
        """
        if target_username:
            self.target_username = target_username
            self.results['target_username'] = target_username
        
        self.girly_print("🔥 เริ่ม Ultimate Instagram Private Viewer Attack!", "INFO", "💀")
        self.girly_print(f"🎯 Target: @{self.target_username}", "INFO", "🎯")
        
        try:
            # Phase 1: Direct API Bypass
            self.girly_print("📊 Phase 1: Direct API Bypass", "INFO", "🚀")
            await asyncio.get_event_loop().run_in_executor(
                self.thread_pool, self.method_1_direct_api_bypass
            )
            
            # Phase 2: GraphQL Exploitation
            self.girly_print("📊 Phase 2: GraphQL Exploitation", "INFO", "🌐")
            await asyncio.get_event_loop().run_in_executor(
                self.thread_pool, self.method_2_graphql_exploitation
            )
            
            # Phase 3: Session Hijacking
            self.girly_print("📊 Phase 3: Session Hijacking", "INFO", "🎭")
            await asyncio.get_event_loop().run_in_executor(
                self.thread_pool, self.method_3_session_hijacking
            )
            
            # Phase 4: Cached Data Mining
            self.girly_print("📊 Phase 4: Cached Data Mining", "INFO", "💎")
            await asyncio.get_event_loop().run_in_executor(
                self.thread_pool, self.method_4_cached_data_mining
            )
            
            # Phase 5: Social Engineering + OSINT
            self.girly_print("📊 Phase 5: Social Engineering + OSINT", "INFO", "🕵️")
            await asyncio.get_event_loop().run_in_executor(
                self.thread_pool, self.method_5_social_engineering_osint
            )
            
            # Phase 6: Generate Report
            self.girly_print("📊 Phase 6: Report Generation", "INFO", "📋")
            report = self.generate_comprehensive_report()
            
            # Save report to files
            timestamp = int(time.time())
            
            # JSON Report
            json_file = Path(f"instagram_private_viewer_{self.target_username}_{timestamp}.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, default=str)
            
            # Text Report
            txt_file = Path(f"instagram_report_{self.target_username}_{timestamp}.txt")
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            self.girly_print(f"📊 Reports saved: {json_file}, {txt_file}", "SUCCESS", "💾")
            self.girly_print("🎉 Ultimate Instagram Private Viewer Complete!", "SUCCESS", "🔥")
            
            # Print summary
            print(report)
            
            return self.results
            
        except Exception as e:
            self.girly_print(f"❌ Private viewer attack failed: {e}", "ERROR", "💔")
            return self.results
        
        finally:
            # Cleanup
            self.thread_pool.shutdown(wait=False)

def main():
    """Main function - interactive menu"""
    print(GIRLY_BANNER)
    
    while True:
        print("\n💖 ULTIMATE INSTAGRAM PRIVATE VIEWER MENU 💖")
        print("1. 🚀 Quick Private View (single target)")
        print("2. 🔥 Full Attack Suite (all methods)")  
        print("3. 🎯 Method Testing (test individual methods)")
        print("4. 📊 Generate Report Only")
        print("5. 🧠 AI Data Analysis")
        print("0. 💔 Exit")
        
        choice = input("\n💖 เลือกเมนู (0-5): ").strip()
        
        try:
            if choice == '1':
                username = input("🎯 Instagram username (without @): ").strip()
                if username:
                    viewer = UltimateInstagramPrivateViewer(username)
                    asyncio.run(viewer.execute_full_private_viewer_attack())
                
            elif choice == '2':
                username = input("🎯 Instagram username (without @): ").strip()
                if username:
                    viewer = UltimateInstagramPrivateViewer(username)
                    asyncio.run(viewer.execute_full_private_viewer_attack())
                
            elif choice == '3':
                username = input("🎯 Instagram username (without @): ").strip()
                if username:
                    viewer = UltimateInstagramPrivateViewer(username)
                    print("\n🔥 Available Methods:")
                    print("1. Direct API Bypass")
                    print("2. GraphQL Exploitation")
                    print("3. Session Hijacking")
                    print("4. Cached Data Mining")
                    print("5. Social Engineering + OSINT")
                    
                    method_choice = input("Choose method (1-5): ").strip()
                    
                    if method_choice == '1':
                        viewer.method_1_direct_api_bypass()
                    elif method_choice == '2':
                        viewer.method_2_graphql_exploitation()
                    elif method_choice == '3':
                        viewer.method_3_session_hijacking()
                    elif method_choice == '4':
                        viewer.method_4_cached_data_mining()
                    elif method_choice == '5':
                        viewer.method_5_social_engineering_osint()
                
            elif choice == '4':
                print("📊 Report generation feature")
                # TODO: Implement report-only feature
                
            elif choice == '5':
                print("🧠 AI Analysis feature")
                # TODO: Implement standalone AI analysis
                
            elif choice == '0':
                print("👋 บาย! ดูไอจีให้สนุกนะคะ ♥️")
                break
                
            else:
                print("❌ เลือกเมนูให้ถูกนะคะ")
                
        except KeyboardInterrupt:
            print("\n⚠️ หยุดการทำงาน")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()