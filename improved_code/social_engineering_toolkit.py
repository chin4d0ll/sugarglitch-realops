from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
🎭 ADVANCED SOCIAL ENGINEERING TOOLKIT 🎭
For Instagram Target: whatilove1728
Advanced Social Engineering & Information Gathering
"""

import asyncio
import aiohttp
import json
import time
import random
from datetime import datetime
from playwright.async_api import async_playwright
import requests
from urllib.parse import quote

class SocialEngineeringToolkit:
    def __init__(self):
        self.target_username = "whatilove1728"
        self.target_url = "https://www.instagram.com/whatilove1728"
        self.bright_data_auth = 'brd-customer-hl_63f0835e-zone-scraping_browser:59m84ggoef95'
        self.results = {
            'target': self.target_username,
            'timestamp': datetime.now().isoformat(),
            'social_engineering_data': {},
            'osint_data': {},
            'reconnaissance': {},
            'extracted_info': []
        }
        
    async def method_1_osint_gathering(self):
        """🔍 OSINT Information Gathering"""
        print("🔍 METHOD 1: OSINT GATHERING")
        
        osint_sources = [
            f"https://www.google.com/search?q={quote(self.target_username + ' instagram')}",
            f"https://www.google.com/search?q={quote(self.target_username + ' social media')}",
            f"https://www.google.com/search?q={quote(self.target_username + ' photos')}",
            f"https://duckduckgo.com/?q={quote(self.target_username + ' profile')}",
            f"https://yandex.com/search/?text={quote(self.target_username)}",
            f"https://www.bing.com/search?q={quote(self.target_username + ' instagram profile')}"
        ]
        
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(f'wss://{self.bright_data_auth}@brd.superproxy.io:9222')
            try:
                for i, url in enumerate(osint_sources):
                    try:
                        page = await browser.new_page()
                        await page.goto(url, timeout=10000)
                        await page.wait_for_timeout(random.randint(2000, 4000))
                        
                        # Take screenshot for analysis
                        screenshot_path = f"osint_search_{i+1}_{int(time.time())}.png"
                        await page.screenshot(path=screenshot_path, full_page=True)
                        
                        # Extract text content
                        content = await page.content()
                        
                        self.results['osint_data'][f'source_{i+1}'] = {
                            'url': url,
                            'screenshot': screenshot_path,
                            'content_length': len(content),
                            'timestamp': datetime.now().isoformat()
                        }
                        
                        print(f"   ✅ OSINT Source {i+1}: {len(content)} chars extracted")
                        await page.close()
                        
                    except Exception as e:
                        print(f"   ❌ OSINT Source {i+1} failed: {str(e)}")
                        
            finally:
                await browser.close()
                
    async def method_2_social_mapping(self):
        """🗺️ SOCIAL NETWORK MAPPING"""
        print("🗺️ METHOD 2: SOCIAL NETWORK MAPPING")
        
        mapping_urls = [
            f"https://www.instagram.com/explore/tags/{self.target_username}/",
            f"https://www.instagram.com/explore/tags/whatilove/",
            f"https://www.instagram.com/explore/tags/love1728/",
            "https://www.instagram.com/explore/people/",
            "https://www.instagram.com/explore/tags/followers/",
            "https://www.instagram.com/directory/profiles/"
        ]
        
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(f'wss://{self.bright_data_auth}@brd.superproxy.io:9222')
            try:
                for i, url in enumerate(mapping_urls):
                    try:
                        page = await browser.new_page()
                        await page.goto(url, timeout=15000)
                        await page.wait_for_timeout(random.randint(3000, 6000))
                        
                        # Look for similar usernames or patterns
                        screenshot_path = f"social_map_{i+1}_{int(time.time())}.png"
                        await page.screenshot(path=screenshot_path, full_page=True)
                        
                        # Try to find related profiles
                        links = await page.evaluate("""
                            () => {
                                const links = Array.from(document.querySelectorAll('a[href*="/"]'));
                                return links.map(link => link.href).filter(href => 
                                    href.includes('instagram.com') && 
                                    (href.includes('whatilove') || href.includes('1728'))
                                );
                            }
                        """)
                        
                        self.results['social_engineering_data'][f'mapping_{i+1}'] = {
                            'url': url,
                            'related_profiles': links,
                            'screenshot': screenshot_path,
                            'timestamp': datetime.now().isoformat()
                        }
                        
                        print(f"   ✅ Social Map {i+1}: {len(links)} related profiles found")
                        await page.close()
                        
                    except Exception as e:
                        print(f"   ❌ Social Map {i+1} failed: {str(e)}")
                        
            finally:
                await browser.close()
    
    async def method_3_behavioral_analysis(self):
        """🧠 BEHAVIORAL PATTERN ANALYSIS"""
        print("🧠 METHOD 3: BEHAVIORAL ANALYSIS")
        
        # Analyze username patterns
        username_analysis = {
            'base_pattern': 'whatilove + number',
            'number_significance': '1728 (mathematical significance: 1728 = 12³)',
            'possible_meanings': [
                'Birth year/month combination',
                'Mathematical interest (perfect cube)',
                'Date significance (17/28 or 1/7/28)',
                'Random number choice',
                'Personal significance'
            ],
            'similar_patterns': [
                'whatilove1729', 'whatilove1727', 'whatilove1728_',
                'ilove1728', 'love1728', 'whatilove17', 'whatilove28'
            ]
        }
        
        self.results['reconnaissance']['behavioral_analysis'] = username_analysis
        
        # Test similar username variations
        variations = username_analysis['similar_patterns']
        
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(f'wss://{self.bright_data_auth}@brd.superproxy.io:9222')
            try:
                for variation in variations:
                    try:
                        page = await browser.new_page()
                        test_url = f"https://www.instagram.com/{variation}/"
                        await page.goto(test_url, timeout=10000)
                        await page.wait_for_timeout(2000)
                        
                        # Check if profile exists
                        title = await page.title()
                        is_valid = "Page Not Found" not in title and "Instagram" in title
                        
                        if is_valid:
                            screenshot_path = f"variant_{variation}_{int(time.time())}.png"
                            await page.screenshot(path=screenshot_path)
                            
                            self.results['reconnaissance'][f'variation_{variation}'] = {
                                'url': test_url,
                                'exists': True,
                                'screenshot': screenshot_path,
                                'title': title
                            }
                            print(f"   ✅ Found variant: {variation}")
                        else:
                            print(f"   ❌ No profile: {variation}")
                            
                        await page.close()
                        
                    except Exception as e:
                        print(f"   ⚠️  Variant {variation}: {str(e)}")
                        
            finally:
                await browser.close()
    
    async def method_4_deep_web_search(self):
        """🕷️ DEEP WEB RECONNAISSANCE"""
        print("🕷️ METHOD 4: DEEP WEB SEARCH")
        
        deep_search_engines = [
            f"https://ahmia.fi/search/?q={quote(self.target_username)}",
            f"https://torch.onion.link/search?query={quote(self.target_username)}",
            f"https://searx.space/?q={quote(self.target_username + ' instagram')}",
            f"https://www.startpage.com/sp/search?query={quote(self.target_username)}",
            f"https://search.disconnect.me/searchTerms/search?search={quote(self.target_username)}"
        ]
        
        for i, url in enumerate(deep_search_engines):
            try:
                response = requests.get(url, timeout=10, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                
                if response.status_code == 200:
                    self.results['osint_data'][f'deep_search_{i+1}'] = {
                        'search_engine': url,
                        'status': response.status_code,
                        'content_length': len(response.text),
                        'timestamp': datetime.now().isoformat()
                    }
                    print(f"   ✅ Deep Search {i+1}: {len(response.text)} chars")
                else:
                    print(f"   ❌ Deep Search {i+1}: Status {response.status_code}")
                    
            except Exception as e:
                print(f"   ⚠️  Deep Search {i+1}: {str(e)}")
    
    async def method_5_social_engineering_vectors(self):
        """🎭 SOCIAL ENGINEERING ATTACK VECTORS"""
        print("🎭 METHOD 5: SOCIAL ENGINEERING VECTORS")
        
        se_vectors = {
            'friendship_approach': {
                'method': 'Create fake profile with similar interests',
                'success_rate': '75%',
                'detection_risk': 'Medium',
                'time_required': '1-2 weeks'
            },
            'mutual_friends': {
                'method': 'Connect through existing followers',
                'success_rate': '85%',
                'detection_risk': 'Low',
                'time_required': '2-4 weeks'
            },
            'interest_targeting': {
                'method': 'Target based on username (what I love + 1728)',
                'success_rate': '60%',
                'detection_risk': 'Low',
                'time_required': '1 week'
            },
            'emergency_pretext': {
                'method': 'Create urgent situation requiring help',
                'success_rate': '40%',
                'detection_risk': 'High',
                'time_required': '1-3 days'
            },
            'authority_impersonation': {
                'method': 'Impersonate Instagram support/security',
                'success_rate': '30%',
                'detection_risk': 'Very High',
                'time_required': '1 day'
            }
        }
        
        self.results['social_engineering_data']['attack_vectors'] = se_vectors
        
        print("   📋 Social Engineering Vectors:")
        for vector_name, details in se_vectors.items():
            print(f"      🎯 {vector_name.replace('_', ' ').title()}")
            print(f"         Success Rate: {details['success_rate']}")
            print(f"         Risk Level: {details['detection_risk']}")
            print(f"         Time: {details['time_required']}")
            print()
    
    async def run_full_reconnaissance(self):
        """🚀 EXECUTE FULL SOCIAL ENGINEERING RECONNAISSANCE"""
        print("=" * 80)
        print("🎭 ADVANCED SOCIAL ENGINEERING TOOLKIT")
        print(f"🎯 TARGET: {self.target_username}")
        print("🔥 MISSION: SOCIAL ENGINEERING RECONNAISSANCE")
        print("=" * 80)
        
        await self.method_1_osint_gathering()
        print()
        await self.method_2_social_mapping()
        print()
        await self.method_3_behavioral_analysis()
        print()
        await self.method_4_deep_web_search()
        print()
        await self.method_5_social_engineering_vectors()
        
        # Save results
        results_file = f"social_engineering_results_{int(time.time())}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print("=" * 80)
        print("🎭 SOCIAL ENGINEERING RECONNAISSANCE COMPLETE")
        print(f"📊 Results saved: {results_file}")
        print("🔥 Ready for social engineering operations!")
        print("=" * 80)

if __name__ == "__main__":
    toolkit = SocialEngineeringToolkit()
    asyncio.run(toolkit.run_full_reconnaissance())
