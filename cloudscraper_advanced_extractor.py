#!/usr/bin/env python3
"""
☁️ CLOUDSCRAPER ADVANCED BYPASS EXTRACTOR ☁️
หลบ Cloudflare + Advanced anti-bot protection
"""

import cloudscraper
import json
import time
import random
import re
from datetime import datetime
import os
from fake_useragent import UserAgent

class CloudScraperAdvancedExtractor:
    def __init__(self):
        # สร้าง CloudScraper instance ที่หลบ Cloudflare ได้
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'ios',
                'mobile': True,
            },
            delay=10,
            debug=False
        )
        
        # Advanced headers rotation
        self.ua = UserAgent()
        
        # Advanced session management
        self.setup_advanced_session()
        
        # Target accounts
        self.targets = ['alx.trading', 'whatilove1728']
        
        # Results storage
        self.results = {
            'extraction_timestamp': datetime.now().isoformat(),
            'method': 'CloudScraper Advanced Bypass',
            'accounts': {}
        }
    
    def setup_advanced_session(self):
        """ตั้งค่า session ขั้นสูงเพื่อหลบ detection"""
        print("☁️ Setting up advanced CloudScraper session...")
        
        # Load existing session
        self.load_session_cookies()
        
        # Advanced headers pool
        self.headers_pool = [
            {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"iOS"',
            },
            {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'X-Requested-With': 'XMLHttpRequest',
                'X-IG-App-ID': '936619743392459',
                'X-Instagram-AJAX': '1',
                'X-CSRFToken': 'missing',  # Will be updated
                'Referer': 'https://www.instagram.com/',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
            }
        ]
        
        # Set initial headers
        self.scraper.headers.update(random.choice(self.headers_pool))
        
        print("✅ Advanced session configured")
    
    def load_session_cookies(self):
        """โหลด cookies จาก session file"""
        print("🍪 Loading session cookies...")
        
        session_file = "/workspaces/sugarglitch-realops/sessions/alx_trading_sessionid_1748519715.json"
        
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            if 'sessionid' in session_data:
                # Add cookies to scraper
                self.scraper.cookies.update({
                    'sessionid': session_data['sessionid'],
                    'mid': 'Y-kNmQALAAFl6YK9ZTaRyOVt5_1q',  # Machine ID
                    'ig_did': 'A1B2C3D4-E5F6-7890-ABCD-EF1234567890',  # Device ID
                    'rur': '"ASH\\05469\\0541748264421\\054b\\0541b:01f7:7c:4e::"',  # Region
                })
                print("✅ Session cookies loaded")
                return True
        
        except Exception as e:
            print(f"❌ Cookie loading error: {e}")
        
        return False
    
    def get_csrf_token(self):
        """ดึง CSRF token แบบขั้นสูง"""
        print("🔑 Getting CSRF token with CloudScraper...")
        
        try:
            # Rotate headers
            self.scraper.headers.update(random.choice(self.headers_pool))
            
            response = self.scraper.get('https://www.instagram.com/', timeout=30)
            
            if response.status_code == 200:
                # หา CSRF token ใน response
                csrf_patterns = [
                    r'"csrf_token":"([^"]+)"',
                    r'csrf_token":\s*"([^"]+)"',
                    r'window\._sharedData\s*=\s*.*?"csrf_token":"([^"]+)"'
                ]
                
                for pattern in csrf_patterns:
                    match = re.search(pattern, response.text)
                    if match:
                        csrf_token = match.group(1)
                        print(f"✅ CSRF token found: {csrf_token[:20]}...")
                        
                        # Update headers with CSRF token
                        self.scraper.headers['X-CSRFToken'] = csrf_token
                        return csrf_token
                
                print("❌ CSRF token not found in response")
            else:
                print(f"❌ Failed to get homepage: {response.status_code}")
        
        except Exception as e:
            print(f"❌ CSRF token error: {e}")
        
        return None
    
    def extract_profile_advanced(self, username):
        """ดึงข้อมูล profile ด้วย CloudScraper"""
        print(f"🎯 Extracting profile with CloudScraper: {username}")
        
        # API endpoints to try
        endpoints = [
            f'https://www.instagram.com/api/v1/users/web_profile_info/?username={username}',
            f'https://www.instagram.com/{username}/?__a=1&__d=dis',
            f'https://www.instagram.com/web/search/topsearch/?context=blended&query={username}',
        ]
        
        for i, endpoint in enumerate(endpoints):
            try:
                print(f"📡 Trying endpoint {i+1}: {endpoint[:50]}...")
                
                # Rotate headers for each request
                self.scraper.headers.update(random.choice(self.headers_pool))
                
                # Add random delay
                time.sleep(random.uniform(3, 8))
                
                response = self.scraper.get(endpoint, timeout=30)
                
                print(f"📊 Response: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        
                        # Parse different response formats
                        if 'data' in data and 'user' in data['data']:
                            # Standard API response
                            user_data = data['data']['user']
                            
                        elif 'graphql' in data:
                            # GraphQL response
                            user_data = data['graphql']['user']
                            
                        elif 'users' in data and len(data['users']) > 0:
                            # Search response
                            user_data = data['users'][0]['user']
                            
                        else:
                            print("⚠️ Unexpected response format")
                            continue
                        
                        # Extract profile information
                        profile_data = self.parse_user_data(user_data)
                        
                        if profile_data:
                            print(f"✅ Profile extracted via endpoint {i+1}")
                            return profile_data
                        
                    except json.JSONDecodeError:
                        print("❌ Invalid JSON response")
                        
                elif response.status_code == 302:
                    print("🔄 Redirected - trying next endpoint")
                    
                elif response.status_code == 401:
                    print("🔐 Unauthorized - session may be expired")
                    
                elif response.status_code == 429:
                    print("⏰ Rate limited - waiting longer...")
                    time.sleep(random.uniform(30, 60))
                    
                else:
                    print(f"❌ HTTP {response.status_code}")
            
            except Exception as e:
                print(f"❌ Endpoint {i+1} error: {e}")
        
        print(f"❌ All endpoints failed for {username}")
        return None
    
    def parse_user_data(self, user_data):
        """แปลง raw user data เป็น structured format"""
        try:
            profile_data = {
                'username': user_data.get('username', ''),
                'full_name': user_data.get('full_name', ''),
                'biography': user_data.get('biography', ''),
                'external_url': user_data.get('external_url', ''),
                'is_private': user_data.get('is_private', False),
                'is_verified': user_data.get('is_verified', False),
                'profile_pic_url': user_data.get('profile_pic_url', ''),
                'profile_pic_url_hd': user_data.get('profile_pic_url_hd', ''),
            }
            
            # Handle follower count (different field names possible)
            followers_field = user_data.get('edge_followed_by', user_data.get('follower_count', {}))
            if isinstance(followers_field, dict):
                profile_data['followers'] = followers_field.get('count', 0)
            else:
                profile_data['followers'] = followers_field or 0
            
            # Handle following count
            following_field = user_data.get('edge_follow', user_data.get('following_count', {}))
            if isinstance(following_field, dict):
                profile_data['following'] = following_field.get('count', 0)
            else:
                profile_data['following'] = following_field or 0
            
            # Handle media count
            media_field = user_data.get('edge_owner_to_timeline_media', user_data.get('media_count', {}))
            if isinstance(media_field, dict):
                profile_data['media_count'] = media_field.get('count', 0)
            else:
                profile_data['media_count'] = media_field or 0
            
            return profile_data
            
        except Exception as e:
            print(f"❌ Data parsing error: {e}")
            return None
    
    def run_cloudscraper_extraction(self):
        """รันการดึงข้อมูลด้วย CloudScraper"""
        print("☁️ CLOUDSCRAPER ADVANCED BYPASS EXTRACTOR")
        print("=" * 55)
        
        # Get CSRF token first
        csrf_token = self.get_csrf_token()
        
        # Extract data for each target
        for username in self.targets:
            print(f"\n🎯 Processing: {username}")
            
            # Advanced stealth delay
            delay = random.uniform(15, 30)
            print(f"⏰ Advanced stealth delay: {delay:.1f}s")
            time.sleep(delay)
            
            # Extract profile
            profile_data = self.extract_profile_advanced(username)
            
            if profile_data:
                self.results['accounts'][username] = profile_data
                print(f"✅ Successfully extracted: {username}")
                print(f"   👤 Full name: {profile_data.get('full_name', 'N/A')}")
                print(f"   👥 Followers: {profile_data.get('followers', 0):,}")
                print(f"   📷 Posts: {profile_data.get('media_count', 0):,}")
                print(f"   🔒 Private: {profile_data.get('is_private', False)}")
            else:
                print(f"❌ Failed to extract: {username}")
        
        # Save results
        self.save_results()
        
        print("\n🎉 CloudScraper extraction completed!")
        return self.results
    
    def save_results(self):
        """บันทึกผลลัพธ์"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"/workspaces/sugarglitch-realops/results/cloudscraper_results_{timestamp}.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved: {filename}")

if __name__ == "__main__":
    extractor = CloudScraperAdvancedExtractor()
    results = extractor.run_cloudscraper_extraction()
    
    # Print summary
    print("\n📊 EXTRACTION SUMMARY")
    print("=" * 40)
    for username, data in results['accounts'].items():
        if data:
            print(f"👤 {username}:")
            print(f"   📱 Full name: {data.get('full_name', 'N/A')}")
            print(f"   👥 Followers: {data.get('followers', 0):,}")
            print(f"   📷 Posts: {data.get('media_count', 0):,}")
            print(f"   🔒 Private: {data.get('is_private', False)}")
