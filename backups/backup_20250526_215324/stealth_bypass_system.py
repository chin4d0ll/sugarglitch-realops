#!/usr/bin/env python3
"""
💀 ULTIMATE STEALTH BYPASS SYSTEM 💀
Advanced Instagram Bypass Techniques
Target: whatilove1728
"""

import asyncio
import aiohttp
import json
import time
import random
import base64
import hashlib
from datetime import datetime
from playwright.async_api import async_playwright
import requests
from urllib.parse import quote, urlencode

class StealthBypassSystem:
    def __init__(self):
        self.target_username = "whatilove1728"
        self.target_url = "https://www.instagram.com/whatilove1728"
        self.bright_data_auth = 'brd-customer-hl_63f0835e-zone-scraping_browser:59m84ggoef95'
        self.mobile_proxy = 'http://brd-customer-hl_63f0835e-zone-mobile:fl13j3qcjvqh@brd.superproxy.io:33335'
        
        self.results = {
            'target': self.target_username,
            'timestamp': datetime.now().isoformat(),
            'bypass_attempts': {},
            'extracted_data': [],
            'success_count': 0
        }
        
        # Advanced Headers Pool
        self.header_pools = {
            'mobile_ios': {
                'User-Agent': 'Instagram 301.0.0.27.111 (iPhone13,2; iOS 17_0; en_US; en-US; scale=3.00; 1170x2532; 456070817)',
                'X-IG-App-ID': '936619743392459',
                'X-IG-WWW-Claim': '0',
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin'
            },
            'mobile_android': {
                'User-Agent': 'Instagram 301.0.0.27.111 (SM-G998B; Android 13; 30; en_US; 456070817)',
                'X-IG-App-ID': '936619743392459',
                'X-Instagram-AJAX': '1007616710',
                'X-IG-WWW-Claim': 'hmac.AR0rU5dHkflQOM8SzfithTJ5YDR4-cPJJMZFOvSUu5R0_JI',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest'
            },
            'desktop_chrome': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'X-IG-App-ID': '936619743392459',
                'X-IG-WWW-Claim': '0',
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
        }
    
    async def bypass_method_1_api_endpoints(self):
        """🔥 BYPASS METHOD 1: API ENDPOINT EXPLOITATION"""
        print("🔥 BYPASS METHOD 1: API ENDPOINT EXPLOITATION")
        
        api_endpoints = [
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={self.target_username}",
            f"https://www.instagram.com/api/v1/users/web_profile_info/?username={self.target_username}",
            f"https://www.instagram.com/{self.target_username}/?__a=1&__d=dis",
            f"https://www.instagram.com/api/v1/users/{self.target_username}/info/",
            f"https://i.instagram.com/api/v1/users/{self.target_username}/",
            f"https://www.instagram.com/web/search/topsearch/?query={self.target_username}",
            f"https://i.instagram.com/api/v1/web/search/topsearch/?query={self.target_username}",
            f"https://www.instagram.com/{self.target_username}/channel/?__a=1",
            f"https://graph.instagram.com/{self.target_username}?fields=id,username,account_type,media_count",
        ]
        
        success_count = 0
        
        for i, endpoint in enumerate(api_endpoints):
            for header_type, headers in self.header_pools.items():
                try:
                    print(f"   🔍 Testing API {i+1}/{len(api_endpoints)} with {header_type}")
                    
                    response = requests.get(
                        endpoint,
                        headers=headers,
                        timeout=10,
                        proxies={'http': self.mobile_proxy, 'https': self.mobile_proxy} if random.random() > 0.5 else None
                    )
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            if 'user' in str(data) or 'username' in str(data):
                                success_count += 1
                                filename = f"api_success_{i}_{header_type}_{int(time.time())}.json"
                                
                                with open(filename, 'w') as f:
                                    json.dump(data, f, indent=2)
                                
                                self.results['bypass_attempts'][f'api_{i}_{header_type}'] = {
                                    'method': 'API Endpoint',
                                    'endpoint': endpoint,
                                    'status': response.status_code,
                                    'success': True,
                                    'data_file': filename,
                                    'response_size': len(response.text)
                                }
                                
                                print(f"   ✅ SUCCESS! API {i+1} with {header_type}: {len(response.text)} chars")
                                break
                        except:
                            pass
                    
                    await asyncio.sleep(random.uniform(1, 3))
                    
                except Exception as e:
                    continue
        
        print(f"   📊 API Method Success: {success_count} endpoints")
        return success_count > 0
    
    async def bypass_method_2_graphql_queries(self):
        """🌐 BYPASS METHOD 2: GRAPHQL EXPLOITATION"""
        print("🌐 BYPASS METHOD 2: GRAPHQL EXPLOITATION")
        
        graphql_queries = [
            {
                'query_hash': '58b6785bea111c67129decbe6a448951',
                'variables': json.dumps({'username': self.target_username, 'fetch_mutual': True})
            },
            {
                'query_hash': '69cba40317214236af40e7efa697781d',
                'variables': json.dumps({'username': self.target_username})
            },
            {
                'query_hash': 'c76146de99bb02f6415203be841dd25a',
                'variables': json.dumps({'user_id': self.target_username})
            }
        ]
        
        success_count = 0
        
        for i, query_data in enumerate(graphql_queries):
            for header_type, headers in self.header_pools.items():
                try:
                    print(f"   🔍 Testing GraphQL {i+1}/{len(graphql_queries)} with {header_type}")
                    
                    url = "https://www.instagram.com/graphql/query/"
                    params = {
                        'query_hash': query_data['query_hash'],
                        'variables': query_data['variables']
                    }
                    
                    response = requests.get(
                        url,
                        params=params,
                        headers=headers,
                        timeout=10,
                        proxies={'http': self.mobile_proxy, 'https': self.mobile_proxy} if random.random() > 0.3 else None
                    )
                    
                    if response.status_code == 200 and 'data' in response.text:
                        try:
                            data = response.json()
                            if data.get('data'):
                                success_count += 1
                                filename = f"graphql_success_{i}_{header_type}_{int(time.time())}.json"
                                
                                with open(filename, 'w') as f:
                                    json.dump(data, f, indent=2)
                                
                                self.results['bypass_attempts'][f'graphql_{i}_{header_type}'] = {
                                    'method': 'GraphQL Query',
                                    'query_hash': query_data['query_hash'],
                                    'status': response.status_code,
                                    'success': True,
                                    'data_file': filename,
                                    'response_size': len(response.text)
                                }
                                
                                print(f"   ✅ SUCCESS! GraphQL {i+1} with {header_type}: {len(response.text)} chars")
                                break
                        except:
                            pass
                    
                    await asyncio.sleep(random.uniform(2, 4))
                    
                except Exception as e:
                    continue
        
        print(f"   📊 GraphQL Method Success: {success_count} queries")
        return success_count > 0
    
    async def bypass_method_3_browser_automation(self):
        """🤖 BYPASS METHOD 3: ADVANCED BROWSER AUTOMATION"""
        print("🤖 BYPASS METHOD 3: ADVANCED BROWSER AUTOMATION")
        
        success_count = 0
        
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(f'wss://{self.bright_data_auth}@brd.superproxy.io:9222')
            
            try:
                # Method 3a: Stealth Navigation
                page = await browser.new_page()
                await page.route("**/*", lambda route: route.continue_())
                
                # Add stealth scripts
                await page.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                    Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                    Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                    window.chrome = {runtime: {}};
                """)
                
                try:
                    await page.goto(self.target_url, timeout=30000)
                    await page.wait_for_timeout(random.randint(3000, 7000))
                    
                    # Try to extract data via JavaScript
                    data = await page.evaluate("""
                        () => {
                            const scripts = Array.from(document.querySelectorAll('script'));
                            const jsonScripts = scripts.filter(s => s.textContent && s.textContent.includes('window._sharedData'));
                            if (jsonScripts.length > 0) {
                                try {
                                    const match = jsonScripts[0].textContent.match(/window._sharedData = ({.*?});/);
                                    if (match) return JSON.parse(match[1]);
                                } catch (e) {}
                            }
                            return null;
                        }
                    """)
                    
                    if data:
                        success_count += 1
                        filename = f"browser_shared_data_{int(time.time())}.json"
                        with open(filename, 'w') as f:
                            json.dump(data, f, indent=2)
                        
                        print(f"   ✅ SUCCESS! Extracted _sharedData: {filename}")
                        
                        self.results['bypass_attempts']['browser_shared_data'] = {
                            'method': 'Browser Automation - SharedData',
                            'success': True,
                            'data_file': filename
                        }
                    
                    # Take screenshot
                    screenshot_path = f"browser_capture_{int(time.time())}.png"
                    await page.screenshot(path=screenshot_path, full_page=True)
                    
                    print(f"   📸 Screenshot saved: {screenshot_path}")
                    
                except Exception as e:
                    print(f"   ❌ Browser automation failed: {str(e)}")
                
                await page.close()
                
            finally:
                await browser.close()
        
        print(f"   📊 Browser Method Success: {success_count} extractions")
        return success_count > 0
    
    async def bypass_method_4_session_hijacking(self):
        """🔓 BYPASS METHOD 4: SESSION SIMULATION"""
        print("🔓 BYPASS METHOD 4: SESSION SIMULATION")
        
        # Simulate different session types
        session_types = [
            'logged_out_visitor',
            'mobile_app_user',
            'web_browser_user',
            'api_client',
            'bot_crawler'
        ]
        
        success_count = 0
        
        for session_type in session_types:
            try:
                print(f"   🔍 Testing session type: {session_type}")
                
                # Create session-specific headers
                if session_type == 'mobile_app_user':
                    headers = self.header_pools['mobile_ios'].copy()
                    headers['X-IG-Connection-Type'] = 'WIFI'
                    headers['X-IG-Capabilities'] = '3brTvw=='
                elif session_type == 'web_browser_user':
                    headers = self.header_pools['desktop_chrome'].copy()
                    headers['Cache-Control'] = 'max-age=0'
                elif session_type == 'api_client':
                    headers = self.header_pools['mobile_android'].copy()
                    headers['X-IG-App-Locale'] = 'en_US'
                    headers['X-IG-Device-Locale'] = 'en_US'
                else:
                    headers = self.header_pools['desktop_chrome']
                
                response = requests.get(
                    self.target_url,
                    headers=headers,
                    timeout=15,
                    proxies={'http': self.mobile_proxy, 'https': self.mobile_proxy}
                )
                
                if response.status_code == 200 and len(response.text) > 10000:
                    success_count += 1
                    filename = f"session_{session_type}_{int(time.time())}.html"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    
                    self.results['bypass_attempts'][f'session_{session_type}'] = {
                        'method': 'Session Simulation',
                        'session_type': session_type,
                        'status': response.status_code,
                        'success': True,
                        'data_file': filename,
                        'response_size': len(response.text)
                    }
                    
                    print(f"   ✅ SUCCESS! {session_type}: {len(response.text)} chars")
                
                await asyncio.sleep(random.uniform(2, 5))
                
            except Exception as e:
                print(f"   ❌ {session_type} failed: {str(e)}")
        
        print(f"   📊 Session Method Success: {success_count} sessions")
        return success_count > 0
    
    async def bypass_method_5_cached_data_mining(self):
        """💎 BYPASS METHOD 5: CACHED DATA MINING"""
        print("💎 BYPASS METHOD 5: CACHED DATA MINING")
        
        cache_sources = [
            f"https://webcache.googleusercontent.com/search?q=cache:{quote(self.target_url)}",
            f"https://archive.org/wayback/available?url={quote(self.target_url)}",
            f"https://cached.to/{quote(self.target_url)}",
            f"https://www.google.com/search?q=site:instagram.com+{self.target_username}",
            f"https://yandex.com/search/?text=site:instagram.com+{self.target_username}",
        ]
        
        success_count = 0
        
        for i, cache_url in enumerate(cache_sources):
            try:
                print(f"   🔍 Testing cache source {i+1}/{len(cache_sources)}")
                
                response = requests.get(
                    cache_url,
                    headers=self.header_pools['desktop_chrome'],
                    timeout=15,
                    proxies={'http': self.mobile_proxy, 'https': self.mobile_proxy} if random.random() > 0.7 else None
                )
                
                if response.status_code == 200 and self.target_username in response.text:
                    success_count += 1
                    filename = f"cache_data_{i}_{int(time.time())}.html"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    
                    self.results['bypass_attempts'][f'cache_{i}'] = {
                        'method': 'Cached Data Mining',
                        'source': cache_url,
                        'status': response.status_code,
                        'success': True,
                        'data_file': filename,
                        'response_size': len(response.text)
                    }
                    
                    print(f"   ✅ SUCCESS! Cache {i+1}: {len(response.text)} chars")
                
                await asyncio.sleep(random.uniform(3, 6))
                
            except Exception as e:
                print(f"   ❌ Cache {i+1} failed: {str(e)}")
        
        print(f"   📊 Cache Method Success: {success_count} sources")
        return success_count > 0
    
    async def execute_stealth_bypass(self):
        """🚀 EXECUTE COMPLETE STEALTH BYPASS OPERATION"""
        print("=" * 80)
        print("💀 ULTIMATE STEALTH BYPASS SYSTEM")
        print(f"🎯 TARGET: {self.target_username}")
        print("🔥 MISSION: COMPLETE SECURITY BYPASS")
        print("=" * 80)
        
        total_success = 0
        
        # Execute all bypass methods
        if await self.bypass_method_1_api_endpoints():
            total_success += 1
        print()
        
        if await self.bypass_method_2_graphql_queries():
            total_success += 1
        print()
        
        if await self.bypass_method_3_browser_automation():
            total_success += 1
        print()
        
        if await self.bypass_method_4_session_hijacking():
            total_success += 1
        print()
        
        if await self.bypass_method_5_cached_data_mining():
            total_success += 1
        
        self.results['success_count'] = total_success
        
        # Save results
        results_file = f"stealth_bypass_results_{int(time.time())}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print("=" * 80)
        print("💀 STEALTH BYPASS OPERATION COMPLETE")
        print(f"✅ Successful methods: {total_success}/5")
        print(f"📊 Results saved: {results_file}")
        print("🔥 Data extraction complete!")
        print("=" * 80)

if __name__ == "__main__":
    bypass_system = StealthBypassSystem()
    asyncio.run(bypass_system.execute_stealth_bypass())
