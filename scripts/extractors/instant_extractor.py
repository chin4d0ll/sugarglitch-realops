#!/usr/bin/env python3
"""
⚡ INSTANT DATA EXTRACTOR ⚡
Direct extraction for whatilove1728
All methods simultaneously!
"""

import asyncio
import aiohttp
import requests
import json
import time
import random
import concurrent.futures
from datetime import datetime
from playwright.async_api import async_playwright
import threading

class InstantExtractor:
    def __init__(self):
        self.target = "whatilove1728"
        self.target_url = "https://www.instagram.com/whatilove1728"
        self.bright_data_auth = 'brd-customer-hl_63f0835e-zone-scraping_browser:59m84ggoef95'
        self.mobile_proxy = 'http://brd-customer-hl_63f0835e-zone-mobile:fl13j3qcjvqh@brd.superproxy.io:33335'
        
        self.extracted_data = {
            'target': self.target,
            'timestamp': datetime.now().isoformat(),
            'extraction_results': {},
            'images_found': [],
            'profile_data': {},
            'success_methods': []
        }
        
        self.api_endpoints = [
            f"https://www.instagram.com/{self.target}/?__a=1&__d=dis",
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={self.target}",
            f"https://www.instagram.com/web/search/topsearch/?query={self.target}",
            f"https://graph.instagram.com/{self.target}?fields=id,username,media_count",
            f"https://www.instagram.com/api/v1/users/{self.target}/info/",
            f"https://www.instagram.com/{self.target}/channel/?__a=1"
        ]
        
        self.headers_pool = [
            {
                'User-Agent': 'Instagram 301.0.0.27.111 (iPhone13,2; iOS 17_0; en_US)',
                'X-IG-App-ID': '936619743392459',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9'
            },
            {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5'
            },
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json, text/plain, */*',
                'X-Requested-With': 'XMLHttpRequest'
            }
        ]
    
    def rapid_api_assault(self):
        """⚡ RAPID API ASSAULT"""
        print("⚡ LAUNCHING RAPID API ASSAULT...")
        
        def test_api(endpoint, headers):
            try:
                response = requests.get(
                    endpoint, 
                    headers=headers, 
                    timeout=8,
                    proxies={'http': self.mobile_proxy, 'https': self.mobile_proxy}
                )
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if data and (self.target in str(data) or 'user' in str(data).lower()):
                            timestamp = int(time.time())
                            filename = f"api_extract_{timestamp}_{random.randint(1000,9999)}.json"
                            
                            with open(filename, 'w') as f:
                                json.dump(data, f, indent=2)
                            
                            print(f"   💎 API SUCCESS: {len(str(data))} chars -> {filename}")
                            return {'success': True, 'file': filename, 'data': data, 'endpoint': endpoint}
                    except:
                        pass
                        
                return {'success': False, 'status': response.status_code, 'endpoint': endpoint}
            except Exception as e:
                return {'success': False, 'error': str(e), 'endpoint': endpoint}
        
        # Parallel API testing
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            futures = []
            for endpoint in self.api_endpoints:
                for headers in self.headers_pool:
                    futures.append(executor.submit(test_api, endpoint, headers))
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result['success']:
                    results.append(result)
                    self.extracted_data['success_methods'].append('API_ASSAULT')
        
        self.extracted_data['extraction_results']['api_assault'] = results
        print(f"   📊 API Results: {len(results)} successful extractions")
        return len(results) > 0
    
    async def stealth_browser_extraction(self):
        """🕵️ STEALTH BROWSER EXTRACTION"""
        print("🕵️ LAUNCHING STEALTH BROWSER...")
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.connect_over_cdp(f'wss://{self.bright_data_auth}@brd.superproxy.io:9222')
                
                # Multiple stealth approaches
                extraction_methods = [
                    self.extract_via_direct_access,
                    self.extract_via_embed_trick,
                    self.extract_via_stories_endpoint,
                    self.extract_via_hashtag_search
                ]
                
                results = []
                for i, method in enumerate(extraction_methods):
                    try:
                        page = await browser.new_page()
                        
                        # Anti-detection measures
                        await page.add_init_script("""
                            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
                            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                        """)
                        
                        result = await method(page, i+1)
                        if result['success']:
                            results.append(result)
                            
                        await page.close()
                        await asyncio.sleep(random.uniform(1, 3))
                        
                    except Exception as e:
                        print(f"   ❌ Browser method {i+1} failed: {str(e)}")
                
                await browser.close()
                self.extracted_data['extraction_results']['stealth_browser'] = results
                
                if results:
                    self.extracted_data['success_methods'].append('STEALTH_BROWSER')
                    print(f"   📊 Browser Results: {len(results)} successful extractions")
                    return True
                    
        except Exception as e:
            print(f"   ❌ Browser connection failed: {str(e)}")
        
        return False
    
    async def extract_via_direct_access(self, page, method_num):
        """Direct profile access"""
        try:
            await page.goto(self.target_url, timeout=15000)
            await page.wait_for_timeout(random.randint(2000, 5000))
            
            # Extract any visible data
            data = await page.evaluate("""
                () => {
                    const result = {};
                    
                    // Try to find profile data
                    const scripts = Array.from(document.querySelectorAll('script'));
                    scripts.forEach(script => {
                        if (script.textContent && script.textContent.includes('ProfilePage')) {
                            try {
                                const match = script.textContent.match(/"ProfilePage":\\[.*?\\]/);
                                if (match) result.profile_data = match[0];
                            } catch(e) {}
                        }
                    });
                    
                    // Extract meta data
                    const title = document.title;
                    const metaDesc = document.querySelector('meta[name="description"]');
                    if (metaDesc) result.description = metaDesc.content;
                    result.title = title;
                    
                    // Look for image URLs
                    const images = Array.from(document.querySelectorAll('img')).map(img => img.src);
                    result.images = images.filter(src => src.includes('instagram') || src.includes('cdninstagram'));
                    
                    return result;
                }
            """)
            
            if data and (data.get('images') or data.get('profile_data')):
                timestamp = int(time.time())
                
                # Save screenshot
                screenshot_path = f"stealth_extract_{method_num}_{timestamp}.png"
                await page.screenshot(path=screenshot_path, full_page=True)
                
                # Save data
                data_file = f"browser_data_{method_num}_{timestamp}.json"
                with open(data_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"   💎 Direct Access SUCCESS: {len(str(data))} chars")
                return {
                    'success': True,
                    'method': 'direct_access',
                    'data_file': data_file,
                    'screenshot': screenshot_path,
                    'images_found': len(data.get('images', []))
                }
                
        except Exception as e:
            pass
        
        return {'success': False, 'method': 'direct_access'}
    
    async def extract_via_embed_trick(self, page, method_num):
        """Embed trick extraction"""
        try:
            embed_url = f"https://www.instagram.com/p/embed/?url={self.target_url}"
            await page.goto(embed_url, timeout=10000)
            await page.wait_for_timeout(2000)
            
            content = await page.content()
            if self.target in content and len(content) > 5000:
                timestamp = int(time.time())
                filename = f"embed_data_{method_num}_{timestamp}.html"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"   💎 Embed Trick SUCCESS: {len(content)} chars")
                return {
                    'success': True,
                    'method': 'embed_trick',
                    'data_file': filename
                }
                
        except Exception as e:
            pass
        
        return {'success': False, 'method': 'embed_trick'}
    
    async def extract_via_stories_endpoint(self, page, method_num):
        """Stories endpoint extraction"""
        try:
            stories_url = f"https://www.instagram.com/stories/{self.target}/"
            await page.goto(stories_url, timeout=10000)
            await page.wait_for_timeout(3000)
            
            # Check for any story data
            story_data = await page.evaluate("""
                () => {
                    const scripts = Array.from(document.querySelectorAll('script'));
                    for (let script of scripts) {
                        if (script.textContent && script.textContent.includes('story')) {
                            return script.textContent;
                        }
                    }
                    return null;
                }
            """)
            
            if story_data and len(story_data) > 1000:
                timestamp = int(time.time())
                filename = f"stories_data_{method_num}_{timestamp}.txt"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(story_data)
                
                print(f"   💎 Stories SUCCESS: {len(story_data)} chars")
                return {
                    'success': True,
                    'method': 'stories_endpoint',
                    'data_file': filename
                }
                
        except Exception as e:
            pass
        
        return {'success': False, 'method': 'stories_endpoint'}
    
    async def extract_via_hashtag_search(self, page, method_num):
        """Hashtag search extraction"""
        try:
            search_url = f"https://www.instagram.com/explore/tags/{self.target}/"
            await page.goto(search_url, timeout=10000)
            await page.wait_for_timeout(3000)
            
            content = await page.content()
            if self.target in content:
                timestamp = int(time.time())
                filename = f"hashtag_search_{method_num}_{timestamp}.html"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"   💎 Hashtag Search SUCCESS: {len(content)} chars")
                return {
                    'success': True,
                    'method': 'hashtag_search',
                    'data_file': filename
                }
                
        except Exception as e:
            pass
        
        return {'success': False, 'method': 'hashtag_search'}
    
    def cache_and_archive_mining(self):
        """🏴‍☠️ CACHE & ARCHIVE MINING"""
        print("🏴‍☠️ LAUNCHING CACHE MINING...")
        
        cache_sources = [
            f"https://webcache.googleusercontent.com/search?q=cache:{self.target_url}",
            f"https://www.google.com/search?q=site:instagram.com+{self.target}",
            f"https://archive.org/wayback/available?url={self.target_url}",
            f"https://yandex.com/search/?text=site:instagram.com+{self.target}",
            f"https://duckduckgo.com/?q=site:instagram.com+{self.target}"
        ]
        
        def mine_cache(url):
            try:
                response = requests.get(
                    url, 
                    headers=random.choice(self.headers_pool), 
                    timeout=10,
                    proxies={'http': self.mobile_proxy, 'https': self.mobile_proxy}
                )
                
                if response.status_code == 200 and self.target in response.text:
                    timestamp = int(time.time())
                    filename = f"cache_data_{timestamp}_{random.randint(100,999)}.html"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    
                    print(f"   💎 Cache SUCCESS: {len(response.text)} chars -> {filename}")
                    return {'success': True, 'file': filename, 'source': url}
                    
            except Exception as e:
                pass
            
            return {'success': False, 'source': url}
        
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(mine_cache, url) for url in cache_sources]
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result['success']:
                    results.append(result)
        
        if results:
            self.extracted_data['success_methods'].append('CACHE_MINING')
            
        self.extracted_data['extraction_results']['cache_mining'] = results
        print(f"   📊 Cache Results: {len(results)} successful extractions")
        return len(results) > 0
    
    async def execute_instant_extraction(self):
        """🚀 EXECUTE INSTANT EXTRACTION"""
        print("=" * 80)
        print("⚡ INSTANT DATA EXTRACTOR")
        print(f"🎯 TARGET: {self.target}")
        print("🔥 LAUNCHING ALL EXTRACTION METHODS SIMULTANEOUSLY!")
        print("=" * 80)
        
        # Launch all methods in parallel
        tasks = []
        
        # API Assault (in thread)
        api_task = asyncio.create_task(asyncio.to_thread(self.rapid_api_assault))
        tasks.append(api_task)
        
        # Browser extraction
        browser_task = asyncio.create_task(self.stealth_browser_extraction())
        tasks.append(browser_task)
        
        # Cache mining (in thread)
        cache_task = asyncio.create_task(asyncio.to_thread(self.cache_and_archive_mining))
        tasks.append(cache_task)
        
        # Wait for all methods to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Calculate success
        successful_methods = len(self.extracted_data['success_methods'])
        
        # Save final results
        results_file = f"INSTANT_EXTRACTION_{self.target}_{int(time.time())}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.extracted_data, f, indent=2, ensure_ascii=False)
        
        print("=" * 80)
        print("⚡ INSTANT EXTRACTION COMPLETE!")
        print(f"✅ Successful methods: {successful_methods}")
        print(f"🎯 Methods used: {', '.join(self.extracted_data['success_methods'])}")
        print(f"📊 Full results: {results_file}")
        print("🔥 DATA EXTRACTION COMPLETE!")
        print("=" * 80)

if __name__ == "__main__":
    extractor = InstantExtractor()
    asyncio.run(extractor.execute_instant_extraction())
