#!/usr/bin/env python3
"""
🔥 SUGARGLITCH REALOPS - FRESH SESSION EXTRACTOR ALX 🔥
ดึงข้อมูล Instagram DMs จริงด้วย Fresh Stealth Bypass Session
🚫 NO SIMULATION - REAL DATA WITH VALID SESSION
"""

import requests
import json
import time
import random
from datetime import datetime
import os
from urllib.parse import quote_plus
import base64

class FreshSessionExtractor:
    def __init__(self):
        self.session_data = None
        self.base_url = "https://www.instagram.com"
        
        print("🔥 SUGARGLITCH REALOPS - FRESH SESSION EXTRACTOR ALX 🔥")
        print("ดึงข้อมูล Instagram DMs จริงด้วย Fresh Stealth Bypass Session")
        print("🚫 NO SIMULATION - REAL DATA WITH VALID SESSION")
        
    def load_fresh_session(self):
        """โหลด fresh stealth bypass session"""
        try:
            with open('fresh_stealth_session.json', 'r') as f:
                self.session_data = json.load(f)
            
            print(f"✅ Loaded fresh session for user: {self.session_data['user']}")
            print(f"🔑 Session ID: {self.session_data['sessionid'][:20]}...")
            print(f"👤 User ID: {self.session_data['ds_user_id']}")
            print(f"🔄 Source: {self.session_data['source']}")
            print(f"✓ Valid: {self.session_data['valid']}")
            return True
        except Exception as e:
            print(f"❌ Failed to load fresh session: {e}")
            return False
    
    def get_advanced_headers(self):
        """สร้าง advanced headers สำหรับ fresh session"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Instagram-AJAX': '1010566531',
            'X-IG-App-ID': '936619743392459',
            'X-ASBD-ID': '129477',
            'X-IG-WWW-Claim': '0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/direct/inbox/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Ch-Ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?1',
            'Sec-Ch-Ua-Platform': '"iOS"',
        }
        
        # Build cookie string with fresh session
        cookies = [
            f"sessionid={self.session_data['sessionid']}",
            f"ds_user_id={self.session_data['ds_user_id']}",
            "ig_did=B8F4A4A0-8E3D-4B7A-9C2D-1F6E5A3B7C9D",
            "ig_nrcb=1",
            "mid=ZF8sIAALAAF7U6Kt7-8h_z_4K8z1",
            "fbm_124024574287414=base_domain=.instagram.com",
            "shbid=\"12025\\05444976283726\\0541748270421:01f7f:85e7c8b9f5d4a3c2d1e0f6b8a7c9e5f3d2a1b0c8\"",
            "shbts=\"1716870421\\05444976283726\\0541748270421:01f7f:85e7c8b9f5d4a3c2d1e0f6b8a7c9e5f3d2a1b0c8\"",
            "rur=\"VLL\\05444976283726\\0541748270421:01f7f:85e7c8b9f5d4a3c2d1e0f6b8a7c9e5f3d2a1b0c8\""
        ]
        
        headers['Cookie'] = '; '.join(cookies)
        return headers
    
    def test_session_validity(self):
        """ทดสอบ fresh session validity"""
        print(f"\n🧪 Testing fresh session validity...")
        
        headers = self.get_advanced_headers()
        
        # Test with multiple endpoints
        test_endpoints = [
            ('Account Info', f"{self.base_url}/accounts/edit/"),
            ('Current User', f"{self.base_url}/api/v1/users/{self.session_data['ds_user_id']}/info/"),
            ('Timeline', f"{self.base_url}/api/v1/feed/timeline/"),
            ('Direct Inbox', f"{self.base_url}/api/v1/direct_v2/inbox/")
        ]
        
        valid_endpoints = []
        
        for name, url in test_endpoints:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                print(f"🔍 {name}: HTTP {response.status_code}")
                
                if response.status_code == 200:
                    valid_endpoints.append(name)
                    print(f"✅ {name} - Session Valid!")
                else:
                    print(f"❌ {name} - HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {name} - Error: {e}")
            
            time.sleep(random.uniform(0.5, 1.5))
        
        if valid_endpoints:
            print(f"\n✅ Session validation successful! Valid endpoints: {valid_endpoints}")
            return True
        else:
            print(f"\n❌ Session validation failed on all endpoints")
            return False
    
    def extract_direct_messages(self):
        """ดึงข้อมูล Direct Messages จริง"""
        print(f"\n📥 กำลังดึงข้อมูล DMs จาก fresh session...")
        
        headers = self.get_advanced_headers()
        
        # Try multiple DM endpoints
        dm_endpoints = [
            f"{self.base_url}/api/v1/direct_v2/inbox/",
            f"{self.base_url}/api/v1/direct_v2/inbox/?visual_message_return_type=unseen",
            f"https://i.instagram.com/api/v1/direct_v2/inbox/",
            f"{self.base_url}/direct/inbox/"
        ]
        
        extracted_data = []
        
        for endpoint in dm_endpoints:
            print(f"🔗 Trying endpoint: {endpoint}")
            
            try:
                response = requests.get(endpoint, headers=headers, timeout=15)
                print(f"📊 Response: {response.status_code}")
                
                if response.status_code == 200:
                    print("✅ SUCCESS! Real data extracted!")
                    
                    # Try to parse as JSON
                    try:
                        data = response.json()
                        extracted_data.append({
                            'endpoint': endpoint,
                            'data': data,
                            'timestamp': datetime.now().isoformat()
                        })
                        
                        # Save raw response
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_file = f"data/extractions/fresh_session_dm_{timestamp}.json"
                        os.makedirs(os.path.dirname(output_file), exist_ok=True)
                        
                        with open(output_file, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        
                        print(f"💾 Real DM data saved: {output_file}")
                        
                        # Analyze extracted data
                        self.analyze_dm_data(data)
                        
                    except json.JSONDecodeError:
                        print("📄 Response is not JSON, saving as text")
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        text_file = f"data/extractions/fresh_session_response_{timestamp}.txt"
                        os.makedirs(os.path.dirname(text_file), exist_ok=True)
                        with open(text_file, 'w', encoding='utf-8') as f:
                            f.write(response.text)
                        print(f"💾 Response saved: {text_file}")
                
                else:
                    print(f"❌ HTTP Error: {response.status_code}")
                    print(f"Response snippet: {response.text[:200]}")
                    
            except Exception as e:
                print(f"❌ Request failed: {e}")
            
            # Random delay between requests
            time.sleep(random.uniform(1, 3))
        
        return extracted_data
    
    def analyze_dm_data(self, data):
        """วิเคราะห์ข้อมูล DM ที่ดึงมาได้"""
        print(f"\n📊 Analyzing extracted DM data...")
        
        if isinstance(data, dict):
            if 'inbox' in data:
                inbox = data['inbox']
                threads = inbox.get('threads', [])
                print(f"📨 Found {len(threads)} conversation threads")
                
                for i, thread in enumerate(threads[:5], 1):
                    thread_id = thread.get('thread_id', 'Unknown')
                    thread_title = thread.get('thread_title', 'No title')
                    user_count = len(thread.get('users', []))
                    
                    print(f"💬 Thread {i}: {thread_title} (ID: {thread_id}, Users: {user_count})")
                    
                    # Get recent messages
                    items = thread.get('items', [])
                    if items:
                        recent_msg = items[0]
                        msg_type = recent_msg.get('item_type', 'unknown')
                        timestamp = recent_msg.get('timestamp', 'unknown')
                        print(f"   📝 Recent message: {msg_type} at {timestamp}")
                        
                        # Check for media
                        if 'media' in recent_msg:
                            media = recent_msg['media']
                            media_type = media.get('media_type', 'unknown')
                            print(f"   🖼️ Contains media: {media_type}")
            
            elif 'viewer' in data:
                # GraphQL format
                viewer = data['viewer']
                if 'message_threads' in viewer:
                    edges = viewer['message_threads'].get('edges', [])
                    print(f"📨 Found {len(edges)} conversation threads (GraphQL)")
        
        else:
            print(f"📄 Data type: {type(data)}")
            print(f"📊 Data preview: {str(data)[:200]}")
    
    def run_extraction(self):
        """เริ่มต้น REAL extraction ด้วย fresh session"""
        print(f"\n🚀 เริ่มต้น FRESH SESSION REAL EXTRACTION")
        print("=" * 60)
        
        if not self.load_fresh_session():
            print("❌ Failed to load fresh session!")
            return False
        
        if not self.test_session_validity():
            print("❌ Fresh session validation failed!")
            return False
        
        print("✅ Fresh session validated! Proceeding with extraction...")
        
        extracted_data = self.extract_direct_messages()
        
        if extracted_data:
            print(f"\n🎉 REAL DATA EXTRACTION SUCCESSFUL!")
            print(f"📊 Extracted data from {len(extracted_data)} endpoints")
            
            # Generate summary report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = f"data/extractions/extraction_report_{timestamp}.json"
            os.makedirs(os.path.dirname(report_file), exist_ok=True)
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'session_info': self.session_data,
                    'extraction_timestamp': timestamp,
                    'extracted_endpoints': len(extracted_data),
                    'success': True,
                    'data_summary': extracted_data
                }, f, indent=2, ensure_ascii=False)
            
            print(f"📄 Extraction report saved: {report_file}")
            return True
        else:
            print(f"\n❌ EXTRACTION FAILED!")
            print("ไม่สามารถดึงข้อมูลจริงได้")
            return False

def main():
    print("\n🔥 FRESH SESSION REAL INSTAGRAM DM EXTRACTOR 🔥")
    print("🎯 Target: alx.trading")
    print("🔑 Using: Fresh Stealth Bypass Session")
    print("🚫 NO SIMULATION - REAL DATA EXTRACTION")
    print("🔒 Advanced Session Management")
    
    extractor = FreshSessionExtractor()
    success = extractor.run_extraction()
    
    if success:
        print("\n🎉 MISSION ACCOMPLISHED!")
        print("✅ Real Instagram DMs extracted successfully with fresh session")
        print("📁 Check data/extractions/ for output files")
    else:
        print("\n💥 MISSION FAILED!")
        print("❌ Unable to extract real data even with fresh session")

if __name__ == "__main__":
    main()
