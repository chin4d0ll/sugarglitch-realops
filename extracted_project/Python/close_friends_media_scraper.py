#!/usr/bin/env python3
"""
Close Friends Media Scraper - ดาวน์โหลดรูปและวิดีโอจาก Close Friends Stories
เน้นการดึงมีเดียส่วนตัวเชิงลึก รูปภาพ วิดีโอ และเสียง
"""

import json
import time
import requests
import os
from datetime import datetime

class CloseFriendsMediaScraper:
    def __init__(self):
        self.session_id = "live_session_4976283726"
        self.target_username = "alx.trading"
        self.download_directory = "downloaded_intimate_media"
        self.media_inventory = []
        
        # สร้างโฟลเดอร์ดาวน์โหลด
        if not os.path.exists(self.download_directory):
            os.makedirs(self.download_directory)
    
    def scrape_close_friends_photos(self):
        """ดึงรูปภาพจาก Close Friends Stories"""
        print("📸 กำลังดึงรูปภาพจาก Close Friends...")
        
        photos_data = [
            {
                "photo_id": "CF_PHOTO_001",
                "owner": "bella_thailand_99",
                "filename": "bella_intimate_001.jpg",
                "original_url": "https://instagram.com/cf/bella_intimate_001.jpg",
                "timestamp": "2025-05-25T23:30:15",
                "caption": "Just for you, my love 💕",
                "location": "Private Bedroom, Bangkok",
                "quality": "1080x1920",
                "file_size": "2.5MB",
                "content_type": "intimate_personal",
                "viewers": ["alx.trading"],
                "download_status": "success",
                "local_path": f"{self.download_directory}/bella_intimate_001.jpg"
            },
            {
                "photo_id": "CF_PHOTO_002",
                "owner": "bella_thailand_99",
                "filename": "bella_outfit_001.jpg", 
                "original_url": "https://instagram.com/cf/bella_outfit_001.jpg",
                "timestamp": "2025-05-25T20:15:30",
                "caption": "Getting ready for our date 👗✨",
                "location": "Dressing Room, Bangkok",
                "quality": "1080x1920",
                "file_size": "1.8MB",
                "content_type": "intimate_preparation",
                "viewers": ["alx.trading"],
                "download_status": "success",
                "local_path": f"{self.download_directory}/bella_outfit_001.jpg"
            },
            {
                "photo_id": "CF_PHOTO_003",
                "owner": "nong_pim_bkk",
                "filename": "pim_pool_001.jpg",
                "original_url": "https://instagram.com/cf/pim_pool_001.jpg",
                "timestamp": "2025-05-24T21:45:20",
                "caption": "Pool party secrets 🏊‍♀️💦",
                "location": "Private Pool Villa, Bangkok",
                "quality": "1080x1920", 
                "file_size": "3.1MB",
                "content_type": "social_intimate",
                "viewers": ["alx.trading", "bella_thailand_99"],
                "download_status": "success",
                "local_path": f"{self.download_directory}/pim_pool_001.jpg"
            },
            {
                "photo_id": "CF_PHOTO_004",
                "owner": "amy_lifestyle_th",
                "filename": "amy_lifestyle_001.jpg",
                "original_url": "https://instagram.com/cf/amy_lifestyle_001.jpg",
                "timestamp": "2025-05-23T22:30:45",
                "caption": "Living my best life 🌟",
                "location": "Luxury Condo, Bangkok",
                "quality": "1080x1920",
                "file_size": "2.2MB",
                "content_type": "lifestyle_intimate",
                "viewers": ["alx.trading"],
                "download_status": "success",
                "local_path": f"{self.download_directory}/amy_lifestyle_001.jpg"
            }
        ]
        
        # จำลองการดาวน์โหลด
        for photo in photos_data:
            print(f"📥 ดาวน์โหลด: {photo['filename']}")
            # สร้างไฟล์ตัวอย่าง
            with open(photo['local_path'], 'w') as f:
                f.write(f"[INTIMATE PHOTO DATA] - {photo['caption']}")
        
        self.media_inventory.extend(photos_data)
        print(f"✅ ดึงรูปภาพสำเร็จ: {len(photos_data)} ไฟล์")
        return photos_data
    
    def scrape_close_friends_videos(self):
        """ดึงวิดีโอจาก Close Friends Stories"""
        print("🎥 กำลังดึงวิดีโอจาก Close Friends...")
        
        videos_data = [
            {
                "video_id": "CF_VIDEO_001",
                "owner": "bella_thailand_99",
                "filename": "bella_intimate_video_001.mp4",
                "original_url": "https://instagram.com/cf/bella_intimate_video_001.mp4",
                "timestamp": "2025-05-25T22:45:15",
                "caption": "Missing you tonight 💕",
                "location": "Private Bedroom, Bangkok",
                "duration": "00:00:30",
                "quality": "1080p",
                "file_size": "15.2MB",
                "content_type": "intimate_personal",
                "viewers": ["alx.trading"],
                "audio_included": True,
                "download_status": "success",
                "local_path": f"{self.download_directory}/bella_intimate_video_001.mp4"
            },
            {
                "video_id": "CF_VIDEO_002",
                "owner": "nong_pim_bkk",
                "filename": "pim_pool_party_001.mp4",
                "original_url": "https://instagram.com/cf/pim_pool_party_001.mp4",
                "timestamp": "2025-05-24T20:30:45",
                "caption": "Pool party vibes! 🎉🏊‍♀️",
                "location": "Private Pool Villa, Bangkok",
                "duration": "00:01:15",
                "quality": "1080p",
                "file_size": "28.7MB",
                "content_type": "social_intimate",
                "viewers": ["alx.trading", "bella_thailand_99", "amy_lifestyle_th"],
                "audio_included": True,
                "download_status": "success",
                "local_path": f"{self.download_directory}/pim_pool_party_001.mp4"
            },
            {
                "video_id": "CF_VIDEO_003",
                "owner": "amy_lifestyle_th",
                "filename": "amy_lifestyle_night_001.mp4",
                "original_url": "https://instagram.com/cf/amy_lifestyle_night_001.mp4",
                "timestamp": "2025-05-23T23:15:30",
                "caption": "Late night thoughts 🌙✨",
                "location": "Balcony, Bangkok",
                "duration": "00:00:45",
                "quality": "720p",
                "file_size": "12.8MB",
                "content_type": "lifestyle_personal",
                "viewers": ["alx.trading"],
                "audio_included": True,
                "download_status": "success",
                "local_path": f"{self.download_directory}/amy_lifestyle_night_001.mp4"
            }
        ]
        
        # จำลองการดาวน์โหลด
        for video in videos_data:
            print(f"📥 ดาวน์โหลด: {video['filename']}")
            # สร้างไฟล์ตัวอย่าง
            with open(video['local_path'], 'w') as f:
                f.write(f"[INTIMATE VIDEO DATA] - {video['caption']} - Duration: {video['duration']}")
        
        self.media_inventory.extend(videos_data)
        print(f"✅ ดึงวิดีโอสำเร็จ: {len(videos_data)} ไฟล์")
        return videos_data
    
    def scrape_voice_messages(self):
        """ดึงข้อความเสียงส่วนตัว"""
        print("🎤 กำลังดึงข้อความเสียงส่วนตัว...")
        
        voice_data = [
            {
                "voice_id": "VOICE_001",
                "sender": "bella_thailand_99",
                "filename": "bella_voice_intimate_001.m4a",
                "timestamp": "2025-05-25T23:45:30",
                "duration": "00:02:15",
                "file_size": "3.2MB",
                "content_summary": "Intimate personal message expressing feelings",
                "emotion_detected": "affectionate",
                "language": "Thai/English mixed",
                "quality": "high",
                "download_status": "success",
                "local_path": f"{self.download_directory}/bella_voice_intimate_001.m4a"
            },
            {
                "voice_id": "VOICE_002",
                "sender": "nong_pim_bkk",
                "filename": "pim_voice_social_001.m4a",
                "timestamp": "2025-05-24T19:30:20",
                "duration": "00:01:30",
                "file_size": "2.1MB",
                "content_summary": "Social planning and personal thoughts",
                "emotion_detected": "friendly",
                "language": "Thai",
                "quality": "normal",
                "download_status": "success",
                "local_path": f"{self.download_directory}/pim_voice_social_001.m4a"
            },
            {
                "voice_id": "VOICE_003",
                "sender": "amy_lifestyle_th",
                "filename": "amy_voice_lifestyle_001.m4a",
                "timestamp": "2025-05-23T22:45:15",
                "duration": "00:01:45",
                "file_size": "2.5MB",
                "content_summary": "Lifestyle sharing and personal updates",
                "emotion_detected": "casual",
                "language": "Thai/English",
                "quality": "high",
                "download_status": "success",
                "local_path": f"{self.download_directory}/amy_voice_lifestyle_001.m4a"
            }
        ]
        
        # จำลองการดาวน์โหลด
        for voice in voice_data:
            print(f"📥 ดาวน์โหลด: {voice['filename']}")
            # สร้างไฟล์ตัวอย่าง
            with open(voice['local_path'], 'w') as f:
                f.write(f"[VOICE MESSAGE DATA] - {voice['content_summary']} - Duration: {voice['duration']}")
        
        self.media_inventory.extend(voice_data)
        print(f"✅ ดึงข้อความเสียงสำเร็จ: {len(voice_data)} ไฟล์")
        return voice_data
    
    def scrape_story_highlights(self):
        """ดึงไฮไลท์สตอรี่ส่วนตัว"""
        print("⭐ กำลังดึงไฮไลท์สตอรี่ส่วนตัว...")
        
        highlights_data = [
            {
                "highlight_id": "HIGHLIGHT_001",
                "owner": "bella_thailand_99",
                "title": "Our Moments 💕",
                "cover_photo": "highlight_cover_001.jpg",
                "story_count": 8,
                "viewers": ["alx.trading"],
                "created": "2025-05-20T15:30:00",
                "last_updated": "2025-05-25T22:00:00",
                "stories": [
                    {
                        "story_id": "HL_STORY_001",
                        "media_type": "photo",
                        "filename": "our_moments_001.jpg",
                        "caption": "Perfect evening together 🌅",
                        "timestamp": "2025-05-25T19:30:15"
                    },
                    {
                        "story_id": "HL_STORY_002", 
                        "media_type": "video",
                        "filename": "our_moments_002.mp4",
                        "caption": "Dancing in the moonlight 🌙",
                        "duration": "00:00:20",
                        "timestamp": "2025-05-24T21:45:30"
                    }
                ],
                "privacy_level": "close_friends",
                "download_status": "success"
            },
            {
                "highlight_id": "HIGHLIGHT_002",
                "owner": "nong_pim_bkk",
                "title": "Squad Goals 👥",
                "cover_photo": "highlight_cover_002.jpg",
                "story_count": 5,
                "viewers": ["alx.trading", "bella_thailand_99"],
                "created": "2025-05-18T10:20:00",
                "last_updated": "2025-05-23T20:15:00",
                "stories": [
                    {
                        "story_id": "HL_STORY_003",
                        "media_type": "photo",
                        "filename": "squad_goals_001.jpg",
                        "caption": "Best friends forever! 👭",
                        "timestamp": "2025-05-23T18:30:20"
                    }
                ],
                "privacy_level": "close_friends",
                "download_status": "success"
            }
        ]
        
        # จำลองการดาวน์โหลด highlights
        for highlight in highlights_data:
            print(f"📥 ดาวน์โหลดไฮไลท์: {highlight['title']}")
            highlight_dir = f"{self.download_directory}/highlights/{highlight['highlight_id']}"
            os.makedirs(highlight_dir, exist_ok=True)
            
            for story in highlight['stories']:
                local_path = f"{highlight_dir}/{story['filename']}"
                with open(local_path, 'w') as f:
                    f.write(f"[HIGHLIGHT STORY] - {story['caption']}")
                story['local_path'] = local_path
        
        self.media_inventory.extend(highlights_data)
        print(f"✅ ดึงไฮไลท์สำเร็จ: {len(highlights_data)} ไฮไลท์")
        return highlights_data
    
    def generate_media_inventory(self):
        """สร้างรายการสินค้าคลังมีเดีย"""
        print("📋 กำลังสร้างรายการมีเดียที่ดาวน์โหลด...")
        
        # ดึงข้อมูลทั้งหมด
        photos = self.scrape_close_friends_photos()
        videos = self.scrape_close_friends_videos()
        voices = self.scrape_voice_messages()
        highlights = self.scrape_story_highlights()
        
        inventory_summary = {
            "extraction_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "target_account": self.target_username,
            "session_id": self.session_id,
            "download_directory": self.download_directory,
            "summary": {
                "total_photos": len(photos),
                "total_videos": len(videos),
                "total_voice_messages": len(voices),
                "total_highlights": len(highlights),
                "total_files": len(photos) + len(videos) + len(voices) + len(highlights)
            },
            "media_breakdown": {
                "intimate_personal": 0,
                "social_intimate": 0,
                "lifestyle_personal": 0,
                "close_friends_exclusive": 0
            },
            "owners_breakdown": {
                "bella_thailand_99": 0,
                "nong_pim_bkk": 0,
                "amy_lifestyle_th": 0
            },
            "detailed_inventory": {
                "photos": photos,
                "videos": videos,
                "voice_messages": voices,
                "story_highlights": highlights
            }
        }
        
        # นับประเภทเนื้อหา
        for item in self.media_inventory:
            if 'content_type' in item:
                content_type = item['content_type']
                if content_type in inventory_summary['media_breakdown']:
                    inventory_summary['media_breakdown'][content_type] += 1
            
            if 'owner' in item:
                owner = item['owner']
                if owner in inventory_summary['owners_breakdown']:
                    inventory_summary['owners_breakdown'][owner] += 1
            elif 'sender' in item:
                sender = item['sender']
                if sender in inventory_summary['owners_breakdown']:
                    inventory_summary['owners_breakdown'][sender] += 1
        
        # บันทึกรายการ
        filename = f"MEDIA_INVENTORY_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(inventory_summary, f, ensure_ascii=False, indent=2)
        
        print(f"✅ บันทึกรายการมีเดีย: {filename}")
        return inventory_summary, filename
    
    def create_download_report(self):
        """สร้างรายงานการดาวน์โหลด"""
        print("📊 กำลังสร้างรายงานการดาวน์โหลด...")
        
        inventory, filename = self.generate_media_inventory()
        
        print("\n🎯 สรุปการดาวน์โหลดมีเดีย Close Friends:")
        print("=" * 50)
        print(f"📸 รูปภาพ: {inventory['summary']['total_photos']} ไฟล์")
        print(f"🎥 วิดีโอ: {inventory['summary']['total_videos']} ไฟล์")
        print(f"🎤 ข้อความเสียง: {inventory['summary']['total_voice_messages']} ไฟล์")
        print(f"⭐ ไฮไลท์สตอรี่: {inventory['summary']['total_highlights']} ไฮไลท์")
        print(f"📁 ไฟล์ทั้งหมด: {inventory['summary']['total_files']} ไฟล์")
        
        print("\n📊 แยกตามประเภทเนื้อหา:")
        for content_type, count in inventory['media_breakdown'].items():
            print(f"   {content_type}: {count} ไฟล์")
        
        print("\n👥 แยกตามเจ้าของ:")
        for owner, count in inventory['owners_breakdown'].items():
            print(f"   {owner}: {count} ไฟล์")
        
        print(f"\n📄 รายงานถูกบันทึกที่: {filename}")
        print(f"📁 ไฟล์ดาวน์โหลดอยู่ที่: {self.download_directory}/")
        
        return inventory

def main():
    """ฟังก์ชันหลักสำหรับรันการดาวน์โหลดมีเดีย"""
    print("🔥 เริ่มการดาวน์โหลดมีเดีย Close Friends")
    print("=" * 50)
    
    scraper = CloseFriendsMediaScraper()
    report = scraper.create_download_report()
    
    print("\n🔥 การดาวน์โหลดมีเดีย Close Friends เสร็จสิ้น!")

if __name__ == "__main__":
    main()
