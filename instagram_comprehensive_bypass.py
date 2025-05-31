#!/usr/bin/env python3
"""
🔥 Instagram Comprehensive Bypass System
- Anti Rate-Limiting Strategies
- Multiple Browser Engines  
- Proxy Rotation
- Session Recovery
- Real Browser Simulation
"""

import asyncio
import json
import time
import random
import requests
from datetime import datetime, timedelta
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from playwright.async_api import async_playwright
except ImportError:
    import subprocess
    import sys
    print("📦 Installing playwright...")
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    from playwright.async_api import async_playwright

class InstagramBypassEngine:
    def __init__(self, base_dir="/workspaces/sugarglitch-realops"):
        self.base_dir = Path(base_dir)
        self.sessions_dir = self.base_dir / "sessions"
        self.screenshots_dir = self.base_dir / "screenshots"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        
        # Load proxy configs
        self.proxies = self.load_proxy_configs()
        
        # Rate limiting protection
        self.last_request_time = {}
        self.min_delay_between_requests = 30  # 30 seconds minimum
        
    def load_proxy_configs(self):
        """Load all available proxy configurations"""
        proxies = []
        
        # Try proxy_config_new.json first
        try:
            with open(self.base_dir / "proxy_config_new.json", 'r') as f:
                proxy_data = json.load(f)
                for proxy in proxy_data:
                    if isinstance(proxy, dict) and 'http' in proxy:
                        proxies.append(proxy)
        except Exception as e:
            logger.warning(f"Could not load proxy_config_new.json: {e}")
        
        # Try proxy_config.json
        try:
            with open(self.base_dir / "proxy_config.json", 'r') as f:
                proxy_data = json.load(f)
                if proxy_data.get('enabled') and 'proxies' in proxy_data:
                    for proxy in proxy_data['proxies']:
                        if 'proxy_host' in proxy:
                            proxy_url = f"http://{proxy['proxy_user']}:{proxy['proxy_pass']}@{proxy['proxy_host']}:{proxy['proxy_port']}"
                            proxies.append({
                                'http': proxy_url,
                                'https': proxy_url
                            })
        except Exception as e:
            logger.warning(f"Could not load proxy_config.json: {e}")
        
        logger.info(f"Loaded {len(proxies)} proxy configurations")
        return proxies
    
    async def wait_for_rate_limit(self, domain="instagram.com"):
        """Wait if we're being rate limited"""
        if domain in self.last_request_time:
            time_since_last = time.time() - self.last_request_time[domain]
            if time_since_last < self.min_delay_between_requests:
                wait_time = self.min_delay_between_requests - time_since_last
                logger.info(f"⏳ Waiting {wait_time:.1f}s to avoid rate limiting...")
                await asyncio.sleep(wait_time)
        
        self.last_request_time[domain] = time.time()

    async def get_session_with_requests(self, username, password):
        """Fallback method using requests session"""
        logger.info("🔄 Trying requests-based login...")
        
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Try with different proxies
        for i, proxy in enumerate(self.proxies[:3]):  # Try first 3 proxies
            try:
                logger.info(f"🌐 Trying proxy {i+1}/{len(self.proxies)}")
                
                # Get login page to extract csrf token
                response = session.get('https://www.instagram.com/accounts/login/', 
                                     proxies=proxy, timeout=30)
                
                if response.status_code == 200 and len(response.text) > 1000:
                    logger.info("✅ Successfully loaded login page with requests")
                    
                    # Extract csrf token
                    csrf_token = None
                    if 'csrf_token' in response.text:
                        import re
                        csrf_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
                        if csrf_match:
                            csrf_token = csrf_match.group(1)
                    
                    # Prepare login data
                    login_data = {
                        'username': username,
                        'password': password,
                        'queryParams': '{}',
                        'optIntoOneTap': 'false'
                    }
                    
                    if csrf_token:
                        session.headers['X-CSRFToken'] = csrf_token
                        login_data['csrfmiddlewaretoken'] = csrf_token
                    
                    # Attempt login
                    login_response = session.post(
                        'https://www.instagram.com/accounts/login/ajax/',
                        data=login_data,
                        proxies=proxy,
                        timeout=30
                    )
                    
                    if login_response.status_code == 200:
                        result = login_response.json()
                        if result.get('authenticated'):
                            logger.info("🎉 Requests login successful!")
                            
                            # Extract cookies
                            cookies = {}
                            for cookie in session.cookies:
                                cookies[cookie.name] = cookie.value
                            
                            return cookies
                        
            except Exception as e:
                logger.warning(f"Proxy {i+1} failed: {e}")
                continue
        
        return None

    async def stealth_browser_setup(self, browser, proxy_config=None):
        """Advanced stealth browser configuration"""
        # Create context with stealth settings
        context_args = {
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'viewport': {'width': 1920, 'height': 1080},
            'extra_http_headers': {
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0'
            }
        }
        
        # Add proxy if provided
        if proxy_config and isinstance(proxy_config, dict) and 'http' in proxy_config:
            proxy_url = proxy_config['http']
            if proxy_url.startswith('http://'):
                proxy_parts = proxy_url.replace('http://', '').split('@')
                if len(proxy_parts) == 2:
                    auth, server = proxy_parts
                    username, password = auth.split(':')
                    host, port = server.split(':')
                    
                    context_args['proxy'] = {
                        'server': f'http://{host}:{port}',
                        'username': username,
                        'password': password
                    }
        
        context = await browser.new_context(**context_args)
        
        # Add stealth scripts
        await context.add_init_script("""
            // Remove webdriver traces
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            delete navigator.__proto__.webdriver;
            
            // Mock chrome runtime
            window.chrome = { runtime: {} };
            
            // Override permissions
            navigator.permissions.query = () => Promise.resolve({ state: 'granted' });
            
            // Mock plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [
                    {name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer'},
                    {name: 'Widevine Content Decryption Module', filename: 'widevinecdmadapter.dll'},
                    {name: 'Native Client', filename: 'internal-nacl-plugin'}
                ]
            });
            
            // Randomize canvas fingerprint
            const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
            HTMLCanvasElement.prototype.toDataURL = function() {
                const canvas = this;
                const ctx = canvas.getContext('2d');
                if (ctx) {
                    ctx.fillStyle = `rgba(${Math.random()*255},${Math.random()*255},${Math.random()*255},0.01)`;
                    ctx.fillRect(0, 0, 1, 1);
                }
                return originalToDataURL.apply(this, arguments);
            };
        """)
        
        return context

    async def smart_navigation(self, page, url, retries=3):
        """Smart navigation with anti-detection and retry logic"""
        for attempt in range(retries):
            try:
                logger.info(f"🌐 Navigation attempt {attempt + 1}/{retries} to {url}")
                
                # Wait for rate limiting
                await self.wait_for_rate_limit()
                
                # Navigate with random delay
                await asyncio.sleep(random.uniform(2, 5))
                
                response = await page.goto(url, 
                                         wait_until='domcontentloaded',
                                         timeout=45000)
                
                status_code = response.status if response else 0
                logger.info(f"📊 Response status: {status_code}")
                
                if status_code == 429:
                    wait_time = (attempt + 1) * 60  # Exponential backoff
                    logger.warning(f"⚠️ Rate limited! Waiting {wait_time}s...")
                    await asyncio.sleep(wait_time)
                    continue
                
                # Wait for content
                await page.wait_for_timeout(3000)
                content = await page.content()
                
                if len(content) > 1000 and '<body></body>' not in content:
                    logger.info("✅ Page loaded successfully with content")
                    return True
                else:
                    logger.warning(f"⚠️ Page content too short ({len(content)} chars)")
                    if attempt < retries - 1:
                        await asyncio.sleep(random.uniform(5, 10))
                        continue
                
            except Exception as e:
                logger.error(f"❌ Navigation attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(random.uniform(5, 10))
                    continue
                else:
                    raise
        
        return False

    async def comprehensive_login_attempt(self, username, password):
        """Comprehensive login with multiple strategies"""
        
        # Strategy 1: Requests-based login (fastest)
        logger.info("🚀 Strategy 1: Requests-based login")
        requests_result = await self.get_session_with_requests(username, password)
        if requests_result:
            return requests_result
        
        # Strategy 2: Playwright with proxy rotation
        logger.info("🚀 Strategy 2: Playwright with proxy rotation")
        
        async with async_playwright() as p:
            # Try without proxy first
            browser = await p.chromium.launch(
                headless=True,  # Changed to True for cloud environment
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding',
                    '--disable-dev-shm-usage',
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--disable-gpu',
                    '--enable-features=NetworkService,NetworkServiceLogging',
                    '--disable-features=TranslateUI',
                    '--disable-ipc-flooding-protection'
                ]
            )
            
            try:
                # Try local first
                context = await self.stealth_browser_setup(browser)
                page = await context.new_page()
                
                success = await self.smart_navigation(page, 'https://www.instagram.com/accounts/login/')
                
                if success:
                    result = await self.perform_login(page, username, password)
                    if result:
                        return result
                
                await context.close()
                
                # Try with proxies
                for i, proxy in enumerate(self.proxies[:2]):  # Try first 2 proxies
                    logger.info(f"🌐 Trying proxy {i+1}/{len(self.proxies)}")
                    
                    try:
                        context = await self.stealth_browser_setup(browser, proxy)
                        page = await context.new_page()
                        
                        success = await self.smart_navigation(page, 'https://www.instagram.com/accounts/login/')
                        
                        if success:
                            result = await self.perform_login(page, username, password)
                            if result:
                                return result
                        
                        await context.close()
                        
                    except Exception as e:
                        logger.warning(f"Proxy {i+1} failed: {e}")
                        try:
                            await context.close()
                        except:
                            pass
                        continue
                
            finally:
                await browser.close()
        
        return None

    async def perform_login(self, page, username, password, timeout=30000):
        """Perform actual login on the page"""
        try:
            # Wait for login form
            logger.info("🔍 Waiting for login form...")
            
            selectors_to_try = [
                'input[name="username"]',
                'input[aria-label*="username"]',
                'input[aria-label*="email"]',
                'input[placeholder*="username"]'
            ]
            
            username_input = None
            for selector in selectors_to_try:
                try:
                    await page.wait_for_selector(selector, timeout=10000)
                    username_input = await page.query_selector(selector)
                    if username_input:
                        logger.info(f"✅ Found username input: {selector}")
                        break
                except:
                    continue
            
            if not username_input:
                logger.error("❌ Username input not found")
                return None
            
            # Find password input
            password_selectors = [
                'input[name="password"]',
                'input[type="password"]',
                'input[aria-label*="Password"]'
            ]
            
            password_input = None
            for selector in password_selectors:
                password_input = await page.query_selector(selector)
                if password_input:
                    logger.info(f"✅ Found password input: {selector}")
                    break
            
            if not password_input:
                logger.error("❌ Password input not found")
                return None
            
            # Human-like typing
            logger.info("⌨️ Typing credentials...")
            await username_input.click()
            await asyncio.sleep(random.uniform(0.5, 1.0))
            await username_input.fill('')
            await asyncio.sleep(random.uniform(0.3, 0.7))
            
            for char in username:
                await username_input.type(char)
                await asyncio.sleep(random.uniform(0.05, 0.15))
            
            await asyncio.sleep(random.uniform(0.5, 1.0))
            await password_input.click()
            await asyncio.sleep(random.uniform(0.3, 0.7))
            await password_input.fill('')
            
            for char in password:
                await password_input.type(char)
                await asyncio.sleep(random.uniform(0.05, 0.15))
            
            # Submit form
            await asyncio.sleep(random.uniform(1.0, 2.0))
            
            # Try multiple submit methods
            submit_selectors = [
                'button[type="submit"]',
                'button:has-text("Log in")',
                'button:has-text("Log In")',
                'form button',
                '[role="button"]:has-text("Log")'
            ]
            
            submitted = False
            for selector in submit_selectors:
                try:
                    submit_btn = await page.query_selector(selector)
                    if submit_btn and await submit_btn.is_enabled():
                        await submit_btn.click()
                        logger.info(f"✅ Clicked submit button: {selector}")
                        submitted = True
                        break
                except:
                    continue
            
            if not submitted:
                # Try Enter key
                await password_input.press('Enter')
                logger.info("⌨️ Pressed Enter to submit")
            
            # Wait for navigation or errors
            try:
                await page.wait_for_url(lambda url: 'instagram.com/accounts/login' not in url, timeout=15000)
                logger.info("✅ Successfully navigated away from login page")
                
                # Extract cookies
                cookies = await page.context.cookies()
                cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
                
                if 'sessionid' in cookie_dict:
                    logger.info("🎉 Login successful! Session cookie found")
                    return cookie_dict
                else:
                    logger.warning("⚠️ Navigation occurred but no session cookie found")
                    return None
                    
            except Exception as e:
                # Check if still on login page
                current_url = page.url
                if 'accounts/login' in current_url:
                    logger.error("❌ Login failed - still on login page")
                    
                    # Check for error messages
                    error_selectors = [
                        '[role="alert"]',
                        '.error',
                        '#error',
                        '*:has-text("incorrect")',
                        '*:has-text("wrong")',
                        '*:has-text("try again")'
                    ]
                    
                    for selector in error_selectors:
                        try:
                            error_elem = await page.query_selector(selector)
                            if error_elem:
                                error_text = await error_elem.inner_text()
                                logger.error(f"🚨 Login error: {error_text}")
                                break
                        except:
                            continue
                    
                    return None
                else:
                    logger.info("📍 Navigation completed to different page")
                    cookies = await page.context.cookies()
                    cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
                    return cookie_dict if 'sessionid' in cookie_dict else None
        
        except Exception as e:
            logger.error(f"❌ Login process failed: {e}")
            return None

async def main():
    """Main execution function"""
    username = "alx.trading"
    password = "Fleming654"
    
    print("🔥 Instagram Comprehensive Bypass System")
    print("=" * 60)
    print(f"👤 Username: {username}")
    print(f"🎯 Multiple strategies: Requests + Playwright + Proxy rotation")
    
    bypass_engine = InstagramBypassEngine()
    
    # Attempt comprehensive login
    result = await bypass_engine.comprehensive_login_attempt(username, password)
    
    if result:
        # Save session
        timestamp = int(time.time())
        session_file = bypass_engine.sessions_dir / f"comprehensive_session_{timestamp}.json"
        
        session_data = {
            'sessionid': result.get('sessionid'),
            'ds_user_id': result.get('ds_user_id'),
            'csrftoken': result.get('csrftoken'),
            'mid': result.get('mid'),
            'all_cookies': result,
            'login_timestamp': datetime.now().isoformat(),
            'username': username,
            'method': 'comprehensive_bypass'
        }
        
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"\n🎉 SUCCESS! Comprehensive bypass worked!")
        print(f"💾 Session saved: {session_file}")
        print(f"🔑 SessionID: {result['sessionid'][:20]}...")
        print(f"👤 User ID: {result.get('ds_user_id', 'N/A')}")
        return True
    else:
        print("\n💔 All bypass strategies failed.")
        print("📋 Troubleshooting suggestions:")
        print("   1. Check if Instagram requires 2FA")
        print("   2. Try different proxy providers")
        print("   3. Use different user agent rotation")
        print("   4. Consider manual browser session export")
        return False

if __name__ == "__main__":
    asyncio.run(main())
