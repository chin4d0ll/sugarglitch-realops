#!/usr/bin/env python3
"""
🌍 PUBLIC INSTAGRAM SCRAPER - NO SESSION REQUIRED 🌍
ดึงข้อมูล public profiles โดยไม่ต้อง login
"""

import requests
import json
import re
import time
import random
from datetime import datetime
import os
from fake_useragent import UserAgent

class PublicInstagramScraper:
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        
        # Target accounts
        self.targets = ['alx.trading', 'whatilove1728']
        
        # Results storage
        self.results = {
            'extraction_timestamp': datetime.now().isoformat(),
            'method': 'Public Instagram Scraper (No Session)',
            'accounts': {}
        }
        
        self.setup_session()
    
    def setup_session(self):
        """ตั้งค่า session สำหรับ public scraping"""
        print("🌍 Setting up public scraping session...")
        
        # Headers pool for rotation
        self.headers_pool = [
            {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0',
            },
            {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
            }
        ]
        
        # Set random initial headers
        self.session.headers.update(random.choice(self.headers_pool))
        
        print("✅ Public session ready")
    
    def extract_from_html(self, username):
        """ดึงข้อมูลจาก HTML ของ public profile"""
        print(f"🌐 Scraping HTML for: {username}")
        
        url = f"https://www.instagram.com/{username}/"
        
        try:
            # Rotate headers
            self.session.headers.update(random.choice(self.headers_pool))
            
            # Add random delay
            time.sleep(random.uniform(5, 10))
            
            response = self.session.get(url, timeout=30, allow_redirects=False)
            
            print(f"📊 Response: {response.status_code}")
            
            if response.status_code == 200:
                html = response.text
                
                # Extract data from various sources in HTML
                profile_data = {}
                
                # Method 1: จาก window._sharedData
                shared_data = self.extract_shared_data(html)
                if shared_data:
                    profile_data.update(shared_data)
                
                # Method 2: จาก meta tags
                meta_data = self.extract_meta_data(html)
                if meta_data:
                    profile_data.update(meta_data)
                
                # Method 3: จาก JSON-LD
                jsonld_data = self.extract_jsonld_data(html)
                if jsonld_data:
                    profile_data.update(jsonld_data)
                
                # Method 4: จาก regex patterns
                regex_data = self.extract_regex_data(html)
                if regex_data:
                    profile_data.update(regex_data)
                
                if profile_data:
                    print(f"✅ HTML data extracted for {username}")
                    return profile_data
                else:
                    print(f"❌ No data found in HTML for {username}")
                
            elif response.status_code == 302:
                print("🔄 Redirected - profile may be private or deleted")
                
            elif response.status_code == 404:
                print("❌ Profile not found")
                
            else:
                print(f"❌ HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ HTML extraction error: {e}")
        
        return None
    
    def extract_shared_data(self, html):
        """ดึงข้อมูลจาก window._sharedData"""
        try:
            # Pattern สำหรับ _sharedData
            pattern = r'window\._sharedData\s*=\s*({.*?});'
            match = re.search(pattern, html, re.DOTALL)
            
            if match:
                shared_data = json.loads(match.group(1))
                
                # Navigate to user data
                entry_data = shared_data.get('entry_data', {})
                profile_page = entry_data.get('ProfilePage', [])
                
                if profile_page and len(profile_page) > 0:
                    user_data = profile_page[0].get('graphql', {}).get('user', {})
                    
                    if user_data:
                        return {
                            'username': user_data.get('username', ''),
                            'full_name': user_data.get('full_name', ''),
                            'biography': user_data.get('biography', ''),
                            'external_url': user_data.get('external_url', ''),
                            'followers': user_data.get('edge_followed_by', {}).get('count', 0),
                            'following': user_data.get('edge_follow', {}).get('count', 0),
                            'posts': user_data.get('edge_owner_to_timeline_media', {}).get('count', 0),
                            'is_private': user_data.get('is_private', False),
                            'is_verified': user_data.get('is_verified', False),
                            'profile_pic_url': user_data.get('profile_pic_url_hd', ''),
                            'source': 'shared_data'
                        }
                        
        except Exception as e:
            print(f"⚠️ Shared data extraction error: {e}")
        
        return None
    
    def extract_meta_data(self, html):
        """ดึงข้อมูลจาก meta tags"""
        try:
            profile_data = {}
            
            # Meta patterns
            patterns = {
                'description': r'<meta\s+property="og:description"\s+content="([^"]*)"',
                'title': r'<meta\s+property="og:title"\s+content="([^"]*)"',
                'image': r'<meta\s+property="og:image"\s+content="([^"]*)"',
                'url': r'<meta\s+property="og:url"\s+content="([^"]*)"',
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, html, re.IGNORECASE)
                if match:
                    profile_data[f'meta_{key}'] = match.group(1)
            
            # Parse description for follower count
            desc = profile_data.get('meta_description', '')
            if desc:
                # Pattern: "X Followers, Y Following, Z Posts"
                follower_match = re.search(r'([\d,]+)\s*Followers?', desc, re.IGNORECASE)
                if follower_match:
                    followers_str = follower_match.group(1).replace(',', '')
                    profile_data['followers'] = int(followers_str)
                
                following_match = re.search(r'([\d,]+)\s*Following', desc, re.IGNORECASE)
                if following_match:
                    following_str = following_match.group(1).replace(',', '')
                    profile_data['following'] = int(following_str)
                
                posts_match = re.search(r'([\d,]+)\s*Posts?', desc, re.IGNORECASE)
                if posts_match:
                    posts_str = posts_match.group(1).replace(',', '')
                    profile_data['posts'] = int(posts_str)
            
            if profile_data:
                profile_data['source'] = 'meta_tags'
                return profile_data
                
        except Exception as e:
            print(f"⚠️ Meta data extraction error: {e}")
        
        return None
    
    def extract_jsonld_data(self, html):
        """ดึงข้อมูลจาก JSON-LD structured data"""
        try:
            # Pattern สำหรับ JSON-LD
            pattern = r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>'
            matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
            
            for match in matches:
                try:
                    data = json.loads(match)
                    
                    if isinstance(data, dict) and data.get('@type') == 'Person':
                        return {
                            'full_name': data.get('name', ''),
                            'description': data.get('description', ''),
                            'image': data.get('image', ''),
                            'url': data.get('url', ''),
                            'source': 'json_ld'
                        }
                        
                except json.JSONDecodeError:
                    continue
                    
        except Exception as e:
            print(f"⚠️ JSON-LD extraction error: {e}")
        
        return None
    
    def extract_regex_data(self, html):
        """ดึงข้อมูลด้วย regex patterns"""
        try:
            profile_data = {}
            
            # Regex patterns สำหรับข้อมูลต่าง ๆ
            patterns = {
                'biography': r'"biography":"([^"]*)"',
                'full_name': r'"full_name":"([^"]*)"',
                'username': r'"username":"([^"]*)"',
                'is_private': r'"is_private":(true|false)',
                'is_verified': r'"is_verified":(true|false)',
                'profile_pic_url': r'"profile_pic_url_hd":"([^"]*)"',
                'external_url': r'"external_url":"([^"]*)"',
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, html)
                if match:
                    value = match.group(1)
                    if key in ['is_private', 'is_verified']:
                        profile_data[key] = value == 'true'
                    else:
                        profile_data[key] = value
            
            # Count patterns
            count_patterns = {
                'followers': r'"edge_followed_by":\{"count":(\d+)\}',
                'following': r'"edge_follow":\{"count":(\d+)\}',
                'posts': r'"edge_owner_to_timeline_media":\{"count":(\d+)\}',
            }
            
            for key, pattern in count_patterns.items():
                match = re.search(pattern, html)
                if match:
                    profile_data[key] = int(match.group(1))
            
            if profile_data:
                profile_data['source'] = 'regex_patterns'
                return profile_data
                
        except Exception as e:
            print(f"⚠️ Regex extraction error: {e}")
        
        return None
    
    def run_public_scraping(self):
        """รันการ scraping แบบ public"""
        print("🌍 PUBLIC INSTAGRAM SCRAPER - NO SESSION REQUIRED")
        print("=" * 60)
        
        for username in self.targets:
            print(f"\n🎯 Processing: {username}")
            
            # Human-like delay
            delay = random.uniform(10, 20)
            print(f"⏰ Delay: {delay:.1f}s")
            time.sleep(delay)
            
            # Extract profile data
            profile_data = self.extract_from_html(username)
            
            if profile_data:
                self.results['accounts'][username] = profile_data
                print(f"✅ Successfully extracted: {username}")
                
                # Display results
                print(f"   👤 Full name: {profile_data.get('full_name', 'N/A')}")
                print(f"   👥 Followers: {profile_data.get('followers', 'N/A')}")
                print(f"   📷 Posts: {profile_data.get('posts', 'N/A')}")
                print(f"   🔒 Private: {profile_data.get('is_private', 'N/A')}")
                print(f"   📊 Source: {profile_data.get('source', 'unknown')}")
            else:
                print(f"❌ Failed to extract: {username}")
        
        # Save results
        self.save_results()
        
        print("\n🎉 Public scraping completed!")
        return self.results
    
    def save_results(self):
        """บันทึกผลลัพธ์"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"/workspaces/sugarglitch-realops/results/public_scraper_results_{timestamp}.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved: {filename}")

if __name__ == "__main__":
    scraper = PublicInstagramScraper()
    results = scraper.run_public_scraping()
    
    # Print final summary
    print("\n📊 FINAL EXTRACTION SUMMARY")
    print("=" * 50)
    for username, data in results['accounts'].items():
        if data:
            print(f"🎯 {username}:")
            print(f"   📱 Full name: {data.get('full_name', 'N/A')}")
            print(f"   👥 Followers: {data.get('followers', 'N/A'):,}" if isinstance(data.get('followers'), int) else f"   👥 Followers: {data.get('followers', 'N/A')}")
            print(f"   📷 Posts: {data.get('posts', 'N/A'):,}" if isinstance(data.get('posts'), int) else f"   📷 Posts: {data.get('posts', 'N/A')}")
            print(f"   🔒 Private: {data.get('is_private', 'N/A')}")
            print(f"   ✅ Method: {data.get('source', 'unknown')}")
        else:
            print(f"❌ {username}: No data extracted")
