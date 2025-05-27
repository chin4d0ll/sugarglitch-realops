#!/usr/bin/env python3
"""
🐍 INSTAGRAPI INSTAGRAM EXTRACTOR
=================================
Python API-based Instagram data extraction
Target: alx.trading profile
"""

import json
import time
import os
from datetime import datetime
from pathlib import Path
import requests
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired, ClientError
import logging

class InstagrapiExtractor:
    def __init__(self, output_dir=None):
        self.target_username = "alx.trading"
        self.target_user_id = "4976283726"
        self.sessionid = "4976283726%3A1JgRzA56Q8e8Qs%3A12"
        self.ds_user_id = "4976283726"
        
        self.output_dir = Path(output_dir) if output_dir else Path("instagrapi_extraction")
        self.setup_directories()
        
        # Initialize client
        self.client = Client()
        self.client.delay_range = [1, 3]
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        print("🐍 INSTAGRAPI EXTRACTOR INITIALIZED")
        print(f"📁 Output Directory: {self.output_dir}")
        print(f"🎯 Target: {self.target_username} (ID: {self.target_user_id})")
        
    def setup_directories(self):
        """Setup organized directory structure"""
        directories = [
            'data',
            'media/images',
            'media/videos',
            'media/stories',
            'logs'
        ]
        
        for directory in directories:
            (self.output_dir / directory).mkdir(parents=True, exist_ok=True)
            
        print(f"📁 Directory structure created: {self.output_dir}")
        
    def setup_session(self):
        """Setup session using sessionid"""
        print("🔧 Setting up Instagrapi session...")
        
        try:
            # Set session
            self.client.set_settings({
                "sessionid": self.sessionid,
                "ds_user_id": self.ds_user_id,
                "user_agent": "Instagram 219.0.0.12.117 Android",
            })
            
            # Try to get account info to verify session
            account_info = self.client.account_info()
            print(f"✅ Session verified! Logged in as: {account_info.username}")
            
            # Save session for future use
            session_file = self.output_dir / "session.json"
            self.client.dump_settings(session_file)
            
            return True
            
        except Exception as e:
            print(f"❌ Session setup failed: {e}")
            return False
            
    def extract_user_info(self):
        """Extract detailed user information"""
        print("📊 Extracting user information...")
        
        try:
            # Get user ID
            user_id = self.client.user_id_from_username(self.target_username)
            
            # Get user info
            user_info = self.client.user_info(user_id)
            
            # Convert to dict and make serializable
            user_data = {
                'user_id': str(user_info.pk),
                'username': user_info.username,
                'full_name': user_info.full_name,
                'biography': user_info.biography,
                'external_url': user_info.external_url,
                'follower_count': user_info.follower_count,
                'following_count': user_info.following_count,
                'media_count': user_info.media_count,
                'is_private': user_info.is_private,
                'is_verified': user_info.is_verified,
                'is_business': user_info.is_business,
                'profile_pic_url': str(user_info.profile_pic_url),
                'profile_pic_url_hd': str(user_info.profile_pic_url_hd) if hasattr(user_info, 'profile_pic_url_hd') else None,
                'category': user_info.category,
                'business_category_name': getattr(user_info, 'business_category_name', None),
                'contact_phone_number': getattr(user_info, 'contact_phone_number', None),
                'public_email': getattr(user_info, 'public_email', None),
                'extracted_at': datetime.now().isoformat()
            }
            
            # Save user info
            output_file = self.output_dir / "data" / "user_info.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=2, ensure_ascii=False)
                
            print(f"✅ User information extracted: {user_data['follower_count']} followers, {user_data['following_count']} following")
            return user_data
            
        except Exception as e:
            print(f"❌ Error extracting user info: {e}")
            return None
            
    def extract_posts(self, count=50):
        """Extract user posts"""
        print(f"📷 Extracting {count} posts...")
        
        try:
            # Get user ID
            user_id = self.client.user_id_from_username(self.target_username)
            
            # Get user medias
            medias = self.client.user_medias(user_id, amount=count)
            
            posts_data = []
            for i, media in enumerate(medias):
                print(f"Processing post {i+1}/{len(medias)}...")
                
                post_data = {
                    'id': str(media.pk),
                    'code': media.code,
                    'taken_at': media.taken_at.isoformat() if media.taken_at else None,
                    'media_type': media.media_type,
                    'thumbnail_url': str(media.thumbnail_url) if media.thumbnail_url else None,
                    'caption': media.caption_text if hasattr(media, 'caption_text') else None,
                    'like_count': media.like_count,
                    'comment_count': media.comment_count,
                    'view_count': getattr(media, 'view_count', None),
                    'play_count': getattr(media, 'play_count', None),
                    'location': media.location.dict() if media.location else None,
                    'user_tags': [tag.dict() for tag in media.usertags] if hasattr(media, 'usertags') and media.usertags else [],
                    'hashtags': getattr(media, 'hashtags', []),
                    'mentions': getattr(media, 'mentions', []),
                    'is_paid_partnership': getattr(media, 'is_paid_partnership', False),
                    'url': f"https://www.instagram.com/p/{media.code}/",
                }
                
                # Download media if it's an image or video
                try:
                    if media.media_type == 1:  # Photo
                        photo_path = self.client.photo_download(media.pk, folder=self.output_dir / "media" / "images")
                        post_data['local_path'] = str(photo_path)
                    elif media.media_type == 2:  # Video
                        video_path = self.client.video_download(media.pk, folder=self.output_dir / "media" / "videos")
                        post_data['local_path'] = str(video_path)
                    elif media.media_type == 8:  # Carousel
                        carousel_paths = []
                        for resource in media.resources:
                            if resource.media_type == 1:
                                path = self.client.photo_download(resource.pk, folder=self.output_dir / "media" / "images")
                            else:
                                path = self.client.video_download(resource.pk, folder=self.output_dir / "media" / "videos")
                            carousel_paths.append(str(path))
                        post_data['local_paths'] = carousel_paths
                        
                except Exception as e:
                    print(f"⚠️ Failed to download media for post {media.code}: {e}")
                    post_data['download_error'] = str(e)
                
                posts_data.append(post_data)
                time.sleep(0.5)  # Rate limiting
                
            # Save posts data
            output_file = self.output_dir / "data" / "posts.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(posts_data, f, indent=2, ensure_ascii=False)
                
            print(f"✅ Extracted {len(posts_data)} posts")
            return posts_data
            
        except Exception as e:
            print(f"❌ Error extracting posts: {e}")
            return []
            
    def extract_stories(self):
        """Extract user stories"""
        print("📚 Extracting stories...")
        
        try:
            # Get user ID
            user_id = self.client.user_id_from_username(self.target_username)
            
            # Get user stories
            stories = self.client.user_stories(user_id)
            
            stories_data = []
            for i, story in enumerate(stories):
                print(f"Processing story {i+1}/{len(stories)}...")
                
                story_data = {
                    'id': str(story.pk),
                    'taken_at': story.taken_at.isoformat() if story.taken_at else None,
                    'expiring_at': story.expiring_at.isoformat() if story.expiring_at else None,
                    'media_type': story.media_type,
                    'thumbnail_url': str(story.thumbnail_url) if story.thumbnail_url else None,
                    'view_count': getattr(story, 'view_count', None),
                    'story_hashtags': [tag.dict() for tag in story.story_hashtags] if hasattr(story, 'story_hashtags') and story.story_hashtags else [],
                    'story_locations': [loc.dict() for loc in story.story_locations] if hasattr(story, 'story_locations') and story.story_locations else [],
                    'story_mentions': [mention.dict() for mention in story.story_mentions] if hasattr(story, 'story_mentions') and story.story_mentions else [],
                    'story_stickers': [sticker.dict() for sticker in story.story_stickers] if hasattr(story, 'story_stickers') and story.story_stickers else [],
                }
                
                # Download story media
                try:
                    if story.media_type == 1:  # Photo
                        photo_path = self.client.photo_download(story.pk, folder=self.output_dir / "media" / "stories")
                        story_data['local_path'] = str(photo_path)
                    elif story.media_type == 2:  # Video
                        video_path = self.client.video_download(story.pk, folder=self.output_dir / "media" / "stories")
                        story_data['local_path'] = str(video_path)
                        
                except Exception as e:
                    print(f"⚠️ Failed to download story media: {e}")
                    story_data['download_error'] = str(e)
                
                stories_data.append(story_data)
                time.sleep(0.5)  # Rate limiting
                
            # Save stories data
            output_file = self.output_dir / "data" / "stories.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(stories_data, f, indent=2, ensure_ascii=False)
                
            print(f"✅ Extracted {len(stories_data)} stories")
            return stories_data
            
        except Exception as e:
            print(f"❌ Error extracting stories: {e}")
            return []
            
    def extract_followers(self, count=1000):
        """Extract followers list"""
        print(f"👥 Extracting {count} followers...")
        
        try:
            # Get user ID
            user_id = self.client.user_id_from_username(self.target_username)
            
            # Get followers
            followers = self.client.user_followers(user_id, amount=count)
            
            followers_data = []
            for user_id, user_info in followers.items():
                follower_data = {
                    'user_id': str(user_info.pk),
                    'username': user_info.username,
                    'full_name': user_info.full_name,
                    'profile_pic_url': str(user_info.profile_pic_url),
                    'is_private': user_info.is_private,
                    'is_verified': user_info.is_verified,
                    'follower_count': getattr(user_info, 'follower_count', None),
                    'following_count': getattr(user_info, 'following_count', None),
                    'media_count': getattr(user_info, 'media_count', None),
                }
                followers_data.append(follower_data)
                
            # Save followers data
            output_file = self.output_dir / "data" / "followers.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(followers_data, f, indent=2, ensure_ascii=False)
                
            print(f"✅ Extracted {len(followers_data)} followers")
            return followers_data
            
        except Exception as e:
            print(f"❌ Error extracting followers: {e}")
            return []
            
    def extract_following(self, count=1000):
        """Extract following list"""
        print(f"👤 Extracting {count} following...")
        
        try:
            # Get user ID
            user_id = self.client.user_id_from_username(self.target_username)
            
            # Get following
            following = self.client.user_following(user_id, amount=count)
            
            following_data = []
            for user_id, user_info in following.items():
                following_user_data = {
                    'user_id': str(user_info.pk),
                    'username': user_info.username,
                    'full_name': user_info.full_name,
                    'profile_pic_url': str(user_info.profile_pic_url),
                    'is_private': user_info.is_private,
                    'is_verified': user_info.is_verified,
                    'follower_count': getattr(user_info, 'follower_count', None),
                    'following_count': getattr(user_info, 'following_count', None),
                    'media_count': getattr(user_info, 'media_count', None),
                }
                following_data.append(following_user_data)
                
            # Save following data
            output_file = self.output_dir / "data" / "following.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(following_data, f, indent=2, ensure_ascii=False)
                
            print(f"✅ Extracted {len(following_data)} following")
            return following_data
            
        except Exception as e:
            print(f"❌ Error extracting following: {e}")
            return []
            
    def extract_highlights(self):
        """Extract story highlights"""
        print("⭐ Extracting story highlights...")
        
        try:
            # Get user ID
            user_id = self.client.user_id_from_username(self.target_username)
            
            # Get highlights
            highlights = self.client.user_highlights(user_id)
            
            highlights_data = []
            for highlight in highlights:
                highlight_data = {
                    'id': str(highlight.pk),
                    'title': highlight.title,
                    'cover_media_id': str(highlight.cover_media.pk) if highlight.cover_media else None,
                    'media_count': highlight.media_count,
                    'created_at': highlight.created_at.isoformat() if highlight.created_at else None,
                }
                
                # Get highlight stories
                highlight_stories = self.client.highlight_info(highlight.pk)
                highlight_data['stories'] = []
                
                for story in highlight_stories.items:
                    story_data = {
                        'id': str(story.pk),
                        'taken_at': story.taken_at.isoformat() if story.taken_at else None,
                        'media_type': story.media_type,
                        'thumbnail_url': str(story.thumbnail_url) if story.thumbnail_url else None,
                    }
                    highlight_data['stories'].append(story_data)
                    
                highlights_data.append(highlight_data)
                time.sleep(0.5)  # Rate limiting
                
            # Save highlights data
            output_file = self.output_dir / "data" / "highlights.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(highlights_data, f, indent=2, ensure_ascii=False)
                
            print(f"✅ Extracted {len(highlights_data)} highlights")
            return highlights_data
            
        except Exception as e:
            print(f"❌ Error extracting highlights: {e}")
            return []
            
    def run_full_extraction(self):
        """Run complete extraction process"""
        print("🚀 Starting full Instagrapi extraction...")
        
        if not self.setup_session():
            print("❌ Failed to setup session. Aborting.")
            return None
            
        results = {
            'user_info': self.extract_user_info(),
            'posts': self.extract_posts(50),
            'stories': self.extract_stories(),
            'followers': self.extract_followers(1000),
            'following': self.extract_following(1000),
            'highlights': self.extract_highlights(),
            'extraction_completed_at': datetime.now().isoformat()
        }
        
        # Save complete results
        output_file = self.output_dir / "complete_extraction.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            
        print("🎉 Instagrapi extraction completed successfully!")
        print(f"📊 Results saved to: {self.output_dir}")
        
        return results

if __name__ == "__main__":
    import sys
    output_dir = sys.argv[1] if len(sys.argv) > 1 else None
    
    extractor = InstagrapiExtractor(output_dir)
    extractor.run_full_extraction()
