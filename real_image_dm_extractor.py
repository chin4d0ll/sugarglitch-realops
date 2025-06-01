#!/usr/bin/env python3
"""
🔥💀 REAL IMAGE & DM EXTRACTOR 2025 💀🔥
======================================
ดึงรูปภาพและ DM จริงๆ ไม่ใช่ mock!

Features:
📸 Real Image Download
💬 Real DM Extraction
🍪 Real Cookie Management
📱 Real Browser Automation
"""

import os
import sys
import json
import time
import requests
import sqlite3
from datetime import datetime
from pathlib import Path
import base64
import hashlib

# Try selenium for real browser automation
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import undetected_chromedriver as uc
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

class RealImageDMExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.driver = None
        self.database_path = "extracted_images_dms.db"
        self.images_folder = "extracted_images_real"
        self.dms_folder = "extracted_dms_real"
        
        # Real Instagram headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        
        self.session.headers.update(self.headers)
        self._setup_folders_and_db()
    
    def _setup_folders_and_db(self):
        """Setup real folders and database"""
        os.makedirs(self.images_folder, exist_ok=True)
        os.makedirs(self.dms_folder, exist_ok=True)
        
        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()
        
        # Real tables for extracted data
        c.execute('''CREATE TABLE IF NOT EXISTS extracted_images
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     username TEXT,
                     image_url TEXT,
                     local_path TEXT,
                     caption TEXT,
                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
                     
        c.execute('''CREATE TABLE IF NOT EXISTS extracted_dms
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     from_user TEXT,
                     to_user TEXT,
                     message_text TEXT,
                     message_type TEXT,
                     media_url TEXT,
                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
                     
        conn.commit()
        conn.close()
    
    def init_real_browser(self):
        """Initialize real browser with stealth"""
        if not SELENIUM_AVAILABLE:
            print("❌ Selenium not available - using requests only")
            return False
            
        try:
            options = uc.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = uc.Chrome(options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Real browser initialized")
            return True
            
        except Exception as e:
            print(f"❌ Browser init failed: {e}")
            return False
    
    def extract_real_images(self, username):
        """Extract real images from Instagram profile"""
        print(f"📸 Starting real image extraction for @{username}")
        
        try:
            # Method 1: Try browser automation
            if self.init_real_browser():
                return self._extract_images_browser(username)
            
            # Method 2: Direct requests
            return self._extract_images_requests(username)
            
        except Exception as e:
            print(f"❌ Image extraction failed: {e}")
            return []
    
    def _extract_images_browser(self, username):
        """Extract images using real browser"""
        extracted_images = []
        
        try:
            # Navigate to Instagram profile
            url = f"https://www.instagram.com/{username}/"
            self.driver.get(url)
            
            # Wait for page load
            time.sleep(5)
            
            # Find image elements
            image_elements = self.driver.find_elements(By.CSS_SELECTOR, "img[src*='cdninstagram']")
            
            for i, img_element in enumerate(image_elements[:10]):  # Limit to 10 images
                try:
                    img_url = img_element.get_attribute('src')
                    alt_text = img_element.get_attribute('alt') or ""
                    
                    if img_url and 'cdninstagram' in img_url:
                        # Download real image
                        local_path = self._download_real_image(img_url, username, i)
                        if local_path:
                            extracted_images.append({
                                'url': img_url,
                                'path': local_path,
                                'caption': alt_text
                            })
                            
                            # Save to database
                            self._save_image_to_db(username, img_url, local_path, alt_text)
                            
                except Exception as e:
                    print(f"⚠️ Error processing image {i}: {e}")
                    
        except Exception as e:
            print(f"❌ Browser extraction failed: {e}")
            
        finally:
            if self.driver:
                self.driver.quit()
                
        return extracted_images
    
    def _extract_images_requests(self, username):
        """Extract images using requests"""
        extracted_images = []
        
        try:
            # Get profile page
            url = f"https://www.instagram.com/{username}/"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                # Look for image URLs in page source
                import re
                img_pattern = r'"display_url":"([^"]*cdninstagram[^"]*)"'
                matches = re.findall(img_pattern, response.text)
                
                for i, img_url in enumerate(matches[:5]):  # Limit to 5 images
                    # Clean URL
                    img_url = img_url.replace('\\u0026', '&')
                    
                    # Download image
                    local_path = self._download_real_image(img_url, username, i)
                    if local_path:
                        extracted_images.append({
                            'url': img_url,
                            'path': local_path,
                            'caption': f"Image {i+1} from @{username}"
                        })
                        
                        # Save to database
                        self._save_image_to_db(username, img_url, local_path, f"Image {i+1}")
                        
            else:
                print(f"⚠️ HTTP {response.status_code} for @{username}")
                
        except Exception as e:
            print(f"❌ Requests extraction failed: {e}")
            
        return extracted_images
    
    def _download_real_image(self, img_url, username, index):
        """Download real image file"""
        try:
            # Get image data
            response = self.session.get(img_url, timeout=30)
            
            if response.status_code == 200:
                # Create filename
                timestamp = int(time.time())
                filename = f"{username}_{index}_{timestamp}.jpg"
                filepath = os.path.join(self.images_folder, filename)
                
                # Save real image
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"✅ Downloaded: {filename}")
                return filepath
                
        except Exception as e:
            print(f"❌ Download failed: {e}")
            
        return None
    
    def extract_real_dms(self, username):
        """Extract real DMs (requires login)"""
        print(f"💬 Starting real DM extraction for @{username}")
        
        # Note: Real DM extraction requires authentication
        extracted_dms = []
        
        try:
            # Check for existing session cookies
            cookie_files = [
                'harvested_cookies_1748760474.json',
                'fresh_stealth_session.json',
                'alx_trading_active_session_20250601_061205.json'
            ]
            
            for cookie_file in cookie_files:
                if os.path.exists(cookie_file):
                    print(f"🍪 Found cookie file: {cookie_file}")
                    
                    # Load and use cookies
                    with open(cookie_file, 'r') as f:
                        cookie_data = json.load(f)
                        
                    # Apply cookies to session
                    if isinstance(cookie_data, list):
                        for cookie in cookie_data:
                            if 'name' in cookie and 'value' in cookie:
                                self.session.cookies.set(cookie['name'], cookie['value'])
                    
                    # Try to access DMs
                    dm_data = self._extract_dms_with_session(username)
                    if dm_data:
                        extracted_dms.extend(dm_data)
                        break
            
            if not extracted_dms:
                print("⚠️ No valid session found for DM extraction")
                print("💡 Need fresh login cookies for real DM access")
                
        except Exception as e:
            print(f"❌ DM extraction failed: {e}")
            
        return extracted_dms
    
    def _extract_dms_with_session(self, username):
        """Extract DMs using authenticated session"""
        try:
            # Try Instagram's internal API
            api_url = "https://www.instagram.com/api/v1/direct_v2/inbox/"
            response = self.session.get(api_url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Successfully accessed DM API")
                
                # Process DM data
                dms = []
                if 'inbox' in data and 'threads' in data['inbox']:
                    for thread in data['inbox']['threads'][:5]:  # Limit to 5 threads
                        for message in thread.get('items', [])[:10]:  # Limit to 10 messages per thread
                            dm_info = {
                                'from_user': message.get('user_id', 'unknown'),
                                'to_user': username,
                                'message_text': message.get('text', ''),
                                'message_type': message.get('item_type', 'text'),
                                'timestamp': message.get('timestamp', '')
                            }
                            dms.append(dm_info)
                            
                            # Save to database
                            self._save_dm_to_db(dm_info)
                
                return dms
                
            else:
                print(f"⚠️ DM API returned {response.status_code}")
                
        except Exception as e:
            print(f"❌ Session DM extraction failed: {e}")
            
        return []
    
    def _save_image_to_db(self, username, img_url, local_path, caption):
        """Save image info to database"""
        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()
        c.execute('''INSERT INTO extracted_images (username, image_url, local_path, caption)
                    VALUES (?, ?, ?, ?)''', (username, img_url, local_path, caption))
        conn.commit()
        conn.close()
    
    def _save_dm_to_db(self, dm_info):
        """Save DM to database"""
        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()
        c.execute('''INSERT INTO extracted_dms (from_user, to_user, message_text, message_type, media_url)
                    VALUES (?, ?, ?, ?, ?)''', 
                    (dm_info['from_user'], dm_info['to_user'], dm_info['message_text'], 
                     dm_info['message_type'], dm_info.get('media_url', '')))
        conn.commit()
        conn.close()
    
    def run_full_extraction(self, username):
        """Run complete extraction for target"""
        print(f"""
🔥💀 REAL EXTRACTION STARTING 💀🔥
================================
🎯 Target: @{username}
📸 Extracting images...
💬 Extracting DMs...
""")
        
        # Extract images
        images = self.extract_real_images(username)
        
        # Extract DMs
        dms = self.extract_real_dms(username)
        
        # Generate report
        self._generate_extraction_report(username, images, dms)
        
        return {
            'username': username,
            'images': images,
            'dms': dms,
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_extraction_report(self, username, images, dms):
        """Generate real extraction report"""
        report_file = f"extraction_report_{username}_{int(time.time())}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"""
🔥💀 REAL EXTRACTION REPORT 💀🔥
==============================
Target: @{username}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📸 IMAGES EXTRACTED: {len(images)}
{'-' * 40}
""")
            
            for i, img in enumerate(images, 1):
                f.write(f"{i}. {img['path']}\n")
                f.write(f"   Caption: {img['caption']}\n")
                f.write(f"   URL: {img['url'][:60]}...\n\n")
            
            f.write(f"""
💬 DMs EXTRACTED: {len(dms)}
{'-' * 40}
""")
            
            for i, dm in enumerate(dms, 1):
                f.write(f"{i}. From: {dm['from_user']}\n")
                f.write(f"   Message: {dm['message_text'][:100]}...\n")
                f.write(f"   Type: {dm['message_type']}\n\n")
            
            f.write(f"""
📊 SUMMARY
{'-' * 40}
Total Images: {len(images)}
Total DMs: {len(dms)}
Database: {self.database_path}
Images Folder: {self.images_folder}

🔥 EXTRACTION COMPLETE 🔥
""")
        
        print(f"📊 Report saved: {report_file}")

def main():
    extractor = RealImageDMExtractor()
    
    # Get target from user
    target = input("🎯 Enter Instagram username (without @): ").strip()
    
    if target:
        # Run real extraction
        result = extractor.run_full_extraction(target)
        
        print(f"""
🏁 EXTRACTION COMPLETE!
======================
📸 Images extracted: {len(result['images'])}
💬 DMs extracted: {len(result['dms'])}
📁 Check folders: {extractor.images_folder}/
📊 Database: {extractor.database_path}
""")
    else:
        print("❌ No username provided")

if __name__ == "__main__":
    main()
