#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ ADVANCED STEALTH INSTALOADER ⚡
ใช้ realistic delays + proper session management
Enhanced for reliability, stealth, and maintainability.
"""
"""
⚡ ADVANCED STEALTH INSTALOADER ⚡
ใช้ realistic delays + proper session management
"""

import instaloader
import json
import time
import random
import os
from datetime import datetime
from pathlib import Path

class AdvancedStealthInstaloader:
    def __init__(self):
        self.targets = ['alx.trading', 'whatilove1728']
        self.results = {}
        
    def stealth_delay(self, min_delay=8, max_delay=14):
        """Realistic human delay"""
        delay = random.uniform(min_delay, max_delay)
        print(f"🕐 Stealth delay: {delay:.2f}s")
        time.sleep(delay)
    
    def load_fresh_session(self):
        """โหลด fresh session จากไฟล์"""
        session_files = [
            "/workspaces/sugarglitch-realops/sessions/fresh_session.json",
            "/workspaces/sugarglitch-realops/sessions/alx_trading_sessionid_1748519715.json"
        ]
        
        for session_file in session_files:
            if os.path.exists(session_file):
                print(f"🔑 Loading session: {session_file}")
                try:
                    with open(session_file, 'r') as f:
                        session_data = json.load(f)
                    
                    if 'sessionid' in session_data:
                        print(f"✅ Found sessionid: {session_data['sessionid'][:20]}...")
                        return session_data
                        
                except Exception as e:
                    print(f"❌ Session load error: {e}")
        
        print("❌ No valid session found")
        return None
    
    def create_instaloader_session(self, session_data):
        """สร้าง Instaloader session file"""
        print("🔧 Creating Instaloader session...")
        
        try:
            # สร้าง Instaloader instance
            L = instaloader.Instaloader(
                sleep=True,
                quiet=False,
                user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
                request_timeout=30
            )
            
            # ตั้งค่า session cookies
            if 'sessionid' in session_data:
                # ใช้ manual session loading
                session_filename = f"session-alx.trading"
                session_path = Path(f"./sessions/{session_filename}")
                session_path.parent.mkdir(exist_ok=True)
                
                # Login โดยใช้ session
                L.context._session.cookies.update({
                    'sessionid': session_data['sessionid']
                })
                
                # เพิ่ม cookies อื่น ถ้ามี
                for key in ['csrftoken', 'ds_user_id', 'mid', 'rur']:
                    if key in session_data:
                        L.context._session.cookies[key] = session_data[key]
                
                # บันทึก session
                L.save_session_to_file(session_filename)
                print("✅ Instaloader session created")
                
                return L
                
        except Exception as e:
            print(f"❌ Session creation error: {e}")
            
        return None
    
    def extract_with_stealth(self, username, L):
        """ดึงข้อมูลแบบ stealth"""
        print(f"🎯 Extracting: {username}")
        
        try:
            # Stealth delay ก่อนดึงข้อมูล
            self.stealth_delay(10, 18)
            
            # ดึง profile
            profile = instaloader.Profile.from_username(L.context, username)
            
            # Random delay ระหว่างการดึงข้อมูล
            time.sleep(random.uniform(2, 5))
            
            # ดึงข้อมูลแบบครบถ้วน
            profile_data = {
                'basic_info': {
                    'username': profile.username,
                    'userid': profile.userid,
                    'full_name': profile.full_name,
                    'biography': profile.biography,
                    'external_url': profile.external_url,
                    'followers': profile.followers,
                    'followees': profile.followees,
                    'mediacount': profile.mediacount,
                    'is_private': profile.is_private,
                    'is_verified': profile.is_verified,
                    'is_business_account': profile.is_business_account,
                    'profile_pic_url': profile.profile_pic_url,
                },
                'extracted_at': datetime.now().isoformat()
            }
            
            # ถ้าเป็น public account ดึงโพสต์ล่าสุด
            if not profile.is_private:
                try:
                    print(f"📸 Getting recent posts for {username}...")
                    recent_posts = []
                    
                    for i, post in enumerate(profile.get_posts()):
                        if i >= 5:  # เอาแค่ 5 โพสต์ล่าสุด
                            break
                        
                        recent_posts.append({
                            'shortcode': post.shortcode,
                            'date': post.date.isoformat(),
                            'caption': post.caption[:200] + '...' if post.caption and len(post.caption) > 200 else post.caption,
                            'likes': post.likes,
                            'comments': post.comments,
                            'is_video': post.is_video,
                            'url': f"https://www.instagram.com/p/{post.shortcode}/"
                        })
                        
                        # Delay ระหว่างโพสต์
                        time.sleep(random.uniform(1, 3))
                    
                    profile_data['recent_posts'] = recent_posts
                    print(f"✅ Got {len(recent_posts)} recent posts")
                    
                except Exception as e:
                    print(f"⚠️ Recent posts error: {e}")
                    profile_data['recent_posts'] = []
            
            print(f"✅ Profile extracted: {username}")
            print(f"   👤 Name: {profile.full_name}")
            print(f"   👥 Followers: {profile.followers:,}")
            print(f"   📷 Posts: {profile.mediacount:,}")
            print(f"   🔒 Private: {profile.is_private}")
            
            return profile_data
            
        except Exception as e:
            print(f"❌ Extraction failed for {username}: {e}")
            return None
    
    def run_advanced_extraction(self):
        """รันการดึงข้อมูลแบบขั้นสูง"""
        print("⚡ ADVANCED STEALTH INSTALOADER")
        print("=" * 50)
        
        # โหลด session
        session_data = self.load_fresh_session()
        
        if not session_data:
            print("❌ No session data available")
            print("📝 Please run: python fresh_cookie_extractor.py")
            print("   And follow the instructions to get fresh cookies")
            return None
        
        # สร้าง Instaloader
        L = self.create_instaloader_session(session_data)
        
        if not L:
            print("❌ Failed to create Instaloader session")
            return None
        
        # ดึงข้อมูลแต่ละ account
        for username in self.targets:
            print(f"\n🎯 Processing: {username}")
            
            profile_data = self.extract_with_stealth(username, L)
            
            if profile_data:
                self.results[username] = profile_data
                print(f"✅ Success: {username}")
            else:
                print(f"❌ Failed: {username}")
            
            # Long delay between accounts
            if username != self.targets[-1]:  # ถ้าไม่ใช่ account สุดท้าย
                self.stealth_delay(20, 35)
        
        # บันทึกผล
        self.save_results()
        
        print("\n🎉 Advanced extraction completed!")
        return self.results
    
    def save_results(self):
        """บันทึกผลลัพธ์"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"/workspaces/sugarglitch-realops/results/advanced_stealth_results_{timestamp}.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved: {filename}")

if __name__ == "__main__":
    extractor = AdvancedStealthInstaloader()
    results = extractor.run_advanced_extraction()
    
    if results:
        print("\n📊 EXTRACTION SUMMARY")
        print("=" * 40)
        for username, data in results.items():
            basic = data['basic_info']
            print(f"👤 {username}:")
            print(f"   📱 Full name: {basic['full_name']}")
            print(f"   👥 Followers: {basic['followers']:,}")
            print(f"   📷 Posts: {basic['mediacount']:,}")
            print(f"   🔒 Private: {basic['is_private']}")
            if 'recent_posts' in data:
                print(f"   📸 Recent posts: {len(data['recent_posts'])}")
    else:
        print("\n❌ No data extracted")
