#!/usr/bin/env python3
"""
🔐 PRIVATE PROFILE EXTRACTOR WITH AUTH
Advanced extraction for private Instagram profiles
"""

import asyncio
from playwright.async_api import async_playwright
import json
import os
from datetime import datetime

class PrivateProfileExtractor:
    def __init__(self):
        self.auth = 'brd-customer-hl_63f0835e-zone-scraping_browser:59m84ggoef95'
        self.sbr_ws_cdp = f'wss://{self.auth}@brd.superproxy.io:9222'
        self.session_file = 'instagram_session.json'
        
    async def load_session(self):
        """Load saved Instagram session"""
        if os.path.exists(self.session_file):
            with open(self.session_file, 'r') as f:
                return json.load(f)
        return None
    
    async def extract_private_profile(self, profile_url):
        """
        🎯 Extract data from private profile (requires login)
        """
        session_data = await self.load_session()
        if not session_data:
            print("❌ No valid session found! Run instagram_auth_setup.py first")
            return None
            
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(self.sbr_ws_cdp)
            
            try:
                context = await browser.new_context()
                await context.add_cookies(session_data['cookies'])
                
                page = await context.new_page()
                
                print(f"🎯 Accessing private profile: {profile_url}")
                await page.goto(profile_url)
                await page.wait_for_load_state('networkidle')
                
                # Take screenshot first
                await page.screenshot(path='private_profile_view.png', full_page=True)
                
                # Extract profile data
                profile_data = {}
                
                try:
                    # Basic profile info
                    username = await page.locator('h2').first.inner_text()
                    profile_data['username'] = username
                    
                    # Follower count
                    followers = await page.locator('a[href*="/followers/"] span').inner_text()
                    profile_data['followers'] = followers
                    
                    # Following count  
                    following = await page.locator('a[href*="/following/"] span').inner_text()
                    profile_data['following'] = following
                    
                    # Posts count
                    posts = await page.locator('span').filter(has_text='posts').inner_text()
                    profile_data['posts'] = posts
                    
                    print(f"✅ Profile Data Extracted:")
                    print(f"   👤 Username: {username}")
                    print(f"   👥 Followers: {followers}")
                    print(f"   👥 Following: {following}")
                    print(f"   📸 Posts: {posts}")
                    
                except Exception as e:
                    print(f"⚠️  Profile data extraction error: {e}")
                
                # Extract post images
                images_data = []
                try:
                    # Wait for images to load
                    await page.wait_for_selector('img', timeout=5000)
                    
                    # Get all post images
                    images = await page.locator('article img').all()
                    
                    for i, img in enumerate(images[:12]):  # First 12 images
                        try:
                            src = await img.get_attribute('src')
                            if src and 'instagram' in src:
                                images_data.append({
                                    'index': i,
                                    'url': src,
                                    'alt': await img.get_attribute('alt') or ''
                                })
                                
                                # Download image
                                await self.download_image(page, src, f'private_image_{i}.jpg')
                                
                        except Exception as e:
                            print(f"⚠️  Image {i} extraction error: {e}")
                    
                    profile_data['images'] = images_data
                    print(f"📸 Extracted {len(images_data)} images")
                    
                except Exception as e:
                    print(f"⚠️  Images extraction error: {e}")
                
                # Save extracted data
                with open(f'private_profile_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w') as f:
                    json.dump(profile_data, f, indent=2)
                
                return profile_data
                
            finally:
                await browser.close()
    
    async def download_image(self, page, image_url, filename):
        """Download image from URL"""
        try:
            response = await page.request.get(image_url)
            if response.ok:
                with open(f'extracted_images/{filename}', 'wb') as f:
                    f.write(await response.body())
                print(f"💾 Downloaded: {filename}")
        except Exception as e:
            print(f"❌ Download failed for {filename}: {e}")

async def main():
    extractor = PrivateProfileExtractor()
    
    # Target profile
    profile_url = "https://www.instagram.com/whatilove1728/"
    
    print("🔐 PRIVATE PROFILE EXTRACTION")
    print("=" * 50)
    
    # Extract data
    data = await extractor.extract_private_profile(profile_url)
    
    if data:
        print("\n🎉 Extraction Complete!")
        print(f"📁 Data saved to JSON file")
        print(f"📸 Images saved to extracted_images/")
    else:
        print("\n❌ Extraction failed!")
        print("💡 Make sure to run instagram_auth_setup.py first")

if __name__ == "__main__":
    # Ensure images directory exists
    os.makedirs('extracted_images', exist_ok=True)
    asyncio.run(main())
