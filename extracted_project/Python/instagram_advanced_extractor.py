#!/usr/bin/env python3
"""
Instagram Advanced Safe Extractor - เครื่องมือสกัดข้อมูลขั้นสูง
สำหรับการอ่าน DMs, Stories, Posts โดยไม่โดน checkpoint + Auto session refresh

🎯 Target: alx.trading
🔐 Method: instagrapi + auto session management
🛡️ Safety: Maximum stealth, checkpoint avoidance
"""

import json
import time
import random
import os
import sys
from datetime import datetime, timedelta
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired, PleaseWaitFewMinutes
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InstagramAdvancedExtractor:
    def __init__(self, session_file="session.json"):
        """Initialize advanced Instagram extractor"""
        self.cl = Client()
        self.session_file = session_file
        self.target_username = "alx.trading"
        self.username = "alx.trading"
        self.password = "Fleming654"
        
        # Configure client for maximum stealth
        self.setup_stealth_mode()
        
        self.extracted_data = {
            "timestamp": datetime.now().isoformat(),
            "target": self.target_username,
            "status": "initialized",
            "session_info": {},
            "data": {
                "account_info": {},
                "direct_messages": [],
                "stories": [],
                "posts": [],
                "liked_posts": [],
                "followers_sample": [],
                "following_sample": [],
                "recent_activity": [],
                "search_history": []
            },
            "errors": [],
            "extraction_summary": {},
            "stealth_metrics": {
                "total_delays": 0,
                "total_delay_time": 0,
                "requests_made": 0,
                "avg_delay": 0
            }
        }
        
    def setup_stealth_mode(self):
        """Configure client for maximum stealth"""
        # Realistic device settings
        settings = {
            "USER_AGENT": "Instagram 276.0.0.18.119 Android (30/11; 450dpi; 1080x2340; samsung; SM-G973F; beyond1; exynos9820; th_TH; 458229237)",
            "BUILD_VERSION": "276.0.0.18.119",
            "APP_VERSION": "276.0.0.18.119"
        }
        
        self.cl.set_settings(settings)
        self.cl.delay_range = [3, 12]  # Random delays between requests
        logger.info("🥷 Stealth mode activated")
    
    def stealth_delay(self, min_seconds=2, max_seconds=10, reason="general"):
        """Add intelligent stealth delays"""
        base_delay = random.uniform(min_seconds, max_seconds)
        
        # Add extra delay for sensitive operations
        if reason in ["login", "dm_access", "user_lookup"]:
            base_delay += random.uniform(5, 15)
        elif reason in ["story_view", "post_access"]:
            base_delay += random.uniform(2, 8)
        
        time.sleep(base_delay)
        
        # Update stealth metrics
        self.extracted_data["stealth_metrics"]["total_delays"] += 1
        self.extracted_data["stealth_metrics"]["total_delay_time"] += base_delay
        
        logger.info(f"🥷 Stealth delay ({reason}): {base_delay:.2f}s")
    
    def load_or_refresh_session(self):
        """Load existing session or create new one safely"""
        try:
            # Try loading existing session
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    session_data = json.load(f)
                
                # Check if session is recent (less than 24 hours old)
                if 'timestamp' in session_data:
                    session_time = datetime.fromisoformat(session_data['timestamp'])
                    if datetime.now() - session_time < timedelta(hours=24):
                        self.cl.set_settings(session_data)
                        
                        # Test session validity
                        try:
                            self.cl.account_info()
                            logger.info("✅ Existing session is valid")
                            self.extracted_data["session_info"] = {
                                "type": "existing",
                                "age_hours": (datetime.now() - session_time).total_seconds() / 3600,
                                "status": "valid"
                            }
                            return True
                        except:
                            logger.info("❌ Existing session expired")
            
            # Need fresh session
            logger.info("🔄 Creating fresh session...")
            return self.create_fresh_session()
            
        except Exception as e:
            logger.error(f"❌ Session management error: {str(e)}")
            return False
    
    def create_fresh_session(self):
        """Create fresh session with maximum safety"""
        try:
            logger.info("🔐 Attempting fresh login with stealth mode")
            
            # Pre-login stealth delay
            self.stealth_delay(10, 25, "login")
            
            # Attempt login
            result = self.cl.login(self.username, self.password)
            
            if result:
                logger.info("✅ Fresh login successful!")
                
                # Save session
                self.save_session_data()
                
                # Post-login stealth delay
                self.stealth_delay(15, 30, "login")
                
                self.extracted_data["session_info"] = {
                    "type": "fresh",
                    "created": datetime.now().isoformat(),
                    "status": "created"
                }
                
                return True
            else:
                logger.error("❌ Fresh login failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Fresh session creation failed: {str(e)}")
            self.extracted_data["errors"].append(f"Session creation error: {str(e)}")
            return False
    
    def save_session_data(self):
        """Save current session data"""
        try:
            settings = self.cl.get_settings()
            settings["timestamp"] = datetime.now().isoformat()
            settings["username"] = self.username
            
            with open(self.session_file, 'w') as f:
                json.dump(settings, f, indent=2)
            
            logger.info(f"💾 Session saved to {self.session_file}")
            
        except Exception as e:
            logger.error(f"❌ Failed to save session: {str(e)}")
    
    def extract_account_info(self):
        """Extract detailed account information"""
        try:
            logger.info("👤 Extracting account information...")
            self.stealth_delay(3, 8, "user_lookup")
            
            # Get own account info
            own_info = self.cl.account_info()
            
            # Get target user info (same user in this case)
            user_info = self.cl.user_info_by_username(self.target_username)
            
            account_data = {
                "user_id": str(user_info.pk),
                "username": user_info.username,
                "full_name": user_info.full_name,
                "biography": user_info.biography,
                "external_url": user_info.external_url,
                "followers_count": user_info.follower_count,
                "following_count": user_info.following_count,
                "media_count": user_info.media_count,
                "is_private": user_info.is_private,
                "is_verified": user_info.is_verified,
                "is_business": user_info.is_business,
                "category": user_info.category_name if hasattr(user_info, 'category_name') else None,
                "profile_pic_url": user_info.profile_pic_url,
                "account_type": str(user_info.account_type) if hasattr(user_info, 'account_type') else None
            }
            
            self.extracted_data["data"]["account_info"] = account_data
            logger.info(f"✅ Account info extracted: @{account_data['username']} ({account_data['followers_count']} followers)")
            
        except Exception as e:
            error_msg = f"Failed to extract account info: {str(e)}"
            logger.error(f"❌ {error_msg}")
            self.extracted_data["errors"].append(error_msg)
    
    def extract_direct_messages_advanced(self, limit=30):
        """Extract direct messages with advanced analysis"""
        try:
            logger.info("💬 Extracting direct messages (advanced)...")
            self.stealth_delay(5, 15, "dm_access")
            
            # Get DM threads
            threads = self.cl.direct_threads(amount=limit)
            
            dm_data = []
            for thread in threads:
                self.stealth_delay(2, 6, "dm_access")
                
                thread_info = {
                    "thread_id": thread.id,
                    "thread_title": thread.thread_title,
                    "thread_type": str(thread.thread_type),
                    "users": [],
                    "last_activity": thread.last_activity_at.isoformat() if thread.last_activity_at else None,
                    "message_count": 0,
                    "recent_messages": [],
                    "analysis": {}
                }
                
                # Extract user info
                for user in thread.users:
                    thread_info["users"].append({
                        "user_id": str(user.pk),
                        "username": user.username,
                        "full_name": user.full_name,
                        "is_verified": user.is_verified,
                        "profile_pic_url": user.profile_pic_url
                    })
                
                # Get recent messages
                try:
                    messages = self.cl.direct_messages(thread.id, amount=15)
                    thread_info["message_count"] = len(messages)
                    
                    for msg in messages[:10]:  # Analyze only recent 10
                        message_data = {
                            "message_id": msg.id,
                            "user_id": str(msg.user_id),
                            "timestamp": msg.timestamp.isoformat(),
                            "text": msg.text,
                            "message_type": msg.item_type,
                            "is_sent_by_viewer": msg.user_id == int(self.cl.user_id)
                        }
                        thread_info["recent_messages"].append(message_data)
                    
                    # Basic analysis
                    if messages:
                        thread_info["analysis"] = {
                            "total_messages": len(messages),
                            "last_message_date": messages[0].timestamp.isoformat(),
                            "conversation_active": (datetime.now() - messages[0].timestamp).days < 7,
                            "message_frequency": "high" if len(messages) > 10 else "low"
                        }
                        
                except Exception as e:
                    logger.warning(f"⚠️ Could not extract messages from thread {thread.id}: {str(e)}")
                
                dm_data.append(thread_info)
            
            self.extracted_data["data"]["direct_messages"] = dm_data
            logger.info(f"✅ Extracted {len(dm_data)} DM threads with advanced analysis")
            
        except Exception as e:
            error_msg = f"Failed to extract DMs: {str(e)}"
            logger.error(f"❌ {error_msg}")
            self.extracted_data["errors"].append(error_msg)
    
    def extract_stories_advanced(self):
        """Extract stories with metadata analysis"""
        try:
            logger.info("📖 Extracting stories (advanced)...")
            self.stealth_delay(3, 10, "story_view")
            
            user_info = self.cl.user_info_by_username(self.target_username)
            stories = self.cl.user_stories(user_info.pk)
            
            story_data = []
            for story in stories:
                self.stealth_delay(2, 5, "story_view")
                
                story_info = {
                    "story_id": story.id,
                    "media_type": story.media_type,
                    "timestamp": story.taken_at.isoformat(),
                    "expiring_at": story.expiring_at.isoformat() if hasattr(story, 'expiring_at') else None,
                    "image_url": story.thumbnail_url if hasattr(story, 'thumbnail_url') else None,
                    "video_url": story.video_url if hasattr(story, 'video_url') else None,
                    "viewers_count": getattr(story, 'viewer_count', 0),
                    "story_type": str(story.media_type),
                    "has_audio": getattr(story, 'has_audio', False),
                    "duration": getattr(story, 'video_duration', 0) if story.media_type == 2 else None
                }
                story_data.append(story_info)
            
            self.extracted_data["data"]["stories"] = story_data
            logger.info(f"✅ Extracted {len(story_data)} stories with metadata")
            
        except Exception as e:
            error_msg = f"Failed to extract stories: {str(e)}"
            logger.error(f"❌ {error_msg}")
            self.extracted_data["errors"].append(error_msg)
    
    def extract_posts_advanced(self, limit=25):
        """Extract posts with engagement analysis"""
        try:
            logger.info("📸 Extracting posts (advanced)...")
            self.stealth_delay(4, 12, "post_access")
            
            user_info = self.cl.user_info_by_username(self.target_username)
            posts = self.cl.user_medias(user_info.pk, amount=limit)
            
            post_data = []
            for post in posts:
                self.stealth_delay(2, 6, "post_access")
                
                post_info = {
                    "post_id": post.id,
                    "media_type": post.media_type,
                    "timestamp": post.taken_at.isoformat(),
                    "caption": post.caption_text if post.caption_text else "",
                    "like_count": post.like_count,
                    "comment_count": post.comment_count,
                    "image_url": post.thumbnail_url,
                    "is_video": post.media_type == 2,
                    "video_duration": getattr(post, 'video_duration', 0) if post.media_type == 2 else None,
                    "location": {
                        "name": post.location.name,
                        "address": getattr(post.location, 'address', ''),
                        "lat": getattr(post.location, 'lat', 0),
                        "lng": getattr(post.location, 'lng', 0)
                    } if post.location else None,
                    "hashtags": [tag for tag in (post.caption_text or "").split() if tag.startswith('#')],
                    "mentions": [tag for tag in (post.caption_text or "").split() if tag.startswith('@')],
                    "engagement_rate": round((post.like_count + post.comment_count) / max(user_info.follower_count, 1) * 100, 2),
                    "recent_comments": [],
                    "analysis": {}
                }
                
                # Get top comments
                try:
                    if post.comment_count > 0:
                        comments = self.cl.media_comments(post.id, amount=5)
                        for comment in comments:
                            post_info["recent_comments"].append({
                                "user": comment.user.username,
                                "text": comment.text,
                                "timestamp": comment.created_at.isoformat(),
                                "like_count": comment.comment_like_count
                            })
                except Exception as e:
                    logger.warning(f"⚠️ Could not get comments for post {post.id}")
                
                # Post performance analysis
                post_info["analysis"] = {
                    "performance": "high" if post_info["engagement_rate"] > 5 else "medium" if post_info["engagement_rate"] > 2 else "low",
                    "content_type": "video" if post.media_type == 2 else "photo",
                    "has_location": post.location is not None,
                    "hashtag_count": len(post_info["hashtags"]),
                    "mention_count": len(post_info["mentions"])
                }
                
                post_data.append(post_info)
            
            self.extracted_data["data"]["posts"] = post_data
            logger.info(f"✅ Extracted {len(post_data)} posts with engagement analysis")
            
        except Exception as e:
            error_msg = f"Failed to extract posts: {str(e)}"
            logger.error(f"❌ {error_msg}")
            self.extracted_data["errors"].append(error_msg)
    
    def extract_liked_posts(self, limit=20):
        """Extract recently liked posts"""
        try:
            logger.info("❤️ Extracting liked posts...")
            self.stealth_delay(3, 8, "post_access")
            
            liked_posts = self.cl.user_medias_liked(amount=limit)
            
            liked_data = []
            for post in liked_posts:
                self.stealth_delay(1, 3, "post_access")
                
                liked_info = {
                    "post_id": post.id,
                    "owner": {
                        "username": post.user.username,
                        "full_name": post.user.full_name,
                        "is_verified": post.user.is_verified
                    },
                    "timestamp": post.taken_at.isoformat(),
                    "caption": post.caption_text[:200] if post.caption_text else "",
                    "like_count": post.like_count,
                    "comment_count": post.comment_count,
                    "media_type": post.media_type,
                    "image_url": post.thumbnail_url
                }
                liked_data.append(liked_info)
            
            self.extracted_data["data"]["liked_posts"] = liked_data
            logger.info(f"✅ Extracted {len(liked_data)} liked posts")
            
        except Exception as e:
            error_msg = f"Failed to extract liked posts: {str(e)}"
            logger.error(f"❌ {error_msg}")
            self.extracted_data["errors"].append(error_msg)
    
    def extract_network_sample(self, limit=50):
        """Extract sample of followers/following for network analysis"""
        try:
            logger.info("👥 Extracting network sample...")
            self.stealth_delay(5, 15, "user_lookup")
            
            user_info = self.cl.user_info_by_username(self.target_username)
            user_id = user_info.pk
            
            # Sample followers
            try:
                followers = self.cl.user_followers(user_id, amount=limit)
                follower_data = []
                
                for uid, user in list(followers.items())[:limit]:
                    self.stealth_delay(1, 3, "user_lookup")
                    
                    follower_data.append({
                        "user_id": str(uid),
                        "username": user.username,
                        "full_name": user.full_name,
                        "is_verified": user.is_verified,
                        "follower_count": user.follower_count,
                        "following_count": user.following_count,
                        "is_private": user.is_private,
                        "profile_pic_url": user.profile_pic_url
                    })
                
                self.extracted_data["data"]["followers_sample"] = follower_data
                logger.info(f"✅ Extracted {len(follower_data)} follower samples")
                
            except Exception as e:
                logger.warning(f"⚠️ Could not extract followers: {str(e)}")
            
            # Sample following
            try:
                following = self.cl.user_following(user_id, amount=limit)
                following_data = []
                
                for uid, user in list(following.items())[:limit]:
                    self.stealth_delay(1, 3, "user_lookup")
                    
                    following_data.append({
                        "user_id": str(uid),
                        "username": user.username,
                        "full_name": user.full_name,
                        "is_verified": user.is_verified,
                        "follower_count": user.follower_count,
                        "following_count": user.following_count,
                        "is_private": user.is_private,
                        "profile_pic_url": user.profile_pic_url
                    })
                
                self.extracted_data["data"]["following_sample"] = following_data
                logger.info(f"✅ Extracted {len(following_data)} following samples")
                
            except Exception as e:
                logger.warning(f"⚠️ Could not extract following: {str(e)}")
                
        except Exception as e:
            error_msg = f"Failed to extract network sample: {str(e)}"
            logger.error(f"❌ {error_msg}")
            self.extracted_data["errors"].append(error_msg)
    
    def run_advanced_extraction(self):
        """Run complete advanced extraction process"""
        logger.info("🚀 Starting Instagram advanced data extraction")
        start_time = time.time()
        
        # Load or refresh session
        if not self.load_or_refresh_session():
            self.extracted_data["status"] = "session_failed"
            return self.extracted_data
        
        try:
            # Test session and get basic info
            self.cl.account_info()
            logger.info("✅ Session validated successfully")
            
            # Extract data progressively with stealth delays
            self.extract_account_info()
            self.stealth_delay(8, 20, "general")
            
            self.extract_direct_messages_advanced()
            self.stealth_delay(10, 25, "general")
            
            self.extract_stories_advanced()
            self.stealth_delay(8, 18, "general")
            
            self.extract_posts_advanced()
            self.stealth_delay(10, 20, "general")
            
            self.extract_liked_posts()
            self.stealth_delay(8, 15, "general")
            
            self.extract_network_sample()
            
            # Calculate final metrics
            total_time = time.time() - start_time
            stealth_metrics = self.extracted_data["stealth_metrics"]
            stealth_metrics["total_extraction_time"] = total_time
            stealth_metrics["avg_delay"] = stealth_metrics["total_delay_time"] / max(stealth_metrics["total_delays"], 1)
            
            # Generate comprehensive summary
            self.extracted_data["extraction_summary"] = {
                "total_extraction_time_minutes": round(total_time / 60, 2),
                "account_info_extracted": bool(self.extracted_data["data"]["account_info"]),
                "total_dm_threads": len(self.extracted_data["data"]["direct_messages"]),
                "total_stories": len(self.extracted_data["data"]["stories"]),
                "total_posts": len(self.extracted_data["data"]["posts"]),
                "total_liked_posts": len(self.extracted_data["data"]["liked_posts"]),
                "follower_samples": len(self.extracted_data["data"]["followers_sample"]),
                "following_samples": len(self.extracted_data["data"]["following_sample"]),
                "errors_count": len(self.extracted_data["errors"]),
                "stealth_delays_used": stealth_metrics["total_delays"],
                "avg_delay_seconds": round(stealth_metrics["avg_delay"], 2)
            }
            
            self.extracted_data["status"] = "completed"
            logger.info("🎉 Advanced extraction completed successfully!")
            
        except LoginRequired:
            error_msg = "Session expired during extraction"
            logger.error(f"❌ {error_msg}")
            self.extracted_data["status"] = "session_expired"
            self.extracted_data["errors"].append(error_msg)
            
        except ChallengeRequired:
            error_msg = "Challenge required - account flagged"
            logger.error(f"❌ {error_msg}")
            self.extracted_data["status"] = "challenge_required"
            self.extracted_data["errors"].append(error_msg)
            
        except PleaseWaitFewMinutes:
            error_msg = "Rate limited - extraction paused"
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
            filename = f"instagram_advanced_extraction_{self.target_username}_{timestamp}.json"
        
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
    print("🎯 Instagram Advanced Safe Data Extractor")
    print("=" * 55)
    print("Target: alx.trading")
    print("Method: instagrapi + Advanced Session Management")
    print("Safety: Maximum Stealth + Checkpoint Avoidance")
    print("Features: DMs, Stories, Posts, Network, Engagement Analysis")
    print("=" * 55)
    
    # Initialize extractor
    extractor = InstagramAdvancedExtractor()
    
    # Run extraction
    results = extractor.run_advanced_extraction()
    
    # Save results
    output_file = extractor.save_results()
    
    # Print comprehensive summary
    print("\n📊 ADVANCED EXTRACTION SUMMARY")
    print("=" * 40)
    print(f"Status: {results['status']}")
    print(f"Target: {results['target']}")
    print(f"Session: {results['session_info'].get('type', 'unknown')}")
    
    if results['status'] == 'completed':
        summary = results['extraction_summary']
        print(f"\n✅ EXTRACTED DATA:")
        print(f"   • Account Info: {'Yes' if summary['account_info_extracted'] else 'No'}")
        print(f"   • DM Threads: {summary['total_dm_threads']}")
        print(f"   • Stories: {summary['total_stories']}")
        print(f"   • Posts: {summary['total_posts']}")
        print(f"   • Liked Posts: {summary['total_liked_posts']}")
        print(f"   • Follower Samples: {summary['follower_samples']}")
        print(f"   • Following Samples: {summary['following_samples']}")
        
        print(f"\n🥷 STEALTH METRICS:")
        print(f"   • Total Time: {summary['total_extraction_time_minutes']} minutes")
        print(f"   • Stealth Delays: {summary['stealth_delays_used']}")
        print(f"   • Avg Delay: {summary['avg_delay_seconds']}s")
        
        if summary['errors_count'] > 0:
            print(f"\n⚠️  Errors: {summary['errors_count']}")
    else:
        print(f"❌ Status: {results['status']}")
        if results['errors']:
            print("Errors:")
            for error in results['errors']:
                print(f"  - {error}")
    
    if output_file:
        print(f"\n💾 Results saved to: {output_file}")
    
    print("\n🛡️ Advanced safe extraction completed!")

if __name__ == "__main__":
    main()
