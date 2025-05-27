#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 ADVANCED REAL INSTAGRAM DM EXTRACTOR WITH API BYPASS 🔥
ใช้เทคนิค API Bypass และ Multiple Attack Vectors
ไม่ใช่ Simulation - เป็นการเข้าถึงจริงผ่าน Instagram API
"""

import json
import os
import sys
import time
import random
from datetime import datetime
from pathlib import Path
import requests
import base64
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
import urllib.request
from PIL import Image
import hashlib
import hmac
import uuid

class AdvancedRealAPIExtractor:
    def __init__(self):
        self.target_account = "alx.trading"
        self.verified_sessions = []
        self.current_session = None
        self.extracted_data = []
        self.user_agents = [
            "Instagram 290.0.0.48.124 Android (31/12; 420dpi; 1080x2239; Xiaomi; Redmi Note 8; ginkgo; qcom; en_US; 458229237)",
            "Instagram 290.0.0.48.124 Android (30/11; 480dpi; 1080x2340; samsung; SM-G975F; beyond2; exynos9820; en_US; 458229237)",
            "Instagram 290.0.0.48.124 iPhone14,7 (iOS 16_6; en_US; Kyiv; Scale/3.00)",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        ]
        
        print("🔥 ADVANCED REAL INSTAGRAM API DM EXTRACTOR 🔥")
        print(f"🎯 Target: {self.target_account}")
        print("📱 Mobile API + Web API Hybrid Method")
        print("🚫 NO SIMULATION - REAL API CALLS")
        print("🔒 Advanced Bypass Techniques")
        print()
        
    def load_verified_sessions(self):
        """โหลด session ที่ verified แล้ว"""
        print("🔑 กำลังโหลด verified sessions...")
        
        session_sources = [
            "data/sessions/alx_session_cookies.txt",
            "config/sessions/alx_trading_sessionid_alt.json",
            "alx_trading_active_session_20250527_050413.json",
            "alx_trading_active_session_20250527_050337.json"
        ]
        
        for source in session_sources:
            if os.path.exists(source):
                print(f"📄 Loading: {source}")
                
                if source.endswith('.txt'):
                    with open(source, 'r') as f:
                        cookie_string = f.read().strip()
                    
                    cookies = {}
                    for part in cookie_string.split(';'):
                        if '=' in part:
                            key, value = part.strip().split('=', 1)
                            cookies[key] = value
                    
                    if 'sessionid' in cookies:
                        session_data = {
                            'sessionid': cookies['sessionid'],
                            'csrftoken': cookies.get('csrftoken', ''),
                            'ds_user_id': '',
                            'source': source
                        }
                        self.verified_sessions.append(session_data)
                        
                elif source.endswith('.json'):
                    with open(source, 'r') as f:
                        session_data = json.load(f)
                    
                    if session_data.get('sessionid'):
                        session_info = {
                            'sessionid': session_data['sessionid'],
                            'csrftoken': session_data.get('csrf_token', ''),
                            'ds_user_id': session_data.get('ds_user_id', ''),
                            'source': source
                        }
                        self.verified_sessions.append(session_info)
        
        print(f"✅ Loaded {len(self.verified_sessions)} verified sessions")
        return len(self.verified_sessions) > 0
    
    def create_api_session(self, session_data):
        """สร้าง API session พร้อม headers ที่เหมือนจริง"""
        session = requests.Session()
        
        # Random user agent
        user_agent = random.choice(self.user_agents)
        
        # Instagram mobile API headers
        if "Android" in user_agent:
            headers = {
                'User-Agent': user_agent,
                'Accept': '*/*',
                'Accept-Language': 'en-US',
                'Accept-Encoding': 'gzip, deflate',
                'X-IG-App-ID': '567067343352427',
                'X-IG-App-Locale': 'en_US',
                'X-IG-Device-Locale': 'en_US',
                'X-IG-Device-ID': str(uuid.uuid4()),
                'X-IG-Family-Device-ID': str(uuid.uuid4()),
                'X-IG-Android-ID': f"android-{hashlib.md5(os.urandom(16)).hexdigest()[:16]}",
                'X-ASBD-ID': '129477',
                'X-IG-Connection-Speed': f'{random.randint(1000, 5000)}kbps',
                'X-IG-Bandwidth-Speed-KBPS': str(random.randint(2000, 8000)),
                'X-IG-Bandwidth-TotalBytes-B': str(random.randint(5000000, 20000000)),
                'X-IG-Bandwidth-TotalTime-MS': str(random.randint(500, 2000)),
                'X-IG-WWW-Claim': '0',
                'X-Bloks-Version-ID': '5f56efad68e1edec7801f630b5c122704ec5378adbee6609a448f105f34a9c73',
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Capabilities': '3brTvwM=',
                'X-IG-App-Startup-Country': 'US',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'i.instagram.com'
            }
        else:
            # iOS headers
            headers = {
                'User-Agent': user_agent,
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'X-IG-App-ID': '567067343352427',
                'X-IG-WWW-Claim': '0',
                'X-Requested-With': 'XMLHttpRequest',
                'Origin': 'https://www.instagram.com',
                'Referer': 'https://www.instagram.com/',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        
        # Add session cookies
        sessionid = session_data.get('sessionid')
        if sessionid:
            session.cookies.set('sessionid', sessionid, domain='.instagram.com')
        
        csrftoken = session_data.get('csrftoken')
        if csrftoken:
            session.cookies.set('csrftoken', csrftoken, domain='.instagram.com')
            headers['X-CSRFToken'] = csrftoken
        
        ds_user_id = session_data.get('ds_user_id')
        if ds_user_id:
            session.cookies.set('ds_user_id', ds_user_id, domain='.instagram.com')
        
        # Additional cookies
        session.cookies.set('mid', f'ZnBMeQABAAF8k9f3nQP-{random.randint(100000, 999999)}', domain='.instagram.com')
        session.cookies.set('ig_did', str(uuid.uuid4()), domain='.instagram.com')
        session.cookies.set('ig_nrcb', '1', domain='.instagram.com')
        session.cookies.set('rur', random.choice(['VLL', 'ATN', 'FRC', 'PRN']), domain='.instagram.com')
        
        session.headers.update(headers)
        return session
    
    def test_session_validity(self, session):
        """ทดสอบความถูกต้องของ session"""
        print("🧪 กำลังทดสอบ session validity...")
        
        # Test endpoints in order of priority
        test_endpoints = [
            # Direct inbox check
            ('https://www.instagram.com/api/v1/direct_v2/inbox/', 'Direct Inbox API'),
            # Account info
            ('https://www.instagram.com/accounts/edit/', 'Account Edit'),
            # Main feed
            ('https://www.instagram.com/api/v1/feed/timeline/', 'Timeline Feed'),
            # User info
            ('https://i.instagram.com/api/v1/accounts/current_user/', 'Current User API'),
        ]
        
        for url, name in test_endpoints:
            try:
                print(f"🔍 Testing: {name}")
                response = session.get(url, timeout=15)
                
                print(f"📊 Status: {response.status_code}")
                
                if response.status_code == 200:
                    content = response.text
                    
                    # Check for success indicators
                    if any(keyword in content.lower() for keyword in ['inbox', 'threads', 'user', 'feed', 'status']):
                        print(f"✅ {name} - Session Valid!")
                        return True, url
                    
                elif response.status_code == 302:
                    print(f"⚠️ {name} - Redirected (possibly valid)")
                    continue
                    
                elif response.status_code == 429:
                    print(f"⚠️ {name} - Rate limited, but session might be valid")
                    time.sleep(random.uniform(3, 8))
                    continue
                    
                else:
                    print(f"❌ {name} - HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {name} - Error: {e}")
                continue
        
        print("❌ All endpoint tests failed")
        return False, None
    
    def extract_via_direct_api(self, session):
        """ดึงข้อมูล DMs ผ่าน Direct API"""
        print("📥 กำลังดึงข้อมูล DMs ผ่าน Direct API...")
        
        extracted_conversations = []
        
        # Instagram Direct API endpoints
        api_endpoints = [
            'https://www.instagram.com/api/v1/direct_v2/inbox/',
            'https://i.instagram.com/api/v1/direct_v2/inbox/',
            'https://www.instagram.com/api/v1/direct_v2/threads/',
        ]
        
        for endpoint in api_endpoints:
            try:
                print(f"🔗 Trying endpoint: {endpoint}")
                
                # Add random delay
                time.sleep(random.uniform(2, 5))
                
                response = session.get(endpoint, timeout=20)
                
                print(f"📊 Response: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        
                        # Parse inbox data
                        if 'inbox' in data:
                            inbox = data['inbox']
                            threads = inbox.get('threads', [])
                            
                            print(f"✅ Found {len(threads)} threads!")
                            
                            for thread in threads:
                                conv_data = self.parse_thread_data(thread)
                                if conv_data:
                                    extracted_conversations.append(conv_data)
                            
                            return extracted_conversations
                        
                        elif 'threads' in data:
                            threads = data['threads']
                            print(f"✅ Found {len(threads)} threads!")
                            
                            for thread in threads:
                                conv_data = self.parse_thread_data(thread)
                                if conv_data:
                                    extracted_conversations.append(conv_data)
                            
                            return extracted_conversations
                        
                        else:
                            print("⚠️ Unexpected API response structure")
                            # Save raw response for analysis
                            self.save_raw_response(data, endpoint)
                    
                    except json.JSONDecodeError:
                        print("❌ Invalid JSON response")
                        continue
                
                elif response.status_code == 429:
                    print("⚠️ Rate limited - waiting...")
                    time.sleep(random.uniform(10, 20))
                    continue
                
                else:
                    print(f"❌ HTTP Error: {response.status_code}")
                    if response.status_code == 403:
                        print("🔒 Access forbidden - session might be expired")
                    
            except Exception as e:
                print(f"❌ API Error: {e}")
                continue
        
        return extracted_conversations
    
    def parse_thread_data(self, thread):
        """แยกข้อมูลจาก thread"""
        try:
            conversation = {
                'thread_id': thread.get('thread_id'),
                'thread_title': thread.get('thread_title'),
                'participants': [],
                'messages': [],
                'last_activity': thread.get('last_activity_at'),
                'message_count': len(thread.get('items', []))
            }
            
            # Parse users
            users = thread.get('users', [])
            for user in users:
                participant = {
                    'user_id': user.get('pk'),
                    'username': user.get('username'),
                    'full_name': user.get('full_name'),
                    'profile_pic': user.get('profile_pic_url'),
                    'is_verified': user.get('is_verified', False)
                }
                conversation['participants'].append(participant)
            
            # Parse messages
            items = thread.get('items', [])
            for item in items:
                message = self.parse_message_item(item)
                if message:
                    conversation['messages'].append(message)
            
            return conversation
            
        except Exception as e:
            print(f"⚠️ Thread parsing error: {e}")
            return None
    
    def parse_message_item(self, item):
        """แยกข้อมูลจาก message item"""
        try:
            message = {
                'item_id': item.get('item_id'),
                'user_id': item.get('user_id'),
                'timestamp': item.get('timestamp'),
                'item_type': item.get('item_type'),
                'text': item.get('text', ''),
                'media': None
            }
            
            # Check for media
            if 'media' in item and item['media']:
                media = item['media']
                message['media'] = {
                    'media_type': media.get('media_type'),
                    'image_url': None,
                    'video_url': None
                }
                
                # Extract image URL
                if 'image_versions2' in media:
                    candidates = media['image_versions2'].get('candidates', [])
                    if candidates:
                        message['media']['image_url'] = candidates[0].get('url')
                
                # Extract video URL
                if 'video_versions' in media:
                    versions = media['video_versions']
                    if versions:
                        message['media']['video_url'] = versions[0].get('url')
            
            return message
            
        except Exception as e:
            print(f"⚠️ Message parsing error: {e}")
            return None
    
    def save_raw_response(self, data, endpoint):
        """บันทึก raw response สำหรับการวิเคราะห์"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"raw_api_response_{timestamp}.json"
        
        os.makedirs("data/debug", exist_ok=True)
        filepath = os.path.join("data/debug", filename)
        
        debug_data = {
            'endpoint': endpoint,
            'timestamp': timestamp,
            'response': data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(debug_data, f, indent=2, ensure_ascii=False)
        
        print(f"🐛 Raw response saved: {filepath}")
    
    def download_media_files(self, conversations, output_dir):
        """ดาวน์โหลดไฟล์สื่อจาก conversations"""
        print("🖼️ กำลังดาวน์โหลดไฟล์สื่อ...")
        
        media_dir = os.path.join(output_dir, 'media')
        os.makedirs(media_dir, exist_ok=True)
        
        downloaded_files = []
        
        for conv_idx, conversation in enumerate(conversations):
            for msg_idx, message in enumerate(conversation.get('messages', [])):
                media = message.get('media')
                
                if media:
                    # Download image
                    image_url = media.get('image_url')
                    if image_url:
                        try:
                            filename = f"conv_{conv_idx}_msg_{msg_idx}_image.jpg"
                            filepath = os.path.join(media_dir, filename)
                            
                            # Download with session
                            response = requests.get(image_url, timeout=30)
                            if response.status_code == 200:
                                with open(filepath, 'wb') as f:
                                    f.write(response.content)
                                
                                downloaded_files.append({
                                    'type': 'image',
                                    'conversation_index': conv_idx,
                                    'message_index': msg_idx,
                                    'original_url': image_url,
                                    'local_path': filepath,
                                    'filename': filename
                                })
                                
                                print(f"✅ Downloaded: {filename}")
                        
                        except Exception as e:
                            print(f"❌ Download error: {e}")
                    
                    # Download video
                    video_url = media.get('video_url')
                    if video_url:
                        try:
                            filename = f"conv_{conv_idx}_msg_{msg_idx}_video.mp4"
                            filepath = os.path.join(media_dir, filename)
                            
                            response = requests.get(video_url, timeout=60)
                            if response.status_code == 200:
                                with open(filepath, 'wb') as f:
                                    f.write(response.content)
                                
                                downloaded_files.append({
                                    'type': 'video',
                                    'conversation_index': conv_idx,
                                    'message_index': msg_idx,
                                    'original_url': video_url,
                                    'local_path': filepath,
                                    'filename': filename
                                })
                                
                                print(f"✅ Downloaded: {filename}")
                        
                        except Exception as e:
                            print(f"❌ Video download error: {e}")
        
        print(f"📊 Total media files downloaded: {len(downloaded_files)}")
        return downloaded_files
    
    def create_comprehensive_pdf(self, conversations, media_files, output_dir):
        """สร้าง PDF รายงานแบบครอบคลุม"""
        print("📄 กำลังสร้าง comprehensive PDF report...")
        
        try:
            pdf_file = os.path.join(output_dir, 'ALX_TRADING_REAL_API_EXTRACTION.pdf')
            doc = SimpleDocTemplate(pdf_file, pagesize=A4)
            story = []
            
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'Title',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                textColor=HexColor('#E1306C'),
                alignment=1  # Center
            )
            
            subtitle_style = ParagraphStyle(
                'Subtitle',
                parent=styles['Heading2'],
                fontSize=18,
                spaceAfter=20,
                textColor=HexColor('#405DE6')
            )
            
            # Title page
            story.append(Paragraph("🔥 REAL INSTAGRAM DM EXTRACTION 🔥", title_style))
            story.append(Spacer(1, 20))
            story.append(Paragraph(f"Target Account: {self.target_account}", subtitle_style))
            story.append(Paragraph(f"Extraction Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            story.append(Paragraph("Method: Advanced API Bypass", styles['Normal']))
            story.append(Spacer(1, 40))
            
            # Summary
            story.append(Paragraph("📊 Extraction Summary", subtitle_style))
            story.append(Paragraph(f"• Total Conversations: {len(conversations)}", styles['Normal']))
            total_messages = sum(len(conv.get('messages', [])) for conv in conversations)
            story.append(Paragraph(f"• Total Messages: {total_messages}", styles['Normal']))
            story.append(Paragraph(f"• Media Files Downloaded: {len(media_files)}", styles['Normal']))
            story.append(Spacer(1, 30))
            
            # Conversations detail
            for i, conversation in enumerate(conversations):
                story.append(Paragraph(f"💬 Conversation #{i+1}", subtitle_style))
                
                # Participants
                participants = conversation.get('participants', [])
                if participants:
                    participants_text = ", ".join([p.get('username', 'Unknown') for p in participants])
                    story.append(Paragraph(f"👥 Participants: {participants_text}", styles['Normal']))
                
                # Message count
                messages = conversation.get('messages', [])
                story.append(Paragraph(f"📝 Messages: {len(messages)}", styles['Normal']))
                
                # Sample messages
                for j, message in enumerate(messages[:10]):  # Show first 10 messages
                    if message.get('text'):
                        story.append(Paragraph(f"• {message['text'][:150]}...", styles['Normal']))
                
                story.append(Spacer(1, 20))
            
            # Build PDF
            doc.build(story)
            print(f"✅ PDF report created: {pdf_file}")
            return pdf_file
            
        except Exception as e:
            print(f"❌ PDF creation error: {e}")
            return None
    
    def run_advanced_extraction(self):
        """รันการดึงข้อมูลแบบ advanced"""
        print("🚀 เริ่มต้น ADVANCED REAL API EXTRACTION")
        print("=" * 60)
        
        try:
            # Step 1: Load sessions
            if not self.load_verified_sessions():
                print("❌ No verified sessions available")
                return False
            
            # Step 2: Try each session
            for i, session_data in enumerate(self.verified_sessions):
                print(f"\n🔄 Testing session {i+1}/{len(self.verified_sessions)}")
                print(f"📄 Source: {session_data.get('source')}")
                
                # Create API session
                api_session = self.create_api_session(session_data)
                
                # Test session
                is_valid, working_endpoint = self.test_session_validity(api_session)
                
                if is_valid:
                    print("✅ Session validated! Extracting data...")
                    self.current_session = api_session
                    
                    # Extract conversations
                    conversations = self.extract_via_direct_api(api_session)
                    
                    if conversations:
                        print(f"✅ Extracted {len(conversations)} conversations")
                        
                        # Create output directory
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_dir = f"data/extractions/ADVANCED_REAL_API_ALX_{timestamp}"
                        os.makedirs(output_dir, exist_ok=True)
                        
                        # Download media
                        media_files = self.download_media_files(conversations, output_dir)
                        
                        # Save extraction data
                        extraction_data = {
                            'target': self.target_account,
                            'extraction_timestamp': datetime.now().isoformat(),
                            'method': 'advanced_api_bypass',
                            'session_source': session_data.get('source'),
                            'total_conversations': len(conversations),
                            'total_messages': sum(len(c.get('messages', [])) for c in conversations),
                            'total_media': len(media_files),
                            'conversations': conversations,
                            'media_files': media_files
                        }
                        
                        # Save JSON
                        json_file = os.path.join(output_dir, 'advanced_api_extraction.json')
                        with open(json_file, 'w', encoding='utf-8') as f:
                            json.dump(extraction_data, f, indent=2, ensure_ascii=False)
                        
                        # Create PDF
                        pdf_file = self.create_comprehensive_pdf(conversations, media_files, output_dir)
                        
                        print("\n🎉 ADVANCED API EXTRACTION COMPLETED!")
                        print("=" * 50)
                        print(f"📁 Output Directory: {output_dir}")
                        print(f"💬 Conversations: {len(conversations)}")
                        print(f"📝 Total Messages: {extraction_data['total_messages']}")
                        print(f"🖼️ Media Files: {len(media_files)}")
                        if pdf_file:
                            print(f"📄 PDF Report: {pdf_file}")
                        
                        return True
                    
                    else:
                        print("⚠️ No conversations extracted")
                        continue
                
                else:
                    print("❌ Session validation failed")
                    continue
            
            print("❌ All sessions failed validation")
            return False
            
        except Exception as e:
            print(f"❌ Extraction error: {e}")
            return False

def main():
    """Main function"""
    print("🔥 SUGARGLITCH REALOPS - ADVANCED REAL API EXTRACTOR 🔥")
    print("ดึงข้อมูล Instagram DMs จริงด้วย Advanced API Bypass")
    print("🚫 NO SIMULATION - REAL API EXTRACTION")
    print()
    
    extractor = AdvancedRealAPIExtractor()
    
    try:
        success = extractor.run_advanced_extraction()
        
        if success:
            print("\n✅ ADVANCED API EXTRACTION MISSION ACCOMPLISHED!")
            print("ดึงข้อมูล DMs จริงผ่าน API สำเร็จแล้ว")
        else:
            print("\n❌ ADVANCED API EXTRACTION MISSION FAILED!")
            print("ไม่สามารถดึงข้อมูลจริงผ่าน API ได้")
            
    except KeyboardInterrupt:
        print("\n⚠️ การดำเนินการถูกยกเลิก")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
