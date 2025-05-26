#!/usr/bin/env python3
"""
📸 WHATILOVE1728 IMAGE DOWNLOADER 📸
Download all pictures and media from whatilove1728 Instagram account
Using existing session data for authenticated access
"""

import json
import requests
import os
import time
import random
from datetime import datetime
from pathlib import Path
import re
from urllib.parse import urlparse, urljoin
import hashlib

class WhatILove1728ImageDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.target_username = "whatilove1728"
        self.output_folder = "/workspaces/sugarglitch-realops/whatilove1728_images"
        self.session_data = None
        
        # Create output folders
        Path(self.output_folder).mkdir(exist_ok=True)
        Path(f"{self.output_folder}/profile_pics").mkdir(exist_ok=True)
        Path(f"{self.output_folder}/posts").mkdir(exist_ok=True)
        Path(f"{self.output_folder}/stories").mkdir(exist_ok=True)
        Path(f"{self.output_folder}/thumbnails").mkdir(exist_ok=True)
        
        # Load session data
        self.load_session_data()
        self.setup_session()
        
        # Download statistics
        self.download_stats = {
            'total_found': 0,
            'successfully_downloaded': 0,
            'failed_downloads': 0,
            'already_exists': 0
        }
    
    def load_session_data(self):
        """Load existing whatilove1728 session data"""
        session_files = [
            "./extracted_project/Python/PRIVATE_BYPASS_SUCCESS_whatilove1728_20250525_234142.json",
            "./extracted_project/Python/success_whatilove1728_20250525_153247.json",
            "./extracted_project/Python/success_whatilove1728_20250525_153334.json",
            "./extracted_project/Python/success_whatilove1728_20250525_153211.json"
        ]
        
        for file in session_files:
            if os.path.exists(file):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                    
                    if 'sessionid' in data or ('session_data' in data and 'cookies_before' in data['session_data']):
                        self.session_data = data
                        print(f"✅ Loaded session from: {file}")
                        return True
                        
                except Exception as e:
                    print(f"❌ Error loading {file}: {e}")
        
        print("❌ No valid session data found!")
        return False
    
    def setup_session(self):
        """Setup session with Instagram cookies and headers"""
        if not self.session_data:
            print("❌ No session data available")
            return False
        
        # Setup headers
        headers = {
            'User-Agent': 'Instagram 219.0.0.12.117 Android (33/13; 420dpi; 1080x2400; samsung; SM-G973F; beyond1; exynos9820; en_US; 314665256)',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'X-IG-App-ID': '936619743392459',
            'X-ASBD-ID': '198387',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }
        
        self.session.headers.update(headers)
        
        # Setup cookies
        if 'sessionid' in self.session_data:
            # Direct session format
            self.session.cookies.set('sessionid', self.session_data['sessionid'])
            self.session.cookies.set('ds_user_id', self.session_data.get('ds_user_id', ''))
        elif 'session_data' in self.session_data and 'cookies_before' in self.session_data['session_data']:
            # Detailed session format
            for cookie in self.session_data['session_data']['cookies_before']:
                self.session.cookies.set(cookie['name'], cookie['value'])
        
        print("✅ Session configured for image downloading")
        return True
    
    def human_delay(self, min_delay=1, max_delay=3):
        """Human-like delay between requests"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def download_image(self, url, filename, folder="posts"):
        """Download a single image from URL"""
        if not url:
            return False
        
        try:
            # Create full path
            full_path = os.path.join(self.output_folder, folder, filename)
            
            # Check if already exists
            if os.path.exists(full_path):
                print(f"   ⏭️ Already exists: {filename}")
                self.download_stats['already_exists'] += 1
                return True
            
            # Download image
            response = self.session.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Save image
            with open(full_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            file_size = os.path.getsize(full_path)
            print(f"   ✅ Downloaded: {filename} ({file_size:,} bytes)")
            self.download_stats['successfully_downloaded'] += 1
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to download {filename}: {e}")
            self.download_stats['failed_downloads'] += 1
            return False
    
    def extract_images_from_profile_page(self):
        """Extract images from the main profile page"""
        print("🔍 Extracting images from profile page...")
        
        try:
            url = f"https://www.instagram.com/{self.target_username}/"
            response = self.session.get(url, timeout=30)
            
            if response.status_code != 200:
                print(f"❌ Profile page failed: {response.status_code}")
                return []
            
            # Extract image URLs using regex patterns
            image_patterns = [
                r'"display_url":"([^"]+)"',
                r'"thumbnail_src":"([^"]+)"', 
                r'"src":"([^"]+\.jpg[^"]*)"',
                r'"src":"([^"]+\.jpeg[^"]*)"',
                r'"src":"([^"]+\.png[^"]*)"',
                r'"profile_pic_url":"([^"]+)"',
                r'"profile_pic_url_hd":"([^"]+)"'
            ]
            
            found_urls = set()
            
            for pattern in image_patterns:
                matches = re.findall(pattern, response.text, re.IGNORECASE)
                for match in matches:
                    # Clean up URL (remove escapes)
                    clean_url = match.replace('\\u0026', '&').replace('\\/', '/')
                    if clean_url.startswith('http'):
                        found_urls.add(clean_url)
            
            print(f"📊 Found {len(found_urls)} image URLs from profile page")
            self.download_stats['total_found'] += len(found_urls)
            
            return list(found_urls)
            
        except Exception as e:
            print(f"❌ Profile page extraction failed: {e}")
            return []
    
    def extract_images_from_api(self):
        """Extract images using Instagram's internal API"""
        print("🔍 Extracting images via Instagram API...")
        
        image_urls = []
        
        try:
            # Try to get user ID first
            user_info_url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={self.target_username}"
            
            response = self.session.get(user_info_url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and 'user' in data['data']:
                    user_data = data['data']['user']
                    
                    # Profile picture
                    profile_pic = user_data.get('profile_pic_url_hd', user_data.get('profile_pic_url', ''))
                    if profile_pic:
                        image_urls.append(('profile_pic.jpg', profile_pic, 'profile_pics'))
                    
                    # Posts from edge_owner_to_timeline_media
                    if 'edge_owner_to_timeline_media' in user_data:
                        posts = user_data['edge_owner_to_timeline_media'].get('edges', [])
                        
                        for i, post in enumerate(posts):
                            node = post.get('node', {})
                            
                            # Main display URL
                            display_url = node.get('display_url', '')
                            if display_url:
                                filename = f"post_{i+1}_{node.get('id', 'unknown')}.jpg"
                                image_urls.append((filename, display_url, 'posts'))
                            
                            # Thumbnail
                            thumbnail_url = node.get('thumbnail_src', '')
                            if thumbnail_url:
                                filename = f"thumb_{i+1}_{node.get('id', 'unknown')}.jpg"
                                image_urls.append((filename, thumbnail_url, 'thumbnails'))
                            
                            # Sidecar children (multiple images in one post)
                            if 'edge_sidecar_to_children' in node:
                                children = node['edge_sidecar_to_children'].get('edges', [])
                                for j, child in enumerate(children):
                                    child_node = child.get('node', {})
                                    child_url = child_node.get('display_url', '')
                                    if child_url:
                                        filename = f"post_{i+1}_{j+1}_{child_node.get('id', 'unknown')}.jpg"
                                        image_urls.append((filename, child_url, 'posts'))
                
                print(f"📊 Found {len(image_urls)} images via API")
                self.download_stats['total_found'] += len(image_urls)
                
            else:
                print(f"❌ API request failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ API extraction failed: {e}")
        
        return image_urls
    
    def extract_images_from_existing_files(self):
        """Extract image URLs from already downloaded HTML files"""
        print("🔍 Extracting images from existing HTML files...")
        
        image_urls = []
        html_files = [
            "./extracted_project/Python/PRIVATE_PROFILE_whatilove1728_20250525_234142.html",
            "./extracted_project/Python/PRIVATE_DMS_whatilove1728_20250525_234143.html"
        ]
        
        for html_file in html_files:
            if os.path.exists(html_file):
                try:
                    with open(html_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract image URLs
                    patterns = [
                        r'"(https://[^"]*\.cdninstagram\.com/[^"]*\.jpg[^"]*)"',
                        r'"(https://[^"]*\.cdninstagram\.com/[^"]*\.jpeg[^"]*)"',
                        r'"(https://[^"]*\.cdninstagram\.com/[^"]*\.png[^"]*)"',
                        r'src="(https://[^"]*\.jpg[^"]*)"',
                        r'src="(https://[^"]*\.jpeg[^"]*)"',
                        r'src="(https://[^"]*\.png[^"]*)"'
                    ]
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        for match in matches:
                            # Generate filename from URL
                            parsed_url = urlparse(match)
                            filename = os.path.basename(parsed_url.path)
                            if not filename.endswith(('.jpg', '.jpeg', '.png')):
                                filename += '.jpg'
                            
                            # Create unique filename
                            url_hash = hashlib.md5(match.encode()).hexdigest()[:8]
                            filename = f"{url_hash}_{filename}"
                            
                            image_urls.append((filename, match, 'posts'))
                    
                    print(f"   📄 {os.path.basename(html_file)}: {len(re.findall(r'https://[^"]*\.cdninstagram\.com/[^"]*\.(jpg|jpeg|png)', content))} images")
                    
                except Exception as e:
                    print(f"   ❌ Error processing {html_file}: {e}")
        
        # Remove duplicates
        seen_urls = set()
        unique_images = []
        for filename, url, folder in image_urls:
            if url not in seen_urls:
                seen_urls.add(url)
                unique_images.append((filename, url, folder))
        
        print(f"📊 Found {len(unique_images)} unique images from HTML files")
        self.download_stats['total_found'] += len(unique_images)
        
        return unique_images
    
    def download_all_images(self):
        """Download all found images"""
        print("📸 WHATILOVE1728 IMAGE DOWNLOAD STARTED")
        print("=" * 60)
        print(f"🎯 Target: {self.target_username}")
        print(f"📁 Output: {self.output_folder}")
        print()
        
        if not self.session_data:
            print("❌ No valid session data found!")
            return
        
        all_images = []
        
        # Method 1: Extract from existing HTML files
        print("📄 Method 1: Extracting from existing HTML files...")
        html_images = self.extract_images_from_existing_files()
        all_images.extend(html_images)
        self.human_delay(2, 4)
        
        # Method 2: Extract from profile page
        print("\n🌐 Method 2: Extracting from live profile page...")
        profile_images = self.extract_images_from_profile_page()
        for i, url in enumerate(profile_images):
            filename = f"profile_extract_{i+1}.jpg"
            all_images.append((filename, url, 'posts'))
        self.human_delay(2, 4)
        
        # Method 3: Extract via API
        print("\n🔌 Method 3: Extracting via Instagram API...")
        api_images = self.extract_images_from_api()
        all_images.extend(api_images)
        
        # Remove duplicates
        print(f"\n🔄 Removing duplicates...")
        seen_urls = set()
        unique_images = []
        for filename, url, folder in all_images:
            if url not in seen_urls:
                seen_urls.add(url)
                unique_images.append((filename, url, folder))
        
        print(f"📊 Total unique images to download: {len(unique_images)}")
        print()
        
        # Download all images
        for i, (filename, url, folder) in enumerate(unique_images, 1):
            print(f"📸 Downloading {i}/{len(unique_images)}: {filename}")
            self.download_image(url, filename, folder)
            
            # Human-like delay between downloads
            if i < len(unique_images):
                self.human_delay(0.5, 2)
        
        # Display final statistics
        self.display_download_summary()
    
    def display_download_summary(self):
        """Display download statistics and summary"""
        print("\n" + "=" * 60)
        print("📊 DOWNLOAD SUMMARY")
        print("=" * 60)
        print(f"🎯 Target Account: {self.target_username}")
        print(f"📁 Output Folder: {self.output_folder}")
        print()
        print("📈 Statistics:")
        print(f"   🔍 Total images found: {self.download_stats['total_found']}")
        print(f"   ✅ Successfully downloaded: {self.download_stats['successfully_downloaded']}")
        print(f"   ⏭️ Already existed: {self.download_stats['already_exists']}")
        print(f"   ❌ Failed downloads: {self.download_stats['failed_downloads']}")
        print()
        
        # Calculate success rate
        total_processed = (self.download_stats['successfully_downloaded'] + 
                          self.download_stats['already_exists'] + 
                          self.download_stats['failed_downloads'])
        
        if total_processed > 0:
            success_rate = ((self.download_stats['successfully_downloaded'] + 
                           self.download_stats['already_exists']) / total_processed) * 100
            print(f"📊 Success Rate: {success_rate:.1f}%")
        
        print()
        print("📁 Downloaded files are organized in:")
        print(f"   📸 Profile Pictures: {self.output_folder}/profile_pics/")
        print(f"   🖼️ Posts: {self.output_folder}/posts/")
        print(f"   🔍 Thumbnails: {self.output_folder}/thumbnails/")
        print(f"   📱 Stories: {self.output_folder}/stories/")
        
        print("\n✅ WHATILOVE1728 IMAGE DOWNLOAD COMPLETE!")
        print("=" * 60)

def main():
    print("📸💀 WHATILOVE1728 IMAGE DOWNLOADER 💀📸")
    print("Downloading all pictures from whatilove1728 account")
    print()
    
    try:
        downloader = WhatILove1728ImageDownloader()
        downloader.download_all_images()
    except KeyboardInterrupt:
        print("\n⚠️ Download interrupted by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()
