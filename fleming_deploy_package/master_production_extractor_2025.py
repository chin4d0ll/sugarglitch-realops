#!/usr/bin/env python3
"""
Master Production Extractor 2025
Extracts DMs, Stories, Posts using regenerated Fleming654 session
Production-ready with PDF export and media download
"""

import os
import sys
import json
import time
import random
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes
except ImportError:
    os.system("pip install instagrapi")
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes

try:
    from fpdf import FPDF
except ImportError:
    os.system("pip install fpdf2")
    from fpdf import FPDF

try:
    from PIL import Image
except ImportError:
    os.system("pip install Pillow")
    from PIL import Image

class MasterProductionExtractor:
    """Production-ready Instagram extractor for DMs, Stories, Posts"""
    
    def __init__(self):
        self.username = "alx.trading"
        self.target_accounts = ["alx.trading", "whatilove1728"]
        
        # Setup directories
        self.base_dir = Path("/workspaces/sugarglitch-realops")
        self.sessions_dir = self.base_dir / "sessions"
        self.results_dir = self.base_dir / "results"
        self.media_dir = self.base_dir / "media"
        self.logs_dir = self.base_dir / "logs"
        
        for dir_path in [self.results_dir, self.media_dir, self.logs_dir]:
            dir_path.mkdir(exist_ok=True)
        
        self.client = None
        self.extracted_data = {
            "dms": [],
            "stories": [],
            "posts": [],
            "metadata": {}
        }
        
        print("🚀 Master Production Extractor 2025 - Ready")
    
    def load_fleming_session(self):
        """Load the latest Fleming654 session"""
        print("🔄 Loading Fleming654 session...")
        
        # Try latest session first
        latest_session = self.sessions_dir / "fleming_latest.json"
        if latest_session.exists():
            try:
                with open(latest_session, 'r') as f:
                    session_data = json.load(f)
                return self.initialize_client_with_session(session_data)
            except Exception as e:
                print(f"❌ Failed to load latest session: {e}")
        
        # Try to find any Fleming session
        fleming_sessions = list(self.sessions_dir.glob("fleming_session_*.json"))
        if fleming_sessions:
            # Use the most recent one
            latest_file = max(fleming_sessions, key=lambda p: p.stat().st_mtime)
            try:
                with open(latest_file, 'r') as f:
                    session_data = json.load(f)
                return self.initialize_client_with_session(session_data)
            except Exception as e:
                print(f"❌ Failed to load session from {latest_file}: {e}")
        
        print("❌ No Fleming sessions found - run session_regenerator_fleming654.py first")
        # Add a helper function to guide users
        print("💡 To generate a session, run: python3 session_regenerator_fleming654.py")
        
        return False
    
    def initialize_client_with_session(self, session_data):
        """Initialize instagrapi client with session data"""
        try:
            self.client = Client()
            
            # Set device settings
            device_settings = {
                "app_version": "203.0.0.29.118",
                "android_version": 26,
                "android_release": "8.0.0",
                "dpi": "480dpi", 
                "resolution": "1080x1920",
                "manufacturer": "samsung",
                "device": "SM-G950F",
                "model": "galaxy_s8",
                "cpu": "samsungexynos8895",
                "version_code": "314665256",
            }
            self.client.set_device(device_settings)
            self.client.delay_range = [1, 3]
            
            # Set session data
            if "sessionid" in session_data:
                self.client.sessionid = session_data["sessionid"]
            if "csrftoken" in session_data:
                self.client.csrftoken = session_data["csrftoken"]
            if "device_id" in session_data:
                self.client.device_id = session_data["device_id"]
            if "uuid" in session_data:
                self.client.uuid = session_data["uuid"]
            
            # Test the session
            user_info = self.client.user_info_by_username(self.username)
            print(f"✅ Session loaded successfully - User ID: {user_info.pk}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize client: {e}")
            return False
    
    def extract_dms(self):
        """Extract Direct Messages"""
        print("📥 Extracting Direct Messages...")
        
        try:
            threads = self.client.direct_threads()
            print(f"📊 Found {len(threads)} DM threads")
            
            for i, thread in enumerate(threads[:20]):  # Limit to 20 threads
                try:
                    thread_id = thread.id
                    thread_title = thread.thread_title or f"Thread {i+1}"
                    participants = [user.username for user in thread.users]
                    
                    print(f"📨 Processing: {thread_title}")
                    
                    # Get messages
                    messages = self.client.direct_messages(thread_id, amount=100)
                    
                    thread_data = {
                        "thread_id": thread_id,
                        "title": thread_title,
                        "participants": participants,
                        "message_count": len(messages),
                        "messages": []
                    }
                    
                    for msg in messages:
                        msg_data = {
                            "id": msg.id,
                            "user_id": msg.user_id,
                            "timestamp": msg.timestamp.isoformat(),
                            "text": msg.text or "",
                            "media_type": None,
                            "media_url": None,
                            "media_path": None
                        }
                        
                        # Handle media
                        if hasattr(msg, 'visual_media') and msg.visual_media:
                            media = msg.visual_media
                            if hasattr(media, 'url'):
                                msg_data["media_type"] = "image"
                                msg_data["media_url"] = media.url
                                
                                # Download media
                                media_filename = f"dm_{thread_id}_{msg.id}.jpg"
                                if self.download_media(media.url, media_filename):
                                    msg_data["media_path"] = str(self.media_dir / media_filename)
                        
                        thread_data["messages"].append(msg_data)
                    
                    self.extracted_data["dms"].append(thread_data)
                    print(f"✅ Extracted {len(messages)} messages from {thread_title}")
                    
                    # Delay between threads
                    time.sleep(random.uniform(2, 4))
                    
                except Exception as e:
                    print(f"❌ Failed to extract thread {i}: {e}")
                    continue
            
            print(f"✅ DM extraction complete - {len(self.extracted_data['dms'])} threads")
            
        except Exception as e:
            print(f"❌ DM extraction failed: {e}")
    
    def extract_stories(self):
        """Extract Stories from target accounts"""
        print("📖 Extracting Stories...")
        
        try:
            for account in self.target_accounts:
                try:
                    user_info = self.client.user_info_by_username(account)
                    user_id = user_info.pk
                    
                    # Get user stories
                    stories = self.client.user_stories(user_id)
                    print(f"📚 Found {len(stories)} stories for @{account}")
                    
                    account_stories = {
                        "username": account,
                        "user_id": str(user_id),
                        "story_count": len(stories),
                        "stories": []
                    }
                    
                    for story in stories:
                        story_data = {
                            "id": story.id,
                            "taken_at": story.taken_at.isoformat(),
                            "media_type": story.media_type,
                            "thumbnail_url": story.thumbnail_url,
                            "video_url": story.video_url if hasattr(story, 'video_url') else None,
                            "media_path": None
                        }
                        
                        # Download story media
                        if story.thumbnail_url:
                            filename = f"story_{account}_{story.id}.jpg"
                            if self.download_media(story.thumbnail_url, filename):
                                story_data["media_path"] = str(self.media_dir / filename)
                        
                        account_stories["stories"].append(story_data)
                    
                    self.extracted_data["stories"].append(account_stories)
                    print(f"✅ Extracted stories from @{account}")
                    
                    time.sleep(random.uniform(3, 5))
                    
                except Exception as e:
                    print(f"❌ Failed to extract stories from @{account}: {e}")
                    continue
            
            print(f"✅ Story extraction complete")
            
        except Exception as e:
            print(f"❌ Story extraction failed: {e}")
    
    def extract_posts(self):
        """Extract Posts from target accounts"""
        print("📸 Extracting Posts...")
        
        try:
            for account in self.target_accounts:
                try:
                    user_info = self.client.user_info_by_username(account)
                    user_id = user_info.pk
                    
                    # Get user medias (posts)
                    medias = self.client.user_medias(user_id, amount=50)
                    print(f"🖼️ Found {len(medias)} posts for @{account}")
                    
                    account_posts = {
                        "username": account,
                        "user_id": str(user_id),
                        "post_count": len(medias),
                        "posts": []
                    }
                    
                    for media in medias:
                        post_data = {
                            "id": media.id,
                            "code": media.code,
                            "taken_at": media.taken_at.isoformat(),
                            "media_type": media.media_type,
                            "caption_text": media.caption_text,
                            "like_count": media.like_count,
                            "comment_count": media.comment_count,
                            "thumbnail_url": media.thumbnail_url,
                            "video_url": media.video_url if hasattr(media, 'video_url') else None,
                            "media_path": None
                        }
                        
                        # Download post media
                        if media.thumbnail_url:
                            filename = f"post_{account}_{media.code}.jpg"
                            if self.download_media(media.thumbnail_url, filename):
                                post_data["media_path"] = str(self.media_dir / filename)
                        
                        account_posts["posts"].append(post_data)
                    
                    self.extracted_data["posts"].append(account_posts)
                    print(f"✅ Extracted posts from @{account}")
                    
                    time.sleep(random.uniform(3, 5))
                    
                except Exception as e:
                    print(f"❌ Failed to extract posts from @{account}: {e}")
                    continue
            
            print(f"✅ Post extraction complete")
            
        except Exception as e:
            print(f"❌ Post extraction failed: {e}")
    
    def download_media(self, url: str, filename: str) -> bool:
        """Download media file"""
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                file_path = self.media_dir / filename
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                return True
            return False
        except Exception as e:
            print(f"❌ Failed to download {filename}: {e}")
            return False
    
    def generate_pdf_report(self) -> str:
        """Generate comprehensive PDF report"""
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=16)
            
            # Title page
            pdf.cell(200, 10, txt="Instagram Extraction Report - Fleming654", ln=1, align='C')
            pdf.ln(10)
            
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Account: {self.username}", ln=1)
            pdf.cell(200, 10, txt=f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1)
            pdf.ln(10)
            
            # Summary
            pdf.set_font("Arial", "B", size=14)
            pdf.cell(200, 10, txt="EXTRACTION SUMMARY", ln=1)
            pdf.set_font("Arial", size=12)
            
            total_dms = sum(len(thread["messages"]) for thread in self.extracted_data["dms"])
            total_stories = sum(len(acc["stories"]) for acc in self.extracted_data["stories"])
            total_posts = sum(len(acc["posts"]) for acc in self.extracted_data["posts"])
            
            pdf.cell(200, 8, txt=f"DM Threads: {len(self.extracted_data['dms'])}", ln=1)
            pdf.cell(200, 8, txt=f"Total Messages: {total_dms}", ln=1)
            pdf.cell(200, 8, txt=f"Total Stories: {total_stories}", ln=1)
            pdf.cell(200, 8, txt=f"Total Posts: {total_posts}", ln=1)
            pdf.ln(10)
            
            # DMs section
            if self.extracted_data["dms"]:
                pdf.set_font("Arial", "B", size=14)
                pdf.cell(200, 10, txt="DIRECT MESSAGES", ln=1)
                pdf.set_font("Arial", size=10)
                
                for thread in self.extracted_data["dms"][:5]:  # First 5 threads
                    pdf.set_font("Arial", "B", size=11)
                    pdf.cell(200, 8, txt=f"Thread: {thread['title']}", ln=1)
                    pdf.set_font("Arial", size=9)
                    pdf.cell(200, 6, txt=f"Participants: {', '.join(thread['participants'])}", ln=1)
                    pdf.cell(200, 6, txt=f"Messages: {thread['message_count']}", ln=1)
                    
                    # Sample messages
                    for msg in thread["messages"][:3]:
                        if msg["text"]:
                            text = msg["text"][:80] + "..." if len(msg["text"]) > 80 else msg["text"]
                            pdf.cell(200, 5, txt=f"- {text}", ln=1)
                    pdf.ln(5)
            
            # Save PDF
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            pdf_path = self.results_dir / f"fleming_extraction_report_{timestamp}.pdf"
            pdf.output(str(pdf_path))
            
            print(f"📄 PDF report generated: {pdf_path}")
            return str(pdf_path)
            
        except Exception as e:
            print(f"❌ Failed to generate PDF: {e}")
            return ""
    
    def save_results(self) -> Dict[str, str]:
        """Save all results in multiple formats"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        saved_files = {}
        
        try:
            # Add metadata
            total_dms = sum(len(thread["messages"]) for thread in self.extracted_data["dms"])
            total_stories = sum(len(acc["stories"]) for acc in self.extracted_data["stories"])
            total_posts = sum(len(acc["posts"]) for acc in self.extracted_data["posts"])
            
            self.extracted_data["metadata"] = {
                "extraction_date": datetime.now().isoformat(),
                "username": self.username,
                "total_dm_threads": len(self.extracted_data["dms"]),
                "total_messages": total_dms,
                "total_stories": total_stories,
                "total_posts": total_posts,
                "media_downloaded": len(list(self.media_dir.glob("*")))
            }
            
            # Save as JSON
            json_path = self.results_dir / f"fleming_extraction_{timestamp}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self.extracted_data, f, indent=2, ensure_ascii=False)
            saved_files["json"] = str(json_path)
            
            # Save as text summary
            txt_path = self.results_dir / f"fleming_extraction_{timestamp}.txt"
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(f"Instagram Extraction Report - Fleming654\n")
                f.write(f"Account: {self.username}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*50 + "\n\n")
                
                f.write(f"SUMMARY:\n")
                f.write(f"DM Threads: {len(self.extracted_data['dms'])}\n")
                f.write(f"Total Messages: {total_dms}\n")
                f.write(f"Total Stories: {total_stories}\n")
                f.write(f"Total Posts: {total_posts}\n\n")
                
                # DMs
                f.write("DIRECT MESSAGES:\n")
                f.write("-"*30 + "\n")
                for thread in self.extracted_data["dms"]:
                    f.write(f"\nThread: {thread['title']}\n")
                    f.write(f"Participants: {', '.join(thread['participants'])}\n")
                    f.write(f"Messages: {thread['message_count']}\n")
                    for msg in thread["messages"][:5]:  # First 5 messages
                        if msg["text"]:
                            f.write(f"[{msg['timestamp']}] {msg['text']}\n")
            
            saved_files["txt"] = str(txt_path)
            
            # Generate PDF
            pdf_path = self.generate_pdf_report()
            if pdf_path:
                saved_files["pdf"] = pdf_path
            
            print(f"💾 Results saved: {len(saved_files)} files")
            return saved_files
            
        except Exception as e:
            print(f"❌ Failed to save results: {e}")
            return {}
    
    def run_complete_extraction(self):
        """Run complete extraction process"""
        print("🚀 Starting Master Production Extraction...")
        
        # Load session
        if not self.load_fleming_session():
            return {"success": False, "error": "Failed to load Fleming session"}
        
        # Extract all data types
        self.extract_dms()
        self.extract_stories() 
        self.extract_posts()
        
        # Save results
        saved_files = self.save_results()
        
        # Summary
        total_dms = sum(len(thread["messages"]) for thread in self.extracted_data["dms"])
        total_stories = sum(len(acc["stories"]) for acc in self.extracted_data["stories"])
        total_posts = sum(len(acc["posts"]) for acc in self.extracted_data["posts"])
        
        return {
            "success": True,
            "summary": {
                "dm_threads": len(self.extracted_data["dms"]),
                "total_messages": total_dms,
                "total_stories": total_stories,
                "total_posts": total_posts,
                "media_files": len(list(self.media_dir.glob("*")))
            },
            "files": saved_files,
            "data": self.extracted_data
        }

def main():
    """Main execution"""
    print("🎯 Master Production Extractor 2025 - Fleming654")
    print("="*60)
    
    extractor = MasterProductionExtractor()
    results = extractor.run_complete_extraction()
    
    print("\n" + "="*60)
    print("📊 EXTRACTION RESULTS")
    print("="*60)
    
    if results["success"]:
        summary = results["summary"]
        print(f"✅ SUCCESS!")
        print(f"📥 DM Threads: {summary['dm_threads']}")
        print(f"💬 Total Messages: {summary['total_messages']}")
        print(f"📖 Total Stories: {summary['total_stories']}")
        print(f"📸 Total Posts: {summary['total_posts']}")
        print(f"🖼️ Media Files: {summary['media_files']}")
        
        print(f"\n📁 Files saved:")
        for file_type, path in results["files"].items():
            print(f"   {file_type.upper()}: {path}")
            
        print(f"\n✅ Extraction complete! Check /workspaces/sugarglitch-realops/results/")
    else:
        print(f"❌ FAILED: {results['error']}")
    
    return results

if __name__ == "__main__":
    main()
