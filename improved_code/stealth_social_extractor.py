from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
🔥 STEALTH SOCIAL EXTRACTOR 🔥
Advanced stealth methods for private social media profiles
"""

import asyncio
import json
import requests
import time
from datetime import datetime
from playwright.async_api import async_playwright

class StealthSocialExtractor:
    def __init__(self):
        self.mobile_proxy = 'http://brd-customer-hl_63f0835e-zone-mobile:fl13j3qcjvqh@brd.superproxy.io:33335'
        self.browser_auth = 'brd-customer-hl_63f0835e-zone-scraping_browser:59m84ggoef95'
        self.sbr_ws_cdp = f'wss://{self.browser_auth}@brd.superproxy.io:9222'
        
    async def method_1_public_api_scraping(self, username):
        """วิธีที่ 1: ใช้ Public API และ Web Scraping"""
        print("🔍 Method 1: Public API + Web Scraping...")
        
        # ลองดึงข้อมูลจาก public endpoints
        public_urls = [
            f"https://www.instagram.com/{username}/?__a=1",
            f"https://www.instagram.com/web/search/topsearch/?query={username}",
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
        ]
        
        for url in public_urls:
            try:
                response = requests.get(url, proxies={'http': self.mobile_proxy, 'https': self.mobile_proxy})
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Found data from: {url}")
                    return data
            except:
                continue
                
        return None

    async def method_2_browser_automation(self, target_url):
        """วิธีที่ 2: Browser Automation แบบ Stealth"""
        print("🎭 Method 2: Stealth Browser Automation...")
        
        async with async_playwright() as pw:
            browser = await pw.chromium.connect_over_cdp(self.sbr_ws_cdp)
            
            try:
                page = await browser.new_page()
                
                # ตั้งค่า stealth mode
                await page.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                    Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                    Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                """)
                
                # เข้าชม profile
                await page.goto(target_url)
                await page.wait_for_timeout(5000)
                
                # สกัดข้อมูลที่มองเห็นได้
                profile_data = await self.extract_visible_data(page)
                
                # ลองหา linked accounts
                linked_accounts = await self.find_linked_accounts(page)
                
                # บันทึกหน้าจอ
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                await page.screenshot(path=f"stealth_capture_{timestamp}.png", full_page=True)
                
                return {
                    'profile_data': profile_data,
                    'linked_accounts': linked_accounts,
                    'screenshot': f"stealth_capture_{timestamp}.png"
                }
                
            finally:
                await browser.close()

    async def method_3_social_engineering(self, username):
        """วิธีที่ 3: Social Engineering Techniques"""
        print("🕵️ Method 3: Social Engineering Analysis...")
        
        techniques = {
            'cross_platform_search': await self.search_cross_platforms(username),
            'reverse_image_search': await self.reverse_image_search(username),
            'username_variations': await self.check_username_variations(username),
            'mutual_connections': await self.find_mutual_connections(username)
        }
        
        return techniques

    async def search_cross_platforms(self, username):
        """ค้นหาบนแพลตฟอร์มอื่น"""
        platforms = [
            f"https://twitter.com/{username}",
            f"https://tiktok.com/@{username}",
            f"https://facebook.com/{username}",
            f"https://youtube.com/@{username}"
        ]
        
        found_platforms = []
        
        for platform in platforms:
            try:
                response = requests.get(platform, proxies={'http': self.mobile_proxy, 'https': self.mobile_proxy})
                if response.status_code == 200 and "not found" not in response.text.lower():
                    found_platforms.append(platform)
            except:
                continue
                
        return found_platforms

    async def reverse_image_search(self, username):
        """Reverse image search for profile pictures"""
        print("🔍 Performing reverse image search...")
        # Implementation for reverse image search
        return {"status": "analyzing", "results": []}

    async def check_username_variations(self, username):
        """ตรวจสอบ username variations"""
        variations = [
            f"{username}_",
            f"_{username}",
            f"{username}1",
            f"{username}official",
            f"real{username}"
        ]
        
        valid_variations = []
        
        for variation in variations:
            url = f"https://www.instagram.com/{variation}/"
            try:
                response = requests.get(url, proxies={'http': self.mobile_proxy, 'https': self.mobile_proxy})
                if response.status_code == 200:
                    valid_variations.append(variation)
            except:
                continue
                
        return valid_variations

    async def find_mutual_connections(self, username):
        """หา mutual connections"""
        print("🤝 Finding mutual connections...")
        # Implementation for finding mutual connections
        return {"status": "analyzing", "connections": []}

    async def extract_visible_data(self, page):
        """สกัดข้อมูลที่มองเห็นได้"""
        data = {}
        
        try:
            # Profile name
            name_element = await page.query_selector('h2')
            if name_element:
                data['name'] = await name_element.text_content()
            
            # Follower count (ถ้ามองเห็นได้)
            follower_elements = await page.query_selector_all('a[href*="followers"] span')
            if follower_elements:
                data['followers'] = await follower_elements[0].text_content()
            
            # Bio
            bio_element = await page.query_selector('div.-vDIg span')
            if bio_element:
                data['bio'] = await bio_element.text_content()
                
            # Profile picture
            img_element = await page.query_selector('img[data-testid="user-avatar"]')
            if img_element:
                data['profile_pic'] = await img_element.get_attribute('src')
                
        except Exception as e:
            print(f"Data extraction error: {e}")
            
        return data

    async def find_linked_accounts(self, page):
        """หา linked social accounts"""
        linked = []
        
        try:
            # ค้นหาลิงค์ในโปรไฟล์
            links = await page.query_selector_all('a[href*="http"]')
            for link in links:
                href = await link.get_attribute('href')
                if any(platform in href for platform in ['twitter.com', 'tiktok.com', 'youtube.com', 'facebook.com']):
                    linked.append(href)
                    
        except Exception as e:
            print(f"Linked accounts error: {e}")
            
        return linked

async def run_stealth_extraction():
    extractor = StealthSocialExtractor()
    username = "whatilove1728"
    target_url = f"https://www.instagram.com/{username}?igsh=Z2lua3Awcm1ldXJ6"
    
    print("🔥 STEALTH SOCIAL EXTRACTOR 🔥")
    print(f"Target: {username}")
    print("="*50)
    
    # รันทุกวิธี
    results = {}
    
    # Method 1: Public API
    print("\n1️⃣ Public API Scraping...")
    results['method_1'] = await extractor.method_1_public_api_scraping(username)
    
    # Method 2: Browser Automation
    print("\n2️⃣ Stealth Browser Automation...")
    results['method_2'] = await extractor.method_2_browser_automation(target_url)
    
    # Method 3: Social Engineering
    print("\n3️⃣ Social Engineering Analysis...")
    results['method_3'] = await extractor.method_3_social_engineering(username)
    
    # บันทึกผลลัพธ์
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"stealth_extraction_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Stealth extraction complete!")
    print(f"📁 Results saved to: {output_file}")
    
    return results

if __name__ == "__main__":
    asyncio.run(run_stealth_extraction())
