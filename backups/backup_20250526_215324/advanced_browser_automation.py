#!/usr/bin/env python3
"""
🔥 ADVANCED BROWSER AUTOMATION WITH BRIGHT DATA 🔥
Playwright + Bright Data Scraping Browser Integration
"""

import asyncio
import os
import json
from datetime import datetime
from playwright.async_api import async_playwright

# Bright Data Scraping Browser credentials
AUTH = 'brd-customer-hl_63f0835e-zone-scraping_browser:59m84ggoef95'
SBR_WS_CDP = f'wss://{AUTH}@brd.superproxy.io:9222'

class AdvancedBrowserAutomation:
    def __init__(self):
        self.browser = None
        self.page = None
        self.session_data = {}
        
    async def connect_browser(self):
        """Connect to Bright Data Scraping Browser"""
        print('🔥 Connecting to Bright Data Browser API...')
        async with async_playwright() as playwright:
            try:
                self.browser = await playwright.chromium.connect_over_cdp(SBR_WS_CDP)
                print('✅ Connected to Scraping Browser!')
                return True
            except Exception as e:
                print(f'❌ Connection failed: {e}')
                return False
    
    async def create_stealth_page(self):
        """Create a new page with stealth configurations"""
        if not self.browser:
            return None
            
        self.page = await self.browser.new_page()
        
        # Set stealth headers
        await self.page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # Set viewport
        await self.page.set_viewport_size({"width": 1920, "height": 1080})
        
        print('✅ Stealth page created!')
        return self.page
    
    async def advanced_screenshot(self, url, filename=None):
        """Take advanced screenshot with full page capture"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            
        try:
            print(f'🎯 Navigating to: {url}')
            await self.page.goto(url, wait_until='networkidle')
            
            # More info at https://playwright.dev/python/docs/screenshots
            await self.page.screenshot(path=filename, full_page=True)
            
            print(f'📸 Screenshot saved as: {filename}')
            return filename
        except Exception as e:
            print(f'❌ Screenshot failed: {e}')
            return None
    
    async def extract_page_data(self, url):
        """Extract comprehensive page data"""
        try:
            await self.page.goto(url, wait_until='networkidle')
            
            # Extract page content
            html = await self.page.content()
            title = await self.page.title()
            
            # Extract all links
            links = await self.page.evaluate("""
                () => {
                    return Array.from(document.querySelectorAll('a')).map(a => ({
                        href: a.href,
                        text: a.textContent.trim()
                    }));
                }
            """)
            
            # Extract all images
            images = await self.page.evaluate("""
                () => {
                    return Array.from(document.querySelectorAll('img')).map(img => ({
                        src: img.src,
                        alt: img.alt
                    }));
                }
            """)
            
            # Extract forms
            forms = await self.page.evaluate("""
                () => {
                    return Array.from(document.querySelectorAll('form')).map(form => ({
                        action: form.action,
                        method: form.method,
                        inputs: Array.from(form.querySelectorAll('input')).map(input => ({
                            name: input.name,
                            type: input.type,
                            value: input.value
                        }))
                    }));
                }
            """)
            
            data = {
                'url': url,
                'title': title,
                'html_length': len(html),
                'links_count': len(links),
                'images_count': len(images),
                'forms_count': len(forms),
                'links': links[:10],  # First 10 links
                'images': images[:10],  # First 10 images
                'forms': forms,
                'timestamp': datetime.now().isoformat()
            }
            
            return data
            
        except Exception as e:
            print(f'❌ Data extraction failed: {e}')
            return None
    
    async def multi_target_operation(self, urls):
        """Execute operations on multiple targets"""
        results = []
        
        for i, url in enumerate(urls):
            print(f'\n🎯 Target {i+1}/{len(urls)}: {url}')
            
            try:
                # Take screenshot
                screenshot_file = await self.advanced_screenshot(url)
                
                # Extract data
                page_data = await self.extract_page_data(url)
                
                result = {
                    'url': url,
                    'screenshot': screenshot_file,
                    'data': page_data,
                    'status': 'success'
                }
                
                results.append(result)
                
                # Random delay between requests
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f'❌ Operation failed for {url}: {e}')
                results.append({
                    'url': url,
                    'error': str(e),
                    'status': 'failed'
                })
        
        return results
    
    async def save_session_data(self, data, filename=None):
        """Save session data to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"session_data_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            print(f'💾 Session data saved to: {filename}')
            return filename
        except Exception as e:
            print(f'❌ Failed to save session data: {e}')
            return None
    
    async def close(self):
        """Clean up browser connection"""
        if self.browser:
            await self.browser.close()
            print('🔥 Browser connection closed')

async def run_advanced_automation():
    """Main execution function"""
    automation = AdvancedBrowserAutomation()
    
    try:
        # Connect to browser
        async with async_playwright() as playwright:
            automation.browser = await playwright.chromium.connect_over_cdp(SBR_WS_CDP)
            print('✅ Connected to Bright Data Scraping Browser!')
            
            # Create stealth page
            await automation.create_stealth_page()
            
            # Test targets
            test_urls = [
                'https://www.example.com',
                'https://httpbin.org/ip',
                'https://geo.brdtest.com/mygeo.json'
            ]
            
            print('\n🔥 STARTING MULTI-TARGET OPERATION...')
            results = await automation.multi_target_operation(test_urls)
            
            # Save results
            session_file = await automation.save_session_data(results)
            
            print('\n🎉 OPERATION COMPLETE!')
            print(f'📊 Processed {len(test_urls)} targets')
            print(f'💾 Results saved to: {session_file}')
            
    except Exception as e:
        print(f'❌ Critical error: {e}')
    finally:
        await automation.close()

async def quick_screenshot_test():
    """Quick test function for single screenshot"""
    print('🔥 QUICK SCREENSHOT TEST...')
    
    async with async_playwright() as playwright:
        try:
            browser = await playwright.chromium.connect_over_cdp(SBR_WS_CDP)
            page = await browser.new_page()
            
            print('Connected! Navigating to webpage')
            await page.goto('https://www.example.com')
            
            # More info at https://playwright.dev/python/docs/screenshots
            await page.screenshot(path='screenshot.png', full_page=True)
            
            print("✅ Screenshot saved as 'screenshot.png'")
            
            html = await page.content()
            print(f"📄 Page HTML length: {len(html)} characters")
            
        except Exception as e:
            print(f'❌ Error: {e}')
        finally:
            if 'browser' in locals():
                await browser.close()

if __name__ == '__main__':
    print('🔥 ADVANCED BROWSER AUTOMATION SYSTEM 🔥')
    print('Choose operation:')
    print('1. Quick Screenshot Test')
    print('2. Full Advanced Automation')
    
    choice = input('Enter choice (1 or 2): ').strip()
    
    if choice == '1':
        asyncio.run(quick_screenshot_test())
    else:
        asyncio.run(run_advanced_automation())
