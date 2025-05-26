#!/usr/bin/env python3
"""
🔐 SESSION ID EXTRACTOR 🔐
Extract session IDs and authentication tokens
Target: whatilove1728
"""

import asyncio
import json
import re
import time
from datetime import datetime
from playwright.async_api import async_playwright
import requests

class SessionExtractor:
    def __init__(self):
        self.target = "whatilove1728"
        self.target_url = "https://www.instagram.com/whatilove1728"
        self.bright_data_auth = 'brd-customer-hl_63f0835e-zone-scraping_browser:59m84ggoef95'
        self.mobile_proxy = 'http://brd-customer-hl_63f0835e-zone-mobile:fl13j3qcjvqh@brd.superproxy.io:33335'
        
        self.session_data = {
            'target': self.target,
            'timestamp': datetime.now().isoformat(),
            'session_info': {},
            'cookies': {},
            'tokens': {},
            'headers': {}
        }

    async def extract_browser_session_data(self):
        """🔍 EXTRACT SESSION DATA FROM BROWSER"""
        print("🔍 EXTRACTING BROWSER SESSION DATA...")
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.connect_over_cdp(f'wss://{self.bright_data_auth}@brd.superproxy.io:9222')
                page = await browser.new_page()
                
                # Navigate to Instagram
                await page.goto("https://www.instagram.com/", timeout=15000)
                await page.wait_for_timeout(3000)
                
                # Extract cookies
                cookies = await page.context.cookies()
                print(f"   📊 Found {len(cookies)} cookies")
                
                # Convert cookies to dict for easier access
                cookie_dict = {}
                for cookie in cookies:
                    cookie_dict[cookie['name']] = cookie['value']
                
                self.session_data['cookies'] = cookie_dict
                
                # Extract session-related cookies
                session_cookies = {}
                for name, value in cookie_dict.items():
                    if any(keyword in name.lower() for keyword in ['session', 'id', 'token', 'csrf', 'auth']):
                        session_cookies[name] = value
                        print(f"   🔑 Session Cookie: {name} = {value[:20]}...")
                
                self.session_data['session_info']['session_cookies'] = session_cookies
                
                # Extract JavaScript session data
                session_js_data = await page.evaluate("""
                    () => {
                        const result = {};
                        
                        // Look for session ID in localStorage
                        try {
                            for (let i = 0; i < localStorage.length; i++) {
                                const key = localStorage.key(i);
                                if (key && (key.includes('session') || key.includes('id') || key.includes('token'))) {
                                    result['localStorage_' + key] = localStorage.getItem(key);
                                }
                            }
                        } catch(e) {}
                        
                        // Look for session ID in sessionStorage
                        try {
                            for (let i = 0; i < sessionStorage.length; i++) {
                                const key = sessionStorage.key(i);
                                if (key && (key.includes('session') || key.includes('id') || key.includes('token'))) {
                                    result['sessionStorage_' + key] = sessionStorage.getItem(key);
                                }
                            }
                        } catch(e) {}
                        
                        // Look for window variables
                        if (window._sharedData) {
                            result['_sharedData'] = window._sharedData;
                        }
                        
                        if (window.__additionalDataLoaded) {
                            result['__additionalDataLoaded'] = window.__additionalDataLoaded;
                        }
                        
                        // Look for any Instagram-specific variables
                        const igVars = {};
                        for (let prop in window) {
                            if (prop.includes('ig') || prop.includes('IG') || prop.includes('instagram')) {
                                try {
                                    igVars[prop] = typeof window[prop] === 'object' ? '[Object]' : String(window[prop]).substring(0, 100);
                                } catch(e) {}
                            }
                        }
                        result['instagram_variables'] = igVars;
                        
                        return result;
                    }
                """)
                
                self.session_data['session_info']['javascript_data'] = session_js_data
                
                # Navigate to target profile to get specific session data
                await page.goto(self.target_url, timeout=15000)
                await page.wait_for_timeout(3000)
                
                # Extract any session data from network requests
                page_content = await page.content()
                
                # Look for session IDs in page content
                session_patterns = [
                    r'"sessionid":"([^"]+)"',
                    r'"session_id":"([^"]+)"',
                    r'"csrftoken":"([^"]+)"',
                    r'"csrf_token":"([^"]+)"',
                    r'"x-csrftoken":"([^"]+)"',
                    r'"ig_app_id":"([^"]+)"',
                    r'"app_id":"([^"]+)"',
                    r'"user_id":"([^"]+)"',
                    r'sessionid=([^;]+)',
                    r'csrftoken=([^;]+)'
                ]
                
                extracted_tokens = {}
                for pattern in session_patterns:
                    matches = re.findall(pattern, page_content, re.IGNORECASE)
                    if matches:
                        pattern_name = pattern.split('"')[1] if '"' in pattern else pattern.split('=')[0]
                        extracted_tokens[pattern_name] = matches[0]
                        print(f"   🎯 Found {pattern_name}: {matches[0][:20]}...")
                
                self.session_data['tokens'] = extracted_tokens
                
                # Get request headers
                request_headers = {}
                
                def handle_request(request):
                    if 'instagram.com' in request.url:
                        headers = request.headers
                        for header_name, header_value in headers.items():
                            if any(keyword in header_name.lower() for keyword in ['session', 'csrf', 'auth', 'token', 'id']):
                                request_headers[header_name] = header_value
                
                page.on('request', handle_request)
                
                # Trigger some requests by interacting with the page
                try:
                    await page.reload()
                    await page.wait_for_timeout(2000)
                except:
                    pass
                
                self.session_data['headers'] = request_headers
                
                await browser.close()
                
        except Exception as e:
            print(f"   ❌ Browser session extraction failed: {str(e)}")
    
    def extract_api_session_data(self):
        """🌐 EXTRACT SESSION DATA FROM API CALLS"""
        print("🌐 EXTRACTING API SESSION DATA...")
        
        headers = {
            'User-Agent': 'Instagram 301.0.0.27.111 (iPhone13,2; iOS 17_0; en_US)',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        api_endpoints = [
            "https://www.instagram.com/",
            "https://www.instagram.com/api/v1/web/get_ruling_for_content/",
            "https://i.instagram.com/api/v1/",
            self.target_url
        ]
        
        api_session_data = {}
        
        for endpoint in api_endpoints:
            try:
                response = requests.get(
                    endpoint,
                    headers=headers,
                    timeout=10,
                    proxies={'http': self.mobile_proxy, 'https': self.mobile_proxy}
                )
                
                # Extract session data from response headers
                session_headers = {}
                for header_name, header_value in response.headers.items():
                    if any(keyword in header_name.lower() for keyword in ['session', 'csrf', 'auth', 'token', 'id']):
                        session_headers[header_name] = header_value
                
                # Extract session data from response cookies
                session_cookies = {}
                if response.cookies:
                    for cookie in response.cookies:
                        if any(keyword in cookie.name.lower() for keyword in ['session', 'csrf', 'auth', 'token', 'id']):
                            session_cookies[cookie.name] = cookie.value
                            print(f"   🔑 API Cookie: {cookie.name} = {cookie.value[:20]}...")
                
                # Look for session data in response content
                content_tokens = {}
                if response.text:
                    session_patterns = [
                        r'"sessionid":"([^"]+)"',
                        r'"csrftoken":"([^"]+)"',
                        r'"csrf_token":"([^"]+)"',
                        r'"app_id":"([^"]+)"',
                        r'"client_id":"([^"]+)"'
                    ]
                    
                    for pattern in session_patterns:
                        matches = re.findall(pattern, response.text, re.IGNORECASE)
                        if matches:
                            pattern_name = pattern.split('"')[1]
                            content_tokens[pattern_name] = matches[0]
                            print(f"   🎯 API Token: {pattern_name} = {matches[0][:20]}...")
                
                api_session_data[endpoint] = {
                    'headers': session_headers,
                    'cookies': session_cookies,
                    'content_tokens': content_tokens,
                    'status_code': response.status_code
                }
                
            except Exception as e:
                print(f"   ❌ API extraction failed for {endpoint}: {str(e)}")
        
        self.session_data['api_data'] = api_session_data
    
    def analyze_session_data(self):
        """🔍 ANALYZE EXTRACTED SESSION DATA"""
        print("🔍 ANALYZING SESSION DATA...")
        
        analysis = {
            'session_identifiers': [],
            'csrf_tokens': [],
            'app_identifiers': [],
            'user_identifiers': [],
            'authentication_data': []
        }
        
        # Analyze cookies
        for name, value in self.session_data.get('cookies', {}).items():
            if 'session' in name.lower():
                analysis['session_identifiers'].append({
                    'type': 'cookie',
                    'name': name,
                    'value': value,
                    'length': len(value)
                })
            elif 'csrf' in name.lower():
                analysis['csrf_tokens'].append({
                    'type': 'cookie',
                    'name': name,
                    'value': value,
                    'length': len(value)
                })
            elif any(keyword in name.lower() for keyword in ['app', 'client']):
                analysis['app_identifiers'].append({
                    'type': 'cookie',
                    'name': name,
                    'value': value,
                    'length': len(value)
                })
        
        # Analyze tokens
        for name, value in self.session_data.get('tokens', {}).items():
            if 'session' in name.lower():
                analysis['session_identifiers'].append({
                    'type': 'token',
                    'name': name,
                    'value': value,
                    'length': len(value)
                })
            elif 'csrf' in name.lower():
                analysis['csrf_tokens'].append({
                    'type': 'token',
                    'name': name,
                    'value': value,
                    'length': len(value)
                })
            elif 'user' in name.lower():
                analysis['user_identifiers'].append({
                    'type': 'token',
                    'name': name,
                    'value': value,
                    'length': len(value)
                })
        
        self.session_data['analysis'] = analysis
        
        # Print analysis results
        print("\n🔐 SESSION ANALYSIS RESULTS:")
        print(f"   📊 Session Identifiers: {len(analysis['session_identifiers'])}")
        print(f"   🛡️  CSRF Tokens: {len(analysis['csrf_tokens'])}")
        print(f"   📱 App Identifiers: {len(analysis['app_identifiers'])}")
        print(f"   👤 User Identifiers: {len(analysis['user_identifiers'])}")
        
        # Display found session data
        for session_id in analysis['session_identifiers']:
            print(f"   🔑 {session_id['type'].upper()} Session: {session_id['name']} = {session_id['value'][:50]}...")
        
        for csrf in analysis['csrf_tokens']:
            print(f"   🛡️  {csrf['type'].upper()} CSRF: {csrf['name']} = {csrf['value'][:50]}...")
    
    async def execute_session_extraction(self):
        """🚀 EXECUTE COMPLETE SESSION EXTRACTION"""
        print("=" * 80)
        print("🔐 SESSION ID EXTRACTOR")
        print(f"🎯 TARGET: {self.target}")
        print("🔥 EXTRACTING ALL SESSION DATA")
        print("=" * 80)
        
        # Extract from browser
        await self.extract_browser_session_data()
        print()
        
        # Extract from API
        self.extract_api_session_data()
        print()
        
        # Analyze the data
        self.analyze_session_data()
        
        # Save results
        results_file = f"SESSION_EXTRACTION_{self.target}_{int(time.time())}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.session_data, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 80)
        print("🔐 SESSION EXTRACTION COMPLETE!")
        print(f"📊 Results saved: {results_file}")
        print("🔥 SESSION DATA READY FOR ANALYSIS!")
        print("=" * 80)

if __name__ == "__main__":
    extractor = SessionExtractor()
    asyncio.run(extractor.execute_session_extraction())
