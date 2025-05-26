#!/usr/bin/env python3
"""
🔥 REAL INSTAGRAM IMAGE EXTRACTOR 🔥
แก้ไขปัญหารูปภาพที่ไม่ใช่รูปจริง
ดึงรูปภาพจริงจากบัญชี Instagram
"""

import json
import requests
import os
import time
import random
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, urljoin
import re
from fake_useragent import UserAgent
import hashlib
from typing import List, Dict, Optional


class RealImageExtractor:
    def __init__(self, target_username: str = "whatilove1728"):
        self.session = requests.Session()
        self.target_username = target_username
        self.output_folder = f"/workspaces/sugarglitch-realops/{target_username}_real_images"
        self.session_data = None
        self.ua = UserAgent()
        
        # สร้าง output folders
        self.create_output_folders()
        
        # โหลด session data
        self.load_session_data()
        
        # ตั้งค่า session
        self.setup_session()
    
    def create_output_folders(self):
        """สร้างโฟลเดอร์สำหรับเก็บรูปภาพ"""
        folders = [
            f"{self.output_folder}/posts",
            f"{self.output_folder}/profile_pics", 
            f"{self.output_folder}/stories",
            f"{self.output_folder}/highlights",
            f"{self.output_folder}/thumbnails",
            f"{self.output_folder}/metadata"
        ]
        
        for folder in folders:
            Path(folder).mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Created output folders in: {self.output_folder}")
    
    def load_session_data(self):
        """โหลด session data จริง"""
        session_files = [
            "/workspaces/sugarglitch-realops/extracted_project/Python/success_whatilove1728_20250525_153247.json",
            "/workspaces/sugarglitch-realops/extracted_project/Python/PRIVATE_BYPASS_SUCCESS_whatilove1728_20250525_234142.json",
            "/workspaces/sugarglitch-realops/extracted_project/Python/alx_trading_complete_package_20250525_231905/session.json"
        ]
        
        for file in session_files:
            if os.path.exists(file):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                    
                    # ตรวจสอบว่ามี session data ที่ใช้การได้
                    if any(key in data for key in ['sessionid', 'cookies', 'session_data']):
                        self.session_data = data
                        print(f"✅ Loaded session from: {file}")
                        break
                        
                except Exception as e:
                    print(f"❌ Error loading {file}: {e}")
        
        if not self.session_data:
            print("⚠️ No session data found, will use basic headers")
    
    def setup_session(self):
        """ตั้งค่า session สำหรับ Instagram"""
        # Headers พื้นฐาน
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none'
        }
        
        self.session.headers.update(headers)
        
        # ตั้งค่า cookies ถ้ามี session data
        if self.session_data:
            if 'cookies' in self.session_data:
                for cookie in self.session_data['cookies']:
                    if isinstance(cookie, dict) and 'name' in cookie and 'value' in cookie:
                        self.session.cookies.set(cookie['name'], cookie['value'])
            
            # Session ID specific
            if 'sessionid' in self.session_data:
                self.session.cookies.set('sessionid', self.session_data['sessionid'])
        
        print("🔧 Session configured for image extraction")
    
    def human_delay(self, min_delay=2, max_delay=5):
        """Human-like delay"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def download_image(self, url: str, filename: str, folder: str) -> bool:
        """ดาวน์โหลดรูปภาพ"""
        try:
            # Add delay before each download
            self.human_delay(1, 3)
            
            headers = {
                'User-Agent': self.ua.random,
                'Referer': 'https://www.instagram.com/',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8'
            }
            
            response = self.session.get(url, headers=headers, timeout=30, stream=True)
            response.raise_for_status()
            
            # ตรวจสอบ content type
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                print(f"⚠️ Not an image: {url} (content-type: {content_type})")
                return False
            
            # สร้างชื่อไฟล์
            file_path = os.path.join(folder, filename)
            
            # ดาวน์โหลด
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            file_size = os.path.getsize(file_path)
            print(f"✅ Downloaded: {filename} ({file_size} bytes)")
            return True
            
        except Exception as e:
            print(f"❌ Failed to download {url}: {e}")
            return False
    
    def extract_images_from_profile_page(self) -> List[str]:
        """ดึงลิงก์รูปภาพจากหน้า profile"""
        url = f"https://www.instagram.com/{self.target_username}/"
        image_urls = []
        
        try:
            print(f"🔍 Fetching profile page: {url}")
            response = self.session.get(url, timeout=30)
            
            if response.status_code != 200:
                print(f"❌ Failed to fetch profile page: {response.status_code}")
                return []
            
            html_content = response.text
            
            # บันทึก HTML สำหรับ debug
            with open(f"{self.output_folder}/metadata/profile_page.html", 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # หา JSON data ที่ฝังอยู่ใน HTML
            json_patterns = [
                r'window\._sharedData\s*=\s*({.*?});',
                r'window\.__additionalDataLoaded\([^,]+,({.*?})\);',
            ]
            
            for pattern in json_patterns:
                matches = re.findall(pattern, html_content, re.DOTALL)
                for match in matches:
                    try:
                        data = json.loads(match)
                        urls = self.extract_urls_from_json(data)
                        image_urls.extend(urls)
                    except:
                        continue
            
            # หารูปภาพจาก HTML tags
            img_patterns = [
                r'<img[^>]+src="([^"]+)"[^>]*>',
                r'src="([^"]*\.(?:jpg|jpeg|png|webp)[^"]*)"',
                r'"display_url":"([^"]+)"',
                r'"profile_pic_url[^"]*":"([^"]+)"',
            ]
            
            for pattern in img_patterns:
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                for match in matches:
                    if self.is_valid_instagram_image_url(match):
                        image_urls.append(match)
            
            # ลบ duplicates
            image_urls = list(set(image_urls))
            print(f"🎯 Found {len(image_urls)} image URLs")
            
            return image_urls
            
        except Exception as e:
            print(f"❌ Error extracting from profile page: {e}")
            return []
    
    def extract_urls_from_json(self, data: dict) -> List[str]:
        """ดึง URLs จาก JSON data"""
        urls = []
        
        def recursive_search(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key in ['display_url', 'profile_pic_url', 'src', 'url'] and isinstance(value, str):
                        if self.is_valid_instagram_image_url(value):
                            urls.append(value)
                    else:
                        recursive_search(value)
            elif isinstance(obj, list):
                for item in obj:
                    recursive_search(item)
        
        recursive_search(data)
        return urls
    
    def is_valid_instagram_image_url(self, url: str) -> bool:
        """ตรวจสอบว่า URL เป็นรูปภาพ Instagram หรือไม่"""
        if not url or not isinstance(url, str):
            return False
        
        # ต้องเป็น https
        if not url.startswith('https://'):
            return False
        
        # ต้องเป็น domain ของ Instagram
        valid_domains = [
            'instagram.com',
            'cdninstagram.com', 
            'fbcdn.net',
            'scontent-',
            'scontent.cdninstagram.com'
        ]
        
        if not any(domain in url for domain in valid_domains):
            return False
        
        # ต้องมี extension ของรูปภาพ
        image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        if not any(ext in url.lower() for ext in image_extensions):
            return False
        
        # ไม่เอา static assets
        exclude_patterns = [
            '/static/',
            '/rsrc.php',
            'instagram-logo',
            'favicon',
            'sprite'
        ]
        
        if any(pattern in url.lower() for pattern in exclude_patterns):
            return False
        
        return True
    
    def generate_filename(self, url: str, index: int) -> str:
        """สร้างชื่อไฟล์"""
        # ใช้ hash ของ URL เป็นส่วนหนึ่งของชื่อไฟล์
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        
        # ดึง extension จาก URL
        extension = '.jpg'  # default
        if '.png' in url.lower():
            extension = '.png'
        elif '.webp' in url.lower():
            extension = '.webp'
        elif '.jpeg' in url.lower():
            extension = '.jpeg'
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{self.target_username}_{timestamp}_{index:03d}_{url_hash}{extension}"
    
    def run_extraction(self) -> Dict:
        """รันการดึงรูปภาพจริง"""
        print("🚀 STARTING REAL IMAGE EXTRACTION")
        print("=" * 50)
        print(f"🎯 Target: {self.target_username}")
        print(f"📁 Output: {self.output_folder}")
        print()
        
        # ดึงลิงก์รูปภาพ
        print("🔍 Step 1: Extracting image URLs...")
        image_urls = self.extract_images_from_profile_page()
        
        if not image_urls:
            print("❌ No image URLs found!")
            return {'success': False, 'downloaded': 0}
        
        # จัดประเภทรูปภาพ
        profile_pics = []
        post_images = []
        other_images = []
        
        for url in image_urls:
            if 'profile_pic' in url.lower() or '/s150x150/' in url:
                profile_pics.append(url)
            elif any(x in url for x in ['/p/', '/media/', 'scontent']):
                post_images.append(url)
            else:
                other_images.append(url)
        
        print(f"📊 Found images:")
        print(f"   👤 Profile pics: {len(profile_pics)}")
        print(f"   📷 Post images: {len(post_images)}")
        print(f"   🖼️ Other images: {len(other_images)}")
        print()
        
        # ดาวน์โหลดรูปภาพ
        downloaded = 0
        
        print("📥 Step 2: Downloading images...")
        
        # Profile pictures
        for i, url in enumerate(profile_pics):
            filename = self.generate_filename(url, i)
            if self.download_image(url, filename, f"{self.output_folder}/profile_pics"):
                downloaded += 1
        
        # Post images  
        for i, url in enumerate(post_images):
            filename = self.generate_filename(url, i)
            if self.download_image(url, filename, f"{self.output_folder}/posts"):
                downloaded += 1
        
        # Other images
        for i, url in enumerate(other_images):
            filename = self.generate_filename(url, i)
            if self.download_image(url, filename, f"{self.output_folder}/thumbnails"):
                downloaded += 1
        
        # บันทึก metadata
        metadata = {
            'extraction_date': datetime.now().isoformat(),
            'target_username': self.target_username,
            'total_urls_found': len(image_urls),
            'images_downloaded': downloaded,
            'urls': image_urls
        }
        
        with open(f"{self.output_folder}/metadata/extraction_log.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # สรุปผล
        print()
        print("✅ REAL IMAGE EXTRACTION COMPLETED!")
        print("=" * 40)
        print(f"🎯 Target: {self.target_username}")
        print(f"🔍 URLs found: {len(image_urls)}")
        print(f"📥 Downloaded: {downloaded}")
        print(f"📁 Output folder: {self.output_folder}")
        
        if downloaded > 0:
            print("🎉 SUCCESS: Real images extracted!")
        else:
            print("⚠️ No images could be downloaded")
        
        return {
            'success': downloaded > 0,
            'downloaded': downloaded,
            'total_urls': len(image_urls),
            'output_folder': self.output_folder
        }


def main():
    print("🔥💀 REAL INSTAGRAM IMAGE EXTRACTOR 💀🔥")
    print("แก้ไขปัญหารูปภาพที่ไม่ใช่รูปจริง")
    print("=" * 50)
    
    extractor = RealImageExtractor("whatilove1728")
    result = extractor.run_extraction()
    
    if result['success']:
        print(f"\n🎉 Successfully extracted {result['downloaded']} real images!")
        print(f"📁 Check folder: {result['output_folder']}")
    else:
        print(f"\n❌ Failed to extract real images")


if __name__ == "__main__":
    main()
