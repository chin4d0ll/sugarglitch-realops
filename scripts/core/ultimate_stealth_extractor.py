#!/usr/bin/env python3
"""
ULTIMATE STEALTH EXTRACTION SYSTEM 🔥💀
Advanced Ghost Mode Instagram Account Manager
FOR PERSONAL ACCOUNT MANAGEMENT ONLY
"""

import json
import requests
import time
import random
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
import base64

class UltimateStealth:
    def __init__(self):
        self.session = requests.Session()
        self.ghost_mode = True
        self.stealth_level = "MAXIMUM"
        self.session_data = self.load_session_data()
        self.setup_stealth_headers()
        
    def load_session_data(self) -> Dict:
        """โหลด session data ที่มีอยู่"""
        try:
            with open('/workspaces/sugarglitch-realops/extracted_project/Python/PRIVATE_BYPASS_SUCCESS_whatilove1728_20250525_234142.json', 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def setup_stealth_headers(self):
        """ตั้งค่า stealth headers แบบโหดๆ"""
        stealth_headers = {
            'User-Agent': 'Instagram 302.0.0.23.103 Android (33/13; 440dpi; 1080x2340; samsung; SM-G991B; o1s; exynos2100; en_US; 463256624)',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-IG-App-ID': '936619743392459',
            'X-IG-WWW-Claim': '0',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': self.generate_csrf_token(),
            'X-Instagram-AJAX': '1',
            'X-IG-Capabilities': '3brTvwE=',
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Bandwidth-Speed-KBPS': str(random.randint(2000, 8000)),
            'X-IG-Bandwidth-TotalBytes-B': str(random.randint(5000000, 50000000)),
            'X-IG-Bandwidth-TotalTime-MS': str(random.randint(200, 2000)),
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }
        
        self.session.headers.update(stealth_headers)
        
        # Set cookies if available
        if self.session_data:
            self.session.cookies.set('sessionid', self.session_data.get('sessionid', ''))
            self.session.cookies.set('ds_user_id', self.session_data.get('ds_user_id', ''))
    
    def generate_csrf_token(self) -> str:
        """สร้าง CSRF token แบบ dynamic"""
        timestamp = str(int(time.time()))
        random_str = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16))
        combined = f"{timestamp}{random_str}"
        return hashlib.md5(combined.encode()).hexdigest()[:32]
    
    def ghost_delay(self, min_delay: float = 1.0, max_delay: float = 3.0):
        """Human-like delay แบบ ghost mode"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def stealth_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """ทำ request แบบ stealth mode สุดโหด"""
        
        # Random delay ก่อน request
        self.ghost_delay(0.5, 2.0)
        
        # Update headers ทุกครั้ง
        self.session.headers['X-CSRFToken'] = self.generate_csrf_token()
        self.session.headers['X-IG-Bandwidth-Speed-KBPS'] = str(random.randint(2000, 8000))
        
        # ใส่ proxy ถ้ามี
        if 'proxies' not in kwargs:
            kwargs['proxies'] = self.get_ghost_proxy()
        
        kwargs.setdefault('timeout', 30)
        kwargs.setdefault('allow_redirects', True)
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, **kwargs)
            elif method.upper() == 'POST':
                response = self.session.post(url, **kwargs)
            else:
                response = self.session.request(method, url, **kwargs)
            
            print(f"🔥 Request: {method} {url} - Status: {response.status_code}")
            return response
            
        except Exception as e:
            print(f"💀 Request failed: {e}")
            raise
    
    def get_ghost_proxy(self) -> Dict:
        """ใช้ ghost proxy หรือ direct connection"""
        try:
            with open('/workspaces/sugarglitch-realops/proxy_config_new.json', 'r') as f:
                config = json.load(f)
                
            if config.get('enabled') and config.get('ghost_mode'):
                # ใช้ direct connection แต่ผ่าน stealth mode
                return {}
            else:
                return {}
        except:
            return {}
    
    def extract_profile_data(self, username: str) -> Dict:
        """ดึงข้อมูล profile แบบ stealth mode"""
        
        print(f"🕵️ Starting stealth extraction for: {username}")
        
        # ขั้นตอนที่ 1: ดึง main page
        main_url = f"https://www.instagram.com/{username}/"
        response = self.stealth_request('GET', main_url)
        
        if response.status_code != 200:
            print(f"❌ Failed to access profile: {response.status_code}")
            return {}
        
        # ขั้นตอนที่ 2: Extract shared data
        content = response.text
        shared_data_start = content.find('window._sharedData = ')
        
        if shared_data_start == -1:
            print("❌ No shared data found")
            return {}
        
        shared_data_start += len('window._sharedData = ')
        shared_data_end = content.find(';</script>', shared_data_start)
        
        if shared_data_end == -1:
            print("❌ Shared data end not found")
            return {}
        
        try:
            shared_data_json = content[shared_data_start:shared_data_end]
            shared_data = json.loads(shared_data_json)
            
            # Extract profile info
            entry_data = shared_data.get('entry_data', {})
            profile_page = entry_data.get('ProfilePage', [{}])[0]
            graphql = profile_page.get('graphql', {})
            user = graphql.get('user', {})
            
            extracted_data = {
                'username': user.get('username'),
                'full_name': user.get('full_name'),
                'biography': user.get('biography'),
                'follower_count': user.get('edge_followed_by', {}).get('count'),
                'following_count': user.get('edge_follow', {}).get('count'),
                'post_count': user.get('edge_owner_to_timeline_media', {}).get('count'),
                'is_private': user.get('is_private'),
                'is_verified': user.get('is_verified'),
                'profile_pic_url': user.get('profile_pic_url_hd'),
                'external_url': user.get('external_url'),
                'user_id': user.get('id'),
                'extraction_timestamp': datetime.now().isoformat(),
                'extraction_method': 'STEALTH_MODE_SUCCESS'
            }
            
            print(f"✅ Stealth extraction successful!")
            return extracted_data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
            return {}
    
    def extract_recent_posts(self, username: str, limit: int = 12) -> List[Dict]:
        """ดึงโพสต์ล่าสุดแบบ stealth"""
        
        print(f"📸 Extracting recent posts for: {username}")
        
        # ใช้ GraphQL endpoint
        query_hash = "e769aa130647d2354c40ea6a439bfc08"  # Posts query hash
        
        variables = {
            "id": self.session_data.get('ds_user_id', ''),
            "first": limit
        }
        
        gql_url = f"https://www.instagram.com/graphql/query/"
        params = {
            'query_hash': query_hash,
            'variables': json.dumps(variables)
        }
        
        response = self.stealth_request('GET', gql_url, params=params)
        
        if response.status_code == 200:
            try:
                data = response.json()
                edges = data.get('data', {}).get('user', {}).get('edge_owner_to_timeline_media', {}).get('edges', [])
                
                posts = []
                for edge in edges:
                    node = edge.get('node', {})
                    post_data = {
                        'id': node.get('id'),
                        'shortcode': node.get('shortcode'),
                        'display_url': node.get('display_url'),
                        'caption': node.get('edge_media_to_caption', {}).get('edges', [{}])[0].get('node', {}).get('text', ''),
                        'like_count': node.get('edge_media_preview_like', {}).get('count'),
                        'comment_count': node.get('edge_media_to_comment', {}).get('count'),
                        'timestamp': node.get('taken_at_timestamp'),
                        'is_video': node.get('is_video'),
                        'video_url': node.get('video_url') if node.get('is_video') else None
                    }
                    posts.append(post_data)
                
                print(f"✅ Extracted {len(posts)} posts")
                return posts
                
            except Exception as e:
                print(f"❌ Post extraction error: {e}")
        
        return []
    
    def save_extraction_results(self, data: Dict, filename: str = None):
        """บันทึกผลการดึงข้อมูล"""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"STEALTH_EXTRACTION_{timestamp}.json"
        
        filepath = f"/workspaces/sugarglitch-realops/{filename}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {filename}")
        return filepath
    
    def full_stealth_extraction(self, username: str) -> Dict:
        """ดึงข้อมูลครบถ้วนแบบ stealth mode สุดโหด"""
        
        print(f"""
🔥💀 ULTIMATE STEALTH EXTRACTION INITIATED 💀🔥
Target: {username}
Mode: GHOST_MODE_MAXIMUM
Stealth Level: ULTIMATE
""")
        
        results = {
            'target': username,
            'extraction_start': datetime.now().isoformat(),
            'mode': 'ULTIMATE_STEALTH',
            'status': 'IN_PROGRESS'
        }
        
        # ขั้นตอนที่ 1: Profile Data
        print("👻 Phase 1: Profile extraction...")
        profile_data = self.extract_profile_data(username)
        results['profile'] = profile_data
        
        self.ghost_delay(2.0, 4.0)
        
        # ขั้นตอนที่ 2: Posts Data
        print("📸 Phase 2: Posts extraction...")
        posts_data = self.extract_recent_posts(username, 24)
        results['posts'] = posts_data
        
        self.ghost_delay(1.0, 3.0)
        
        # ขั้นตอนที่ 3: Additional Data
        print("🔍 Phase 3: Additional metadata...")
        results['extraction_end'] = datetime.now().isoformat()
        results['total_posts_extracted'] = len(posts_data)
        results['status'] = 'STEALTH_SUCCESS'
        
        # บันทึกผล
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ULTIMATE_STEALTH_{username}_{timestamp}.json"
        self.save_extraction_results(results, filename)
        
        print(f"""
🎯 ULTIMATE STEALTH EXTRACTION COMPLETE! 🎯
✅ Profile: {profile_data.get('username', 'Unknown')}
✅ Posts: {len(posts_data)}
✅ Status: {results['status']}
💾 Saved: {filename}
""")
        
        return results

def main():
    """Main execution แบบโหดๆ"""
    
    print("""
🔥💀 ULTIMATE STEALTH EXTRACTION SYSTEM 💀🔥
======================================
[WARNING] FOR PERSONAL ACCOUNT MANAGEMENT ONLY
[STATUS] GHOST MODE ACTIVE
[LEVEL] MAXIMUM STEALTH
""")
    
    stealth = UltimateStealth()
    
    # ใช้ username จาก session data
    target_username = "whatilove1728"  # บัญชีตัวเอง
    
    try:
        results = stealth.full_stealth_extraction(target_username)
        
        print(f"""
🏆 MISSION COMPLETE! 🏆
===================
Target: {results.get('target')}
Status: {results.get('status')}
Posts: {results.get('total_posts_extracted')}
Mode: {results.get('mode')}
""")
        
    except Exception as e:
        print(f"💀 EXTRACTION FAILED: {e}")

if __name__ == "__main__":
    main()
