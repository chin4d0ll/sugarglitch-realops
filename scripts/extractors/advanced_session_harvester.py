#!/usr/bin/env python3
"""
🔥 ADVANCED SESSION HARVESTER 🔥
Target: whatilove1728
Mission: Extract ALL session identifiers and authentication tokens
"""

import asyncio
import aiohttp
import json
import time
import random
from datetime import datetime
from playwright.async_api import async_playwright
import ssl
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AdvancedSessionHarvester:
    def __init__(self):
        self.target_username = "whatilove1728"
        self.target_url = f"https://www.instagram.com/{self.target_username}/"
        
        # Proxy configurations
        self.mobile_proxy = "brd-customer-hl_63f0835e-zone-mobile:fl13j3qcjvqh@brd.superproxy.io:22225"
        self.scraping_proxy = "brd-customer-hl_63f0835e-zone-scraping_browser:59m84ggoef95@brd.superproxy.io:22225"
        
        # Anti-detection headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        
        self.session_data = {
            'target': self.target_username,
            'timestamp': datetime.now().isoformat(),
            'browser_sessions': {},
            'api_sessions': {},
            'authenticated_sessions': {},
            'session_cookies': {},
            'authentication_tokens': {},
            'csrf_tokens': {},
            'device_identifiers': {},
            'session_analysis': {}
        }

    async def extract_browser_session(self):
        """Extract session data using browser automation"""
        print("🌐 EXTRACTING BROWSER SESSION DATA...")
        
        async with async_playwright() as p:
            try:
                # Launch browser with proxy
                browser = await p.chromium.launch(
                    headless=False,
                    proxy={
                        "server": f"http://{self.scraping_proxy}",
                    },
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-dev-shm-usage',
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-web-security',
                        '--disable-features=VizDisplayCompositor',
                        '--ignore-ssl-errors=yes',
                        '--ignore-certificate-errors=yes'
                    ]
                )
                
                context = await browser.new_context(
                    user_agent=self.headers['User-Agent'],
                    viewport={'width': 1920, 'height': 1080},
                    ignore_https_errors=True
                )
                
                page = await context.new_page()
                
                # Navigate to Instagram
                await page.goto('https://www.instagram.com', wait_until='networkidle')
                await asyncio.sleep(3)
                
                # Extract all cookies
                cookies = await context.cookies()
                for cookie in cookies:
                    self.session_data['session_cookies'][cookie['name']] = cookie['value']
                    print(f"   🍪 Cookie: {cookie['name']} = {cookie['value'][:20]}...")
                
                # Extract session storage
                session_storage = await page.evaluate('() => JSON.stringify(sessionStorage)')
                if session_storage != '{}':
                    self.session_data['browser_sessions']['sessionStorage'] = json.loads(session_storage)
                
                # Extract local storage
                local_storage = await page.evaluate('() => JSON.stringify(localStorage)')
                if local_storage != '{}':
                    self.session_data['browser_sessions']['localStorage'] = json.loads(local_storage)
                
                # Extract window._sharedData
                shared_data = await page.evaluate('() => window._sharedData')
                if shared_data:
                    self.session_data['browser_sessions']['_sharedData'] = shared_data
                
                # Extract Instagram config
                config_data = await page.evaluate('''() => {
                    const data = {};
                    if (window._sharedData) {
                        data.config = window._sharedData.config;
                        data.csrf_token = window._sharedData.config?.csrf_token;
                        data.viewer = window._sharedData.config?.viewer;
                        data.viewerId = window._sharedData.config?.viewerId;
                    }
                    return data;
                }''')
                
                if config_data:
                    self.session_data['authentication_tokens'].update(config_data)
                
                # Try to access the target profile
                try:
                    await page.goto(self.target_url, wait_until='networkidle')
                    await asyncio.sleep(2)
                    
                    # Extract profile-specific data
                    profile_data = await page.evaluate('''() => {
                        const data = {};
                        if (window._sharedData && window._sharedData.entry_data) {
                            data.entry_data = window._sharedData.entry_data;
                        }
                        return data;
                    }''')
                    
                    if profile_data:
                        self.session_data['browser_sessions']['profile_data'] = profile_data
                
                except Exception as e:
                    print(f"   ⚠️  Profile access failed: {str(e)[:50]}...")
                
                await browser.close()
                print(f"   ✅ Browser session extraction complete")
                
            except Exception as e:
                print(f"   ❌ Browser extraction failed: {str(e)[:100]}...")

    async def extract_api_sessions(self):
        """Extract session data from API endpoints"""
        print("🔧 EXTRACTING API SESSION DATA...")
        
        # Create SSL context that ignores certificate errors
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        
        async with aiohttp.ClientSession(
            headers=self.headers,
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=30)
        ) as session:
            
            # API endpoints to check
            endpoints = [
                'https://www.instagram.com/',
                'https://www.instagram.com/api/v1/web/get_ruling_for_content/',
                'https://i.instagram.com/api/v1/',
                f'https://www.instagram.com/{self.target_username}/',
                'https://www.instagram.com/api/v1/users/web_profile_info/',
                'https://www.instagram.com/graphql/query/',
                'https://i.instagram.com/api/v1/users/search/',
                'https://www.instagram.com/web/search/topsearch/'
            ]
            
            for endpoint in endpoints:
                try:
                    async with session.get(endpoint, ssl=False) as response:
                        # Extract cookies from response
                        if response.cookies:
                            for cookie in response.cookies:
                                self.session_data['api_sessions'][f'{endpoint}_cookie_{cookie.key}'] = cookie.value
                        
                        # Extract headers
                        headers = dict(response.headers)
                        if 'set-cookie' in headers:
                            self.session_data['api_sessions'][f'{endpoint}_headers'] = headers
                        
                        # Try to extract JSON data
                        if 'application/json' in response.headers.get('content-type', ''):
                            try:
                                data = await response.json()
                                if 'csrf_token' in str(data):
                                    self.session_data['api_sessions'][f'{endpoint}_data'] = data
                            except:
                                pass
                        
                        print(f"   ✅ API endpoint checked: {endpoint}")
                        
                except Exception as e:
                    print(f"   ❌ API endpoint failed {endpoint}: {str(e)[:50]}...")

    async def extract_authenticated_sessions(self):
        """Attempt to extract authenticated session data"""
        print("🔑 EXTRACTING AUTHENTICATED SESSION DATA...")
        
        # Use existing session cookies to make authenticated requests
        if self.session_data['session_cookies']:
            cookie_string = '; '.join([f"{k}={v}" for k, v in self.session_data['session_cookies'].items()])
            
            auth_headers = self.headers.copy()
            auth_headers['Cookie'] = cookie_string
            
            if 'csrftoken' in self.session_data['session_cookies']:
                auth_headers['X-CSRFToken'] = self.session_data['session_cookies']['csrftoken']
            
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            
            async with aiohttp.ClientSession(
                headers=auth_headers,
                connector=connector,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as session:
                
                # Authenticated endpoints
                auth_endpoints = [
                    'https://www.instagram.com/api/v1/web/fxcal/ig_sso_users/',
                    'https://www.instagram.com/api/v1/accounts/edit/',
                    'https://www.instagram.com/api/v1/direct_v2/inbox/',
                    'https://www.instagram.com/api/v1/news/inbox/',
                    'https://www.instagram.com/api/v1/users/self/',
                    f'https://www.instagram.com/api/v1/users/{self.target_username}/info/',
                    f'https://www.instagram.com/api/v1/friendships/show/{self.target_username}/'
                ]
                
                for endpoint in auth_endpoints:
                    try:
                        async with session.get(endpoint, ssl=False) as response:
                            if response.status == 200:
                                try:
                                    data = await response.json()
                                    self.session_data['authenticated_sessions'][endpoint] = data
                                    print(f"   ✅ Authenticated endpoint success: {endpoint}")
                                except:
                                    text = await response.text()
                                    if len(text) > 100:
                                        self.session_data['authenticated_sessions'][endpoint] = text[:500]
                            else:
                                print(f"   ⚠️  Authenticated endpoint {response.status}: {endpoint}")
                                
                    except Exception as e:
                        print(f"   ❌ Authenticated endpoint failed {endpoint}: {str(e)[:50]}...")

    def analyze_session_data(self):
        """Analyze extracted session data for authentication tokens"""
        print("🔍 ANALYZING SESSION DATA...")
        
        analysis = {
            'session_identifiers': [],
            'csrf_tokens': [],
            'authentication_tokens': [],
            'device_identifiers': [],
            'user_identifiers': [],
            'app_identifiers': []
        }
        
        # Search for session IDs in all data
        all_data = json.dumps(self.session_data)
        
        # Session ID patterns
        session_patterns = [
            'sessionid', 'session_id', 'sid', 'PHPSESSID', 'JSESSIONID',
            'ASP.NET_SessionId', 'session', 'sess', 'token', 'auth_token',
            'access_token', 'bearer', 'authorization'
        ]
        
        for pattern in session_patterns:
            if pattern in all_data.lower():
                analysis['session_identifiers'].append({
                    'pattern': pattern,
                    'found': True,
                    'context': 'Multiple locations'
                })
        
        # Extract CSRF tokens
        csrf_tokens = []
        if 'csrftoken' in self.session_data['session_cookies']:
            csrf_tokens.append({
                'type': 'cookie',
                'name': 'csrftoken',
                'value': self.session_data['session_cookies']['csrftoken'],
                'length': len(self.session_data['session_cookies']['csrftoken'])
            })
        
        if 'csrf_token' in self.session_data.get('authentication_tokens', {}):
            csrf_tokens.append({
                'type': 'token',
                'name': 'csrf_token',
                'value': self.session_data['authentication_tokens']['csrf_token'],
                'length': len(str(self.session_data['authentication_tokens']['csrf_token']))
            })
        
        analysis['csrf_tokens'] = csrf_tokens
        
        # Extract device identifiers
        device_ids = []
        for key, value in self.session_data['session_cookies'].items():
            if 'did' in key.lower() or 'device' in key.lower():
                device_ids.append({
                    'type': 'cookie',
                    'name': key,
                    'value': value,
                    'length': len(value)
                })
        
        analysis['device_identifiers'] = device_ids
        
        # Extract user identifiers
        user_ids = []
        if 'viewerId' in self.session_data.get('authentication_tokens', {}):
            user_ids.append({
                'type': 'viewer',
                'name': 'viewerId',
                'value': self.session_data['authentication_tokens']['viewerId'],
                'length': len(str(self.session_data['authentication_tokens']['viewerId']))
            })
        
        analysis['user_identifiers'] = user_ids
        
        self.session_data['session_analysis'] = analysis
        
        # Print summary
        print(f"   📊 Session Identifiers: {len(analysis['session_identifiers'])}")
        print(f"   🛡️  CSRF Tokens: {len(analysis['csrf_tokens'])}")
        print(f"   📱 Device Identifiers: {len(analysis['device_identifiers'])}")
        print(f"   👤 User Identifiers: {len(analysis['user_identifiers'])}")
        
        for csrf in analysis['csrf_tokens']:
            print(f"   🔑 {csrf['type'].upper()} CSRF: {csrf['name']} = {csrf['value'][:20]}...")

    async def harvest_all_sessions(self):
        """Main harvesting function"""
        print("=" * 80)
        print("🔥 ADVANCED SESSION HARVESTER ACTIVATED")
        print(f"🎯 TARGET: {self.target_username}")
        print("🔥 HARVESTING ALL SESSION DATA")
        print("=" * 80)
        
        # Execute all extraction methods
        await self.extract_browser_session()
        await asyncio.sleep(2)
        
        await self.extract_api_sessions()
        await asyncio.sleep(2)
        
        await self.extract_authenticated_sessions()
        await asyncio.sleep(1)
        
        self.analyze_session_data()
        
        # Save results
        timestamp = int(time.time())
        filename = f"ADVANCED_SESSION_HARVEST_{self.target_username}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.session_data, f, indent=2)
        
        print("=" * 80)
        print("🔥 SESSION HARVESTING COMPLETE!")
        print(f"📊 Results saved: {filename}")
        print("🔥 SESSION DATA READY FOR EXPLOITATION!")
        print("=" * 80)
        
        return self.session_data

async def main():
    harvester = AdvancedSessionHarvester()
    return await harvester.harvest_all_sessions()

if __name__ == "__main__":
    asyncio.run(main())
