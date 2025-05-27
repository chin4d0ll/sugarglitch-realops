#!/usr/bin/env python3
"""
🕵️ INSTAGRAM STEALTH DATA EXTRACTOR
การดึงข้อมูล Instagram แบบปลอดภัย - ไม่โดน checkpoint!
Target: alx.trading - Safe DMs, Stories, Posts extraction using instagrapi
"""

import json
import time
import sys
import os
from datetime import datetime
from instagrapi import Client
import traceback

def safe_print(*args, **kwargs):
    try:
        print(*args, **kwargs)
        sys.stdout.flush()
    except (BrokenPipeError, IOError):
        sys.exit(1)

class InstagramStealthExtractor:
    def __init__(self, target_username="alx.trading"):
        self.target_username = target_username
        self.client = None
        self.session_data = None
        self.extracted_data = {
            "target_info": {},
            "direct_messages": [],
            "stories": [],
            "posts": [],
            "followers": [],
            "following": [],
            "media_data": []
        }
        
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def load_session(self):
        """โหลด session จากไฟล์ที่มีอยู่"""
        safe_print("🔐 LOADING INSTAGRAM SESSION")
        safe_print("=" * 50)
        
        # ลองโหลดจากไฟล์ session ต่างๆ
        session_files = [
            "session.json",
            "converted_session.json", 
            "main_session_extract.json",
            "logs_session_extract.json"
        ]
        
        for session_file in session_files:
            if os.path.exists(session_file):
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        self.session_data = json.load(f)
                    
                    safe_print(f"✅ Session loaded from: {session_file}")
                    
                    # ตรวจสอบว่ามี sessionid หรือไม่
                    if 'sessionid' in self.session_data:
                        safe_print(f"✅ Found sessionid: {self.session_data['sessionid'][:20]}...")
                        return True
                    elif 'cookies' in self.session_data:
                        # ถ้าเป็นรูปแบบ cookies
                        for cookie in self.session_data['cookies']:
                            if cookie.get('name') == 'sessionid':
                                self.session_data['sessionid'] = cookie['value']
                                safe_print(f"✅ Found sessionid in cookies: {cookie['value'][:20]}...")
                                return True
                    
                except Exception as e:
                    safe_print(f"❌ Error loading {session_file}: {e}")
                    continue
        
        safe_print("❌ No valid session found!")
        return False
    
    def initialize_client(self):
        """เริ่มต้น Instagram client ด้วย session"""
        safe_print("🚀 INITIALIZING INSTAGRAM CLIENT")
        safe_print("=" * 50)
        
        try:
            self.client = Client()
            
            # ตั้งค่า client ให้ปลอดภัย
            self.client.delay_range = [3, 7]  # Delay เพื่อหลีกเลี่ยงการตรวจจับ
            
            # Login ด้วย sessionid
            if 'sessionid' in self.session_data:
                sessionid = self.session_data['sessionid']
                safe_print(f"🔑 Logging in with sessionid: {sessionid[:20]}...")
                
                # ใช้ login_by_sessionid
                self.client.login_by_sessionid(sessionid)
                
                # ตรวจสอบการ login
                account_info = self.client.account_info()
                safe_print(f"✅ Successfully logged in as: @{account_info.username}")
                safe_print(f"👤 Account ID: {account_info.pk}")
                safe_print(f"📊 Followers: {account_info.follower_count}")
                safe_print(f"📊 Following: {account_info.following_count}")
                
                return True
            else:
                safe_print("❌ No sessionid found in session data")
                return False
                
        except Exception as e:
            safe_print(f"❌ Client initialization failed: {e}")
            traceback.print_exc()
            return False
    
    def get_target_info(self):
        """ดึงข้อมูลพื้นฐานของเป้าหมาย"""
        safe_print(f"🎯 GETTING TARGET INFO: @{self.target_username}")
        safe_print("=" * 50)
        
        try:
            # ค้นหา user ID ของเป้าหมาย
            user_id = self.client.user_id_from_username(self.target_username)
            safe_print(f"🔍 Found user ID: {user_id}")
            
            # ดึงข้อมูลรายละเอียด
            user_info = self.client.user_info(user_id)
            
            target_data = {
                "username": user_info.username,
                "user_id": str(user_id),
                "full_name": user_info.full_name,
                "biography": user_info.biography,
                "follower_count": user_info.follower_count,
                "following_count": user_info.following_count,
                "media_count": user_info.media_count,
                "is_private": user_info.is_private,
                "is_verified": user_info.is_verified,
                "profile_pic_url": str(user_info.profile_pic_url) if user_info.profile_pic_url else None,
                "external_url": user_info.external_url,
                "category": user_info.category
            }
            
            self.extracted_data["target_info"] = target_data
            
            safe_print(f"👤 Username: @{target_data['username']}")
            safe_print(f"📝 Full Name: {target_data['full_name']}")
            safe_print(f"📊 Followers: {target_data['follower_count']}")
            safe_print(f"📊 Following: {target_data['following_count']}")
            safe_print(f"📸 Posts: {target_data['media_count']}")
            safe_print(f"🔒 Private: {target_data['is_private']}")
            safe_print()
            
            return user_id
            
        except Exception as e:
            safe_print(f"❌ Error getting target info: {e}")
            return None
    
    def extract_direct_messages(self):
        """ดึง Direct Messages (DMs) ทั้งหมด"""
        safe_print("💬 EXTRACTING DIRECT MESSAGES")
        safe_print("=" * 50)
        
        try:
            # ดึง direct message threads
            threads = self.client.direct_threads(amount=50)
            safe_print(f"🔍 Found {len(threads)} message threads")
            
            dm_data = []
            
            for i, thread in enumerate(threads):
                try:
                    safe_print(f"📱 Processing thread {i+1}/{len(threads)}")
                    
                    # ข้อมูลพื้นฐานของ thread
                    thread_info = {
                        "thread_id": thread.id,
                        "thread_title": thread.thread_title,
                        "users": [{"username": user.username, "full_name": user.full_name} for user in thread.users],
                        "last_activity": str(thread.last_activity_at) if thread.last_activity_at else None,
                        "messages": []
                    }
                    
                    # ดึงข้อความในแต่ละ thread (20 ข้อความล่าสุด)
                    messages = self.client.direct_messages(thread.id, amount=20)
                    
                    for msg in messages:
                        message_data = {
                            "message_id": msg.id,
                            "text": msg.text,
                            "timestamp": str(msg.timestamp) if msg.timestamp else None,
                            "user_id": str(msg.user_id) if msg.user_id else None,
                            "item_type": msg.item_type,
                            "is_sent_by_viewer": msg.is_sent_by_viewer
                        }
                        
                        # ถ้ามีรูปภาพหรือไฟล์แนบ
                        if hasattr(msg, 'visual_media') and msg.visual_media:
                            message_data["media_url"] = str(msg.visual_media.url) if msg.visual_media.url else None
                        
                        thread_info["messages"].append(message_data)
                    
                    dm_data.append(thread_info)
                    safe_print(f"  ✅ Thread with @{thread.users[0].username if thread.users else 'Unknown'}: {len(thread_info['messages'])} messages")
                    
                    # หน่วงเวลาเพื่อความปลอดภัย
                    time.sleep(2)
                    
                except Exception as e:
                    safe_print(f"  ❌ Error processing thread {i+1}: {e}")
                    continue
            
            self.extracted_data["direct_messages"] = dm_data
            safe_print(f"✅ Extracted {len(dm_data)} DM threads with total messages")
            safe_print()
            
            return True
            
        except Exception as e:
            safe_print(f"❌ Error extracting DMs: {e}")
            return False
    
    def extract_stories(self, user_id):
        """ดึง Stories ของเป้าหมาย"""
        safe_print(f"📖 EXTRACTING STORIES: @{self.target_username}")
        safe_print("=" * 50)
        
        try:
            # ดึง stories ของเป้าหมาย
            stories = self.client.user_stories(user_id)
            safe_print(f"🔍 Found {len(stories)} stories")
            
            stories_data = []
            
            for i, story in enumerate(stories):
                try:
                    story_data = {
                        "story_id": str(story.pk),
                        "taken_at": str(story.taken_at) if story.taken_at else None,
                        "caption": story.caption_text,
                        "media_type": str(story.media_type),
                        "view_count": story.view_count if hasattr(story, 'view_count') else None,
                        "url": str(story.thumbnail_url) if story.thumbnail_url else None,
                        "video_url": str(story.video_url) if hasattr(story, 'video_url') and story.video_url else None
                    }
                    
                    stories_data.append(story_data)
                    safe_print(f"  ✅ Story {i+1}: {story_data['caption'][:50] if story_data['caption'] else 'No caption'}...")
                    
                except Exception as e:
                    safe_print(f"  ❌ Error processing story {i+1}: {e}")
                    continue
            
            self.extracted_data["stories"] = stories_data
            safe_print(f"✅ Extracted {len(stories_data)} stories")
            safe_print()
            
            return True
            
        except Exception as e:
            safe_print(f"❌ Error extracting stories: {e}")
            return False
    
    def extract_posts(self, user_id):
        """ดึงโพสต์ล่าสุดของเป้าหมาย"""
        safe_print(f"📸 EXTRACTING POSTS: @{self.target_username}")
        safe_print("=" * 50)
        
        try:
            # ดึงโพสต์ล่าสุด 20 โพสต์
            posts = self.client.user_medias(user_id, amount=20)
            safe_print(f"🔍 Found {len(posts)} posts")
            
            posts_data = []
            
            for i, post in enumerate(posts):
                try:
                    post_data = {
                        "post_id": str(post.pk),
                        "caption": post.caption_text,
                        "taken_at": str(post.taken_at) if post.taken_at else None,
                        "media_type": str(post.media_type),
                        "like_count": post.like_count,
                        "comment_count": post.comment_count,
                        "thumbnail_url": str(post.thumbnail_url) if post.thumbnail_url else None,
                        "video_url": str(post.video_url) if hasattr(post, 'video_url') and post.video_url else None,
                        "location": str(post.location.name) if post.location else None
                    }
                    
                    # ดึงแฮชแท็กและ mentions
                    if hasattr(post, 'usertags') and post.usertags:
                        post_data["tagged_users"] = [{"username": tag.user.username} for tag in post.usertags]
                    
                    posts_data.append(post_data)
                    safe_print(f"  ✅ Post {i+1}: {post_data['like_count']} likes, {post_data['comment_count']} comments")
                    
                    # หน่วงเวลาเพื่อความปลอดภัย
                    time.sleep(1)
                    
                except Exception as e:
                    safe_print(f"  ❌ Error processing post {i+1}: {e}")
                    continue
            
            self.extracted_data["posts"] = posts_data
            safe_print(f"✅ Extracted {len(posts_data)} posts")
            safe_print()
            
            return True
            
        except Exception as e:
            safe_print(f"❌ Error extracting posts: {e}")
            return False
    
    def extract_followers_following(self, user_id):
        """ดึงรายชื่อผู้ติดตามและคนที่ติดตาม (ถ้าไม่ private)"""
        safe_print(f"👥 EXTRACTING FOLLOWERS/FOLLOWING: @{self.target_username}")
        safe_print("=" * 50)
        
        try:
            # ตรวจสอบว่าบัญชีเป็น private หรือไม่
            if self.extracted_data["target_info"].get("is_private", False):
                safe_print("🔒 Account is private - skipping followers/following extraction")
                return True
            
            # ดึงผู้ติดตาม (50 คนแรก)
            try:
                followers = self.client.user_followers(user_id, amount=50)
                followers_data = []
                
                for follower_id, follower_info in followers.items():
                    follower_data = {
                        "user_id": str(follower_id),
                        "username": follower_info.username,
                        "full_name": follower_info.full_name,
                        "is_verified": follower_info.is_verified,
                        "is_private": follower_info.is_private
                    }
                    followers_data.append(follower_data)
                
                self.extracted_data["followers"] = followers_data
                safe_print(f"✅ Extracted {len(followers_data)} followers")
                
            except Exception as e:
                safe_print(f"❌ Error extracting followers: {e}")
            
            # หน่วงเวลา
            time.sleep(3)
            
            # ดึงคนที่ติดตาม (50 คนแรก)
            try:
                following = self.client.user_following(user_id, amount=50)
                following_data = []
                
                for following_id, following_info in following.items():
                    following_data_item = {
                        "user_id": str(following_id),
                        "username": following_info.username,
                        "full_name": following_info.full_name,
                        "is_verified": following_info.is_verified,
                        "is_private": following_info.is_private
                    }
                    following_data.append(following_data_item)
                
                self.extracted_data["following"] = following_data
                safe_print(f"✅ Extracted {len(following_data)} following")
                
            except Exception as e:
                safe_print(f"❌ Error extracting following: {e}")
            
            safe_print()
            return True
            
        except Exception as e:
            safe_print(f"❌ Error extracting followers/following: {e}")
            return False
    
    def save_extracted_data(self):
        """บันทึกข้อมูลที่ดึงมาได้"""
        safe_print("💾 SAVING EXTRACTED DATA")
        safe_print("=" * 50)
        
        try:
            # สร้างรายงานสรุป
            summary = {
                "extraction_timestamp": datetime.now().isoformat(),
                "target_username": self.target_username,
                "extraction_summary": {
                    "target_info": "✅ Complete" if self.extracted_data["target_info"] else "❌ Failed",
                    "direct_messages": f"✅ {len(self.extracted_data['direct_messages'])} threads",
                    "stories": f"✅ {len(self.extracted_data['stories'])} stories",
                    "posts": f"✅ {len(self.extracted_data['posts'])} posts",
                    "followers": f"✅ {len(self.extracted_data['followers'])} followers",
                    "following": f"✅ {len(self.extracted_data['following'])} following"
                },
                "data": self.extracted_data
            }
            
            # บันทึกไฟล์หลัก
            main_filename = f"INSTAGRAM_STEALTH_EXTRACT_{self.target_username}_{self.timestamp}.json"
            with open(main_filename, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            # บันทึกไฟล์แยกส่วน
            if self.extracted_data["direct_messages"]:
                dm_filename = f"DMs_{self.target_username}_{self.timestamp}.json"
                with open(dm_filename, 'w', encoding='utf-8') as f:
                    json.dump(self.extracted_data["direct_messages"], f, indent=2, ensure_ascii=False)
                safe_print(f"💬 DMs saved: {dm_filename}")
            
            if self.extracted_data["posts"]:
                posts_filename = f"POSTS_{self.target_username}_{self.timestamp}.json"
                with open(posts_filename, 'w', encoding='utf-8') as f:
                    json.dump(self.extracted_data["posts"], f, indent=2, ensure_ascii=False)
                safe_print(f"📸 Posts saved: {posts_filename}")
            
            if self.extracted_data["stories"]:
                stories_filename = f"STORIES_{self.target_username}_{self.timestamp}.json"
                with open(stories_filename, 'w', encoding='utf-8') as f:
                    json.dump(self.extracted_data["stories"], f, indent=2, ensure_ascii=False)
                safe_print(f"📖 Stories saved: {stories_filename}")
            
            safe_print(f"✅ Main extraction report saved: {main_filename}")
            safe_print()
            
            return True
            
        except Exception as e:
            safe_print(f"❌ Error saving data: {e}")
            return False
    
    def print_extraction_summary(self):
        """แสดงสรุปผลการดึงข้อมูล"""
        safe_print("📊 EXTRACTION SUMMARY")
        safe_print("=" * 50)
        
        target_info = self.extracted_data.get("target_info", {})
        
        safe_print(f"🎯 Target: @{target_info.get('username', self.target_username)}")
        safe_print(f"👤 Full Name: {target_info.get('full_name', 'N/A')}")
        safe_print(f"📊 Followers: {target_info.get('follower_count', 'N/A'):,}")
        safe_print(f"📊 Following: {target_info.get('following_count', 'N/A'):,}")
        safe_print(f"📸 Posts: {target_info.get('media_count', 'N/A'):,}")
        safe_print(f"🔒 Private: {'Yes' if target_info.get('is_private') else 'No'}")
        safe_print()
        
        safe_print("📈 EXTRACTED DATA:")
        safe_print(f"💬 Direct Messages: {len(self.extracted_data['direct_messages'])} threads")
        safe_print(f"📖 Stories: {len(self.extracted_data['stories'])} stories")
        safe_print(f"📸 Posts: {len(self.extracted_data['posts'])} posts")
        safe_print(f"👥 Followers: {len(self.extracted_data['followers'])} users")
        safe_print(f"👥 Following: {len(self.extracted_data['following'])} users")
        safe_print()
        
        # แสดง DM ล่าสุด 3 thread
        if self.extracted_data["direct_messages"]:
            safe_print("💬 RECENT DMS PREVIEW:")
            for i, thread in enumerate(self.extracted_data["direct_messages"][:3]):
                users = ", ".join([user["username"] for user in thread["users"]])
                message_count = len(thread["messages"])
                safe_print(f"  📱 Thread {i+1}: {users} ({message_count} messages)")
                
                # แสดงข้อความล่าสุด
                if thread["messages"]:
                    latest_msg = thread["messages"][0]
                    text_preview = latest_msg["text"][:100] if latest_msg["text"] else "[Media/No text]"
                    safe_print(f"    💭 Latest: {text_preview}...")
            safe_print()
        
        # แสดงโพสต์ล่าสุด
        if self.extracted_data["posts"]:
            safe_print("📸 RECENT POSTS PREVIEW:")
            for i, post in enumerate(self.extracted_data["posts"][:3]):
                caption_preview = post["caption"][:100] if post["caption"] else "[No caption]"
                likes = post["like_count"]
                comments = post["comment_count"]
                safe_print(f"  📷 Post {i+1}: {likes:,} likes, {comments:,} comments")
                safe_print(f"    📝 Caption: {caption_preview}...")
            safe_print()
    
    def run_stealth_extraction(self):
        """เรียกใช้การดึงข้อมูลแบบปลอดภัย"""
        try:
            safe_print("🕵️ STARTING INSTAGRAM STEALTH EXTRACTION")
            safe_print("=" * 70)
            safe_print(f"🎯 Target: @{self.target_username}")
            safe_print(f"⏰ Timestamp: {self.timestamp}")
            safe_print("=" * 70)
            safe_print()
            
            # โหลด session
            if not self.load_session():
                safe_print("❌ Failed to load session!")
                return False
            
            # เริ่มต้น client
            if not self.initialize_client():
                safe_print("❌ Failed to initialize client!")
                return False
            
            # ดึงข้อมูลเป้าหมาย
            user_id = self.get_target_info()
            if not user_id:
                safe_print("❌ Failed to get target info!")
                return False
            
            # ดึง Direct Messages
            safe_print("🚀 Starting data extraction...")
            self.extract_direct_messages()
            
            # ดึง Stories
            self.extract_stories(user_id)
            
            # ดึงโพสต์
            self.extract_posts(user_id)
            
            # ดึงผู้ติดตาม/ติดตาม
            self.extract_followers_following(user_id)
            
            # บันทึกข้อมูล
            self.save_extracted_data()
            
            # แสดงสรุป
            self.print_extraction_summary()
            
            safe_print("🎉 STEALTH EXTRACTION COMPLETED SUCCESSFULLY!")
            safe_print("💯 All data extracted without triggering Instagram security!")
            safe_print("🔒 No login required - Used existing session safely!")
            
            return True
            
        except Exception as e:
            safe_print(f"❌ Stealth extraction failed: {e}")
            traceback.print_exc()
            return False

def main():
    """Main execution"""
    extractor = InstagramStealthExtractor()
    success = extractor.run_stealth_extraction()
    
    if success:
        safe_print("✅ Instagram stealth extraction completed successfully!")
        safe_print("🇹🇭 การดึงข้อมูล Instagram แบบปลอดภัยเสร็จสมบูรณ์!")
        sys.exit(0)
    else:
        safe_print("❌ Instagram stealth extraction failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
