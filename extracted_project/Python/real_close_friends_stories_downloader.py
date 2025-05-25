#!/usr/bin/env python3
"""
REAL Instagram Close Friends Stories Downloader
Downloads actual close friends stories from Instagram account
NO MOCKUP - REAL EXTRACTION ONLY
"""

import json
import requests
import os
import time
from datetime import datetime
import base64

class RealStoriesDownloader:
    def __init__(self):
        # Load session data
        try:
            with open('session.json', 'r') as f:
                self.session = json.load(f)
            
            self.sessionid = self.session['sessionid']
            self.user_id = self.session['ds_user_id']
            print(f"✅ Session loaded - User ID: {self.user_id}")
        except:
            print("❌ Could not load session")
            return
        
        self.headers = {
            'User-Agent': 'Instagram 219.0.0.12.117 Android (28/9; 420dpi; 1080x2130; samsung; SM-G973F; beyond1; exynos9820; en_US; 314665256)',
            'Accept': '*/*',
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
            'Cookie': f'sessionid={self.sessionid}; ds_user_id={self.user_id}',
            'X-Instagram-AJAX': '1',
            'X-CSRFToken': 'missing',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        # Create download directory
        self.download_dir = "downloaded_close_friends_stories"
        os.makedirs(self.download_dir, exist_ok=True)
        print(f"📁 Download directory: {self.download_dir}")
    
    def get_stories_feed(self):
        """Get the stories feed including close friends stories"""
        print("🔍 Fetching stories feed...")
        
        # Instagram Stories API endpoint
        url = "https://i.instagram.com/api/v1/feed/reels_tray/"
        
        try:
            response = requests.get(url, headers=self.headers)
            print(f"📡 Stories feed response: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"❌ Failed to get stories: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error getting stories: {e}")
            return None
    
    def get_user_stories(self, user_id):
        """Get specific user's stories"""
        url = f"https://i.instagram.com/api/v1/feed/user/{user_id}/story/"
        
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get user {user_id} stories: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error getting user stories: {e}")
            return None
    
    def download_story_media(self, media_url, filename):
        """Download story media (image/video)"""
        try:
            print(f"⬬ Downloading: {filename}")
            
            # Add Instagram headers for media download
            media_headers = {
                'User-Agent': self.headers['User-Agent'],
                'Referer': 'https://www.instagram.com/',
                'Cookie': self.headers['Cookie']
            }
            
            response = requests.get(media_url, headers=media_headers, stream=True)
            
            if response.status_code == 200:
                filepath = os.path.join(self.download_dir, filename)
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"✅ Downloaded: {filepath}")
                return filepath
            else:
                print(f"❌ Failed to download media: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Download error: {e}")
            return None
    
    def extract_close_friends_stories(self):
        """Extract and download close friends stories"""
        print("🔍 EXTRACTING CLOSE FRIENDS STORIES")
        print("=" * 50)
        
        # Get stories feed
        stories_data = self.get_stories_feed()
        if not stories_data:
            return []
        
        close_friends_stories = []
        tray = stories_data.get('tray', [])
        
        print(f"📱 Found {len(tray)} story users")
        
        for story_user in tray:
            user_info = story_user.get('user', {})
            username = user_info.get('username', 'unknown')
            full_name = user_info.get('full_name', 'unknown')
            user_id = user_info.get('pk', '')
            
            print(f"\n👤 {username} ({full_name})")
            
            # Check if this user has stories
            items = story_user.get('items', [])
            if not items:
                print("   📭 No stories")
                continue
            
            print(f"   📸 {len(items)} stories found")
            
            user_stories = []
            for i, item in enumerate(items):
                story_data = self.process_story_item(item, username, i)
                if story_data:
                    user_stories.append(story_data)
            
            if user_stories:
                close_friends_stories.append({
                    'username': username,
                    'full_name': full_name,
                    'user_id': user_id,
                    'is_close_friend': story_user.get('is_close_friend', False),
                    'stories': user_stories,
                    'total_stories': len(user_stories)
                })
        
        return close_friends_stories
    
    def process_story_item(self, item, username, index):
        """Process individual story item"""
        try:
            # Get story metadata
            story_id = item.get('id', f'story_{index}')
            taken_at = item.get('taken_at', 0)
            timestamp = datetime.fromtimestamp(taken_at).isoformat() if taken_at else 'unknown'
            
            # Check story type
            media_type = item.get('media_type', 1)  # 1=image, 2=video
            
            story_data = {
                'story_id': story_id,
                'timestamp': timestamp,
                'taken_at': taken_at,
                'media_type': 'image' if media_type == 1 else 'video',
                'username': username,
                'downloaded_file': None
            }
            
            # Get media URL
            if media_type == 1:  # Image
                media_url = item.get('image_versions2', {}).get('candidates', [{}])[0].get('url')
                if media_url:
                    filename = f"{username}_story_{story_id}_{index}.jpg"
                    downloaded_file = self.download_story_media(media_url, filename)
                    story_data['downloaded_file'] = downloaded_file
                    story_data['media_url'] = media_url
            
            elif media_type == 2:  # Video
                video_versions = item.get('video_versions', [])
                if video_versions:
                    media_url = video_versions[0].get('url')
                    if media_url:
                        filename = f"{username}_story_{story_id}_{index}.mp4"
                        downloaded_file = self.download_story_media(media_url, filename)
                        story_data['downloaded_file'] = downloaded_file
                        story_data['media_url'] = media_url
            
            # Get story text/caption if available
            if 'story_cta' in item:
                story_data['caption'] = item['story_cta'].get('text', '')
            
            # Check for close friends indicator
            if item.get('audience') == 'close_friends':
                story_data['is_close_friends'] = True
                print(f"   💚 Close Friends story detected!")
            
            return story_data
            
        except Exception as e:
            print(f"❌ Error processing story: {e}")
            return None
    
    def save_stories_metadata(self, stories_data):
        """Save stories metadata and download info"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"REAL_CLOSE_FRIENDS_STORIES_{timestamp}.json"
        
        # Count downloads
        total_downloaded = 0
        for user_stories in stories_data:
            for story in user_stories['stories']:
                if story.get('downloaded_file'):
                    total_downloaded += 1
        
        output_data = {
            'extraction_timestamp': datetime.now().isoformat(),
            'target_account': 'alx.trading',
            'extraction_method': 'REAL_INSTAGRAM_API',
            'is_real_data': True,
            'is_mockup': False,
            'download_directory': self.download_dir,
            'summary': {
                'total_users_with_stories': len(stories_data),
                'total_stories_found': sum(len(user['stories']) for user in stories_data),
                'total_downloaded': total_downloaded,
                'close_friends_stories': len([user for user in stories_data if user.get('is_close_friend')])
            },
            'stories_data': stories_data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Stories metadata saved: {filename}")
        return filename
    
    def create_download_archive(self):
        """Create zip archive of downloaded stories"""
        try:
            import zipfile
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"close_friends_stories_download_{timestamp}.zip"
            
            with zipfile.ZipFile(archive_name, 'w') as zipf:
                for root, dirs, files in os.walk(self.download_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, self.download_dir)
                        zipf.write(file_path, arcname)
                        print(f"📦 Added to archive: {arcname}")
            
            print(f"✅ Archive created: {archive_name}")
            return archive_name
            
        except Exception as e:
            print(f"❌ Archive creation failed: {e}")
            return None

def main():
    print("📸 REAL CLOSE FRIENDS STORIES DOWNLOADER")
    print("=" * 60)
    print("🎯 Downloading actual stories from Instagram account")
    print("🚫 NO MOCKUP - REAL EXTRACTION & DOWNLOAD")
    print("=" * 60)
    
    downloader = RealStoriesDownloader()
    
    # Extract stories
    stories_data = downloader.extract_close_friends_stories()
    
    if stories_data:
        # Save metadata
        metadata_file = downloader.save_stories_metadata(stories_data)
        
        # Create download archive
        archive_file = downloader.create_download_archive()
        
        print(f"\n🎯 STORIES EXTRACTION COMPLETE")
        print("=" * 60)
        print(f"👥 Users with stories: {len(stories_data)}")
        
        total_stories = sum(len(user['stories']) for user in stories_data)
        total_downloaded = sum(1 for user in stories_data for story in user['stories'] if story.get('downloaded_file'))
        close_friends_count = len([user for user in stories_data if user.get('is_close_friend')])
        
        print(f"📸 Total stories found: {total_stories}")
        print(f"⬬ Successfully downloaded: {total_downloaded}")
        print(f"💚 Close friends stories: {close_friends_count}")
        
        if archive_file:
            print(f"📦 Download archive: {archive_file}")
        
        print(f"\n📁 Files location:")
        print(f"   📊 Metadata: {metadata_file}")
        print(f"   📁 Media files: {downloader.download_dir}/")
        
        # Show breakdown by user
        for user_data in stories_data:
            username = user_data['username']
            story_count = len(user_data['stories'])
            is_close_friend = "💚" if user_data.get('is_close_friend') else "👤"
            print(f"   {is_close_friend} {username}: {story_count} stories")
    
    else:
        print("\n📊 STORIES EXTRACTION COMPLETE")
        print("=" * 60)
        print("❌ NO STORIES FOUND")
        print()
        print("📈 Possible reasons:")
        print("   📱 No active stories at this time")
        print("   🔒 Stories may be private/restricted")
        print("   ⏰ Stories may have expired (24h limit)")
        print("   🚫 Account may not follow users with stories")

if __name__ == "__main__":
    main()
