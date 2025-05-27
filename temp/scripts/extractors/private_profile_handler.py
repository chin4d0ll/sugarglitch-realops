#!/usr/bin/env python3
"""
🔥 PRIVATE PROFILE HANDLER 🔥
Advanced system for handling private Instagram profiles
"""

import asyncio
import json
import time
from datetime import datetime
from playwright.async_api import async_playwright
import requests
import os

class PrivateProfileHandler:
    def __init__(self):
        self.auth = 'brd-customer-hl_63f0835e-zone-scraping_browser:59m84ggoef95'
        self.sbr_ws_cdp = f'wss://{self.auth}@brd.superproxy.io:9222'
        self.session_file = 'instagram_session.json'
        self.results = {
            'profile_data': {},
            'images': [],
            'followers_visible': [],
            'status': 'analyzing'
        }

    async def create_authenticated_session(self, username, password):
        """สร้าง session ที่ login แล้ว"""
        async with async_playwright() as pw:
            print("🔐 Creating authenticated session...")
            browser = await pw.chromium.connect_over_cdp(self.sbr_ws_cdp)
            
            try:
                page = await browser.new_page()
                
                # ไปที่หน้า login
                await page.goto('https://www.instagram.com/accounts/login/')
                await page.wait_for_timeout(3000)
                
                # กรอก username และ password
                await page.fill('input[name="username"]', username)
                await page.fill('input[name="password"]', password)
                
                # คลิก login
                await page.click('button[type="submit"]')
                await page.wait_for_timeout(5000)
                
                # ตรวจสอบว่า login สำเร็จ
                if await page.is_visible('text=Save Your Login Info?'):
                    await page.click('text=Not Now')
                    await page.wait_for_timeout(2000)
                
                if await page.is_visible('text=Turn on Notifications'):
                    await page.click('text=Not Now')
                    await page.wait_for_timeout(2000)
                
                # บันทึก cookies
                cookies = await page.context.cookies()
                session_data = {
                    'cookies': cookies,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'authenticated'
                }
                
                with open(self.session_file, 'w') as f:
                    json.dump(session_data, f, indent=2)
                
                print("✅ Authentication session saved!")
                return True
                
            except Exception as e:
                print(f"❌ Authentication failed: {e}")
                return False
            finally:
                await browser.close()

    async def load_session(self):
        """โหลด session ที่บันทึกไว้"""
        if not os.path.exists(self.session_file):
            return False
            
        try:
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            return session_data
        except:
            return False

    async def extract_private_profile(self, target_url):
        """สกัดข้อมูลจาก private profile"""
        session_data = await self.load_session()
        
        if not session_data:
            print("❌ No authenticated session found!")
            print("💡 Use create_session() first with your credentials")
            return False
            
        async with async_playwright() as pw:
            print("🔍 Extracting private profile data...")
            browser = await pw.chromium.connect_over_cdp(self.sbr_ws_cdp)
            
            try:
                context = await browser.new_context()
                
                # โหลด cookies
                await context.add_cookies(session_data['cookies'])
                
                page = await context.new_page()
                
                # ไปที่โปรไฟล์ target
                await page.goto(target_url)
                await page.wait_for_timeout(5000)
                
                # ตรวจสอบว่าเข้าถึงได้
                if await page.is_visible('text=This Account is Private'):
                    print("🔒 Profile is private - checking follow status...")
                    
                    # ตรวจสอบว่า follow แล้วหรือยัง
                    if await page.is_visible('text=Follow'):
                        print("❌ Need to follow this account first")
                        return self.results
                
                # สกัดข้อมูลโปรไฟล์
                await self.extract_profile_info(page)
                await self.extract_visible_content(page)
                
                # บันทึกผลลัพธ์
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"private_extraction_{timestamp}.json"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(self.results, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Private profile data extracted to {output_file}")
                return self.results
                
            except Exception as e:
                print(f"❌ Extraction error: {e}")
                return False
            finally:
                await browser.close()

    async def extract_profile_info(self, page):
        """สกัดข้อมูลพื้นฐานของโปรไฟล์"""
        try:
            # Profile name
            name_element = await page.query_selector('h2')
            if name_element:
                self.results['profile_data']['name'] = await name_element.text_content()
            
            # Bio
            bio_element = await page.query_selector('div.-vDIg span')
            if bio_element:
                self.results['profile_data']['bio'] = await bio_element.text_content()
            
            # Stats (posts, followers, following)
            stats = await page.query_selector_all('span.g47SY')
            if stats:
                stats_text = []
                for stat in stats:
                    text = await stat.text_content()
                    stats_text.append(text)
                self.results['profile_data']['stats'] = stats_text
            
            # Profile picture
            profile_pic = await page.query_selector('img[data-testid="user-avatar"]')
            if profile_pic:
                src = await profile_pic.get_attribute('src')
                self.results['profile_data']['profile_picture'] = src
                
        except Exception as e:
            print(f"Profile info extraction error: {e}")

    async def extract_visible_content(self, page):
        """สกัดเนื้อหาที่มองเห็นได้"""
        try:
            # รอให้โหลดเสร็จ
            await page.wait_for_timeout(3000)
            
            # สกัดรูปภาพ
            images = await page.query_selector_all('img')
            for img in images:
                src = await img.get_attribute('src')
                if src and 'instagram' in src and 'profile' not in src:
                    self.results['images'].append(src)
            
            # สกัดข้อมูล followers ที่มองเห็นได้
            followers_section = await page.query_selector('a[href*="/followers/"]')
            if followers_section:
                await followers_section.click()
                await page.wait_for_timeout(3000)
                
                # สกัดรายชื่อ followers ที่มองเห็นได้
                follower_elements = await page.query_selector_all('div[role="dialog"] a')
                for element in follower_elements[:50]:  # จำกัดที่ 50 คน
                    username = await element.get_attribute('href')
                    if username and '//' not in username:
                        self.results['followers_visible'].append(username.replace('/', ''))
                
                # ปิด dialog
                close_btn = await page.query_selector('button[aria-label="Close"]')
                if close_btn:
                    await close_btn.click()
                    
        except Exception as e:
            print(f"Content extraction error: {e}")

    async def try_alternative_methods(self, target_url):
        """ลองวิธีอื่นๆ สำหรับ private profiles"""
        print("🔄 Trying alternative extraction methods...")
        
        # Method 1: ดูผ่าน stories highlights
        await self.check_story_highlights(target_url)
        
        # Method 2: ตรวจสอบ tagged photos
        await self.check_tagged_photos(target_url)
        
        # Method 3: ค้นหาผ่าน hashtags ที่เกี่ยวข้อง
        await self.search_related_hashtags(target_url)

    async def check_story_highlights(self, target_url):
        """ตรวจสอบ story highlights"""
        print("📖 Checking story highlights...")
        # Implementation for story highlights

    async def check_tagged_photos(self, target_url):
        """ตรวจสอบรูปที่ถูก tag"""
        print("🏷️ Checking tagged photos...")
        # Implementation for tagged photos

    async def search_related_hashtags(self, target_url):
        """ค้นหาผ่าน hashtags ที่เกี่ยวข้อง"""
        print("🔍 Searching related hashtags...")
        # Implementation for hashtag search

async def main():
    handler = PrivateProfileHandler()
    
    print("🔥 PRIVATE PROFILE HANDLER 🔥")
    print("1. Create authenticated session")
    print("2. Extract private profile")
    print("3. Try alternative methods")
    
    choice = input("Select option (1-3): ")
    
    if choice == "1":
        username = input("Instagram username: ")
        password = input("Instagram password: ")
        await handler.create_authenticated_session(username, password)
    
    elif choice == "2":
        target_url = "https://www.instagram.com/whatilove1728?igsh=Z2lua3Awcm1ldXJ6"
        await handler.extract_private_profile(target_url)
    
    elif choice == "3":
        target_url = "https://www.instagram.com/whatilove1728?igsh=Z2lua3Awcm1ldXJ6"
        await handler.try_alternative_methods(target_url)

if __name__ == "__main__":
    asyncio.run(main())
