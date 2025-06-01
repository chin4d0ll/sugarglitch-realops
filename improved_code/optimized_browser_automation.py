from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
🔥 OPTIMIZED BRIGHT DATA BROWSER AUTOMATION 🔥
Simplified but powerful Playwright integration
"""

import asyncio
import json
from datetime import datetime
from playwright.async_api import async_playwright

AUTH = 'brd-customer-hl_63f0835e-zone-scraping_browser:59m84ggoef95'
SBR_WS_CDP = f'wss://{AUTH}@brd.superproxy.io:9222'

class OptimizedBrowserBot:
    def __init__(self):
        self.browser = None
        self.page = None
        
    async def connect(self):
        """Connect to Bright Data browser"""
        print('🔥 Connecting to Bright Data Scraping Browser...')
        async with async_playwright() as playwright:
            self.browser = await playwright.chromium.connect_over_cdp(SBR_WS_CDP)
            self.page = await self.browser.new_page()
            print('✅ Connected and ready!')
            return True
    
    async def smart_screenshot(self, url, filename=None):
        """Take intelligent screenshots"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"capture_{timestamp}.png"
        
        print(f'📸 Capturing: {url}')
        await self.page.goto(url, wait_until='load')
        
        # More info at https://playwright.dev/python/docs/screenshots
        await self.page.screenshot(path=filename, full_page=True)
        
        print(f'✅ Saved: {filename}')
        return filename
    
    async def extract_intelligence(self, url):
        """Extract deep page intelligence"""
        print(f'🕵️ Analyzing: {url}')
        await self.page.goto(url, wait_until='load')
        
        # Get page title and basic info
        title = await self.page.title()
        content = await self.page.content()
        
        # Extract all text content
        text_content = await self.page.evaluate('() => document.body.innerText')
        
        # Get all links with analytics
        links = await self.page.evaluate('''
            () => {
                const links = Array.from(document.querySelectorAll('a[href]'));
                return links.map(link => ({
                    text: link.textContent.trim(),
                    href: link.href,
                    target: link.target,
                    rel: link.rel
                })).filter(link => link.text.length > 0);
            }
        ''')
        
        # Get all forms with detailed info
        forms = await self.page.evaluate('''
            () => {
                const forms = Array.from(document.querySelectorAll('form'));
                return forms.map(form => ({
                    action: form.action,
                    method: form.method,
                    inputs: Array.from(form.querySelectorAll('input, textarea, select')).map(input => ({
                        name: input.name,
                        type: input.type,
                        placeholder: input.placeholder,
                        required: input.required,
                        value: input.value
                    }))
                }));
            }
        ''')
        
        # Get meta information
        meta_data = await self.page.evaluate('''
            () => {
                const metas = Array.from(document.querySelectorAll('meta'));
                const result = {};
                metas.forEach(meta => {
                    if (meta.name) result[meta.name] = meta.content;
                    if (meta.property) result[meta.property] = meta.content;
                });
                return result;
            }
        ''')
        
        intelligence = {
            'url': url,
            'title': title,
            'content_length': len(content),
            'text_length': len(text_content),
            'links_count': len(links),
            'forms_count': len(forms),
            'links': links[:20],  # Top 20 links
            'forms': forms,
            'meta_data': meta_data,
            'timestamp': datetime.now().isoformat()
        }
        
        return intelligence
    
    async def multi_target_raid(self, urls):
        """Execute operations on multiple targets"""
        results = []
        
        async with async_playwright() as playwright:
            self.browser = await playwright.chromium.connect_over_cdp(SBR_WS_CDP)
            self.page = await self.browser.new_page()
            
            for i, url in enumerate(urls):
                print(f'\n🎯 TARGET {i+1}/{len(urls)}: {url}')
                
                try:
                    # Take screenshot
                    screenshot = await self.smart_screenshot(url)
                    
                    # Extract intelligence
                    intel = await self.extract_intelligence(url)
                    
                    result = {
                        'target': url,
                        'screenshot': screenshot,
                        'intelligence': intel,
                        'status': 'SUCCESS'
                    }
                    
                    results.append(result)
                    print(f'✅ Target {i+1} completed')
                    
                    # Pause between targets
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    print(f'❌ Target {i+1} failed: {e}')
                    results.append({
                        'target': url,
                        'error': str(e),
                        'status': 'FAILED'
                    })
            
            await self.browser.close()
        
        return results
    
    async def save_mission_report(self, data, filename=None):
        """Save mission results"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"mission_report_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f'📊 Mission report saved: {filename}')
        return filename

async def execute_deep_mission():
    """Execute deep browser mission"""
    bot = OptimizedBrowserBot()
    
    # Target list
    targets = [
        'https://www.example.com',
        'https://httpbin.org/headers',
        'https://geo.brdtest.com/mygeo.json',
        'https://httpbin.org/user-agent'
    ]
    
    print('🔥 STARTING DEEP BROWSER MISSION...')
    print(f'🎯 Targets: {len(targets)}')
    
    # Execute raid
    results = await bot.multi_target_raid(targets)
    
    # Save report
    report_file = await bot.save_mission_report(results)
    
    # Summary
    successful = len([r for r in results if r['status'] == 'SUCCESS'])
    failed = len([r for r in results if r['status'] == 'FAILED'])
    
    print('\n🎉 MISSION COMPLETE!')
    print(f'✅ Successful: {successful}')
    print(f'❌ Failed: {failed}')
    print(f'📊 Report: {report_file}')

async def quick_test():
    """Quick single-page test"""
    print('🔥 QUICK BROWSER TEST...')
    
    async with async_playwright() as playwright:
        browser = await playwright.chromium.connect_over_cdp(SBR_WS_CDP)
        page = await browser.new_page()
        
        # Test with example.com
        await page.goto('https://www.example.com')
        
        # More info at https://playwright.dev/python/docs/screenshots
        await page.screenshot(path='test_capture.png', full_page=True)
        
        title = await page.title()
        print(f'✅ Captured: {title}')
        print('📸 Screenshot: test_capture.png')
        
        await browser.close()

if __name__ == '__main__':
    print('🔥 OPTIMIZED BRIGHT DATA BROWSER AUTOMATION 🔥')
    print('Select operation:')
    print('1. Quick Test')
    print('2. Deep Mission')
    
    choice = input('Choice (1/2): ').strip()
    
    if choice == '1':
        asyncio.run(quick_test())
    else:
        asyncio.run(execute_deep_mission())
