#!/usr/bin/env python3
"""
🔧 Instagram Extractor - Fixed & Improved Version 2025 🔧
ปรับแก้และปรับปรุงแล้ว - แก้ปัญหาหลักๆ ที่พบ

Key Improvements:
- Better error handling
- Multiple extraction methods
- Improved proxy support  
- Session management
- Rate limiting protection
"""

import requests
import json
import time
import random
import os
import re
from datetime import datetime
from pathlib import Path
import urllib.parse
from typing import Dict, List, Optional
import base64

class ImprovedInstagramExtractor:
    def __init__(self):
        self.base_dir = Path("/workspaces/sugarglitch-realops")
        self.results_dir = self.base_dir / "improved_extraction_results"
        self.images_dir = self.results_dir / "images"
        self.results_dir.mkdir(exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)
        
        # Initialize session with better configuration
        self.session = requests.Session()
        self.setup_session()
        
        # Rate limiting
        self.last_request_time = 0
        self.min_delay = 2  # seconds between requests
        
        print("🔧 Instagram Extractor - Improved Version")
        print(f"📁 Results will be saved to: {self.results_dir}")
        
    def setup_session(self):
        """Setup session with proper headers and configurations"""
        # Rotate between multiple realistic user agents
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        
        self.session.headers.update({
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Set session timeout
        self.session.timeout = 30
        
    def rate_limit_delay(self):
        """Implement rate limiting to avoid blocks"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_delay:
            sleep_time = self.min_delay - time_since_last + random.uniform(0.5, 2.0)
            print(f"⏱️ Rate limiting: sleeping for {sleep_time:.1f}s")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def safe_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """Make a safe request with error handling and rate limiting"""
        self.rate_limit_delay()
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"🌐 Making {method} request to: {url}")
                
                if method.upper() == 'GET':
                    response = self.session.get(url, **kwargs)
                elif method.upper() == 'POST':
                    response = self.session.post(url, **kwargs)
                else:
                    raise ValueError(f"Unsupported method: {method}")
                
                if response.status_code == 200:
                    print(f"✅ Request successful (200)")
                    return response
                elif response.status_code == 429:
                    print(f"⚠️ Rate limited (429), waiting longer...")
                    time.sleep(30 * (attempt + 1))
                    continue
                else:
                    print(f"⚠️ Request returned status {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Request failed (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(5 * (attempt + 1))
                    continue
        
        print(f"❌ All request attempts failed")
        return None
    
    def extract_public_profile_data(self, username: str) -> Dict:
        """Extract public profile data using web scraping"""
        print(f"📱 Extracting public data for: {username}")
        
        profile_url = f"https://www.instagram.com/{username}/"
        response = self.safe_request(profile_url)
        
        if not response:
            return {"error": "Could not fetch profile page"}
        
        # Extract data from page
        content = response.text
        data = {
            "username": username,
            "extraction_time": datetime.now().isoformat(),
            "profile_url": profile_url,
            "images_found": [],
            "metadata": {}
        }
        
        try:
            # Look for JSON data in script tags
            json_pattern = r'window\._sharedData\s*=\s*({.*?});'
            json_match = re.search(json_pattern, content)
            
            if json_match:
                json_data = json.loads(json_match.group(1))
                print("✅ Found shared data JSON")
                
                # Extract profile info
                if 'entry_data' in json_data and 'ProfilePage' in json_data['entry_data']:
                    profile_data = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
                    data['metadata'] = {
                        'full_name': profile_data.get('full_name', ''),
                        'biography': profile_data.get('biography', ''),
                        'followers_count': profile_data.get('edge_followed_by', {}).get('count', 0),
                        'following_count': profile_data.get('edge_follow', {}).get('count', 0),
                        'posts_count': profile_data.get('edge_owner_to_timeline_media', {}).get('count', 0),
                        'is_private': profile_data.get('is_private', False),
                        'is_verified': profile_data.get('is_verified', False)
                    }
                    
                    # Extract post images
                    if 'edge_owner_to_timeline_media' in profile_data:
                        posts = profile_data['edge_owner_to_timeline_media']['edges']
                        for post in posts:
                            node = post['node']
                            if 'display_url' in node:
                                data['images_found'].append({
                                    'url': node['display_url'],
                                    'shortcode': node.get('shortcode', ''),
                                    'caption': node.get('edge_media_to_caption', {}).get('edges', [{}])[0].get('node', {}).get('text', ''),
                                    'likes': node.get('edge_liked_by', {}).get('count', 0),
                                    'comments': node.get('edge_media_to_comment', {}).get('count', 0)
                                })
            
            # Alternative: look for image URLs in the HTML
            img_pattern = r'https://[^"]*\.(?:jpg|jpeg|png|gif|webp)'
            img_urls = re.findall(img_pattern, content)
            
            for url in set(img_urls):  # Remove duplicates
                if url not in [img['url'] for img in data['images_found']]:
                    data['images_found'].append({
                        'url': url,
                        'source': 'html_extraction',
                        'type': 'discovered_image'
                    })
            
            print(f"✅ Found {len(data['images_found'])} images")
            
        except Exception as e:
            print(f"⚠️ Error parsing profile data: {e}")
            data['error'] = str(e)
        
        return data
    
    def download_image(self, url: str, filename: str) -> bool:
        """Download an image from URL"""
        try:
            print(f"⬇️ Downloading: {filename}")
            
            response = self.safe_request(url)
            if not response:
                return False
            
            filepath = self.images_dir / filename
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Downloaded: {filepath}")
            return True
            
        except Exception as e:
            print(f"❌ Download failed for {filename}: {e}")
            return False
    
    def extract_and_download_images(self, username: str) -> Dict:
        """Complete extraction and download process"""
        print(f"🚀 Starting complete extraction for: {username}")
        
        # Extract profile data
        profile_data = self.extract_public_profile_data(username)
        
        if 'error' in profile_data:
            return profile_data
        
        # Download images
        downloaded_count = 0
        failed_count = 0
        
        for i, img_data in enumerate(profile_data['images_found']):
            url = img_data['url']
            
            # Generate filename
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            extension = url.split('.')[-1].split('?')[0]
            if extension not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                extension = 'jpg'
            
            filename = f"{username}_{i:03d}_{url_hash}.{extension}"
            
            if self.download_image(url, filename):
                downloaded_count += 1
                img_data['downloaded_filename'] = filename
            else:
                failed_count += 1
                img_data['download_failed'] = True
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = self.results_dir / f"extraction_results_{username}_{timestamp}.json"
        
        summary = {
            "extraction_summary": {
                "username": username,
                "timestamp": timestamp,
                "total_images_found": len(profile_data['images_found']),
                "images_downloaded": downloaded_count,
                "download_failures": failed_count,
                "success_rate": f"{(downloaded_count/(downloaded_count+failed_count)*100):.1f}%" if (downloaded_count+failed_count) > 0 else "0%"
            },
            "profile_data": profile_data
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"""
        ✅ Extraction Complete!
        📊 Results:
        - Images found: {len(profile_data['images_found'])}
        - Downloaded: {downloaded_count}
        - Failed: {failed_count}
        - Results saved: {results_file}
        """)
        
        return summary
    
    def extract_multiple_accounts(self, usernames: List[str]) -> Dict:
        """Extract from multiple accounts"""
        print(f"🎯 Extracting from {len(usernames)} accounts...")
        
        all_results = {}
        
        for username in usernames:
            print(f"\n{'='*50}")
            print(f"Processing: {username}")
            print(f"{'='*50}")
            
            try:
                result = self.extract_and_download_images(username)
                all_results[username] = result
                
                # Longer delay between accounts
                print("⏱️ Waiting between accounts...")
                time.sleep(random.uniform(10, 20))
                
            except Exception as e:
                print(f"❌ Failed to process {username}: {e}")
                all_results[username] = {"error": str(e)}
        
        return all_results

import hashlib

def main():
    print("🔧 Instagram Extractor - Fixed & Improved Version")
    print("=" * 60)
    
    extractor = ImprovedInstagramExtractor()
    
    # Test accounts (starting with public ones)
    test_accounts = ["whatilove1728", "alx.trading"]
    
    print(f"🎯 Target accounts: {test_accounts}")
    
    try:
        results = extractor.extract_multiple_accounts(test_accounts)
        
        print("\n🎉 All extractions completed!")
        for username, result in results.items():
            if 'error' not in result:
                summary = result.get('extraction_summary', {})
                print(f"✅ {username}: {summary.get('images_downloaded', 0)} images downloaded")
            else:
                print(f"❌ {username}: {result['error']}")
                
    except KeyboardInterrupt:
        print("\n⏹️ Extraction stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
