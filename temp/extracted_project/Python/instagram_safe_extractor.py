#!/usr/bin/env python3
"""
Instagram Safe Data Extractor - เครื่องมือสกัดข้อมูลปลอดภัย
สำหรับการอ่าน DMs, Stories, และ Posts โดยไม่โดน checkpoint

🎯 Target: alx.trading
🔐 Method: instagrapi + sessionid (NO BROWSER LOGIN)
🛡️ Safety: Checkpoint avoidance, natural delays, error handling
"""

import json
import time
import random
import os
from datetime import datetime
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired, PleaseWaitFewMinutes
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InstagramSafeExtractor:
    def __init__(self, session_file="session.json"):
        """Initialize safe Instagram extractor"""
        self.cl = Client()
        self.session_file = session_file
        self.target_username = "alx.trading"
        self.extracted_data = {
            "timestamp": datetime.now().isoformat(),
            "target": self.target_username,
            "status": "initialized",
            "data": {
                "direct_messages": [],
                "stories": [],
                "posts": [],
                "followers": [],
                "following": [],
                "user_info": {}
            },
            "errors": [],
            "extraction_summary": {}
        }
        
    def load_session(self):
        """Load existing session data safely"""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    session_data = json.load(f)
                
                # Set session using sessionid
                if 'sessionid' in session_data:
                    self.cl.set_settings({
                        "sessionid": session_data['sessionid'],
                        "ds_user_id": session_data.get('ds_user_id', '')
                    })
                    logger.info("✅ Session loaded successfully")
                    return True
                else:
                    logger.error("❌ No sessionid found in session file")
                    return False
            else:
                logger.error(f"❌ Session file {self.session_file} not found")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to load session: {str(e)}")
            self.extracted_data["errors"].append(f"Session load error: {str(e)}")
            return False
    
    def safe_delay(self, min_seconds=2, max_seconds=8):
        """Add random delay to avoid detection"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        logger.info(f"⏳ Safety delay: {delay:.2f}s")
    
    def get_user_info(self):
        """Get target user information safely"""
        try:
            logger.info(f"🔍 Getting user info for {self.target_username}")
            self.safe_delay()
            
            user_info = self.cl.user_info_by_username(self.target_username)
            
            self.extracted_data["data"]["user_info"] = {
                "user_id": str(user_info.pk),
                "username": user_info.username,
                "full_name": user_info.full_name,
                "biography": user_info.biography,
                "followers_count": user_info.follower_count,
                "following_count": user_info.following_count,
                "media_count": user_info.media_count,
                "is_private": user_info.is_private,
                "is_verified": user_info.is_verified,
                "profile_pic_url": user_info.profile_pic_url
            }
            
            logger.info(f"✅ User info extracted: {user_info.username} ({user_info.follower_count} followers)")
            return user_info
            
        except Exception as e:
            error_msg = f"Failed to get user info: {str(e)}"
            logger.error(f"❌ {error_msg}")
            self.extracted_data["errors"].append(error_msg)
            return None
    
    def extract_direct_messages(self, limit=50):
        """Extract direct messages safely"""
        try:
            logger.info("💬 Extracting direct messages...")
            self.safe_delay(3, 10)
            
            # Get direct message threads
            threads = self.cl.direct_threads(amount=limit)
            
            dm_data = []
            for thread in threads:
                self.safe_delay(1, 3)  # Delay between threads
                
                thread_info = {
                    "thread_id": thread.id,
                    "thread_title": thread.thread_title,
                    "users": [{"username": user.username, "full_name": user.full_name} for user in thread.users],
                    "last_activity": thread.last_activity_at.isoformat() if thread.last_activity_at else None,
                    "messages": []
                }
                
                # Get messages from this thread
                try:
                    messages = self.cl.direct_messages(thread.id, amount=20)
                    for msg in messages:
                        message_data = {
                            "message_id": msg.id,
                            "user_id": str(msg.user_id),
                            "timestamp": msg.timestamp.isoformat(),
                            "text": msg.text,
                            "message_type": msg.item_type
                        }
                        thread_info["messages"].append(message_data)
                except Exception as e:
                    logger.warning(f"⚠️ Could not extract messages from thread {thread.id}: {str(e)}")
                
                dm_data.append(thread_info)
            
            self.extracted_data["data"]["direct_messages"] = dm_data
            logger.info(f"✅ Extracted {len(dm_data)} DM threads")
            
        except Exception as e:
            error_msg = f"Failed to extract DMs: {str(e)}"
            logger.error(f"❌ {error_msg}")
            self.extracted_data["errors"].append(error_msg)
    
    def extract_stories(self):
        """Extract available stories safely"""
        try:
            logger.info("📖 Extracting stories...")
            self.safe_delay(2, 6)
            
            # Get user ID first
            user_info = self.cl.user_info_by_username(self.target_username)
            user_id = user_info.pk
            
            # Get stories
            stories = self.cl.user_stories(user_id)
            
            story_data = []
            for story in stories:
                self.safe_delay(1, 3)
                
                story_info = {
                    "story_id": story.id,
                    "media_type": story.media_type,
                    "timestamp": story.taken_at.isoformat(),
                    "image_url": story.thumbnail_url if hasattr(story, 'thumbnail_url') else None,
                    "video_url": story.video_url if hasattr(story, 'video_url') else None,
                    "viewers_count": getattr(story, 'viewer_count', 0),
                    "story_type": str(story.media_type)
                }
                story_data.append(story_info)
            
            self.extracted_data["data"]["stories"] = story_data
            logger.info(f"✅ Extracted {len(story_data)} stories")
            
        except Exception as e:
            error_msg = f"Failed to extract stories: {str(e)}"
            logger.error(f"❌ {error_msg}")
            self.extracted_data["errors"].append(error_msg)
    
    def extract_recent_posts(self, limit=20):
        """Extract recent posts safely"""
        try:
            logger.info("📸 Extracting recent posts...")
            self.safe_delay(3, 8)
            
            # Get user ID
            user_info = self.cl.user_info_by_username(self.target_username)
            user_id = user_info.pk
            
            # Get recent posts
            posts = self.cl.user_medias(user_id, amount=limit)
            
            post_data = []
            for post in posts:
                self.safe_delay(1, 3)
                
                post_info = {
                    "post_id": post.id,
                    "media_type": post.media_type,
                    "timestamp": post.taken_at.isoformat(),
                    "caption": post.caption_text if post.caption_text else "",
                    "like_count": post.like_count,
                    "comment_count": post.comment_count,
                    "image_url": post.thumbnail_url,
                    "is_video": post.media_type == 2,
                    "location": post.location.name if post.location else None,
                    "hashtags": [tag for tag in (post.caption_text or "").split() if tag.startswith('#')]
                }
                
                # Get comments if any
                try:
                    if post.comment_count > 0:
                        comments = self.cl.media_comments(post.id, amount=5)
                        post_info["recent_comments"] = [
                            {
                                "user": comment.user.username,
                                "text": comment.text,
                                "timestamp": comment.created_at.isoformat()
                            } for comment in comments
                        ]
                except Exception as e:
                    logger.warning(f"⚠️ Could not get comments for post {post.id}")
                
                post_data.append(post_info)
            
            self.extracted_data["data"]["posts"] = post_data
            logger.info(f"✅ Extracted {len(post_data)} posts")
            
        except Exception as e:
            error_msg = f"Failed to extract posts: {str(e)}"
            logger.error(f"❌ {error_msg}")
            self.extracted_data["errors"].append(error_msg)
    
    def extract_followers_following(self, limit=100):
        """Extract followers and following lists safely"""
        try:
            logger.info("👥 Extracting followers/following...")
            self.safe_delay(3, 8)
            
            # Get user ID
            user_info = self.cl.user_info_by_username(self.target_username)
            user_id = user_info.pk
            
            # Extract followers
            try:
                followers = self.cl.user_followers(user_id, amount=limit)
                follower_data = []
                for user_id, user_info in followers.items():
                    follower_data.append({
                        "user_id": str(user_id),
                        "username": user_info.username,
                        "full_name": user_info.full_name,
                        "is_verified": user_info.is_verified,
                        "follower_count": user_info.follower_count
                    })
                    self.safe_delay(0.5, 1.5)  # Short delay between users
                
                self.extracted_data["data"]["followers"] = follower_data
                logger.info(f"✅ Extracted {len(follower_data)} followers")
            except Exception as e:
                logger.warning(f"⚠️ Could not extract followers: {str(e)}")
            
            # Extract following
            try:
                following = self.cl.user_following(user_id, amount=limit)
                following_data = []
                for user_id, user_info in following.items():
                    following_data.append({
                        "user_id": str(user_id),
                        "username": user_info.username,
                        "full_name": user_info.full_name,
                        "is_verified": user_info.is_verified,
                        "follower_count": user_info.follower_count
                    })
                    self.safe_delay(0.5, 1.5)
                
                self.extracted_data["data"]["following"] = following_data
                logger.info(f"✅ Extracted {len(following_data)} following")
            except Exception as e:
                logger.warning(f"⚠️ Could not extract following: {str(e)}")
                
        except Exception as e:
            error_msg = f"Failed to extract followers/following: {str(e)}"
            logger.error(f"❌ {error_msg}")
            self.extracted_data["errors"].append(error_msg)
    
    def run_safe_extraction(self):
        """Run complete safe extraction process"""
        logger.info("🚀 Starting Instagram safe data extraction")
        
        # Load session
        if not self.load_session():
            self.extracted_data["status"] = "failed_session_load"
            return self.extracted_data
        
        try:
            # Test session validity
            self.cl.account_info()
            logger.info("✅ Session is valid")
            
            # Extract data step by step
            self.get_user_info()
            self.safe_delay(5, 12)
            
            self.extract_direct_messages()
            self.safe_delay(8, 15)
            
            self.extract_stories()
            self.safe_delay(5, 10)
            
            self.extract_recent_posts()
            self.safe_delay(8, 15)
            
            self.extract_followers_following()
            
            # Generate summary
            self.extracted_data["extraction_summary"] = {
                "total_dms": len(self.extracted_data["data"]["direct_messages"]),
                "total_stories": len(self.extracted_data["data"]["stories"]),
                "total_posts": len(self.extracted_data["data"]["posts"]),
                "total_followers": len(self.extracted_data["data"]["followers"]),
                "total_following": len(self.extracted_data["data"]["following"]),
                "errors_count": len(self.extracted_data["errors"])
            }
            
            self.extracted_data["status"] = "completed"
            logger.info("🎉 Safe extraction completed successfully!")
            
        except LoginRequired:
            error_msg = "Session expired - login required"
            logger.error(f"❌ {error_msg}")
            self.extracted_data["status"] = "session_expired"
            self.extracted_data["errors"].append(error_msg)
            
        except ChallengeRequired:
            error_msg = "Challenge required - account flagged"
            logger.error(f"❌ {error_msg}")
            self.extracted_data["status"] = "challenge_required"
            self.extracted_data["errors"].append(error_msg)
            
        except PleaseWaitFewMinutes:
            error_msg = "Rate limited - please wait"
            logger.error(f"❌ {error_msg}")
            self.extracted_data["status"] = "rate_limited"
            self.extracted_data["errors"].append(error_msg)
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(f"❌ {error_msg}")
            self.extracted_data["status"] = "error"
            self.extracted_data["errors"].append(error_msg)
        
        return self.extracted_data
    
    def save_results(self, filename=None):
        """Save extraction results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"instagram_safe_extraction_{self.target_username}_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.extracted_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Results saved to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"❌ Failed to save results: {str(e)}")
            return None

def main():
    """Main execution function"""
    print("🎯 Instagram Safe Data Extractor")
    print("=" * 50)
    print("Target: alx.trading")
    print("Method: instagrapi + sessionid (NO BROWSER)")
    print("Safety: Checkpoint avoidance enabled")
    print("=" * 50)
    
    # Initialize extractor
    extractor = InstagramSafeExtractor()
    
    # Run extraction
    results = extractor.run_safe_extraction()
    
    # Save results
    output_file = extractor.save_results()
    
    # Print summary
    print("\n📊 EXTRACTION SUMMARY")
    print("=" * 30)
    print(f"Status: {results['status']}")
    print(f"Target: {results['target']}")
    
    if results['status'] == 'completed':
        summary = results['extraction_summary']
        print(f"✅ DMs: {summary['total_dms']}")
        print(f"✅ Stories: {summary['total_stories']}")
        print(f"✅ Posts: {summary['total_posts']}")
        print(f"✅ Followers: {summary['total_followers']}")
        print(f"✅ Following: {summary['total_following']}")
        
        if summary['errors_count'] > 0:
            print(f"⚠️  Errors: {summary['errors_count']}")
    else:
        print(f"❌ Status: {results['status']}")
        if results['errors']:
            print("Errors:")
            for error in results['errors']:
                print(f"  - {error}")
    
    if output_file:
        print(f"\n💾 Results saved to: {output_file}")
    
    print("\n🛡️ Safe extraction completed!")

if __name__ == "__main__":
    main()
