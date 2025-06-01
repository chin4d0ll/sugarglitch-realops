#!/usr/bin/env python3
"""
🛡️ Safe Instagram Image Extractor 2025 🛡️
วิธีการปลอดภัย - ไม่ต้อง login, ไม่เสี่ยงโดนแบน

Features:
- Public profile extraction only
- No login required
- Multiple fallback methods
- Respects rate limits
- Advanced image discovery
"""

import requests
import json
import time
import os
import re
from datetime import datetime
from pathlib import Path
import hashlib
from urllib.parse import urlparse, unquote
import random

class SafeInstagramExtractor:
    def __init__(self):
        self.base_dir = Path("/workspaces/sugarglitch-realops")
        self.safe_results_dir = self.base_dir / "safe_extraction_results"
        self.images_dir = self.safe_results_dir / "downloaded_images"
        
        # Create directories
        self.safe_results_dir.mkdir(exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)
        
        # Session setup
        self.session = requests.Session()
        self.setup_safe_session()
        
        print("🛡️ Safe Instagram Image Extractor 2025")
        print(f"📁 Safe results directory: {self.safe_results_dir}")
        print("✅ No login required - Public profiles only")
        
    def setup_safe_session(self):
        """Setup session to look like a regular browser"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        
        self.session.headers.update({
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
    
    def safe_wait(self, min_seconds=3, max_seconds=7):
        """Safe waiting between requests"""
        wait_time = random.uniform(min_seconds, max_seconds)
        print(f"⏱️ Waiting {wait_time:.1f}s to respect rate limits...")
        time.sleep(wait_time)
    
    def get_profile_page(self, username: str) -> str:
        """Get Instagram profile page HTML"""
        url = f"https://www.instagram.com/{username}/"
        
        try:
            print(f"🌐 Fetching profile page: {url}")
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                print("✅ Profile page loaded successfully")
                return response.text
            elif response.status_code == 404:
                print("❌ Profile not found (404)")
                return None
            elif response.status_code == 429:
                print("⚠️ Rate limited (429) - need to wait longer")
                return None
            else:
                print(f"⚠️ Unexpected status code: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error fetching profile: {e}")
            return None
    
    def extract_images_from_html(self, html_content: str, username: str) -> list:
        """Extract image URLs from HTML content using multiple methods"""
        images = []
        
        print("🔍 Extracting images from HTML...")
        
        # Method 1: Look for high-quality image URLs
        hq_patterns = [
            r'https://[^"]*\.cdninstagram\.com/[^"]*\.jpg\?[^"]*',
            r'https://[^"]*\.fbcdn\.net/[^"]*\.jpg\?[^"]*',
            r'https://[^"]*instagram[^"]*\.jpg[^"]*',
            r'https://[^"]*\.cdninstagram\.com/[^"]*\.webp\?[^"]*'
        ]
        
        for pattern in hq_patterns:
            matches = re.findall(pattern, html_content)
            for match in matches:
                # Clean up URL
                clean_url = match.split('&')[0]  # Remove tracking parameters
                if clean_url not in [img['url'] for img in images]:
                    images.append({
                        'url': clean_url,
                        'source': 'html_pattern',
                        'quality': 'high' if '640x640' in clean_url or '1080x1080' in clean_url else 'medium'
                    })
        
        # Method 2: Look for JSON data with image info
        try:
            # Find window._sharedData
            shared_data_match = re.search(r'window\._sharedData\s*=\s*({.*?});', html_content)
            if shared_data_match:
                print("✅ Found shared data")
                shared_data = json.loads(shared_data_match.group(1))
                
                # Navigate through the data structure
                if 'entry_data' in shared_data:
                    if 'ProfilePage' in shared_data['entry_data']:
                        profile_page = shared_data['entry_data']['ProfilePage'][0]
                        if 'graphql' in profile_page and 'user' in profile_page['graphql']:
                            user_data = profile_page['graphql']['user']
                            
                            # Get profile picture
                            if 'profile_pic_url_hd' in user_data:
                                images.append({
                                    'url': user_data['profile_pic_url_hd'],
                                    'source': 'profile_picture',
                                    'quality': 'hd',
                                    'type': 'profile_pic'
                                })
                            
                            # Get posts
                            if 'edge_owner_to_timeline_media' in user_data:
                                posts = user_data['edge_owner_to_timeline_media']['edges']
                                for post in posts:
                                    node = post['node']
                                    if 'display_url' in node:
                                        images.append({
                                            'url': node['display_url'],
                                            'source': 'timeline_post',
                                            'quality': 'high',
                                            'shortcode': node.get('shortcode', ''),
                                            'likes': node.get('edge_liked_by', {}).get('count', 0)
                                        })
                                    
                                    # Check for carousel (multiple images)
                                    if node.get('__typename') == 'GraphSidecar':
                                        if 'edge_sidecar_to_children' in node:
                                            for child in node['edge_sidecar_to_children']['edges']:
                                                child_node = child['node']
                                                if 'display_url' in child_node:
                                                    images.append({
                                                        'url': child_node['display_url'],
                                                        'source': 'carousel_image',
                                                        'quality': 'high',
                                                        'parent_shortcode': node.get('shortcode', '')
                                                    })
        except Exception as e:
            print(f"⚠️ JSON parsing error: {e}")
        
        # Method 3: Look for additional patterns
        additional_patterns = [
            r'src="(https://[^"]*instagram[^"]*\.(?:jpg|jpeg|png|webp))',
            r'"(https://[^"]*\.(?:jpg|jpeg|png|webp))"',
        ]
        
        for pattern in additional_patterns:
            matches = re.findall(pattern, html_content)
            for match in matches:
                if 'instagram' in match and match not in [img['url'] for img in images]:
                    images.append({
                        'url': match,
                        'source': 'additional_pattern',
                        'quality': 'unknown'
                    })
        
        print(f"✅ Found {len(images)} images")
        return images
    
    def download_image_safe(self, url: str, filename: str) -> bool:
        """Safely download an image"""
        try:
            print(f"⬇️ Downloading: {filename}")
            
            # Add headers to look like a browser requesting an image
            headers = {
                'User-Agent': self.session.headers['User-Agent'],
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Referer': 'https://www.instagram.com/',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            
            response = self.session.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                filepath = self.images_dir / filename
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                # Verify file was downloaded properly
                if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:  # At least 1KB
                    print(f"✅ Downloaded successfully: {filename} ({os.path.getsize(filepath)} bytes)")
                    return True
                else:
                    print(f"⚠️ Downloaded file seems too small: {filename}")
                    return False
            else:
                print(f"❌ Download failed: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Download error for {filename}: {e}")
            return False
    
    def extract_profile_safely(self, username: str) -> dict:
        """Extract profile data and images safely"""
        print(f"\n🎯 Starting safe extraction for: {username}")
        print("=" * 50)
        
        result = {
            'username': username,
            'extraction_time': datetime.now().isoformat(),
            'method': 'safe_public_extraction',
            'images': [],
            'download_summary': {
                'attempted': 0,
                'successful': 0,
                'failed': 0
            }
        }
        
        # Get profile page
        html_content = self.get_profile_page(username)
        if not html_content:
            result['error'] = 'Could not fetch profile page'
            return result
        
        self.safe_wait()
        
        # Extract images
        images = self.extract_images_from_html(html_content, username)
        if not images:
            result['error'] = 'No images found'
            return result
        
        # Download images
        for i, img_data in enumerate(images):
            url = img_data['url']
            
            # Generate safe filename
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            extension = self.get_file_extension(url)
            filename = f"{username}_safe_{i:03d}_{img_data['source']}_{url_hash}.{extension}"
            
            result['download_summary']['attempted'] += 1
            
            if self.download_image_safe(url, filename):
                img_data['downloaded_filename'] = filename
                img_data['local_path'] = str(self.images_dir / filename)
                result['download_summary']['successful'] += 1
            else:
                img_data['download_failed'] = True
                result['download_summary']['failed'] += 1
            
            result['images'].append(img_data)
            
            # Wait between downloads
            self.safe_wait(2, 5)
        
        # Save results
        self.save_results(result, username)
        
        return result
    
    def get_file_extension(self, url: str) -> str:
        """Get file extension from URL"""
        parsed = urlparse(url)
        path = unquote(parsed.path)
        
        # Try to get extension from path
        if '.' in path:
            ext = path.split('.')[-1].lower()
            if ext in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
                return ext
        
        # Default to jpg
        return 'jpg'
    
    def save_results(self, result: dict, username: str):
        """Save extraction results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = self.safe_results_dir / f"safe_extraction_{username}_{timestamp}.json"
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved: {results_file}")

def main():
    print("🛡️ Safe Instagram Image Extractor 2025")
    print("=" * 60)
    print("✅ No login required")
    print("✅ Public profiles only")
    print("✅ Respects rate limits")
    print("✅ Browser-like behavior")
    print("=" * 60)
    
    extractor = SafeInstagramExtractor()
    
    # Test with target accounts
    target_accounts = ["whatilove1728", "alx.trading"]
    
    all_results = {}
    
    for username in target_accounts:
        try:
            result = extractor.extract_profile_safely(username)
            all_results[username] = result
            
            # Print summary
            if 'error' not in result:
                summary = result['download_summary']
                print(f"""
                ✅ {username} extraction complete:
                   📊 Images found: {len(result['images'])}
                   ⬇️ Downloads attempted: {summary['attempted']}
                   ✅ Successful: {summary['successful']}
                   ❌ Failed: {summary['failed']}
                   📈 Success rate: {(summary['successful']/summary['attempted']*100):.1f}%
                """)
            else:
                print(f"❌ {username} failed: {result['error']}")
            
            # Longer wait between accounts
            if username != target_accounts[-1]:  # Don't wait after last account
                print("⏱️ Waiting between accounts...")
                time.sleep(random.uniform(15, 25))
                
        except KeyboardInterrupt:
            print("\n⏹️ Extraction stopped by user")
            break
        except Exception as e:
            print(f"❌ Unexpected error for {username}: {e}")
            all_results[username] = {'error': str(e)}
    
    print("\n🎉 Safe extraction process completed!")
    for username, result in all_results.items():
        if 'error' not in result:
            print(f"✅ {username}: {result['download_summary']['successful']} images downloaded")
        else:
            print(f"❌ {username}: {result['error']}")

if __name__ == "__main__":
    main()
