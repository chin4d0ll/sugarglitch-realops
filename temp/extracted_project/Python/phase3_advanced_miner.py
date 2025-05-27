#!/usr/bin/env python3
"""
🔥 PHASE 3: ADVANCED INSTAGRAM DATA MINER
Deep extraction and behavioral analysis system
Target: alx.trading | Password: Fleming654
Phase 3: Advanced Data Mining & Network Analysis
"""

import json
import time
import random
import sys
import os
from datetime import datetime, timedelta
import requests
import re
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import sqlite3
from urllib.parse import urlparse, parse_qs
import hashlib
import pickle

def safe_print(*args, **kwargs):
    try:
        print(*args, **kwargs)
        sys.stdout.flush()
    except (BrokenPipeError, IOError):
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(1)

class AdvancedInstagramMiner:
    def __init__(self, username="alx.trading", password="Fleming654"):
        self.username = username
        self.password = password
        self.driver = None
        self.database_file = f"instagram_deep_data_{username}.db"
        self.session_cookies = None
        
        # Deep mining data structure
        self.deep_data = {
            "profile_complete": {},
            "posts_detailed": [],
            "stories_data": [],
            "direct_messages": [],
            "comments_data": [],
            "likes_history": [],
            "followers_detailed": [],
            "following_detailed": [],
            "activity_history": [],
            "search_history": [],
            "tagged_posts": [],
            "saved_posts": [],
            "network_analysis": {},
            "behavioral_patterns": {},
            "metadata_analysis": {}
        }
        
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def setup_advanced_browser(self):
        """Setup ultra-stealth browser for deep mining"""
        try:
            safe_print("🔧 Setting up advanced stealth browser for Phase 3...")
            
            # Use regular Chrome with fixed config
            from selenium.webdriver.chrome.options import Options
            options = Options()
            
            # Fixed browser configuration
            import tempfile
            user_data_dir = tempfile.mkdtemp()
            options.add_argument(f'--user-data-dir={user_data_dir}')
            
            # Fixed stealth options
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-automation')
            options.add_argument('--disable-extensions')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-features=VizDisplayCompositor')
            options.add_argument('--headless')
            
            # Anti-detection
            options.add_experimental_option('useAutomationExtension', False)
            prefs = {
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_settings.popups": 0,
                "profile.managed_default_content_settings.images": 2
            }
            options.add_experimental_option("prefs", prefs)
            
            options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            options.add_argument('--window-size=1920,1080')
            
            self.driver = webdriver.Chrome(options=options)
            
            # Execute stealth scripts
            stealth_script = """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            window.chrome = { runtime: {} };
            """
            self.driver.execute_script(stealth_script)
            
            safe_print("✅ Advanced stealth browser ready for deep mining")
            return True
            
        except Exception as e:
            safe_print(f"❌ Advanced browser setup failed: {e}")
            return False
    
    def establish_session(self):
        """Establish authenticated session"""
        try:
            safe_print("🔐 Establishing deep mining session...")
            
            # Load existing cookies if available
            cookies_file = f"instagram_cookies_{self.username}.json"
            if os.path.exists(cookies_file):
                try:
                    with open(cookies_file, 'r') as f:
                        session_data = json.load(f)
                    
                    # Check if session is fresh (less than 12 hours)
                    session_time = datetime.fromisoformat(session_data["timestamp"])
                    if datetime.now() - session_time < timedelta(hours=12):
                        safe_print("🍪 Loading existing session...")
                        
                        self.driver.get("https://www.instagram.com/")
                        time.sleep(2)
                        
                        for cookie in session_data["cookies"]:
                            try:
                                self.driver.add_cookie(cookie)
                            except:
                                continue
                        
                        self.driver.refresh()
                        time.sleep(3)
                        
                        if "login" not in self.driver.current_url:
                            safe_print("✅ Session restored successfully")
                            self.session_cookies = session_data["cookies"]
                            return True
                except:
                    pass
            
            # Fresh login if no valid session
            safe_print("🔑 Creating fresh authenticated session...")
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(random.uniform(3, 5))
            
            # Enhanced login process
            username_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = self.driver.find_element(By.NAME, "password")
            
            # Human-like typing
            self.human_type(username_field, self.username)
            time.sleep(random.uniform(1, 2))
            self.human_type(password_field, self.password)
            time.sleep(random.uniform(1, 2))
            
            # Submit login
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            time.sleep(random.uniform(5, 8))
            
            if "login" not in self.driver.current_url:
                safe_print("✅ Fresh session established")
                self.save_session_cookies()
                return True
            else:
                safe_print("❌ Session establishment failed")
                return False
                
        except Exception as e:
            safe_print(f"❌ Session establishment error: {e}")
            return False
    
    def human_type(self, element, text, delay_range=(0.05, 0.15)):
        """Human-like typing with natural variations"""
        for char in text:
            element.send_keys(char)
            # Add occasional pauses and corrections
            if random.random() < 0.1:  # 10% chance of brief pause
                time.sleep(random.uniform(0.2, 0.5))
            time.sleep(random.uniform(*delay_range))
    
    def save_session_cookies(self):
        """Save session cookies for reuse"""
        try:
            cookies = self.driver.get_cookies()
            session_data = {
                "cookies": cookies,
                "timestamp": datetime.now().isoformat(),
                "user_agent": self.driver.execute_script("return navigator.userAgent;"),
                "username": self.username
            }
            
            with open(f"instagram_cookies_{self.username}.json", 'w') as f:
                json.dump(session_data, f, indent=2)
            
            self.session_cookies = cookies
            safe_print("💾 Session cookies saved")
            
        except Exception as e:
            safe_print(f"⚠️ Cookie save failed: {e}")
    
    def initialize_database(self):
        """Initialize SQLite database for deep data storage"""
        try:
            safe_print("🗄️ Initializing deep data database...")
            
            conn = sqlite3.connect(self.database_file)
            cursor = conn.cursor()
            
            # Create tables for different data types
            tables = {
                "profile_data": """
                    CREATE TABLE IF NOT EXISTS profile_data (
                        id INTEGER PRIMARY KEY,
                        username TEXT,
                        full_name TEXT,
                        biography TEXT,
                        external_url TEXT,
                        follower_count INTEGER,
                        following_count INTEGER,
                        post_count INTEGER,
                        is_verified BOOLEAN,
                        is_private BOOLEAN,
                        is_business BOOLEAN,
                        profile_pic_url TEXT,
                        extracted_at TEXT
                    )
                """,
                "posts": """
                    CREATE TABLE IF NOT EXISTS posts (
                        id INTEGER PRIMARY KEY,
                        post_id TEXT UNIQUE,
                        shortcode TEXT,
                        caption TEXT,
                        likes_count INTEGER,
                        comments_count INTEGER,
                        timestamp TEXT,
                        media_urls TEXT,
                        hashtags TEXT,
                        mentions TEXT,
                        location TEXT,
                        extracted_at TEXT
                    )
                """,
                "followers": """
                    CREATE TABLE IF NOT EXISTS followers (
                        id INTEGER PRIMARY KEY,
                        username TEXT,
                        full_name TEXT,
                        profile_pic_url TEXT,
                        is_verified BOOLEAN,
                        follower_count INTEGER,
                        following_count INTEGER,
                        extracted_at TEXT
                    )
                """,
                "following": """
                    CREATE TABLE IF NOT EXISTS following (
                        id INTEGER PRIMARY KEY,
                        username TEXT,
                        full_name TEXT,
                        profile_pic_url TEXT,
                        is_verified BOOLEAN,
                        follower_count INTEGER,
                        following_count INTEGER,
                        extracted_at TEXT
                    )
                """,
                "stories": """
                    CREATE TABLE IF NOT EXISTS stories (
                        id INTEGER PRIMARY KEY,
                        story_id TEXT,
                        media_url TEXT,
                        timestamp TEXT,
                        views_count INTEGER,
                        extracted_at TEXT
                    )
                """,
                "direct_messages": """
                    CREATE TABLE IF NOT EXISTS direct_messages (
                        id INTEGER PRIMARY KEY,
                        thread_id TEXT,
                        participant TEXT,
                        message_text TEXT,
                        timestamp TEXT,
                        message_type TEXT,
                        extracted_at TEXT
                    )
                """,
                "comments": """
                    CREATE TABLE IF NOT EXISTS comments (
                        id INTEGER PRIMARY KEY,
                        post_id TEXT,
                        comment_id TEXT,
                        username TEXT,
                        comment_text TEXT,
                        likes_count INTEGER,
                        timestamp TEXT,
                        extracted_at TEXT
                    )
                """,
                "activity_log": """
                    CREATE TABLE IF NOT EXISTS activity_log (
                        id INTEGER PRIMARY KEY,
                        activity_type TEXT,
                        target_user TEXT,
                        target_post TEXT,
                        timestamp TEXT,
                        extracted_at TEXT
                    )
                """
            }
            
            for table_name, table_sql in tables.items():
                cursor.execute(table_sql)
            
            conn.commit()
            conn.close()
            
            safe_print("✅ Deep data database initialized")
            return True
            
        except Exception as e:
            safe_print(f"❌ Database initialization failed: {e}")
            return False
    
    def extract_complete_profile(self):
        """Extract complete profile information with all details"""
        try:
            safe_print("👤 Extracting complete profile data...")
            
            self.driver.get(f"https://www.instagram.com/{self.username}/")
            time.sleep(random.uniform(3, 5))
            
            profile_data = {
                "username": self.username,
                "extracted_at": datetime.now().isoformat()
            }
            
            # Extract all visible profile information
            try:
                # Basic info
                profile_data["display_name"] = self.driver.find_element(By.XPATH, "//h2").text
                profile_data["bio"] = self.driver.find_element(By.XPATH, "//div[contains(@class, '_a9-z')]//span").text
                
                # Profile picture
                img_element = self.driver.find_element(By.XPATH, "//img[contains(@alt, 'profile picture')]")
                profile_data["profile_pic_url"] = img_element.get_attribute("src")
                
                # Stats
                stat_elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'followers') or contains(@href, 'following')]/span")
                if len(stat_elements) >= 2:
                    profile_data["followers_count"] = self.parse_count(stat_elements[0].text)
                    profile_data["following_count"] = self.parse_count(stat_elements[1].text)
                
                # Posts count
                posts_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'posts')]/preceding-sibling::span")
                profile_data["posts_count"] = self.parse_count(posts_element.text)
                
                # Verification status
                profile_data["is_verified"] = len(self.driver.find_elements(By.XPATH, "//span[contains(@title, 'Verified')]")) > 0
                
                # Business account check
                profile_data["is_business"] = len(self.driver.find_elements(By.XPATH, "//span[contains(text(), 'Business')]")) > 0
                
                # External URL
                try:
                    external_link = self.driver.find_element(By.XPATH, "//a[contains(@class, '_a9--')]")
                    profile_data["external_url"] = external_link.get_attribute("href")
                except:
                    profile_data["external_url"] = None
                
                # Account type
                try:
                    if self.driver.find_elements(By.XPATH, "//*[contains(text(), 'This account is private')]"):
                        profile_data["is_private"] = True
                    else:
                        profile_data["is_private"] = False
                except:
                    profile_data["is_private"] = False
                
            except Exception as e:
                safe_print(f"⚠️ Profile extraction warning: {e}")
            
            # Save to database
            self.save_to_database("profile_data", profile_data)
            self.deep_data["profile_complete"] = profile_data
            
            safe_print(f"✅ Complete profile extracted: {len(profile_data)} fields")
            return profile_data
            
        except Exception as e:
            safe_print(f"❌ Complete profile extraction failed: {e}")
            return {}
    
    def parse_count(self, count_text):
        """Parse Instagram count text (e.g., '1.2K' -> 1200)"""
        try:
            count_text = count_text.replace(',', '').lower()
            if 'k' in count_text:
                return int(float(count_text.replace('k', '')) * 1000)
            elif 'm' in count_text:
                return int(float(count_text.replace('m', '')) * 1000000)
            else:
                return int(count_text)
        except:
            return 0
    
    def extract_deep_posts_data(self, limit=100):
        """Extract detailed posts data with engagement metrics"""
        try:
            safe_print(f"📸 Extracting deep posts data (limit: {limit})...")
            
            self.driver.get(f"https://www.instagram.com/{self.username}/")
            time.sleep(random.uniform(3, 5))
            
            posts_data = []
            processed_posts = set()
            
            # Find all post links
            post_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
            
            for i, post_link in enumerate(post_links[:limit]):
                try:
                    post_url = post_link.get_attribute("href")
                    post_id = post_url.split("/p/")[1].split("/")[0]
                    
                    if post_id in processed_posts:
                        continue
                    
                    processed_posts.add(post_id)
                    
                    # Navigate to post
                    self.driver.execute_script("window.open('');")
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    self.driver.get(post_url)
                    time.sleep(random.uniform(2, 4))
                    
                    post_data = {
                        "post_id": post_id,
                        "shortcode": post_id,
                        "post_url": post_url,
                        "extracted_at": datetime.now().isoformat()
                    }
                    
                    # Extract post details
                    try:
                        # Caption
                        caption_elements = self.driver.find_elements(By.XPATH, "//span[contains(@class, '_aacl _aaco _aacu _aacx _aad7 _aade')]")
                        if caption_elements:
                            post_data["caption"] = caption_elements[0].text
                        
                        # Likes count
                        likes_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'likes') or contains(text(), 'like')]")
                        if likes_elements:
                            likes_text = likes_elements[0].text
                            post_data["likes_count"] = self.parse_count(likes_text.split()[0])
                        
                        # Comments count
                        comments_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'comments') or contains(text(), 'comment')]")
                        if comments_elements:
                            comments_text = comments_elements[0].text
                            post_data["comments_count"] = self.parse_count(comments_text.split()[0])
                        
                        # Media URLs
                        img_elements = self.driver.find_elements(By.XPATH, "//img[contains(@class, '_aagv')]")
                        media_urls = []
                        for img in img_elements:
                            src = img.get_attribute("src")
                            if src and "instagram" in src:
                                media_urls.append(src)
                        post_data["media_urls"] = json.dumps(media_urls)
                        
                        # Hashtags and mentions
                        if "caption" in post_data:
                            hashtags = re.findall(r'#\w+', post_data["caption"])
                            mentions = re.findall(r'@\w+', post_data["caption"])
                            post_data["hashtags"] = json.dumps(hashtags)
                            post_data["mentions"] = json.dumps(mentions)
                        
                        # Timestamp
                        time_elements = self.driver.find_elements(By.XPATH, "//time")
                        if time_elements:
                            post_data["timestamp"] = time_elements[0].get_attribute("datetime")
                        
                        # Location
                        location_elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/locations/')]")
                        if location_elements:
                            post_data["location"] = location_elements[0].text
                        
                    except Exception as e:
                        safe_print(f"⚠️ Post detail extraction warning: {e}")
                    
                    posts_data.append(post_data)
                    
                    # Save to database
                    self.save_to_database("posts", post_data)
                    
                    # Close tab and return to main window
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    
                    if i % 10 == 0:
                        safe_print(f"📸 Processed {i+1}/{min(len(post_links), limit)} posts")
                    
                    # Random delay
                    time.sleep(random.uniform(1, 3))
                    
                except Exception as e:
                    safe_print(f"⚠️ Post {i} processing error: {e}")
                    # Ensure we're back to main window
                    if len(self.driver.window_handles) > 1:
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])
                    continue
            
            self.deep_data["posts_detailed"] = posts_data
            safe_print(f"✅ Deep posts data extracted: {len(posts_data)} posts")
            return posts_data
            
        except Exception as e:
            safe_print(f"❌ Deep posts extraction failed: {e}")
            return []
    
    def save_to_database(self, table, data):
        """Save data to SQLite database"""
        try:
            conn = sqlite3.connect(self.database_file)
            cursor = conn.cursor()
            
            # Prepare insert statement
            columns = list(data.keys())
            placeholders = ', '.join(['?' for _ in columns])
            values = [data[col] for col in columns]
            
            insert_sql = f"INSERT OR REPLACE INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
            cursor.execute(insert_sql, values)
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            safe_print(f"⚠️ Database save error for {table}: {e}")
    
    def run_phase3_mining(self):
        """Execute Phase 3 deep mining operation"""
        safe_print("🔥 STARTING PHASE 3: ADVANCED DATA MINING")
        safe_print("=" * 60)
        safe_print(f"🎯 Target: {self.username}")
        safe_print(f"🔑 Phase: Advanced Deep Mining")
        safe_print(f"⏰ Timestamp: {self.timestamp}")
        safe_print("=" * 60)
        
        try:
            # Setup infrastructure
            if not self.setup_advanced_browser():
                return False
            
            if not self.initialize_database():
                return False
            
            if not self.establish_session():
                return False
            
            # Execute deep mining phases
            safe_print("\n🔍 PHASE 3.1: Complete Profile Analysis")
            self.extract_complete_profile()
            
            safe_print("\n🔍 PHASE 3.2: Deep Posts Mining")
            self.extract_deep_posts_data(limit=50)  # Start with 50 posts
            
            # Save progress
            self.save_phase3_results()
            
            safe_print("\n🎉 PHASE 3 DEEP MINING COMPLETE!")
            safe_print("=" * 60)
            
            return True
            
        except Exception as e:
            safe_print(f"❌ Phase 3 mining failed: {e}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()
    
    def save_phase3_results(self):
        """Save Phase 3 results to files"""
        try:
            # Save JSON data
            filename = f"phase3_deep_mining_{self.username}_{self.timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.deep_data, f, indent=2, ensure_ascii=False)
            
            # Create summary report
            summary_filename = f"phase3_summary_{self.username}_{self.timestamp}.md"
            with open(summary_filename, 'w', encoding='utf-8') as f:
                f.write(f"# 🔥 PHASE 3 DEEP MINING REPORT\n")
                f.write(f"**Target**: {self.username}\n")
                f.write(f"**Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Database**: {self.database_file}\n\n")
                
                f.write("## 📊 EXTRACTION SUMMARY\n")
                f.write(f"- **Profile Data**: {len(self.deep_data.get('profile_complete', {}))} fields\n")
                f.write(f"- **Posts Analyzed**: {len(self.deep_data.get('posts_detailed', []))} posts\n")
                f.write(f"- **Database Records**: Multiple tables populated\n\n")
                
                f.write("## 🎯 NEXT PHASE CAPABILITIES\n")
                f.write("- Network mapping and relationship analysis\n")
                f.write("- Behavioral pattern recognition\n")
                f.write("- Advanced content analysis\n")
                f.write("- Predictive modeling\n\n")
            
            safe_print(f"💾 Phase 3 data saved: {filename}")
            safe_print(f"📄 Summary saved: {summary_filename}")
            
        except Exception as e:
            safe_print(f"❌ Phase 3 save failed: {e}")

def main():
    """Execute Phase 3 advanced mining"""
    miner = AdvancedInstagramMiner()
    success = miner.run_phase3_mining()
    
    if success:
        safe_print("✅ Phase 3 advanced mining completed successfully!")
    else:
        safe_print("❌ Phase 3 advanced mining failed!")

if __name__ == "__main__":
    main()
