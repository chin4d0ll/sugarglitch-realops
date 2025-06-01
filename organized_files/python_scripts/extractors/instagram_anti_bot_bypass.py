#!/usr/bin/env python3
"""
Instagram Anti-Bot Bypass System
Advanced Instagram data extraction with professor-level bot detection evasion
"""

import os
import json
import time
import random
import requests
import threading
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import instaloader
from urllib.parse import quote
import base64

class InstagramAntiBotBypass:
    def __init__(self):
        self.ua = UserAgent()
        self.sessions_dir = "/workspaces/sugarglitch-realops/sessions"
        os.makedirs(self.sessions_dir, exist_ok=True)
        self.cookies_dir = "/workspaces/sugarglitch-realops/cookies"
        os.makedirs(self.cookies_dir, exist_ok=True)
        
        # Advanced stealth settings
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        ]
        
        # Realistic delay patterns
        self.delay_patterns = {
            'page_load': (3, 8),
            'click': (1, 3),
            'scroll': (2, 5),
            'typing': (0.1, 0.3),
            'between_requests': (5, 15)
        }
        
    def generate_random_delay(self, action_type='between_requests'):
        """Generate realistic human-like delays"""
        min_delay, max_delay = self.delay_patterns.get(action_type, (2, 6))
        return random.uniform(min_delay, max_delay)
    
    def get_random_user_agent(self):
        """Get random user agent for stealth"""
        return random.choice(self.user_agents)
    
    def create_stealth_session(self):
        """Create stealth requests session with anti-detection headers"""
        session = requests.Session()
        
        # Advanced headers to mimic real browser
        headers = {
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }
        session.headers.update(headers)
        return session
    
    def extract_browser_cookies(self, username, password):
        """Extract real browser cookies using undetected Chrome"""
        print(f"🚀 Starting browser cookie extraction for {username}...")
        
        try:
            # Setup undetected Chrome
            options = uc.ChromeOptions()
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-web-security")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            options.add_argument(f"--user-agent={self.get_random_user_agent()}")
            
            # Initialize driver
            driver = uc.Chrome(options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Navigate to Instagram
            print("📱 Navigating to Instagram...")
            driver.get("https://www.instagram.com/accounts/login/")
            
            # Wait for page load with realistic delay
            time.sleep(self.generate_random_delay('page_load'))
            
            # Wait for login form
            wait = WebDriverWait(driver, 20)
            
            # Find and fill username
            username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
            self._human_type(username_field, username)
            time.sleep(self.generate_random_delay('typing'))
            
            # Find and fill password
            password_field = driver.find_element(By.NAME, "password")
            self._human_type(password_field, password)
            time.sleep(self.generate_random_delay('click'))
            
            # Click login button
            login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Wait for login process
            print("🔐 Logging in...")
            time.sleep(self.generate_random_delay('page_load') + 5)
            
            # Handle 2FA if prompted
            try:
                two_fa_input = driver.find_element(By.NAME, "verificationCode")
                print("🔑 2FA detected. Please enter verification code manually in browser...")
                input("Press Enter after completing 2FA...")
            except:
                print("✅ No 2FA required")
            
            # Wait for dashboard
            wait.until(EC.url_contains("instagram.com"))
            time.sleep(3)
            
            # Extract all cookies
            cookies = driver.get_cookies()
            cookie_dict = {}
            
            for cookie in cookies:
                cookie_dict[cookie['name']] = cookie['value']
            
            # Save cookies
            timestamp = int(time.time())
            cookie_file = f"{self.cookies_dir}/{username}_cookies_{timestamp}.json"
            
            with open(cookie_file, 'w') as f:
                json.dump(cookie_dict, f, indent=2)
            
            print(f"🍪 Cookies extracted and saved to: {cookie_file}")
            print(f"📊 Extracted {len(cookie_dict)} cookies")
            
            # Create Instaloader session file
            if 'sessionid' in cookie_dict:
                self._create_instaloader_session(username, cookie_dict)
            
            driver.quit()
            return cookie_dict
            
        except Exception as e:
            print(f"❌ Cookie extraction failed: {e}")
            if 'driver' in locals():
                driver.quit()
            return None
    
    def _human_type(self, element, text):
        """Type like a human with random delays"""
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))
    
    def _create_instaloader_session(self, username, cookies):
        """Create Instaloader session file from browser cookies"""
        try:
            L = instaloader.Instaloader()
            
            # Create session using cookies
            if 'sessionid' in cookies:
                session_file = f"{self.sessions_dir}/{username}_instaloader_session"
                
                # Save session
                L.context._session.cookies.update(cookies)
                L.save_session_to_file(session_file)
                
                print(f"📁 Instaloader session saved: {session_file}")
                return session_file
                
        except Exception as e:
            print(f"⚠️ Failed to create Instaloader session: {e}")
            return None
    
    def load_cookies(self, username):
        """Load the latest cookies for a username"""
        try:
            # Find latest cookie file
            cookie_files = [f for f in os.listdir(self.cookies_dir) if f.startswith(f"{username}_cookies_")]
            if not cookie_files:
                print(f"❌ No cookies found for {username}")
                return None
            
            # Get latest file
            latest_file = max(cookie_files, key=lambda x: int(x.split('_')[-1].replace('.json', '')))
            cookie_path = f"{self.cookies_dir}/{latest_file}"
            
            with open(cookie_path, 'r') as f:
                cookies = json.load(f)
            
            print(f"🍪 Loaded cookies from: {latest_file}")
            return cookies
            
        except Exception as e:
            print(f"❌ Failed to load cookies: {e}")
            return None
    
    def extract_with_instaloader(self, username, target_accounts):
        """Extract data using Instaloader with stealth features"""
        print(f"🔍 Starting Instaloader extraction for {username}...")
        
        try:
            # Initialize Instaloader with stealth settings
            L = instaloader.Instaloader(
                download_pictures=True,
                download_videos=True,
                download_video_thumbnails=False,
                download_geotags=True,
                download_comments=True,
                save_metadata=True,
                compress_json=False,
                max_connection_attempts=3
            )
            
            # Load session
            session_files = [f for f in os.listdir(self.sessions_dir) if f.startswith(f"{username}_instaloader")]
            if session_files:
                latest_session = max(session_files, key=lambda x: os.path.getctime(f"{self.sessions_dir}/{x}"))
                session_path = f"{self.sessions_dir}/{latest_session}"
                L.load_session_from_file(username, session_path)
                print(f"📁 Loaded session: {latest_session}")
            else:
                print("⚠️ No session found, extraction may be limited")
            
            results = {}
            
            for target in target_accounts:
                print(f"\n📱 Extracting data from: {target}")
                
                try:
                    # Add realistic delay between accounts
                    time.sleep(self.generate_random_delay('between_requests'))
                    
                    # Get profile
                    profile = instaloader.Profile.from_username(L.context, target)
                    
                    # Extract profile data
                    profile_data = {
                        'username': profile.username,
                        'full_name': profile.full_name,
                        'biography': profile.biography,
                        'followers': profile.followers,
                        'followees': profile.followees,
                        'posts_count': profile.mediacount,
                        'is_verified': profile.is_verified,
                        'is_private': profile.is_private,
                        'external_url': profile.external_url,
                        'business_category': getattr(profile, 'business_category_name', None),
                        'extracted_at': datetime.now().isoformat()
                    }
                    
                    # Extract recent posts (with stealth delays)
                    posts = []
                    post_count = 0
                    max_posts = 10  # Limit to avoid rate limiting
                    
                    for post in profile.get_posts():
                        if post_count >= max_posts:
                            break
                        
                        # Add delay between posts
                        time.sleep(self.generate_random_delay('between_requests'))
                        
                        post_data = {
                            'shortcode': post.shortcode,
                            'caption': post.caption,
                            'likes': post.likes,
                            'comments': post.comments,
                            'date': post.date.isoformat(),
                            'is_video': post.is_video,
                            'url': f"https://www.instagram.com/p/{post.shortcode}/",
                            'hashtags': list(post.caption_hashtags) if post.caption else []
                        }
                        posts.append(post_data)
                        post_count += 1
                        
                        print(f"  📄 Extracted post {post_count}: {post.shortcode}")
                    
                    profile_data['recent_posts'] = posts
                    results[target] = profile_data
                    
                    print(f"✅ Successfully extracted {target}: {len(posts)} posts")
                    
                except Exception as e:
                    print(f"❌ Failed to extract {target}: {e}")
                    results[target] = {'error': str(e)}
            
            # Save results
            timestamp = int(time.time())
            results_file = f"/workspaces/sugarglitch-realops/results/instaloader_extraction_{timestamp}.json"
            os.makedirs(os.path.dirname(results_file), exist_ok=True)
            
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Results saved to: {results_file}")
            return results
            
        except Exception as e:
            print(f"❌ Instaloader extraction failed: {e}")
            return None
    
    def extract_with_requests(self, username, target_accounts):
        """Extract data using requests with anti-bot headers"""
        print(f"🌐 Starting requests-based extraction for {username}...")
        
        cookies = self.load_cookies(username)
        if not cookies:
            print("❌ No cookies available for requests extraction")
            return None
        
        session = self.create_stealth_session()
        
        # Add Instagram cookies
        for name, value in cookies.items():
            session.cookies.set(name, value, domain='.instagram.com')
        
        results = {}
        
        for target in target_accounts:
            print(f"\n🎯 Extracting {target} via requests...")
            
            try:
                # Add delay
                time.sleep(self.generate_random_delay('between_requests'))
                
                # Try different endpoints
                urls = [
                    f"https://www.instagram.com/{target}/?__a=1&__d=dis",
                    f"https://www.instagram.com/api/v1/users/web_profile_info/?username={target}",
                    f"https://www.instagram.com/{target}/"
                ]
                
                profile_data = None
                
                for url in urls:
                    try:
                        print(f"  🔗 Trying: {url}")
                        
                        # Rotate user agent
                        session.headers['User-Agent'] = self.get_random_user_agent()
                        
                        response = session.get(url, timeout=15)
                        
                        if response.status_code == 200:
                            if '{"user":' in response.text or '"data":{' in response.text:
                                # Parse JSON response
                                try:
                                    data = response.json()
                                    if 'graphql' in data and 'user' in data['graphql']:
                                        user_data = data['graphql']['user']
                                    elif 'data' in data and 'user' in data['data']:
                                        user_data = data['data']['user']
                                    else:
                                        continue
                                    
                                    profile_data = {
                                        'username': user_data.get('username'),
                                        'full_name': user_data.get('full_name'),
                                        'biography': user_data.get('biography'),
                                        'followers': user_data.get('edge_followed_by', {}).get('count', 0),
                                        'following': user_data.get('edge_follow', {}).get('count', 0),
                                        'posts_count': user_data.get('edge_owner_to_timeline_media', {}).get('count', 0),
                                        'is_verified': user_data.get('is_verified'),
                                        'is_private': user_data.get('is_private'),
                                        'external_url': user_data.get('external_url'),
                                        'extracted_at': datetime.now().isoformat(),
                                        'extraction_method': 'requests_api'
                                    }
                                    break
                                    
                                except json.JSONDecodeError:
                                    continue
                            
                        time.sleep(2)  # Delay between URL attempts
                        
                    except Exception as e:
                        print(f"    ❌ URL failed: {e}")
                        continue
                
                if profile_data:
                    results[target] = profile_data
                    print(f"✅ Successfully extracted {target}")
                else:
                    results[target] = {'error': 'No data extracted'}
                    print(f"❌ Failed to extract {target}")
                
            except Exception as e:
                print(f"❌ Failed to extract {target}: {e}")
                results[target] = {'error': str(e)}
        
        # Save results
        timestamp = int(time.time())
        results_file = f"/workspaces/sugarglitch-realops/results/requests_extraction_{timestamp}.json"
        os.makedirs(os.path.dirname(results_file), exist_ok=True)
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {results_file}")
        return results
    
    def run_comprehensive_extraction(self, username, password, target_accounts):
        """Run complete extraction process with all methods"""
        print("🔥 INSTAGRAM ANTI-BOT BYPASS SYSTEM ACTIVATED 🔥")
        print("=" * 60)
        
        # Step 1: Extract browser cookies
        print("\n1️⃣ EXTRACTING BROWSER COOKIES...")
        cookies = self.extract_browser_cookies(username, password)
        
        if not cookies:
            print("❌ Cookie extraction failed. Cannot proceed.")
            return None
        
        print(f"✅ Cookies extracted successfully!")
        
        # Step 2: Wait before starting extraction
        delay = self.generate_random_delay('page_load')
        print(f"\n⏱️ Waiting {delay:.1f} seconds before extraction...")
        time.sleep(delay)
        
        # Step 3: Try Instaloader method
        print("\n2️⃣ EXTRACTING WITH INSTALOADER...")
        instaloader_results = self.extract_with_instaloader(username, target_accounts)
        
        # Step 4: Try requests method
        print("\n3️⃣ EXTRACTING WITH REQUESTS...")
        requests_results = self.extract_with_requests(username, target_accounts)
        
        # Combine results
        final_results = {
            'extraction_timestamp': datetime.now().isoformat(),
            'username': username,
            'target_accounts': target_accounts,
            'instaloader_results': instaloader_results,
            'requests_results': requests_results,
            'success_rate': self._calculate_success_rate(instaloader_results, requests_results)
        }
        
        # Save final results
        timestamp = int(time.time())
        final_file = f"/workspaces/sugarglitch-realops/results/comprehensive_extraction_{timestamp}.json"
        
        with open(final_file, 'w') as f:
            json.dump(final_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n🎉 EXTRACTION COMPLETE!")
        print(f"📊 Final results saved to: {final_file}")
        
        return final_results
    
    def _calculate_success_rate(self, instaloader_results, requests_results):
        """Calculate success rate of extractions"""
        total_targets = 0
        successful_extractions = 0
        
        if instaloader_results:
            for target, data in instaloader_results.items():
                total_targets += 1
                if 'error' not in data:
                    successful_extractions += 1
        
        if requests_results:
            for target, data in requests_results.items():
                if instaloader_results and target in instaloader_results:
                    continue  # Don't double count
                total_targets += 1
                if 'error' not in data:
                    successful_extractions += 1
        
        return (successful_extractions / total_targets * 100) if total_targets > 0 else 0

def main():
    """Main execution function"""
    bypass = InstagramAntiBotBypass()
    
    # Configuration
    username = "alx.trading"
    password = "Fleming654"
    target_accounts = ["alx.trading", "whatilove1728"]
    
    print("🚀 Instagram Anti-Bot Bypass System")
    print("==================================")
    print(f"Username: {username}")
    print(f"Targets: {', '.join(target_accounts)}")
    print()
    
    # Run comprehensive extraction
    results = bypass.run_comprehensive_extraction(username, password, target_accounts)
    
    if results:
        print(f"\n✨ SUCCESS RATE: {results['success_rate']:.1f}%")
        
        # Print summary
        if results['instaloader_results']:
            print(f"\n📈 INSTALOADER SUMMARY:")
            for target, data in results['instaloader_results'].items():
                if 'error' not in data:
                    print(f"  ✅ {target}: {data.get('posts_count', 0)} posts, {data.get('followers', 0)} followers")
                else:
                    print(f"  ❌ {target}: {data['error']}")
        
        if results['requests_results']:
            print(f"\n🌐 REQUESTS SUMMARY:")
            for target, data in results['requests_results'].items():
                if 'error' not in data:
                    print(f"  ✅ {target}: {data.get('posts_count', 0)} posts, {data.get('followers', 0)} followers")
                else:
                    print(f"  ❌ {target}: {data['error']}")
    
    else:
        print("❌ Extraction failed completely")

if __name__ == "__main__":
    main()
