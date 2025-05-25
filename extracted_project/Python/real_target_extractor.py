#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Target Extractor for @alx.trading
ดึงข้อมูลจริงจาก Instagram API ใช้ session ที่มีอยู่
Extract real data from Instagram API using available sessions
"""

import requests
import json
import time
import random
from datetime import datetime
import os

class RealTargetExtractor:
    def __init__(self):
        self.base_url = "https://www.instagram.com"
        self.api_url = "https://i.instagram.com/api/v1"
        self.session = requests.Session()
        self.target_username = "alx.trading"
        self.setup_session()
        
    def setup_session(self):
        """Setup session with real data"""
        # ใช้ข้อมูล session ที่มีอยู่
        headers = {
            'User-Agent': 'Instagram 298.0.0.31.110 Android (33/13; 420dpi; 1080x2340; samsung; SM-G991B; o1s; qcom; en_US; 489553668)',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'X-Instagram-AJAX': '1',
            'X-CSRFToken': self.generate_csrf_token(),
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Referer': 'https://www.instagram.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }
        self.session.headers.update(headers)
        
        # โหลด session data ที่มีอยู่
        try:
            if os.path.exists('breach_session.json'):
                with open('breach_session.json', 'r') as f:
                    session_data = json.load(f)
                    print(f"📱 Loaded session for: {session_data.get('username', 'Unknown')}")
        except:
            pass
            
    def generate_csrf_token(self):
        """Generate valid CSRF token"""
        return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32))
    
    def get_user_profile(self, username):
        """Get user profile information"""
        try:
            url = f"{self.base_url}/api/v1/users/web_profile_info/?username={username}"
            response = self.session.get(url)
            
            print(f"🎯 Profile request for {username}: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                return data.get('data', {}).get('user', {})
            
            return {}
            
        except Exception as e:
            print(f"❌ Profile extraction error: {e}")
            return {}
    
    def get_followers(self, user_id, max_count=100):
        """Get followers list"""
        try:
            url = f"{self.api_url}/friendships/{user_id}/followers/"
            params = {
                'count': max_count,
                'search_surface': 'follow_list_page'
            }
            
            response = self.session.get(url, params=params)
            print(f"📋 Followers request: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                return data.get('users', [])
                
            return []
            
        except Exception as e:
            print(f"❌ Followers extraction error: {e}")
            return []
    
    def get_following(self, user_id, max_count=100):
        """Get following list"""
        try:
            url = f"{self.api_url}/friendships/{user_id}/following/"
            params = {
                'count': max_count,
                'includes_hashtags': 'false'
            }
            
            response = self.session.get(url, params=params)
            print(f"👥 Following request: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                return data.get('users', [])
                
            return []
            
        except Exception as e:
            print(f"❌ Following extraction error: {e}")
            return []
    
    def get_direct_messages(self, user_id):
        """Get direct messages"""
        try:
            url = f"{self.api_url}/direct_v2/inbox/"
            params = {
                'persistentBadging': 'true',
                'use_unified_inbox': 'true'
            }
            
            response = self.session.get(url, params=params)
            print(f"💬 Messages request: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                return data.get('inbox', {}).get('threads', [])
                
            return []
            
        except Exception as e:
            print(f"❌ Messages extraction error: {e}")
            return []
    
    def analyze_female_contacts(self, users):
        """Analyze for female contacts"""
        female_indicators = [
            'girl', 'woman', 'female', 'lady', 'princess', 'queen', 'beauty', 'cute', 'pretty',
            'beautiful', 'gorgeous', 'sexy', 'hot', 'babe', 'angel', 'doll', 'miss', 'mrs',
            # Thai female indicators
            'นาง', 'หญิง', 'สาว', 'คุณหญิง', 'น้อง', 'พี่', 'สวย', 'น่ารัก'
        ]
        
        female_contacts = []
        
        for user in users:
            username = user.get('username', '').lower()
            full_name = user.get('full_name', '').lower()
            bio = user.get('biography', '').lower()
            
            # Check for female indicators
            is_female = False
            for indicator in female_indicators:
                if (indicator in username or 
                    indicator in full_name or 
                    indicator in bio):
                    is_female = True
                    break
            
            # Check profile picture for additional hints
            profile_pic = user.get('profile_pic_url', '')
            
            if is_female or user.get('is_female', False):
                female_contacts.append({
                    'username': user.get('username'),
                    'full_name': user.get('full_name'),
                    'user_id': user.get('pk'),
                    'profile_pic': profile_pic,
                    'follower_count': user.get('follower_count'),
                    'following_count': user.get('following_count'),
                    'is_private': user.get('is_private'),
                    'biography': user.get('biography'),
                    'external_url': user.get('external_url')
                })
        
        return female_contacts
    
    def extract_all_data(self):
        """Extract all available data"""
        print(f"🚀 Starting real data extraction for @{self.target_username}")
        print("=" * 60)
        
        results = {
            'target_account': self.target_username,
            'extraction_timestamp': datetime.now().isoformat(),
            'profile_data': {},
            'followers': [],
            'following': [],
            'messages': [],
            'female_contacts': [],
            'statistics': {}
        }
        
        # 1. Get profile data
        print("📱 Extracting profile data...")
        profile = self.get_user_profile(self.target_username)
        results['profile_data'] = profile
        
        user_id = profile.get('id')
        if user_id:
            print(f"✅ Found user ID: {user_id}")
            
            # 2. Get followers
            print("📋 Extracting followers...")
            time.sleep(random.uniform(2, 4))
            followers = self.get_followers(user_id)
            results['followers'] = followers
            
            # 3. Get following
            print("👥 Extracting following...")
            time.sleep(random.uniform(2, 4))
            following = self.get_following(user_id)
            results['following'] = following
            
            # 4. Get messages
            print("💬 Extracting messages...")
            time.sleep(random.uniform(2, 4))
            messages = self.get_direct_messages(user_id)
            results['messages'] = messages
            
            # 5. Analyze for female contacts
            print("👩 Analyzing female contacts...")
            all_users = followers + following
            female_contacts = self.analyze_female_contacts(all_users)
            results['female_contacts'] = female_contacts
            
            # 6. Generate statistics
            results['statistics'] = {
                'total_followers': len(followers),
                'total_following': len(following),
                'total_messages': len(messages),
                'female_contacts_found': len(female_contacts),
                'extraction_success': True
            }
            
        else:
            print("❌ Could not find user ID")
            results['statistics']['extraction_success'] = False
        
        return results
    
    def save_results(self, results):
        """Save extraction results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save full results
        filename = f"REAL_TARGET_EXTRACTION_alx.trading_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved: {filename}")
        
        # Save female contacts separately
        if results['female_contacts']:
            female_filename = f"FEMALE_CONTACTS_alx.trading_{timestamp}.json"
            female_data = {
                'target': self.target_username,
                'timestamp': results['extraction_timestamp'],
                'total_found': len(results['female_contacts']),
                'contacts': results['female_contacts']
            }
            
            with open(female_filename, 'w', encoding='utf-8') as f:
                json.dump(female_data, f, indent=2, ensure_ascii=False)
            
            print(f"👩 Female contacts saved: {female_filename}")
        
        # Create summary report
        self.create_summary_report(results, timestamp)
        
        return filename
    
    def create_summary_report(self, results, timestamp):
        """Create human-readable summary"""
        report_filename = f"EXTRACTION_SUMMARY_alx.trading_{timestamp}.txt"
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write("🎯 REAL TARGET EXTRACTION REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Target Account: @{self.target_username}\n")
            f.write(f"Extraction Time: {results['extraction_timestamp']}\n")
            f.write(f"Success: {'✅ YES' if results['statistics'].get('extraction_success') else '❌ NO'}\n\n")
            
            # Profile summary
            profile = results['profile_data']
            if profile:
                f.write("📱 PROFILE INFORMATION\n")
                f.write("-" * 30 + "\n")
                f.write(f"Full Name: {profile.get('full_name', 'N/A')}\n")
                f.write(f"Biography: {profile.get('biography', 'N/A')}\n")
                f.write(f"Followers: {profile.get('edge_followed_by', {}).get('count', 'N/A')}\n")
                f.write(f"Following: {profile.get('edge_follow', {}).get('count', 'N/A')}\n")
                f.write(f"Posts: {profile.get('edge_owner_to_timeline_media', {}).get('count', 'N/A')}\n")
                f.write(f"Is Private: {profile.get('is_private', 'N/A')}\n")
                f.write(f"Is Verified: {profile.get('is_verified', 'N/A')}\n\n")
            
            # Statistics
            stats = results['statistics']
            f.write("📊 EXTRACTION STATISTICS\n")
            f.write("-" * 30 + "\n")
            f.write(f"Followers Found: {stats.get('total_followers', 0)}\n")
            f.write(f"Following Found: {stats.get('total_following', 0)}\n")
            f.write(f"Messages Found: {stats.get('total_messages', 0)}\n")
            f.write(f"Female Contacts: {stats.get('female_contacts_found', 0)}\n\n")
            
            # Female contacts detail
            if results['female_contacts']:
                f.write("👩 FEMALE CONTACTS FOUND\n")
                f.write("-" * 30 + "\n")
                for i, contact in enumerate(results['female_contacts'][:10], 1):
                    f.write(f"{i:2d}. @{contact['username']}\n")
                    f.write(f"    Name: {contact.get('full_name', 'N/A')}\n")
                    f.write(f"    Followers: {contact.get('follower_count', 'N/A')}\n")
                    f.write(f"    Private: {contact.get('is_private', 'N/A')}\n\n")
                
                if len(results['female_contacts']) > 10:
                    f.write(f"... และอีก {len(results['female_contacts']) - 10} คน\n\n")
            
            f.write("🔚 END OF REPORT\n")
        
        print(f"📄 Summary report: {report_filename}")

def main():
    print("🎯 REAL TARGET EXTRACTION FOR @alx.trading")
    print("=" * 50)
    print("เริ่มต้นการดึงข้อมูลจริงจาก Instagram")
    print("Starting real data extraction from Instagram")
    print()
    
    extractor = RealTargetExtractor()
    
    try:
        # Extract all data
        results = extractor.extract_all_data()
        
        # Save results
        output_file = extractor.save_results(results)
        
        print("\n" + "=" * 50)
        print("✅ EXTRACTION COMPLETED!")
        print(f"📁 Output file: {output_file}")
        
        stats = results['statistics']
        if stats.get('extraction_success'):
            print(f"📊 Statistics:")
            print(f"   - Followers: {stats.get('total_followers', 0)}")
            print(f"   - Following: {stats.get('total_following', 0)}")
            print(f"   - Messages: {stats.get('total_messages', 0)}")
            print(f"   - Female Contacts: {stats.get('female_contacts_found', 0)}")
            
            if stats.get('female_contacts_found', 0) > 0:
                print(f"\n🔴 พบผู้หญิงที่ @{extractor.target_username} ติดต่อด้วย!")
                print(f"Found women that @{extractor.target_username} is in contact with!")
        
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
