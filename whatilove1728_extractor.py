#!/usr/bin/env python3
"""
🔥 REAL INSTAGRAM EXTRACTOR 🔥
Target: whatilove1728
Purpose: Extract real data from personal Instagram account
"""

import json
import requests
import os
import time
import random
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
import re
from fake_useragent import UserAgent


class RealInstagramExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.target_username = "whatilove1728"
        self.output_folder = "/workspaces/sugarglitch-realops/real_extracted_data"
        self.session_data = None
        self.ua = UserAgent()
        
        # สร้าง output folder
        Path(self.output_folder).mkdir(exist_ok=True)
        
        # โหลด session data
        self.load_session_data()
        
        # ตั้งค่า session
        self.setup_session()
    
    def load_session_data(self):
        """โหลด session data จริง"""
        session_files = [
            "./extracted_project/Python/alx_trading_complete_package_20250525_231905/session.json",
            "./extracted_project/Python/PRIVATE_BYPASS_SUCCESS_whatilove1728_20250525_234142.json"
        ]
        
        for file in session_files:
            if os.path.exists(file):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                    
                    if 'sessionid' in data:
                        self.session_data = data
                        print(f"✅ Loaded session from: {file}")
                        break
                        
                except Exception as e:
                    print(f"❌ Error loading {file}: {e}")
        
        if not self.session_data:
            print("❌ No valid session data found!")
            return False
        
        return True
    
    def setup_session(self):
        }

        try:
            response = requests.get(self.api_url, headers=headers)
            response.raise_for_status()
            print("✅ Data fetched successfully.")
            return response.json()
        except requests.RequestException as e:
            print(f"❌ Failed to fetch data: {e}")
            return None

    def extract(self):
        """
        Main extraction logic.
        """
        data = self.fetch_data()
        if data:
            # Process and extract the required information
            print("🔄 Processing data...")
            # Example: Print the data (replace with actual processing logic)
            print(json.dumps(data, indent=4))
        else:
            print("❌ No data to process.")
    
    def setup_session(self):
        """ตั้งค่า session สำหรับ Instagram"""
        if not self.session_data:
            return
        
        # Cookies
        cookies = {
            'sessionid': self.session_data.get('sessionid', ''),
            'ds_user_id': self.session_data.get('ds_user_id', ''),
            'mid': 'aDM32wALAAHsm3VMVlb-YBH1iciS',
            'ig_did': 'A702C7AD-4B55-461A-9B0A-54D11694E0D7',
            'csrftoken': 'missing'
        }
        
        self.session.cookies.update(cookies)
        
        # Headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        self.session.headers.update(headers)
        print("🔧 Session configured with real cookies")
    
    def human_delay(self, min_delay=1, max_delay=3):
        """Human-like delay"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def extract_profile_data(self):
        """ดึงข้อมูล profile จริง"""
        print(f"🎯 Extracting profile data for: {self.target_username}")
        
        url = f"https://www.instagram.com/{self.target_username}/"
        
        try:
            response = self.session.get(url, timeout=30, allow_redirects=False)
            
            print(f"📊 Response Status: {response.status_code}")
            print(f"📏 Content Length: {len(response.text)} chars")
            
            if response.status_code == 200:
                # บันทึก raw HTML
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                html_file = f"{self.output_folder}/profile_raw_{timestamp}.html"
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                print(f"💾 Saved raw HTML: {html_file}")
                
                # แยกข้อมูล JSON
                json_data = self.extract_json_from_html(response.text)
                
                if json_data:
                    json_file = f"{self.output_folder}/profile_data_{timestamp}.json"
                    with open(json_file, 'w', encoding='utf-8') as f:
                        json.dump(json_data, f, indent=2, ensure_ascii=False)
                    
                    print(f"💾 Saved JSON data: {json_file}")
                    return json_data
                
            elif response.status_code == 302:
                print("⚠️ Redirect detected - possible login required")
                print(f"🔗 Redirect to: {response.headers.get('Location', 'Unknown')}")
                
            else:
                print(f"❌ Request failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        return None
    
    def extract_json_from_html(self, html_content):
        """แยก JSON data จาก HTML"""
        patterns = [
            r'window\._sharedData\s*=\s*({.*?});',
            r'window\.__additionalDataLoaded\([^,]+,({.*?})\);',
            r'{"config":.*?"profilePage_.*?".*?}',
        ]
        
        extracted_data = {}
        
        for i, pattern in enumerate(patterns):
            matches = re.findall(pattern, html_content, re.DOTALL)
            if matches:
                for j, match in enumerate(matches):
                    try:
                        data = json.loads(match)
                        extracted_data[f'pattern_{i}_match_{j}'] = data
                        print(f"✅ Extracted JSON pattern {i}, match {j}")
                    except:
                        print(f"❌ Failed to parse JSON pattern {i}, match {j}")
        
        return extracted_data if extracted_data else None

    def run_full_extraction(self):
        """รันการดึงข้อมูลแบบครบถ้วน"""
        print("🚀 STARTING REAL INSTAGRAM EXTRACTION")
        print("=" * 50)
        print(f"🎯 Target: {self.target_username}")
        print(f"📁 Output: {self.output_folder}")
        print()
        
        if not self.session_data:
            print("❌ No session data available!")
            return
        
        # ขั้นตอน 1: ดึงข้อมูล profile
        print("📊 Step 1: Profile data extraction...")
        profile_data = self.extract_profile_data()
        
        if profile_data:
            print("✅ Profile extraction successful!")
        else:
            print("❌ Profile extraction failed!")
        
        # สรุปผล
        print()
        print("✅ EXTRACTION COMPLETED!")
        print("=" * 30)
        print(f"📊 Profile data: {'✅' if profile_data else '❌'}")
        print(f"📁 Output folder: {self.output_folder}")

def main():
    print("🔥💀 REAL INSTAGRAM EXTRACTOR 💀🔥")
    print("Target: whatilove1728")
    print("Mode: REAL DATA EXTRACTION")
    print()
    
    extractor = RealInstagramExtractor()
    extractor.run_full_extraction()

if __name__ == "__main__":
    main()