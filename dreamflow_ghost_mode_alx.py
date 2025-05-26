#!/usr/bin/env python3
"""
🔥 DREAMFLOW GHOST MODE - ULTIMATE ALX.TRADING EXTRACTOR
=======================================================
✨ ANTI-RATE-LIMIT + SESSION INJECTION + INSTAGRAPI FUSION
🎯 Target: alx.trading (Alex Fleming)
💎 Method: Stealth session hijacking + intelligent retry
🚀 Author: SugarGlitch RealOps Team
"""

import requests
import json
import time
import random
import os
from datetime import datetime
from urllib.parse import quote
import hashlib
import base64

# Import instagrapi for advanced extraction
try:
    from instagrapi import Client
    INSTAGRAPI_AVAILABLE = True
    print("✅ Instagrapi loaded - Advanced extraction enabled")
except ImportError:
    INSTAGRAPI_AVAILABLE = False
    print("⚠️ Instagrapi not available - Using fallback methods")

class DreamflowGhostMode:
    def __init__(self):
        self.session = requests.Session()
        self.target = "alx.trading"
        self.base_url = "https://www.instagram.com"
        self.data = {}
        self.proxies = []
        self.current_proxy = 0
        self.sessionid = None
        self.csrf_token = None
        self.user_agent_pool = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        ]
        
        print("🔥 DREAMFLOW GHOST MODE INITIALIZED")
        print("=" * 50)
        print(f"🎯 Target: {self.target}")
        print(f"⚡ Mode: ANTI-RATE-LIMIT + SESSION INJECTION")
        print(f"🚀 Status: READY TO EXECUTE")
        print("=" * 50)

    def load_existing_session(self):
        """Load sessionid from stealth bypass results"""
        session_files = [
            "sessionid_alx.txt",
            "alx.trading_session_success.txt", 
            "stealth_session_alx.txt"
        ]
        
        for file in session_files:
            if os.path.exists(file):
                try:
                    with open(file, 'r') as f:
                        content = f.read().strip()
                        if 'sessionid=' in content:
                            self.sessionid = content.split('sessionid=')[1].split(';')[0]
                        else:
                            self.sessionid = content
                    print(f"✅ Loaded sessionid from {file}: {self.sessionid[:20]}...")
                    return True
                except:
                    continue
        
        print("⚠️ No valid sessionid found - will extract without auth")
        return False

    def setup_session_with_auth(self):
        """Setup session with proper authentication"""
        if self.sessionid:
            # Generate CSRF token
            self.csrf_token = hashlib.md5(f"{self.sessionid}{random.random()}".encode()).hexdigest()
            
            cookies = {
                'sessionid': self.sessionid,
                'csrftoken': self.csrf_token,
                'ds_user_id': str(random.randint(10000000, 99999999)),
                'ig_did': base64.b64encode(os.urandom(16)).decode(),
                'ig_nrcb': '1',
                'mid': base64.b64encode(os.urandom(16)).decode(),
                'rur': '"EAG\\05454839508743\\0541777398632:01f7e1c9c1e8e4d8c5e5f1a3d5e2a8f0e1d8c5e5f1a3d5e2a8f0"'
            }
            
            headers = {
                'User-Agent': random.choice(self.user_agent_pool),
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'X-CSRFToken': self.csrf_token,
                'X-Instagram-AJAX': '1',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            self.session.cookies.update(cookies)
            self.session.headers.update(headers)
            print("✅ Session configured with authentication")
        else:
            # Fallback headers without auth
            self.session.headers.update({
                'User-Agent': random.choice(self.user_agent_pool),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            })
            print("⚠️ Using fallback headers without authentication")

    def smart_delay(self, base_delay=3):
        """Intelligent delay to avoid rate limiting"""
        delay = random.uniform(base_delay, base_delay * 2.5)
        time.sleep(delay)

    def rotate_proxy(self):
        """Rotate proxy if available"""
        if self.proxies:
            self.current_proxy = (self.current_proxy + 1) % len(self.proxies)
            proxy = self.proxies[self.current_proxy]
            self.session.proxies.update(proxy)
            print(f"🔄 Rotated to proxy {self.current_proxy + 1}")

    def safe_request(self, url, method='GET', **kwargs):
        """Make safe request with retry logic"""
        max_retries = 3
        base_delay = 5
        
        for attempt in range(max_retries):
            try:
                # Rotate proxy every 2 requests
                if attempt > 0:
                    self.rotate_proxy()
                
                if method.upper() == 'GET':
                    response = self.session.get(url, timeout=30, **kwargs)
                else:
                    response = self.session.post(url, timeout=30, **kwargs)
                
                if response.status_code == 429:
                    wait_time = base_delay * (2 ** attempt) + random.uniform(5, 15)
                    print(f"⚠️ Rate limited (429) - waiting {wait_time:.1f}s before retry {attempt + 1}")
                    time.sleep(wait_time)
                    continue
                
                if response.status_code in [200, 201]:
                    return response
                
                print(f"⚠️ Status {response.status_code} - attempt {attempt + 1}")
                self.smart_delay(base_delay)
                
            except Exception as e:
                print(f"⚠️ Request error: {e} - attempt {attempt + 1}")
                self.smart_delay(base_delay)
        
        return None

    def extract_basic_profile(self):
        """Extract basic profile information"""
        print("\n🎯 PHASE 1: BASIC PROFILE EXTRACTION")
        print("-" * 40)
        
        # Try multiple endpoints
        endpoints = [
            f"{self.base_url}/{self.target}/",
            f"{self.base_url}/{self.target}/?__a=1",
            f"{self.base_url}/api/v1/users/web_profile_info/?username={self.target}"
        ]
        
        for endpoint in endpoints:
            print(f"🔍 Trying: {endpoint}")
            response = self.safe_request(endpoint)
            
            if response:
                print(f"✅ Success: {response.status_code}")
                
                try:
                    if '?__a=1' in endpoint or 'api/v1' in endpoint:
                        data = response.json()
                        self.data['profile_api'] = data
                    else:
                        self.data['profile_html'] = response.text
                        
                    self.smart_delay()
                    
                except:
                    self.data['profile_raw'] = response.text
            else:
                print(f"❌ Failed: {endpoint}")
            
            self.smart_delay(2)

    def instagrapi_extraction(self):
        """Advanced extraction using instagrapi"""
        if not INSTAGRAPI_AVAILABLE or not self.sessionid:
            print("⚠️ Instagrapi extraction skipped")
            return
        
        print("\n🚀 PHASE 2: ADVANCED INSTAGRAPI EXTRACTION")
        print("-" * 45)
        
        try:
            cl = Client()
            
            # Login with sessionid
            print("🔐 Authenticating with sessionid...")
            if cl.login_by_sessionid(self.sessionid):
                print("✅ Instagrapi authentication successful")
                
                # Get user info
                try:
                    user_info = cl.user_info_by_username(self.target)
                    self.data['instagrapi_user_info'] = user_info.dict()
                    print("✅ User info extracted")
                    time.sleep(2)
                except Exception as e:
                    print(f"⚠️ User info error: {e}")
                
                # Get recent media
                try:
                    medias = cl.user_medias(cl.user_id_from_username(self.target), 20)
                    self.data['instagrapi_medias'] = [m.dict() for m in medias]
                    print(f"✅ Extracted {len(medias)} media items")
                    time.sleep(3)
                except Exception as e:
                    print(f"⚠️ Media extraction error: {e}")
                
                # Get followers (if accessible)
                try:
                    user_id = cl.user_id_from_username(self.target)
                    followers = cl.user_followers(user_id, amount=50)
                    self.data['instagrapi_followers'] = {k: v.dict() for k, v in followers.items()}
                    print(f"✅ Extracted {len(followers)} followers")
                    time.sleep(3)
                except Exception as e:
                    print(f"⚠️ Followers extraction error: {e}")
                
                # Get following
                try:
                    following = cl.user_following(user_id, amount=50)
                    self.data['instagrapi_following'] = {k: v.dict() for k, v in following.items()}
                    print(f"✅ Extracted {len(following)} following")
                    time.sleep(3)
                except Exception as e:
                    print(f"⚠️ Following extraction error: {e}")
                
            else:
                print("❌ Instagrapi authentication failed")
                
        except Exception as e:
            print(f"❌ Instagrapi error: {e}")

    def fallback_extraction(self):
        """Fallback extraction methods"""
        print("\n🔄 PHASE 3: FALLBACK EXTRACTION")
        print("-" * 35)
        
        # Search for user
        search_url = f"{self.base_url}/web/search/topsearch/?context=blended&query={self.target}"
        response = self.safe_request(search_url)
        if response:
            try:
                self.data['search_results'] = response.json()
                print("✅ Search results extracted")
            except:
                pass
        
        self.smart_delay()
        
        # Try to get shared data from main page
        main_response = self.safe_request(f"{self.base_url}/{self.target}/")
        if main_response and main_response.text:
            # Extract shared data
            text = main_response.text
            if 'window._sharedData' in text:
                try:
                    start = text.find('window._sharedData = ') + len('window._sharedData = ')
                    end = text.find(';</script>', start)
                    shared_data = json.loads(text[start:end])
                    self.data['shared_data'] = shared_data
                    print("✅ Shared data extracted")
                except:
                    pass

    def intelligence_analysis(self):
        """Analyze extracted data for intelligence"""
        print("\n🧠 PHASE 4: INTELLIGENCE ANALYSIS")
        print("-" * 35)
        
        intelligence = {
            'extraction_timestamp': datetime.now().isoformat(),
            'target': self.target,
            'extraction_method': 'dreamflow_ghost_mode',
            'data_sources': list(self.data.keys()),
            'intelligence': {}
        }
        
        # Analyze profile data
        if 'profile_api' in self.data:
            try:
                profile = self.data['profile_api']
                if 'data' in profile and 'user' in profile['data']:
                    user = profile['data']['user']
                    intelligence['intelligence'].update({
                        'username': user.get('username'),
                        'full_name': user.get('full_name'),
                        'biography': user.get('biography'),
                        'external_url': user.get('external_url'),
                        'follower_count': user.get('edge_followed_by', {}).get('count'),
                        'following_count': user.get('edge_follow', {}).get('count'),
                        'post_count': user.get('edge_owner_to_timeline_media', {}).get('count'),
                        'is_private': user.get('is_private'),
                        'is_verified': user.get('is_verified'),
                        'profile_pic_url': user.get('profile_pic_url_hd')
                    })
            except Exception as e:
                print(f"⚠️ Profile analysis error: {e}")
        
        # Analyze instagrapi data
        if 'instagrapi_user_info' in self.data:
            try:
                user_info = self.data['instagrapi_user_info']
                intelligence['intelligence'].update({
                    'instagrapi_full_name': user_info.get('full_name'),
                    'instagrapi_biography': user_info.get('biography'),
                    'instagrapi_external_url': user_info.get('external_url'),
                    'instagrapi_follower_count': user_info.get('follower_count'),
                    'instagrapi_following_count': user_info.get('following_count'),
                    'instagrapi_media_count': user_info.get('media_count'),
                    'instagrapi_is_private': user_info.get('is_private'),
                    'instagrapi_is_verified': user_info.get('is_verified')
                })
            except Exception as e:
                print(f"⚠️ Instagrapi analysis error: {e}")
        
        self.data['intelligence'] = intelligence
        print("✅ Intelligence analysis complete")

    def save_results(self):
        """Save extraction results"""
        print("\n💾 PHASE 5: SAVING RESULTS")
        print("-" * 25)
        
        timestamp = int(time.time())
        
        # Save complete data
        filename = f"DREAMFLOW_GHOST_EXTRACTION_{self.target}_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False, default=str)
        print(f"✅ Complete data saved: {filename}")
        
        # Save intelligence summary
        if 'intelligence' in self.data:
            intel_filename = f"DREAMFLOW_INTELLIGENCE_{self.target}_{timestamp}.json"
            with open(intel_filename, 'w', encoding='utf-8') as f:
                json.dump(self.data['intelligence'], f, indent=2, ensure_ascii=False, default=str)
            print(f"✅ Intelligence saved: {intel_filename}")
        
        # Save summary report
        summary = f"""
🔥 DREAMFLOW GHOST MODE - EXTRACTION REPORT
==========================================
🎯 Target: {self.target}
📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🚀 Method: Anti-Rate-Limit + Session Injection

📊 EXTRACTION SUMMARY:
{"".join([f"  ✅ {source}\n" for source in self.data.keys()])}

🧠 KEY INTELLIGENCE:
{json.dumps(self.data.get('intelligence', {}).get('intelligence', {}), indent=2)}

🎉 STATUS: EXTRACTION COMPLETE
💎 Files generated: {filename}, {intel_filename if 'intelligence' in self.data else 'N/A'}
"""
        
        summary_filename = f"DREAMFLOW_SUMMARY_{self.target}_{timestamp}.txt"
        with open(summary_filename, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"✅ Summary saved: {summary_filename}")

    def execute(self):
        """Execute the complete dreamflow ghost mode operation"""
        print("🚀 EXECUTING DREAMFLOW GHOST MODE")
        print("=" * 50)
        
        # Phase 0: Setup
        self.load_existing_session()
        self.setup_session_with_auth()
        
        # Phase 1: Basic extraction
        self.extract_basic_profile()
        
        # Phase 2: Advanced extraction
        self.instagrapi_extraction()
        
        # Phase 3: Fallback methods
        self.fallback_extraction()
        
        # Phase 4: Intelligence analysis
        self.intelligence_analysis()
        
        # Phase 5: Save results
        self.save_results()
        
        print("\n🎉 DREAMFLOW GHOST MODE COMPLETE!")
        print("=" * 40)
        print(f"🎯 Target: {self.target}")
        print(f"📊 Data sources: {len(self.data)} sources")
        print(f"💎 Status: MISSION ACCOMPLISHED")
        print("=" * 40)

if __name__ == "__main__":
    ghost = DreamflowGhostMode()
    ghost.execute()
