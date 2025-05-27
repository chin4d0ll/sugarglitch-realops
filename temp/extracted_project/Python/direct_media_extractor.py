#!/usr/bin/env python3
"""
Direct Stories & Media Extractor
Alternative method to extract stories, posts, and media from Instagram
"""

import json
import requests
import os
from datetime import datetime
import time

class DirectMediaExtractor:
    def __init__(self):
        # Load existing session
        with open('session.json', 'r') as f:
            self.session = json.load(f)
        
        self.sessionid = self.session['sessionid']
        self.user_id = self.session['ds_user_id']
        
        # Web browser headers
        self.web_headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': f'sessionid={self.sessionid}; ds_user_id={self.user_id}',
            'Referer': 'https://www.instagram.com/',
            'Connection': 'keep-alive'
        }
        
        print(f"✅ Session initialized for user: {self.user_id}")
    
    def get_user_media(self, username="alx.trading"):
        """Get user's posts and media"""
        print(f"🔍 Extracting media from {username}...")
        
        # Instagram web API for user posts
        url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
        
        try:
            response = requests.get(url, headers=self.web_headers)
            print(f"📡 Profile response: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                user_data = data.get('data', {}).get('user', {})
                
                # Get media from timeline
                edge_timeline = user_data.get('edge_owner_to_timeline_media', {})
                posts = edge_timeline.get('edges', [])
                
                print(f"📸 Found {len(posts)} posts")
                return posts
            else:
                print(f"❌ Failed: {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def get_stories_highlights(self, username="alx.trading"):
        """Get story highlights"""
        print(f"🔍 Getting story highlights for {username}...")
        
        url = f"https://www.instagram.com/{username}/"
        
        try:
            response = requests.get(url, headers=self.web_headers)
            
            if response.status_code == 200:
                # Look for story highlights in page data
                content = response.text
                
                # Extract story highlights data from page
                if '"highlight_reel_count":' in content:
                    print("📱 Story highlights detected")
                    return True
                else:
                    print("📭 No story highlights found")
                    return False
            
        except Exception as e:
            print(f"❌ Error getting highlights: {e}")
            return False
    
    def extract_media_urls(self, posts):
        """Extract downloadable media URLs from posts"""
        media_items = []
        
        for i, post_edge in enumerate(posts):
            post = post_edge.get('node', {})
            
            # Basic post info
            post_id = post.get('id', f'post_{i}')
            shortcode = post.get('shortcode', '')
            caption_edges = post.get('edge_media_to_caption', {}).get('edges', [])
            caption = caption_edges[0].get('node', {}).get('text', '') if caption_edges else ''
            taken_at = datetime.fromtimestamp(post.get('taken_at_timestamp', 0)).isoformat()
            
            # Media URL
            display_url = post.get('display_url', '')
            is_video = post.get('is_video', False)
            
            media_item = {
                'post_id': post_id,
                'shortcode': shortcode,
                'caption': caption,
                'timestamp': taken_at,
                'media_type': 'video' if is_video else 'image',
                'media_url': display_url,
                'likes_count': post.get('edge_liked_by', {}).get('count', 0),
                'comments_count': post.get('edge_media_to_comment', {}).get('count', 0)
            }
            
            # Get video URL if it's a video
            if is_video:
                video_url = post.get('video_url', '')
                if video_url:
                    media_item['video_url'] = video_url
            
            media_items.append(media_item)
            print(f"   📸 Post {i+1}: {media_item['media_type']} - {caption[:50]}...")
        
        return media_items
    
    def download_media_file(self, media_url, filename):
        """Download media file"""
        try:
            print(f"⬬ Downloading: {filename}")
            
            download_headers = {
                'User-Agent': self.web_headers['User-Agent'],
                'Referer': 'https://www.instagram.com/',
                'Cookie': self.web_headers['Cookie']
            }
            
            response = requests.get(media_url, headers=download_headers, stream=True)
            
            if response.status_code == 200:
                os.makedirs('downloaded_media', exist_ok=True)
                filepath = os.path.join('downloaded_media', filename)
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"✅ Downloaded: {filepath}")
                return filepath
            else:
                print(f"❌ Download failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Download error: {e}")
            return None
    
    def extract_and_download_all(self):
        """Extract and download all available media"""
        print("📸 EXTRACTING ALL AVAILABLE MEDIA")
        print("=" * 50)
        
        # Get user posts
        posts = self.get_user_media()
        
        if not posts:
            print("❌ No posts found")
            return None
        
        # Extract media URLs
        media_items = self.extract_media_urls(posts)
        
        # Download media files
        downloaded_files = []
        for i, media in enumerate(media_items):
            if media.get('media_url'):
                # Determine file extension
                ext = '.mp4' if media['media_type'] == 'video' else '.jpg'
                filename = f"alx_trading_post_{i+1}_{media['post_id']}{ext}"
                
                # Download
                downloaded_file = self.download_media_file(media['media_url'], filename)
                if downloaded_file:
                    media['downloaded_file'] = downloaded_file
                    downloaded_files.append(downloaded_file)
                
                time.sleep(1)  # Rate limiting
        
        # Save metadata
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        metadata_file = f"EXTRACTED_MEDIA_DATA_{timestamp}.json"
        
        output_data = {
            'extraction_timestamp': datetime.now().isoformat(),
            'target_account': 'alx.trading',
            'extraction_method': 'DIRECT_WEB_API',
            'total_posts': len(posts),
            'total_media_items': len(media_items),
            'successfully_downloaded': len(downloaded_files),
            'media_data': media_items
        }
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Extraction complete!")
        print(f"📊 Posts found: {len(posts)}")
        print(f"📸 Media items: {len(media_items)}")
        print(f"⬬ Downloaded: {len(downloaded_files)}")
        print(f"📄 Metadata: {metadata_file}")
        
        return {
            'media_items': media_items,
            'downloaded_files': downloaded_files,
            'metadata_file': metadata_file
        }

def main():
    print("📸 DIRECT MEDIA EXTRACTOR")
    print("=" * 40)
    print("🎯 Extracting posts, stories, and media")
    print("=" * 40)
    
    extractor = DirectMediaExtractor()
    
    # Check for story highlights
    has_highlights = extractor.get_stories_highlights()
    
    # Extract and download all media
    results = extractor.extract_and_download_all()
    
    if results:
        print(f"\n🎯 EXTRACTION RESULTS:")
        print(f"   📁 Download folder: downloaded_media/")
        print(f"   📄 Metadata file: {results['metadata_file']}")
        
        if results['downloaded_files']:
            print(f"\n📸 Downloaded files:")
            for file in results['downloaded_files']:
                print(f"   ✅ {file}")
    
    print(f"\n📱 Story highlights: {'✅ Available' if has_highlights else '❌ None found'}")

if __name__ == "__main__":
    main()
