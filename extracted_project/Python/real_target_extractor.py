#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Target Extractor - ใช้ session จริงดึงข้อมูล target จริง
"""

import requests
import json
import time
import random
from datetime import datetime
import os

class RealTargetExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive'
        }
        self.extracted_targets = []
        
    def setup_session(self):
        """โหลด session จริงจากไฟล์ที่มีอยู่แล้ว"""
        try:
            # โหลด session หลัก
            with open('session.json', 'r') as f:
                main_session = json.load(f)
            
            # โหลด breach session
            with open('breach_session.json', 'r') as f:
                breach_session = json.load(f)
            
            # ตั้งค่า cookies
            self.session.cookies.set('sessionid', main_session.get('sessionid', ''))
            self.session.cookies.set('ds_user_id', main_session.get('ds_user_id', ''))
            self.session.cookies.set('mid', f"Y{random.randint(1000000, 9999999)}ABC")
            self.session.cookies.set('ig_did', f"{random.randint(10000000, 99999999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(100000000000, 999999999999)}")
            self.session.cookies.set('csrftoken', f"csrf{random.randint(10000000, 99999999)}")
            
            print(f"[+] Session loaded: {main_session.get('ds_user_id', 'Unknown')}")
            return True
            
        except Exception as e:
            print(f"[!] Error loading session: {e}")
            return False
    
    def get_csrf_token(self):
        """ดึง CSRF token ใหม่"""
        try:
            response = self.session.get('https://www.instagram.com/', headers=self.base_headers)
            csrf_token = response.cookies.get('csrftoken')
            if csrf_token:
                self.session.cookies.set('csrftoken', csrf_token)
                return csrf_token
            return None
        except:
            return None
    
    def extract_from_followers(self, username="alx.trading"):
        """ดึงข้อมูลจาก followers ของ target"""
        print(f"[*] Extracting followers from {username}...")
        
        try:
            # ดึง user ID ก่อน
            user_info_url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
            headers = self.base_headers.copy()
            headers['X-CSRFToken'] = self.session.cookies.get('csrftoken', '')
            headers['X-Instagram-AJAX'] = '1'
            headers['X-Requested-With'] = 'XMLHttpRequest'
            
            response = self.session.get(user_info_url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                user_id = data.get('data', {}).get('user', {}).get('id')
                
                if user_id:
                    # ดึง followers
                    followers_url = f"https://www.instagram.com/api/v1/friendships/{user_id}/followers/"
                    
                    followers_response = self.session.get(followers_url, headers=headers)
                    
                    if followers_response.status_code == 200:
                        followers_data = followers_response.json()
                        users = followers_data.get('users', [])
                        
                        for user in users[:20]:  # เอาแค่ 20 คนแรก
                            target = {
                                'username': user.get('username'),
                                'full_name': user.get('full_name'),
                                'profile_pic_url': user.get('profile_pic_url'),
                                'is_private': user.get('is_private', False),
                                'follower_count': user.get('follower_count', 0),
                                'following_count': user.get('following_count', 0),
                                'is_verified': user.get('is_verified', False),
                                'external_url': user.get('external_url'),
                                'biography': user.get('biography'),
                                'extracted_from': 'followers',
                                'source_account': username,
                                'timestamp': datetime.now().isoformat()
                            }
                            self.extracted_targets.append(target)
                            
                        print(f"[+] Extracted {len(users)} followers")
                        return True
            
            print(f"[!] Failed to extract followers: {response.status_code}")
            return False
            
        except Exception as e:
            print(f"[!] Error extracting followers: {e}")
            return False
    
    def extract_from_hashtags(self, hashtag="trading"):
        """ดึงข้อมูลจาก hashtag"""
        print(f"[*] Extracting from #{hashtag}...")
        
        try:
            hashtag_url = f"https://www.instagram.com/api/v1/tags/web_info/?tag_name={hashtag}"
            headers = self.base_headers.copy()
            headers['X-CSRFToken'] = self.session.cookies.get('csrftoken', '')
            
            response = self.session.get(hashtag_url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                posts = data.get('data', {}).get('top', {}).get('sections', [])
                
                for section in posts:
                    layout_content = section.get('layout_content', {})
                    medias = layout_content.get('medias', [])
                    
                    for media in medias[:10]:  # เอาแค่ 10 posts
                        media_info = media.get('media', {})
                        user = media_info.get('user', {})
                        
                        if user:
                            target = {
                                'username': user.get('username'),
                                'full_name': user.get('full_name'),
                                'profile_pic_url': user.get('profile_pic_url'),
                                'is_private': user.get('is_private', False),
                                'is_verified': user.get('is_verified', False),
                                'extracted_from': f'hashtag_{hashtag}',
                                'media_id': media_info.get('id'),
                                'like_count': media_info.get('like_count', 0),
                                'timestamp': datetime.now().isoformat()
                            }
                            self.extracted_targets.append(target)
                
                print(f"[+] Extracted targets from #{hashtag}")
                return True
            
            print(f"[!] Failed to extract from hashtag: {response.status_code}")
            return False
            
        except Exception as e:
            print(f"[!] Error extracting from hashtag: {e}")
            return False
    
    def extract_from_location(self, location_id="213385402"):
        """ดึงข้อมูลจาก location (Bangkok default)"""
        print(f"[*] Extracting from location {location_id}...")
        
        try:
            location_url = f"https://www.instagram.com/api/v1/locations/{location_id}/info/"
            headers = self.base_headers.copy()
            headers['X-CSRFToken'] = self.session.cookies.get('csrftoken', '')
            
            response = self.session.get(location_url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                posts = data.get('location', {}).get('top_posts', {}).get('nodes', [])
                
                for post in posts[:10]:
                    owner = post.get('owner', {})
                    if owner:
                        target = {
                            'username': owner.get('username'),
                            'full_name': owner.get('full_name'),
                            'profile_pic_url': owner.get('profile_pic_url'),
                            'is_private': owner.get('is_private', False),
                            'is_verified': owner.get('is_verified', False),
                            'extracted_from': f'location_{location_id}',
                            'media_id': post.get('id'),
                            'timestamp': datetime.now().isoformat()
                        }
                        self.extracted_targets.append(target)
                
                print(f"[+] Extracted targets from location")
                return True
            
            print(f"[!] Failed to extract from location: {response.status_code}")
            return False
            
        except Exception as e:
            print(f"[!] Error extracting from location: {e}")
            return False
    
    def extract_suggested_users(self):
        """ดึง suggested users"""
        print("[*] Extracting suggested users...")
        
        try:
            suggested_url = "https://www.instagram.com/api/v1/fb/discover/aymt/?max_id="
            headers = self.base_headers.copy()
            headers['X-CSRFToken'] = self.session.cookies.get('csrftoken', '')
            
            response = self.session.get(suggested_url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                suggested_users = data.get('suggested_users', {}).get('suggestions', [])
                
                for suggestion in suggested_users[:15]:
                    user = suggestion.get('user', {})
                    if user:
                        target = {
                            'username': user.get('username'),
                            'full_name': user.get('full_name'),
                            'profile_pic_url': user.get('profile_pic_url'),
                            'is_private': user.get('is_private', False),
                            'follower_count': user.get('follower_count', 0),
                            'following_count': user.get('following_count', 0),
                            'is_verified': user.get('is_verified', False),
                            'extracted_from': 'suggested_users',
                            'timestamp': datetime.now().isoformat()
                        }
                        self.extracted_targets.append(target)
                
                print(f"[+] Extracted {len(suggested_users)} suggested users")
                return True
            
            print(f"[!] Failed to extract suggested users: {response.status_code}")
            return False
            
        except Exception as e:
            print(f"[!] Error extracting suggested users: {e}")
            return False
    
    def save_results(self):
        """บันทึกผลลัพธ์"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"REAL_TARGET_EXTRACTION_{timestamp}.json"
        
        results = {
            'extraction_timestamp': datetime.now().isoformat(),
            'total_targets_extracted': len(self.extracted_targets),
            'unique_usernames': len(set(t['username'] for t in self.extracted_targets if t.get('username'))),
            'extraction_sources': list(set(t['extracted_from'] for t in self.extracted_targets)),
            'targets': self.extracted_targets,
            'summary': {
                'private_accounts': len([t for t in self.extracted_targets if t.get('is_private')]),
                'verified_accounts': len([t for t in self.extracted_targets if t.get('is_verified')]),
                'accounts_with_external_url': len([t for t in self.extracted_targets if t.get('external_url')]),
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"[+] Results saved to {filename}")
        return filename
    
    def run_extraction(self):
        """เรียกใช้การดึงข้อมูลทั้งหมด"""
        print("=" * 60)
        print("🎯 REAL TARGET EXTRACTOR - Using Live Sessions")
        print("=" * 60)
        
        # ดึง CSRF token ใหม่
        csrf = self.get_csrf_token()
        if csrf:
            print(f"[+] CSRF Token updated: {csrf[:20]}...")
        
        # รอสักครู่
        time.sleep(random.uniform(2, 5))
        
        # ดึงข้อมูลจากแหล่งต่างๆ
        extraction_methods = [
            ('followers', lambda: self.extract_from_followers("alx.trading")),
            ('hashtag_trading', lambda: self.extract_from_hashtags("trading")),
            ('hashtag_forex', lambda: self.extract_from_hashtags("forex")),
            ('hashtag_bitcoin', lambda: self.extract_from_hashtags("bitcoin")),
            ('location_bangkok', lambda: self.extract_from_location("213385402")),
            ('suggested_users', lambda: self.extract_suggested_users())
        ]
        
        for method_name, method_func in extraction_methods:
            try:
                print(f"\n[*] Running: {method_name}")
                success = method_func()
                if success:
                    print(f"[+] {method_name} completed successfully")
                else:
                    print(f"[!] {method_name} failed")
                
                # รอระหว่างการ request
                time.sleep(random.uniform(3, 8))
                
            except Exception as e:
                print(f"[!] Error in {method_name}: {e}")
                continue
        
        # บันทึกผลลัพธ์
        if self.extracted_targets:
            filename = self.save_results()
            print(f"\n🎉 Extraction Complete!")
            print(f"📊 Total Targets: {len(self.extracted_targets)}")
            print(f"📁 Saved to: {filename}")
        else:
            print(f"\n❌ No targets extracted")

if __name__ == "__main__":
    extractor = RealTargetExtractor()
    extractor.run_extraction()
