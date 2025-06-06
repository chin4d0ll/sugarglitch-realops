#!/usr/bin/env python3
"""
🎭 REAL DM EXTRACTOR - Using Playwright with Manual Session
Extract real Instagram DMs using Playwright automation
"""

import asyncio
import json
import time
from datetime import datetime
from playwright.async_api import async_playwright
import os

class PlaywrightDMExtractor:
    def __init__(self):
        self.target = "alx.trading"
        self.output_dir = "/workspaces/sugarglitch-realops/data/playwright_extraction"
        self.session_file = "/workspaces/sugarglitch-realops/tools/session_alx_trading.json"
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        print("🎭 REAL DM EXTRACTOR - Using Playwright")
        print("=" * 60)
        print(f"Target: {self.target}")
        
    async def setup_browser(self):
        """Setup browser with session cookies"""
        playwright = await async_playwright().start()
        
        # Launch browser
        browser = await playwright.chromium.launch(
            headless=True,  # Run headless in codespace
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        
        # Load cookies if available
        try:
            with open(self.session_file, 'r') as f:
                cookies = json.load(f)
            
            # Add cookies to context
            await context.add_cookies(cookies)
            print(f"✅ Loaded {len(cookies)} cookies")
        except Exception as e:
            print(f"⚠️ Could not load cookies: {e}")
        
        page = await context.new_page()
        return playwright, browser, context, page
    
    async def login_and_navigate(self, page):
        """Navigate to Instagram and check login status"""
        print("\n🔐 Navigating to Instagram...")
        
        try:
            await page.goto('https://www.instagram.com/', timeout=30000)
            await page.wait_for_load_state('networkidle', timeout=10000)
            
            # Check if we're logged in
            current_url = page.url
            print(f"Current URL: {current_url}")
            
            # Look for login indicators
            if 'login' in current_url:
                print("❌ Not logged in - on login page")
                return False
            
            # Try to find user-specific elements
            try:
                # Wait for the main navigation or user menu
                await page.wait_for_selector('[data-testid="app-nav-bar"]', timeout=5000)
                print("✅ Appears to be logged in")
                return True
            except:
                print("⚠️ Cannot determine login status")
                return True  # Continue anyway
                
        except Exception as e:
            print(f"❌ Error navigating to Instagram: {e}")
            return False
    
    async def navigate_to_dms(self, page):
        """Navigate to direct messages"""
        print("\n💬 Navigating to DMs...")
        
        try:
            # Go directly to DM URL
            await page.goto('https://www.instagram.com/direct/inbox/', timeout=30000)
            await page.wait_for_load_state('networkidle', timeout=10000)
            
            print("✅ Navigated to DM inbox")
            return True
            
        except Exception as e:
            print(f"❌ Error navigating to DMs: {e}")
            return False
    
    async def search_for_target(self, page):
        """Search for target user in DMs"""
        print(f"\n🔍 Searching for {self.target}...")
        
        try:
            # Look for search box or new message button
            search_selectors = [
                '[placeholder*="Search"]',
                '[aria-label*="Search"]',
                'input[type="text"]'
            ]
            
            search_box = None
            for selector in search_selectors:
                try:
                    search_box = await page.wait_for_selector(selector, timeout=3000)
                    if search_box:
                        print(f"✅ Found search box: {selector}")
                        break
                except:
                    continue
            
            if search_box:
                await search_box.fill(self.target)
                await search_box.press('Enter')
                await page.wait_for_timeout(3000)
                
                # Look for the target in results
                await page.click(f'text="{self.target}"', timeout=5000)
                print(f"✅ Found and clicked on {self.target}")
                return True
            else:
                print("❌ Could not find search functionality")
                return False
                
        except Exception as e:
            print(f"❌ Error searching for target: {e}")
            return False
    
    async def extract_messages(self, page):
        """Extract messages from the conversation"""
        print(f"\n📥 Extracting messages...")
        
        try:
            # Wait for messages to load
            await page.wait_for_timeout(3000)
            
            # Try to scroll up to load more messages
            for i in range(3):
                await page.keyboard.press('PageUp')
                await page.wait_for_timeout(1000)
            
            # Look for message containers
            message_selectors = [
                '[data-testid="message"]',
                '.message',
                '[role="listitem"]',
                'div[style*="padding"]'
            ]
            
            messages = []
            for selector in message_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    if elements:
                        print(f"✅ Found {len(elements)} potential message elements with {selector}")
                        
                        for i, element in enumerate(elements[:20]):  # Limit to first 20
                            try:
                                text = await element.inner_text()
                                if text and len(text.strip()) > 0:
                                    messages.append({
                                        'index': i,
                                        'text': text.strip(),
                                        'selector': selector,
                                        'timestamp': datetime.now().isoformat()
                                    })
                            except:
                                continue
                        
                        if messages:
                            break
                except:
                    continue
            
            if not messages:
                # Try to get any visible text
                print("⚠️ No structured messages found, trying to extract visible text...")
                try:
                    page_text = await page.inner_text('body')
                    if self.target.lower() in page_text.lower():
                        messages.append({
                            'index': 0,
                            'text': f"Page contains reference to {self.target}",
                            'raw_content': page_text[:500],  # First 500 chars
                            'timestamp': datetime.now().isoformat()
                        })
                except:
                    pass
            
            return messages
            
        except Exception as e:
            print(f"❌ Error extracting messages: {e}")
            return []
    
    async def save_screenshot(self, page, filename):
        """Save screenshot for debugging"""
        try:
            screenshot_path = f"{self.output_dir}/{filename}"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Screenshot saved: {screenshot_path}")
        except Exception as e:
            print(f"❌ Error saving screenshot: {e}")
    
    def save_results(self, messages, metadata=None):
        """Save extraction results"""
        timestamp = int(time.time())
        output_file = f"{self.output_dir}/playwright_dm_extraction_{timestamp}.json"
        
        results = {
            'target': self.target,
            'extraction_timestamp': datetime.now().isoformat(),
            'method': 'playwright_automation',
            'total_messages': len(messages),
            'messages': messages,
            'metadata': metadata or {}
        }
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Results saved to: {output_file}")
            print(f"📊 Total messages extracted: {len(messages)}")
            
        except Exception as e:
            print(f"❌ Error saving results: {e}")
    
    async def run(self):
        """Main extraction process"""
        print("\n🚀 Starting Playwright DM extraction...")
        
        playwright, browser, context, page = await self.setup_browser()
        
        try:
            # Navigate and login
            if not await self.login_and_navigate(page):
                print("❌ Could not access Instagram")
                return
            
            # Take initial screenshot
            await self.save_screenshot(page, "01_login_status.png")
            
            # Navigate to DMs
            if not await self.navigate_to_dms(page):
                print("❌ Could not access DM inbox")
                return
            
            # Take DM inbox screenshot
            await self.save_screenshot(page, "02_dm_inbox.png")
            
            # Search for target (optional - may already be in inbox)
            await self.search_for_target(page)
            
            # Take conversation screenshot
            await self.save_screenshot(page, "03_conversation.png")
            
            # Extract messages
            messages = await self.extract_messages(page)
            
            # Save results
            self.save_results(messages, {
                'browser_user_agent': await page.evaluate('navigator.userAgent'),
                'final_url': page.url
            })
            
            print("\n✅ Playwright extraction completed!")
            
        except Exception as e:
            print(f"❌ Extraction failed: {e}")
        finally:
            await browser.close()
            await playwright.stop()

if __name__ == "__main__":
    extractor = PlaywrightDMExtractor()
    asyncio.run(extractor.run())
