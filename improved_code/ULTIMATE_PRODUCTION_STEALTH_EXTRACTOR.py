from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
🎯 ULTIMATE PRODUCTION-GRADE STEALTH EXTRACTOR 🎯
ระบบสกัดข้อมูลระดับ Production ด้วย Stealth + Proxy + Anti-Detection
ไม่เล่นๆ ขอของจริง! 💀
"""

import requests
import json
import time
import random
from datetime import datetime
import re
import base64
import hashlib
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import threading
import queue
import os

class UltimateProductionStealthExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.target_username = "whatilove1728"
        self.target_url = "https://www.instagram.com/whatilove1728?igsh=Z2lua3Awcm1ldXJ6"
        self.proxies = self.load_proxy_list()
        self.user_agents = UserAgent()
        self.results = {}
        
        # Production-grade stealth headers
        self.stealth_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }
        
        print("🎯 ULTIMATE PRODUCTION STEALTH EXTRACTOR INITIALIZED")
        print("🔥 TARGET: whatilove1728")
        print("💀 MODE: HARDCORE PRODUCTION")
        print("🚀 READY FOR REAL DATA EXTRACTION!")
        
    def load_proxy_list(self):
        """โหลด proxy list สำหรับ rotation"""
        # Production proxy list (ตัวอย่าง - ใส่ proxy จริงที่นี่)
        proxies = [
            # Free proxy examples (ใน production ใช้ premium proxy)
            {'http': 'http://proxy1.example.com:8080', 'https': 'http://proxy1.example.com:8080'},
            {'http': 'http://proxy2.example.com:8080', 'https': 'http://proxy2.example.com:8080'},
            # สำหรับ demo จะใช้ no proxy
            None  # No proxy
        ]
        return proxies
    
    def get_random_proxy(self):
        """สุ่ม proxy สำหรับ rotation"""
        return random.choice(self.proxies)
    
    def get_stealth_headers(self):
        """สร้าง stealth headers แบบสุ่ม"""
        headers = self.stealth_headers.copy()
        headers['User-Agent'] = self.user_agents.random
        
        # เพิ่ม random headers
        if random.choice([True, False]):
            headers['X-Forwarded-For'] = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        
        return headers
    
    def stealth_delay(self):
        """Delay แบบ human-like"""
        delay = random.uniform(2, 7)
        print(f"   ⏳ Stealth delay: {delay:.1f}s")
        time.sleep(delay)
    
    def method1_requests_stealth(self):
        """วิธีที่ 1: Requests พร้อม Stealth + Proxy"""
        print("\n🔄 METHOD 1: REQUESTS STEALTH + PROXY")
        
        try:
            proxy = self.get_random_proxy()
            headers = self.get_stealth_headers()
            
            print(f"   🌐 Proxy: {proxy}")
            print(f"   🎭 User-Agent: {headers['User-Agent'][:50]}...")
            
            # เข้าหน้าแรก
            response = self.session.get(
                'https://www.instagram.com/',
                headers=headers,
                proxies=proxy,
                timeout=30,
                allow_redirects=True
            )
            
            print(f"   📊 Status: {response.status_code}")
            
            self.stealth_delay()
            
            # เข้าหน้า profile
            profile_response = self.session.get(
                self.target_url,
                headers=headers,
                proxies=proxy,
                timeout=30,
                allow_redirects=True
            )
            
            print(f"   📊 Profile Status: {profile_response.status_code}")
            
            # วิเคราะห์ข้อมูล
            data = self.analyze_html_response(profile_response.text)
            
            if data:
                self.results['method1_requests'] = data
                return True
                
        except Exception as e:
            print(f"   ❌ Method 1 error: {e}")
        
        return False
    
    def method2_selenium_stealth(self):
        """วิธีที่ 2: Selenium Undetected Chrome + Stealth"""
        print("\n🔄 METHOD 2: SELENIUM UNDETECTED + STEALTH")
        
        try:
            # Setup undetected chrome
            options = uc.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Stealth mode
            options.add_argument(f'--user-agent={self.user_agents.random}')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins-discovery')
            options.add_argument('--disable-preconnect')
            
            # หากมี proxy
            proxy = self.get_random_proxy()
            if proxy and proxy.get('http'):
                proxy_server = proxy['http'].replace('http://', '')
                options.add_argument(f'--proxy-server={proxy_server}')
            
            print("   🚀 Starting undetected Chrome...")
            driver = uc.Chrome(options=options)
            
            # Anti-detection script
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("   🌐 Loading Instagram...")
            driver.get('https://www.instagram.com/')
            
            self.stealth_delay()
            
            print("   🎯 Loading target profile...")
            driver.get(self.target_url)
            
            # รอให้โหลด
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            self.stealth_delay()
            
            # สกัดข้อมูล
            data = self.extract_from_selenium(driver)
            
            if data:
                self.results['method2_selenium'] = data
                driver.quit()
                return True
            
            driver.quit()
            
        except Exception as e:
            print(f"   ❌ Method 2 error: {e}")
            try:
                driver.quit()
            except:
                pass
        
        return False
    
    def method3_api_stealth(self):
        """วิธีที่ 3: Instagram API bypass + Stealth"""
        print("\n🔄 METHOD 3: API STEALTH BYPASS")
        
        try:
            proxy = self.get_random_proxy()
            headers = self.get_stealth_headers()
            
            # ลอง API endpoints ต่างๆ
            api_endpoints = [
                f'https://www.instagram.com/{self.target_username}/?__a=1',
                f'https://i.instagram.com/api/v1/users/web_profile_info/?username={self.target_username}',
                f'https://www.instagram.com/api/v1/users/{self.target_username}/info/',
            ]
            
            for endpoint in api_endpoints:
                print(f"   🔗 Testing: {endpoint}")
                
                try:
                    response = self.session.get(
                        endpoint,
                        headers=headers,
                        proxies=proxy,
                        timeout=30
                    )
                    
                    print(f"   📊 Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            if data:
                                processed_data = self.process_api_data(data)
                                if processed_data:
                                    self.results['method3_api'] = processed_data
                                    return True
                        except:
                            # ไม่ใช่ JSON ลองวิเคราะห์ HTML
                            data = self.analyze_html_response(response.text)
                            if data:
                                self.results['method3_api'] = data
                                return True
                    
                    self.stealth_delay()
                    
                except Exception as e:
                    print(f"   ⚠️ Endpoint error: {e}")
                    continue
            
        except Exception as e:
            print(f"   ❌ Method 3 error: {e}")
        
        return False
    
    def method4_mobile_stealth(self):
        """วิธีที่ 4: Mobile Instagram + Stealth"""
        print("\n🔄 METHOD 4: MOBILE STEALTH MODE")
        
        try:
            proxy = self.get_random_proxy()
            
            # Mobile headers
            mobile_headers = {
                'User-Agent': 'Instagram 219.0.0.12.117 Android (29/10; 300dpi; 720x1440; samsung; SM-A205F; a20; exynos7884B; en_US; 336918506)',
                'Accept': '*/*',
                'Accept-Language': 'en-US',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'X-IG-App-ID': '936619743392459',
                'X-IG-Capabilities': '3brTvwE=',
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Bandwidth-Speed-kbps': '2000.000',
                'X-IG-Bandwidth-TotalBytes-B': '5000000',
                'X-IG-Bandwidth-TotalTime-ms': '2500'
            }
            
            print(f"   📱 Mobile Mode: {mobile_headers['User-Agent'][:50]}...")
            
            # ลอง mobile endpoints
            mobile_endpoints = [
                f'https://i.instagram.com/api/v1/users/{self.target_username}/info/',
                f'https://i.instagram.com/{self.target_username}/',
            ]
            
            for endpoint in mobile_endpoints:
                print(f"   🔗 Mobile endpoint: {endpoint}")
                
                try:
                    response = self.session.get(
                        endpoint,
                        headers=mobile_headers,
                        proxies=proxy,
                        timeout=30
                    )
                    
                    print(f"   📊 Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            processed_data = self.process_api_data(data)
                            if processed_data:
                                self.results['method4_mobile'] = processed_data
                                return True
                        except:
                            data = self.analyze_html_response(response.text)
                            if data:
                                self.results['method4_mobile'] = data
                                return True
                    
                    self.stealth_delay()
                    
                except Exception as e:
                    print(f"   ⚠️ Mobile endpoint error: {e}")
                    continue
            
        except Exception as e:
            print(f"   ❌ Method 4 error: {e}")
        
        return False
    
    def analyze_html_response(self, html):
        """วิเคราะห์ HTML เพื่อหาข้อมูล"""
        try:
            data = {}
            
            # หา JSON data ใน HTML
            json_matches = re.findall(r'window\._sharedData\s*=\s*({.*?});', html)
            if json_matches:
                try:
                    shared_data = json.loads(json_matches[0])
                    data['shared_data'] = shared_data
                    print("   ✅ Found shared_data!")
                except:
                    pass
            
            # หา profile data
            profile_matches = re.findall(r'"ProfilePage":\[({.*?})\]', html)
            if profile_matches:
                try:
                    profile_data = json.loads(profile_matches[0])
                    data['profile_data'] = profile_data
                    print("   ✅ Found profile_data!")
                except:
                    pass
            
            # หา additional data
            additional_matches = re.findall(r'"' + self.target_username + '".*?"full_name":"([^"]*)"', html)
            if additional_matches:
                data['full_name'] = additional_matches[0]
                print(f"   ✅ Found full_name: {additional_matches[0]}")
            
            # หา follower count
            follower_matches = re.findall(r'"edge_followed_by":{"count":(\d+)}', html)
            if follower_matches:
                data['followers'] = int(follower_matches[0])
                print(f"   ✅ Found followers: {follower_matches[0]}")
            
            # หา following count
            following_matches = re.findall(r'"edge_follow":{"count":(\d+)}', html)
            if following_matches:
                data['following'] = int(following_matches[0])
                print(f"   ✅ Found following: {following_matches[0]}")
            
            # หา posts count
            posts_matches = re.findall(r'"edge_owner_to_timeline_media":{"count":(\d+)}', html)
            if posts_matches:
                data['posts'] = int(posts_matches[0])
                print(f"   ✅ Found posts: {posts_matches[0]}")
            
            if data:
                data['extraction_method'] = 'html_analysis'
                data['timestamp'] = datetime.now().isoformat()
                return data
            
        except Exception as e:
            print(f"   ⚠️ HTML analysis error: {e}")
        
        return None
    
    def extract_from_selenium(self, driver):
        """สกัดข้อมูลจาก Selenium"""
        try:
            data = {}
            
            # หา username
            try:
                username_element = driver.find_element(By.CSS_SELECTOR, 'h2')
                data['username'] = username_element.text
                print(f"   ✅ Username: {username_element.text}")
            except:
                pass
            
            # หา stats
            try:
                stats = driver.find_elements(By.CSS_SELECTOR, 'a span, div span')
                for stat in stats:
                    text = stat.text
                    if text.isdigit():
                        if 'followers' not in data and int(text) > 0:
                            data['followers'] = int(text)
                            print(f"   ✅ Found stat: {text}")
                        elif 'following' not in data and int(text) > 0:
                            data['following'] = int(text)
                            print(f"   ✅ Found stat: {text}")
                        elif 'posts' not in data and int(text) > 0:
                            data['posts'] = int(text)
                            print(f"   ✅ Found stat: {text}")
            except:
                pass
            
            # หา bio
            try:
                bio_elements = driver.find_elements(By.CSS_SELECTOR, 'div span, p')
                for bio in bio_elements:
                    text = bio.text.strip()
                    if len(text) > 10 and not text.isdigit():
                        data['bio'] = text
                        print(f"   ✅ Bio: {text[:50]}...")
                        break
            except:
                pass
            
            # หา page source สำหรับข้อมูลเพิ่มเติม
            page_source = driver.page_source
            html_data = self.analyze_html_response(page_source)
            
            if html_data:
                data.update(html_data)
            
            if data:
                data['extraction_method'] = 'selenium'
                data['timestamp'] = datetime.now().isoformat()
                return data
            
        except Exception as e:
            print(f"   ⚠️ Selenium extraction error: {e}")
        
        return None
    
    def process_api_data(self, api_data):
        """ประมวลผลข้อมูลจาก API"""
        try:
            data = {}
            
            # ตรวจสอบ structure ต่างๆ ของ Instagram API
            if isinstance(api_data, dict):
                # Structure 1: Direct user data
                if 'user' in api_data:
                    user_data = api_data['user']
                    data.update(self.extract_user_data(user_data))
                
                # Structure 2: GraphQL data
                elif 'data' in api_data and 'user' in api_data['data']:
                    user_data = api_data['data']['user']
                    data.update(self.extract_user_data(user_data))
                
                # Structure 3: Direct data
                else:
                    data.update(self.extract_user_data(api_data))
            
            if data:
                data['extraction_method'] = 'api'
                data['timestamp'] = datetime.now().isoformat()
                return data
            
        except Exception as e:
            print(f"   ⚠️ API data processing error: {e}")
        
        return None
    
    def extract_user_data(self, user_data):
        """สกัดข้อมูลจาก user object"""
        data = {}
        
        try:
            # Basic info
            if 'username' in user_data:
                data['username'] = user_data['username']
            if 'full_name' in user_data:
                data['full_name'] = user_data['full_name']
            if 'biography' in user_data:
                data['bio'] = user_data['biography']
            
            # Stats
            if 'edge_followed_by' in user_data:
                data['followers'] = user_data['edge_followed_by'].get('count', 0)
            elif 'follower_count' in user_data:
                data['followers'] = user_data['follower_count']
            
            if 'edge_follow' in user_data:
                data['following'] = user_data['edge_follow'].get('count', 0)
            elif 'following_count' in user_data:
                data['following'] = user_data['following_count']
            
            if 'edge_owner_to_timeline_media' in user_data:
                data['posts'] = user_data['edge_owner_to_timeline_media'].get('count', 0)
            elif 'media_count' in user_data:
                data['posts'] = user_data['media_count']
            
            # Additional info
            if 'is_private' in user_data:
                data['is_private'] = user_data['is_private']
            if 'is_verified' in user_data:
                data['is_verified'] = user_data['is_verified']
            if 'profile_pic_url' in user_data:
                data['profile_pic_url'] = user_data['profile_pic_url']
            
        except Exception as e:
            print(f"   ⚠️ User data extraction error: {e}")
        
        return data
    
    def save_results(self):
        """บันทึกผลลัพธ์"""
        if not self.results:
            print("❌ No results to save!")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # สร้างโฟลเดอร์
        output_dir = f"PRODUCTION_EXTRACTION_{self.target_username}"
        os.makedirs(output_dir, exist_ok=True)
        
        # บันทึก JSON
        json_file = f"{output_dir}/PRODUCTION_DATA_{self.target_username}_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # บันทึก SQLite
        db_file = f"{output_dir}/PRODUCTION_DATABASE_{self.target_username}_{timestamp}.db"
        self.save_to_database(db_file)
        
        # สร้างรายงาน
        report_file = f"{output_dir}/PRODUCTION_REPORT_{self.target_username}_{timestamp}.md"
        self.create_report(report_file)
        
        print(f"\n💾 PRODUCTION RESULTS SAVED:")
        print(f"   📄 JSON: {json_file}")
        print(f"   🗄️ Database: {db_file}")
        print(f"   📊 Report: {report_file}")
    
    def save_to_database(self, db_file):
        """บันทึกลง SQLite"""
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            # สร้างตาราง
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS extractions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    method TEXT,
                    username TEXT,
                    full_name TEXT,
                    followers INTEGER,
                    following INTEGER,
                    posts INTEGER,
                    bio TEXT,
                    is_private BOOLEAN,
                    is_verified BOOLEAN,
                    profile_pic_url TEXT,
                    extraction_method TEXT,
                    timestamp TEXT,
                    raw_data TEXT
                )
            ''')
            
            # บันทึกข้อมูล
            for method, data in self.results.items():
                cursor.execute('''
                    INSERT INTO extractions (
                        method, username, full_name, followers, following, 
                        posts, bio, is_private, is_verified, profile_pic_url,
                        extraction_method, timestamp, raw_data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    method,
                    data.get('username', ''),
                    data.get('full_name', ''),
                    data.get('followers', 0),
                    data.get('following', 0),
                    data.get('posts', 0),
                    data.get('bio', ''),
                    data.get('is_private', False),
                    data.get('is_verified', False),
                    data.get('profile_pic_url', ''),
                    data.get('extraction_method', ''),
                    data.get('timestamp', ''),
                    json.dumps(data, ensure_ascii=False)
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"   ⚠️ Database save error: {e}")
    
    def create_report(self, report_file):
        """สร้างรายงาน Markdown"""
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(f"# 🎯 PRODUCTION EXTRACTION REPORT\n\n")
                f.write(f"**Target:** {self.target_username}\n")
                f.write(f"**URL:** {self.target_url}\n")
                f.write(f"**Timestamp:** {datetime.now().isoformat()}\n")
                f.write(f"**Methods Used:** {len(self.results)}\n\n")
                
                f.write("## 📊 EXTRACTION RESULTS\n\n")
                
                for method, data in self.results.items():
                    f.write(f"### {method.upper()}\n\n")
                    f.write(f"- **Username:** {data.get('username', 'N/A')}\n")
                    f.write(f"- **Full Name:** {data.get('full_name', 'N/A')}\n")
                    f.write(f"- **Followers:** {data.get('followers', 'N/A')}\n")
                    f.write(f"- **Following:** {data.get('following', 'N/A')}\n")
                    f.write(f"- **Posts:** {data.get('posts', 'N/A')}\n")
                    f.write(f"- **Bio:** {data.get('bio', 'N/A')}\n")
                    f.write(f"- **Private:** {data.get('is_private', 'N/A')}\n")
                    f.write(f"- **Verified:** {data.get('is_verified', 'N/A')}\n")
                    f.write(f"- **Extraction Method:** {data.get('extraction_method', 'N/A')}\n")
                    f.write(f"- **Timestamp:** {data.get('timestamp', 'N/A')}\n\n")
                
                f.write("## 🔥 PRODUCTION STATUS\n\n")
                f.write("✅ **MISSION ACCOMPLISHED!**\n")
                f.write("💀 **REAL DATA EXTRACTED!**\n")
                f.write("🎯 **PRODUCTION-GRADE SUCCESS!**\n\n")
                
        except Exception as e:
            print(f"   ⚠️ Report creation error: {e}")
    
    def run_production_extraction(self):
        """รันการสกัดข้อมูลแบบ Production"""
        print("🚀 STARTING PRODUCTION-GRADE EXTRACTION")
        print("=" * 60)
        print(f"🎯 TARGET: {self.target_username}")
        print(f"🔗 URL: {self.target_url}")
        print("💀 MODE: HARDCORE PRODUCTION - NO GAMES!")
        print("=" * 60)
        
        methods = [
            self.method1_requests_stealth,
            self.method2_selenium_stealth,
            self.method3_api_stealth,
            self.method4_mobile_stealth
        ]
        
        success_count = 0
        
        for i, method in enumerate(methods, 1):
            print(f"\n{'='*60}")
            print(f"PRODUCTION METHOD {i}/{len(methods)}")
            print(f"{'='*60}")
            
            try:
                if method():
                    success_count += 1
                    print(f"✅ METHOD {i} SUCCESS!")
                else:
                    print(f"❌ METHOD {i} FAILED")
            except Exception as e:
                print(f"❌ METHOD {i} ERROR: {e}")
            
            # Delay between methods
            if i < len(methods):
                self.stealth_delay()
        
        print(f"\n{'='*60}")
        print("🎯 PRODUCTION EXTRACTION COMPLETE")
        print(f"{'='*60}")
        print(f"✅ Successful methods: {success_count}/{len(methods)}")
        print(f"📊 Data sources: {len(self.results)}")
        
        if self.results:
            print("💀 REAL DATA EXTRACTED! 🔥")
            self.save_results()
            
            # แสดงข้อมูลที่ได้
            print(f"\n🎉 PRODUCTION RESULTS:")
            for method, data in self.results.items():
                print(f"   📋 {method}:")
                print(f"      Username: {data.get('username', 'N/A')}")
                print(f"      Full Name: {data.get('full_name', 'N/A')}")
                print(f"      Followers: {data.get('followers', 'N/A')}")
                print(f"      Following: {data.get('following', 'N/A')}")
                print(f"      Posts: {data.get('posts', 'N/A')}")
        else:
            print("❌ NO DATA EXTRACTED")
            print("🔧 Consider using premium proxies or different timing")

@safe_execution
def main():
    print("🎯 ULTIMATE PRODUCTION-GRADE STEALTH EXTRACTOR")
    print("💀 REAL DATA EXTRACTION - NO GAMES!")
    print("=" * 60)
    
    extractor = UltimateProductionStealthExtractor()
    extractor.run_production_extraction()

if __name__ == "__main__":
    main()
