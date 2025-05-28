#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 REAL STEALTH INSTAGRAM DM EXTRACTOR 🔥
ใช้เทคนิค Browser Automation เพื่อเข้าถึงข้อมูลจริง
ไม่ใช่ Simulation - เป็นการเข้าถึงจริงผ่าน Browser
"""

import json
import os
import sys
import time
import random
from datetime import datetime
from pathlib import Path
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import base64
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
import urllib.request
from PIL import Image

class RealStealthDMExtractor:
    def __init__(self):
        self.target_account = "alx.trading"
        self.driver = None
        self.verified_sessions = []
        self.current_session_index = 0
        self.extracted_conversations = []
        self.downloaded_images = []
        
        print("🔥 REAL STEALTH INSTAGRAM DM EXTRACTOR 🔥")
        print(f"🎯 Target: {self.target_account}")
        print("🤖 Browser Automation Method")
        print("🚫 NO SIMULATION - REAL DATA EXTRACTION")
        print("🔒 Anti-Detection Measures Enabled")
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
                    
                    # Parse cookies
                    cookies = {}
                    for part in cookie_string.split(';'):
                        if '=' in part:
                            key, value = part.strip().split('=', 1)
                            cookies[key] = value
                    
                    if 'sessionid' in cookies:
                        session_data = {
                            'sessionid': cookies['sessionid'],
                            'csrftoken': cookies.get('csrftoken', 'missing'),
                            'rur': cookies.get('rur', 'VLL'),
                            'source': source
                        }
                        self.verified_sessions.append(session_data)
                        
                elif source.endswith('.json'):
                    with open(source, 'r') as f:
                        session_data = json.load(f)
                    
                    if session_data.get('sessionid'):
                        session_info = {
                            'sessionid': session_data['sessionid'],
                            'csrftoken': session_data.get('csrf_token', 'missing'),
                            'ds_user_id': session_data.get('ds_user_id', ''),
                            'source': source
                        }
                        self.verified_sessions.append(session_info)
        
        print(f"✅ Loaded {len(self.verified_sessions)} verified sessions")
        return len(self.verified_sessions) > 0
    
    def setup_stealth_browser(self):
        """ตั้งค่า browser แบบ stealth เพื่อหลีกเลี่ยงการตรวจจับ"""
        print("🤖 กำลังตั้งค่า stealth browser...")
        
        # Use remote Selenium endpoint (Browser API)
        print("🌐 Connecting to remote Browser API endpoint for Selenium...")
        selenium_remote_url = "https://brd-customer-hl_63f0835e-zone-scraping_browser1:bj0nymiw6mij@brd.superproxy.io:9515"
        chrome_options = Options()
        # You may still set user-agent and other stealth options if needed
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
        try:
            self.driver = webdriver.Remote(
                command_executor=selenium_remote_url,
                options=chrome_options
            )
            # Execute script to hide automation indicators
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("✅ Connected to remote Browser API and initialized browser!")
            return True
            
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False
    
    def inject_session_cookies(self, session_data):
        """ฉีด session cookies เข้าไปใน browser"""
        print(f"🍪 กำลังฉีด session cookies...")
        
        try:
            # Navigate to Instagram first
            self.driver.get("https://www.instagram.com/")
            time.sleep(2)
            
            # Inject cookies
            cookies_to_set = [
                {'name': 'sessionid', 'value': session_data['sessionid'], 'domain': '.instagram.com'},
                {'name': 'csrftoken', 'value': session_data.get('csrftoken', 'missing'), 'domain': '.instagram.com'},
                {'name': 'mid', 'value': 'ZnBMeQABAAF8k9f3nQP-s71Bk5wZ', 'domain': '.instagram.com'},
                {'name': 'ig_did', 'value': 'A1B2C3D4-E5F6-7890-ABCD-EF1234567890', 'domain': '.instagram.com'},
                {'name': 'ig_nrcb', 'value': '1', 'domain': '.instagram.com'}
            ]
            
            if session_data.get('ds_user_id'):
                cookies_to_set.append({
                    'name': 'ds_user_id', 
                    'value': session_data['ds_user_id'], 
                    'domain': '.instagram.com'
                })
            
            if session_data.get('rur'):
                cookies_to_set.append({
                    'name': 'rur', 
                    'value': session_data['rur'], 
                    'domain': '.instagram.com'
                })
            
            for cookie in cookies_to_set:
                self.driver.add_cookie(cookie)
            
            print(f"✅ Injected {len(cookies_to_set)} cookies")
            
            # Refresh to apply cookies
            self.driver.refresh()
            time.sleep(3)
            
            return True
            
        except Exception as e:
            print(f"❌ Cookie injection failed: {e}")
            return False
    
    def verify_login_status(self):
        """ตรวจสอบสถานะการ login ใน browser"""
        print("🧪 กำลังตรวจสอบ login status...")
        
        try:
            # Check for login indicators
            current_url = self.driver.current_url
            print(f"📍 Current URL: {current_url}")
            
            # Method 1: Check for user menu
            try:
                user_menu = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='user-avatar']"))
                )
                print("✅ Found user avatar - logged in!")
                return True
            except TimeoutException:
                pass
            
            # Method 2: Check for profile link in navigation
            try:
                profile_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/']")
                for link in profile_links:
                    href = link.get_attribute('href')
                    if href and self.target_account in href:
                        print(f"✅ Found profile link: {href}")
                        return True
            except:
                pass
            
            # Method 3: Check page content
            page_source = self.driver.page_source
            if 'is_logged_in' in page_source or 'sessionStorage' in page_source:
                print("✅ Login indicators found in page source")
                return True
            
            # Method 4: Try to access DM directly
            dm_url = "https://www.instagram.com/direct/inbox/"
            self.driver.get(dm_url)
            time.sleep(5)
            
            if "direct" in self.driver.current_url and "login" not in self.driver.current_url:
                print("✅ Successfully accessed DM inbox!")
                return True
            
            print("❌ Login verification failed")
            return False
            
        except Exception as e:
            print(f"❌ Login verification error: {e}")
            return False
    
    def navigate_to_dm_inbox(self):
        """เข้าไปยังหน้า DM inbox"""
        print("📥 กำลังเข้าไปยัง DM inbox...")
        
        try:
            dm_url = "https://www.instagram.com/direct/inbox/"
            self.driver.get(dm_url)
            
            # Wait for page to load
            time.sleep(5)
            
            # Check if we're in the right place
            if "direct" in self.driver.current_url:
                print("✅ Successfully navigated to DM inbox")
                return True
            else:
                print(f"❌ Failed to reach DM inbox. Current URL: {self.driver.current_url}")
                return False
                
        except Exception as e:
            print(f"❌ Navigation error: {e}")
            return False
    
    def extract_conversation_list(self):
        """ดึงรายการ conversations จากหน้า DM"""
        print("💬 กำลังดึงรายการ conversations...")
        
        conversations = []
        
        try:
            # Wait for conversation list to load
            time.sleep(5)
            
            # Look for conversation elements
            conversation_selectors = [
                "[role='button'][tabindex='0']",  # Common conversation button
                "div[role='listitem']",  # List item role
                "a[href*='/direct/t/']",  # Direct thread links
                ".x1n2onr6",  # Instagram specific classes (may change)
                "[data-testid*='conversation']"  # Testid patterns
            ]
            
            for selector in conversation_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"🔍 Found {len(elements)} elements with selector: {selector}")
                    
                    for element in elements:
                        try:
                            # Extract conversation info
                            conv_data = self.extract_conversation_data(element)
                            if conv_data:
                                conversations.append(conv_data)
                        except:
                            continue
                            
                except Exception as e:
                    print(f"⚠️ Selector {selector} failed: {e}")
                    continue
            
            # Remove duplicates
            unique_conversations = []
            seen_ids = set()
            
            for conv in conversations:
                conv_id = conv.get('id', conv.get('href', ''))
                if conv_id and conv_id not in seen_ids:
                    unique_conversations.append(conv)
                    seen_ids.add(conv_id)
            
            print(f"✅ Found {len(unique_conversations)} unique conversations")
            return unique_conversations
            
        except Exception as e:
            print(f"❌ Conversation extraction error: {e}")
            return []
    
    def extract_conversation_data(self, element):
        """ดึงข้อมูลจาก conversation element"""
        try:
            conv_data = {}
            
            # Get conversation link
            href = element.get_attribute('href')
            if href and '/direct/t/' in href:
                conv_data['href'] = href
                conv_data['id'] = href.split('/direct/t/')[-1].split('/')[0]
            
            # Get participant name
            try:
                text_content = element.text
                if text_content:
                    conv_data['preview_text'] = text_content.strip()
            except:
                pass
            
            # Get any image elements
            try:
                img_elements = element.find_elements(By.TAG_NAME, 'img')
                if img_elements:
                    conv_data['has_avatar'] = True
                    conv_data['avatar_src'] = img_elements[0].get_attribute('src')
            except:
                pass
            
            return conv_data if conv_data else None
            
        except Exception as e:
            print(f"⚠️ Element extraction error: {e}")
            return None
    
    def extract_conversation_messages(self, conv_data):
        """เข้าไปดึงข้อความจาก conversation"""
        print(f"📝 กำลังดึงข้อความจาก conversation: {conv_data.get('id', 'Unknown')}")
        
        messages = []
        images = []
        
        try:
            if conv_data.get('href'):
                self.driver.get(conv_data['href'])
                time.sleep(3)
                
                # Wait for messages to load
                self.simulate_human_behavior()
                
                # Scroll to load more messages
                self.scroll_to_load_messages()
                
                # Extract messages
                message_elements = self.find_message_elements()
                
                for element in message_elements:
                    message_data = self.extract_message_data(element)
                    if message_data:
                        messages.append(message_data)
                        
                        # Check for images in message
                        if message_data.get('has_image'):
                            image_data = self.extract_image_from_message(element, message_data)
                            if image_data:
                                images.append(image_data)
                
                print(f"✅ Extracted {len(messages)} messages, {len(images)} images")
                
        except Exception as e:
            print(f"❌ Message extraction error: {e}")
        
        return messages, images
    
    def find_message_elements(self):
        """ค้นหา message elements ในหน้า conversation"""
        message_elements = []
        
        # Common message selectors
        selectors = [
            "[role='listitem']",
            ".x1n2onr6",  # Instagram message container
            "div[dir='auto']",  # Text direction auto
            "[data-testid*='message']"
        ]
        
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                message_elements.extend(elements)
            except:
                continue
        
        return message_elements
    
    def extract_message_data(self, element):
        """ดึงข้อมูลจาก message element"""
        try:
            message_data = {
                'timestamp': datetime.now().isoformat(),
                'text': '',
                'has_image': False,
                'sender': 'unknown'
            }
            
            # Extract text content
            text_content = element.text
            if text_content:
                message_data['text'] = text_content.strip()
            
            # Check for images
            img_elements = element.find_elements(By.TAG_NAME, 'img')
            if img_elements:
                message_data['has_image'] = True
                message_data['image_count'] = len(img_elements)
            
            # Try to determine sender
            # Look for visual indicators or position
            element_html = element.get_attribute('outerHTML')
            if 'right' in element_html or 'sent' in element_html:
                message_data['sender'] = 'self'
            elif 'left' in element_html or 'received' in element_html:
                message_data['sender'] = 'other'
            
            return message_data
            
        except Exception as e:
            print(f"⚠️ Message data extraction error: {e}")
            return None
    
    def extract_image_from_message(self, element, message_data):
        """ดึงรูปภาพจาก message"""
        try:
            img_elements = element.find_elements(By.TAG_NAME, 'img')
            
            for img in img_elements:
                src = img.get_attribute('src')
                if src and 'http' in src:
                    image_data = {
                        'message_id': message_data.get('timestamp'),
                        'src': src,
                        'alt': img.get_attribute('alt'),
                        'sender': message_data.get('sender'),
                        'extracted_at': datetime.now().isoformat()
                    }
                    return image_data
            
        except Exception as e:
            print(f"⚠️ Image extraction error: {e}")
        
        return None
    
    def scroll_to_load_messages(self):
        """เลื่อนหน้าเพื่อโหลดข้อความเพิ่มเติม"""
        print("📜 กำลังเลื่อนเพื่อโหลดข้อความเพิ่มเติม...")
        
        try:
            # Scroll up to load older messages
            for i in range(5):  # Scroll 5 times
                self.driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(2)
                
                # Random human-like delay
                time.sleep(random.uniform(1, 3))
            
            # Scroll back down
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
        except Exception as e:
            print(f"⚠️ Scrolling error: {e}")
    
    def simulate_human_behavior(self):
        """จำลองพฤติกรรมของมนุษย์"""
        # Random mouse movements
        try:
            action = ActionChains(self.driver)
            action.move_by_offset(random.randint(10, 100), random.randint(10, 100))
            action.perform()
        except:
            pass
        
        # Random delay
        time.sleep(random.uniform(1, 3))
    
    def download_images_from_browser(self, images, output_dir):
        """ดาวน์โหลดรูปภาพผ่าน browser session"""
        print("🖼️ กำลังดาวน์โหลดรูปภาพผ่าน browser...")
        
        images_dir = os.path.join(output_dir, 'images')
        os.makedirs(images_dir, exist_ok=True)
        
        downloaded = []
        
        for i, image_data in enumerate(images):
            try:
                src = image_data.get('src')
                if not src:
                    continue
                
                # Use browser to download with session
                self.driver.get(src)
                time.sleep(2)
                
                # Get image as base64
                image_base64 = self.driver.execute_script("""
                    var canvas = document.createElement('canvas');
                    var ctx = canvas.getContext('2d');
                    var img = document.querySelector('img');
                    if (img) {
                        canvas.width = img.naturalWidth;
                        canvas.height = img.naturalHeight;
                        ctx.drawImage(img, 0, 0);
                        return canvas.toDataURL('image/jpeg');
                    }
                    return null;
                """)
                
                if image_base64:
                    # Decode and save
                    image_data_clean = image_base64.split(',')[1]
                    image_bytes = base64.b64decode(image_data_clean)
                    
                    filename = f"dm_image_{i}_{image_data.get('message_id', 'unknown')}.jpg"
                    filepath = os.path.join(images_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(image_bytes)
                    
                    downloaded.append({
                        **image_data,
                        'local_path': filepath,
                        'filename': filename
                    })
                    
                    print(f"✅ Downloaded: {filename}")
                
            except Exception as e:
                print(f"❌ Download error for image {i}: {e}")
                continue
        
        return downloaded
    
    def run_real_extraction(self):
        """รันการดึงข้อมูลจริง"""
        print("🚀 เริ่มต้น REAL DM Extraction")
        print("=" * 60)
        
        try:
            # Step 1: Load verified sessions
            if not self.load_verified_sessions():
                print("❌ No verified sessions available")
                return False
            
            # Step 2: Setup stealth browser
            if not self.setup_stealth_browser():
                print("❌ Browser setup failed")
                return False
            
            # Step 3: Try each session until one works
            for i, session_data in enumerate(self.verified_sessions):
                print(f"\n🔄 Trying session {i+1}/{len(self.verified_sessions)}")
                print(f"📄 Source: {session_data.get('source', 'Unknown')}")
                
                # Inject session cookies
                if not self.inject_session_cookies(session_data):
                    continue
                
                # Verify login
                if not self.verify_login_status():
                    print("❌ Session verification failed, trying next...")
                    continue
                
                print("✅ Session verified! Proceeding with extraction...")
                
                # Step 4: Navigate to DM inbox
                if not self.navigate_to_dm_inbox():
                    continue
                
                # Step 5: Extract conversations
                conversations = self.extract_conversation_list()
                if not conversations:
                    print("⚠️ No conversations found")
                    continue
                
                # Step 6: Extract messages from each conversation
                all_messages = []
                all_images = []
                
                for conv in conversations[:5]:  # Limit to first 5 conversations
                    messages, images = self.extract_conversation_messages(conv)
                    all_messages.extend(messages)
                    all_images.extend(images)
                
                # Step 7: Create output directory
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_dir = f"data/extractions/REAL_ALX_DMs_{timestamp}"
                os.makedirs(output_dir, exist_ok=True)
                
                # Step 8: Download images
                downloaded_images = self.download_images_from_browser(all_images, output_dir)
                
                # Step 9: Save extraction data
                extraction_data = {
                    'target': self.target_account,
                    'extraction_timestamp': datetime.now().isoformat(),
                    'method': 'real_browser_automation',
                    'session_source': session_data.get('source'),
                    'conversations_found': len(conversations),
                    'messages_extracted': len(all_messages),
                    'images_downloaded': len(downloaded_images),
                    'conversations': conversations,
                    'messages': all_messages,
                    'images': downloaded_images
                }
                
                # Save JSON data
                json_file = os.path.join(output_dir, 'real_dm_extraction.json')
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(extraction_data, f, indent=2, ensure_ascii=False)
                
                # Step 10: Create PDF report
                self.create_real_pdf_report(extraction_data, output_dir)
                
                print("\n🎉 REAL EXTRACTION COMPLETED!")
                print("=" * 50)
                print(f"📁 Output: {output_dir}")
                print(f"💬 Conversations: {len(conversations)}")
                print(f"📝 Messages: {len(all_messages)}")
                print(f"🖼️ Images: {len(downloaded_images)}")
                
                return True
            
            print("❌ All sessions failed")
            return False
            
        except Exception as e:
            print(f"❌ Extraction error: {e}")
            return False
            
        finally:
            if self.driver:
                print("🔚 Closing browser...")
                self.driver.quit()
    
    def create_real_pdf_report(self, data, output_dir):
        """สร้าง PDF report จากข้อมูลจริง"""
        print("📄 กำลังสร้าง PDF report...")
        
        try:
            pdf_file = os.path.join(output_dir, 'ALX_TRADING_REAL_DM_REPORT.pdf')
            doc = SimpleDocTemplate(pdf_file, pagesize=A4)
            story = []
            
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=20,
                spaceAfter=30,
                textColor=HexColor('#E1306C')
            )
            
            # Title
            story.append(Paragraph("🔥 REAL Instagram DM Extraction Report 🔥", title_style))
            story.append(Paragraph(f"Target: {data['target']}", styles['Heading2']))
            story.append(Paragraph(f"Extracted: {data['extraction_timestamp']}", styles['Normal']))
            story.append(Paragraph(f"Method: {data['method']}", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Summary
            story.append(Paragraph("📊 Extraction Summary", styles['Heading2']))
            story.append(Paragraph(f"• Conversations Found: {data['conversations_found']}", styles['Normal']))
            story.append(Paragraph(f"• Messages Extracted: {data['messages_extracted']}", styles['Normal']))
            story.append(Paragraph(f"• Images Downloaded: {data['images_downloaded']}", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Messages
            story.append(Paragraph("💬 Extracted Messages", styles['Heading2']))
            for i, message in enumerate(data.get('messages', [])[:20]):  # First 20 messages
                if message.get('text'):
                    story.append(Paragraph(f"{i+1}. {message['text'][:200]}...", styles['Normal']))
                story.append(Spacer(1, 5))
            
            doc.build(story)
            print(f"✅ PDF report created: {pdf_file}")
            
        except Exception as e:
            print(f"❌ PDF creation error: {e}")

def main():
    """Main function"""
    print("🔥 SUGARGLITCH REALOPS - REAL STEALTH DM EXTRACTOR 🔥")
    print("ดึงข้อมูล Instagram DMs จริงด้วย Browser Automation")
    print("🚫 NO SIMULATION - REAL DATA EXTRACTION")
    print()
    
    extractor = RealStealthDMExtractor()
    
    try:
        success = extractor.run_real_extraction()
        
        if success:
            print("\n✅ REAL EXTRACTION MISSION ACCOMPLISHED!")
            print("ดึงข้อมูล DMs จริงสำเร็จแล้ว")
        else:
            print("\n❌ REAL EXTRACTION MISSION FAILED!")
            print("ไม่สามารถดึงข้อมูลจริงได้")
            
    except KeyboardInterrupt:
        print("\n⚠️ การดำเนินการถูกยกเลิก")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
