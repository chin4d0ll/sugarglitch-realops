from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
💀 ULTIMATE BYPASS EXTRACTOR V2.0 💀
ระบบสกัดข้อมูลขั้นสุดยอดที่ bypass ทุกอย่าง!
ไม่เล่นๆ ขอของจริง!! 🔥🔥🔥
"""

import requests
import json
import time
import random
from datetime import datetime
import re
import sqlite3
import os
from urllib.parse import quote
import base64

class UltimateBypassExtractorV2:
    def __init__(self):
        self.session = requests.Session()
        self.target_username = "whatilove1728"
        self.target_url = "https://www.instagram.com/whatilove1728"
        self.results = {}
        
        print("💀 ULTIMATE BYPASS EXTRACTOR V2.0 INITIALIZED")
        print("🎯 TARGET: whatilove1728")
        print("🔥 MISSION: REAL DATA EXTRACTION")
        print("💥 STATUS: READY TO BYPASS EVERYTHING!")
        
    def setup_session(self):
        """ตั้งค่า session แบบขั้นสูง"""
        # Headers แบบ real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        self.session.headers.update(headers)
        
    def bypass_method_1_slow_crawl(self):
        """วิธีที่ 1: Slow crawl แบบ human"""
        print("\n🔄 BYPASS METHOD 1: SLOW HUMAN CRAWL")
        
        try:
            self.setup_session()
            
            # Step 1: เข้าหน้าแรก
            print("   🌐 Step 1: Loading Instagram home...")
            response1 = self.session.get('https://www.instagram.com/', timeout=30)
            print(f"   📊 Home Status: {response1.status_code}")
            
            # Human delay
            delay = random.uniform(3, 8)
            print(f"   ⏳ Human delay: {delay:.1f}s")
            time.sleep(delay)
            
            # Step 2: เข้าหน้า explore
            print("   🔍 Step 2: Loading explore...")
            response2 = self.session.get('https://www.instagram.com/explore/', timeout=30)
            print(f"   📊 Explore Status: {response2.status_code}")
            
            # Human delay
            delay = random.uniform(2, 5)
            print(f"   ⏳ Human delay: {delay:.1f}s")
            time.sleep(delay)
            
            # Step 3: ค้นหา username
            print("   🔍 Step 3: Searching for user...")
            search_url = f'https://www.instagram.com/web/search/topsearch/?query={self.target_username}'
            response3 = self.session.get(search_url, timeout=30)
            print(f"   📊 Search Status: {response3.status_code}")
            
            if response3.status_code == 200:
                try:
                    search_data = response3.json()
                    if 'users' in search_data:
                        for user in search_data['users']:
                            if user['user']['username'] == self.target_username:
                                data = self.extract_user_info(user['user'])
                                if data:
                                    self.results['slow_crawl'] = data
                                    print("   ✅ Found user data in search!")
                                    return True
                except:
                    pass
            
            # Human delay
            delay = random.uniform(2, 5)
            print(f"   ⏳ Human delay: {delay:.1f}s")
            time.sleep(delay)
            
            # Step 4: เข้าหน้า profile โดยตรง
            print("   👤 Step 4: Loading profile page...")
            profile_response = self.session.get(self.target_url, timeout=30)
            print(f"   📊 Profile Status: {profile_response.status_code}")
            
            if profile_response.status_code == 200:
                data = self.extract_from_html(profile_response.text)
                if data:
                    self.results['slow_crawl'] = data
                    print("   ✅ Extracted data from profile!")
                    return True
            
        except Exception as e:
            print(f"   ❌ Slow crawl error: {e}")
        
        return False
    
    def bypass_method_2_embed_trick(self):
        """วิธีที่ 2: Instagram embed trick"""
        print("\n🔄 BYPASS METHOD 2: EMBED TRICK")
        
        try:
            # ลอง embed URL
            embed_url = f"https://www.instagram.com/p/embed/?url=https://www.instagram.com/{self.target_username}/"
            
            print(f"   🔗 Embed URL: {embed_url}")
            response = self.session.get(embed_url, timeout=30)
            print(f"   📊 Embed Status: {response.status_code}")
            
            if response.status_code == 200:
                data = self.extract_from_html(response.text)
                if data:
                    self.results['embed_trick'] = data
                    print("   ✅ Extracted data from embed!")
                    return True
            
        except Exception as e:
            print(f"   ❌ Embed trick error: {e}")
        
        return False
    
    def bypass_method_3_external_tools(self):
        """วิธีที่ 3: External tools simulation"""
        print("\n🔄 BYPASS METHOD 3: EXTERNAL TOOLS SIMULATION")
        
        try:
            # แกล้งเป็น external tool
            external_headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; Instagram-Analysis-Tool/1.0; +http://example.com/bot)',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            # ลอง API endpoints ต่างๆ
            endpoints = [
                f'https://www.instagram.com/{self.target_username}/?__a=1&__d=dis',
                f'https://instagram.com/{self.target_username}/channel/?__a=1',
                f'https://www.instagram.com/api/v1/users/{self.target_username}/info/',
            ]
            
            for endpoint in endpoints:
                print(f"   🔗 Testing: {endpoint}")
                
                # ใช้ session ใหม่
                temp_session = requests.Session()
                temp_session.headers.update(external_headers)
                
                try:
                    response = temp_session.get(endpoint, timeout=30)
                    print(f"   📊 Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            processed_data = self.process_api_response(data)
                            if processed_data:
                                self.results['external_tools'] = processed_data
                                print("   ✅ Success with external tool simulation!")
                                return True
                        except:
                            # ลองวิเคราะห์ HTML
                            data = self.extract_from_html(response.text)
                            if data:
                                self.results['external_tools'] = data
                                print("   ✅ Success with HTML analysis!")
                                return True
                
                except Exception as e:
                    print(f"   ⚠️ Endpoint error: {e}")
                    continue
                
                time.sleep(1)
            
        except Exception as e:
            print(f"   ❌ External tools error: {e}")
        
        return False
    
    def bypass_method_4_direct_scraping(self):
        """วิธีที่ 4: Direct scraping with rotation"""
        print("\n🔄 BYPASS METHOD 4: DIRECT SCRAPING")
        
        try:
            # สร้าง user agents หลายตัว
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
                'Mozilla/5.0 (Android 12; Mobile; rv:102.0) Gecko/102.0 Firefox/102.0'
            ]
            
            for i, ua in enumerate(user_agents, 1):
                print(f"   🎭 User Agent {i}: {ua[:50]}...")
                
                # สร้าง session ใหม่
                temp_session = requests.Session()
                temp_session.headers.update({
                    'User-Agent': ua,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive'
                })
                
                try:
                    response = temp_session.get(self.target_url, timeout=30)
                    print(f"   📊 Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        data = self.extract_from_html(response.text)
                        if data:
                            self.results['direct_scraping'] = data
                            print(f"   ✅ Success with User Agent {i}!")
                            return True
                    
                    # Delay between attempts
                    time.sleep(random.uniform(1, 3))
                    
                except Exception as e:
                    print(f"   ⚠️ User Agent {i} error: {e}")
                    continue
            
        except Exception as e:
            print(f"   ❌ Direct scraping error: {e}")
        
        return False
    
    def bypass_method_5_cached_data(self):
        """วิธีที่ 5: ใช้ cached data และ archived data"""
        print("\n🔄 BYPASS METHOD 5: CACHED & ARCHIVED DATA")
        
        try:
            # ลอง Google Cache
            print("   🔍 Checking Google Cache...")
            cache_url = f"https://webcache.googleusercontent.com/search?q=cache:instagram.com/{self.target_username}"
            
            try:
                response = self.session.get(cache_url, timeout=30)
                print(f"   📊 Cache Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = self.extract_from_html(response.text)
                    if data:
                        self.results['cached_data'] = data
                        print("   ✅ Found data in Google Cache!")
                        return True
            except:
                pass
            
            # ลอง Archive.org
            print("   📚 Checking Archive.org...")
            archive_url = f"https://web.archive.org/web/*/instagram.com/{self.target_username}"
            
            try:
                response = self.session.get(archive_url, timeout=30)
                print(f"   📊 Archive Status: {response.status_code}")
                
                if response.status_code == 200 and "instagram.com" in response.text:
                    # หา snapshots ล่าสุด
                    snapshot_matches = re.findall(r'href="(/web/\d+/[^"]*instagram\.com/' + self.target_username + '[^"]*)"', response.text)
                    if snapshot_matches:
                        latest_snapshot = snapshot_matches[0]
                        snapshot_url = f"https://web.archive.org{latest_snapshot}"
                        
                        print(f"   📸 Found snapshot: {snapshot_url}")
                        
                        snapshot_response = self.session.get(snapshot_url, timeout=30)
                        if snapshot_response.status_code == 200:
                            data = self.extract_from_html(snapshot_response.text)
                            if data:
                                self.results['cached_data'] = data
                                print("   ✅ Found data in Archive.org!")
                                return True
            except:
                pass
            
        except Exception as e:
            print(f"   ❌ Cached data error: {e}")
        
        return False
    
    def extract_from_html(self, html):
        """สกัดข้อมูลจาก HTML"""
        try:
            data = {
                'username': self.target_username,
                'extraction_method': 'html_analysis',
                'timestamp': datetime.now().isoformat()
            }
            
            # หา JSON data
            json_patterns = [
                r'window\._sharedData\s*=\s*({.*?});',
                r'"ProfilePage":\[({.*?})\]',
                r'"User":({.*?"username":"' + self.target_username + '".*?})',
                r'"' + self.target_username + '".*?"full_name":"([^"]*)"',
            ]
            
            for pattern in json_patterns:
                matches = re.findall(pattern, html, re.DOTALL)
                if matches:
                    try:
                        if 'full_name' in pattern:
                            data['full_name'] = matches[0]
                            print(f"   ✅ Found full_name: {matches[0]}")
                        else:
                            json_data = json.loads(matches[0])
                            extracted = self.extract_from_json_data(json_data)
                            data.update(extracted)
                            print(f"   ✅ Found JSON data!")
                    except:
                        continue
            
            # หา stats โดยตรง
            stats_patterns = [
                (r'"edge_followed_by":{"count":(\d+)}', 'followers'),
                (r'"edge_follow":{"count":(\d+)}', 'following'),
                (r'"edge_owner_to_timeline_media":{"count":(\d+)}', 'posts'),
                (r'(\d+)\s*followers?', 'followers'),
                (r'(\d+)\s*following', 'following'),
                (r'(\d+)\s*posts?', 'posts'),
            ]
            
            for pattern, key in stats_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                if matches and key not in data:
                    try:
                        data[key] = int(matches[0])
                        print(f"   ✅ Found {key}: {matches[0]}")
                    except:
                        continue
            
            # หา bio
            bio_patterns = [
                r'"biography":"([^"]*)"',
                r'<meta name="description" content="([^"]*)"',
            ]
            
            for pattern in bio_patterns:
                matches = re.findall(pattern, html)
                if matches and 'bio' not in data:
                    bio = matches[0].strip()
                    if len(bio) > 5:
                        data['bio'] = bio
                        print(f"   ✅ Found bio: {bio[:50]}...")
                        break
            
            # หา additional info
            if '"is_private":true' in html:
                data['is_private'] = True
            elif '"is_private":false' in html:
                data['is_private'] = False
            
            if '"is_verified":true' in html:
                data['is_verified'] = True
            elif '"is_verified":false' in html:
                data['is_verified'] = False
            
            # ถ้าได้ข้อมูลอะไรบ้าง ให้ return
            if len(data) > 3:  # มากกว่า username, method, timestamp
                return data
            
        except Exception as e:
            print(f"   ⚠️ HTML extraction error: {e}")
        
        return None
    
    def extract_from_json_data(self, json_data):
        """สกัดข้อมูลจาก JSON"""
        data = {}
        
        try:
            # ลองหา user data ใน structure ต่างๆ
            user_data = None
            
            if isinstance(json_data, dict):
                # Check various structures
                if 'graphql' in json_data and 'user' in json_data['graphql']:
                    user_data = json_data['graphql']['user']
                elif 'entry_data' in json_data and 'ProfilePage' in json_data['entry_data']:
                    if json_data['entry_data']['ProfilePage']:
                        user_data = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
                elif 'user' in json_data:
                    user_data = json_data['user']
                elif 'username' in json_data:
                    user_data = json_data
            
            if user_data:
                data.update(self.extract_user_info(user_data))
            
        except Exception as e:
            print(f"   ⚠️ JSON extraction error: {e}")
        
        return data
    
    def extract_user_info(self, user_data):
        """สกัดข้อมูล user"""
        data = {}
        
        try:
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
            
            # Additional
            if 'is_private' in user_data:
                data['is_private'] = user_data['is_private']
            if 'is_verified' in user_data:
                data['is_verified'] = user_data['is_verified']
            if 'profile_pic_url' in user_data:
                data['profile_pic_url'] = user_data['profile_pic_url']
            
        except Exception as e:
            print(f"   ⚠️ User info extraction error: {e}")
        
        return data
    
    def process_api_response(self, api_data):
        """ประมวลผล API response"""
        try:
            if isinstance(api_data, dict):
                return self.extract_from_json_data(api_data)
        except Exception as e:
            print(f"   ⚠️ API processing error: {e}")
        return None
    
    def save_results(self):
        """บันทึกผลลัพธ์"""
        if not self.results:
            print("❌ No results to save!")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # สร้างโฟลเดอร์
        output_dir = f"ULTIMATE_BYPASS_RESULTS_{self.target_username}"
        os.makedirs(output_dir, exist_ok=True)
        
        # บันทึก JSON
        json_file = f"{output_dir}/BYPASS_DATA_{self.target_username}_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # บันทึก SQLite
        db_file = f"{output_dir}/BYPASS_DATABASE_{self.target_username}_{timestamp}.db"
        self.save_to_database(db_file)
        
        # สร้างรายงาน
        report_file = f"{output_dir}/BYPASS_REPORT_{self.target_username}_{timestamp}.md"
        self.create_report(report_file)
        
        print(f"\n💾 BYPASS RESULTS SAVED:")
        print(f"   📄 JSON: {json_file}")
        print(f"   🗄️ Database: {db_file}")
        print(f"   📊 Report: {report_file}")
    
    def save_to_database(self, db_file):
        """บันทึกลง SQLite"""
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bypass_extractions (
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
            
            for method, data in self.results.items():
                cursor.execute('''
                    INSERT INTO bypass_extractions (
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
        """สร้างรายงาน"""
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(f"# 💀 ULTIMATE BYPASS EXTRACTION REPORT\n\n")
                f.write(f"**Target:** {self.target_username}\n")
                f.write(f"**URL:** {self.target_url}\n")
                f.write(f"**Timestamp:** {datetime.now().isoformat()}\n")
                f.write(f"**Bypass Methods Used:** {len(self.results)}\n\n")
                
                f.write("## 🔥 BYPASS RESULTS\n\n")
                
                for method, data in self.results.items():
                    f.write(f"### {method.upper().replace('_', ' ')}\n\n")
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
                
                f.write("## 💀 BYPASS STATUS\n\n")
                f.write("✅ **ULTIMATE BYPASS SUCCESSFUL!**\n")
                f.write("🔥 **REAL DATA EXTRACTED!**\n")
                f.write("💀 **NO GAMES - HARDCORE RESULTS!**\n\n")
                
        except Exception as e:
            print(f"   ⚠️ Report creation error: {e}")
    
    def run_ultimate_bypass(self):
        """รันการ bypass ขั้นสุดยอด"""
        print("💀 STARTING ULTIMATE BYPASS EXTRACTION")
        print("=" * 60)
        print(f"🎯 TARGET: {self.target_username}")
        print(f"🔗 URL: {self.target_url}")
        print("🔥 MISSION: BYPASS EVERYTHING!")
        print("=" * 60)
        
        methods = [
            self.bypass_method_1_slow_crawl,
            self.bypass_method_2_embed_trick,
            self.bypass_method_3_external_tools,
            self.bypass_method_4_direct_scraping,
            self.bypass_method_5_cached_data
        ]
        
        success_count = 0
        
        for i, method in enumerate(methods, 1):
            print(f"\n{'='*60}")
            print(f"ULTIMATE BYPASS METHOD {i}/{len(methods)}")
            print(f"{'='*60}")
            
            try:
                if method():
                    success_count += 1
                    print(f"✅ BYPASS METHOD {i} SUCCESS!")
                else:
                    print(f"❌ BYPASS METHOD {i} FAILED")
            except Exception as e:
                print(f"❌ BYPASS METHOD {i} ERROR: {e}")
            
            # Delay between methods
            if i < len(methods):
                delay = random.uniform(2, 5)
                print(f"⏳ Cool down: {delay:.1f}s")
                time.sleep(delay)
        
        print(f"\n{'='*60}")
        print("💀 ULTIMATE BYPASS EXTRACTION COMPLETE")
        print(f"{'='*60}")
        print(f"✅ Successful bypasses: {success_count}/{len(methods)}")
        print(f"📊 Data sources: {len(self.results)}")
        
        if self.results:
            print("🔥 REAL DATA EXTRACTED! 💀")
            self.save_results()
            
            # แสดงข้อมูลที่ได้
            print(f"\n🎉 ULTIMATE BYPASS RESULTS:")
            for method, data in self.results.items():
                print(f"   💀 {method.upper()}:")
                print(f"      Username: {data.get('username', 'N/A')}")
                print(f"      Full Name: {data.get('full_name', 'N/A')}")
                print(f"      Followers: {data.get('followers', 'N/A')}")
                print(f"      Following: {data.get('following', 'N/A')}")
                print(f"      Posts: {data.get('posts', 'N/A')}")
                print(f"      Bio: {data.get('bio', 'N/A')[:50]}..." if data.get('bio') else "      Bio: N/A")
        else:
            print("❌ NO DATA EXTRACTED")
            print("🔧 All bypass methods blocked - Instagram security is strong!")

@safe_execution
def main():
    print("💀 ULTIMATE BYPASS EXTRACTOR V2.0")
    print("🔥 REAL DATA EXTRACTION - NO GAMES!")
    print("=" * 60)
    
    extractor = UltimateBypassExtractorV2()
    extractor.run_ultimate_bypass()

if __name__ == "__main__":
    main()
