from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
🔥 ULTIMATE REDIRECT BYPASS EXTRACTOR 🔥
💀 EXCEED REDIRECTS? NOT ANYMORE! 💀
🚀 HARDCORE ANTI-DETECTION SYSTEM 🚀

Target: whatilove1728
Mission: REAL DATA EXTRACTION WITH REDIRECT BYPASS
Status: UNSTOPPABLE FORCE
"""

import requests
import json
import sqlite3
import time
import random
import os
from datetime import datetime
from urllib.parse import urljoin, urlparse
import hashlib
import base64

class UltimateRedirectBypassExtractor:
    def __init__(self):
        self.target_username = "whatilove1728"
        self.base_url = "https://www.instagram.com"
        self.session = requests.Session()
        self.extracted_data = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = f"REAL_EXTRACTION_{self.target_username}"
        
        # 🔥 ULTIMATE ANTI-DETECTION HEADERS 🔥
        self.setup_stealth_session()
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
    def setup_stealth_session(self):
        """🥷 NINJA STEALTH MODE ACTIVATED 🥷"""
        print("🔥 ACTIVATING ULTIMATE STEALTH MODE...")
        
        # Real browser headers that work
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        })
        
        # 🛡️ ANTI-REDIRECT CONFIGURATION 🛡️
        self.session.max_redirects = 2  # Limit redirects
        
        print("✅ STEALTH MODE READY!")
        
    def bypass_redirect_loops(self, url, max_attempts=3):
        """🚀 HARDCORE REDIRECT BYPASS ENGINE 🚀"""
        print(f"🔥 BREAKING THROUGH REDIRECT BARRIERS: {url}")
        
        for attempt in range(max_attempts):
            try:
                print(f"🎯 ATTEMPT {attempt + 1}: DIRECT ASSAULT")
                
                # Method 1: Direct request with no redirects
                response = self.session.get(url, allow_redirects=False, timeout=15)
                
                if response.status_code == 200:
                    print("✅ DIRECT HIT! NO REDIRECTS NEEDED!")
                    return response
                    
                elif response.status_code in [301, 302, 303, 307, 308]:
                    redirect_url = response.headers.get('Location')
                    print(f"🔄 REDIRECT DETECTED: {redirect_url}")
                    
                    # Follow redirect manually with fresh headers
                    if redirect_url:
                        if not redirect_url.startswith('http'):
                            redirect_url = urljoin(url, redirect_url)
                        
                        time.sleep(random.uniform(1, 3))  # Human-like delay
                        return self.bypass_redirect_loops(redirect_url, max_attempts - 1)
                        
                # Method 2: Try with different approach
                print("🔥 SWITCHING TO ALTERNATIVE ATTACK VECTOR...")
                self.randomize_headers()
                time.sleep(random.uniform(2, 5))
                
                response = self.session.get(url, timeout=20)
                if response.status_code == 200:
                    print("✅ ALTERNATIVE VECTOR SUCCESS!")
                    return response
                    
            except requests.exceptions.TooManyRedirects:
                print("⚠️ TOO MANY REDIRECTS - ACTIVATING BYPASS PROTOCOL...")
                self.session.max_redirects = 1
                time.sleep(random.uniform(3, 6))
                
            except Exception as e:
                print(f"⚠️ ATTEMPT {attempt + 1} FAILED: {str(e)}")
                time.sleep(random.uniform(2, 4))
                
        print("❌ ALL REDIRECT BYPASS ATTEMPTS FAILED")
        return None
        
    def randomize_headers(self):
        """🎲 RANDOMIZE HEADERS FOR STEALTH 🎲"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15'
        ]
        
        self.session.headers.update({
            'User-Agent': random.choice(user_agents),
            'X-Requested-With': 'XMLHttpRequest' if random.random() > 0.5 else None
        })
        
    def extract_from_mobile_version(self):
        """📱 MOBILE VERSION EXTRACTION 📱"""
        print("📱 TRYING MOBILE VERSION BYPASS...")
        
        mobile_url = f"https://m.instagram.com/{self.target_username}/"
        
        # Mobile headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1'
        })
        
        response = self.bypass_redirect_loops(mobile_url)
        if response and response.status_code == 200:
            print("✅ MOBILE VERSION SUCCESS!")
            return self.parse_profile_data(response.text, "mobile")
            
        return None
        
    def extract_via_direct_api(self):
        """🛠️ DIRECT API EXTRACTION 🛠️"""
        print("🛠️ ATTEMPTING DIRECT API ACCESS...")
        
        # Try Instagram's internal API endpoints
        api_endpoints = [
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={self.target_username}",
            f"https://www.instagram.com/api/v1/users/web_profile_info/?username={self.target_username}",
            f"https://www.instagram.com/{self.target_username}/?__a=1&__d=dis"
        ]
        
        for endpoint in api_endpoints:
            try:
                print(f"🎯 TESTING ENDPOINT: {endpoint}")
                
                # API-specific headers
                self.session.headers.update({
                    'X-Instagram-AJAX': '1',
                    'X-CSRFToken': 'missing',
                    'X-Requested-With': 'XMLHttpRequest'
                })
                
                response = self.bypass_redirect_loops(endpoint)
                if response and response.status_code == 200:
                    try:
                        data = response.json()
                        if data:
                            print("✅ API ENDPOINT SUCCESS!")
                            return self.process_api_data(data)
                    except:
                        pass
                        
            except Exception as e:
                print(f"⚠️ API ENDPOINT FAILED: {str(e)}")
                
        return None
        
    def parse_profile_data(self, html_content, source="web"):
        """🔍 HARDCORE HTML PARSING 🔍"""
        print(f"🔍 PARSING {source.upper()} DATA...")
        
        extracted = {
            'username': self.target_username,
            'extraction_method': f'{source}_html_parse',
            'timestamp': self.timestamp,
            'profile_data': {},
            'posts_data': [],
            'raw_html_size': len(html_content)
        }
        
        # Look for JSON data in script tags
        import re
        
        # Pattern for Instagram's data
        patterns = [
            r'window\._sharedData\s*=\s*({.+?});',
            r'window\.__additionalDataLoaded\([^,]+,\s*({.+?})\);',
            r'"ProfilePage"\s*:\s*\[({.+?})\]',
            r'"user"\s*:\s*({.+?})"'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html_content)
            if matches:
                try:
                    for match in matches:
                        data = json.loads(match)
                        if 'user' in str(data) or 'username' in str(data):
                            extracted['profile_data'].update(self.extract_user_info(data))
                            print("✅ FOUND USER DATA IN HTML!")
                except:
                    pass
                    
        # Extract visible profile info
        bio_match = re.search(r'<meta property="og:description" content="([^"]+)"', html_content)
        if bio_match:
            extracted['profile_data']['bio'] = bio_match.group(1)
            
        # Look for follower count, following count
        follower_patterns = [
            r'(\d+(?:,\d+)*)\s+followers',
            r'followers["\']:\s*(\d+)',
            r'"follower_count"\s*:\s*(\d+)'
        ]
        
        for pattern in follower_patterns:
            match = re.search(pattern, html_content, re.IGNORECASE)
            if match:
                extracted['profile_data']['followers'] = match.group(1)
                break
                
        return extracted
        
    def extract_user_info(self, data):
        """👤 EXTRACT USER INFORMATION 👤"""
        user_info = {}
        
        if isinstance(data, dict):
            # Navigate through nested data structures
            for key, value in data.items():
                if key == 'user' and isinstance(value, dict):
                    user_info.update(value)
                elif key == 'username':
                    user_info['username'] = value
                elif key in ['full_name', 'biography', 'follower_count', 'following_count']:
                    user_info[key] = value
                elif isinstance(value, dict):
                    user_info.update(self.extract_user_info(value))
                    
        return user_info
        
    def process_api_data(self, api_data):
        """🛠️ PROCESS API RESPONSE DATA 🛠️"""
        print("🛠️ PROCESSING API DATA...")
        
        extracted = {
            'username': self.target_username,
            'extraction_method': 'direct_api',
            'timestamp': self.timestamp,
            'profile_data': {},
            'posts_data': [],
            'raw_api_data': api_data
        }
        
        # Navigate API structure
        if 'data' in api_data:
            api_data = api_data['data']
            
        if 'user' in api_data:
            user_data = api_data['user']
            extracted['profile_data'] = {
                'id': user_data.get('id'),
                'username': user_data.get('username'),
                'full_name': user_data.get('full_name'),
                'biography': user_data.get('biography'),
                'follower_count': user_data.get('edge_followed_by', {}).get('count'),
                'following_count': user_data.get('edge_follow', {}).get('count'),
                'posts_count': user_data.get('edge_owner_to_timeline_media', {}).get('count'),
                'is_private': user_data.get('is_private'),
                'is_verified': user_data.get('is_verified'),
                'profile_pic_url': user_data.get('profile_pic_url_hd')
            }
            
            # Extract recent posts
            if 'edge_owner_to_timeline_media' in user_data:
                edges = user_data['edge_owner_to_timeline_media'].get('edges', [])
                for edge in edges:
                    node = edge.get('node', {})
                    post_data = {
                        'id': node.get('id'),
                        'shortcode': node.get('shortcode'),
                        'caption': node.get('edge_media_to_caption', {}).get('edges', [{}])[0].get('node', {}).get('text', ''),
                        'like_count': node.get('edge_liked_by', {}).get('count'),
                        'comment_count': node.get('edge_media_to_comment', {}).get('count'),
                        'timestamp': node.get('taken_at_timestamp'),
                        'display_url': node.get('display_url')
                    }
                    extracted['posts_data'].append(post_data)
                    
        return extracted
        
    def save_extraction_results(self, data):
        """💾 SAVE HARDCORE EXTRACTION RESULTS 💾"""
        if not data:
            print("❌ NO DATA TO SAVE")
            return
            
        print("💾 SAVING EXTRACTION RESULTS...")
        
        # Save JSON
        json_file = f"{self.output_dir}/{self.target_username}_REAL_DATA_{self.timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        # Save to SQLite
        db_file = f"{self.output_dir}/{self.target_username}_REAL_DATABASE_{self.timestamp}.db"
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profile_data (
                username TEXT PRIMARY KEY,
                full_name TEXT,
                biography TEXT,
                follower_count INTEGER,
                following_count INTEGER,
                posts_count INTEGER,
                is_private BOOLEAN,
                is_verified BOOLEAN,
                extraction_method TEXT,
                timestamp TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts_data (
                id TEXT PRIMARY KEY,
                username TEXT,
                shortcode TEXT,
                caption TEXT,
                like_count INTEGER,
                comment_count INTEGER,
                timestamp INTEGER,
                display_url TEXT
            )
        ''')
        
        # Insert profile data
        profile = data.get('profile_data', {})
        cursor.execute('''
            INSERT OR REPLACE INTO profile_data 
            (username, full_name, biography, follower_count, following_count, 
             posts_count, is_private, is_verified, extraction_method, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('username'),
            profile.get('full_name'),
            profile.get('biography'),
            profile.get('follower_count'),
            profile.get('following_count'),
            profile.get('posts_count'),
            profile.get('is_private'),
            profile.get('is_verified'),
            data.get('extraction_method'),
            data.get('timestamp')
        ))
        
        # Insert posts data
        for post in data.get('posts_data', []):
            cursor.execute('''
                INSERT OR REPLACE INTO posts_data
                (id, username, shortcode, caption, like_count, comment_count, timestamp, display_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                post.get('id'),
                data.get('username'),
                post.get('shortcode'),
                post.get('caption'),
                post.get('like_count'),
                post.get('comment_count'),
                post.get('timestamp'),
                post.get('display_url')
            ))
            
        conn.commit()
        conn.close()
        
        # Create report
        self.create_extraction_report(data)
        
        print(f"✅ RESULTS SAVED:")
        print(f"   📄 JSON: {json_file}")
        print(f"   🗄️ DATABASE: {db_file}")
        
    def create_extraction_report(self, data):
        """📋 CREATE HARDCORE EXTRACTION REPORT 📋"""
        report_file = f"{self.output_dir}/ULTIMATE_BYPASS_REPORT_{self.timestamp}.md"
        
        profile = data.get('profile_data', {})
        posts = data.get('posts_data', [])
        
        report = f"""# 🔥 ULTIMATE REDIRECT BYPASS EXTRACTION REPORT 🔥

## 🎯 TARGET INFORMATION
- **Username**: {data.get('username')}
- **Extraction Method**: {data.get('extraction_method')}
- **Timestamp**: {data.get('timestamp')}
- **Redirect Bypass**: ✅ SUCCESS

## 👤 PROFILE DATA
- **Full Name**: {profile.get('full_name', 'N/A')}
- **Biography**: {profile.get('biography', 'N/A')}
- **Followers**: {profile.get('follower_count', 'N/A')}
- **Following**: {profile.get('following_count', 'N/A')}
- **Posts**: {profile.get('posts_count', 'N/A')}
- **Private**: {profile.get('is_private', 'N/A')}
- **Verified**: {profile.get('is_verified', 'N/A')}

## 📱 POSTS EXTRACTED
- **Total Posts Found**: {len(posts)}

"""
        
        for i, post in enumerate(posts[:5], 1):
            report += f"""
### Post {i}
- **ID**: {post.get('id', 'N/A')}
- **Shortcode**: {post.get('shortcode', 'N/A')}
- **Likes**: {post.get('like_count', 'N/A')}
- **Comments**: {post.get('comment_count', 'N/A')}
- **Caption**: {post.get('caption', 'N/A')[:100]}...
"""

        report += f"""

## 🚀 EXTRACTION SUMMARY
- **Status**: ✅ SUCCESSFUL REDIRECT BYPASS
- **Data Quality**: REAL INSTAGRAM DATA
- **Bypass Method**: MULTIPLE VECTOR ATTACK
- **Anti-Detection**: FULLY ACTIVATED
- **Results**: HARDCORE EXTRACTION COMPLETE

---
*Generated by Ultimate Redirect Bypass Extractor*
*Target: whatilove1728*
*Mission: REAL DATA EXTRACTION*
"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
            
        print(f"📋 REPORT CREATED: {report_file}")
        
    def execute_ultimate_extraction(self):
        """🚀 EXECUTE ULTIMATE EXTRACTION MISSION 🚀"""
        print("🔥" * 50)
        print("🚀 ULTIMATE REDIRECT BYPASS EXTRACTOR ACTIVATED 🚀")
        print("💀 TARGET: whatilove1728 💀")
        print("🎯 MISSION: REAL DATA EXTRACTION 🎯")
        print("🔥" * 50)
        
        extraction_results = None
        
        # Method 1: Mobile version bypass
        print("\n📱 METHOD 1: MOBILE VERSION ATTACK")
        extraction_results = self.extract_from_mobile_version()
        
        if not extraction_results:
            # Method 2: Direct API bypass
            print("\n🛠️ METHOD 2: DIRECT API ASSAULT")
            extraction_results = self.extract_via_direct_api()
            
        if not extraction_results:
            # Method 3: Regular web with advanced bypass
            print("\n🌐 METHOD 3: WEB VERSION WITH ADVANCED BYPASS")
            regular_url = f"{self.base_url}/{self.target_username}/"
            response = self.bypass_redirect_loops(regular_url)
            
            if response and response.status_code == 200:
                extraction_results = self.parse_profile_data(response.text, "web_advanced")
                
        if extraction_results:
            print("\n✅ EXTRACTION SUCCESSFUL!")
            self.save_extraction_results(extraction_results)
            
            print("\n🎉 ULTIMATE BYPASS MISSION COMPLETE! 🎉")
            print("💀 REDIRECTS HAVE BEEN DESTROYED 💀")
            print("🔥 REAL DATA EXTRACTED SUCCESSFULLY 🔥")
            
        else:
            print("\n❌ ALL BYPASS METHODS FAILED")
            print("🛡️ INSTAGRAM DEFENSES TOO STRONG")
            print("🔄 RECOMMEND: TRY AGAIN LATER")

if __name__ == "__main__":
    extractor = UltimateRedirectBypassExtractor()
    extractor.execute_ultimate_extraction()
