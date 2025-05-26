from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
🔥 ADVANCED INSTAGRAM EXTRACTION SYSTEM 🔥
Deep extraction of posts, images, followers, and content
Using Bright Data Scraping Browser for stealth operations
"""

import asyncio
import json
import os
import time
from datetime import datetime
from playwright.async_api import async_playwright
import aiohttp
import urllib.parse

class InstagramAdvancedExtractor:
    def __init__(self):
        self.auth = 'brd-customer-hl_63f0835e-zone-scraping_browser:59m84ggoef95'
        self.ws_endpoint = f'wss://{self.auth}@brd.superproxy.io:9222'
        self.session_data = {}
        self.extracted_data = {
            'profile_info': {},
            'posts': [],
            'images': [],
            'followers': [],
            'following': [],
            'stories': [],
            'timestamp': datetime.now().isoformat()
        }
        
    async def setup_browser(self, playwright):
        """Initialize stealth browser with mobile simulation"""
        print("🔥 Connecting to Bright Data Scraping Browser...")
        browser = await playwright.chromium.connect_over_cdp(self.ws_endpoint)
        
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            viewport={'width': 375, 'height': 812},
            device_scale_factor=3,
            is_mobile=True,
            has_touch=True
        )
        
        page = await context.new_page()
        
        # Enhanced stealth settings
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            window.chrome = {runtime: {}};
        """)
        
        return browser, context, page
    
    async def extract_profile_data(self, page, username):
        """Extract comprehensive profile information"""
        print(f"🎯 Extracting profile data for: {username}")
        
        try:
            # Navigate to profile
            profile_url = f"https://www.instagram.com/{username}/"
            await page.goto(profile_url, wait_until='networkidle')
            await asyncio.sleep(3)
            
            # Take screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"instagram_profile_{username}_{timestamp}.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Profile screenshot saved: {screenshot_path}")
            
            # Extract profile information
            profile_data = await page.evaluate("""
                () => {
                    const data = {};
                    
                    // Basic profile info
                    const profilePic = document.querySelector('img[data-testid="user-avatar"]');
                    data.profile_picture = profilePic ? profilePic.src : null;
                    
                    const username = document.querySelector('h2');
                    data.username = username ? username.textContent : null;
                    
                    const bio = document.querySelector('div[data-testid="user-bio"]');
                    data.bio = bio ? bio.textContent : null;
                    
                    // Stats
                    const stats = document.querySelectorAll('a[role="link"] span');
                    if (stats.length >= 3) {
                        data.posts_count = stats[0].textContent;
                        data.followers_count = stats[1].textContent;
                        data.following_count = stats[2].textContent;
                    }
                    
                    // Links
                    const links = [];
                    document.querySelectorAll('a[target="_blank"]').forEach(link => {
                        links.push(link.href);
                    });
                    data.external_links = links;
                    
                    return data;
                }
            """)
            
            self.extracted_data['profile_info'] = profile_data
            print(f"✅ Profile data extracted: {json.dumps(profile_data, indent=2)}")
            
        except Exception as e:
            print(f"❌ Profile extraction error: {e}")
    
    async def extract_posts_and_images(self, page, username, max_posts=50):
        """Extract posts and download images"""
        print(f"🖼️ Extracting posts and images (max: {max_posts})")
        
        try:
            # Scroll to load more posts
            print("📜 Scrolling to load posts...")
            for i in range(10):
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(2)
            
            # Extract post data
            posts_data = await page.evaluate(f"""
                () => {{
                    const posts = [];
                    const articles = document.querySelectorAll('article');
                    
                    articles.forEach((article, index) => {{
                        if (index >= {max_posts}) return;
                        
                        const post = {{}};
                        
                        // Images
                        const images = [];
                        article.querySelectorAll('img').forEach(img => {{
                            if (img.src && !img.src.includes('profile')) {{
                                images.push(img.src);
                            }}
                        }});
                        post.images = images;
                        
                        // Caption
                        const caption = article.querySelector('div[data-testid="post-caption"]');
                        post.caption = caption ? caption.textContent : '';
                        
                        // Likes
                        const likes = article.querySelector('span[aria-label*="like"]');
                        post.likes = likes ? likes.textContent : '0';
                        
                        // Date
                        const timeElement = article.querySelector('time');
                        post.date = timeElement ? timeElement.getAttribute('datetime') : null;
                        
                        // Post URL
                        const link = article.querySelector('a[href*="/p/"]');
                        post.url = link ? 'https://www.instagram.com' + link.getAttribute('href') : null;
                        
                        posts.push(post);
                    }});
                    
                    return posts;
                }}
            """)
            
            self.extracted_data['posts'] = posts_data
            
            # Download images
            if not os.path.exists('extracted_images'):
                os.makedirs('extracted_images')
            
            print(f"💾 Downloading {len(posts_data)} posts with images...")
            
            for i, post in enumerate(posts_data):
                for j, image_url in enumerate(post.get('images', [])):
                    try:
                        # Download image
                        response = await page.goto(image_url)
                        if response:
                            image_data = await response.body()
                            filename = f"extracted_images/{username}_post_{i+1}_img_{j+1}.jpg"
                            with open(filename, 'wb') as f:
                                f.write(image_data)
                            print(f"📥 Downloaded: {filename}")
                    except Exception as e:
                        print(f"❌ Image download error: {e}")
            
            print(f"✅ Extracted {len(posts_data)} posts")
            
        except Exception as e:
            print(f"❌ Posts extraction error: {e}")
    
    async def extract_followers_data(self, page, username):
        """Extract followers and following data"""
        print(f"👥 Extracting followers data...")
        
        try:
            # Click followers link
            followers_link = await page.query_selector('a[href*="/followers/"]')
            if followers_link:
                await followers_link.click()
                await asyncio.sleep(3)
                
                # Extract followers
                followers_data = await page.evaluate("""
                    () => {
                        const followers = [];
                        const userElements = document.querySelectorAll('div[role="dialog"] a');
                        
                        userElements.forEach(user => {
                            const username = user.getAttribute('href');
                            const img = user.querySelector('img');
                            const profilePic = img ? img.src : null;
                            
                            if (username && username.includes('/')) {
                                followers.push({
                                    username: username.replace('/', ''),
                                    profile_picture: profilePic
                                });
                            }
                        });
                        
                        return followers.slice(0, 100); // Limit to 100
                    }
                """)
                
                self.extracted_data['followers'] = followers_data
                print(f"✅ Extracted {len(followers_data)} followers")
                
                # Close dialog
                close_btn = await page.query_selector('button[aria-label="Close"]')
                if close_btn:
                    await close_btn.click()
                    await asyncio.sleep(1)
            
        except Exception as e:
            print(f"❌ Followers extraction error: {e}")
    
    async def save_results(self, username):
        """Save all extracted data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"instagram_extraction_{username}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.extracted_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {filename}")
        
        # Summary
        print("\n🎯 EXTRACTION SUMMARY:")
        print(f"Profile: {self.extracted_data['profile_info'].get('username', 'N/A')}")
        print(f"Posts: {len(self.extracted_data['posts'])}")
        print(f"Images downloaded: {sum(len(post.get('images', [])) for post in self.extracted_data['posts'])}")
        print(f"Followers: {len(self.extracted_data['followers'])}")
        
        return filename
    
    async def run_extraction(self, target_url):
        """Main extraction function"""
        print("🚀 STARTING INSTAGRAM ADVANCED EXTRACTION")
        print(f"🎯 Target: {target_url}")
        
        # Extract username from URL
        if 'instagram.com/' in target_url:
            username = target_url.split('instagram.com/')[1].split('?')[0].strip('/')
        else:
            username = target_url
        
        async with async_playwright() as playwright:
            browser, context, page = await self.setup_browser(playwright)
            
            try:
                # Extract profile data
                await self.extract_profile_data(page, username)
                
                # Extract posts and images
                await self.extract_posts_and_images(page, username)
                
                # Extract followers (if possible)
                await self.extract_followers_data(page, username)
                
                # Save results
                result_file = await self.save_results(username)
                
                print("🔥 EXTRACTION COMPLETE!")
                return result_file
                
            finally:
                await browser.close()

async @safe_execution
def main():
    extractor = InstagramAdvancedExtractor()
    
    # Target profile
    target = "https://www.instagram.com/whatilove1728?igsh=Z2lua3Awcm1ldXJ6"
    
    try:
        result_file = await extractor.run_extraction(target)
        print(f"\n✅ Complete extraction saved to: {result_file}")
    except Exception as e:
        print(f"❌ Extraction failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
