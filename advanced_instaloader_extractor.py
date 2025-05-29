#!/usr/bin/env python3
"""
🔥 ADVANCED INSTALOADER STEALTH EXTRACTOR 🔥
ระดับอาจารณ์ - หลบ bot detection ทุกรูปแบบ
"""

import instaloader
import json
import time
import random
import os
from datetime import datetime
from pathlib import Path
from fake_useragent import UserAgent
import requests

class AdvancedStealthExtractor:
    def __init__(self):
        # สร้าง Instaloader instance with advanced stealth
        self.L = instaloader.Instaloader(
            # Advanced stealth options
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=True,
            compress_json=False,
            
            # Rate limiting protection
            sleep=True,
            
            # User agent rotation
            user_agent=UserAgent().random,
            
            # Request headers customization
            request_timeout=30,
        )
        
        # Advanced stealth settings
        self.setup_stealth_mode()
        
        # Target accounts
        self.targets = ['alx.trading', 'whatilove1728']
        
        # Results storage
        self.results = {
            'extraction_timestamp': datetime.now().isoformat(),
            'method': 'Advanced Instaloader Stealth',
            'accounts': {}
        }
    
    def setup_stealth_mode(self):
        """ตั้งค่าโหมดหลบตัวขั้นสูง"""
        print("🥷 Setting up advanced stealth mode...")
        
        # Custom session management
        self.L.context._session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        })
        
        # Random delays between requests
        self.L.context.rate_controller = lambda query_type: random.uniform(5, 12)
        
        print("✅ Advanced stealth mode activated")
    
    def load_existing_session(self):
        """โหลด session ที่มีอยู่"""
        print("🔑 Attempting to load existing session...")
        
        session_file = "/workspaces/sugarglitch-realops/sessions/alx_trading_sessionid_1748519715.json"
        
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            if 'sessionid' in session_data:
                # สร้าง session file สำหรับ Instaloader
                insta_session_file = Path("./sessions/session-alx.trading")
                insta_session_file.parent.mkdir(exist_ok=True)
                
                # Instaloader ใช้ format ที่ต่างออกไป
                with open(insta_session_file, 'w') as f:
                    # สร้าง session format ที่ Instaloader เข้าใจ
                    session_content = {
                        'cookies': {
                            'sessionid': session_data['sessionid']
                        }
                    }
                    json.dump(session_content, f)
                
                print("✅ Session file created for Instaloader")
                return True
                
        except Exception as e:
            print(f"❌ Session load error: {e}")
            
        return False
    
    def extract_profile_advanced(self, username):
        """ดึงข้อมูล profile แบบขั้นสูง"""
        print(f"🎯 Extracting advanced profile data: {username}")
        
        try:
            # Load profile with stealth
            profile = instaloader.Profile.from_username(self.L.context, username)
            
            # Extract comprehensive data
            profile_data = {
                'basic_info': {
                    'username': profile.username,
                    'full_name': profile.full_name,
                    'biography': profile.biography,
                    'external_url': profile.external_url,
                    'followers': profile.followers,
                    'followees': profile.followees,
                    'mediacount': profile.mediacount,
                    'userid': profile.userid,
                    'is_private': profile.is_private,
                    'is_verified': profile.is_verified,
                    'is_business_account': profile.is_business_account,
                    'business_category_name': profile.business_category_name,
                    'profile_pic_url': profile.profile_pic_url,
                },
                'advanced_metrics': {
                    'engagement_rate': self.calculate_engagement_rate(profile),
                    'posting_frequency': self.analyze_posting_pattern(profile),
                    'account_age_estimate': self.estimate_account_age(profile),
                },
                'recent_activity': self.get_recent_activity(profile, limit=5)
            }
            
            print(f"✅ Profile extracted: {username}")
            print(f"   👥 Followers: {profile.followers:,}")
            print(f"   📷 Posts: {profile.mediacount:,}")
            print(f"   🔒 Private: {profile.is_private}")
            
            return profile_data
            
        except Exception as e:
            print(f"❌ Profile extraction failed for {username}: {e}")
            return None
    
    def calculate_engagement_rate(self, profile):
        """คำนวณ engagement rate"""
        try:
            if profile.mediacount == 0 or profile.followers == 0:
                return 0
            
            # Sample recent posts for engagement calculation
            recent_posts = list(profile.get_posts())[:10]  # Get last 10 posts
            
            total_engagement = 0
            for post in recent_posts:
                engagement = post.likes + post.comments
                total_engagement += engagement
            
            avg_engagement = total_engagement / len(recent_posts)
            engagement_rate = (avg_engagement / profile.followers) * 100
            
            return round(engagement_rate, 2)
            
        except Exception as e:
            print(f"⚠️ Engagement calculation error: {e}")
            return 0
    
    def analyze_posting_pattern(self, profile):
        """วิเคราะห์ pattern การโพสต์"""
        try:
            posts = list(profile.get_posts())[:20]  # Analyze last 20 posts
            
            if len(posts) < 2:
                return "Insufficient data"
            
            # คำนวณ average time between posts
            time_diffs = []
            for i in range(1, len(posts)):
                diff = posts[i-1].date - posts[i].date
                time_diffs.append(diff.days)
            
            avg_days = sum(time_diffs) / len(time_diffs)
            
            if avg_days < 1:
                return "Daily poster"
            elif avg_days < 7:
                return f"Regular ({avg_days:.1f} days avg)"
            else:
                return f"Infrequent ({avg_days:.1f} days avg)"
                
        except Exception as e:
            print(f"⚠️ Posting pattern analysis error: {e}")
            return "Analysis failed"
    
    def estimate_account_age(self, profile):
        """ประมาณอายุของ account"""
        try:
            posts = list(profile.get_posts())
            
            if not posts:
                return "No posts available"
            
            # หาโพสต์เก่าสุด
            oldest_post = min(posts, key=lambda x: x.date)
            account_age = datetime.now() - oldest_post.date.replace(tzinfo=None)
            
            years = account_age.days // 365
            months = (account_age.days % 365) // 30
            
            if years > 0:
                return f"~{years} years {months} months"
            else:
                return f"~{months} months"
                
        except Exception as e:
            print(f"⚠️ Account age estimation error: {e}")
            return "Estimation failed"
    
    def get_recent_activity(self, profile, limit=5):
        """ดึงกิจกรรมล่าสุด"""
        try:
            posts = list(profile.get_posts())[:limit]
            
            activity = []
            for post in posts:
                activity.append({
                    'date': post.date.isoformat(),
                    'type': 'video' if post.is_video else 'photo',
                    'caption': post.caption[:100] + '...' if post.caption and len(post.caption) > 100 else post.caption,
                    'likes': post.likes,
                    'comments': post.comments,
                    'url': f"https://www.instagram.com/p/{post.shortcode}/"
                })
            
            return activity
            
        except Exception as e:
            print(f"⚠️ Recent activity error: {e}")
            return []
    
    def run_advanced_extraction(self):
        """รันการดึงข้อมูลแบบขั้นสูง"""
        print("🔥 ADVANCED INSTALOADER STEALTH EXTRACTOR")
        print("=" * 60)
        
        # Try to load existing session
        session_loaded = self.load_existing_session()
        
        if session_loaded:
            print("✅ Using existing session")
        else:
            print("⚠️ No session - extracting public data only")
        
        # Extract data for each target
        for username in self.targets:
            print(f"\n🎯 Processing: {username}")
            
            # Random delay for stealth
            delay = random.uniform(8, 15)
            print(f"⏰ Stealth delay: {delay:.1f}s")
            time.sleep(delay)
            
            # Extract profile data
            profile_data = self.extract_profile_advanced(username)
            
            if profile_data:
                self.results['accounts'][username] = profile_data
                print(f"✅ Successfully extracted: {username}")
            else:
                print(f"❌ Failed to extract: {username}")
        
        # Save results
        self.save_results()
        
        print("\n🎉 Advanced extraction completed!")
        return self.results
    
    def save_results(self):
        """บันทึกผลลัพธ์"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"/workspaces/sugarglitch-realops/results/advanced_instaloader_results_{timestamp}.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved: {filename}")

if __name__ == "__main__":
    extractor = AdvancedStealthExtractor()
    results = extractor.run_advanced_extraction()
    
    # Print summary
    print("\n📊 EXTRACTION SUMMARY")
    print("=" * 40)
    for username, data in results['accounts'].items():
        if data:
            basic = data['basic_info']
            print(f"👤 {username}:")
            print(f"   📱 Full name: {basic['full_name']}")
            print(f"   👥 Followers: {basic['followers']:,}")
            print(f"   📷 Posts: {basic['mediacount']:,}")
            print(f"   🔒 Private: {basic['is_private']}")
            if 'engagement_rate' in data['advanced_metrics']:
                print(f"   📈 Engagement: {data['advanced_metrics']['engagement_rate']}%")
