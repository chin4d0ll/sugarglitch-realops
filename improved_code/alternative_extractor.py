from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
🔥 ALTERNATIVE IMAGE EXTRACTOR 🔥
ใช้วิธีอื่นในการดึงรูปภาพเมื่อ session หมดอายุ
"""

import json
import requests
import os
import time
import random
from datetime import datetime
from pathlib import Path
import re
from fake_useragent import UserAgent
import hashlib


class AlternativeImageExtractor:
    def __init__(self, target_username: str = "whatilove1728"):
        self.target_username = target_username
        self.output_folder = f"/workspaces/sugarglitch-realops/{target_username}_extracted_images"
        self.session = requests.Session()
        self.ua = UserAgent()
        
        # สร้าง output folders
        self.create_output_folders()
        
        # ตั้งค่า session แบบ stealth
        self.setup_stealth_session()
    
    def create_output_folders(self):
        """สร้างโฟลเดอร์สำหรับเก็บรูปภาพ"""
        folders = [
            f"{self.output_folder}/found_images",
            f"{self.output_folder}/cached_data",
            f"{self.output_folder}/metadata"
        ]
        
        for folder in folders:
            Path(folder).mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Created output folders in: {self.output_folder}")
    
    def setup_stealth_session(self):
        """ตั้งค่า session แบบ stealth"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1'
        }
        
        self.session.headers.update(headers)
        print("🔧 Stealth session configured")
    
    def search_cached_data(self) -> list:
        """ค้นหารูปภาพจากข้อมูลที่ cache ไว้แล้ว"""
        print("🔍 Searching cached data for images...")
        found_images = []
        
        # ค้นหาไฟล์ที่อาจมีรูปภาพ
        search_paths = [
            "/workspaces/sugarglitch-realops/extracted_project/Python/",
            "/workspaces/sugarglitch-realops/extracted_images/",
            "/workspaces/sugarglitch-realops/"
        ]
        
        for base_path in search_paths:
            if os.path.exists(base_path):
                for root, dirs, files in os.walk(base_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        
                        # ค้นหาไฟล์รูปภาพ
                        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
                            # ตรวจสอบว่าไม่ใช่ demo images
                            if not any(demo in file.lower() for demo in ['demo', 'test', 'sample']):
                                found_images.append({
                                    'type': 'cached_image',
                                    'path': file_path,
                                    'filename': file,
                                    'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0
                                })
                        
                        # ค้นหาไฟล์ JSON ที่อาจมี URLs
                        elif file.lower().endswith('.json') and self.target_username in file:
                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    data = json.load(f)
                                
                                urls = self.extract_image_urls_from_json(data)
                                for url in urls:
                                    found_images.append({
                                        'type': 'json_url',
                                        'url': url,
                                        'source_file': file_path
                                    })
                            except:
                                continue
                        
                        # ค้นหาไฟล์ HTML
                        elif file.lower().endswith('.html') and self.target_username in file:
                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    html_content = f.read()
                                
                                urls = self.extract_image_urls_from_html(html_content)
                                for url in urls:
                                    found_images.append({
                                        'type': 'html_url',
                                        'url': url,
                                        'source_file': file_path
                                    })
                            except:
                                continue
        
        print(f"🎯 Found {len(found_images)} potential images/URLs")
        return found_images
    
    def extract_image_urls_from_json(self, data) -> list:
        """ดึง image URLs จาก JSON"""
        urls = []
        
        def search_recursive(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key in ['url', 'src', 'display_url', 'profile_pic_url', 'thumbnail_url']:
                        if isinstance(value, str) and self.is_valid_image_url(value):
                            urls.append(value)
                    else:
                        search_recursive(value)
            elif isinstance(obj, list):
                for item in obj:
                    search_recursive(item)
            elif isinstance(obj, str):
                # ค้นหา URLs ใน strings
                url_pattern = r'https?://[^\s<>"\']+\.(?:jpg|jpeg|png|webp|gif)'
                matches = re.findall(url_pattern, obj, re.IGNORECASE)
                for match in matches:
                    if self.is_valid_image_url(match):
                        urls.append(match)
        
        search_recursive(data)
        return list(set(urls))  # Remove duplicates
    
    def extract_image_urls_from_html(self, html_content: str) -> list:
        """ดึง image URLs จาก HTML"""
        urls = []
        
        # Patterns สำหรับค้นหา image URLs
        patterns = [
            r'<img[^>]+src="([^"]+)"',
            r'src="([^"]*\.(?:jpg|jpeg|png|webp|gif)[^"]*)"',
            r'"display_url":"([^"]+)"',
            r'"profile_pic_url[^"]*":"([^"]+)"',
            r'https://[^\s<>"\']+\.(?:jpg|jpeg|png|webp|gif)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                if self.is_valid_image_url(match):
                    urls.append(match)
        
        return list(set(urls))
    
    def is_valid_image_url(self, url: str) -> bool:
        """ตรวจสอบว่า URL เป็นรูปภาพที่ถูกต้องหรือไม่"""
        if not url or not isinstance(url, str):
            return False
        
        # ต้องเป็น https
        if not url.startswith('https://'):
            return False
        
        # ต้องมี image extension
        if not re.search(r'\.(jpg|jpeg|png|webp|gif)', url.lower()):
            return False
        
        # ไม่เอา static assets หรือ icons
        exclude_patterns = [
            'favicon',
            'sprite',
            'logo',
            'icon',
            '/static/',
            'data:image'
        ]
        
        for pattern in exclude_patterns:
            if pattern in url.lower():
                return False
        
        return True
    
    def download_image_from_url(self, url: str, index: int) -> bool:
        """ดาวน์โหลดรูปภาพจาก URL"""
        try:
            # Human-like delay
            time.sleep(random.uniform(1, 3))
            
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
                print(f"⚠️ Not an image: {url}")
                return False
            
            # สร้างชื่อไฟล์
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            extension = '.jpg'
            
            for ext in ['.png', '.webp', '.jpeg', '.gif']:
                if ext in url.lower():
                    extension = ext
                    break
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.target_username}_extracted_{timestamp}_{index:03d}_{url_hash}{extension}"
            file_path = f"{self.output_folder}/found_images/{filename}"
            
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
    
    def copy_cached_image(self, source_path: str, index: int) -> bool:
        """คัดลอกรูปภาพจาก cache"""
        try:
            if not os.path.exists(source_path):
                return False
            
            # สร้างชื่อไฟล์ใหม่
            original_name = os.path.basename(source_path)
            name, ext = os.path.splitext(original_name)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"{self.target_username}_cached_{timestamp}_{index:03d}_{name}{ext}"
            new_path = f"{self.output_folder}/found_images/{new_filename}"
            
            # คัดลอกไฟล์
            import shutil
            shutil.copy2(source_path, new_path)
            
            file_size = os.path.getsize(new_path)
            print(f"✅ Copied: {new_filename} ({file_size} bytes)")
            return True
            
        except Exception as e:
            print(f"❌ Failed to copy {source_path}: {e}")
            return False
    
    def run_alternative_extraction(self):
        """รันการดึงรูปภาพแบบทางเลือก"""
        print("🔥 ALTERNATIVE IMAGE EXTRACTION")
        print("=" * 40)
        print(f"🎯 Target: {self.target_username}")
        print(f"📁 Output: {self.output_folder}")
        print()
        
        # ค้นหาข้อมูลที่ cache ไว้
        found_items = self.search_cached_data()
        
        if not found_items:
            print("❌ No cached data found!")
            return
        
        # แยกประเภท
        cached_images = [item for item in found_items if item['type'] == 'cached_image']
        url_sources = [item for item in found_items if item['type'] in ['json_url', 'html_url']]
        
        print(f"📊 Analysis:")
        print(f"   🖼️ Cached images: {len(cached_images)}")
        print(f"   🔗 URLs found: {len(url_sources)}")
        print()
        
        downloaded = 0
        
        # คัดลอกรูปภาพที่มีอยู่แล้ว
        print("📥 Copying cached images...")
        for i, item in enumerate(cached_images):
            if self.copy_cached_image(item['path'], i):
                downloaded += 1
        
        # ดาวน์โหลดจาก URLs
        print("📥 Downloading from URLs...")
        unique_urls = list(set([item['url'] for item in url_sources]))
        
        for i, url in enumerate(unique_urls):
            if self.download_image_from_url(url, i + len(cached_images)):
                downloaded += 1
        
        # บันทึก metadata
        metadata = {
            'extraction_date': datetime.now().isoformat(),
            'target_username': self.target_username,
            'method': 'alternative_extraction',
            'cached_images_found': len(cached_images),
            'urls_found': len(unique_urls),
            'total_downloaded': downloaded,
            'source_details': found_items
        }
        
        with open(f"{self.output_folder}/metadata/alternative_extraction.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # สรุปผล
        print()
        print("✅ ALTERNATIVE EXTRACTION COMPLETED!")
        print("=" * 40)
        print(f"🎯 Target: {self.target_username}")
        print(f"🖼️ Cached images: {len(cached_images)}")
        print(f"🔗 URLs processed: {len(unique_urls)}")
        print(f"📥 Total extracted: {downloaded}")
        print(f"📁 Output folder: {self.output_folder}")
        
        if downloaded > 0:
            print("🎉 SUCCESS: Images extracted using alternative method!")
        else:
            print("⚠️ No images could be extracted")


@safe_execution
def main():
    print("🔥💀 ALTERNATIVE IMAGE EXTRACTOR 💀🔥")
    print("วิธีทางเลือกเมื่อ session หมดอายุ")
    print("=" * 50)
    
    extractor = AlternativeImageExtractor("whatilove1728")
    extractor.run_alternative_extraction()


if __name__ == "__main__":
    main()
