#!/usr/bin/env python3
"""
Advanced Instagram Bypass System - 2025 Edition 
ระบบ bypass ที่ใช้การหลบหลีกแบบ advanced
"""

import requests
import random
import time
import json
from datetime import datetime
import base64
import hashlib

class AdvancedInstagramBypass:
    def __init__(self):
        self.session_cookies = self.load_all_sessions()
        self.working_proxies = self.load_working_proxies()
        self.user_agents = [
            # Mobile Instagram app UAs
            'Instagram 308.0.0.16.113 Android (30/11; 450dpi; 1080x2400; samsung; SM-G991B)',
            'Instagram 307.0.0.15.107 Android (29/10; 420dpi; 1080x2340; OnePlus; HD1903)',
            'Instagram 306.0.0.18.108 Android (28/9; 480dpi; 1080x2160; Xiaomi; MI 8)',
            'Instagram 305.0.0.16.109 Android (31/12; 560dpi; 1440x3040; samsung; SM-G973F)',
            
            # iOS Instagram app UAs
            'Instagram 308.0.0.28.102 (iPhone14,2; iOS 16_6; en_US; en-US; scale=3.00; 1170x2532)',
            'Instagram 307.0.0.27.99 (iPhone13,3; iOS 15_5; en_US; en-US; scale=3.00; 1284x2778)',
            
            # Web browser UAs
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 13; SM-S918B) Chrome/121.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; Pixel 6) Chrome/120.0.0.0 Mobile Safari/537.36'
        ]
        
    def load_all_sessions(self):
        """โหลด session cookies ทั้งหมด"""
        sessions = []
        import os
        import glob
        
        session_files = glob.glob("sessions/*sessionid*.json")
        for file_path in session_files:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if 'sessionid' in data:
                        sessions.append(data['sessionid'])
                    elif 'cookies' in data and 'sessionid' in data['cookies']:
                        sessions.append(data['cookies']['sessionid'])
            except:
                pass
                
        print(f"[SESSIONS] Loaded {len(sessions)} session cookies")
        return sessions
        
    def load_working_proxies(self):
        """โหลด working proxies"""
        try:
            with open("config/working_proxies.json", 'r') as f:
                proxy_data = json.load(f)
                proxies = [item["proxy"] for item in proxy_data]
                proxies.append("socks5://127.0.0.1:9050")  # Add TOR
                print(f"[PROXIES] Loaded {len(proxies)} working proxies")
                return proxies
        except:
            print(f"[PROXIES] No working proxies, using direct connection")
            return ["direct"]
            
    def generate_device_id(self):
        """สร้าง device ID แบบสุ่ม"""
        timestamp = str(int(time.time()))
        random_str = ''.join(random.choices('0123456789abcdef', k=16))
        device_id = hashlib.md5((timestamp + random_str).encode()).hexdigest()
        return device_id[:16]
        
    def create_bypass_session(self, use_proxy=False):
        """สร้าง session แบบ bypass"""
        session = requests.Session()
        
        # Random user agent
        ua = random.choice(self.user_agents)
        device_id = self.generate_device_id()
        
        # Advanced headers ที่ดูเหมือน real Instagram app
        headers = {
            'User-Agent': ua,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'X-IG-App-ID': '936619743392459',
            'X-IG-WWW-Claim': '0',
            'X-Requested-With': 'XMLHttpRequest',
            'X-ASBD-ID': '129477',
            'X-CSRFToken': self.generate_csrf_token(),
            'X-Instagram-AJAX': str(random.randint(1000000000, 9999999999)),
            'sec-ch-ua-mobile': '?1' if 'Mobile' in ua else '?0',
            'sec-ch-ua-platform': '"Android"' if 'Android' in ua else '"iOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
        }
        
        session.headers.update(headers)
        
        # Random sessionid if available
        if self.session_cookies:
            sessionid = random.choice(self.session_cookies)
            session.cookies.set('sessionid', sessionid)
            
        # Use proxy only if explicitly requested and available
        if use_proxy and self.working_proxies and self.working_proxies != ["direct"]:
            proxy = random.choice(self.working_proxies)
            if proxy != "direct":
                try:
                    # Test proxy first
                    test_response = requests.get("http://httpbin.org/ip", 
                                               proxies={'http': proxy, 'https': proxy}, 
                                               timeout=5)
                    if test_response.status_code == 200:
                        session.proxies = {'http': proxy, 'https': proxy}
                        print(f"   🌐 Using proxy: {proxy}")
                    else:
                        print(f"   ⚠️ Proxy test failed, using direct connection")
                except:
                    print(f"   ⚠️ Proxy error, using direct connection")
            else:
                print(f"   🔗 Using direct connection")
        else:
            print(f"   🔗 Using direct connection")
                
        return session
        
    def generate_csrf_token(self):
        """สร้าง CSRF token แบบสุ่ม"""
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        return ''.join(random.choices(chars, k=32))
        
    def intelligent_delay(self, base_delay=1.0, variance=0.5):
        """Delay แบบ intelligent ที่ดูเหมือน human behavior"""
        # Random delay with human-like pattern
        delay = base_delay + random.uniform(-variance, variance)
        
        # Add occasional longer delays (like human would pause)
        if random.random() < 0.1:  # 10% chance
            delay += random.uniform(2, 5)
            
        time.sleep(max(0.1, delay))
        
    def bypass_rate_limit(self, target_username, max_attempts=10):
        """Bypass rate limit ด้วยเทคนิค advanced"""
        
        # Multiple endpoints to try
        endpoints = [
            f"https://www.instagram.com/api/v1/users/web_profile_info/?username={target_username}",
            f"https://www.instagram.com/{target_username}/?__a=1&__d=dis",
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={target_username}",
        ]
        
        for attempt in range(max_attempts):
            try:
                # Create fresh session for each attempt
                # Use proxy only on some attempts to mix strategies
                use_proxy = (attempt > 5 and attempt % 3 == 0)
                session = self.create_bypass_session(use_proxy=use_proxy)
                
                # Choose random endpoint
                endpoint = random.choice(endpoints)
                
                print(f"🎯 Attempt {attempt+1}/{max_attempts}: {endpoint.split('/')[-1]}")
                
                # Add random delay before request
                self.intelligent_delay(random.uniform(0.5, 2.0))
                
                # Make request
                response = session.get(endpoint, timeout=15)
                
                print(f"   Status: {response.status_code}, Size: {len(response.content)} bytes")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"   ✅ SUCCESS! Got JSON data")
                        return data, response
                    except:
                        print(f"   ⚠️ HTML response (might be blocked)")
                        if len(response.content) > 50000:  # Large HTML response
                            print(f"   📄 Large HTML response - extracting...")
                            return response.text, response
                        
                elif response.status_code == 401:
                    print(f"   🔒 401 Unauthorized - trying different session...")
                    
                elif response.status_code == 429:
                    print(f"   ⏱️ Rate limited - increasing delay...")
                    self.intelligent_delay(random.uniform(5, 15))
                    
                else:
                    print(f"   ❌ Unexpected status: {response.status_code}")
                    
            except Exception as e:
                print(f"   💥 Error: {str(e)[:100]}...")
                
            # Progressive delay increase
            base_delay = 1.0 + (attempt * 0.5)
            self.intelligent_delay(base_delay)
            
        print(f"❌ Failed after {max_attempts} attempts")
        return None, None
        
    def extract_profile_data(self, data):
        """แยกข้อมูล profile จาก response"""
        if isinstance(data, dict):
            if 'data' in data and 'user' in data['data']:
                user = data['data']['user']
                return {
                    'username': user.get('username', ''),
                    'full_name': user.get('full_name', ''),
                    'follower_count': user.get('edge_followed_by', {}).get('count', 0),
                    'following_count': user.get('edge_follow', {}).get('count', 0),
                    'media_count': user.get('edge_owner_to_timeline_media', {}).get('count', 0),
                    'is_private': user.get('is_private', False),
                    'is_verified': user.get('is_verified', False),
                    'biography': user.get('biography', ''),
                    'external_url': user.get('external_url', ''),
                    'profile_pic_url': user.get('profile_pic_url_hd', ''),
                }
        return None

def main():
    bypass = AdvancedInstagramBypass()
    
    targets = ["alx.trading", "whatilove1728"]
    
    for target in targets:
        print(f"\n🎯 TARGET: {target}")
        print("="*50)
        
        data, response = bypass.bypass_rate_limit(target, max_attempts=15)
        
        if data:
            profile = bypass.extract_profile_data(data)
            if profile:
                print(f"\n📊 PROFILE EXTRACTED:")
                for key, value in profile.items():
                    print(f"   {key}: {value}")
            else:
                print(f"\n📄 Raw data received ({len(str(data))} chars)")
                
            # Save raw response
            timestamp = int(time.time())
            filename = f"bypass_result_{target}_{timestamp}.json"
            try:
                with open(filename, 'w') as f:
                    if isinstance(data, dict):
                        json.dump(data, f, indent=2)
                    else:
                        f.write(str(data))
                print(f"💾 Saved to: {filename}")
            except Exception as e:
                print(f"❌ Save error: {e}")
        else:
            print(f"❌ Failed to extract data for {target}")
            
        print(f"\n⏱️ Cooling down...")
        time.sleep(random.uniform(10, 20))

if __name__ == "__main__":
    main()
