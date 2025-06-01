#!/usr/bin/env python3
"""
🚀 Quick Instagram Image Extractor 2025
ดึงรูปภาพจาก Instagram อย่างรวดเร็ว
Based on working patterns from your existing extractors
"""

import requests
import json
import os
import time
import hashlib
from pathlib import Path
from datetime import datetime
import re
from urllib.parse import urlparse
import base64

class QuickInstagramImageExtractor:
    def __init__(self):
        self.workspace = Path("/workspaces/sugarglitch-realops")
        self.output_dir = self.workspace / "quick_extracted_images"
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "profiles").mkdir(exist_ok=True)
        (self.output_dir / "posts").mkdir(exist_ok=True)
        (self.output_dir / "stories").mkdir(exist_ok=True)
        (self.output_dir / "metadata").mkdir(exist_ok=True)
        
        self.session = requests.Session()
        self.setup_session()
        
        # Image extraction patterns
        self.image_patterns = [
            r'https://[^"]*\.cdninstagram\.com/[^"]*\.(jpg|jpeg|png|webp)',
            r'https://[^"]*\.fbcdn\.net/[^"]*\.(jpg|jpeg|png|webp)',
            r'https://scontent[^"]*\.(jpg|jpeg|png|webp)',
            r'"display_url":"([^"]*)"',
            r'"thumbnail_src":"([^"]*)"',
            r'"profile_pic_url":"([^"]*)"'
        ]
        
        self.extracted_images = []
        self.extraction_stats = {
            'total_found': 0,
            'successfully_downloaded': 0,
            'failed_downloads': 0,
            'start_time': datetime.now()
        }
        
        print("🚀 Quick Instagram Image Extractor 2025")
        print(f"📁 Output directory: {self.output_dir}")
    
    def setup_session(self):
        """Setup session with proper headers"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
    
    def extract_from_public_url(self, username):
        """Extract images from public Instagram profile"""
        print(f"\n🔍 Extracting from public profile: @{username}")
        
        # Try different URL patterns
        urls_to_try = [
            f"https://www.instagram.com/{username}/",
            f"https://www.instagram.com/{username}/?__a=1",
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
        ]
        
        for url in urls_to_try:
            try:
                print(f"🌐 Trying: {url}")
                response = self.session.get(url, timeout=15)
                
                if response.status_code == 200:
                    print(f"✅ Success! Got response from {url}")
                    return self.process_response_content(response.text, username, 'profile')
                else:
                    print(f"❌ Failed: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error with {url}: {e}")
                continue
        
        return False
    
    def process_response_content(self, content, username, content_type):
        """Process response content and extract images"""
        print(f"📊 Processing {content_type} content for @{username}")
        
        found_urls = set()
        
        # Extract using regex patterns
        for pattern in self.image_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    # For patterns with groups, take the first group
                    url = match[0] if match[0] else match
                else:
                    url = match
                
                # Clean up URL
                url = url.replace('\\u0026', '&').replace('\\/', '/')
                if url.startswith('http'):
                    found_urls.add(url)
        
        print(f"🔍 Found {len(found_urls)} unique image URLs")
        
        # Download images
        downloaded_count = 0
        for i, url in enumerate(found_urls, 1):
            if self.download_image(url, username, content_type, i):
                downloaded_count += 1
            
            # Rate limiting
            if i % 5 == 0:
                time.sleep(1)
        
        print(f"✅ Downloaded {downloaded_count}/{len(found_urls)} images")
        self.extraction_stats['total_found'] += len(found_urls)
        self.extraction_stats['successfully_downloaded'] += downloaded_count
        self.extraction_stats['failed_downloads'] += len(found_urls) - downloaded_count
        
        return downloaded_count > 0
    
    def download_image(self, url, username, content_type, index):
        """Download individual image"""
        try:
            # Generate filename
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Determine file extension
            parsed_url = urlparse(url)
            ext = '.jpg'  # default
            if any(e in parsed_url.path.lower() for e in ['.png', '.jpeg', '.webp']):
                ext = '.' + parsed_url.path.split('.')[-1].lower()
            
            filename = f"{username}_{content_type}_{timestamp}_{index:03d}_{url_hash}{ext}"
            filepath = self.output_dir / content_type.replace('profile', 'profiles') / filename
            
            # Download
            response = self.session.get(url, timeout=10, stream=True)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # Verify file size
                file_size = filepath.stat().st_size
                if file_size > 100:  # At least 100 bytes
                    print(f"✅ Downloaded: {filename} ({file_size} bytes)")
                    
                    # Store metadata
                    self.extracted_images.append({
                        'filename': filename,
                        'url': url,
                        'username': username,
                        'content_type': content_type,
                        'size_bytes': file_size,
                        'download_time': datetime.now().isoformat()
                    })
                    return True
                else:
                    filepath.unlink()  # Delete small/empty file
                    print(f"❌ File too small: {filename}")
            else:
                print(f"❌ Download failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Download error: {e}")
        
        return False
    
    def extract_from_search(self, hashtag):
        """Extract images from hashtag search"""
        print(f"\n🔍 Extracting from hashtag: #{hashtag}")
        
        search_url = f"https://www.instagram.com/explore/tags/{hashtag}/"
        
        try:
            response = self.session.get(search_url, timeout=15)
            if response.status_code == 200:
                return self.process_response_content(response.text, f"hashtag_{hashtag}", 'posts')
        except Exception as e:
            print(f"❌ Error extracting from hashtag: {e}")
        
        return False
    
    def extract_from_existing_data(self):
        """Extract images from existing JSON data in workspace"""
        print("\n🔍 Extracting from existing data files...")
        
        json_files = list(self.workspace.rglob("*.json"))
        processed_count = 0
        
        for json_file in json_files:
            if 'node_modules' in str(json_file) or '.git' in str(json_file):
                continue
                
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Look for image URLs in JSON content
                found_urls = set()
                for pattern in self.image_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    for match in matches:
                        if isinstance(match, tuple):
                            url = match[0] if match[0] else match
                        else:
                            url = match
                        
                        url = url.replace('\\u0026', '&').replace('\\/', '/')
                        if url.startswith('http'):
                            found_urls.add(url)
                
                if found_urls:
                    print(f"📁 Found {len(found_urls)} URLs in {json_file.name}")
                    for i, url in enumerate(found_urls, 1):
                        if self.download_image(url, "existing_data", "posts", processed_count + i):
                            processed_count += 1
                        
                        if i % 3 == 0:  # Rate limiting
                            time.sleep(0.5)
                            
            except Exception as e:
                continue  # Skip problematic files
        
        print(f"✅ Processed {processed_count} images from existing data")
        return processed_count > 0
    
    def generate_report(self):
        """Generate extraction report"""
        report = {
            'extraction_date': datetime.now().isoformat(),
            'duration_seconds': (datetime.now() - self.extraction_stats['start_time']).total_seconds(),
            'statistics': self.extraction_stats,
            'extracted_images': self.extracted_images,
            'output_directory': str(self.output_dir)
        }
        
        # Save report
        report_file = self.output_dir / "metadata" / f"extraction_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report, report_file
    
    def show_summary(self):
        """Show extraction summary"""
        duration = (datetime.now() - self.extraction_stats['start_time']).total_seconds()
        
        print("\n" + "="*60)
        print("📊 EXTRACTION SUMMARY")
        print("="*60)
        print(f"⏱️  Duration: {duration:.1f} seconds")
        print(f"🔍 Total URLs found: {self.extraction_stats['total_found']}")
        print(f"✅ Successfully downloaded: {self.extraction_stats['successfully_downloaded']}")
        print(f"❌ Failed downloads: {self.extraction_stats['failed_downloads']}")
        print(f"📁 Output directory: {self.output_dir}")
        
        if self.extracted_images:
            print(f"\n📸 Recent downloads:")
            for img in self.extracted_images[-5:]:  # Show last 5
                print(f"   🖼️  {img['filename']} ({img['size_bytes']} bytes)")
    
    def run_extraction(self):
        """Run the complete extraction process"""
        print("🚀 Starting Quick Instagram Image Extraction...")
        
        # Target accounts to extract from
        target_accounts = ["alx.trading", "whatilove1728", "natgeo", "nasa"]
        
        # Extract from existing data first (fastest)
        print("\n📊 Phase 1: Extracting from existing data...")
        self.extract_from_existing_data()
        
        # Extract from public profiles
        print("\n👥 Phase 2: Extracting from public profiles...")
        for username in target_accounts:
            try:
                self.extract_from_public_url(username)
                time.sleep(2)  # Rate limiting between accounts
            except Exception as e:
                print(f"❌ Error extracting from @{username}: {e}")
        
        # Extract from popular hashtags
        print("\n📱 Phase 3: Extracting from hashtags...")
        hashtags = ["photography", "nature", "art", "travel"]
        for hashtag in hashtags:
            try:
                self.extract_from_search(hashtag)
                time.sleep(3)  # Rate limiting between hashtags
            except Exception as e:
                print(f"❌ Error extracting from #{hashtag}: {e}")
        
        # Generate report and show summary
        report, report_file = self.generate_report()
        self.show_summary()
        
        print(f"\n📄 Report saved: {report_file}")
        print(f"🌐 Run image viewer to see results!")

def main():
    """Main entry point"""
    try:
        extractor = QuickInstagramImageExtractor()
        extractor.run_extraction()
        
        # Auto-update image gallery
        print("\n🔄 Updating image gallery...")
        import subprocess
        subprocess.run([
            "python", "image_discovery_tool.py"
        ], cwd="/workspaces/sugarglitch-realops")
        
    except KeyboardInterrupt:
        print("\n👋 Extraction stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
